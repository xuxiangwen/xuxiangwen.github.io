import csv
import datetime
import logging
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import pickle
import posixpath
import requests
import re
import seaborn as sns
import sys
import tensorflow as tf
import tensorflow_hub as hub
import time

from IPython.lib import kernel
from sklearn.feature_extraction import text
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from tensorflow.keras import preprocessing
from tensorflow.keras import models


class ProgressCounter:
    def __init__(self, total_count, step=0, name=''):
        self.total_count = total_count
        self.count = 0
        self.step = step
        self.name = name

    def add_one(self):
        self.count += 1
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        if self.step==0 or self.count==self.total_count or self.count % self.step == 0:
            sys.stdout.write('%s: %s %d/%d\r' % (current_time, self.name, self.count, self.total_count))


def set_gpu_memory(gpu_memory_limit=None):
    gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
    print('set max gpu memory to {}'.format(gpu_memory_limit))
    for device in gpus:
        tf.config.experimental.set_virtual_device_configuration(
            device,
            [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=gpu_memory_limit)]
        )


def set_gpu_memory_growth(enable=True):
    physical_devices = tf.config.experimental.list_physical_devices('GPU')
    for device in physical_devices:
        tf.config.experimental.set_memory_growth(device, enable)


def get_notebook_name(host='127.0.0.1', port='8888', password='xxw'):
    connection_file_path = kernel.get_connection_file()
    connection_file = os.path.basename(connection_file_path)
    kernel_id = connection_file.split('-', 1)[1].split('.')[0]

    base_url = 'http://{0}:{1}/'.format(host, port)
    url = base_url + 'login?next=%2F'
    s = requests.Session()
    resp = s.get(url)
    xsrf_cookie = resp.cookies['_xsrf']
    params = {'_xsrf': xsrf_cookie, 'password': password}
    res = s.post(url, data=params)
    url = posixpath.join(base_url, 'api', 'sessions')
    ret = s.get(url)
    notebooks = json.loads(ret.text)

    kernel_ids = [notebook['kernel']['id'] for notebook in notebooks]
    notebook_names = [os.path.basename(notebook['path']) for notebook in notebooks]

    index = kernel_ids.index(kernel_id)
    return notebook_names[index]


class ObjectPickle(object):
    @classmethod
    def save(cls, path, object_):
        parent_path = os.path.dirname(path)
        if not os.path.exists(parent_path):
            os.makedirs(parent_path)

        with open(path, 'wb') as output:
            pickle.dump(object_, output, pickle.HIGHEST_PROTOCOL)
        print('save object to {}'.format(path))

    @classmethod
    def load(cls, path):
        with open(path, 'rb') as input_:
            object_ = pickle.load(input_)
        return object_


class JsonPickle(object):
    @classmethod
    def save(cls, path, object_):
        parent_path = os.path.dirname(path)
        if not os.path.exists(parent_path):
            os.makedirs(parent_path)

        with open(path, 'w') as output:
            output.write(json.dumps(object_))
        print('save json to {}'.format(path))

    @classmethod
    def load(cls, path):
        with open(path, 'r') as input_:
            content = input_.read()
            object_ = json.loads(content)
        return object_


def get_weight_num(obj):
    """得到模型或layer可训练参数的个数"""
    return np.sum([np.prod(p.shape) for p in obj.trainable_weights]).item()


def show_tree(path, max_depth=10, max_num=100):
    def _show_tree(path, depth, max_num, prefix):
        if max_num<=0 or depth>max_depth:
            return max_num
        if depth == 1:
            print(path)
            max_num = max_num - 1
        items = os.listdir(path)
        for i, item in enumerate(items):
            if max_num<=0: return max_num
            new_item = path + '/' + item
            if i == len(items)-1:
                print(prefix  + "└──" + item)
                new_prefix = prefix+"    "
            else:
                print(prefix  + "├──" + item)
                new_prefix = prefix+"│   "
            max_num = max_num-1
            if os.path.isdir(new_item):
                max_num = _show_tree(new_item, depth=depth+1, max_num=max_num, prefix=new_prefix)
        return max_num
    _show_tree(path, depth=1, max_num=max_num, prefix="")


