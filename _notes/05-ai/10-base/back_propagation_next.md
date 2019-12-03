
# 反向传播（Back Propagation）再谈

下面是[反向传播](./back_propagation.ipynb)一文中，推导的反向传播的公式，应该说总体比较清楚。但是当网络更加的复杂，一个layer中的激活函数更加的丰富（比如：CNN中的卷积层和池化层），要来推导反向传播的公式会更加的复杂。网络的层级越来越多，相互关系越来越复杂，这要求反向传播的时候，layer之间的耦合性越来越小。

$
\delta^{(n_l)} = \frac {\mathrm{d} J} {\mathrm{d} z^{(n_l)}}
=   {f'(z^{(n_l)})} .* J'(a^{(n_l)})
$

$ \delta^{(l)} = \frac {\mathrm{d} J} {\mathrm{d} z^{(l)}}  = (W^{(l+1)}  \ )^\mathrm{T} \cdot \delta^{(l+1)}\ .* f'(z^{(l)})    $

$ \frac {\mathrm{d} J(W)} {\mathrm{d} w^{(l)}} 
=  \delta^{(l)} \cdot  (a^{(l-1)}\ )^\mathrm{T}   $  

$ \frac {\mathrm{d} J(W)} {\mathrm{d} b^{(l)}} 
=  \delta^{(l)} \cdot u  $ 

而之前的公式计算$ \frac {\mathrm{d} J(W)} {\mathrm{d} w^{(l)}} $的时，需要间接调用$\delta^{(l+1)} $(即$ \frac {\mathrm{d} J} {\mathrm{d} z^{(l+1)}}\ $), 也就是需要知道下一层中间变量的梯度，这样其实强制了要求知道更多其他层的内容。本文中将把公式改成$ \delta^{(l)} = \frac {\mathrm{d} J} {\mathrm{d} a^{(n_l)}} $, 这样各层之间的依赖关系仅仅取决于输入输出，而和中间变量无关。这样无疑使得网络有更好的直观性。以下是推导完成的公式。

$
\delta^{(n_l)} = \frac {\mathrm{d} J} {\mathrm{d} a^{(n_l)}}
=    J'(a^{(n_l)})
$

$ \delta^{(l)} = \frac {\mathrm{d} J} {\mathrm{d} a^{(l)}}  = (W^{(l+1)}  \ )^\mathrm{T} \cdot (\delta^{(l+1)}\ .* f'(z^{(l+1)}))   $

$ \frac {\mathrm{d} J(W)} {\mathrm{d} w^{(l)}} 
=  (f'(z^{(l)}) .* \delta^{(l)}) \cdot  (a^{(l-1)}\ )^\mathrm{T}   $  

$ \frac {\mathrm{d} J(W)} {\mathrm{d} b^{(l)}} 
=  (f'(z^{(l)}) .* \delta^{(l)}) \cdot u  $ 

经过这个调整，其实计算方式和流程没有根本的变化，和之前的公式是完全等价的。但唯一的变化是更加的直观了。对于第$l$层layer来说，正向传播时，输入是$a^{(l-1)}$, 输出是$a^{(l)}$，而反向传播时， 输出是$\frac {\mathrm{d} J} {\mathrm{d} a^{(l-1)}} $，输入是 $\frac {\mathrm{d} J} {\mathrm{d} a^{(l)}} $。输入输出的方向相反，但一一对应，维度完全相同（$a^{(l-1)} $和 $\frac {\mathrm{d} J} {\mathrm{d} a^{(l-1)}}$， $a^{(l)} $和 $\frac {\mathrm{d} J} {\mathrm{d} a^{(l)}}$的维度完全相同），这样整个过程更加的直观，更好理解。

```python

```
