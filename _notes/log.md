

## 2021-12-05

### TextVectorization保存和恢复

这两天好好研究了一下 TextVectorization的保存，恢复问题。详见：http://15.15.175.163:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/text_classification/save_load_textvectorization.ipynb#save-and-load-test

[以前的代码](https://github.com/xuxiangwen/qbz95/blob/master/qbz95/tf/classification/text_generator.py)在tf2.5下没有问题。

~~~python
class LayerGenerator(DatasetGenerator):
    @classmethod
    def get_ngram_layer(cls, name, standardize, texts, max_features):
        ngrams = (1, 2)
        output_mode = 'tf-idf'
        max_sequence_length = None
        return LayerGenerator(name, standardize, texts, max_features,
                              ngrams=ngrams, output_mode=output_mode,
                              max_sequence_length=max_sequence_length)

    @classmethod
    def get_sequence_layer(cls, name, standardize, texts, max_features, max_sequence_length):
        ngrams = None
        output_mode = 'int'
        return LayerGenerator(name, standardize, texts, max_features,
                              ngrams=ngrams, output_mode=output_mode,
                              max_sequence_length=max_sequence_length)

    def __init__(self, name, standardize, texts, max_features,
                 ngrams, output_mode, max_sequence_length):
        super().__init__(name)
        self.standardize = standardize
        self.layer = TextVectorization(
            max_tokens=max_features, standardize='lower_and_strip_punctuation',
            split='whitespace', ngrams=ngrams, output_mode=output_mode,
            output_sequence_length=max_sequence_length, pad_to_max_tokens=False,
            vocabulary=None
        )

        texts = [standardize(text) for text in texts]
        self.layer.adapt(texts)
        self.layer_path = None

    def map(self, text):
        text = self.standardize(text)
        texts = tf.expand_dims(text, axis=-1)
        sequences = self.layer([texts])[0]
        return sequences

    def before_pickle(self, pickle_path):
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Input(shape=(1,), dtype=tf.string))
        model.add(self.layer)

        self.layer_path = os.path.join(os.path.dirname(pickle_path), self.name + '.layer')
        model.save(self.layer_path, save_format="tf")
        return self

    def after_pickle(self, generator_path):
        if not os.path.exists(self.layer_path):
            self.layer_path = generator_path.replace('.generator', '.layer')
            print(self.layer_path)
        model = tf.keras.models.load_model(self.layer_path)
        self.layer = model.layers[0]
        return self

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["layer"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
~~~

​	但在tf2.7报错如下:

~~~


~~~

