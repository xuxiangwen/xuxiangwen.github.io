#!/usr/bin/env python

import logging
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
import time

from IPython.display import display, Image
from sklearn.metrics import confusion_matrix
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

    def get_similar_attribute(self, names):
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


def image_data_generator():
    datagen = preprocessing.image.ImageDataGenerator(
        # set input mean to 0 over the dataset
        featurewise_center=False,
        # set each sample mean to 0
        samplewise_center=False,
        # divide inputs by std of dataset
        featurewise_std_normalization=False,
        # divide each input by its std
        samplewise_std_normalization=False,
        # apply ZCA whitening
        zca_whitening=False,
        # randomly rotate images in the range (deg 0 to 180)
        rotation_range=15,
        # randomly shift images horizontally
        width_shift_range=0.05,
        # randomly shift images vertically
        height_shift_range=0.05,
        # randomly flip images
        horizontal_flip=False,
        # randomly flip images
        vertical_flip=False
    )    
    return datagen     


class ImageClassificationHelper(object):
    
    def __init__(self, params, data, model_results={}):
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
        
    def train(self, model, callbacks=None, epochs=None, verbose=True):
        """要求模型设置name属性，用于保存模型。"""
        if epochs is None:
            epochs = self.params.epochs
        if callbacks is None:
            callbacks = self.get_callbacks(model, verbose)

        if self.data.val_dataset is None:
            validation_dataset = self.data.test_dataset
        else:
            validation_dataset = self.data.val_dataset          

        with TaskTime('training', True) as t: 
            if self.params.use_data_augmentation:
                print('use data augmentation')
                steps_per_epoch = self.data.train_dataset_aug.steps_per_epoch
                history = model.fit(self.data.train_dataset_aug, validation_data=validation_dataset, 
                                    epochs=epochs, verbose=verbose, steps_per_epoch=steps_per_epoch,
                                    callbacks=callbacks)
            else:
                history = model.fit(self.data.train_dataset, validation_data=validation_dataset, 
                                    epochs=epochs, verbose=verbose, 
                                    callbacks=callbacks)
            history.train_time = t.elapsed_time()
        plot_history(history)
        return history  
    
    def compile(self, model):
        learning_rate = self.get_learning_rate(model.name)
        print('learning_rate={}'.format(learning_rate))
        model.compile(optimizer=optimizers.Adam(learning_rate=learning_rate),
                      loss=losses.SparseCategoricalCrossentropy(from_logits=True),
                      metrics=self.params.metrics)

        dataset_path = './checkpoints/{}'.format(self.params.dataset_name)
        model.checkpoint_path = '{}/{}/checkpoint'.format(dataset_path, model.name)
        print('checkpoint_path={}'.format(model.checkpoint_path))
        return model    
                                                         
    def evaluate(self, model, train_time, train_dataset=None, val_dataset=None, test_dataset=None):
        """评估当前模型，并且显示所有模型的信息"""
        model_results = self.model_results
        if train_dataset is None:
            train_dataset = self.data.train_dataset
        if val_dataset is None:
            val_dataset = self.data.val_dataset
        if test_dataset is None:
            test_dataset = self.data.test_dataset
        
        train_loss, train_accuracy = model.evaluate(train_dataset, verbose=False)
        if val_dataset is not None:
            val_loss, val_accuracy = model.evaluate(val_dataset, verbose=False)
        test_loss, test_accuracy = model.evaluate(test_dataset, verbose=False)
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
                                             'train_time': round(train_time, 0)}
            else:
                model_results[model.name] = {'train_loss': round(train_loss, 6),
                                             'train_accuracy': round(train_accuracy, 4),
                                             'test_loss': round(test_loss, 6),
                                             'test_accuracy': round(test_accuracy, 4),
                                             'weight_number': get_weight_num(model),
                                             'model': model,
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

        # 模型对比
        print('-'*40, 'model improvement'.format(model.name), '-'*40)
        self.plot_predicted_sample(model, sample_count=5, only_compare_best=True) 
        
        # 错误比较        
        if len(self.model_results.keys())>1:
            print('-'*40, 'error analysis'.format(model.name), '-'*40)
            self.plot_predicted_sample(model, sample_count=5)

        # 所有模型结果
        print('-'*50, 'all models'.format(model.name), '-'*50)
        self.show_model_results()

    def get_learning_rate(self, model_name):
        learning_rate = self.params.model_params.get_similar_attribute([model_name, 'learning_rate'])
        if learning_rate is None:
            learning_rate = self.params.learning_rate
        return learning_rate
 
    def get_dropout(self, model_name):
        dropout = self.params.model_params.get_similar_attribute([model_name, 'dropout'])
        if dropout is None:
            dropout = self.params.dropout
        return dropout   
    
    def get_best_model(self, exclude_mode_name=''):
        models = [(model_name, model_result['test_accuracy'])
                  for model_name, model_result in self.model_results.items() 
                  if model_name != exclude_mode_name]
        if len(models) == 0:
            return None
        models = sorted(models, key=lambda item: item[1])
        best_model_name = models[-1][0]
        return self.model_results[best_model_name]['model']     
        
    def show_model_results(self):
        """按照test_accuracy倒序显示所有模型的信息"""
        model_results = self.model_results
        models_remove1 = {key:{key1:value1 for key1, value1 in value.items() if key1 != 'model'} 
                          for key, value in model_results.items()}
        df_models = pd.DataFrame.from_dict(models_remove1, orient='index')
        df_models = df_models.sort_values('test_accuracy', ascending=False) 
        display(df_models)       
        
    def show_images(self, images, labels, x_num=6, y_num=6, figsize=(8,8), images_mean=None):
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

    def plot_distribution(self, train_labels=None, test_labels=None):
        """打印类的分布"""
        if train_labels is None: train_labels = self.data.train_labels
        if test_labels is None: test_labels = self.data.test_labels
            
        classes = self.data.classes
        
        def plot_dist(labels, title, color='blue', width = 0.7):
            bin_count = np.bincount(labels)
            bin_percentage = bin_count/len(labels)
            rects = plt.bar(np.arange(len(bin_count)), bin_count, width, color=color)
            plt.title(title)
            if classes is None:
                plt.xticks(range(len(bin_count))) 
            else:
                plt.xticks(range(len(bin_count)), labels=classes, rotation = 45) 
            plt.ylim(0, max(bin_count)*1.1) 

            for i, r in enumerate(rects):
                plt.annotate('{:0.1f}%'.format(int(bin_percentage[i]*100)),
                             xy=(r.get_x() + r.get_width() / 2, r.get_height()),
                             xytext=(0, 3),  # 3 points vertical offset
                             textcoords="offset points",
                             ha='center', va='bottom')

        plt.figure(figsize=(16, 4))
        plt.subplot(121)
        plot_dist(train_labels, 'Train', color='teal')
        plt.subplot(122)
        plot_dist(test_labels, 'Test', color='coral')

        plt.show()

    def plot_confusion_matrix(self, model1, images=None, labels=None, model2=None, compared=True):
        """打印混淆矩阵"""
        def plot_cm(model):
            predictions = model.predict(images).argmax(axis=-1)               
            cm = confusion_matrix(labels, predictions)
            bin_count = np.bincount(labels)
            if classes is None: 
                index = range(len(bin_count))      
                columns = range(len(bin_count))  
            else:
                index = classes     
                columns = classes           
            df_cm = pd.DataFrame(cm, index=index, columns=columns)

            plt.title("{} - Confusion matrix".format(model.name))
            sns.heatmap(df_cm, annot=True, fmt='g',cmap='coolwarm')
            if classes is not None: 
                plt.yticks(rotation = 0)
                plt.xticks(rotation = 45)
            plt.xlabel("Predicted")
            plt.ylabel("Actual")

        if images is None: images = self.data.test_images
        if labels is None: labels = self.data.test_labels 
        classes = self.data.classes
        
        if compared and model2 is None:
            model2 = self.get_best_model(model1.name)

        if model2 is not None:            
            plt.figure(figsize=(16, 6))
            plt.subplot(1, 2, 1)
            plot_cm(model2)
            plt.subplot(1, 2, 2)
            plot_cm(model1)         
        else:  
            plt.figure(figsize=(8, 6))
            plot_cm(model1)

        plt.show()    

    def plot_predicted_sample(self, model, images=None, labels=None, sample_count=5, 
                              show_error=True, images_mean=None, only_compare_best=False):
        """查看一些样本的分类情况"""
        def get_class(label):
            if classes is None:
                return label
            else:
                return classes[label]

        def plot_var(model, image, label):
            predict = np.squeeze(tf.nn.softmax(model.predict(image)).numpy())
            max_like = np.argmax(predict)
            max_like_value = predict[max_like]

            if classes is None:
                _classes = range(label_count)
                plt.text(max_like-0.5, max_like_value+0.02, 
                         '{:0.1f}%'.format(max_like_value*100), fontsize=8)            
                plt.bar(_classes, predict, width=0.9, color='steelblue', alpha=0.8) 
                plt.ylim(0, 1.2)
                plt.xticks(range(label_count), _classes, fontsize=8)          
            else:
                _classes = classes
                plt.text(max_like_value+0.02, max_like, 
                         '{:0.1f}%'.format(max_like_value*100), fontsize=8)             
                plt.barh(_classes, predict, height=0.9, color='steelblue', alpha=0.8) 
                plt.xlim(0, 1.2)
                plt.yticks(range(label_count), _classes, fontsize=8)
            plt.title('{}: {}'.format(model.name, get_class(max_like)), fontsize=10)

        if images is None: images = self.data.test_images
        if labels is None: labels = self.data.test_labels 
        classes = self.data.classes
        
        if only_compare_best:
            best_model = self.get_best_model(model.name)
            if best_model is None:
                models = [model]   
            else:
                models = [best_model, model]
        else:   
            models = [model] + [model_result['model'] for model_name, model_result in self.model_results.items() 
                      if model_name!=model.name]
        
        if show_error:
            base_predictions = models[0].predict(images).argmax(axis=-1)  
            error_indexes = base_predictions != labels
            error_images = images[error_indexes]
            error_labels = labels[error_indexes]
            sample_indexes = np.random.randint(len(error_images), size=sample_count)  
            sample_images = error_images[sample_indexes]
            sample_labels = error_labels[sample_indexes]
        else:
            sample_indexes = np.random.randint(len(labels), size=sample_count)  
            sample_images = images[sample_indexes]
            sample_labels = labels[sample_indexes]

        bin_count = np.bincount(labels)
        label_count = len(bin_count)
        column_count = len(models)+1 
        if classes is None:
            plt.figure(figsize=(2.2*column_count, sample_count*2.2))
        else:
            plt.figure(figsize=(2.8*column_count, sample_count*2.8))
        channel_count = images.shape[-1]
        for i in range(sample_count):
            plt.subplot(sample_count, column_count, column_count*i+1)        
            if images_mean is not None:
                image = sample_images[i]+images_mean
            else:
                image = sample_images[i]
            if channel_count==1:
                plt.imshow(image, cmap='gray')
            else:
                plt.imshow(image)        
            plt.title('actual: {}'.format(get_class(sample_labels[i])), fontsize=10)
            plt.xticks([])
            plt.yticks([])

            for j, model in enumerate(models):
                plt.subplot(sample_count, column_count, column_count*i+j+2)
                plot_var(model, sample_images[i:i+1], sample_labels[i])

        plt.subplots_adjust(wspace=0.5, hspace=0.5)         
        plt.show()
        

class ImageDataset(object):
    def __init__(self, params):
        super(ImageDataset, self).__init__()

        self.dataset_name = params.dataset_name
        self.batch_size = params.batch_size
        self.validation_percent = params.validation_percent
        self.augmentation_generator = params.augmentation_generator
                
        print('load {} data from source'.format(self.dataset_name))
        self.classes = self.get_classes()
        (self.train_images, self.train_labels), (self.test_images, self.test_labels) = self.load_data()
        self.input_shape = self.train_images.shape[1:]
        
        print('create train, validation and test dataset')
        self.train_dataset, self.val_dataset, self.test_dataset, self.train_dataset_aug = self.get_datasets() 

    def get_classes(self):
        dataset_name = self.dataset_name
        if dataset_name[0:len('mnist')]=='mnist':
            classes = None            
        elif dataset_name[0:len('fashion-mnist')]=='fashion-mnist':
            classes = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 
                       'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
        elif dataset_name[0:len('cifar10')]=='cifar10':
            classes = ['plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
        else:
            raise Exception('{} is not supported '.format(dataset_name))
        return classes
        
    def load_data(self):
        dataset_name = self.dataset_name
        if dataset_name[0:len('mnist')]=='mnist':
            (train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data()
        elif dataset_name[0:len('fashion-mnist')]=='fashion-mnist':
            (train_images, train_labels), (test_images, test_labels) = datasets.fashion_mnist.load_data()
        elif dataset_name[0:len('cifar10')]=='cifar10':
            (train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()
        else:
            raise Exception('{} is not supported '.format(dataset_name))
        if len(train_images.shape)<4:
            train_images = np.expand_dims(train_images, axis=-1) 
            test_images = np.expand_dims(test_images, axis=-1)

        train_labels = np.squeeze(train_labels)
        test_labels = np.squeeze(test_labels)
            
        train_images = train_images/255.0   
        test_images = test_images/255.0   
            
        print('train:', train_images.shape, train_labels.shape)
        print('test:', test_images.shape, test_labels.shape)            
        return (train_images, train_labels), (test_images, test_labels)
        
    def get_datasets(self, random_state=42):
        validation_percent = self.validation_percent
        batch_size = self.batch_size
        if validation_percent>0:
            print('split train into train and validation')
            X_train, X_val, y_train, y_val = train_test_split(self.train_images, self.train_labels, 
                                                              test_size=validation_percent, 
                                                              random_state=random_state)
            print('train:', X_train.shape, y_train.shape)
            print('validation:', X_val.shape, y_val.shape)    
        else:
            X_train, X_val, y_train, y_val = self.train_images, None, self.train_labels, None

        test_dataset = tf.data.Dataset.from_tensor_slices((self.test_images, self.test_labels))
        test_dataset = test_dataset.batch(batch_size)

        train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train))
        train_dataset = train_dataset.shuffle(len(y_train), reshuffle_each_iteration = True)
        train_dataset = train_dataset.batch(batch_size, drop_remainder=True)
        
        train_steps_per_epoch =  int(len(X_train) / batch_size)
        
        if self.augmentation_generator is not None: 
            # compute quantities required for featurewise normalization
            # (std, mean, and principal components if ZCA whitening is applied).              
            self.augmentation_generator.fit(X_train)            
            train_dataset_aug = self.augmentation_generator.flow(X_train, y_train, batch_size=batch_size, 
                                                                 shuffle=True)             
            train_dataset_aug.steps_per_epoch = int(len(X_train) / batch_size)
        else:
            train_dataset_aug = None
   
        if validation_percent>0: 
            val_dataset = tf.data.Dataset.from_tensor_slices((X_val, y_val))
            val_dataset = val_dataset.shuffle(len(y_val), reshuffle_each_iteration = True)
            val_dataset = val_dataset.batch(batch_size)
        else:
            val_dataset = None
        
        return train_dataset, val_dataset, test_dataset, train_dataset_aug

    
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
        time.sleep(0.2)
        logging.info('finish {} [elapsed time: {:.2f} seconds]'.format(self.task_name, self.elapsed_time()))   
