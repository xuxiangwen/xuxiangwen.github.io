本文是[Forecasting: Principles and Practice](https://otexts.com/fpp3/index.html)一书的内容的读后总结，其它书籍有：

- 本书的[中文版](https://otexts.com/fppcn/)。是第二版本，而英文版是第三版本。
- [Time Series for Macroeconomics and Finance](https://faculty.chicagobooth.edu/john.cochrane/research/Papers/time_series_book.pdf)
- [应用时间序列分析备课笔记]([http://www.math.pku.edu.cn/teachers/lidf/course/atsa/atsanotes/html/_atsanotes/index.html#%E8%AF%BE%E7%A8%8B%E5%86%85%E5%AE%B9](http://www.math.pku.edu.cn/teachers/lidf/course/atsa/atsanotes/html/_atsanotes/index.html#课程内容))
- [时间序列分析基于R](C:/Users/xu6/Downloads/时间序列分析基于R_王燕编著.pdf)
- [统计笔记](https://guangchuangyu.github.io/statistics_notes/) : 比较简略，不过还不错。

## 0. 前言

- 安装fpp3。

    ~~~R
    install.packages('fpp3')
    ~~~
    
    本书种所有例子和练习都使用`fpp3`。`library(fpp3)`将会加载下面的package。
    
    - [tibble](https://tibble.tidyverse.org/), for tibbles, a modern re-imagining of data frames.
    - [dplyr](https://dplyr.tidyverse.org/), for data manipulation.
    - [tidyr](https://tidyr.tidyverse.org/), to easily tidy data using `spread()` and `gather()`.
    - [lubridate](https://lubridate.tidyverse.org/), for date/times.
    - [ggplot2](https://ggplot2.tidyverse.org/), for data visualisation.
    - [tsibble](https://tsibble.tidyverts.org/), for tsibbles, a time series version of a tibble.
    - [tsibbledata](https://tsibbledata.tidyverts.org/), various time series data sets in the form of tsibbles.
    - [feasts](https://feasts.tidyverts.org/), for features and statistics of time series.
    - [fable](https://fable.tidyverts.org/), for fitting models and producing forecasts.
    
- 第三版的改变

    - 使用`tsibble` 和 `fable`  替换 `forecast` 

    - 紧密整合`tidyverse`包含的一系列包

      ~~~
      install.packages("tidyverse")
      ~~~

      [`tidyverse`](https://github.com/tidyverse/tidyverse)是一系列优秀软件库的合集。包括如下常用的包。
    
      ![image-20200324094007700](images/image-20200324094007700.png)
      
      - 数据导入
        - readr：read_csv(); read_tsv(); read_delim(); read_fwf(); read_table(); read_log();
        - readxl：read_xls(); read_xlsx();
        - haven：打开SAS 、SPSS、Stata等外部数据
      - 数据整理
        - tibble: 对data.frame的改进，一种数据格式
        - tidyr:清洗数据 gather(); spread();
      
      - 数据转换
        - dplyr:处理数据 mutate();select(); filter(); summarise();arrange();
        - lubridate：处理时间数据
        - stringr：处理字符串类型
        - forcats：处理因子变量（factors）
      - 数据可视化
        - ggplot2
      - 编程
        - magrittr：管道运算符
        - purr：通过提供一些完整连贯用于函数和向量的工具集，增强R的函数编程。

## 1. 开始

正确的Forcasting就像魔术，而错误的Forcasting似乎更多。下面是一些看起来可笑的预测：

- *I think there is a world market for maybe five computers.* (Chairman of IBM, 1943)

- *Computers in the future may weigh no more than 1.5 tons.* (Popular Mechanics, 1949)

- *There is no reason anyone would want a computer in their home.* (President, DEC, 1977)

  :cold_sweat:三年就被迅速打脸，IBM第一台个人电脑就推出了。

> 对于没有明显周期性的事情，越是长期预测，越不准确。

### 1.1 什么可以被预测（What can be forecast）

可预测性取决于几个因素：

1. 对影响事情发展的因素的了解程度
2. 是否有充分可用的数据
3. 预测是否会影响我们试图预测的事物

比如：预测电力需求可以非常准确。电力需求和以下因素有关：

- 主要因素：温度
- 次要因素：假期，经济情况

这些因素的历史数据可以很容易得到，这意味着我们可以建立一个模型来进行准确的预测。

相反的例子，对于货币汇率的预测，或许仅仅满足第二个条件（汇率本身变化的数据很充分），但我们并不非常清楚影响汇率的因素，而且对汇率的预测对汇率本身有直接的影响。也就是说，如果有一个预测（比如预测汇率会增长）被众人所知，人们就会立即调整他们的价格，而这使得预测被自我验证了（self-fulfilling）。

对于预测，关键的一步是知道什么时候预测是准的，什么时候预测就像投硬币。好的预测可以捕捉真实的模式和关系，而不是重复过去的事件，因为它们将再也不会发生。本书中，我们将学会区分随机波动（random fluctuation）和真实的模式（genuine pattern）。

> 股市的涨跌也是不可预测的。其原因在于，影响股市涨跌的因素（比如：宏观经济，政策，突发事件，庄家）在股市买卖数据中并没有完全体现，这就是技术分析的局限根本所在。没有任何一个人或机构可以掌握完整的数据。
>
> - 时间维度上，股市不可预测。精确预测某个时间的股市表现是不可能的。比如，我们无法预测几天后，股票会涨还是会跌。在超短时间维度上，似乎是可以预测的，比如，预测下一秒，或者下一分钟某个股票涨跌的准确率会很高，但是由于买卖交易的限制（竞价，手续费，延时等），以及你的买卖会干扰实际的价格，实际操作起来也是不可能的（文艺复兴等基金公司或许可以？）。
> - 空间维度上，股市可以预测。比如，某支股票的价格远远高于或低于其实际价值，在某个未来其价格将被修正。而要判断一个股票的价格是否背离了其价值，必须要了解这个公司是如何运作，如何盈利的，它的盈利和哪些因素直接有关系，这些直接因素又收到哪些间接因素的影响。只有了解了这些，才能进行精确的预测。巴菲特的投资理念也是如此。
>
> 由于时间维度上，无法进行精确的预测，而空间维度可以进行预测。这决定了股票投资的策略是：
>
> - 分析：综合大量数据，判断股票在空间维度上的趋势，锁定目标。
> - 等待：监控相关因素，计算事件发生概率。
> - 买入：等到事件发生概率达到买入临界值，进行买入。
> - 等待：监控相关因素，计算事件发生概率。
> - 卖出：等到事件发生概率达到卖出临界值，进行卖出。

### 1.2 预测什么（Determining what to forecast）

在开始，我们要决定应当预测什么。假设预测的是在制造业领域，需要回答以下问题：

1. 预测每个product line还是groups of products?
2. 预测总体销售额，还是每个区域的销售额？
3. 预测是周度，月度，还是年度数据？

### 1.3 预测数据和方法（Forecasting data and methods）

预测方法的选择很大程度依赖于数据，如果数据很难获取，往往采用定性预测（**qualitative forecasting** ）的方法。而要采用定量预测（**Quantitative forecasting** ）需要满足以下两个条件：

1. 过去的数据是足够的
2. 过去的模式在未来仍然会继续延续。

本书只讨论有规律间隔时间（比如：小时，日，周，月，季度，年等）的time series，对于同一不规则间隔的time series不在本书的讨论范围。

#### Time Series预测示例

下图中，显示的澳大利亚1992-2010年啤酒的产量。

![Australian quarterly beer production: 1992Q1–2010Q2, with two years of forecasts.](images/beer-1.png)

蓝色线是接下来两年的预测。预测已经获取了seasonal 模式。深色阴影显示了80%的预测间隔（意味着未来的值80%的可能性处于这个区域），而浅色阴影显示了95%的预测间隔。

由于上面的预测是最简单的time series预测，因为它仅仅推断了trend和seasonal 模式，而忽略了其它的信息：市场营销，竞争对手活动，经济条件的改变等等。

#### 预测变量（Predictor variables）和time series预测

下面以预测夏季热点地区每个小时电力需求(ED)为例。可以有下面几种模型：

- 预测变量模型：这是一种可解释模型（explanatory model），帮助我们理解哪些因素会影响电力需求。
  $$
  \begin{align*}
    \text{ED} = & f(\text{current temperature, strength of economy, population,}\\
   &  \qquad\text{time of day, day of week, error}).
  \end{align*}
  $$

- time series预测模型
  $$
  \text{ED}_{t+1} = f(\text{ED}_{t}, \text{ED}_{t-1}, \text{ED}_{t-2}, \text{ED}_{t-3},\dots, \text{error})
  $$

- mixed模型：混合前两种模型。
  $$
  \text{ED}_{t+1} = f(\text{ED}_{t}, \text{current temperature, time of day, day of week, error})
  $$

在很多情况下，我们会采用time series预测模型，这是因为：

- 系统无法理解。

  > 我也无法理解

- 很难获得预测变量在未来的值。

  > 比如，预测变量和被预测值之间是同时产生的。

- 只关心未来会发生什么，而不需要知道为什么。

#### 预测任务的基本步骤

1. 问题定义。经常这是预测中最难的一部分。

   - 预测结果如何被使用
   - 谁需要这些预测
   - 如何来收集数据，维护数据。

2. 收集信息。有两类信息

   - 统计数据
   - （数据收集和使用预测的）相关人员的业务知识和经验。

3. 初步探索分析（Preliminary (exploratory) analysis）

   通过可视化技术来展示数据。比如以下问题：

   - 是否有稳定的模式？
   - 是否有明显趋势？
   - 是否是季节性的？
   - 是否有商业周期？
   - 是否有异常数据（需要被专家来解释）？
   - 变量之间是否有强的相关性？

4. 选择和拟合模型。

5. 使用和评估预测模型。

## 2. Times Series图形

###  2.1 `tsibble` objects

详见https://github.com/tidyverts/tsibble。

#### 特性

`tsibble`对象继承了`tidy` data frame(`tibble` objects)。其独有的特性有：

- index：一个时间变量，按照从过去到现在排列

- key： 通过这个key，可以把数据分成多个组。每一组都是一个time series数据。

- key + index 构成数据的唯一键

- 数据之间的间隔（interval）必须是均匀的（Each observational unit should be measured at a common **interval**, if regularly spaced）

  | **Interval** | **Class**                 | Function            |
  | ------------ | ------------------------- | ------------------- |
  | Annual       | `integer`/`double`        | `start:end`         |
  | Quarterly    | `yearquarter`             | `yearquarter()`     |
  | Monthly      | `yearmonth`               | `yearmonth()`       |
  | Weekly       | `yearweek`                | `yearweek()`        |
  | Daily        | `Date`/`difftime`         | `as_date()`,`ymd()` |
  | Subdaily     | `POSIXt`/`difftime`/`hms` | `as_datetime()`     |

#### 创建

~~~R
library(dplyr)
library(tsibble)

show_object_type <- function(X){
    cat('X = \n')
    print(X)
    cat('class(X) =', paste(class(X), collapse=", "), '\n')
    cat('mode(X) =', mode(X), '\n')
    cat('typeof(X) =', typeof(X), '\n')
#    cat('str(X) =\n')
#    str(X)
}

weather <- nycflights13::weather %>% 
  select(origin, time_hour, temp, humid, precip)
weather_tsbl <- as_tsibble(weather, key = origin, index = time_hour)
weather_tsbl
show_object_type(weather_tsbl)

y <- tsibble(Year = 2015:2019, Observation =
             c(123,39,78,52,110), index = Year)
show_object_type(y)
~~~

#### 从文本创建

~~~R
text <- "Month, Observation
2019 Jan, 50
2019 Feb, 23
2019 Mar, 34
2019 Apr, 30
2019 May, 25
"
# 读入tibble
z <- read_csv(text, col_types = "cd")
# 转化为tsibble
z %>%
  mutate(Month= yearmonth(Month)) %>%
  as_tsibble(index = Month)
~~~

返回结果如下：

![image-20200327185513948](images/image-20200327185513948.png)

注意，其中[1M]表示time interval时一个月。

#### 读取csv 

~~~R
library(tsibble)
library(dplyr)

prison <- readr::read_csv("https://OTexts.com/fpp3/extrafiles/prison_population.csv")

prison <- prison %>%
  mutate(quarter = yearquarter(date)) %>%
  select(-date) %>%
  as_tsibble(key = c(state, gender, legal, indigenous), index = quarter)

prison
~~~

>如果无法下载数据，请设置代理
>
>~~~R
>Sys.setenv("http_proxy"="http://web-proxy.rose.hp.com:8080") 
>Sys.setenv("https_proxy"="http://web-proxy.rose.hp.com:8080") 
>~~~

#### 缺失数据补齐

可以使用`fill_gaps()`来把缺失数据补齐，避免不规则的interval

~~~
harvest <- tsibble(
  year = c(2010, 2011, 2013, 2011, 2012, 2014),
  fruit = rep(c("kiwi", "cherry"), each = 3),
  kilo = sample(1:10, size = 6),
  key = fruit, index = year
)

harvest
harvest %>%  fill_gaps(kilo = 0L)
~~~

![image-20200403160451341](images/image-20200403160451341.png)

#### index_by() + summarise()

index_by和group_by类似，不同在于index_by仅仅针对index。如果相对index进行分组，必须要使用index_by。

~~~R
library(dplyr)
library(tsibble)
weather <- nycflights13::weather %>% 
  select(origin, time_hour, temp, humid, precip)
weather_tsbl <- as_tsibble(weather, key = origin, index = time_hour)
weather_tsbl

# 处理缺失的数据
full_weather <- weather_tsbl %>%
  fill_gaps(.full=T) 
na_s <- is.na(full_weather$temp) | is.na(full_weather$humid) |
  is.na(full_weather$precip) 
# 查看缺失数据
view(full_weather[na_s,])

# 处理na值
full_weather <- full_weather %>% 
  group_by_key() %>% 
  tidyr::fill(temp, humid, precip, .direction = "down")
full_weather
view(full_weather[na_s,])

# index_by + summarise
full_weather %>%
  index_by(year_month = ~ yearmonth(.)) %>% # monthly aggregates
  summarise(
    avg_temp = mean(temp, na.rm = TRUE),
    ttl_precip = sum(precip, na.rm = TRUE)
  )
~~~

####  difference

计算时间序列中差分。

~~~R
x <- cumsum(cumsum(1:10))
x
difference(x, lag = 1)
difference(x, lag = 2)
difference(x, differences = 1)	# 一阶差分
difference(x, differences = 2)	# 二阶差分
~~~

![image-20200403214346863](images/image-20200403214346863.png)

### 2.2 Time plots

下面显示Ansett 航空公司在澳洲最大的两个城市之间每周经济仓乘客量。

~~~R
library(fpp3)
melsyd_economy <- ansett %>%
  filter(Airports == "MEL-SYD", Class=="Economy")
melsyd_economy %>%
  autoplot(Passengers) +
    labs(title = "Ansett economy class passengers", subtitle = "Melbourne-Sydney") +
    xlab("Year")
~~~

`autoplot()`自动产生合适的图形，由于识别到`tisbble`是一个time series，所以产生一个time plot。

![image-20200327202449891](images/image-20200327202449891.png)

### 2.3 Time series patterns

- 趋势（Trend）

  下图中，很明显有一个长期（long-term）增长的趋势。

  ![image-20200327203804431](images/image-20200327203804431.png)

  

- 季节性（Seasonal ）：固定的一段时间。年，季度，月，或者周

  上图中，很明显季度因子是一年。

- 周期性（Cyclic）：数据体现周期性，但这个周期并不是固定的频率。这种数据的波动通常是由于经济条件，所以经常被称之为"商业周期"。这种周期比起季节性的跨度药更大，一般至少两年。

下面以几个time plot来观察数据的特性：

![image-20200327205110403](images/image-20200327205110403.png)

1. 美国新建房屋月度销售数据（The monthly housing sales）
   - Trend: 无
   - Seasonal： Year。一年里有明显的周期
   - Cyclic： 6-10年一个周期。
2. 1981年芝加哥地区美国短期国库券合约（The US treasury bill contracts）连续100天交易数量。
   
   - Trend: 向下
   - Seasonal： 无
   - Cyclic： 无。实际上，如果有更多数据，可能可以发现处于一个周期中。
3. 澳大利亚季度电力产量（The Australian quarterly electricity production）
   - Trend: 向上
   - Seasonal： Year。很明显，波动非常固定，有规律。
   - Cyclic： 无

4. Google公司每日的收盘价（The daily change in the Google closing stock price）

   - Trend: 无
   - Seasonal： 无
   - Cyclic： 无

   呈现随机波动的特点，这种数据是无法预测的。

### 2.4 Seasonal plots

`vic_elec` 包含澳洲Victoria州了半小时电力需求。 下面来观察以下daily pattern, weekly pattern, yearly pattern。

- daily pattern

  ~~~R
  library(fpp3)
  vic_elec %>% gg_season(Demand, period="day") + theme(legend.position = "none")
  ~~~

  ![image-20200328015044665](images/image-20200328015044665.png)

- weekly pattern

  ~~~R
  vic_elec %>% gg_season(Demand, period="week") + theme(legend.position = "none")
  ~~~

  ![image-20200328015116415](images/image-20200328015116415.png)

- yearly pattern

  ~~~R
  vic_elec %>% gg_season(Demand, period="year")
  ~~~

  ![image-20200328015153935](images/image-20200328015153935.png)

### 2.5 Seasonal subseries plots

#### Example: 澳大利亚人假期旅游（Australian holiday tourism）

~~~R
library(fpp3)
holidays <- tourism %>%
  filter(Purpose == "Holiday") %>%
  group_by(State) %>%
  summarise(Trips = sum(Trips))

holidays
holidays %>% autoplot(Trips) +
  ylab("thousands of trips") + xlab("Year") +
  ggtitle("Australian domestic holiday nights")
~~~

![image-20200328020235073](images/image-20200328020235073.png)

上图中可以看出：

- Trend: 无
- Seasonal： 强烈。但seasonal peak并不一致。
- Cyclic： 无

下面进一步观察seasonal peak。

~~~R
holidays %>% gg_season(Trips) +
  ylab("thousands of trips") +
  ggtitle("Australian domestic holiday nights")
~~~

![image-20200328021010319](images/image-20200328021010319.png)

~~~R
holidays %>%
  gg_subseries(Trips) + ylab("thousands of trips") +
  ggtitle("Australian domestic holiday nights")
~~~

![image-20200328022316457](images/image-20200328022316457.png)

### 2.6 散点图（Scatterplots）

`vic_elec` 包含澳洲Victoria州了半小时电力需求。下面的代码生成散点图，可以分析每四个小时电力需求和平均温度的关系。

~~~R
library(fpp3)
vic_elec %>%
  filter(year(Time) == 2014) %>% 
  index_by(Time1=floor_date(Time,  "4 hour"))  %>% 
  summarise(
    Temperature = mean(Temperature, na.rm = TRUE),
    Demand = sum(Demand, na.rm = TRUE)
  ) %>% 
  ggplot(aes(x = Temperature, y = Demand)) +
    geom_point() +
    ylab("Demand (GW)") + xlab("Temperature (Celsius)")
~~~

![image-20200328152936958](images/image-20200328152936958.png)

> index_by: tsibble的函数，用于在时间轴上对数据的粒度进行限制。

可以看出：

- 温度越高，电力消耗增加很快。可能是空调的使用
- 温度越低，电力消耗也会增加。主要是暖气的使用。

#### 相关系数（Correlation）

散点图可以让我们对数据相关性，有一个感性的认识，而相关系数可以定量描述了它们的关系。公式如下：
$$
r = \frac{\sum (x_{t} - \bar{x})(y_{t}-\bar{y})}{\sqrt{\sum(x_{t}-\bar{x})^2}\sqrt{\sum(y_{t}-\bar{y})^2}}.
$$
相关系数和散点图的对应关系如下。

![image-20200328155318222](images/image-20200328155318222.png)

相关系数刻画了变量之间的线性关系，如果变量之间不存在线性关系，可能会有误导。比如上个例子中，Temperature和Demand之间，是有很强的相互关联的（非线性关系），但是它们的相关系数只有0.26。

~~~R
library(fpp3)
cor(vic_elec$Demand, vic_elec$Temperature)
~~~

反过来也是，有些数据相关系数很高，但是其并不一定有线性关系。

~~~R
attach(anscombe)
opar <- par(no.readonly=TRUE)
par(mfrow=c(2,2), mar=c (2,2,2,2))
plot(x1, y1, xlab = "", ylab = "", main = bquote(paste("a. ", italic(r), "= ",.(round(cor(x1, y1),2)))))
abline(3,0.5) 
plot(x2, y2, xlab = "", ylab = "",, main = bquote(paste("b. ", italic(r),  "= ",.(round(cor(x2, y2),2)))))
abline(3,0.5) 
plot(x3, y3, xlab = "", ylab = "",, main = bquote(paste("c. ", italic(r), "= ",.(round(cor(x3, y3),2)))))
abline(3,0.5) 
plot(x4, y4, xlab = "", ylab = "",, main = bquote(paste("d. ", italic(r), "= ",.(round(cor(x4, y4),2)))))
abline(3,0.5) 
par(opar)
detach(anscombe)
~~~

上面代码运行结果如下。四组数据其相关系数都是0.82，但是a，d明显不是线性关系，而c有异常值（实际相关系数更高）。

![image-20200328164544589](images/image-20200328164544589.png)

下面是更加有意思的例子，来自[Same Stats, Different Graphs: Generating Datasets with Varied Appearance and Identical Statistics through Simulated Annealing](https://www.autodeskresearch.com/publications/samestats)。

![img](images/DinoSequentialSmaller.gif)

> 相关系数，从几何上可以理解为两个（中心化后）向量的余弦夹角。

#### Scatterplots 矩阵

再次来观察澳大利亚人假期旅游（Australian holiday tourism），首先显示每个州的time plot。

~~~R
library(fpp3)
library(GGally)
visitors <- tourism %>%
  group_by(State) %>%
  summarise(Trips = sum(Trips))
visitors %>%
  ggplot(aes(x = Quarter, y = Trips)) +
    geom_line() +
    facet_grid(vars(State), scales = "free_y") +
    ylab("Number of visitor nights each quarter (millions)")
~~~

![image-20200328165541804](images/image-20200328165541804.png)

然后显示各个州的数据之间的相关系数矩阵。

~~~R
visitors %>%
  spread(State, Trips) %>%
  GGally::ggpairs(columns = 2:9)
~~~

![image-20200328170033599](images/image-20200328170033599.png)

可以发现：

1. 相邻的州其正向相关比较强
2. 南部的州和北部的州呈现负相关。

### 2.7 Lag plots

下面分析澳大利亚季度啤酒产量。

~~~R
library(fpp3)
recent_production <- aus_production %>% filter(year(Quarter) >= 1992)
recent_production %>% autoplot(Beer) + 
  ggtitle("Australian Beer Production")
~~~

![image-20200328201439600](images/image-20200328201439600.png)

不难看出：

- Trend： 销量逐渐下降
- Seasonality： 明显的周期性
- Cyclicity：无

然后看lag散点图。

~~~R
recent_production %>% gg_lag(Beer, geom="point")
~~~

![image-20200328191815709](images/image-20200328191815709.png)

从上面图中可以发现：

- lag 4和lag 8体现了强烈的正相关性。季节性特性明显（周期为4）。
- lag 2和lag 6体现了强烈的负相关性。夏季和冬季的销量正好相反

### 2.8 自相关（Autocorrelation）

上节中，Lag plots可以显示自相关性，同样可以量化这一指标，即计算自相关系数（autocorrelation coefficients）。公式如下：
$$
r_{k} = \frac{\sum\limits_{t=k+1}^T (y_{t}-\bar{y})(y_{t-k}-\bar{y})}
 {\sum\limits_{t=1}^T (y_{t}-\bar{y})^2},
$$
计算自相关系数函数`ACF`

~~~R
recent_production %>% ACF(Beer, lag_max = 9)
~~~

![image-20200328200435895](images/image-20200328200435895.png)

自相关图（ACF plot）

~~~
recent_production %>% ACF(Beer) %>% autoplot()
~~~

![image-20200328200630505](images/image-20200328200630505.png)

和Lag plots类似，我们可以很容易得到以下结论。

1. r4, r8, r12, r16 有很强的正相关，其中r4是最强的相关性，然后依次降低
2. r2, r6, r10, r14, r18有很强的负相关，其中r2是最强的相关性，然后依次降低
3. 蓝色线用于指示相关性的显著程度。

上面第1，2点，进一步验证了前面观察到的Trend和Seasonality。

### 2.9 白噪音（White noise）

白噪声是一个对所有时间其自相关系数为零的随机过程。也就是说，白噪声表现在任何两个时点的随机变量都不相关，序列中没有任何可以利用的动态规律，因此不能用历史数据对未来进行预测和推断。白噪音数学定义如下：

如果时间序列$\{\epsilon_t, t=1,2,3,...,T\}$满足：

1. $ E(\epsilon_t)=0$
2. $ Var(\epsilon_t)=\sigma^2$
3. 当$k!= 0, 相关系数：Cov(\epsilon_t, \epsilon_{t+k})=0$

则称该序列为白噪声（white noise）。

~~~R
library(fpp3)
set.seed(30)
y <- tsibble(sample = 1:100, wn = rnorm(100), index = sample)
y %>% autoplot(wn) + ggtitle("White noise")
~~~

![image-20200328203558919](images/image-20200328203558919.png)

~~~
y %>% ACF(wn) %>% autoplot()
~~~

![image-20200328221644266](images/image-20200328221644266.png)

对于平稳的时间序列，理想情形是自相关函数在一定的条件下服从正态分布，当样本量n很大时，相关落在区间$[-\frac {1.96} {\sqrt n}, \frac {1.96} {\sqrt n}]$（书中提到的区间是$[-\frac {2} {\sqrt n}, \frac {2} {\sqrt n}]$）的概率为95%，ACF plot中的两条蓝色虚线就是这个范围。

> 蓝色虚线的计算，或许是这样（好像推不下去了）
> $$
> \begin{align}
> r &= \frac{\sum (x_{t} - \bar{x})(y_{t}-\bar{y})}{\sqrt{\sum(x_{t}-\bar{x})^2}\sqrt{\sum(y_{t}-\bar{y})^2}}  \\
> &= \frac 1 n \sum  \frac {(x_{t} - \bar{x})} {\sqrt{\frac 1 n \sum(x_{t}-\bar{x})^2}} \frac {(y_{t} - \bar{y})} {\sqrt{\frac 1 n \sum(y_{t}-\bar{y})^2}}  \\
> &= \frac 1 n \sum  x_t^{'} y_t^{'}
> \end{align}
> $$
>
> 其中
> $$
> x_t^{'} =  \frac {(x_{t} - \bar{x})} {\sqrt{\frac 1 n \sum(x_{t}-\bar{x})^2}},  y_t^{'} =  \frac {(y_{t} - \bar{y})} {\sqrt{\frac 1 n \sum(y_{t}-\bar{y})^2}}
> $$
> 假设$x, y$都是相互独立的正态分布，则$x^{'},y^{'} $分别服从标准正态分布$\mathcal{N}(0,\,1)$。则认为$r$符合$\mathcal{N}(0,\,\frac 1 n)$分布。（中间过程没法推，好像有漏洞）。

#### Barlett定理

上面自我的推导虽然没有成功，但其描述的就是Barlett定理。其定义如下：

观察期数为 $n$ 的观察序列，若为纯随机序列，则该序列延迟非零期的样本自相关系数$\hat \rho_k$近似服从正态分布$\mathcal{N}(0,\,\frac 1 n)$。95%的置信空间计算方法如下：

~~~R
qnorm(0.975)	# 返回1.959964
qnorm(0.025)	# 返回1.959964
~~~
Python代码如下。

~~~python
from scipy.stats import norm

print(norm.ppf(0.975))  # 计算上限
print(norm.ppf(0.025))  # 计算下限
~~~
上面的结果，说明了1.96的由来。

#### 白噪音的检验

白噪音检查的应用非常广泛，一般来说，对时间序列预测后，需要进行残差（residual）分析，检查残差是否是白噪音。如果残差是白噪音，则说明序列中有用的信息已经被提取完毕了，剩下的全是随机扰动，是无法预测和使用的。如果残差不是白噪声，就说明残差中还有有用的信息，需要修改模型或者进一步提取。

- Box.test()

  Box.test()是对randomness的检验，基于一系列滞后阶数，判断序列总体的相关性或者说随机性是否存在。原假设为序列为白噪音，当p<0.05，拒绝原假设，即序列不是白噪音。

  ~~~R
  set.seed(30)
  y <- tsibble(sample = 1:100, wn = rnorm(100), index = sample)
  Box.test(y$wn, lag=log(length(y$wn)), type='Ljung')
  ~~~

  ![image-20200404152240953](images/image-20200404152240953.png)

- acf()：检验残差滞后各ACF期是否存在显著的自相关性。

  ~~~R
  y %>% ACF(wn) %>% autoplot()
  ~~~

  ![image-20200407095309737](images/image-20200407095309737.png)

  除去lag(1)，其它lag都在95%置信区间之内。如果95%的lag在95%置信区间内，则认为序列是白噪音。

- pacf()：检验残差滞后各期是否存在显著的偏自相关性。

  ~~~R
  y %>% PACF(wn) %>% autoplot()
  ~~~

  ![image-20200407095215814](images/image-20200407095215814.png)

  所有lag都在95%置信区间之内。

- qqnorm()，qqline()：画出qq图，检验序列服从正态分布。

  统计分布的检验有很多种，例如KS检验、卡方检验等，从图形的角度来说，可以用**QQ图**（Quantile-Quantile Plots）来检查数据是否服从某种分布。

  ~~~R
  qqnorm(y$wn)
  qqline(y$wn, col=2, lwd=2)
  ~~~

- Kolmogorov-Smirnov检验和Shapiro - Wilk检验

  - 样本含量3≤n ≤5000 时，Shapiro - Wilk 检验为准
  - 样本含量n >5000 时，Kolmogorov-Smirnov 检验为准

  ~~~R
  ks.test(y$wn，"pnorm", mean=mean(y$wn), sd=sd(y$wn))
  shapiro.test(y$wn)
  ~~~

  ![image-20200407093759897](images/image-20200407093759897.png)

  p值>0.05，不能拒绝该分布是正态分布

## 3. 时间序列分解（Time Series Decomposition）

观察时间序列，可以发现不同的pattern，这能够有助于把时间序列才分成不同的组件。每一个组件都表示了底层运行的pattern。

在2.3一节中，谈到有三种时间序列pattern: 趋势（Trend），季节性（Seasonality）和周期性（Cycle），当分解time series时，通常会把trend和cycle合并成trend-cycle。由此，可以把组件分为三类：

- 趋势-周期（Trend-Cycle） 
- 季节性（Seasonal)
- 其它

### 3.1 转换（Transformation）和调整（Adjustment）

- 日历：比如，可以使用每月平均值来消除每个月的天数的差异。

- 人口（Population）：比如，分析某个地区医院的床位数，就必须要考虑到该地区人口的增长，有时，床位数增加了，但人均的床位数反而下降，这是由于总人口的增速大于床位的增速。所以，使用人均数量往往比总量更加的好。

  ~~~R
  global_economy %>%
    filter(Country == "Australia" | Country == "China" | Country == "United States") %>%
    autoplot(GDP/Population)
  ~~~

  ![image-20200407135738702](images/image-20200407135738702.png)

  > 从上面这个图，似乎时美国和澳大利亚人均GDP增加更快，但实际情况时中国的增速更快。原因何在呢？

  - 通货膨胀（Inflation）

    经常会使用CPI（Consumer Price Index）来调整。

    ~~~R
    print_retail <- aus_retail %>%
      filter(Industry == "Newspaper and book retailing") %>%
      group_by(Industry) %>%
      index_by(Year = year(Month)) %>%
      summarise(Turnover = sum(Turnover))
    aus_economy <- global_economy %>%
      filter(Code == "AUS")
    print_retail %>%
      left_join(aus_economy, by = "Year") %>%
      mutate(Adjusted_turnover = Turnover / CPI) %>%
      gather("Type", "Turnover", Turnover, Adjusted_turnover, factor_key = TRUE) %>%
      ggplot(aes(x = Year, y = Turnover)) +
        geom_line() +
        facet_grid(vars(Type), scales = "free_y") +
        xlab("Years") + ylab(NULL) +
        ggtitle("Turnover for the Australian print media industry")
    ~~~

    ![image-20200407145133189](images/image-20200407145133189.png)

    上图中可以明显看出，如果使用CPI调整，会发现`Newspaper and book retailing`行业从很早开始，已经陷入了衰退。

    > CPI：即居民消费价格指数，是一个反映居民家庭一般所购买的消费品和服务项目价格水平变动情况的宏观经济指标。
    >
    > CPI=（一组固定商品按当期价格计算的价值除以一组固定商品按基期价格计算的价值）×100%。
    >
    > 例如，若1995年某国普通家庭每个月购买一组商品的费用为1000元，而2000年购买这一组商品的费用为1100元，以1995年为基期，那么：
    > $$
    > CPI_{1995}= (1000/1000) = 1 \\ 
    > CPI_{2000}=（1100/1000) = 1.1
    > $$
    > 实际在日常生活中，通常往往关注的是CPI增长，即当期CPI的同比和环比。中国居民的CPI增长是较高的，见[中国 居民消费价格指数（CPI）增长](https://www.ceicdata.com/zh-hans/indicator/china/consumer-price-index-cpi-growth)。

  - 数学（Mathematica）

    - log
      $$
      w_t = \log(y_t) \\
      $$

    - 指数
      $$
      w_{t} = y_{t}^p
      $$

    - Box-Cox变换：把数据转化为正态分布
      $$
      y(\lambda)=
      \left\{
      \begin{aligned}
       & \frac { y^{\lambda}-1} \lambda ,  & \lambda \neq 0 \\
      & ln(y) ,    &  \lambda = 0 \\
      \end{aligned}
      \right.
      $$
      

      详见[Transformations and adjustments](https://otexts.com/fpp3/transformations.html)

      ~~~R
      lambda <- aus_production %>%
        features(Gas, features = guerrero) %>%
        pull(lambda_guerrero)
      
      shapiro.test(aus_production$Gas)	# p-value = 2.873e-10
      
      aus_production <- aus_production %>% 
        mutate(adjust_Gas=box_cox(Gas, lambda))
      aus_production %>% autoplot(adjust_Gas) 
      
      # 调整后，仍然不是正态分布
      shapiro.test(aus_production$adjust_Gas) # p-value = 7.016e-14
      ~~~

      ![image-20200407164106314](images/image-20200407164106314.png)

### 3.2 时间序列成分（Time Series Components）

有两种分解的方法：

- additive decompositon：
  $$
  y_{t} = S_{t} + T_{t} + R_t
  $$

- multiplicative decomposition
  $$
  y_{t} = S_{t} \times T_{t} \times R_t
  $$

其中$y_t$是原时间序列，$S_t$是seasonal因素，$T_t$是 trend-cycle因素，$R_t$是其余的因素。

- 当$S_t，T_t，R_t$呈现线性关系时，建议使用additive decompositon

- 当$S_t，T_t，R_t$呈现非线性关系时，建议使用multiplicative decomposition，常用于经济的时间序列。

  通过log可以，把multiplicative 转化成additive 
  $$
  y_{t} = S_{t} \times T_{t} \times R_t \quad\text{is equivalent to}\quad
    \log y_{t} = \log S_{t} + \log T_{t} + \log R_t
  $$
  



