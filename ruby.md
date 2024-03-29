## ruby安装

**安装rbenv**

rbenv 用来管理多个版本的 ruby 在用户目录的安装和使用.

~~~shell
curl -fsSL https://github.com/rbenv/rbenv-installer/raw/master/bin/rbenv-installer | bash
echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc
echo eval \"\$\(rbenv init -\)\" >>  ~/.bashrc
source ~/.bashrc

rbenv -v
~~~

**安装ruby**

~~~shell
sudo yum remove -y ruby
sudo yum install -y readline-devel
ruby_file=~/.rbenv/cache/ruby-2.6.5.tar.bz2
if [ ! -f "$ruby_file" ]; then
  wget 'https://cache.ruby-china.com/pub/ruby/2.6/ruby-2.6.5.tar.bz2' -P ~/.rbenv/cache
fi
rbenv install 2.6.5
rbenv global 2.6.5
rbenv versions

ruby -v

~~~

**检查安装**

~~~SHELL
curl -fsSL https://github.com/rbenv/rbenv-installer/raw/master/bin/rbenv-doctor | bash
ruby -v
~~~

如果输出如下信息，表示

![1571194274287](images/1571194274287.png)

## 进入Interactive Ruby

```ruby
irb
```

## 入门

### hello world*

~~~ruby
"Hello World"
puts "Hello World"
3+2
Math.sqrt(9)
~~~

### 函数

~~~ruby
def h
puts "Hello World!"
end

h
h()

def h(name)
puts "Hello #{name}!"
end

h("Matz")

def h(name = "world")
puts "Hello #{name.capitalize}!"
end

h "chris"
h
~~~

### 类

~~~ruby
class Greeter
  def initialize(name = "World")
    @name = name
  end
  def say_hi
    puts "Hi #{@name}!"
  end
  def say_bye
    puts "Bye #{@name}, come back soon."
  end
end

g = Greeter.new("Pat")
g.say_hi
g.say_bye
g.@name      # 无法访问

# 显示实例函数
Greeter.instance_methods
Greeter.instance_methods(false)

g.respond_to?("name")
g.respond_to?("say_hi")
g.respond_to?("to_s")
~~~

获取实例变量名。在 Ruby 里，您可以把一个类打开然后改变它。这些改变会对以后生成的甚至是已经生成的对象产生即时效果。

~~~
class Greeter
  attr_accessor :name
end

g = Greeter.new("Andy")
g.respond_to?("name")
g.respond_to?("name=")
g.say_hi
g.name="Betty"

g
Greeter.instance_methods(false)
~~~

更加完整的例子：

~~~ruby
cat << EOF > ri20min.rb
#!/usr/bin/env ruby

class MegaGreeter
  attr_accessor :names

  # Create the object
  def initialize(names = "World")
    @names = names
  end

  # Say hi to everybody
  def say_hi
    if @names.nil?
      puts "..."
    elsif @names.respond_to?("each")
      # @names is a list of some kind, iterate!
      @names.each do |name|
        puts "Hello #{name}!"
      end
    else
      puts "Hello #{@names}!"
    end
  end

  # Say bye to everybody
  def say_bye
    if @names.nil?
      puts "..."
    elsif @names.respond_to?("join")
      # Join the list elements with commas
      puts "Goodbye #{@names.join(", ")}.  Come back soon!"
    else
      puts "Goodbye #{@names}.  Come back soon!"
    end
  end

end

if __FILE__ == \$0
  mg = MegaGreeter.new
  mg.say_hi
  mg.say_bye

  # Change name to be "Zeke"
  mg.names = "Zeke"
  mg.say_hi
  mg.say_bye

  # Change the name to an array of names
  mg.names = ["Albert", "Brenda", "Charles",
    "Dave", "Engelbert"]
  mg.say_hi
  mg.say_bye

  # Change to nil
  mg.names = nil
  mg.say_hi
  mg.say_bye
end

EOF

chmod 755 ri20min.rb
./ri20min.rb
~~~

### irb支持中文

```
export LANG=en_US.UTF-8
irb
puts "你好，世界！";
```

```
 ruby -e 'puts Encoding.find("locale")'
```

### Here Document

