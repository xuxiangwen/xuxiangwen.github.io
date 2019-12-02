Jekyll 是一个简单的博客形态的静态站点生产机器。它有一个模版目录，其中包含原始文本格式的文档，通过一个转换器（如 [Markdown](http://daringfireball.net/projects/markdown/)）和我们的 [Liquid](https://github.com/Shopify/liquid/wiki) 渲染器转化成一个完整的可发布的静态网站，你可以发布在任何你喜爱的服务器上。Jekyll 也可以运行在 [GitHub Page](http://pages.github.com/) 上，也就是说，你可以使用 GitHub 的服务来搭建你的项目页面、博客或者网站，而且是**完全免费**的。

## 例子

- [入门](example\myblog\README.md) 
-  [Docker](example\docker-myblog\README.md) 






### themes

#### use theme from gem

查找[jekyll-theme](https://rubygems.org/search?utf8=✓&query=jekyll-theme)

~~~
theme=classic-jekyll-theme
# theme=minima
sed -i  "s/theme:.*/theme: $theme/g" _config.yml
if [ `grep -c $theme Gemfile` -eq 0 ];then  
    echo add $theme in Gemfile
    echo gem \"$theme\" >> Gemfile
fi  
bundle update

# 更新layout
folder=_posts
layout=post
for file_name in `ls $folder/*.md`
do
  sed -i  "s/layout:.*/layout: $layout/g" $file_name
done

bundle exec jekyll serve
~~~

#### custom theme

~~~
mkdir -p _layouts
cat << EOF > _layouts/post.html
---
author: "xu jian"
---
<h1>{{ page.title }}</h1>
<h3>{{ layout.author }}</h3>
{{ content }}

EOF
~~~

查看页面变化， 还原页面。

~~~
rm -rf _layouts/post.html
~~~


# 

- `_site`文件夹需要你在`.gitignore`中加入屏蔽