def load_data(text_file, use_augument=False):
    if use_augument:
        names = ['id', 'owner', 'label', 'train_test_flag', 'snps_comment_origin','snps_comment',
                 'support_attribute_comment_origin', 'support_attribute_comment', 'key_words', 'snps_score',
                 'main_symptom_new', 'area', 'survey_language', 'case_id',
                 'cs_response_date', 'main_symptom',
                 'snps_sa_comments_origin', 'snps_sa_comments', 'label_id',
                 'augument_count', 'augment_language']
        dtypes = [np.str, np.str, np.str, np.str, np.str, np.str,
                  np.str, np.str, np.str, np.int,
                  np.str, np.str, np.str, np.str,
                  np.str, np.str,
                  np.str, np.str, np.int,
                  np.int, np.str]
    else:
        names = ['id', 'owner', 'label', 'train_test_flag', 'snps_comment_origin', 'snps_comment',
                 'support_attribute_comment_origin', 'support_attribute_comment', 'key_words', 'snps_score',
                 'main_symptom_new', 'area', 'survey_language', 'case_id',
                 'cs_response_date', 'main_symptom',
                 'snps_sa_comments_origin', 'snps_sa_comments', 'label_id']
        dtypes = [np.str, np.str, np.str, np.str, np.str, np.str,
                  np.str, np.str, np.str, np.int,
                  np.str, np.str, np.str, np.str,
                  np.str, np.str,
                  np.str, np.str, np.int]
    dtypes = {name:dtype for name, dtype in zip(names, dtypes)}
    df = pd.read_table(text_file, names=names, dtype=dtypes, quoting=csv.QUOTE_NONE, skiprows=1)
    df.index = df.id
    classes = list(df.label.sort_values(ascending=True).unique())
    print('loading {} records from {}'.format(len(df), text_file))
    return df, classes


def get_data_result(text_file):
    names = ['id', 'owner', 'label', 'train_test_flag', 'snps_comment_origin', 'snps_comment',
             'support_attribute_comment_origin', 'support_attribute_comment', 'key_words', 'snps_score',
             'main_symptom_new', 'area', 'survey_language', 'case_id',
             'cs_response_date', 'main_symptom',
             'snps_sa_comments_origin',  'snps_sa_comments', 'label_id',
             'top1_predict_label', 'top2_predict_label',
             'top1_predict_correct', 'top2_predict_correct']
    dtypes = [np.str, np.str, np.str, np.str, np.str, np.str,
              np.str, np.str, np.str, np.int,
              np.str, np.str, np.str,  np.str,
              np.str, np.str,
              np.str, np.str, np.int,
              np.str, np.str,
              np.str, np.str
              ]
    dtypes = {name:dtype for name, dtype in zip(names, dtypes)}
    df = pd.read_table(text_file, names=names, dtype=dtypes, quoting=csv.QUOTE_NONE, skiprows=1)
    df.index = df.id
    df['cs_response_date'] = pd.to_datetime(df['cs_response_date']).apply(
        lambda x: datetime.datetime.strftime(x, format='%Y-%m-%d'))
    names = ['id', 'owner', 'main_symptom', 'label', 'train_test_flag', 'snps_comment_origin', 'snps_comment',
             'support_attribute_comment_origin', 'support_attribute_comment', 'key_words', 'snps_score',
             'main_symptom_new', 'area', 'survey_language', 'case_id',
             'cs_response_date',
             'top1_predict_label', 'top2_predict_label',
             'top1_predict_correct', 'top2_predict_correct',
             'snps_sa_comments', 'label_id']
    df = df[names]
    print('loading {} records from {}'.format(len(df), text_file))
    return df


