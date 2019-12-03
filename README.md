---
layout: default
title: README
---

## Github Pages配置

### 配置_config.yml

~~~
cat << EOF > _config.yml
title: 欢迎来到eipi10!
description: 记录了学习的经历和所得，分享给所有的朋友
theme: jekyll-theme-architect
permalink: pretty 
show_downloads: false
markdown: kramdown
highlighter: rouge
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
      
EOF
~~~

### 配置Gemfile

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

### 安装依赖包

#### 第一次

~~~
bundle install
~~~

#### 更新

~~~
bundle update
~~~

### 运行

##### 本地开发

~~~
bundle exec jekyll serve --host 0.0.0.0 --port 4000
~~~

### 配置theme

#### Stylesheet

在 `@import` 后面添加自定义的 CSS (or Sass, including imports)

~~~
mkdir -p assets/css
cat << EOF > assets/css/style.scss
---
---

@import "{{ site.theme }}";

EOF
~~~

> *Note: If you'd like to change the theme's Sass variables, you must set new values before the `@import` line in your stylesheet.*

#### Layouts

为了更好的展现效果，需要自定义layout，下面代码从原来的theme中下载layout。

~~~
mkdir -p _layouts
wget https://raw.githubusercontent.com/pages-themes/architect/master/_layouts/default.html -P _layouts
~~~

#### Latex支持

默认情况下，不支持Latex（也就是\$\$或\$）。

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

### 整理latex

markdown中的latex部分，\$\$表示居中，在github pages中需要前面必须有一个空行才可以达到这样的效果。

#### **整理文件夹**

~~~
_bin/md_clean.sh _posts
_bin/md_clean.sh _notes
~~~

#### **整理一个文件**

~~~
_bin/md_clean.sh _posts/vector-and-matrix.md
~~~

### 发布blog

每一篇文章，其front matter中必须有日期，然后通过下面命令进行发布。

~~~
_bin/publish.sh _posts
_bin/publish.sh _posts/vector-and-matrix.md
~~~



