#!/usr/bin/env python

import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import scipy
import seaborn as sns
import tensorflow as tf
import time

from IPython.display import display, Image
from sklearn.feature_extraction import text
from sklearn.metrics import confusion_matrix
from sklearn.feature_selection import SelectKBest, f_classif
from tensorflow import keras
from tensorflow.keras import preprocessing, datasets
from tensorflow.keras import losses, optimizers, regularizers
from sklearn.model_selection import train_test_split

# 设置日志
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)


def set_gpu_memory(gpu_memory_limit=None):
    gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
    print('set max gpu memory to {}'.format(gpu_memory_limit))
    tf.config.experimental.set_virtual_device_configuration(
        gpus[0],
        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=gpu_memory_limit)]
    )


def plot_model_structure(model):
    """打印模型的结构"""
    img = tf.keras.utils.plot_model(model, '{}.png'.format(model.name), show_shapes=True)
    display(img)


def get_weight_num(obj):
    """得到模型或layer可训练参数的个数"""
    return np.sum([np.prod(p.shape) for p in obj.trainable_weights])


def sequence_vectorize(train_texts, val_texts, top_k, max_sequence_length):
    """Vectorizes texts as sequence vectors.

    1 text = 1 sequence vector with fixed length.

    # Arguments
        train_texts: list, training text strings.
        val_texts: list, validation text strings.

    # Returns
        x_train, x_val, word_index: vectorized training and validation
            texts and word index dictionary.
    """
    # Create vocabulary with training texts.
    tokenizer = preprocessing.text.Tokenizer(num_words=top_k)
    tokenizer.fit_on_texts(train_texts)

    # Vectorize training and validation texts.
    x_train = tokenizer.texts_to_sequences(train_texts)
    x_val = tokenizer.texts_to_sequences(val_texts)

    # Get max sequence length.
    max_length = len(max(x_train, key=len))
    if max_length > max_sequence_length:
        max_length = max_sequence_length

    # Fix sequence length to max value. Sequences shorter than the length are
    # padded in the beginning and sequences longer are truncated
    # at the beginning.
    x_train = preprocessing.sequence.pad_sequences(x_train, maxlen=max_length)
    x_val = preprocessing.sequence.pad_sequences(x_val, maxlen=max_length)
    return x_train, x_val, tokenizer


def ngram_vectorize(train_texts, train_labels, val_texts, top_k, ngram_range=(1, 2),
                    token_mode='word', min_document_frequency=2, stop_words=None):
    """Vectorizes texts as n-gram vectors.

    1 text = 1 tf-idf vector the length of vocabulary of unigrams + bigrams.

    # Arguments
        train_texts: list, training text strings.
        train_labels: np.ndarray, training labels.
        val_texts: list, validation text strings.

    # Returns
        x_train, x_val: vectorized training and validation texts
    """
    # Create keyword arguments to pass to the 'tf-idf' vectorizer.
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

    # Learn vocabulary from training texts and vectorize training texts.
    x_train = vectorizer.fit_transform(train_texts)
    print('before SelectKBest, the shape of train data is {}'.format(x_train.shape))

    # Vectorize validation texts.
    x_val = vectorizer.transform(val_texts)

    # Select top 'k' of the vectorized features.
    selector = SelectKBest(f_classif, k=min(top_k, x_train.shape[1]))
    selector.fit(x_train, train_labels)
    x_train = selector.transform(x_train).astype('float32')
    x_val = selector.transform(x_val).astype('float32')

    print('After SelectKBest, the shape of train data is {}'.format(x_train.shape))

    return x_train, x_val, vectorizer


def show_tree(path, max_depth=10, max_num=100):
    def _show_tree(path, depth, max_num, prefix):
        if max_num<=0 or depth>max_depth:
            return max_num
        if depth==1: 
            print(path)
            max_num=max_num-1
        items = os.listdir(path)
        for i, item in enumerate(items):
            if max_num<=0: return max_num
            newitem = path +'/'+ item
            if i==len(items)-1:
                print(prefix  + "└──" + item)            
                new_prefix = prefix+"    "                
            else:
                print(prefix  + "├──" + item)
                new_prefix = prefix+"│   "
            max_num=max_num-1
            if os.path.isdir(newitem):
                max_num = _show_tree(newitem, depth=depth+1, max_num=max_num, prefix=new_prefix)         
        return max_num
    _show_tree(path, depth=1, max_num=max_num, prefix="")