def get_texts(df):
    def get_text(i, row):
        # print('-'*50, i, '-'*50)
        survey_language = row['Survey language']

        snps_comment = row['sNPS Comment']
        snps_comment = str(snps_comment) if pd.notna(snps_comment) else ''
        support_attribute_comment = row['Support Attribute Comment']
        support_attribute_comment = str(support_attribute_comment) if pd.notna(support_attribute_comment) else ''

        snps_comment_en = row['Translation to English for: Assisted Support - sNPS Comment']
        snps_comment_en = str(snps_comment_en) if pd.notna(snps_comment_en) else ''
        support_attribute_comment_en = row['Translation to English for: Assisted Support - Key Metric Comment']
        support_attribute_comment_en = str(support_attribute_comment_en) if pd.notna(
            support_attribute_comment_en) else ''
        snps_score = row['sNPS Score']

        lack_english = False
        status = 'classified'
        if snps_score >= 9:
            status = 'promoter'

        if not survey_language.lower().startswith('english') and status=='classified':
            if snps_comment.strip() != "" and snps_comment_en.strip() == '':
                status = 'lack of english text'
            elif support_attribute_comment.strip() != "" and support_attribute_comment_en.strip() == '':
                status = 'lack of english text'
            else:
                snps_comment = snps_comment_en
                support_attribute_comment = support_attribute_comment_en

        text = snps_comment + '' if support_attribute_comment == '' else '|' + support_attribute_comment
        if len(text) <= 3:
            status = 'no comment'
        return text, status, i

    results = [get_text(i, row) for i, row in df.iterrows()]
    texts = [text for text, _, _ in results]
    status = [status for _, status, _ in results]
    lack_english_rows = [i for _, status, i in results if status == 'lack of english text']
    promoter_rows = [i for _, status, i in results if status == 'promoter']
    no_comment_rows = [i for _, status, i in results if status == 'no comment']
    return texts, status, lack_english_rows, promoter_rows, no_comment_rows


def get_train_test(df, column, use_augument=False):
    if use_augument:
        df_train = df.loc[(df.train_test_flag == 'train') | (df.train_test_flag == 'augument')]
    else:
        df_train = df.loc[df.train_test_flag == 'train']
    df_test = df.loc[df.train_test_flag == 'test']

    train_texts = list(df_train[column].fillna(''))
    train_labels = np.array(df_train.label_id)

    test_texts = list(df_test[column].fillna(''))
    test_labels = np.array(df_test.label_id)

    return (train_texts, train_labels), (test_texts, test_labels)


def clean_texts(texts):
    def clean(text_):
        text_ = text_.strip().lower()
        # add space between punctuation
        text_ = re.sub(r'([.\\!?,\'/()\[\]":|;])', r' \1 ', text_)
        # remove characters except for English letters and some punctuations
        text_ = re.sub(r"[^A-Za-z\.\-\?\!\,\#\@\% ]", "", text_)
        # remove extra spaces
        text_ = re.sub(r'[" "]+', " ", text_)
        return text_

    texts = [clean(text_) for text_ in texts]
    return texts


