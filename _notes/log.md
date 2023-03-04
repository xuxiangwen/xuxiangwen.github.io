

## 任务

- 机器学习培训课程

  - Machine Learning Introduction: 30 hours
  - Deep Learning Introduction: 90 hours
    - Neural Network: 30 hours
    - Nature Learning Introduction: 30 hours
    - Computer Vision Introduction: 30 hours

- 在线考试系统: 30 hours

- [Reinforcement Learning Specialization](https://www.coursera.org/specializations/reinforcement-learning)

  - [Fundamentals of Reinforcement Learning](https://www.coursera.org/learn/fundamentals-of-reinforcement-learning?specialization=reinforcement-learning) : 30 hours

    1/30,2023-1-8; 

  - [Sample-based Learning Methods](https://www.coursera.org/learn/sample-based-learning-methods?specialization=reinforcement-learning): 30 hours

  - [Prediction and Control with Function Approximation](https://www.coursera.org/learn/prediction-control-function-approximation?specialization=reinforcement-learning): 30 hours

  - [A Complete Reinforcement Learning System (Capstone)](https://www.coursera.org/learn/complete-reinforcement-learning-system?specialization=reinforcement-learning): 30 hours

- [Machine Learning Specialization](https://www.coursera.org/specializations/machine-learning-introduction)

  - [Advanced Learning Algorithms](https://www.coursera.org/learn/advanced-learning-algorithms?specialization=machine-learning-introduction): 30 hours

    1/30,2023-1-8; 3/30,2023-1-14; 

  - [Unsupervised Learning, Recommenders, Reinforcement Learning](https://www.coursera.org/learn/unsupervised-learning-recommenders-reinforcement-learning): 30 hours

- TensorFlow Book

  

- RASA Book

## 时间安排

### 2023-02-23

- 每天平均5.5小时。

- 每周学习时间要在40小时。
- 一个月160小时，
- 一年2000小时。这样理论上5年就可以达到1万小时。

#### 周一到周五+在家

学习：2.5-4.5-6.5

05:30-05:45 洗漱
05:45-07:15 学习 
07:15-07:30 早饭
07:30-08:30 学习
08:30-09:30 锻炼/学习
09:30-11:00 学习/工作
11:00-11:30 午饭
11:30-13:30 工作
13:30-15:30 学习/工作
15:30-18:30 工作/学习
18:30-19:30 晚饭
19:30-20:30 工作
20:30-21:30 锻炼/工作
21:30-22:15 陪伴孩子
22:15-22:30 洗漱
22:30-05:30 睡觉

周四晚上踢球。
周五晚上玩1-2个小时游戏。

#### 周末+在家

学习：6.5-8.5-10.5

05:30-05:45 洗漱
05:45-08:15 学习
08:15-08:30 早饭
08:30-11:30 学习
11:30-12:30 做饭/学习
12:30-13:00 午饭
13:00-16:30 学习
16:30-19:30 锻炼+休息+晚饭
19:30-20:30 游戏/学习
20:30-22:15 学习/游戏
22:15-22:30 洗漱
22:30-05:30 睡觉

#### 周末+上海图书馆

学习：7-9-11

05:30-05:45 洗漱
05:45-08:15 学习
08:15-08:30 早饭
08:30-09:30 早饭+图书馆途中
09:30-12:30 学习
12:30-14:00 午饭+休息
14:00-18:00 学习
18:00-19:30 图书馆途中+晚饭
19:30-20:30 游戏/学习
20:30-22:15 学习/游戏
22:15-22:30 洗漱
22:30-05:30 睡觉

#### 周末+傅雷图书馆

学习：7-9-11

05:30-05:45 洗漱
05:45-08:15 学习
08:15-08:30 早饭
08:45-09:15 图书馆途中
09:15-12:30 学习
12:30-14:00 午饭+休息
14:00-18:00 学习
18:00-19:30 图书馆途中+晚饭
19:30-20:30 游戏/学习
20:30-22:15 学习/游戏
22:15-22:30 洗漱
22:30-05:30 睡觉



## 2023-01-08

最近的计划:

- 构建在线考试系统:使用power apps来实现

​        第一个月: 估计要30个小时

- 完成机器学习培训课程: 4个月

  - 创建机器学习课程
    - Machine Learning Introduction: 第一个月
      - 估计30个小时
    - Deep Learning Introduction: 第二个月
      - 估计40个小时
    - Nature Learning Introduction: 第三个月
      - 估计40个小时
    - Computer Vision Introduction: 第四个月
      - 估计40个小时
  
  - 时间: 每天投入两个小时在这个上面。
    - 第一个月:
      - 在线考试系统:1个小时
      - Machine Learning Introduction:1个小时
  
- 强化学习: https://www.coursera.org/specializations/reinforcement-learning#courses: 2个月

  总共四个课程，每个课程都需要4周时间

  - 时间: 每天1个小时

- Machine Learning Specialization: 2个月

  - Course:
    - [Advanced Learning Algorithms](https://www.coursera.org/learn/advanced-learning-algorithms?specialization=machine-learning-introduction)
      - 30 hours
    - [Unsupervised Learning, Recommenders, Reinforcement Learning](https://www.coursera.org/learn/unsupervised-learning-recommenders-reinforcement-learning)
      - 30 hours
  - 时间: 每天1个小时

## 2022-02-22

一个非常好的学习网站，楼主是一个百度的工程师。

https://www.captainai.net/

## 2021-12-05

### TextVectorization保存和恢复

这两天好好研究了一下 TextVectorization的保存，恢复问题。详见:http://15.15.175.163:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/text_classification/save_load_textvectorization.ipynb#save-and-load-test

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

