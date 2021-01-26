import logging
import json
import numpy as np
import os
import pickle
import tensorflow as tf
import time

from sklearn.feature_extraction import text
from sklearn.feature_selection import SelectKBest, f_classif
from tensorflow.keras import preprocessing


def set_gpu_memory(gpu_memory_limit=None):
    gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
    print('set max gpu memory to {}'.format(gpu_memory_limit))
    tf.config.experimental.set_virtual_device_configuration(
        gpus[0],
        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=gpu_memory_limit)]
    )


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
    def apply(self, data):
        pass


class SequenceVectorizer(Vectorizer):
    def __init__(self):
        super().__init__()
        self.tokenizer = None
        self.max_sequence_length = None

    def fit(self, train_texts, max_sequence_length, num_words=None):
        tokenizer = preprocessing.text.Tokenizer(num_words=num_words)
        tokenizer.fit_on_texts(train_texts)

        # Vectorize training and validation texts.
        train_sequences = tokenizer.texts_to_sequences(train_texts)

        # Get max sequence length.
        max_sequence_length = min(len(max(train_sequences, key=len)), max_sequence_length)
        self.tokenizer = tokenizer
        self.max_sequence_length = max_sequence_length

        return self

    def transform(self, texts):
        sequences = self.tokenizer.texts_to_sequences(texts)
        sequences = preprocessing.sequence.pad_sequences(sequences, maxlen=self.max_sequence_length)
        return sequences


class NgramVectorizer(Vectorizer):
    def __init__(self):
        super().__init__()
        self.vectorizer = None
        self.selector = None

    def fit(self, train_texts, train_labels=None, top_k=None, ngram_range=(1, 2),
            token_mode='word', min_document_frequency=2, stop_words=None):
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
            selector = SelectKBest(f_classif, k=min(top_k, train_ngrams.shape[1]))
            selector.fit(train_ngrams, train_labels)
        else:
            selector = None

        self.vectorizer = vectorizer
        self.selector = selector
        return self

    def transform(self, texts):
        ngrams = self.vectorizer.transform(texts)
        if self.selector is not None:
            ngrams = self.selector.transform(ngrams).astype('float32')
        return ngrams