class FastText:
    def __init__(self, classes):
        self.classes = classes
        self.no_blank_classes = [class_.replace(' ', '-').replace('/', '_') for class_ in classes]

    @classmethod
    def text_clean(cls, texts):
        texts = clean_texts(texts)
        return texts

    def save_file(self, texts, labels, file_path):
        def get_no_blank_class(label):
            return self.no_blank_classes[label]

        texts = self.text_clean(texts)
        ft_texts = ['__label__{}'.format(get_no_blank_class(label)) + ' ' + text
                    for text, label in zip(texts, labels)]
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        with open(file_path, 'w') as f:
            for text in ft_texts:
                f.write(text + '\n')
        print('save texts into {}'.format(file_path))

    def predict(self, model, texts, k=1):
        texts = self.text_clean(texts)
        return model.predict(texts, k)

    def save_model(self, model, model_name, save_path):
        save_model_path = os.path.join(save_path, '{}.bin'.format(model_name))
        save_vector_path = os.path.join(save_path, '{}.vec'.format(model_name))
        projector_vector_path = os.path.join(save_path, '{}_vec.tsv'.format(model_name))
        projector_meta_path = os.path.join(save_path, '{}_meta.tsv'.format(model_name))

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        print('saving model to ' + save_model_path)
        model.save_model(save_model_path)

        with open(save_vector_path, 'w') as vector_file:
            print('generating ' + save_vector_path)
            vector_file.write(str(len(model.words)) + " " + str(model.get_dimension()) + "\n")
            for w in model.words:
                vector = model.get_word_vector(w)
                vstr = ' '.join([str(vi) for vi in vector])
                vector_file.write(w + ' ' + vstr + '\n')

        with open(projector_vector_path, 'w') as projector_vector_file:
            print('generating ' + projector_vector_path)
            for i, w in enumerate(model.words):
                if i != 0:
                    projector_vector_file.write('\n')
                vector = model.get_word_vector(w)
                projector_vector_file.write('\t'.join([str(vi) for vi in vector]))

        with open(projector_meta_path, 'w') as projector_meta_file:
            print('generating ' + projector_meta_path)
            for i, w in enumerate(model.words):
                if i != 0:
                    projector_meta_file.write('\n')
                projector_meta_file.write(w)
        return save_model_path, save_vector_path, projector_vector_path, projector_meta_path


def load_model(checkpoint_path):
    print('loading model from {}'.format(checkpoint_path))
    model = models.load_model(checkpoint_path, custom_objects={'tf': tf})
    return model


def load_vectorizer(vectorizer_path):
    if pd.isna(vectorizer_path): return None
    print('loading load_vectorizer from {}'.format(vectorizer_path))
    with open(vectorizer_path, 'rb') as input_:
        vectorizer = pickle.load(input_)
    return vectorizer


def get_model_results(base_path):
    print('getting model_results for {}'.format(base_path))
    result_files = []
    for file_name in os.listdir(base_path):
        notebook_path = os.path.join(base_path, file_name)
        if os.path.isdir(notebook_path):
            result_files = result_files + [os.path.join(notebook_path, notebook_file_name)
                                           for notebook_file_name in os.listdir(notebook_path)
                                           if notebook_file_name == 'model_results.json']
    model_results = []
    for result_file in result_files:
        with open(result_file, 'r') as input_:
            content = input_.read()
            model_results = model_results + json.loads(content)

    df_model_results = pd.DataFrame(model_results)
    df_model_results = df_model_results.sort_values('test_accuracy', ascending=False)
    df_model_results.index = range(1, len(df_model_results) + 1)
    df_model_results['id'] = df_model_results.index
    print(df_model_results.columns)
    columns = ['id', 'model_name', 'dataset_name', 'classes', 'program_name', 'train_loss', 'train_accuracy',
               'test_loss', 'test_accuracy', 'test_top2_accuracy',
               'weight_number', 'checkpoint_path', 'vectorizer_path',
               'predictor_path', 'train_time', 'text_column']
    df_model_results = df_model_results[columns]
    return df_model_results


def get_best_predictor(base_path, root_path_replace=None):
    print('getting the best predictor for {}'.format(base_path))
    df_model_results = get_model_results(base_path)
    row = df_model_results.iloc[0]

    predictor_path = row['predictor_path']
    if root_path_replace is not None:
        predictor_path = root_path_replace(predictor_path)
    predictor = load_predictor(predictor_path, root_path_replace)
    return predictor


def load_predictor(predictor_path, root_path_replace=None):
    if pd.isna(predictor_path):
        return None
    print('loading predictor from {}'.format(predictor_path))
    with open(predictor_path, 'rb') as input_:
        predictor = pickle.load(input_)
        predictor.load(root_path_replace)
    return predictor


