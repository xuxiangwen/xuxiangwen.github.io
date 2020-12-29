---
# generated from _notes/05-ai/05-math/feature_selectio_chi_square.md

title: 特征选择：卡方检验
categories: statistics
date: 2020-12-28
---

在机器学习中，特征选择是从所有特征中选出相关特征 (*relevant feature*)，或者说在不引起重要信息丢失的前提下去除掉无关特征 (*irrelevant feature*) 和冗余特征 (*redundant feature*)。对于分类问题，在过滤方法中一般假设与标签独立的特征为无关特征，而卡方检验恰好可以进行这种独立性检验。

## 卡方分布

在进行卡方检验之前，让我们先看看卡方分布。

设随机变量 $x_1,x_2...x_n,\ i.i.d∼N(0,1)$，即独立同分布于标准正态分布，那么这 $n$ 个随机变量的平方和：

$$

X = \sum\limits_{i=1}^n x_i^2

$$

构成一个新的随机变量，其服从自由度为 $n$ 的卡方分布 ( $\chi^2$分布) ，记为$X \sim \chi^2_n$。

> *i.i.d.*指独立同分布independent and identically distributed

下图显示不同自由度下卡方分布的概率密度曲线，可以看到自由度越大，卡方分布就越接近正态分布：

![img](/assets/images/Chi-square_pdf.svg)

## 实例分析

下面在实例中使用卡方检验来筛查特征。数据是来自于[1994年美国的人口普查数据](https://www.kaggle.com/uciml/adult-census-income?select=adult.csv)，其包含了人们的年龄，工作类型，教育，婚姻，人种，性别，每周工作时长，国家，收入等信息。我们的目标是根据这些信息预测收入（income），在建模之前，需要剔除找出那些和收入无关的特征。

### 数据

引入要使用的包。

~~~python
import logging
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shutil
import six.moves.urllib as urllib
import zipfile

from IPython.display import display
from PIL import Image
from scipy import stats
from sklearn.feature_selection import SelectKBest 
from sklearn.preprocessing import LabelBinarizer
from sklearn.utils.extmath import safe_sparse_dot
from sklearn.utils import check_array

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)

np.set_printoptions(suppress=True)
~~~

下载并加载数据。

~~~python
def aduit_census_download(target_path, source_url="http://archive.ics.uci.edu/ml/machine-learning-databases/adult", http_proxy=None):
    if http_proxy is not None:
        proxy_handler = urllib.request.ProxyHandler({'http': http_proxy, 'https': http_proxy})
        opener = urllib.request.build_opener(proxy_handler)
    else:
        opener = urllib.request.build_opener()

    urllib.request.install_opener(opener)

    def maybe_download(file_name):
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        file_path = os.path.join(target_path, file_name)
        if not os.path.exists(file_path):
            source_file_url = os.path.join(source_url, file_name)
            logging.info(source_file_url)
            filepath, _ = urllib.request.urlretrieve(source_file_url, file_path)
            statinfo = os.stat(filepath)
            logging.info('Successfully downloaded {} {} bytes.'.format(file_name, statinfo.st_size))
        return file_path
    
    csv_file = 'adult.data'
    data_path= maybe_download(csv_file)
    
    extract_path = os.path.join(target_path, csv_file)
    return extract_path

local_path = os.path.join('.', 'data/adult_census')
data_path = aduit_census_download(local_path)

cols = ['age', 'workclass', 'fnlwg', 'education', 'education-num', 
       'marital-status','occupation','relationship', 'race','sex',
       'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income']
df_census = pd.read_csv(data_path, names=cols, sep=', ', engine='python')
df_census.head(5)

~~~

![image-20201228164408318](/assets/images/image-20201228164408318.png)

在分析之前，我们对数据进行一些整理。对age和hour-per-week进行分箱（bin）处理。

~~~python
def process_hours(df):
    cut_points = [0,9,19,29,39,49,1000]
    label_names = ["0-9","10-19","20-29","30-39","40-49","50+"]
    df["hours"] = pd.cut(df["hours-per-week"],
                         cut_points, labels=label_names)
    return df

def process_age(df):
    cut_points = [0,20,40,60,200]
    label_names = ["0-20","21-40","41-60","60+"]
    df["age_"] = pd.cut(df["age"],cut_points, labels=label_names)
    return df

df_census = process_hours(df_census)
df_census = process_age(df_census)
df_census.head(5)
~~~

![image-20201228164337046](/assets/images/image-20201228164337046.png)

### 工作时长 vs. 收入

下面以工作时长（hours）和收入（income）为例，分析它们的独立性关系。下面基本的一些统计信息。

~~~python
def get_observed(df, column1, column2):
    df_observed = pd.crosstab(
        df[column1],
        df[column2]
    )    
    return df_observed
    
