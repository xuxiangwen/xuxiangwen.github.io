```{.python .input  n=38}
%matplotlib inline
```


What is PyTorch?
================

It’s a Python-based scientific computing package targeted at two sets of
audiences:

-  A replacement for NumPy to use the power of GPUs
-  a deep learning research platform that provides maximum flexibility
   and speed

Getting Started
---------------

Tensors
^^^^^^^

Tensors are similar to NumPy’s ndarrays, with the addition being that
Tensors can also be used on a GPU to accelerate computing.


```{.python .input  n=39}
from __future__ import print_function
import torch
import numpy as np
```

<div class="alert alert-info"><h4>Note</h4><p>An uninitialized matrix is
declared,
    but does not contain definite known
    values before it is used. When an
    uninitialized matrix is created,
    whatever values were in the allocated
    memory at the time will appear as the initial values.</p></div>


Construct a 5x3 matrix, uninitialized:


```{.python .input  n=40}
x = torch.empty(5, 3)
print(x)
print(np.empty([5, 3]))
```

```{.json .output n=40}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "tensor([[ 1.4013e-45,  0.0000e+00,  6.2256e-37],\n        [ 0.0000e+00,  1.4013e-45,  0.0000e+00],\n        [ 6.2255e-37,  0.0000e+00,  3.9236e-44],\n        [ 0.0000e+00, -1.6579e+03,  4.5715e-41],\n        [ 2.8026e-45,  0.0000e+00, -1.6579e+03]])\n[[1. 1. 1.]\n [1. 1. 1.]\n [1. 1. 1.]\n [1. 1. 1.]\n [1. 1. 1.]]\n"
 }
]
```

Construct a randomly initialized matrix:


```{.python .input  n=41}
x = torch.rand(5, 3)
print(x)
print(np.random.rand(5, 3))
```

```{.json .output n=41}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "tensor([[0.6845, 0.8593, 0.5880],\n        [0.7123, 0.2612, 1.0000],\n        [0.9157, 0.2335, 0.4868],\n        [0.2518, 0.8301, 0.9084],\n        [0.1778, 0.5326, 0.4678]])\n[[0.12270794 0.90282403 0.09793327]\n [0.82293212 0.2917235  0.82864884]\n [0.95759025 0.06209456 0.76189358]\n [0.47115073 0.46481893 0.36835697]\n [0.7343888  0.38339631 0.20976805]]\n"
 }
]
```

Construct a matrix filled zeros and of dtype long:


```{.python .input  n=42}
x = torch.zeros(5, 3, dtype=torch.long)
x1 = torch.zeros(5, 3)
print(x, x.dtype)
print(x1, x1.dtype)
x2 = np.zeros([5, 3])
print(x2, (x2.dtype))


x = torch.ones(5, 3, dtype=torch.long)
x1 = torch.ones(5, 3)
print(x, x.dtype)
print(x1, x1.dtype)
x2 = np.ones([5, 3])
print(x2, (x2.dtype))
```

```{.json .output n=42}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "tensor([[0, 0, 0],\n        [0, 0, 0],\n        [0, 0, 0],\n        [0, 0, 0],\n        [0, 0, 0]]) torch.int64\ntensor([[0., 0., 0.],\n        [0., 0., 0.],\n        [0., 0., 0.],\n        [0., 0., 0.],\n        [0., 0., 0.]]) torch.float32\n[[0. 0. 0.]\n [0. 0. 0.]\n [0. 0. 0.]\n [0. 0. 0.]\n [0. 0. 0.]] float64\ntensor([[1, 1, 1],\n        [1, 1, 1],\n        [1, 1, 1],\n        [1, 1, 1],\n        [1, 1, 1]]) torch.int64\ntensor([[1., 1., 1.],\n        [1., 1., 1.],\n        [1., 1., 1.],\n        [1., 1., 1.],\n        [1., 1., 1.]]) torch.float32\n[[1. 1. 1.]\n [1. 1. 1.]\n [1. 1. 1.]\n [1. 1. 1.]\n [1. 1. 1.]] float64\n"
 }
]
```

Construct a tensor directly from data:


```{.python .input  n=43}
x = torch.tensor([5.5, 3])
print(x)
print(np.array([5.5, 3]))
print(torch.randn(5, 3))
print(np.random.randn(5, 3))
```

