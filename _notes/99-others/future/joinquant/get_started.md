### 基本结构

~~~python3
  def initialize(context):
      run_daily(period,time='every_bar')
      g.security = '000001.XSHE'

  def period(context):
      order(g.security, 100)
~~~

### context

context是一个回测系统建立的Context类型的对象，其中存储了如当前策略运行的时间点、所持有的股票、数量、持仓成本等数据。

![context](images/3f21926604474d702db5efe2c9154cb1.png)

### 聚宽数据

https://www.joinquant.com/data

![image-20211207174508516](images/image-20211207174508516.png)