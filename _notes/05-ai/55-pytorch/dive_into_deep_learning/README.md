[Dive into Deep Learning (D2L.ai) · GitHub](https://github.com/d2l-ai)

## 前言

- 书： 
  - [《动手学深度学习》 — 动手学深度学习 2.0.0 documentation](https://zh.d2l.ai/)
  - [Dive into Deep Learning — Dive into Deep Learning 1.0.3 documentation](https://d2l.ai/)

## 安装

~~~
conda create --name d2l python=3.9 -y

conda activate d2l
pip install torch==2.0.0 torchvision==0.15.1 --index-url https://download.pytorch.org/whl/cu118
pip install d2l==1.0.3
pip install jupyterlab
~~~

~~~
mkdir d2l-en && cd d2l-en
curl https://d2l.ai/d2l-en-1.0.3.zip -o d2l-en.zip
unzip d2l-en.zip && rm d2l-en.zip
cd pytorch
~~~

~~~
conda activate d2l
jupyter lab --FileContentsManager.checkpoints_kwargs="root_dir"="/tmp"  --port=58888
~~~

