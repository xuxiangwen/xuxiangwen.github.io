https://pytorch.org/get-started

## Start Locally

### Installation

~~~
conda activate XXXX
pip3 install -U torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
~~~

Verification

~~~
conda activate dev312
python -c "import torch; x = torch.rand(5, 3); print(x); "
~~~

Check if CUDA is available.

~~~
x 1conda activate dev312
python -c "import torch; print(torch.cuda.is_available()); "
~~~

### Start

- Local - Windows

  ~~~
  conda activate dev312
  cd C:\Users\xu6\"OneDrive - HP Inc"\xujian
  jupyter lab --FileContentsManager.checkpoints_kwargs="root_dir"="C:\"	
  ~~~

- aa00 - Linux

  ~~~
  conda activate dev
  jupyter lab --FileContentsManager.checkpoints_kwargs="root_dir"="/tmp"
  ~~~



