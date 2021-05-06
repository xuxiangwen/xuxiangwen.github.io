import fasttext
import numpy as np
import os
import pandas as pd
import pickle
import util
import tensorflow as tf
from tensorflow.keras import models


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


class TextPredictor(object):
    def __init__(self, classes):
        super().__init__()
        self.classes = classes

    def predict(self, texts):
        pass

    def evaluate(self, texts, label):
        pass

    def transform(self, texts):
        return texts

    def __setstate__(self, state):
        self.__dict__.update(state)

    def load(self, root_path_replace=None):
        pass


class TfTextPredictor(TextPredictor):

    def __init__(self, classes, model_path='', vectorizer_path='', model=None, vectorizer=None):
        super().__init__(classes)
        self.vectorizer = vectorizer
        self.model = model
        self.vectorizer_path = os.path.abspath(vectorizer_path)
        if self.model is None or self.vectorizer is None:
            self.model_path = os.path.abspath(model_path)
            self.load()
        else:
            self.model_path = os.path.abspath(self.model.checkpoint_path)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["model"]
        del state["vectorizer"]
        return state

    def load(self, root_path_replace=None):
        if root_path_replace is not None:
            self.model_path = root_path_replace(self.model_path)
            self.vectorizer_path = root_path_replace(self.vectorizer_path)
        print('model_path={}, vectorizer_path={}'.format(self.model_path, self.vectorizer_path))
        self.model = load_model(self.model_path)
        self.vectorizer = load_vectorizer(self.vectorizer_path)

    def predict(self, texts):
        data = self.transform(texts)
        return tf.nn.softmax(self.model.predict(data)).numpy()

    def evaluate(self, texts, labels):
        data = self.transform(texts)
        return self.model.evaluate(data, labels)

    def transform(self, texts):
        return self.vectorizer.transform(texts)


class FastTextPredictor(TextPredictor):

    def __init__(self, classes, model_path='', model=None):
        super().__init__(classes)
        self.no_blank_classes = ['__label__' + class_.replace(' ', '-').replace('/', '_') for class_ in self.classes]
        self.model = model
        if self.model is None:
            self.model_path = os.path.abspath(model_path)
            self.load()
        else:
            self.model_path = os.path.abspath(self.model.checkpoint_path)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["model"]
        return state

    def load(self, root_path_replace=None):
        if root_path_replace is not None:
            self.model_path = root_path_replace(self.model_path)
        self.model = fasttext.load_model(self.model_path)

    def predict_(self, texts):
        texts = self.transform(texts)
        results = self.model.predict(texts, 8)
        return results

    def predict(self, texts):
        classes = self.classes
        no_blank_classes = self.no_blank_classes

        texts = self.transform(texts)
        results = self.model.predict(texts, 8)
        results = [{classes[no_blank_classes.index(results[0][i][j])]: results[1][i][j]
                    for j in range(len(no_blank_classes))} for i in range(len(texts))]
        df = pd.DataFrame.from_records(results)
        df = df[classes]
        return df.to_numpy()

    def evaluate(self, texts, labels):
        data = self.vectorizer.transform(texts)
        return self.model.evaluate(data, labels)

    def transform(self, texts):
        return util.FastText.text_clean(texts)