def plot_distribution(df, columns, target_column, column_count = 3, width=18, row_height=5.5):
    def plot_one(ax, column1, column2):
        df_observed = get_observed(df, column1, column2)
        df_observed.plot.bar(stacked=True, rot=45, ax =ax, fontsize=10)
        
    if type(columns)!=list: columns = [columns]
    row_count = (len(columns)-1)//column_count + 1
    plt.figure(figsize=(width, row_count*row_height))
    for i, column in enumerate(columns):
        ax = plt.subplot(row_count, column_count, i+1)
        plot_one(ax, column, target_column)
    plt.subplots_adjust(wspace=0.3, hspace=0.5)             
    plt.show()

column1 = 'hours'
column2 = 'income'

print('-'*50)
print(df_census[column1].value_counts())
print('-'*50)
print(df_census[column2].value_counts())

print('-'*50)
plot_distribution(df_census, column1, column2)

df_observed = get_observed(df_census, column1, column2)
display(df_observed)
~~~

![image-20201228155606255](/assets/images/image-20201228155606255.png)

![image-20201228155619787](/assets/images/image-20201228155619787.png)

从上面信息，我们可以看到：

- 高收入人较少。\>50K​收入的人只有<=50K收入的人的$\frac  1 3$ 。
- 绝大多数人工作时长的区间是40-49小时。
- 随着年龄的增加，收入也逐步增加。

从上面的图可以看到，income和hours是由一定相关性的，但这种相关性有多大呢，这可以用卡方检验来衡量。首先需要建立独立性检验的假设：

- 零假设 $H_0$：收入与工作时长倾向独立
- 备选假设 $H_1$：收入与工作时长倾向独立

卡方检验需要建立两个列联表，一个是实际的频数表，一个是期望频数表。上文我们已经统计得到了实际的频数表，下面来计算期望的频数表。

~~~python
def show_sum(df):
    df.columns =  df.columns.tolist()  
    df = df.reset_index()
    s = df.melt(df.columns[0], var_name=' ')
    ct = pd.crosstab(index=s[df.columns[0]], columns=s.iloc[:,1], values=s.value, 
                     aggfunc='sum', margins=True, margins_name='合计',
                     rownames=[''], 
               ) 
    display(ct)

def get_expected(df_observed):
    observed = df_observed.to_numpy()
    reduce_row = observed.sum(axis=0, keepdims=True)/observed.sum()
    reduce_col = observed.sum(axis=1, keepdims=True)

    expected = reduce_col.dot(reduce_row)
    df_expected = pd.DataFrame(expected, index=df_observed.index, columns=df_observed.columns)
    return df_expected

print('-'*25, 'Observed', '-'*25)
show_sum(df_observed)

df_expected = get_expected(df_observed)

print('-'*25, 'Expected', '-'*25)
show_sum(df_expected)
~~~

![image-20201228141725103](/assets/images/image-20201228141725103.png)

> 在Expected中， 根据所有样本的统计，可以计算出两种收入的概率分别是$\frac {24720} {32561},\frac {7841} {32561}$，然后根据这个概率，计算出如下期望频数表。比如：第一个格子的期望频数为 $\frac {24720} {32561}*458=347.709223 $。

有了这两个列联表后，就可以构建检验统计量 $\chi^2$ 。

$$

\begin{align}
\chi^2 &= \sum\frac{(观测频数 - 期望频数)^2}{期望频数} \\
&= \sum_{i=1}^{r} \sum_{j=1}^{c} {(O_{i,j} - E_{i,j})^2 \over E_{i,j}}
\end{align}

$$

其中$r$为行数，$c $为列数，自由度 $df$为 $(6−1)×(2−1)=5$ 。

$\chi^2$ 越大，表示观测值和理论值相差越大，当$\chi^2$大于某一个临界值（critical_value）时，就能获得统计显著性的结论。

~~~python
observed = df_observed.to_numpy()
expected = df_expected.to_numpy()

chi_squared_stat = ((observed-expected)**2/expected).sum()
print('chi_squared_stat =', chi_squared_stat)

df = np.prod(np.array(observed.shape) - 1)
critical_value  = stats.chi2.ppf(q=0.95, df=df)  #0.95:置信水平, df:自由度
print('critical_value =', critical_value)        #临界值:拒绝域的边界, 当卡方值大于临界值，则原假设不成立，备择假设成立

p_value = 1 - stats.chi2.cdf(x=chi_squared_stat, df=df)
print('p_value =', p_value)
~~~

![image-20201228145805689](/assets/images/image-20201228145805689.png)

上面结果可以看到，$\chi^2$ 大大超过了临界值，这说明我们必须解决原假设，备择假设成立，也就是说，工作时长 和 收入并不是独立的，如果要预测收入，我们不应该剔除该特征。上面的代码，scipy中也提供了直接的函数，可以直接求得。

~~~python
stats.chi2_contingency(df_observed.to_numpy())
~~~

![image-20201228150101198](/assets/images/image-20201228150101198.png)

上面结果中有四项，分别对应$\chi^2$值 ，p值，自由度，期望频数表。

### 离散特征选取

人口普查数据中，还有很多其它（离散）特征，我们也想检验它们和收入的独立关系。首先来看一看这些特征的分布。

