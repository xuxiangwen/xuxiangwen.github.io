```{.python .input}
%matplotlib inline
```


Autograd: Automatic Differentiation
===================================

Central to all neural networks in PyTorch is the ``autograd`` package.
Let’s first briefly visit this, and we will then go to training our
first neural network.


The ``autograd`` package provides automatic differentiation for all operations
on Tensors. It is a define-by-run framework, which means that your backprop is
defined by how your code is run, and that every single iteration can be
different.

Let us see this in more simple terms with some examples.

Tensor
--------

``torch.Tensor`` is the central class of the package. If you set its attribute
``.requires_grad`` as ``True``, it starts to track all operations on it. When
you finish your computation you can call ``.backward()`` and have all the
gradients computed automatically. The gradient for this tensor will be
accumulated into ``.grad`` attribute.

To stop a tensor from tracking history, you can call ``.detach()`` to detach
it from the computation history, and to prevent future computation from being
tracked.

To prevent tracking history (and using memory), you can also wrap the code block
in ``with torch.no_grad():``. This can be particularly helpful when evaluating a
model because the model may have trainable parameters with
``requires_grad=True``, but for which we don't need the gradients.

There’s one more class which is very important for autograd
implementation - a ``Function``.

``Tensor`` and ``Function`` are interconnected and build up an acyclic
graph, that encodes a complete history of computation. Each tensor has
a ``.grad_fn`` attribute that references a ``Function`` that has created
the ``Tensor`` (except for Tensors created by the user - their
``grad_fn is None``).

If you want to compute the derivatives, you can call ``.backward()`` on
a ``Tensor``. If ``Tensor`` is a scalar (i.e. it holds a one element
data), you don’t need to specify any arguments to ``backward()``,
however if it has more elements, you need to specify a ``gradient``
argument that is a tensor of matching shape.


```{.python .input  n=1}
import torch
```

Create a tensor and set ``requires_grad=True`` to track computation with it


```{.python .input  n=2}
x = torch.ones(2,1,requires_grad=True)
print(x, x.shape)
z = (x.T + 0.1).sum()
print(z, z.size())
z.backward()
print(x.grad)
```

```{.json .output n=2}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "tensor([[1.],\n        [1.]], requires_grad=True) torch.Size([2, 1])\ntensor(2.2000, grad_fn=<SumBackward0>) torch.Size([])\ntensor([[1.],\n        [1.]])\n"
 }
]
```

```{.python .input  n=3}
x = torch.ones(2, 2, requires_grad=True)
print(x)
```

```{.json .output n=3}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "tensor([[1., 1.],\n        [1., 1.]], requires_grad=True)\n"
 }
]
```

Do a tensor operation:


```{.python .input  n=4}
y = x + 2
print(y)
```

```{.json .output n=4}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "tensor([[3., 3.],\n        [3., 3.]], grad_fn=<AddBackward0>)\n"
 }
]
```

``y`` was created as a result of an operation, so it has a ``grad_fn``.


```{.python .input  n=5}
print(y.grad_fn)
```

```{.json .output n=5}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "<AddBackward0 object at 0x7fb4abf76160>\n"
 }
]
```

Do more operations on ``y``


```{.python .input  n=8}
z = y * y * 3
out = z.mean()

print(z, out)
```

```{.json .output n=8}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "tensor([[27., 27.],\n        [27., 27.]], grad_fn=<MulBackward0>) tensor(27., grad_fn=<MeanBackward0>)\n"
 }
]
```

``.requires_grad_( ... )`` changes an existing Tensor's ``requires_grad``
flag in-place. The input flag defaults to ``False`` if not given.


```{.python .input  n=10}
a = torch.randn(2, 2)
a = ((a * 3) / (a - 1))
print(a)
print(a.requires_grad)
a.requires_grad_(True)
print(a.requires_grad)
b = (a * a).sum()
print(b.grad_fn)
```

```{.json .output n=10}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "tensor([[ 0.0298,  0.8227],\n        [ 1.7963, -0.6852]])\nFalse\nTrue\n<SumBackward0 object at 0x7f9da6809c88>\n"
 }
]
```

Gradients
---------
Let's backprop now.
Because ``out`` contains a single scalar, ``out.backward()`` is
equivalent to ``out.backward(torch.tensor(1.))``.


```{.python .input  n=7}
out.backward()
```

Print gradients d(out)/dx



```{.python .input  n=8}
print(x.grad)
```

```{.json .output n=8}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "tensor([[4.5000, 4.5000],\n        [4.5000, 4.5000]])\n"
 }
]
```

You should have got a matrix of ``4.5``. Let’s call the ``out``
*Tensor* “$o$”.
We have that $o = \frac{1}{4}\sum_i z_i$,
$z_i = 3(x_i+2)^2$ and $z_i\bigr\rvert_{x_i=1} = 27$.
Therefore,
$\frac{\partial o}{\partial x_i} = \frac{3}{2}(x_i+2)$, hence
$\frac{\partial o}{\partial x_i}\bigr\rvert_{x_i=1} = \frac{9}{2} = 4.5$.


