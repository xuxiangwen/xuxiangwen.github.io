## Question

1. 一个家里有3口人， 请问同月出生的概率是多少？

2. 平面方程为$ w \cdot x + b = 0$，其中$w$是一个向量, 而$b$是一个常量, 求空间任意一点$x^{'}$到该平面的距离?

3. 有两个向量$$ a， b$$， 写出向量$a$在向量$b$上的投影长度的公式? 

4. 有向量$$v = \begin{bmatrix} 
   1 \\
   1 \\
   1
   \end{bmatrix},  b_1 = \begin{bmatrix} 
   2 \\
   1 \\
   0 
   \end{bmatrix},  b_2 = \begin{bmatrix} 
   1 \\
   -2 \\
   -1 
   \end{bmatrix}, b_3 = \begin{bmatrix} 
   -1 \\
   2 \\
   -5 
   \end{bmatrix} $$,  求向量$v$在以$ \begin{bmatrix}  b_1, b_2, b_3 \end{bmatrix} $为基下的坐标?

5. 以下向量是线性独立的吗?
   $$
   a = \begin{bmatrix} 
   1 \\
   2 \\
   -1
   \end{bmatrix},  b = \begin{bmatrix} 
   3 \\
   -4 \\
   5 
   \end{bmatrix},  c = \begin{bmatrix} 
   1 \\
   -8 \\
   7 
   \end{bmatrix}
   $$
   
6. A computer program is said to learn from experience E with respect to some task T and some performance measure P if its performance on T, as measured by P, improves with experience E. Suppose we feed a learning algorithm a lot of historical weather data, and have it learn to predict weather. In this setting, what is E?

     A. None of these.
    
    B. The probability of it correctly predicting a future date's weather.
    
    C. The weather prediction task.
    
    D. The process of the algorithm examining a large amount of historical weather data.
    
7. Some of the problems below are best addressed using a supervised learning algorithm, and the others with an unsupervised          learning algorithm.  Which of the following would you apply  supervised learning to?  (Select all that apply.) In each case, assume some appropriate dataset is available for your algorithm to learn from.

     A. Take a collection of 1000 essays written on the US Economy, and find a way to automatically group these essays into a small number of groups of essays that are somehow "similar" or "related".

     B.  Given 50 articles written by male authors, and 50 articles written by female authors, learn to predict the gender of a new manuscript's author (when the identity of this author is unknown).

     C. Examine a large collection of emails that are known to be spam email, to discover if there are sub-types of spam mail.

     D. Given historical data of children's ages and heights, predict children's height as a function of their age.






## Answer

1.  $\frac  {17}  {72}    $

2.  $$ \frac 1 {|w|} (w \cdot x^{'} + b) $$ ,  参见 [understand_linear_algebra.md](math\understand_linear_algebra.md) 

3.  $a \cdot \frac {b} {|b|} $ ,  参见 [understand_linear_algebra.md](math\understand_linear_algebra.md) 

4.  $$ \begin{bmatrix} 
    3/5 \\
    -1/3 \\
    -2/15
    \end{bmatrix}$$
    
5.  不是线性独立

6.  D

    Explanation: 

    T := The weather prediction task.
    P := The probability of it correctly predicting a future date's weather.
    E := The process of the algorithm examining a large amount of historical weather data.

7.  B, D