"Here Document" 是指建立多行字符串。在 << 之后，您可以指定一个字符串或标识符来终止字符串，且当前行之后直到终止符为止的所有行是字符串的值。

如果终止符用引号括起，引号的类型决定了面向行的字符串类型。请注意<< 和终止符之间必须没有空格。

```
cat << SEOF > here_document.rb
#!/usr/bin/env ruby
# -*- coding : utf-8 -*-
 
print <<EOF
    这是第一种方式创建here document 。
    多行字符串。
EOF
 
print <<"EOF";                # 与上面相同
    这是第二种方式创建here document 。
    多行字符串。
EOF
 
print <<\`EOC\`                 # 执行命令
    echo hi there
    echo lo there
EOC
 
print <<"foo", <<"bar"          # 您可以把它们进行堆叠
    I said foo.
foo
    I said bar.
bar

SEOF

chmod 755 here_document.rb
./here_document.rb
```

### Begin End

~~~ruby
program=begin_end.rb
cat << EOF > $program
#!/usr/bin/env ruby
puts "这是主 Ruby 程序"
 
END {
   puts "停止 Ruby 程序"
}
BEGIN {
   puts "初始化 Ruby 程序"
}
EOF

chmod 755 $program
./$program
~~~

### 集合

- array
- hash

~~~
program=collection.rb
cat << EOF > $program
#!/usr/bin/env ruby

puts '----------------------------------'
ary = [ "fred", 10, 3.14, "This is a string", "last element", ]
ary.each do |i|
    puts i
end

puts '----------------------------------'
hsh = colors = { "red" => 0xf00, "green" => 0x0f0, "blue" => 0x00f }
hsh.each do |key, value|
    print key, " is ", value, "\n"
end

puts '----------------------------------'
(10..15).each do |n|
    print n, ' '
end
print "\n" 

puts '----------------------------------'
nums = Array.new(10) { |e| e = e * 2 }
puts "#{nums}"

puts '----------------------------------'
months = Hash.new( "month" )
 
puts "#{months[0]}"
puts "#{months[72]}"
puts months

EOF

chmod 755 $program
./$program
~~~

### 双引号和单引号区别

双引号里面可以 interpolation 以及 escape 。单引号不可以。单引号字符串字面量里只可以用反斜线来转义单引号和反斜线。

~~~
a = 1
"#{a}"
'#{a}'
puts "a\nb"
puts 'a\nb'
~~~

### 变量

Ruby 支持五种类型的变量。

- 一般小写字母、下划线开头：变量（Variable）。
- `$`开头：全局变量（Global variable）。
- `@`开头：实例变量（Instance variable）。
- `@@`开头：类变量（Class variable）类变量被共享在整个继承链中
- 大写字母开头：常数（Constant）。

~~~ruby
program=variable.rb
cat << EOF > $program
#!/usr/bin/env ruby

\$global_variable = 10
class Class1
  def print_global
      puts "全局变量在 Class1 中输出为 #\$global_variable"
  end
end
class Class2
  def print_global
      puts "全局变量在 Class2 中输出为 #\$global_variable"
  end
end
 
class1obj = Class1.new
class1obj.print_global
class2obj = Class2.new
class2obj.print_global

puts '----------------------------------------------'
class Customer
   def initialize(id, name, addr)
      @cust_id=id
      @cust_name=name
      @cust_addr=addr
   end
   def display_details()
      puts "Customer id #@cust_id"
      puts "Customer name #@cust_name"
      puts "Customer address #@cust_addr"
    end
end
 
# 创建对象
cust1=Customer.new("1", "John", "Wisdom Apartments, Ludhiya")
cust2=Customer.new("2", "Poul", "New Empire road, Khandala")
 
# 调用方法
cust1.display_details()
cust2.display_details()

puts '----------------------------------------------'
class Customer
   @@no_of_customers=0
   def initialize(id, name, addr)
      @cust_id=id
      @cust_name=name
      @cust_addr=addr
   end
   def display_details()
      puts "Customer id #@cust_id"
      puts "Customer name #@cust_name"
      puts "Customer address #@cust_addr"
    end
    def total_no_of_customers()
       @@no_of_customers += 1
       puts "Total number of customers: #@@no_of_customers"
    end
