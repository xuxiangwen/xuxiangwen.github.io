---
title: jekyll下Markdown的填坑技巧
categories: others
date: 2019-12-07
---

花了一周多，总算把blog系统部署在github pages+jekyll的环境下了，其中碰到了一些小坑，下文将把这些坑和以及填坑技巧分享一下。

### 图片路径的引用

在本地编写Markdown文件的时候，往往会引用很多本地图片。比如，`![img](/assets/images/1575457889152.png)`，这条语句将会显示（当前目录下）`images`目录下的`1575457889152.png`文件。当把Markdown文件部署到Jekyll上，它会根据设定会把文件拷贝到_site目录下的某个位置（比如：`\_site/others/2019/12/08/jekyll-Markdown-skills/`），然而这过程中，它并不会去拷贝Markdown中引用的图片，这将造成在图片在网页中无法显示。

一般推荐的解决方案是把`1575457889152.png`拷贝到Jekyll根目录下`assets/images`目录，然后把文件中引用语句变成`![img](/assets/images/1575457889152.png)`，

下面是替换的shell脚本。

~~~shell
markdown_file=<Markdown File>
jekyll_image_path=<Jekyll Root Path>/assets/images
# 修改图片的引用路径
sed -i 's/(images\//(\/assets\/images\//g'  $markdown_file

# 把图片拷贝到Jekyll的图片目录
file_folder=$(dirname "$markdown_file")
file_name=$(basename "$markdown_file")
cp $file_folder/images/* $jekyll_image_path
~~~

需要指定`Markdown File`和`Jekyll Root Path`两个参数。

据说某些Jekyll plugin可以自动J来做上面的动作。比如：[How to get jekyll to copy sub folder?](https://stackoverflow.com/questions/19580492/how-to-get-jekyll-to-copy-sub-folder)， 大家有兴趣可以看看。

> 在windows下，可以安装[git for windows](https://gitforwindows.org/)，然后在git bash中可以执行上面的shell脚本。下文中的所有shell脚本也都是可以在 git bash中执行的。

### 支持Tex/LaTexwenjia

默认情况下，Jekyll不能正确显示Tex/LaTex，需要把下面的代码添加Markdown文件所使用的[Layout](https://jekyllrb.com/docs/layouts/)中去。

~~~
  <script type="text/x-mathjax-config">
    MathJax.Hub.Config({
      tex2jax: {
        skipTags: ['script', 'noscript', 'style', 'textarea', 'pre'],
        inlineMath: [['$','$']]
      }
    });
  </script>
  <script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>
~~~

### Display Math换行居中问题。

平时最喜欢用的Markdown编辑器是[Typora]()，它的Tex/LaTex语法支持Display Math ，也就是在\$\$中编写数学公式。比如：
```Markdown

$$

\begin{align*}
y = y(x,t) &= A e^{i\theta} \\
&= A (\cos \theta + i \sin \theta) \\
&= A (\cos(kx - \omega t) + i \sin(kx - \omega t)) 
\end{align*}

$$

```
在Typora显示如下:

![image-20191207152444450](/assets/images/image-20191207152444450.png)

其中数学公式居中显示，和`公式一:`不在同一行。然而相同语句，Jekyll中的显示如下：

![image-20191207152351788](/assets/images/image-20191207152351788.png)

在Jekyll中，数学公式和文本`公式一:`在一行，而且靠左显示。这样的效果非常难看。解决办法也很简单，即把所有的\$\$前后都插入一个空行，就可以解决这个问题，代码如下。

~~~shell
markdown_file=<Markdown File>
awk '{
if ($0 ~ /^\s*\$\$\s*$/)
	print "\n"$0"\n"
else 
  print $0
}' $markdown_file > temp.md
cat -s temp.md > $markdown_file
rm -rf temp.md
~~~

### Inline Math对矩阵的显示

Typora的Tex/LaTex语法也支持Inline Math，也就是把数学公式和文本在同一行中显示。比如：$e^{i\pi}+1=0$，其背后的语句是**\$e^{i\pi}+1=0\$**，也就是在两个\$符号中编写Tex/LaTex。然而，采用这种方式编写矩阵时，同样的语句，typora和网页上的效果可能不太一样。

- Typora中显示: ![image-20191207152516193](/assets/images/image-20191207152516193.png)
- Jekyll中显示: ![image-20191207152610759](/assets/images/image-20191207152610759.png)

其实上面公式，对应的语句是一个，即
~~~
$\begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}\$
~~~

解决的方法很简单，把一个\$变成两个\$，即

~~~
$$\begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$$
~~~

这样就可以在Typora和Jekyll中获得一样的效果。所以在编写Tex/LaTex，最好就用\$\$而不要用\$。

### Tex/LaTex中\{\{被Jekyll当作[Liquid](https://jekyllrb.com/docs/liquid/)

Jekyll把\{\{和\}\}中内容解析成Liquid，如果Tex/LaTex总包含\{\{，会被误识为Liquid，这样会产生Page Build Error。使用下面脚本，在两个\{中插入一个换行符。

~~~
markdown_file=<Markdown File>
sed -i 's/{\s*{/{ \n {/g' $markdown_file
~~~

### 支持[Mermaid](https://mermaidjs.github.io/)

Mermaid是一个从文本生成图表和流程图的工具。默认情况下，Jekyll不能正确显示它，需要把下面的代码添加Markdown文件所使用的[Layout](https://jekyllrb.com/docs/layouts/)中去。

~~~
<script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/8.0.0/mermaid.min.js"></script>
<script>
  var config = {
    startOnLoad:true,
    theme: 'forest',
    flowchart:{
            useMaxWidth:false,
            htmlLabels:true
        }
  };
  mermaid.initialize(config);
  window.mermaid.init(undefined, document.querySelectorAll('.language-mermaid'));
</script>
~~~

### Summary

把上面的shell脚本汇总起来，可以创建下面的脚本来整理markdown文件。

~~~shell
cat << EOF > clean.sh
markdown_file=$1
jekyll_image_path=$2

cp $markdown_file  $markdown_file.bak
# 修改图片的引用路径
sed -i 's/(images\//(\/assets\/images\//g'  $markdown_file

# 把图片拷贝到Jekyll的图片目录
file_folder=$(dirname "$markdown_file")
file_name=$(basename "$markdown_file")
cp $file_folder/images/* $jekyll_image_path

# Tex/LaTex Display Math换行居中
awk '{
if ($0 ~ /^\s*\$\$\s*$/)
	print "\n"$0"\n"
else 
  print $0
}' $markdown_file > temp.md
cat -s temp.md > $markdown_file
rm -rf temp.md

# 避免\{\{被Jekyll当作Liquid
sed -i 's/{\s*{/{ \n {/g' $markdown_file
  
EOF
~~~

在Jekyll根目录，执行以下语句。

~~~
./clean.sh _posts/<Markdown File> assets/images
~~~

`Markdown File`是要清理的Markdown文件。