```{.json .output n=43}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "tensor([5.5000, 3.0000])\n[5.5 3. ]\ntensor([[ 0.1681,  0.4046, -0.6156],\n        [-0.8879, -1.3654, -0.3469],\n        [ 0.2881,  1.1445,  1.2361],\n        [ 0.3426, -1.3792,  0.1178],\n        [-1.0277,  0.4645,  0.7790]])\n[[ 0.39894275 -0.99914927 -0.17254618]\n [ 1.1450648  -1.52843905  0.4167682 ]\n [-0.31281745  2.47859307  1.25330746]\n [-0.14828477  1.05453558 -0.00555711]\n [ 0.68668069 -0.35007869  1.84621639]]\n"
 }
]
```

or create a tensor based on an existing tensor. These methods
will reuse properties of the input tensor, e.g. dtype, unless
new values are provided by user


```{.python .input  n=45}
x = x.new_ones(5, 3, dtype=torch.double)      # new_* methods take in sizes
print(x)

x = torch.randn_like(x, dtype=torch.float)    # override dtype!
print(x)                                      # result has the same size
x3= np.random.randn(*x2.shape)
print(x1)
```

```{.json .output n=45}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "tensor([[1., 1., 1.],\n        [1., 1., 1.],\n        [1., 1., 1.],\n        [1., 1., 1.],\n        [1., 1., 1.]], dtype=torch.float64)\ntensor([[-1.7399, -0.3425,  1.6261],\n        [ 1.0690, -0.0391, -0.8975],\n        [-1.6120, -0.7214, -1.6938],\n        [-1.3633, -0.5191,  1.1035],\n        [-0.8652, -1.5002, -0.0584]])\ntensor([[1., 1., 1.],\n        [1., 1., 1.],\n        [1., 1., 1.],\n        [1., 1., 1.],\n        [1., 1., 1.]])\n"
 }
]
```

Get its size:


```{.python .input  n=46}
print(x.size())
print(x1.size())
print(x2.shape)
```

```{.json .output n=46}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "torch.Size([5, 3])\ntorch.Size([5, 3])\n(5, 3)\n"
 }
]
```

<div class="alert alert-info"><h4>Note</h4><p>``torch.Size`` is in fact a tuple,
so it supports all tuple operations.</p></div>

Operations
^^^^^^^^^^
There are multiple syntaxes for operations. In the following
example, we will take a look at the addition operation.

Addition: syntax 1


```{.python .input  n=19}
y = torch.rand(5, 3)
print(x + y)
```

```{.json .output n=19}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "tensor([[-0.6111,  1.3671,  0.5913],\n        [ 0.4787,  1.5968,  1.4886],\n        [-0.2882,  0.8896,  1.7288],\n        [ 1.2267, -0.8136,  2.1499],\n        [ 0.5402,  1.6101,  1.5872]])\n"
 }
]
```

Addition: syntax 2


```{.python .input  n=20}
print(x + y)
print(torch.add(x, y))
```

```{.json .output n=20}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "tensor([[-0.6111,  1.3671,  0.5913],\n        [ 0.4787,  1.5968,  1.4886],\n        [-0.2882,  0.8896,  1.7288],\n        [ 1.2267, -0.8136,  2.1499],\n        [ 0.5402,  1.6101,  1.5872]])\ntensor([[-0.6111,  1.3671,  0.5913],\n        [ 0.4787,  1.5968,  1.4886],\n        [-0.2882,  0.8896,  1.7288],\n        [ 1.2267, -0.8136,  2.1499],\n        [ 0.5402,  1.6101,  1.5872]])\n"
 }
]
```

Addition: providing an output tensor as argument


```{.python .input  n=21}
result = torch.empty(5, 3)
torch.add(x, y, out=result)
print(result)
```

```{.json .output n=21}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "tensor([[-0.6111,  1.3671,  0.5913],\n        [ 0.4787,  1.5968,  1.4886],\n        [-0.2882,  0.8896,  1.7288],\n        [ 1.2267, -0.8136,  2.1499],\n        [ 0.5402,  1.6101,  1.5872]])\n"
 }
]
```

Addition: in-place


```{.python .input  n=22}
# adds x to y
y.add_(x)
print(y)
```