end
 
# 创建对象
cust1=Customer.new("1", "John", "Wisdom Apartments, Ludhiya")
cust2=Customer.new("2", "Poul", "New Empire road, Khandala")
 
# 调用方法
cust1.total_no_of_customers()
cust2.total_no_of_customers()

puts '----------------------------------------------'
class Example
   VAR1 = 100
   VAR2 = 200
   def show
       puts "第一个常量的值为 #{VAR1}"
       puts "第二个常量的值为 #{VAR2}"
   end
end
 
# 创建对象
object=Example.new()
object.show

EOF

chmod 755 $program
./$program
~~~

**Ruby 伪变量**

它们是特殊的变量，有着局部变量的外观，但行为却像常量。您不能给这些变量赋任何值。

- **self:** 当前方法的接收器对象。
- **true:** 代表 true 的值。
- **false:** 代表 false 的值。
- **nil:** 代表 undefined 的值。
- **__FILE__:** 当前源文件的名称。
- **__LINE__:** 当前行在源文件中的编号。

### 双冒号运算符 "::"

两个冒号 **::** 来引用类或模块中的常量

~~~
MR_COUNT = 0        # 定义在主 Object 类上的常量
module Foo
  MR_COUNT = 0
  ::MR_COUNT = 1    # 设置全局计数为 1
  MR_COUNT = 2      # 设置局部计数为 2
end
puts MR_COUNT       # 这是全局常量
puts Foo::MR_COUNT  # 这是 "Foo" 的局部常量

CONST = ' out there'
class Inside_one
   CONST = proc {' in there'}
   def where_is_my_CONST
      ::CONST + ' inside one'
   end
end
class Inside_two
   CONST = ' inside two'
   def where_is_my_CONST
      CONST
   end
end
puts Inside_one.new.where_is_my_CONST
puts Inside_two.new.where_is_my_CONST
puts Object::CONST + Inside_two::CONST
puts Inside_two::CONST + CONST
puts Inside_one::CONST
puts Inside_one::CONST.call + Inside_two::CONST
~~~

### 多行注释

使用 **=begin** 和 **=end** 语法注释多行，如下所示：

~~~
program=comment.rb
cat << EOF > $program
#!/usr/bin/env ruby

puts "Hello, Ruby!"
 
=begin
这是一个多行注释。
可扩展至任意数量的行。
但 =begin 和 =end 只能出现在第一行和最后一行。 
=end

EOF

chmod 755 $program
./$program
~~~

### 循环

~~~
program=loop.rb
cat << EOF > $program
#!/usr/bin/env ruby

puts '----------------------------------------------'
i = 0
num = 5
 
while i < num  do
   puts("在循环语句中 i = #{i}" )
   i +=1
end

puts '----------------------------------------------'
\$i = 0
\$num = 5
begin
   puts("在循环语句中 i = #\$i" )
   \$i +=1
end while \$i < \$num

puts '----------------------------------------------'
\$i = 0
\$num = 5
 
until \$i > \$num  do
   puts("在循环语句中 i = #\$i" )
   \$i +=1;
end

puts '----------------------------------------------'
\$i = 0
\$num = 5
begin
   puts("在循环语句中 i = #\$i" )
   \$i +=1;
end until \$i > \$num

puts '----------------------------------------------'
for i in 0..5
   puts "局部变量的值为 #{i}"
end

puts '----------------------------------------------'
(0..5).each do |i|
   puts "局部变量的值为 #{i}"
end

EOF

chmod 755 $program
./$program
~~~

### 块（block）

- 块由大量的代码组成。
- 您需要给块取个名称。
- 块中的代码总是包含在大括号 {} 内。
- 块总是从与其具有相同名称的函数调用。这意味着如果您的块名称为 *test*，那么您要使用函数 *test* 来调用这个块。
- 您可以使用 *yield* 语句来调用块。

~~~
program=block.rb
cat << EOF > $program
#!/usr/bin/env ruby

def test
   puts "在 test 方法内"
   yield
   puts "你又回到了 test 方法内"
   yield
end
test {puts "你在块内"}

puts '----------------------------------------------'
def test
   yield 5, 'five'
   puts "在 test 方法内"
   yield 100, 'one hundred'
