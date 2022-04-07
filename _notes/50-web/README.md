## [JS中$含义及用法](https://www.cnblogs.com/jokerjason/p/7404649.html)

- `$()`可以是`$(expresion)`，即css选择器、Xpath或html元素，也就是通过上述表达式来匹配目标元素。 

  ~~~javascript
  $("a").click(function(){...}) 						//css选择器
  alert($("div>p").html());        					//css选择器
  $("<div><p>Hello</p></div>").appendTo("body");   	//html元素
  ~~~

- `$()`可以是`$(element)`，即一个特定的DOM元素。如常用的DOM对象有document、location、form等

  ~~~javascript
  $(document).find("div>p").html()); 
  ~~~

- `$()`可以是`$(function)`，即一个函数，它是`$(document).ready()`的一个速记方式。

  原表达式：

  ~~~javascript
  $(document).ready(function(){ 
  	alert("Hello world!"); 
  }); 
  ~~~

  速写方式：

  ~~~javascript
  $(function(){ 
  	alert("Hello world!"); 
  }); 
  ~~~

## HTML Tags

### PX

px像素（Pixel）。相对长度单位。像素px是相对于显示器屏幕分辨率而言的。

**PX特点**

- IE无法调整那些使用px作为单位的字体大小；
-  国外的大部分网站能够调整的原因在于其使用了em或rem作为字体单位；
- Firefox能够调整px和em，rem，但是96%以上的中国网民使用IE浏览器(或内核)。

### EM

em是相对长度单位。相对于当前对象内文本的字体尺寸。如当前对行内文本的字体尺寸未被人为设置，则相对于浏览器的默认字体尺寸。

**EM特点**

- em的值并不是固定的；
- em会继承父级元素的字体大小。

> **注意：**任意浏览器的默认字体高都是16px。所有未经调整的浏览器都符合: 1em=16px。那么12px=0.75em,10px=0.625em。为了简化font-size的换算，需要在css中的body选择器中声明Font-size=62.5%，这就使em值变为 16px*62.5%=10px, 这样12px=1.2em, 10px=1em, 也就是说只需要将你的原来的px数值除以10，然后换上em作为单位就行了。
>
> 所以我们在写CSS的时候，需要注意两点：
>
> - body选择器中声明Font-size=62.5%；
> - 将你的原来的px数值除以10，然后换上em作为单位；
> - 重新计算那些被放大的字体的em数值。避免字体大小的重复声明。
>
> 也就是避免1.2 * 1.2= 1.44的现象。比如说你在#content中声明了字体大小为1.2em，那么在声明p的字体大小时就只能是1em，而不是1.2em, 因为此em非彼em，它因继承#content的字体高而变为了1em=12px。

### REM

rem是CSS3新增的一个相对单位（root em，根em），这个单位引起了广泛关注。这个单位与em有什么区别呢？区别在于使用rem为元素设定字体大小时，仍然是相对大小，但相对的只是HTML根元素。这个单位可谓集相对大小和绝对大小的优点于一身，通过它既可以做到只修改根元素就成比例地调整所有字体大小，又可以避免字体大小逐层复合的连锁反应。

> **注意：** *选择使用什么字体单位主要由你的项目来决定，如果你的用户群都使用最新版的浏览器，那推荐使用rem，如果要考虑兼容性，那就使用px,或者两者同时使用。*

### css单位

![img](images/figure-3.png)