```{.json .output n=22}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "tensor([[-0.6111,  1.3671,  0.5913],\n        [ 0.4787,  1.5968,  1.4886],\n        [-0.2882,  0.8896,  1.7288],\n        [ 1.2267, -0.8136,  2.1499],\n        [ 0.5402,  1.6101,  1.5872]])\n"
 }
]
```

<div class="alert alert-info"><h4>Note</h4><p>Any operation that mutates a
tensor in-place is post-fixed with an ``_``.
    For example: ``x.copy_(y)``, ``x.t_()``, will change ``x``.</p></div>

You can use standard NumPy-like indexing with all bells and whistles!


```{.python .input  n=23}
print(x[:, 1])
```

```{.json .output n=23}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "tensor([ 1.3180,  0.9830,  0.6939, -0.9661,  1.4196])\n"
 }
]
```

Resizing: If you want to resize/reshape tensor, you can use ``torch.view``:


```{.python .input  n=24}
x = torch.randn(4, 4)
y = x.view(16)
z = x.view(-1, 8)  # the size -1 is inferred from other dimensions
print(x.size(), y.size(), z.size())
print(x2.reshape((-1, 5)))
print(x2)
```

```{.json .output n=24}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "torch.Size([4, 4]) torch.Size([16]) torch.Size([2, 8])\n[[1. 1. 1. 1. 1.]\n [1. 1. 1. 1. 1.]\n [1. 1. 1. 1. 1.]]\n[[1. 1. 1.]\n [1. 1. 1.]\n [1. 1. 1.]\n [1. 1. 1.]\n [1. 1. 1.]]\n"
 }
]
```

If you have a one element tensor, use ``.item()`` to get the value as a
Python number


```{.python .input  n=25}
x = torch.randn(1)
print(x)
print(x.item())
```

```{.json .output n=25}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "tensor([-0.7751])\n-0.7751093506813049\n"
 }
]
```

# **Read later:**


  100+ Tensor operations, including transposing, indexing, slicing,
  mathematical operations, linear algebra, random numbers, etc.,
  are described
  `here <https://pytorch.org/docs/torch>`_.

NumPy Bridge
------------

Converting a Torch Tensor to a NumPy array and vice versa is a breeze.

The Torch Tensor and NumPy array will share their underlying memory
locations (if the Torch Tensor is on CPU), and changing one will change
the other.

Converting a Torch Tensor to a NumPy Array
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


```{.python .input  n=26}
a = torch.ones(5)
print(a)
```

```{.json .output n=26}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "tensor([1., 1., 1., 1., 1.])\n"
 }
]
```

```{.python .input  n=27}
b = a.numpy()
print(b)
```

```{.json .output n=27}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "[1. 1. 1. 1. 1.]\n"
 }
]
```

See how the numpy array changed in value.


```{.python .input  n=34}
a.add_(1)
print(a)
print(b)
#print(a.add(b))  # TypeError: add_(): argument 'other' (position 1) must be Tensor, not numpy.ndarray
```

```{.json .output n=34}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "tensor([8., 8., 8., 8., 8.])\n[8. 8. 8. 8. 8.]\n"
 }
]
```

Converting NumPy Array to Torch Tensor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
See how changing the np array changed the Torch Tensor automatically


```{.python .input  n=35}
import numpy as np
a = np.ones(5)
b = torch.from_numpy(a)
np.add(a, 1, out=a)
print(a)
print(b)
```

```{.json .output n=35}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "[2. 2. 2. 2. 2.]\ntensor([2., 2., 2., 2., 2.], dtype=torch.float64)\n"
 }
]
```

```{.python .input  n=36}
x = torch.rand(5, 3)
y = torch.rand(3, 4)

x = torch.tensor([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])
x
print(x.t())
```

```{.json .output n=36}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "tensor([[ 1,  6],\n        [ 2,  7],\n        [ 3,  8],\n        [ 4,  9],\n        [ 5, 10]])\n"
 }
]
```

```{.python .input  n=37}
x = torch.randn(5, 3)
x.numpy().T
```

```{.json .output n=37}
[
 {
  "data": {
   "text/plain": "array([[ 0.7500882 ,  0.7524332 ,  0.78759205, -1.0938141 ,  0.34554777],\n       [-0.5738962 ,  0.88437074,  0.9283568 ,  0.33136606,  0.52874875],\n       [ 0.9656862 , -0.88271505,  0.54814184,  0.28887537, -1.130092  ]],\n      dtype=float32)"
  },
  "execution_count": 37,
  "metadata": {},
  "output_type": "execute_result"
 }
]
```