def plot_history(history):
    """显示训练的loss和accuracy的走势图"""
    plt.figure(figsize=(16, 5))
    max_epoch = len(history.history['accuracy'])
    epochs = range(1, max_epoch+1)
    if max_epoch <= 20:
        xticks = range(0, max_epoch+1)
    else:
        xticks = range(0, max_epoch+1, (max_epoch-1)//20+1)
    plt.subplot(121)
    plt.plot(epochs, history.history['accuracy'])
    plt.plot(epochs, history.history['val_accuracy'])
    plt.title('Accuracy vs. epochs')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.xticks(xticks)
    plt.legend(['Training', 'Validation'], loc='lower right')

    plt.subplot(122)
    plt.plot(epochs, history.history['loss'])
    plt.plot(epochs, history.history['val_loss'])
    plt.title('Loss vs. epochs')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.xticks(xticks)
    plt.legend(['Training', 'Validation'], loc='upper right')
    plt.show()


def plot_frequency_distribution(train_texts, test_texts=None, stop_words=text.ENGLISH_STOP_WORDS.union(["br"])):
    def plot_frequency_distribution_of_ngrams(sample_texts,
                                              ngram_range=(1, 2),
                                              num_ngrams=50,
                                              title=''
                                              ):
        """Plots the frequency distribution of n-grams.
        # Arguments
            samples_texts: list, sample texts.
            ngram_range: tuple (min, mplt), The range of n-gram values to consider.
                Min and mplt are the lower and upper bound values for the range.
            num_ngrams: int, number of n-grams to plot.
                Top `num_ngrams` frequent n-grams will be plotted.
        """
        # Create args required for vectorizing.
        kwargs = {
            'ngram_range': (1, 1),
            'dtype': 'int32',
            'strip_accents': 'unicode',
            'decode_error': 'replace',
            'analyzer': 'word',  # Split text into word tokens.
            'stop_words': stop_words
        }
        vectorizer = text.CountVectorizer(**kwargs)

        # This creates a vocabulary (dict, where keys are n-grams and values are
        # idxices). This also converts every text to an array the length of
        # vocabulary, where every element idxicates the count of the n-gram
        # corresponding at that idxex in vocabulary.
        vectorized_texts = vectorizer.fit_transform(sample_texts)

        # This is the list of all n-grams in the index order from the vocabulary.
        all_ngrams = list(vectorizer.get_feature_names())
        num_ngrams = min(num_ngrams, len(all_ngrams))
        # ngrams = all_ngrams[:num_ngrams]

        # Add up the counts per n-gram ie. column-wise
        all_counts = vectorized_texts.sum(axis=0).tolist()[0]

        # Sort n-grams and counts by frequency and get top `num_ngrams` ngrams.
        all_counts, all_ngrams = zip(*[(c, n) for c, n in sorted(
            zip(all_counts, all_ngrams), reverse=True)])
        ngrams = list(all_ngrams)[:num_ngrams]
        counts = list(all_counts)[:num_ngrams]

        idx = np.arange(num_ngrams)
        plt.bar(idx, counts, width=0.8, color='b')
        plt.xlabel('N-grams')
        plt.ylabel('Frequencies')
        plt.title('{} Frequency distribution of n-grams'.format(title))
        plt.xticks(idx, ngrams, rotation=45)

    if test_texts is None:
        plt.figure(figsize=(16, 6))
        plot_frequency_distribution_of_ngrams(train_texts, title='Train')
        plt.show()
    else:
        plt.figure(figsize=(16, 12))
        plt.subplot(211)
        plot_frequency_distribution_of_ngrams(train_texts, title='Train')
        plt.subplot(212)
        plot_frequency_distribution_of_ngrams(test_texts, title='Test')
        plt.show()


def plot_length_distribution(train_text_lengths, test_text_lengths):
    def plot_length_dist(lengths, title):
        median = np.median(lengths)
        plt.hist(lengths, 50)
        plt.axvline(x=median, color='coral', linestyle='dashed', linewidth=2)
        plt.text(median + 30, 100, median, color='coral')
        plt.xlabel('Length of a sample')
        plt.ylabel('Number of samples')
        plt.title('{}: Sample Length Distribution'.format(title))

    plt.figure(figsize=(12, 4))
    plt.subplot(121)
    plot_length_dist(train_text_lengths, 'Train')
    plt.subplot(122)
    plot_length_dist(test_text_lengths, 'Test')

    plt.subplots_adjust(wspace=0.3, hspace=0.3)
    plt.show()


def plot_distribution(train_labels, test_labels, classes):
    """打印类的分布"""
    def plot_dist(labels, title, color='blue', width=0.7):
        bin_count = np.bincount(labels)
        bin_percentage = bin_count / len(labels)
        rects = plt.bar(np.arange(len(bin_count)), bin_count, width, color=color)
        plt.title(title)
        if classes is None:
            plt.xticks(range(len(bin_count)))
        else:
            plt.xticks(range(len(bin_count)), labels=classes, rotation=45)
        plt.ylim(0, max(bin_count) * 1.1)

        for i, r in enumerate(rects):
            plt.annotate('{:0.1f}%'.format(int(bin_percentage[i] * 100)),
                         xy=(r.get_x() + r.get_width() / 2, r.get_height()),
                         xytext=(0, 3),  # 3 points vertical offset
                         textcoords="offset points",
                         ha='center', va='bottom')

    if len(classes) <= 10:
        plt.figure(figsize=(min(4 * len(classes), 16), 4))
        plt.subplot(121)
        plot_dist(train_labels, 'Train', color='teal')
        plt.subplot(122)
        plot_dist(test_labels, 'Test', color='coral')
    else:
        plt.figure(figsize=(20, 12))
        plt.subplot(211)
        plot_dist(train_labels, 'Train', color='teal')
        plt.subplot(212)
        plot_dist(test_labels, 'Test', color='coral')
    plt.show()


def lr_schedule(epoch, lr):
    lr_times = [(0, 1), (60, 1e-1), (90, 1e-2), (105, 1e-3), (120, 0.5e-3)]
    
    base_lr = 1e-3
    new_lr = base_lr
    for border_epoch, times in lr_times:
        if epoch>=border_epoch: 
            new_lr = base_lr*times
    if abs(lr - new_lr)>1e-7:
        # 如果lr比new_lr小，但是又大于0.1倍的new_lr，继续使用lr
        if new_lr > lr > 0.1*new_lr - 1e-7:
            print('Epoch %05d: Still keep learning rate %s instead of %s' % 
                  (epoch + 1, round(lr, 7), round(new_lr, 7))) 
            return lr   
        print('Epoch %05d: LearningRateScheduler reducing learning rate to %s from %s.' % 
              (epoch + 1, round(new_lr, 7), round(lr, 7)))
    return new_lr


class DictToObject(object):

    def __init__(self, dictionary):
        def _traverse(key, element):
            if isinstance(element, dict):
                return key, DictToObject(element)
            else:
                return key, element
        self.source = dictionary
        objd = dict(_traverse(k, v) for k, v in self.source.items())
        self.__dict__.update(objd)

    def get_similar_attribute(self, name):
        names = name.strip().split('.')
        last_name = names[-1]
        for i in range(0, len(names)):
            _names = names[0:(len(names)-1-i)] + [last_name]
            obj = self._get_similar_attribute(_names)
            if obj is not None:
                print('{}={}'.format('.'.join(_names), obj))
                return obj
        print('{}=None'.format('.'.join(names)))
        return None

    def _get_similar_attribute(self, names):
        def similar_attribute(obj, name):
            for key, attribute_ in obj.__dict__.items():
                if key == name:
                    return attribute_
            for key, attribute_ in obj.__dict__.items():
                if key == name[0:len(key)]:
                    return attribute_
            return None
        obj = self
        for name in names:
            obj = similar_attribute(obj, name)
            if obj is None:
                return None
        return obj


class TextClassificationHelper(object):
    
    def __init__(self, params, data=None, model_results={}):
        self.params = params
        self.model_results = model_results
        self.data = data
        
    def set_data(self, data):  
        self.data = data
        
    def set_model_results(self, model_results):  
        self.model_results = model_results

    def get_callbacks(self, model, verbose):
        callbacks_ = []
        if self.params.callbacks.ModelCheckpoint.enabled:
            print('use ModelCheckpoint(filepath={}, monitor={})'.format(
                model.checkpoint_path, self.params.callbacks.ModelCheckpoint.monitor))
            checkpoint_best_only = keras.callbacks.ModelCheckpoint(filepath=model.checkpoint_path,
                                                                   monitor=self.params.callbacks.ModelCheckpoint.monitor,
                                                                   save_weights_only=True,
                                                                   save_best_only=True,
                                                                   verbose=False)
            callbacks_.append(checkpoint_best_only)

        if self.params.callbacks.EarlyStopping.enabled:
            print('use EarlyStopping(monitor={}, patience={})'.format(self.params.callbacks.EarlyStopping.monitor,
                                                                self.params.callbacks.EarlyStopping.patience))
            early_stopping = keras.callbacks.EarlyStopping(monitor=self.params.callbacks.EarlyStopping.monitor,
                                                           patience=self.params.callbacks.EarlyStopping.patience,
                                                           verbose=True)
            callbacks_.append(early_stopping)

        if self.params.callbacks.ReduceLROnPlateau.enabled:
            print('use ReduceLROnPlateau(monitor={}, factor={}, patience={})'.format(
                self.params.callbacks.ReduceLROnPlateau.monitor,
                self.params.callbacks.ReduceLROnPlateau.factor,
                self.params.callbacks.ReduceLROnPlateau.patience))
            reduce_lr = keras.callbacks.ReduceLROnPlateau(monitor=self.params.callbacks.ReduceLROnPlateau.monitor,
                                                          factor=self.params.callbacks.ReduceLROnPlateau.factor,
                                                          patience=self.params.callbacks.ReduceLROnPlateau.patience,
                                                          min_lr=0.5e-6, verbose=verbose)
            callbacks_.append(reduce_lr)

        if self.params.callbacks.LearningRateScheduler.enabled:
            print('use LearningRateScheduler()')
            lr_scheduler = keras.callbacks.LearningRateScheduler(self.params.callbacks.LearningRateScheduler.schedule,
                                                                 verbose=False)
            callbacks_.append(lr_scheduler)
        return callbacks_
        
    def train(self, model, callbacks=None, epochs=None, verbose=True, batch_size=None):
        """要求模型设置name属性，用于保存模型。"""
        if epochs is None:
            epochs = self.get_model_param(model.name, 'epochs')
        if callbacks is None:
            callbacks = self.get_callbacks(model, verbose)
        if batch_size is not None and batch_size != self.data.batch_size:
            print('Refresh datasets because batch_size is changed to {} from {}'.format(batch_size, self.data.batch_size))
            self.data.batch_size = batch_size
            self.data.refresh()

        if self.data.val_dataset is None:
            validation_dataset = self.data.test_dataset
        else:
            validation_dataset = self.data.val_dataset          

        with TaskTime('training', True) as t:
            if isinstance(self.data, SimpleTextDataset):
                history = model.fit(self.data.train_dataset.features,
                                    self.data.train_dataset.labels,
                                    validation_data=(validation_dataset.features, validation_dataset.labels),
                                    epochs=epochs, verbose=verbose,
                                    batch_size=self.params.batch_size,
                                    shuffle=True,
                                    callbacks=callbacks)
            else:
                history = model.fit(self.data.train_dataset, validation_data=validation_dataset,
                                    epochs=epochs, verbose=verbose,
                                    callbacks=callbacks)
            history.train_time = t.elapsed_time()
        plot_history(history)
        return history  
    
    def compile(self, model):
        learning_rate = self.get_model_param(model.name, 'learning_rate')
        # if len(self.params.classes) == 2:
        #     loss = losses.BinaryCrossentropy(from_logits=True),
        # else:
        loss = losses.SparseCategoricalCrossentropy(from_logits=True),
        model.compile(optimizer=optimizers.Adam(learning_rate=learning_rate),
                      loss=loss,
                      metrics=self.params.metrics)

        dataset_path = './checkpoints/{}'.format(self.params.dataset_name)
        model.checkpoint_path = '{}/{}/checkpoint'.format(dataset_path, model.name)
        print('checkpoint_path={}'.format(model.checkpoint_path))
        return model    
                                                         
    def evaluate(self, model, train_time, train_dataset=None, val_dataset=None, test_dataset=None):
        """评估当前模型，并且显示所有模型的信息"""
        def _evaluate(dataset):
            if isinstance(self.data, SimpleTextDataset):
                loss, accuracy = model.evaluate(dataset.features, dataset.labels, verbose=True)
            else:
                loss, accuracy = model.evaluate(dataset, verbose=True)
            return loss, accuracy
        model_results = self.model_results
        if train_dataset is None:
            train_dataset = self.data.train_dataset
        if val_dataset is None:
            val_dataset = self.data.val_dataset
        if test_dataset is None:
            test_dataset = self.data.test_dataset

        train_loss, train_accuracy = _evaluate(train_dataset)
        if val_dataset is not None:
            val_loss, val_accuracy = _evaluate(val_dataset)
        test_loss, test_accuracy = _evaluate(test_dataset)
        if model.name not in model_results or model_results[model.name]['test_accuracy']<test_accuracy:
            if val_dataset is not None:
                model_results[model.name] = {'train_loss': round(train_loss, 6),
                                             'train_accuracy': round(train_accuracy, 4),
                                             'val_loss': round(val_loss, 6),
                                             'val_accuracy': round(val_accuracy, 4),
                                             'test_loss': round(test_loss, 6),
                                             'test_accuracy': round(test_accuracy, 4),
                                             'weight_number': get_weight_num(model),
                                             'model': model,
                                             'data':self.data,
                                             'train_time': round(train_time, 0)}
            else:
                model_results[model.name] = {'train_loss': round(train_loss, 6),
                                             'train_accuracy': round(train_accuracy, 4),
                                             'test_loss': round(test_loss, 6),
                                             'test_accuracy': round(test_accuracy, 4),
                                             'weight_number': get_weight_num(model),
                                             'model': model,
                                             'data': self.data,
                                             'train_time': round(train_time, 0)}
        print('Test loss:{:0.4f}, Test Accuracy:{:0.2%}'.format(test_loss, test_accuracy))
                    
    def model_summary(self, model, history):
        # 加载最佳checkpoint，并评估
        print('-'*40, 'evaluate', '-'*40)
        if self.params.restore_best_checkpoint:
            model.load_weights(model.checkpoint_path)
        self.evaluate(model, train_time=history.train_time)

        # 混淆矩阵
        print('-'*40, 'confusion matrix'  , '-'*40)
        self.plot_confusion_matrix(model)   

        # # 模型对比
        # print('-'*40, 'model improvement'.format(model.name), '-'*40)
        # self.plot_predicted_sample(model, sample_count=5, only_compare_best=True)
        
        # 错误比较        
        if len(self.model_results.keys())>1:
            print('-'*40, 'error analysis'.format(model.name), '-'*40)
            self.plot_predicted_sample(model, sample_count=5)

        # 所有模型结果
        print('-'*50, 'all models'.format(model.name), '-'*50)
        self.show_model_results()

    def get_model_param(self, model_name, attribute):
        return self.params.get_similar_attribute('model_params.{}.{}'.format(model_name, attribute))

    # def get_learning_rate(self, model_name):
    #     return self.get_model_param(model_name, 'learning_rate')
    #
    # def get_dropout(self, model_name):
    #     return self.get_model_param(model_name, 'dropout')
    
    def get_best_model(self, exclude_mode_name=''):
        models = [(model_name, model_result['test_accuracy'])
                  for model_name, model_result in self.model_results.items() 
                  if model_name != exclude_mode_name]
        if len(models) == 0:
            return None, None
        models = sorted(models, key=lambda item: item[1])
        best_model_name = models[-1][0]
        return self.model_results[best_model_name]['model'], self.model_results[best_model_name]['data']
        
    def show_model_results(self):
        """按照test_accuracy倒序显示所有模型的信息"""
        model_results = self.model_results
        models_remove1 = {key:{key1:value1 for key1, value1 in value.items() if key1 != 'model' and key1 != 'data'}
                          for key, value in model_results.items()}
        df_models = pd.DataFrame.from_dict(models_remove1, orient='index')
        df_models = df_models.sort_values('test_accuracy', ascending=False) 
        display(df_models)       
        
    def show_images(self, images, labels, x_num=6, y_num=6, figsize=(8, 8), images_mean=None):
        """显示图片"""
        classes = self.data.classes
        plt.figure(figsize=figsize)
        channel_count = images.shape[-1]
        for i in range(x_num*y_num):
            plt.subplot(x_num, y_num, i+1)
            if images_mean is not None:
                image = images[i]+images_mean
            else:
                image = images[i]
            if channel_count==1:
                plt.imshow(image, cmap='gray')
            else:
                plt.imshow(image)
            label = labels[i] if classes is None else classes[labels[i]]
            plt.title("{}".format(label))
            plt.xticks([])
            plt.yticks([])    

        plt.tight_layout()
        plt.subplots_adjust(wspace=0.3, hspace=0.3)      
        plt.show()

    def plot_distribution(self, train_labels=None, test_labels=None, classes=None):
        """打印类的分布"""
        if train_labels is None:
            train_labels = self.data.train_labels
        if test_labels is None:
            test_labels = self.data.test_labels
        if classes is None:
            classes = self.data.classes

        plot_distribution(train_labels, test_labels, classes)

    def plot_confusion_matrix(self, model1, texts=None, labels=None, model2=None, compared=True):
        """打印混淆矩阵"""
        def plot_cm(model, texts):
            # if len(classes) == 2:
            #     predictions = model.predict(texts) > 0
            # else:
            predictions = model.predict(texts, verbose=True).argmax(axis=-1)
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

            plt.title("{} - Confusion matrix".format(model.name))
            sns.heatmap(df_cm, annot=True, fmt='g',cmap='coolwarm')
            if classes is not None: 
                plt.yticks(rotation=0)
                plt.xticks(rotation=45)
            plt.xlabel("Predicted")
            plt.ylabel("Actual")

        if texts is None:
            texts = self.data.test_texts
        if labels is None:
            labels = self.data.test_labels
        classes = self.data.classes
        
        if compared and model2 is None:
            model2, data2 = self.get_best_model(model1.name)

        if len(classes) <= 10:
            height = min(6, len(classes)*2)
        else:
            height = min(len(classes), 20)
        if model2 is not None:
            if len(classes) <= 10:
                plt.figure(figsize=(height*2+6, height))
                plt.subplot(1, 2, 1)
                plot_cm(model2, data2.test_texts)
                plt.subplot(1, 2, 2)
                plot_cm(model1, texts)
            else:
                plt.figure(figsize=(height, height*2))
                plt.subplot(2, 1, 1)
                plot_cm(model2, data2.test_texts)
                plt.subplot(2, 1, 2)
                plot_cm(model1, texts)
        else:  
            plt.figure(figsize=(height+1, height))
            plot_cm(model1, texts)

        plt.show()    

    def plot_predicted_sample(self, model, texts=None, labels=None, sample_count=5, raw_texts=None,
                              show_error=True, only_compare_best=False):
        """查看一些样本的分类情况"""
        def get_class(label):
            if classes is None:
                return label
            else:
                return classes[label]

        def plot_var(model, text, classes):
            predict = np.squeeze(tf.nn.softmax(model.predict(text)).numpy())
            max_like = np.argmax(predict)
            max_like_value = predict[max_like]

            if classes is None:
                _classes = range(label_count)
                plt.text(max_like-0.4, max_like_value+0.02,
                         '{:0.1f}%'.format(max_like_value*100), fontsize=8)            
                plt.bar(_classes, predict, width=0.8, color='steelblue', alpha=0.8)
                plt.ylim(0, 1.2)
                plt.xticks(range(len(_classes)), _classes, fontsize=8)
            elif len(classes) <= 5:
                _classes = classes
                plt.text(max_like-0.4, max_like_value+0.02,
                         '{:0.1f}%'.format(max_like_value*100), fontsize=8)
                plt.bar(_classes, predict, width=0.8, color='steelblue', alpha=0.8)
                plt.ylim(0, 1.2)
                _classes = [_class[0:10] for _class in _classes]
                plt.xticks(range(len(_classes)), _classes, fontsize=8, rotation=45)
            elif len(classes) > 10:
                idx = predict.argsort()[-10:]
                predict = predict[idx]
                _classes = np.array(classes)[idx]
                plt.text(max_like_value+0.02, label_count-1,
                         '{:0.1f}%'.format(max_like_value*100), fontsize=8)
                plt.barh(_classes, predict, height=0.8, color='steelblue', alpha=0.8)
                plt.xlim(0, 1.2)
                _classes = [_class[0:10] for _class in _classes]
                plt.yticks(range(len(_classes)), _classes, fontsize=8)
            else:
                _classes = classes
                plt.text(max_like_value+0.02, max_like, 
                         '{:0.1f}%'.format(max_like_value*100), fontsize=8)             
                plt.barh(_classes, predict, height=0.8, color='steelblue', alpha=0.8)
                plt.xlim(0, 1.2)
                _classes = [_class[0:10] for _class in _classes]
                plt.yticks(range(len(_classes)), _classes, fontsize=8)
            plt.title('{}: {}'.format(model.name, get_class(max_like)), fontsize=10)

        if texts is None:
            texts = self.data.test_texts
        if labels is None:
            labels = self.data.test_labels
        if raw_texts is None:
            raw_texts = self.data.raw_test_texts
        classes = self.data.classes
        
        if only_compare_best:
            best_model, best_data = self.get_best_model(model.name)
            if best_model is None:
                models = [(model, texts)]
            else:
                models = [(best_model, best_data.test_texts), (model, texts)]
        else:   
            models = [(model, texts)] + [(model_result['model'], model_result['data'].test_texts)
                                         for model_name, model_result in self.model_results.items()
                                         if model_name!=model.name]

        bin_count = np.bincount(labels)
        label_count = len(bin_count)
        column_count = len(models)+1

        if show_error:
            # print(models[0][0])
            # print(texts.shape)
            base_predictions = model.predict(texts, verbose=True).argmax(axis=-1)
            error_indexes = base_predictions != labels
            error_raw_texts = [raw_text for i, raw_text in enumerate(raw_texts) if base_predictions[i] != labels[i]]
            error_labels = labels[error_indexes]
            sample_indexes = np.random.randint(error_labels.shape[0], size=sample_count)
            sample_labels = error_labels[sample_indexes]
            sample_raw_texts = [error_raw_texts[index] for index in sample_indexes]
        else:
            sample_indexes = np.random.randint(len(labels), size=sample_count)
            sample_labels = labels[sample_indexes]
            sample_raw_texts = [raw_texts[index] for index in sample_indexes]

        for i in range(sample_count):
            print('.'*40, classes[sample_labels[i]], '.'*40)
            if len(sample_raw_texts[i]) <= 3000:
                print(sample_raw_texts[i])
            else:
                print(sample_raw_texts[i][0:3000] + '...')
            if classes is None:
                plt.figure(figsize=(2.2 * column_count, 2.2))
            elif len(classes) <= 5:
                plt.figure(figsize=(2.8 * column_count, 2.2))
            else:
                plt.figure(figsize=(3.2* column_count, 2.8))
            for j, (model, _texts) in enumerate(models):
                plt.subplot(1, column_count, j+1)
                if show_error:
                    error_texts = _texts[error_indexes]
                    sample_texts = error_texts[sample_indexes]
                else:
                    sample_texts = _texts[sample_indexes]
                plot_var(model, sample_texts[i:i+1], classes)

            plt.subplots_adjust(wspace=0.5, hspace=0.5)
            plt.show()
        

class SimpleData(object):
    def __init__(self, features, labels):
        self.features = features
        self.labels = labels


class TextDataset(object):
    def __init__(self, params, train_texts, train_labels, test_texts, test_labels, raw_train_texts, raw_test_texts,
                 batch_size=None):
        super().__init__()
        self.dataset_name = params.dataset_name
        if batch_size is None:
            self.batch_size = params.batch_size
        else:
            self.batch_size = batch_size
        self.validation_percent = params.validation_percent
        self.classes = params.classes

        self.train_texts = train_texts
        self.train_labels = train_labels
        self.test_texts = test_texts
        self.test_labels = test_labels
        self.input_shape = self.train_texts.shape[1:]

        self.raw_train_texts = raw_train_texts
        self.raw_test_texts = raw_test_texts
        
        print('create train, validation and test dataset')
        self.train_dataset, self.val_dataset, self.test_dataset = self.get_datasets()

    def get_datasets(self, random_state=42):
        X_train, X_val, y_train, y_val = self._get_train_val(random_state)

        test_dataset = tf.data.Dataset.from_tensor_slices((self.test_texts, self.test_labels))
        test_dataset = test_dataset.batch(self.batch_size)

        train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train))
        train_dataset = train_dataset.shuffle(len(y_train), reshuffle_each_iteration=True)
        train_dataset = train_dataset.batch(self.batch_size, drop_remainder=True)

        if self.validation_percent>0:
            val_dataset = tf.data.Dataset.from_tensor_slices((X_val, y_val))
            val_dataset = val_dataset.shuffle(len(y_val), reshuffle_each_iteration=True)
            val_dataset = val_dataset.batch(self.batch_size)
        else:
            val_dataset = None

        return train_dataset, val_dataset, test_dataset

    def refresh(self):
        self.train_dataset, self.val_dataset, self.test_dataset = self.get_datasets()
        return self

    def _get_train_val(self, random_state=42):
        if self.validation_percent>0:
            print('split train into train and validation')
            X_train, X_val, y_train, y_val = train_test_split(self.train_texts, self.train_labels,
                                                              test_size=self.validation_percent,
                                                              random_state=random_state)
            print('train:', X_train.shape, y_train.shape)
            print('validation:', X_val.shape, y_val.shape)
        else:
            X_train, X_val, y_train, y_val = self.train_texts, None, self.train_labels, None
        return X_train, X_val, y_train, y_val


class SimpleTextDataset(TextDataset):
    def __init__(self, params, train_texts, train_labels, test_texts, test_labels,
                 raw_train_texts, raw_test_texts, batch_size=None):
        super().__init__(params, train_texts, train_labels, test_texts, test_labels,
                                                raw_train_texts, raw_test_texts, batch_size)

    def get_datasets(self, random_state=42):
        X_train, X_val, y_train, y_val = self._get_train_val(random_state)
        train_data = SimpleData(X_train, y_train)
        if X_val is not None:
            val_data = SimpleData(X_train, y_train)
        else:
            val_data = None
        test_data = SimpleData(self.test_texts, self.test_labels)
        return train_data, val_data, test_data


class SequenceTextDataset(TextDataset):
    def __init__(self, params, train_texts, train_labels, test_texts, test_labels,
                 raw_train_texts, raw_test_texts, tokenizer, batch_size=None):
        super().__init__(params, train_texts, train_labels, test_texts, test_labels,
                                                  raw_train_texts, raw_test_texts, batch_size)
        self.tokenizer = tokenizer


class TaskTime:
    '''用于显示执行时间'''

    def __init__(self, task_name, show_start=False):
        super(TaskTime, self).__init__()
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