Mathematically, if you have a vector valued function $\vec{y}=f(\vec{x})$,
then the gradient of $\vec{y}$ with respect to $\vec{x}$
is a Jacobian matrix:

\begin{align}J=\left(\begin{array}{ccc}
   \frac{\partial y_{1}}{\partial x_{1}} & \cdots & \frac{\partial
y_{1}}{\partial x_{n}}\\
   \vdots & \ddots & \vdots\\
   \frac{\partial y_{m}}{\partial x_{1}} & \cdots & \frac{\partial
y_{m}}{\partial x_{n}}
   \end{array}\right)\end{align}

Generally speaking, ``torch.autograd`` is an engine for computing
vector-Jacobian product. That is, given any vector
$v=\left(\begin{array}{cccc} v_{1} & v_{2} & \cdots &
v_{m}\end{array}\right)^{T}$,
compute the product $v^{T}\cdot J$. If $v$ happens to be
the gradient of a scalar function $l=g\left(\vec{y}\right)$,
that is,
$v=\left(\begin{array}{ccc}\frac{\partial l}{\partial y_{1}} & \cdots &
\frac{\partial l}{\partial y_{m}}\end{array}\right)^{T}$,
then by the chain rule, the vector-Jacobian product would be the
gradient of $l$ with respect to $\vec{x}$:

\begin{align}J^{T}\cdot v=\left(\begin{array}{ccc}
   \frac{\partial y_{1}}{\partial x_{1}} & \cdots & \frac{\partial
y_{m}}{\partial x_{1}}\\
   \vdots & \ddots & \vdots\\
   \frac{\partial y_{1}}{\partial x_{n}} & \cdots & \frac{\partial
y_{m}}{\partial x_{n}}
   \end{array}\right)\left(\begin{array}{c}
   \frac{\partial l}{\partial y_{1}}\\
   \vdots\\
   \frac{\partial l}{\partial y_{m}}
   \end{array}\right)=\left(\begin{array}{c}
   \frac{\partial l}{\partial x_{1}}\\
   \vdots\\
   \frac{\partial l}{\partial x_{n}}
   \end{array}\right)\end{align}

(Note that $v^{T}\cdot J$ gives a row vector which can be
treated as a column vector by taking $J^{T}\cdot v$.)

This characteristic of vector-Jacobian product makes it very
convenient to feed external gradients into a model that has
non-scalar output.


Now let's take a look at an example of vector-Jacobian product:


```{.python .input  n=18}
x = torch.randn(3,  4)
print(x.reshape(-1,2))
print(x)
print(x.view(-1,2))
```

```{.json .output n=18}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "tensor([[-0.6336,  0.4542],\n        [-1.5153, -0.0313],\n        [ 0.4923, -0.1952],\n        [-2.0243, -0.9480],\n        [-0.5353,  2.0170],\n        [-0.0465, -1.1799]])\ntensor([[-0.6336,  0.4542, -1.5153, -0.0313],\n        [ 0.4923, -0.1952, -2.0243, -0.9480],\n        [-0.5353,  2.0170, -0.0465, -1.1799]])\ntensor([[-0.6336,  0.4542],\n        [-1.5153, -0.0313],\n        [ 0.4923, -0.1952],\n        [-2.0243, -0.9480],\n        [-0.5353,  2.0170],\n        [-0.0465, -1.1799]])\n"
 }
]
```

```{.python .input  n=26}
x = torch.randn(3, requires_grad=True)
y = x * 2

while y.data.norm() < 1000:
    y = y * 2

print(y)
y.backward(v)

print(x.grad)
```

```{.json .output n=26}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "tensor([-152.5546, 1221.4625,  376.9223], grad_fn=<MulBackward0>)\ntensor([5.1200e+01, 5.1200e+02, 5.1200e-02])\n"
 }
]
```

Now in this case ``y`` is no longer a scalar. ``torch.autograd``
could not compute the full Jacobian directly, but if we just
want the vector-Jacobian product, simply pass the vector to
``backward`` as argument:


```{.python .input  n=25}
v = torch.tensor([0.1, 1.0, 0.0001], dtype=torch.float)
y.backward(v)

print(x.grad)
```

```{.json .output n=25}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "tensor([4.0960e+02, 4.0960e+03, 4.0960e-01])\n"
 }
]
```

You can also stop autograd from tracking history on Tensors
with ``.requires_grad=True`` by wrapping the code block in
``with torch.no_grad():``


```{.python .input  n=59}
print(x.requires_grad)
print((x ** 2).requires_grad)

with torch.no_grad():
    print((x ** 2).requires_grad)
    print(x.requires_grad)
```

```{.json .output n=59}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "True\nTrue\nFalse\nTrue\n"
 }
]
```

**Read Later:**

Document about ``autograd.Function`` is at
https://pytorch.org/docs/stable/autograd.html#function