end
test {|a, b| puts "你在块 #{a} 内 #{b}"}

puts '----------------------------------------------'
def test
  yield
end
test{ puts "Hello world"}

puts '----------------------------------------------'
def test(&block)
   block.call
end
test { puts "Hello World!"}

EOF

chmod 755 $program
./$program
~~~

### 模块（Module）

模块（Module）是一种把方法、类和常量组合在一起的方式。模块（Module）为您提供了两大好处。

- 模块提供了一个*命名空间*和避免名字冲突。
- 模块实现了 *mixin* 装置。

模块（Module）定义了一个命名空间，相当于一个沙盒，在里边您的方法和常量不会与其他地方的方法常量冲突。

模块类似与类，但有一下不同：

- 模块不能实例化
- 模块没有子类
- 模块只能被另一个模块定义

~~~ruby
cat << EOF > support.rb
module Week
   FIRST_DAY = "Sunday"
   def Week.weeks_in_month
      puts "You have four weeks in a month"
   end
   def Week.weeks_in_year
      puts "You have 52 weeks in a year"
   end
end

EOF

program=module.rb
cat << EOF > $program
#!/usr/bin/env ruby

\$LOAD_PATH << '.'
require "support"
 
class Decade
include Week
   no_of_yrs=10
   def no_of_months
      puts Week::FIRST_DAY
      number=10*12
      puts number
   end
end
d1=Decade.new
puts Week::FIRST_DAY
Week.weeks_in_month
Week.weeks_in_year
d1.no_of_months

EOF

chmod 755 $program
./$program
~~~

### Mixins

Ruby 不直接支持多重继承，但是 Ruby 的模块（Module）有另一个神奇的功能。它几乎消除了多重继承的需要，提供了一种名为 *mixin* 的装置。

Ruby 没有真正实现多重继承机制，而是采用成为mixin技术作为替代品。将模块include到类定义中，模块中的方法就mix进了类中。

下面代码中：

- 模块 A 由方法 a1 和 a2 组成。
- 模块 B 由方法 b1 和 b2 组成。
- 类 Sample 包含了模块 A 和 B。
- 类 Sample 可以访问所有四个方法，即 a1、a2、b1 和 b2。

~~~
program=mixin.rb
cat << EOF > $program
#!/usr/bin/env ruby

module A
   def a1
     puts "a1"
   end
   def a2
     puts "a2"   
   end
end
module B
   def b1
     puts "b1"   
   end
   def b2
     puts "b2"   
   end
end
 
class Sample
include A
include B
   def s1
     puts "s1"
   end
end
 
samp=Sample.new
samp.a1
samp.a2
samp.b1
samp.b2
samp.s1

EOF

chmod 755 $program
./$program
~~~

### 时间

~~~
program=time.rb
cat << EOF > $program
#!/usr/bin/env ruby

time1 = Time.new
 
puts "当前时间 : " + time1.inspect
 
# Time.now 功能相同
time2 = Time.now
puts "当前时间 : " + time2.inspect

puts '----------------------------------------------'
time = Time.new
 
# Time 的组件
puts "当前时间 : " + time.inspect
puts time.year    # => 日期的年份
puts time.month   # => 日期的月份（1 到 12）
puts time.day     # => 一个月中的第几天（1 到 31）
puts time.wday    # => 一周中的星期几（0 是星期日）
puts time.yday    # => 365：一年中的第几天
puts time.hour    # => 23：24 小时制
puts time.min     # => 59
puts time.sec     # => 59
puts time.usec    # => 999999：微秒
puts time.zone    # => "UTC"：时区名称

puts '----------------------------------------------'
# July 8, 2008
Time.local(2008, 7, 8)  
# July 8, 2008, 09:10am，本地时间
Time.local(2008, 7, 8, 9, 10)   
# July 8, 2008, 09:10 UTC
Time.utc(2008, 7, 8, 9, 10)  
# July 8, 2008, 09:10:11 GMT （与 UTC 相同）
Time.gm(2008, 7, 8, 9, 10, 11)

puts '----------------------------------------------'
time = Time.new
 
puts time.to_s
puts time.ctime
puts time.localtime
puts time.strftime("%Y-%m-%d %H:%M:%S")

