代码参见 http://15.15.174.138:28888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/55-pytorch/tutorials/introduction_to_pytorch.ipynb

# [安装](https://pytorch.org/get-started/locally/mm)

~~~shell
pip3 install -U torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
~~~

Verify

~~~
import torch

x = torch.rand(5, 3)
print(x)
print(f'torch.__version__={torch.__version__}') 
print(f'torch.cuda.is_available()={torch.cuda.is_available()}')
~~~

# [快速入门](https://pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html)

第一个PyTorch模型。从获取数据，创建模型，训练预测。

# [TENSOR](https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html)

# [DATASET 和 DATALOADER](https://pytorch.org/tutorials/beginner/basics/data_tutorial.html)

Dataset stores the samples and their corresponding labels, and DataLoader wraps an iterable around the Dataset to enable easy access to the samples.

PyTorch内置的数据集参见： [Image Datasets](https://pytorch.org/vision/stable/datasets.html), [Text Datasets](https://pytorch.org/text/stable/datasets.html), and [Audio Datasets](https://pytorch.org/audio/stable/datasets.html)

# [自动微分](https://pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html)

<img src="images/comp-graph.png" alt="img" style="zoom:150%;" />
