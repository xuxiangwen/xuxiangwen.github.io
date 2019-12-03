
# 理解Tensor张量

二维及以下的张量显然可以按照矩阵的方式点乘。 高维张量间的乘法操作是对矩阵乘法的拓展。

如果T的shape是(A,B,C)那么标记T为 $T_C^{AB}$

矩阵乘法可以表示为指标缩并（可以想象成上下抵消了）: $X^A_BY^B_C=M_C^A$

向量内积有了很漂亮的表示（1可以不写）: $X_BY^B=C$

推广一下可以得到张量的乘法规则： $X^{ABC}_I\ Y^{DEI}_F=Z_F^{ABCDE}$

具体算法是：$Z[a,b,c,d,e,f]=\sum_i X[a,b,c,i]∗Y[d,e,i,f]$

- $\href {http://suquark.github.io/deep_learning/2016/07/04/insight-into-a-dl-frontend-1.html} {深入理解 Deep\  Learning 前端框架 (I)} $

```python

```