def plot_confusion_matrix(predictions, labels, classes):
    def plot_cm():

        cm = confusion_matrix(labels, predictions)
        bin_count = np.bincount(labels)

        if classes is None:
            index = range(len(bin_count))
            columns = range(len(bin_count))
        else:
            classes_ = [_class[0:15] for _class in classes]
            index = classes_
            columns = classes_

        df_cm = pd.DataFrame(cm, index=index, columns=columns)

        plt.title("{} - Confusion matrix".format('fasttext'))
        sns.heatmap(df_cm, annot=True, fmt='g', cmap='coolwarm')
        if classes is not None:
            plt.yticks(rotation=0)
            plt.xticks(rotation=45)
        plt.xlabel("Predicted")
        plt.ylabel("Actual")

    height = min(6, len(classes) * 2)

    plt.figure(figsize=(height + 1, height))
    plot_cm()

    plt.show()


def get_top_prediction(predictions, labels, k=1):
    topk_predictions = np.array([labels[i] if labels[i] in list(predictions[i].argsort()[-k:][::-1])
                                 else predictions[i].argmax() for i in range(len(labels))])
    return topk_predictions


def get_top12_probabilities(predictions, classes, status):
    def get_top12_probability(i, prediction):
        if status[i] == 'no comment':
            return 'No Customer Feedback', 1.0, None, None
        if status[i] != 'classified':
            return None, None, None, None

        indexes = prediction.argsort()[-2:][::-1]
        top1_class = classes[indexes[0]]
        top1_probability = prediction[indexes[0]]
        top2_class = classes[indexes[1]]
        top2_probability = prediction[indexes[1]]
        return top1_class, top1_probability, top2_class, top2_probability

    results = [get_top12_probability(i, prediction) for i, prediction in enumerate(predictions)]
    top1_class = [item for item, _, _, _ in results]
    top1_probability = [item for _, item, _, _ in results]
    top2_class = [item for _, _, item, _ in results]
    top2_probability = [item for _, _, _, item in results]
    return top1_class, top1_probability, top2_class, top2_probability


def score(predictions, labels, classes):
    def score_(y_pred, y):
        tp = np.sum((y_pred == 1) * (y == 1)) * 1.0
        fn = np.sum((y_pred == 0) * (y == 1)) * 1.0
        fp = np.sum((y_pred == 1) * (y == 0)) * 1.0
        tn = np.sum((y_pred == 0) * (y == 0)) * 1.0

        recall = tp / (tp + fn) if tp > 0 else 0
        precision = tp / (tp + fp) if tp > 0 else 0
        specificity = tn / (tn + fp) if tn > 0 else 0
        f1 = 2 * recall * precision / (recall + precision) if recall + precision > 0 else 0

        return precision, recall, f1

    scores = []
    for i in range(len(classes)):
        y = np.array([1 if label == i else 0 for label in labels])
        y_pred = np.array([1 if pred == i else 0 for pred in predictions])

        scores.append(score_(y_pred, y))

    df_scores = pd.DataFrame(scores, columns=['precision', 'recall', 'f1'], index=classes)
    return df_scores


def save_prediction_results(df, text_column, predictor, result_path,
                            error_sample_path, error_sample_count=None):
    df = df.copy()
    texts = texts = list(df[text_column].fillna(''))
    label_ids = np.array(df.label_id)

    predictions = predictor.predict(texts)

    top2_label_ids = [list(predictions[i].argsort()[-2:][::-1]) for i in range(len(texts))]
    df['top1_predict_label'] = [predictor.classes[ids[0]] for ids in top2_label_ids]
    df['top2_predict_label'] = [predictor.classes[ids[1]] for ids in top2_label_ids]
    df['top1_predict_correct'] = ['yes' if label_ids[i] == ids[0] else 'no' for i, ids in enumerate(top2_label_ids)]
    df['top2_predict_correct'] = ['yes' if label_ids[i] in ids else 'no' for i, ids in enumerate(top2_label_ids)]

    print('saving data to {}'.format(result_path))
    df.to_csv(result_path, sep='\t', index=False)

    print('saving data to {}'.format(error_sample_path))
    df_error_sample = df.loc[(df.train_test_flag == 'test') & (df.top1_predict_correct == 'no')].copy()
    if error_sample_count is not None:
        df_error_sample = df_error_sample.sample(n=error_sample_count)
    df_error_sample.to_csv(error_sample_path, sep=',', index=False)
    return df, df_error_sample


