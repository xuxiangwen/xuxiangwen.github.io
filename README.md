## Github Pages+Jekyll

### 发布

1. 编写blog，把blog提交到github下_posts目录。

2. 发布blog。

   ~~~
   ~/eipi10/xuxiangwen.github.io/_bin/publish.sh
   ~~~

### 本地开发和测试

~~~shell
cd ~/eipi10/xuxiangwen.github.io
git pull
_bin/generate.sh _posts
_bin/start.sh
~~~

### 部署

#### 配置_config.yml

~~~
cat << EOF > _config.yml
title: Weclome to eipi10
description: stay hungry, stay foolish
theme: jekyll-theme-architect
permalink: pretty 
show_downloads: false
markdown: kramdown
highlighter: rouge
google_analytics: UA-154374268-1
defaults:
  - scope:
      path: ""
      type: "posts"
    values:
      layout: "post"
  - scope:
      path: ""
    values:
      layout: "default"

# Gitalk settings
gitalk_clientID: 8278f492ce9a6b43f85d
gitalk_clientSecret: 68a96d3c76e8ac218d9afa4e93add583ce3535c4
gitalk_repo: xuxiangwen.github.io
gitalk_owner: xuxiangwen
EOF

~~~



#### 配置Gemfile

~~~
cat << EOF >> Gemfile
# frozen_string_literal: true

source "https://rubygems.org"

git_source(:github) {|repo_name| "https://github.com/#{repo_name}" }

# gem "rails"

gem "jekyll"
gem "jekyll-theme-architect"
gem "github-pages", group: :jekyll_plugins
EOF

cat Gemfile
~~~

#### 安装依赖包

##### 第一次

~~~
bundle install
~~~

##### 更新

~~~
bundle update
~~~

#### 配置theme

##### Stylesheet

在 `@import` 后面添加自定义的 CSS (or Sass, including imports)

~~~
mkdir -p assets/css
cat << EOF > assets/css/style.scss
---
---

@import "{{ site.theme }}";

body {
  font-size: 14px;
}

header {
  padding-top: 20px;
  padding-bottom: 20px;
}

header h1 {
  font-size: 36px;
 }
  
header h2 {
  font-size: 18px;
 }  
  
 
#main-content h1 {
  font-size: 32px;
}

#main-content h2 {
  font-size: 28px;
}

#main-content h3 {
  font-size: 24px;
}

#main-content h4 {
  font-size: 18px;
}

aside#sidebar h2 {
  margin-top: 0;
  margin-bottom: 0;
  font-size: 24px;
  font-weight: normal;
  font-family: 'Architects Daughter', 'Helvetica Neue', Helvetica, Arial, serif;
  line-height: 1.3;
  letter-spacing: 0; }

aside#sidebar h3 {
  margin-top: 0;
  margin-bottom: 0;
  font-size: 15px;
  font-weight: normal;
  line-height: 1.5;
  color: #9ddcff;
  letter-spacing: 0; }

EOF
~~~

> *Note: If you'd like to change the theme's Sass variables, you must set new values before the `@import` line in your stylesheet.*

~~~
body {
  background: white; }
aside#sidebar {
  min-height: 100%;
  background: #fafafa; }
~~~

##### Layouts

为了更好的展现效果，需要自定义layout，下面代码从原来的theme中下载layout。

~~~
mkdir -p _layouts
wget https://raw.githubusercontent.com/pages-themes/architect/master/_layouts/default.html -P _layouts
~~~

##### Latex支持

默认情况下，不支持Latex（也就是解释\$\$或\$）。

~~~
mkdir -p _includes
cat << EOF >> _includes/head.html
<script type="text/x-mathjax-config">
    MathJax.Hub.Config({
      tex2jax: {
        skipTags: ['script', 'noscript', 'style', 'textarea', 'pre'],
        inlineMath: [['$','$']]
      }
    });
  </script>
  <script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script> 
  
EOF
~~~

#### 生成blog

每一篇markdown文件，然后通过下面命令进行生成。

~~~
# 重新生成所有的发布文件
_bin/generate.sh _posts     
# 指定文件生成发布文件
_bin/generate.sh _posts/vector-and-matrix.md
~~~

上面命令主要做了：

1. 从要发布的markdown文件的front matter中获取日期，然后复制文件，新的文件名是`<日期>-<原文件名>`
2. 删除之前发布的文件
3. 把文件中图片的相对路径由`images`改成`/assets/images`
4. 把`$$`前后各添加一个换行符。在typora中，如果`$$`是一行的开始，是默认居中，而在github pages中默认显示的是和文本混合在一起（inline mode），在前后添加换行符后，解决这个问题。
5. 把单个`$`换成`$$`。一个`$`在github pages中，对于其中换行符号`\\`会变成`\`，`$$`可以正常显示。
6. 在`{{`中间插入一个换行符，避免被Jekyll识别为Liquid。
7. 把图片从markdown文件所在目录的`images`中拷贝到`/assets/images`目录中去。

### Obsolete

#### 整理latex

>  这部分逻辑已经放到`生成blog`中

markdown中的latex部分，\$\$表示居中，在github pages中需要前面必须有一个空行才可以达到这样的效果。

**整理文件夹**

~~~
_bin/md_clean.sh _posts
_bin/md_clean.sh _notes
~~~

**整理一个文件**

~~~
_bin/md_clean.sh _posts/vector-and-matrix.md
~~~