puts '----------------------------------------------'
now = Time.now           # 当前时间
puts now
 
past = now - 10          # 10 秒之前。Time - number => Time
puts past
 
future = now + 10        # 从现在开始 10 秒之后。Time + number => Time
puts future
 
diff = future - now      # => 10  Time - Time => 秒数
puts diff

EOF

chmod 755 $program
./$program
~~~

### 范围（Range）

~~~
program=range.rb
cat << EOF > $program
#!/usr/bin/env ruby

range1 = (1..10).to_a
range2 = ('bar'..'bat').to_a
puts "#{range1}"
puts "#{range2}"

puts '----------------------------------------------'
digits = 0..9
 
puts digits.include?(5)
ret = digits.min
puts "最小值为 #{ret}"
 
ret = digits.max
puts "最大值为 #{ret}"
 
ret = digits.reject {|i| i < 5 }
puts "不符合条件的有 #{ret}"
 
digits.each do |digit|
   puts "在循环中 #{digit}"
end

puts '----------------------------------------------'
score = 70
 
result = case score
when 0..40
    "糟糕的分数"
when 41..60
    "快要及格"
when 61..70
    "及格分数"
when 71..100
       "良好分数"
else
    "错误的分数"
end

puts result

puts '----------------------------------------------'
if ((1..10) === 5)
  puts "5 在 (1..10)"
end
 
if (('a'..'j') === 'c')
  puts "c 在 ('a'..'j')"
end
 
if (('a'..'j') === 'z')
  puts "z 在 ('a'..'j')"
end

EOF

chmod 755 $program
./$program
~~~

### 迭代器（iterator）

迭代器（iterator）是*集合*支持的方法。存储一组数据成员的对象称为集合。在这里我们将讨论两种迭代器，*each* 和 *collect*。

- each： 迭代器返回数组或哈希的所有元素。
- collect： 返回整个集合，不管它是数组或者是哈希。感觉类似map-reduce中的map。

~~~ruby
program=iterator.rb
cat << EOF > $program
#!/usr/bin/env ruby

puts '----------------------------------------------'
ary = [1,2,3,4,5]
ary.each do |i|
   puts i
end

puts '----------------------------------------------'
a = [1,2,3,4,5]
b = Array.new
b = a.collect{ |x|x }
puts b

puts '----------------------------------------------'
a = [1,2,3,4,5]
b = a.collect{|x| 10*x}
puts b

EOF

chmod 755 $program
./$program
~~~

### 输入输出

~~~
program=input_output.rb
cat << EOF > $program
#!/usr/bin/env ruby

puts '----------------------------------------------'
val1 = "This is variable one"
val2 = "This is variable two"
puts val1
puts val2

puts '----------------------------------------------'
puts "Enter a value :"
val = gets
puts val

puts '----------------------------------------------'
# 与 puts 语句不同，puts 语句输出整个字符串到屏幕上，而 putc 语句可用于依次输出一个字符。
str="Hello Ruby!"
putc str

puts '----------------------------------------------'
# print 语句与 puts 语句类似。唯一的不同在于 puts 语句在输出内容后会跳到下一行，而使用 print 语句时，光标定位在同一行。
print "Hello World"
print "Good Morning"

EOF

chmod 755 $program
./$program
~~~