~~~python
columns = ['workclass', 'education', 'marital-status', 'occupation', 
           'relationship', 'race', 'sex', 'hours', 'age']
target_column = 'income'
plot_distribution(df_census, columns, target_column)
~~~

![image-20201228155759025](/assets/images/image-20201228155759025.png)

![image-20201228164553442](/assets/images/image-20201228164553442.png)

然后是使用上节的方法，依次求出它们和收入的$\chi^2$值 ，然后按照从大到小排序。

~~~python
def chi_square(df, columns, target_column):
    def plot_one(ax, column1, column2):
        df_observed = get_observed(df, column1, column2)
        df_observed.plot.bar(stacked=True, rot=45, ax =ax, fontsize=10)
        
    if type(columns)!=list: columns = [columns]
    
    results = {}
    for column in columns:
        df_observed = get_observed(df, column, target_column)
        results[column] = stats.chi2_contingency(df_observed.to_numpy())[0:2]
    results = pd.DataFrame(results).T
    results.columns = ['chi_squared_stat', 'p_value']
    results = results.sort_values('chi_squared_stat', ascending=False) 
    return  results  

chi_square(df_census, columns, target_column)
~~~

![image-20201228164618554](/assets/images/image-20201228164618554.png)

从上面的结果显示，所有的特征和收入都不是独立的（因为p_value都几乎为0）。根据**卡方统计量**（chi_squared_stat）的排名，相对而言，种族（race）没有那么重要。在实际项目中，可以根据这个排名对特征进行筛选。

### 连续特征选取

上节中，对数据集中离散特征进行了特征选取，下面使用[sklearn.feature_selection.SelectKBest](https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectKBest.html)对连续特征进行特征选取。其中最后一列是随机数，我们希望采用卡方检验剔除这个列。

~~~python
continuous_columns = ['age', 'fnlwg', 'education-num', 'capital-gain', 'capital-loss', 'hours-per-week']
X = df_census[continuous_columns].to_numpy()
# 添加一个随机数列，下面将验证这个列的卡方统计值
np.random.seed(1229)
X = np.concatenate((X, np.random.randint(0, 10, (X.shape[0],1))), axis=1)
y = df_census[['income']].to_numpy()

print('-'*25, 'X', '-'*25)
print(X[0:5], X.shape)

print('-'*25, 'X_selected', '-'*25)
select_kbest = SelectKBest(chi2, k=3)
X_selected = select_kbest.fit_transform(X, y)

print(X_selected[0:5], X_selected.shape)

print('-'*25, 'KBest scores', '-'*25)
print('KBest scores=', np.round(select_kbest.scores_, 0))
print('KBest pvalues=', np.round(select_kbest.pvalues_, 4)) 
~~~

![image-20201229105842832](/assets/images/image-20201229105842832.png)

上面的结果可以看到，最后一列（随机列）的卡方统计量最小，而且p值超过0.05，这样我们可以接受该列和收入之间的关系是独立的，也就是说，可以剔除这一列。下面代码同样实现了上面的功能，可以便于我们理解`chi2`内部的逻辑。

~~~python
def chi_score(X, y):
    # print('-'*25, 'LabelBinarizer y', '-'*25)
    Y = LabelBinarizer().fit_transform(y)
    if Y.shape[1] == 1: Y = np.append(1 - Y, Y, axis=1)    
    # print(Y[48:53], Y.shape)

    print('-'*25, 'observed', '-'*25)
    # 对每个类别的特征的值进行汇总
    observed = safe_sparse_dot(Y.T, X) 
    print(observed, observed.shape)

    print('-'*25, 'expected', '-'*25)
    # 假定根据每个类别数量，均匀分配特征的值
    feature_count = X.sum(axis=0).reshape(1, -1)
    # print(feature_count, feature_count.shape)
    class_prob = Y.mean(axis=0).reshape(1, -1)
    # print(class_prob, class_prob.shape)
    expected = np.dot(class_prob.T, feature_count)
    print(expected, expected.shape)
    
    print('-'*25, 'chi square scores', '-'*25)
    # 分别对于每个特征，计算其对应的卡方值
    df = len(observed)-1
    chi_squared_stats = np.sum((observed-expected)**2/expected,axis=0)
    print('scores=', np.round(chi_squared_stats, 0))
    p_values = np.array([1-stats.chi2.cdf(x=chi_squared_stat, df=df)
                         for chi_squared_stat in chi_squared_stats])
    
    print('p_values=', np.round(p_values, 4))
    
chi_score(X, y)
~~~

![image-20201229110120845](/assets/images/image-20201229110120845.png)

可以看到scores和p_values和SelectKBest的结果完全相同。

## 参考

- [特征选择： 卡方检验、F 检验和互信息](https://www.cnblogs.com/massquantity/p/10486904.html)
- [卡方检验(python)](https://cloud.tencent.com/developer/article/1398177)
- [Adult Census Income](https://www.kaggle.com/uciml/adult-census-income?select=adult.csv)

## 历史

- 2020-12-28：初始版本。
- 2020-12-29：添加对连续特征选取。