def get_embedding_matrix(embeddings_index, vector_size, tokenizer, max_features):
    word_index = tokenizer.word_index
    embedding_matrix = np.zeros((min(max_features, len(word_index)), vector_size))
    missing_words = {}
    match_count = 0
    for word, i in word_index.items():
        if i >= max_features: continue
        vector = embeddings_index.get(word)
        if vector is not None:
            embedding_matrix[i] = vector
            match_count = match_count + 1
        else:
            missing_words[word] = tokenizer.word_counts[word]
    print('embedding_matrix.shape: {}'.format(embedding_matrix.shape))
    print('match cout: {}'.format(match_count))
    print('missing word cout: {}'.format(len(missing_words)))
    return embedding_matrix


def load_embedding(embedding_file, max_length=200000, ignore_rows=0):
    embedding_index = {}
    with open(embedding_file) as f:
        i = 0
        for line in f:
            i = i + 1
            values = line.split()
            if i <= ignore_rows or len(values) < 20:
                continue
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            embedding_index[word] = coefs
            if i > max_length: break
    vector_size = len(coefs)
    print('Loaded %s word vectors. the vector size is %s' % (len(embedding_index), vector_size))
    return embedding_index, vector_size


def load_embedding_matrix(embedding_files, tokenizer, max_features, max_length=200000, ignore_rows=1):
    if not isinstance(embedding_files, list):
        embedding_files = [embedding_files]

    embedding_matrixs = []
    for embedding_file in embedding_files:
        print('-' * 100)
        embedding_index, vector_size = load_embedding(embedding_file, max_length)
        embedding_matrix = get_embedding_matrix(embedding_index, vector_size,
                                                tokenizer, max_features)
        embedding_matrixs.append(embedding_matrix)
    embedding_matrix = np.hstack(embedding_matrixs)
    return embedding_matrix


class TaskTime:
    """用于显示执行时间"""

    def __init__(self, task_name, show_start=False):
        super().__init__()
        self.show_start = show_start
        self.task_name = task_name
        self.start_time = time.time()

    def elapsed_time(self):
        return time.time()-self.start_time

    def __enter__(self):
        if self.show_start:
            logging.info('start {}'.format(self.task_name))
        return self;

    def __exit__(self, exc_type, exc_value, exc_tb):
        time.sleep(0.5)
        logging.info('finish {} [elapsed time: {:.2f} seconds]'.format(self.task_name, self.elapsed_time()))


class Vectorizer(object):
    def __init__(self):
        super().__init__()

    def fit(self, texts):
        return self

    def transform(self, texts):
        return texts

    @classmethod
    def text_clean(self, texts):
        return clean_texts(texts)


class RawVectorizer(Vectorizer):
    def __init__(self):
        super().__init__()

    def transform(self, texts):
        texts = self.text_clean(texts)
        return np.array(texts)


