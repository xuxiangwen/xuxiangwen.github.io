#!/usr/bin/env python

import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import pickle
import seaborn as sns
import tensorflow as tf
import util
import text_predictor

from IPython.display import display
from sklearn.feature_extraction import text
from sklearn.metrics import confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras import losses, optimizers, models, metrics


# 设置日志
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)


def plot_model_structure(model):
    """打印模型的结构"""
    img = tf.keras.utils.plot_model(model, '{}.png'.format(model.name), show_shapes=True)
    display(img)


def plot_history(history, key_metric_name='accuracy'):
    """显示训练的loss和accuracy的走势图"""
    plt.figure(figsize=(16, 5))
    max_epoch = len(history.history[key_metric_name])
    epochs = range(1, max_epoch+1)
    if max_epoch <= 20:
        xticks = range(0, max_epoch+1)
    else:
        xticks = range(0, max_epoch+1, (max_epoch-1)//20+1)
    plt.subplot(121)
    plt.plot(epochs, history.history[key_metric_name])
    plt.plot(epochs, history.history['val_'+key_metric_name])
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


class Params(DictToObject):
    def __init__(self, dictionary, base_path='./models'):
        super().__init__(dictionary)
        self.save_path = os.path.join(base_path, self.dataset_name, self.program_name.split('.')[0])


class TextClassificationHelper(object):
    
    def __init__(self, params, datasets=None, model_results={}):
        self.params = params
        self.model_results = model_results
        self.datasets = datasets
        
    def set_datasets(self, datasets):
        self.datasets = datasets
        
    def set_model_results(self, model_results):  
        self.model_results = model_results

    def get_callbacks(self, model, verbose):
        callbacks_ = []
        if self.params.callbacks.ModelCheckpoint.enabled:
            print('use ModelCheckpoint(filepath={}, monitor={})'.format(
                model.checkpoint_path, self.params.callbacks.ModelCheckpoint.monitor))
            checkpoint_best_only = keras.callbacks.ModelCheckpoint(filepath=model.checkpoint_path,
                                                                   monitor=self.params.callbacks.ModelCheckpoint.monitor,
                                                                   save_weights_only=False,
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
        
    def train(self, model, callbacks=None, epochs=None, verbose=True, batch_size=None, evaluate_before_train=True):
        """要求模型设置name属性，用于保存模型。"""
        if epochs is None:
            epochs = self.get_model_param(model.name, 'epochs')
        if callbacks is None:
            callbacks = self.get_callbacks(model, verbose)
        if batch_size is not None and batch_size != self.datasets.batch_size:
            print('Refresh datasets because batch_size is changed to {} from {}'.format(batch_size,
                                                                                        self.datasets.batch_size))
            self.datasets.batch_size = batch_size
            self.datasets.refresh()

        if self.datasets.val_dataset is None:
            validation_dataset = self.datasets.test_dataset
        else:
            validation_dataset = self.datasets.val_dataset

        if evaluate_before_train:
            self.evaluate(model, is_load_best_model=False)

        with util.TaskTime('training', True) as t:
            use_class_weight = self.params.get_similar_attribute('use_class_weight')
            class_weight = self.params.get_similar_attribute('class_weight')
            if use_class_weight is None or not use_class_weight or class_weight is None:
                class_weight = None
            else:
                class_weight = class_weight

            if isinstance(self.datasets, SimpleTextDatasets):
                history = model.fit(self.datasets.train_dataset.features,
                                    self.datasets.train_dataset.labels,
                                    validation_data=(validation_dataset.features, validation_dataset.labels),
                                    epochs=epochs, verbose=verbose,
                                    batch_size=self.params.batch_size,
                                    shuffle=True,
                                    class_weight=class_weight,
                                    callbacks=callbacks)
            else:
                history = model.fit(self.datasets.train_dataset, validation_data=validation_dataset,
                                    epochs=epochs, verbose=verbose,
                                    class_weight=class_weight,
                                    callbacks=callbacks)
            history.train_time = t.elapsed_time()
        plot_history(history, key_metric_name=self.get_default_metric_name())
        return history

    def get_default_metric_name(self):
        metric = self.params.metrics[0]
        if isinstance(metric, metrics.Metric):
            return metric.name
        else:
            return metric

    def compile(self, model, clip_value=None, learning_rate=None):
        if learning_rate is None:
            learning_rate = self.get_model_param(model.name, 'learning_rate')
        if clip_value is None:
            clip_value = self.get_model_param(model.name, 'clip_value')
        loss = self.params.loss
        if loss is None:
            loss = losses.SparseCategoricalCrossentropy(from_logits=True)
        if clip_value is None:
            optimizer = optimizers.Adam(learning_rate=learning_rate)
        else:
            optimizer = optimizers.Adam(learning_rate=learning_rate, clipvalue=clip_value)
        model.compile(optimizer,
                      loss=loss,
                      metrics=self.params.metrics)
        if self.params.use_savedmodel:
            model.checkpoint_path = os.path.join(self.params.save_path, model.name)
        else:
            model.checkpoint_path = os.path.join(self.params.save_path, model.name+'.h5')
        print('checkpoint_path={}'.format(model.checkpoint_path))
        return model    
                                                         
    def evaluate(self, model, train_time=0, train_dataset=None, val_dataset=None, test_dataset=None, is_load_best_model=True):
        """评估当前模型，并且显示所有模型的信息"""
        def _evaluate(dataset):
            if isinstance(self.datasets, SimpleTextDatasets):
                results = model.evaluate(dataset.features, dataset.labels, verbose=True, return_dict=True)
            else:
                results = model.evaluate(dataset, verbose=True, return_dict=True)
            return results

        model_results = self.model_results
        if train_dataset is None:
            train_dataset = self.datasets.train_dataset
        if val_dataset is None:
            val_dataset = self.datasets.val_dataset
        if test_dataset is None:
            test_dataset = self.datasets.test_dataset

        train_result = _evaluate(train_dataset)
        if val_dataset is not None:
            val_result = _evaluate(val_dataset)
        test_result = _evaluate(test_dataset)

        if is_load_best_model:
            predictor = text_predictor.TfTextPredictor(self.params.classes,
                                                       model_path=model.checkpoint_path,
                                                       vectorizer_path=self.datasets.vectorizer_path)
        else:
            print('1')
            predictor = text_predictor.TfTextPredictor(self.params.classes,
                                                       model_path=model.checkpoint_path,
                                                       vectorizer_path=self.datasets.vectorizer_path,
                                                       model=model,
                                                       vectorizer=self.datasets.vectorizer)

        predictor_path = os.path.abspath(os.path.join(self.params.save_path, model.name + '.predictor'))
        print('save predictor into {}'.format(predictor_path))
        util.ObjectPickle.save(predictor_path, predictor)

        model_result = {'weight_number': util.get_weight_num(model),
                        'model': model,
                        'datasets': self.datasets,
                        'train_time': round(train_time, 0),
                        'predictor_path': predictor_path
                        }
        print('-'*80)
        metrics_name = [metric_name for metric_name in model.metrics_names if metric_name!='auc'] + ['auc']
        for metric_name in metrics_name:
            if metric_name == 'sparse_top_k_categorical_accuracy':
                save_metric_name = 'top2_accuracy'
            else:
                save_metric_name = metric_name
            if metric_name == 'auc':
                train_result[metric_name] = self.roc_auc_score(model, self.datasets.train_data,
                                                               self.datasets.train_labels)[0]
                if val_dataset is not None:
                    val_result[metric_name] = self.roc_auc_score(model, self.datasets.val_data,
                                                                   self.datasets.val_labels)[0]
                test_result[metric_name] = self.roc_auc_score(model, self.datasets.test_data,
                                                              self.datasets.test_labels)[0]

            model_result['train_' + save_metric_name] = round(train_result[metric_name], 4)
            if val_dataset is not None:
                model_result['val_' + save_metric_name] = round(val_result[metric_name], 4)
            model_result['test_' + save_metric_name] = round(test_result[metric_name], 4)
            print('test {}:{:0.4f}'.format(save_metric_name, test_result[metric_name]))

        model_results[model.name] = model_result

    def roc_auc_score(self, model, data=None, labels=None):
        if data is None or labels is None:
            data = self.datasets.test_data
            labels = self.datasets.test_labels
        predictions = model.predict(data)
        if len(labels.shape) <= 1 :
            # convert multiple class to one hot
            new_labels = np.zeros((labels.size, labels.max() + 1))
            new_labels[np.arange(labels.size), labels] = 1
            labels = new_labels
        score = roc_auc_score(labels, predictions)
        scores = []
        if len(labels.shape) >= 1:
            label_count = labels.shape[1]
            for j in range(label_count):
                scores.append(roc_auc_score(labels[:, j], predictions[:, j]))
        else:
            scores = [score]
        return score, scores

    def load_model(self, checkpoint_path, compile_fun=None):
        model = models.load_model(checkpoint_path)
        if compile_fun is None:
            self.compile(model)
        else:
            compile_fun(model)
        return model
                    
    def model_summary(self, model, history, show_error_sample=False, is_show_model_results=True,
                      is_show_confusion_matrix=True):
        # 加载最佳checkpoint，并评估
        print('-'*40, 'evaluate', '-'*40)
        if self.params.restore_best_checkpoint:
            checkpoint_path = model.checkpoint_path
            print('load best checkpoint from {}'.format(checkpoint_path))
            model = self.load_model(checkpoint_path)

        self.evaluate(model, train_time=history.train_time, is_load_best_model=False)

        # 混淆矩阵
        if is_show_confusion_matrix:
            if len(self.datasets.test_labels.shape) <= 1:
                print('-'*40, 'confusion matrix', '-'*40)
                self.plot_confusion_matrix(model)

                # # 模型对比
                # print('-'*40, 'model improvement'.format(model.name), '-'*40)
                # self.plot_predicted_sample(model, sample_count=5, only_compare_best=True)

                # 错误比较
                if show_error_sample and len(self.model_results.keys())>1:
                    print('-'*40, 'error analysis'.format(model.name), '-'*40)
                    self.plot_predicted_sample(model, sample_count=5)

        # 所有模型结果
        if is_show_model_results:
            print('-'*50, 'all models'.format(model.name), '-'*50)
            self.show_model_results()

    def get_model_param(self, model_name, attribute):
        return self.params.get_similar_attribute('model_params.{}.{}'.format(model_name, attribute))
    
    def get_best_model(self, exclude_mode_name=''):
        models = [(model_name, model_result['test_accuracy'])
                  for model_name, model_result in self.model_results.items() 
                  if model_name != exclude_mode_name]
        if len(models) == 0:
            return None, None
        models = sorted(models, key=lambda item: item[1])
        best_model_name = models[-1][0]
        return self.model_results[best_model_name]['model'], self.model_results[best_model_name]['datasets']
        
    def show_model_results(self):
        def get_key_value(key, value):
            if key == 'model':
                return 'checkpoint_path', os.path.abspath(value.checkpoint_path)
            elif key == 'datasets':
                return 'vectorizer_path', os.path.abspath(value.vectorizer_path) if value.vectorizer_path is not None \
                    else None
            else:
                return key, value

        model_results = self.model_results
        models_result_show = {key: {key1: value1 for key1, value1 in value.items()
                                    if key1 not in ['model', 'datasets', 'text_column', 'predictor_path']}
                              for key, value in model_results.items()}
        df_models = pd.DataFrame.from_dict(models_result_show, orient='index')
        """按照test_accuracy倒序显示所有模型的信息"""
        df_models = df_models.sort_values('test_' + self.get_default_metric_name(), ascending=False)
        display(df_models.head(20))

        model_results_save = []
        for key, value in model_results.items():
            items = [get_key_value(key1, value1) for key1, value1 in value.items()]
            metrics = {key1: value1 for key1, value1 in items}
            metrics['dataset_name'] = self.params.dataset_name
            metrics['program_name'] = self.params.program_name
            metrics['model_name'] = key
            metrics['classes'] = self.params.classes
            metrics['text_column'] = self.params.text_column
            model_results_save.append(metrics)

        model_results_path = os.path.join(self.params.save_path, 'model_results.json')
        util.JsonPickle.save(model_results_path, model_results_save)

    def plot_distribution(self, train_labels=None, test_labels=None, classes=None):
        """打印类的分布"""
        if train_labels is None:
            train_labels = self.datasets.train_labels
        if test_labels is None:
            test_labels = self.datasets.test_labels
        if classes is None:
            classes = self.datasets.classes

        plot_distribution(train_labels, test_labels, classes)

    def plot_confusion_matrix(self, model1, data=None, labels=None, model2=None, compared=True, k=1):
        """打印混淆矩阵"""
        def plot_cm(model, data):
            if k == 1:
                predictions = model.predict(data, verbose=True).argmax(axis=-1)
            else:
                predictions = model.predict(data, verbose=True)
                predictions = [labels[i] if labels[i] in list(predictions[i].argsort()[-k:][::-1]) else predictions[i].argmax() for i in range(len(labels))]

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
            sns.heatmap(df_cm, annot=True, fmt='g', cmap='coolwarm')
            if classes is not None: 
                plt.yticks(rotation=0)
                plt.xticks(rotation=45)
            plt.xlabel("Predicted")
            plt.ylabel("Actual")

        if data is None:
            data = self.datasets.test_data
        if labels is None:
            labels = self.datasets.test_labels
        classes = self.datasets.classes
        
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
                plot_cm(model2, data2.test_data)
                plt.subplot(1, 2, 2)
                plot_cm(model1, data)
            else:
                plt.figure(figsize=(height, height*2))
                plt.subplot(2, 1, 1)
                plot_cm(model2, data2.test_data)
                plt.subplot(2, 1, 2)
                plot_cm(model1, data)
        else:  
            plt.figure(figsize=(height+1, height))
            plot_cm(model1, data)

        plt.show()    

    def plot_predicted_sample(self, model, data=None, labels=None, sample_count=5, texts=None,
                              show_error=True, only_compare_best=False):
        """查看一些样本的分类情况"""
        def get_class(label):
            if classes is None:
                return label
            else:
                return classes[label]

        def plot_var(model, data, classes):
            predict = np.squeeze(tf.nn.softmax(model.predict(data)).numpy())
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

        if data is None:
            data = self.datasets.test_data
        if labels is None:
            labels = self.datasets.test_labels
        if texts is None:
            texts = self.datasets.test_texts
        classes = self.datasets.classes
        
        if only_compare_best:
            best_model, best_datasets = self.get_best_model(model.name)
            if best_model is None:
                model_data_list = [(model, data)]
            else:
                model_data_list = [(best_model, best_datasets.test_data), (model, data)]
        else:   
            model_data_list = [(model, data)] + [(model_result['model'], model_result['datasets'].test_data)
                                                 for model_name, model_result in self.model_results.items()
                                                 if model_name != model.name]

        bin_count = np.bincount(labels)
        label_count = len(bin_count)
        column_count = len(model_data_list)+1

        if show_error:
            base_predictions = model.predict(data, verbose=True).argmax(axis=-1)
            error_indexes = base_predictions != labels
            error_texts = [raw_text for i, raw_text in enumerate(texts) if base_predictions[i] != labels[i]]
            error_labels = labels[error_indexes]
            sample_indexes = np.random.randint(error_labels.shape[0], size=sample_count)
            sample_labels = error_labels[sample_indexes]
            sample_texts = [error_texts[index] for index in sample_indexes]
        else:
            sample_indexes = np.random.randint(len(labels), size=sample_count)
            sample_labels = labels[sample_indexes]
            sample_texts = [texts[index] for index in sample_indexes]

        for i in range(sample_count):
            print('.'*40, classes[sample_labels[i]], '.'*40)
            if len(sample_texts[i]) <= 3000:
                print(sample_texts[i])
            else:
                print(sample_texts[i][0:3000] + '...')
            if classes is None:
                plt.figure(figsize=(2.2 * column_count, 2.2))
            elif len(classes) <= 5:
                plt.figure(figsize=(2.8 * column_count, 2.2))
            else:
                plt.figure(figsize=(3.2* column_count, 2.8))
            for j, (model, _data) in enumerate(model_data_list):
                plt.subplot(1, column_count, j+1)
                if show_error:
                    # print(type(_data))
                    error_data = _data[error_indexes]
                    sample_data = error_data[sample_indexes]
                else:
                    sample_data = _data[sample_indexes]
                plot_var(model, sample_data[i:i+1], classes)

            plt.subplots_adjust(wspace=0.5, hspace=0.5)
            plt.show()
        

class SimpleData(object):
    def __init__(self, features, labels):
        self.features = features
        self.labels = labels


class TextDatasets(object):
    def __init__(self, params, train_texts, train_labels, test_texts, test_labels, vectorizer=None,
                 batch_size=None, name='TextDatasets'):
        super().__init__()
        self.name = name
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
        self.vectorizer = vectorizer

        self.train_data = vectorizer.transform(self.train_texts)
        self.test_data = vectorizer.transform(self.test_texts)
        if len(self.train_data.shape) >= 2:
            self.input_shape = self.train_data.shape[1:]
        else:
            self.input_shape = []

        self.vectorizer_path = os.path.join(params.save_path, self.name + '.vectorizer')
        util.ObjectPickle.save(self.vectorizer_path, self.vectorizer)

        print('create train, validation and test dataset')
        self.train_dataset, self.val_dataset, self.test_dataset = self.get_datasets()

    def get_datasets(self, random_state=42):
        X_train, X_val, y_train, y_val = self._get_train_val(random_state)
        train_dataset = SimpleData(X_train, y_train)
        if X_val is not None:
            val_dataset = SimpleData(X_train, y_train)
        else:
            val_dataset = None
        test_dataset = SimpleData(self.test_data, self.test_labels)
        return train_dataset, val_dataset, test_dataset

    def refresh(self):
        self.train_dataset, self.val_dataset, self.test_dataset = self.get_datasets()
        return self

    def _get_train_val(self, random_state=42):
        if self.validation_percent>0:
            print('split train into train and validation')
            X_train, X_val, y_train, y_val = train_test_split(self.train_data, self.train_labels,
                                                              test_size=self.validation_percent,
                                                              random_state=random_state)
            print('train:', X_train.shape, y_train.shape)
            print('validation:', X_val.shape, y_val.shape)
        else:
            X_train, X_val, y_train, y_val = self.train_data, None, self.train_labels, None
        return X_train, X_val, y_train, y_val


class RawTextDatasets(TextDatasets):
    def __init__(self, params, train_texts, train_labels, test_texts, test_labels, vectorizer=util.RawVectorizer(),
                 batch_size=None, name='RawTextDatasets'):
        super().__init__(params, train_texts, train_labels, test_texts, test_labels, vectorizer,
                         batch_size, name)

    def get_datasets(self, random_state=42):
        X_train, X_val, y_train, y_val = self._get_train_val(random_state)

        test_dataset = tf.data.Dataset.from_tensor_slices((self.test_data, self.test_labels))
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


class TransferTextDatasets(TextDatasets):
    def __init__(self, params, train_texts, train_labels, test_texts, test_labels,
                 vectorizer, batch_size=None, name='TransferTextDatasets'):
        super().__init__(params, train_texts, train_labels, test_texts, test_labels, vectorizer,
                         batch_size, name)

    def get_dataset(self, texts, labels):
        def split(text, label):
            return tf.strings.split(text), label

        def embedding(text, label):
            return self.transfer_layer(text), label

        def filter_(text, label):
            return len(text) <= 250

        def padding(text, label):
            if len(text) < 250:
                left_padding = tf.math.maximum(0, 250 - len(text))
                paddings = [[left_padding, 0], [0, 0]]
                text = tf.pad(text, paddings, "CONSTANT")
            else:
                text = text[0:250]
            return text, label

        dataset = tf.data.Dataset.from_tensor_slices((texts, labels))
        dataset = dataset.map(split)
        dataset = dataset.map(embedding)
        dataset = dataset.map(padding)

        return dataset

    def get_datasets(self, random_state=42):
        X_train, X_val, y_train, y_val = self._get_train_val(random_state)

        test_dataset = tf.data.Dataset.from_tensor_slices((self.test_data, self.test_labels))
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


class SimpleTextDatasets(TextDatasets):
    def __init__(self, params, train_texts, train_labels, test_texts, test_labels, vectorizer,
                 batch_size=None, name='SimpleTextDatasets'):
        super().__init__(params, train_texts, train_labels, test_texts, test_labels, vectorizer,
                         batch_size, name)


class SequenceTextDatasets(TextDatasets):
    def __init__(self, params, train_texts, train_labels, test_texts, test_labels, vectorizer,
                 batch_size=None, name='SequenceTextDatasets'):
        super().__init__(params, train_texts, train_labels, test_texts, test_labels, vectorizer,
                         batch_size, name)

    def get_datasets(self, random_state=42):
        X_train, X_val, y_train, y_val = self._get_train_val(random_state)

        test_dataset = tf.data.Dataset.from_tensor_slices((self.test_data, self.test_labels))
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
