https://pytorch.org/get-started

## Start Locally

### Installation

~~~
conda activate XXXX
pip install -U torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install jupyterlab
~~~

Verification

~~~
conda activate dev312
python -c "import torch; x = torch.rand(5, 3); print(x); "
~~~

Check if CUDA is available.

~~~
conda activate dev312
python -c "import torch; print(torch.cuda.is_available()); "
~~~

### Start

- Local - Windows

  ~~~
  conda activate dev312
  cd C:\Users\xu6\"OneDrive - HP Inc"\xujian
  jupyter lab --FileContentsManager.checkpoints_kwargs="root_dir"="C:\"	
  ~~~

  http://localhost:8888/

- aa00 - Linux

  ~~~
  conda activate dev
  jupyter lab --FileContentsManager.checkpoints_kwargs="root_dir"="/tmp"
  ~~~

## Learn the Basics

0. [Quickstart](https://pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html)
1. [Tensors](https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html)
2. [Datasets and DataLoaders](https://pytorch.org/tutorials/beginner/basics/data_tutorial.html)
3. [Transforms](https://pytorch.org/tutorials/beginner/basics/transforms_tutorial.html)
4. [Build Model](https://pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html)
5. [Automatic Differentiation](https://pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html)
6. [Optimization Loop](https://pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)
7. [Save, Load and Use Model](https://pytorch.org/tutorials/beginner/basics/saveloadrun_tutorial.html)

[Deep Learning with PyTorch: A 60 Minute Blitz](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)

