## Index

### [basic_text_classification.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/tensorflow_hub/basic_text_classification.ipynb)

使用tf hub来对imdb数据集进行分类。val数据集的准确率如下：

| model                                                        | trainable=False | trainable=True |
| ------------------------------------------------------------ | --------------- | -------------- |
| https://tfhub.dev/google/nnlm-en-dim50/2                     | 75.54%          | 87.11%         |
| https://tfhub.dev/google/nnlm-en-dim50-with-normalization/2  | 78.25%          | 89.32%         |
| https://tfhub.dev/google/nnlm-en-dim128/2                    | 80.28%          | 87.47%         |
| https://tfhub.dev/google/nnlm-en-dim128-with-normalization/2 | 83.57%          | 89.73%         |

trainable=True效果明显，此外去除标点符号（punctuation）的模型也要更好一些。

### [tf2_image_retraining](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/tensorflow_hub/tf2_image_retraining.ipynb)

 使用tf hub来对[flowers](https://www.tensorflow.org/datasets/catalog/tf_flowers)数据集进行分类。val数据集的准确率如下：

|                         | trainable=False | trainable=True |
| ----------------------- | --------------- | -------------- |
| data_augmentation=False | 87.93%          | 92.61%         |
| data_augmentation=True  | 88.35%          | 92.47%         |

trainable=True效果明显，data_augmentation=True模型稳定性有所提高。

### [Bangla Article Classification](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/tensorflow_hub/bangla_article_classifier.ipynb)

采用fasttext的词向量，对孟加拉语的文章进行分类。其中fasttext的词向量会转化为Tensorflow的模型。

