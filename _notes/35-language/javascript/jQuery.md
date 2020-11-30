# jQuery

## 选择器

### 按ID查找

~~~javascript
// 查找<div id="abc">:
var div = $('#abc');  
// [<div id="abc">...</div>]  返回一个数组

//jQuery对象和DOM对象之间可以互相转化：
var div = $('#abc'); // jQuery对象
var divDom = div.get(0); // 假设存在div，获取第1个DOM元素
var another = $(divDom); // 重新把DOM包装为jQuery对象
~~~

### 按tag查找

~~~javascript
// 按tag查找
var ps = $('p'); // 返回所有<p>节点
ps.length; // 数一数页面有多少个<p>节点
~~~

### 按class查找

~~~js
var a = $('.red'); // 所有节点包含`class="red"`都将返回
// 例如:
// <div class="red">...</div>
// <p class="green red">...</p>

var a = $('.red.green'); // 注意没有空格！
// 符合条件的节点：
// <div class="red green">...</div>
// <div class="blue green red">...</div>
~~~

### 按属性查找

~~~js
var email = $('[name=email]'); // 找出<??? name="email">
var passwordInput = $('[type=password]'); // 找出<??? type="password">
var a = $('[items="A B"]'); // 找出<??? items="A B">

//使用前缀查找或者后缀查找：
var icons = $('[name^=icon]'); // 找出所有name属性值以icon开头的DOM
// 例如: name="icon-1", name="icon-2"
var names = $('[name$=with]'); // 找出所有name属性值以with结尾的DOM
// 例如: name="startswith", name="endswith"
~~~

### 组合查找

~~~js
var emailInput = $('input[name=email]'); // 不会找出<div name="email">

// 根据tag和class
var tr = $('tr.red'); // 找出<tr class="red ...">...</tr> 
~~~

### 多项选择器

~~~js
$('p,div'); // 把<p>和<div>都选出来
$('p.red,p.green'); // 把<p class="red">和<p class="green">都选出来
~~~

### 测试一

参见https://www.liaoxuefeng.com/wiki/1022910821149312/1023023555539648

对于下面的html。

~~~html
<!-- HTML结构 -->
<div id="test-jquery">
    <p id="para-1" class="color-red">JavaScript</p>
    <p id="para-2" class="color-green">Haskell</p>
    <p class="color-red color-green">Erlang</p>
    <p name="name" class="color-black">Python</p>
    <form class="test-form" target="_blank" action="#0" onsubmit="return false;">
        <legend>注册新用户</legend>
        <fieldset>
            <p><label>名字: <input name="name"></label></p>
            <p><label>邮件: <input name="email"></label></p>
            <p><label>口令: <input name="password" type="password"></label></p>
            <p><button type="submit">注册</button></p>
        </fieldset>
    </form>
</div>
~~~

可以用下面的语句来查找相应的内容 

- 仅选择JavaScript
- 仅选择Erlang
- 选择JavaScript和Erlang
- 选择所有编程语言
- 选择名字input
- 选择邮件和名字input

~~~js
'use strict';
var selected = null;

selected = $("p:contains(JavaScript)");
selected = $("p:contains(Erlang)");
selected = $("p:contains(JavaScript), p:contains(Erlang)");
selected =  $('p[class^=color]');
selected =  $('input');
selected =  $('input[name=name], input[name=email]');
~~~

### 层次选择器

~~~html
<!-- HTML结构 -->
<div class="testing">
    <ul class="lang">
        <li class="lang-javascript">JavaScript</li>
        <li class="lang-python">Python</li>
        <li class="lang-lua">Lua</li>
    </ul>
</div>
~~~

对于上面的html

~~~js
$('ul.lang li.lang-javascript'); // [<li class="lang-javascript">JavaScript</li>]
$('div.testing li.lang-javascript'); // [<li class="lang-javascript">JavaScript</li>]

$('ul.lang li'); // 选出JavaScript、Python和Lua 3个节点

$('ul.lang li:first-child'); // 仅选出JavaScript
$('ul.lang li:last-child'); // 仅选出Lua
$('ul.lang li:nth-child(2)'); // 选出第N个元素，N从1开始
$('ul.lang li:nth-child(even)'); // 选出序号为偶数的元素
$('ul.lang li:nth-child(odd)'); // 选出序号为奇数的元素
~~~

### 测试二

参见https://www.liaoxuefeng.com/wiki/1022910821149312/1028314028519040

对于下面的html。

~~~html
<!-- HTML结构 -->

<div class="test-selector">
    <ul class="test-lang">
        <li class="lang-javascript">JavaScript</li>
        <li class="lang-python">Python</li>
        <li class="lang-lua">Lua</li>
    </ul>
    <ol class="test-lang">
        <li class="lang-swift">Swift</li>
        <li class="lang-java">Java</li>
        <li class="lang-c">C</li>
    </ol>
</div>
~~~

分别选择所有语言，所有动态语言，所有静态语言，JavaScript，Lua，C等:

~~~js
'use strict';
var selected = null;

selected = $('li.lang-javascript, li.lang-lua, li.lang-c');
~~~

## 操作