**[puts,p,print的区别](https://www.cnblogs.com/yjmyzz/archive/2010/02/22/1671130.html)**

puts 输出内容后，会自动换行(如果内容参数为空，则仅输出一个换行符号)；另外如果内容参数中有转义符，输出时将先处理转义再输出
p 基本与puts相同，但不会处理参数中的转义符号
print 基本与puts相同，但输出内容后，不会自动在结尾加上换行符

另外，在输出双字节的字符，比如全角英文或汉字时，p会输出对应的二个字节对应的数字，而非字符

```
s = "aaaa\nbb\tbb"
p s
p "****************"
puts s
p "****************"
print s

s = "中"
 
p s
puts s
print s
```

### 文件操作

- *File.new* 方法创建一个 *File* 对象用于读取、写入或者读写，读写权限取决于 mode 参数。最后，您可以使用 *File.close* 方法来关闭该文件。
- *File.open* 方法创建一个新的 file 对象，并把该 file 对象赋值给文件。但是，*File.open* 和 *File.new* 方法之间有一点不同。不同点是 *File.open* 方法可与块关联，而 *File.new* 方法不能。

~~~
program=file.rb
cat << EOF > $program
#!/usr/bin/env ruby

puts '----------------------------------------------'
aFile = File.new("input.txt", "w+")
if aFile
   aFile.syswrite("ABCDEFGHIJKLKMNOPQ\nRSTUVW\nXYZ\n")
   aFile.rewind
   # 方法 each_byte 是个可以迭代字符串中每个字符
   aFile.each_byte {|ch| putc ch; putc ?. }   
else
   puts "Unable to open file!"
end
puts

puts '----------------------------------------------'
aFile = File.new("input.txt", "r")
if aFile
   content = aFile.sysread(10)
   puts content
else
   puts "Unable to open file!"
end

puts '----------------------------------------------'
arr = IO.readlines("input.txt")
puts arr[0]
puts arr[1]

puts '----------------------------------------------'
IO.foreach("input.txt"){|block| puts block}

EOF

chmod 755 $program
./$program
~~~

### 异常

- 使用 *rescue* 块捕获异常，然后使用 *retry* 语句从开头开始执行 *begin* 块。
- 使用 *raise* 语句抛出异常
- 使用 ensure语句，无论是否抛出异常，保证一些处理在代码块结束时完成
- 使用 *else* 子句，表示如果没有异常则执行，它一般是放置在 *rescue* 子句之后，任意 *ensure* 之前。

~~~ruby
program=exception.rb
cat << EOF > $program
#!/usr/bin/env ruby

puts '----------------------------------------------'
begin
   file = open("/unexistant_file")
   if file
      puts "File opened successfully"
   end
rescue
      file = STDIN
end
print file, "==", STDIN, "\n"

puts '----------------------------------------------'
fname = "/unexistant_file"
begin
   file = open(fname)
   if file
      puts "File opened successfully"
   end
rescue
   fname = "input.txt"
   puts 'change file name'
   retry
end

puts '----------------------------------------------'
begin  
    puts 'I am before the raise.'  
    raise 'An error has occurred.'  
    puts 'I am after the raise.'  
rescue  
    puts 'I am rescued.'  
end  
puts 'I am after the begin block.'

puts '----------------------------------------------'
begin  
  raise 'A test exception.'  
rescue Exception => e  
  puts e.message  
  puts e.backtrace.inspect  
end

puts '----------------------------------------------'
begin
  raise 'A test exception.'
rescue Exception => e
  puts e.message
  puts e.backtrace.inspect
ensure
  puts "Ensuring execution"
end

puts '----------------------------------------------'
begin
 # 抛出 'A test exception.'
 puts "I'm not raising exception"
rescue Exception => e
  puts e.message
  puts e.backtrace.inspect
else
   puts "Congratulations-- no errors!"
ensure
  puts "Ensuring execution"
end

EOF

chmod 755 $program
./$program
~~~

**Catch 和 Throw**

raise 和 rescue 的异常机制能在发生错误时放弃执行，有时候需要在正常处理时跳出一些深层嵌套的结构。此时 catch 和 throw 就派上用场了。

*catch* 定义了一个使用给定的名称（可以是 Symbol 或 String）作为标签的块。块会正常执行直到遇到一个 throw。

下面例子中，用户键入 '!' 回应任何提示，使用一个 throw 终止与用户的交互。

~~~
program=try.rb
cat << EOF > $program
#!/usr/bin/env ruby

def promptAndGet(prompt)
   print prompt
   res = readline.chomp
   throw :quitRequested if res == "!"
   return res
end
 
catch :quitRequested do
   name = promptAndGet("Name: ")
   age = promptAndGet("Age: ")
   sex = promptAndGet("Sex: ")
   # ..
   # 处理信息
end

EOF

chmod 755 $program
./$program
~~~

## 参考

- [20 minutes quickstart](https://www.ruby-lang.org/zh_cn/documentation/quickstart/)
- [Ruby 教程](https://www.runoob.com/ruby/ruby-tutorial.html)