class TransferVectorizer(Vectorizer):
    def __init__(self, module_path, max_length):
        super().__init__()
        self.module_path = module_path
        self.max_length = max_length
        self.transfer_layer = hub.KerasLayer(self.module_path, trainable=False, dtype=tf.string)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["transfer_layer"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.transfer_layer = hub.KerasLayer(self.module_path, trainable=False, dtype=tf.string)

    @classmethod
    def transform_(cls, texts, transfer_layer, max_length=250):
        def split(text):
            return text.split(' ')

        def embedding(words):
            return transfer_layer(words).numpy()

        def filter_(vectors):
            return len(vectors) <= max_length

        def padding(vectors):
            if len(vectors) < max_length:
                left_padding = max(0, max_length - len(vectors))
                paddings = [[left_padding, 0], [0, 0]]
                vectors = np.pad(vectors, paddings, "constant")
            else:
                vectors = vectors[0:max_length]
            return vectors

        def transform_(text_):
            words = split(text_)
            vectors = embedding(words)
            vectors = padding(vectors)
            return vectors

        vectors = np.array([transform_(text_) for text_ in texts])
        return vectors

    def transform(self, texts):
        texts = self.text_clean(texts)
        vectors = self.transform_(texts, self.transfer_layer, self.max_length)
        return vectors


class SequenceVectorizer(Vectorizer):
    def __init__(self):
        super().__init__()
        self.tokenizer = None
        self.max_sequence_length = None

    def fit(self, train_texts, max_sequence_length, num_words=None, filters=''):
        # filters = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'

        train_texts = self.text_clean(train_texts)

        tokenizer = preprocessing.text.Tokenizer(num_words=num_words, filters=filters)
        tokenizer.fit_on_texts(train_texts)

        # Vectorize training and validation texts.
        train_sequences = tokenizer.texts_to_sequences(train_texts)

        # Get max sequence length.
        max_sequence_length = min(len(max(train_sequences, key=len)), max_sequence_length)
        self.tokenizer = tokenizer
        self.max_sequence_length = max_sequence_length

        return self

    def transform(self, texts):
        texts = self.text_clean(texts)
        sequences = self.tokenizer.texts_to_sequences(texts)
        sequences = preprocessing.sequence.pad_sequences(sequences, maxlen=self.max_sequence_length)
        return sequences


class MultiSelectKBest(object):
    def __init__(self, score_func=f_classif, k=10):
        super().__init__()
        self.score_func = score_func
        self.k = k
        self.pvalues_ = None
        self.scores_ = None

    def fit(self, X, y):
        scores = []
        pvalues = []
        for j in range(y.shape[1]):
            selector = SelectKBest(self.score_func, k='all')
            selector.fit(X, y[:, j])
            scores.append(list(selector.scores_))
            if selector.pvalues_ is not None:
                pvalues.append(list(selector.pvalues_))

        self.scores_ = np.mean(scores, axis=0)
        if len(pvalues) > 0:
            self.pvalues_ = np.mean(pvalues, axis=0)
        else:
            self.pvalues_ = None

        return self

    def transform(self, X):
        if self.k == 'all':
            return X
        scores = self.scores_
        indexes = np.argsort(scores, kind="mergesort")[-self.k:]
        indexes.sort()
        return X[:, indexes]

    def fit_transform(self, X, y):
        self.fit(X, y)
        return self.transform(X)


class NgramVectorizer(Vectorizer):
    def __init__(self):
        super().__init__()
        self.vectorizer = None
        self.selector = None

    def fit(self, train_texts, train_labels=None, top_k=None, ngram_range=(1, 2),
            token_mode='word', min_document_frequency=2, stop_words=None):

        train_texts = self.text_clean(train_texts)

        kwargs = {
            'ngram_range': ngram_range,  # Use 1-grams + 2-grams.
            'dtype': 'int32',
            'strip_accents': 'unicode',
            'decode_error': 'replace',
            'analyzer': token_mode,  # Split text into word tokens.
            'min_df': min_document_frequency,
            'stop_words': stop_words
        }

        vectorizer = text.TfidfVectorizer(**kwargs)
        train_ngrams = vectorizer.fit_transform(train_texts)

        # Select top 'k' of the vectorized features.
        if top_k > 0 and train_labels is not None:
            if len(train_labels.shape) == 1:
                selector = SelectKBest(f_classif, k=min(top_k, train_ngrams.shape[1]))
            else:
                selector = MultiSelectKBest(f_classif, k=min(top_k, train_ngrams.shape[1]))
            selector.fit(train_ngrams, train_labels)
        else:
            selector = None

        self.vectorizer = vectorizer
        self.selector = selector
        return self

    def transform(self, texts):
        texts = self.text_clean(texts)
        ngrams = self.vectorizer.transform(texts)
        if self.selector is not None:
            ngrams = self.selector.transform(ngrams).astype('float32')
        return ngrams