矩阵乘法
------------

```{.python .input  n=3}
import numpy as np
import torch
x = np.random.rand(5, 3)
y = np.random.rand(3, 2)
print(x.dot(y))
print(x @ y)
x = torch.from_numpy(x)
y = torch.from_numpy(y)
print(x.mm(y))
print(x.matmul(y))
print(x @ y)
```

```{.json .output n=3}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "[[1.42872472 0.96292429]\n [1.02580704 0.23367451]\n [0.97810907 0.90041008]\n [0.60400574 0.45028582]\n [1.23392644 0.88780968]]\n[[1.42872472 0.96292429]\n [1.02580704 0.23367451]\n [0.97810907 0.90041008]\n [0.60400574 0.45028582]\n [1.23392644 0.88780968]]\ntensor([[1.4287, 0.9629],\n        [1.0258, 0.2337],\n        [0.9781, 0.9004],\n        [0.6040, 0.4503],\n        [1.2339, 0.8878]], dtype=torch.float64)\ntensor([[1.4287, 0.9629],\n        [1.0258, 0.2337],\n        [0.9781, 0.9004],\n        [0.6040, 0.4503],\n        [1.2339, 0.8878]], dtype=torch.float64)\ntensor([[1.4287, 0.9629],\n        [1.0258, 0.2337],\n        [0.9781, 0.9004],\n        [0.6040, 0.4503],\n        [1.2339, 0.8878]], dtype=torch.float64)\n"
 }
]
```

矩阵点乘
------------

```{.python .input  n=95}
x = np.random.rand(5, 3)
y = np.random.rand(5, 1)
print(x * y)
x = torch.from_numpy(x)
y = torch.from_numpy(y)
print(x.mul(y))
print(x * y)
```

```{.json .output n=95}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "[[0.11351711 0.07132612 0.11332093]\n [0.04236096 0.0121558  0.07490655]\n [0.25871924 0.23204599 0.34242472]\n [0.49872754 0.07574644 0.58106411]\n [0.01086334 0.01054779 0.00343615]]\ntensor([[0.1135, 0.0713, 0.1133],\n        [0.0424, 0.0122, 0.0749],\n        [0.2587, 0.2320, 0.3424],\n        [0.4987, 0.0757, 0.5811],\n        [0.0109, 0.0105, 0.0034]], dtype=torch.float64)\ntensor([[0.1135, 0.0713, 0.1133],\n        [0.0424, 0.0122, 0.0749],\n        [0.2587, 0.2320, 0.3424],\n        [0.4987, 0.0757, 0.5811],\n        [0.0109, 0.0105, 0.0034]], dtype=torch.float64)\n"
 }
]
```

All the Tensors on the CPU except a CharTensor support converting to
NumPy and back.

CUDA Tensors
------------

Tensors can be moved onto any device using the ``.to`` method.


```{.python .input  n=69}
# let us run this cell only if CUDA is available
# We will use ``torch.device`` objects to move tensors in and out of GPU
if torch.cuda.is_available():
    device = torch.device("cuda")          # a CUDA device object
    x = torch.rand(5, 3)
    y = torch.ones_like(x, device=device)  # directly create a tensor on GPU
    x = x.to(device)                       # or just use strings ``.to("cuda")``
    z = x + y
    print(z)
    print(z.to("cpu", torch.double))       # ``.to`` can also change dtype together!
```

```{.json .output n=69}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "tensor([[1.0403, 1.1154, 1.6679],\n        [1.4616, 1.9931, 1.2849],\n        [1.0592, 1.1075, 1.4568],\n        [1.6452, 1.8758, 1.6133],\n        [1.5751, 1.4320, 1.6804]], device='cuda:0')\ntensor([[1.0403, 1.1154, 1.6679],\n        [1.4616, 1.9931, 1.2849],\n        [1.0592, 1.1075, 1.4568],\n        [1.6452, 1.8758, 1.6133],\n        [1.5751, 1.4320, 1.6804]], dtype=torch.float64)\n"
 }
]
```

```{.python .input}

```
