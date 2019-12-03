
# [Step by Step Tutorial](https://jekyllrb.com/docs/step-by-step/01-setup/)

从scratch 一步一步构建Jekyll site。

## 1. Installation

创建Gemfile

~~~shell
rm -rf Gemfile
bundle init
cat << EOF >> Gemfile

gem "jekyll"
gem "classic-jekyll-theme"
EOF

cat Gemfile
~~~

安装

~~~shell
bundle
~~~

运行

~~~shell
bundle exec jekyll serve -H 0.0.0.0 -P 4000
~~~

添加页面。

~~~shell
cat << EOF > index.html
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Home</title>
  </head>
  <body>
    <h1>Hello World!</h1>
  </body>
</html>

EOF
~~~

访问http://localhost:4000。将显示如下内容。

![1571722746881](image/1571722746881.png)

>  Jekyll是一个静态站点生成器，主要的两个命令如下：
>
> - jekyll build： 构建站点并输出到目录`_site`
> - jekyll serve： 
>     - 构建站点并输出到目录`_site`，并监控本地变化，重建静态站点
>     - 运行一个本地网站`http://localhost:4000`

## 2. Liquid

Liquid是一个模板语言，包含三部分： [objects](https://www.jekyll.com.cn/docs/step-by-step/02-liquid/#objects), [tags](https://www.jekyll.com.cn/docs/step-by-step/02-liquid/#tags) and [filters](https://www.jekyll.com.cn/docs/step-by-step/02-liquid/#filters).

### Objects

~~~html
{{ page.title }}
~~~

### Tags

~~~html
{% if page.show_sidebar %}
  <div class="sidebar">
    sidebar content
  </div>
{% endif %}
~~~

### Filters

~~~html
{{ "hi" | capitalize }}
~~~

### 使用Liquid

~~~shell
cat << EOF > index.html
---
# 添加了front matter，Jekyll会处理Liquid
---
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Home</title>
  </head>
  <body>
    <h1>{{ "Hello World!" | downcase }}</h1>
  </body>
</html>

EOF
~~~

## 3. Front Matter

Front matter是[YAML](http://yaml.org/)的片段，位于两个`---`之间。

~~~
cat << EOF > index.html
---
title: Home
---
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>{{ page.title }}</title>
  </head>
  <body>
    <h1>{{ "Hello World!" | upcase }}</h1>
  </body>
</html>
EOF
~~~

## 4. Layouts

创建Layout来构建页面模板。

~~~shell
mkdir -p _layouts
cat << EOF > _layouts/default.html
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>{{ page.title }}</title>
  </head>
  <body>
    {{ content }}
  </body>
</html>

EOF

cat << EOF > index.html
---
layout: default
title: Home
---
<h1>{{ "Hello World!" | downcase }}</h1>

EOF

cat << EOF > about.md
---
layout: default
title: About
---
# About page

This page tells you a little bit about me.

EOF
~~~

访问http://localhost:4000/about.html。

## 5. Includes

~~~shell
mkdir -p _includes
cat << EOF > _includes/navigation.html
<nav>
  <a href="/" {% if page.url == "/" %}style="color: red;"{% endif %}>
    Home
  </a>
  <a href="/about.html" {% if page.url == "/about.html" %}style="color: red;"{% endif %}>
    About
  </a>
</nav>
EOF

cat << EOF > _layouts/default.html
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>{{ page.title }}</title>
  </head>
  <body>
    {% include navigation.html %}
    {{ content }}
  </body>
</html>

EOF
~~~

访问http://localhost:4000。

## 6. Data Files

Jekyll支持从YAML, JSON, and CSV文件中加载数据。

~~~shell
mkdir -p _data
cat << EOF > _data/navigation.yml
- name: Home
  link: /
- name: About
  link: /about.html
EOF

cat << EOF > _includes/navigation.html
<nav>
  {% for item in site.data.navigation %}
    <a href="{{ item.link }}" {% if page.url == item.link %}style="color: red;"{% endif %}>
      {{ item.name }}
    </a>
  {% endfor %}
</nav>
EOF

~~~

访问http://localhost:4000。

## 7. Assets

Jekyll一般使用结构来存储CSS, JS, image。

~~~shell
.
├── assets
|   ├── css
|   ├── images
|   └── js
...
~~~

#### Sass

[sass](http://www.ruanyifeng.com/blog/2012/06/sass.html)是一种CSS的开发工具，提供了许多便利的写法，大大节省了设计者的时间，使得CSS的开发，变得简单和可维护。

~~~shell
mkdir -p assets/css
cat << EOF > assets/css/styles.scss
---
---
@import "main";
EOF

mkdir -p _sass
cat << EOF > _sass/main.scss
.current {
  color: green;
}
EOF

cat << EOF > _layouts/default.html
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>{{ page.title }}</title>
    <link rel="stylesheet" href="/assets/css/styles.css">
  </head>
  <body>
    {% include navigation.html %}
    {{ content }}
  </body>
</html>

EOF
~~~

访问http://localhost:4000。

> 本例好像不能正常工作，显示颜色没有变化。

## 8. Blogging

~~~shell
mkdir -p _posts
cat << EOF > _posts/2018-08-20-bananas.md
---
layout: post
author: jill
---
A banana is an edible fruit – botanically a berry – produced by several kinds
of large herbaceous flowering plants in the genus Musa.

In some countries, bananas used for cooking may be called "plantains",
distinguishing them from dessert bananas. The fruit is variable in size, color,
and firmness, but is usually elongated and curved, with soft flesh rich in
starch covered with a rind, which may be green, yellow, red, purple, or brown
when ripe.

EOF

cat << EOF > _posts/2018-08-20-apples.md
---
layout: post
author: jill
---
An apple is a sweet, edible fruit produced by an apple tree.

Apple trees are cultivated worldwide, and are the most widely grown species in
the genus Malus. The tree originated in Central Asia, where its wild ancestor,
Malus sieversii, is still found today. Apples have been grown for thousands of
years in Asia and Europe, and were brought to North America by European
colonists.

EOF

cat << EOF > _posts/2018-08-20-kiwifruit.md
---
layout: post
author: ted
---
Kiwifruit (often abbreviated as kiwi), or Chinese gooseberry is the edible
berry of several species of woody vines in the genus Actinidia.

The most common cultivar group of kiwifruit is oval, about the size of a large
hen's egg (5–8 cm (2.0–3.1 in) in length and 4.5–5.5 cm (1.8–2.2 in) in
diameter). It has a fibrous, dull greenish-brown skin and bright green or
golden flesh with rows of tiny, black, edible seeds. The fruit has a soft
texture, with a sweet and unique flavor.

EOF

cat << EOF > _layouts/post.html
---
layout: default
---
<h1>{{ page.title }}</h1>
<p>{{ page.date | date_to_string }} - {{ page.author }}</p>

{{ content }}
EOF

cat << EOF > blog.html
---
layout: default
title: Blog
---
<h1>Latest Posts</h1>

<ul>
  {% for post in site.posts %}
    <li>
      <h2><a href="{{ post.url }}">{{ post.title }}</a></h2>
      <p>{{ post.excerpt }}</p>
    </li>
  {% endfor %}
</ul>
EOF
~~~

post变量的常用属性：

- `post.url` is automatically set by Jekyll to the output path of the post
- `post.title` is pulled from the post filename and can be overridden by setting `title` in front matter
- `post.excerpt` is the first paragraph of content by default

访问http://localhost:4000。

## 9. Collections

Collections和posts非常相似，只是它没有日期。

~~~shell
cat << EOF > _config.yml
collections:
  authors:
    output: true
    
defaults:
  - scope:
      path: ""
      type: "authors"
    values:
      layout: "author"
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

mkdir -p _authors
cat << EOF > _authors/jill.md
---
short_name: jill
name: Jill Smith
position: Chief Editor
---
Jill is an avid fruit grower based in the south of France.

EOF

cat << EOF > _authors/ted.md
---
short_name: ted
name: Ted Doe
position: Writer
---
Ted has been eating fruit since he was baby.

EOF

cat << EOF > staff.html
---
layout: default
---
<h1>Staff</h1>

<ul>
  {% for author in site.authors %}
    <li>
      <h2><a href="{{ author.url }}">{{ author.name }}</a></h2>
      <h3>{{ author.position }}</h3>
      <p>{{ author.content | markdownify }}</p>
    </li>
  {% endfor %}
</ul>
EOF

mkdir -p _data
cat << EOF > _data/navigation.yml
- name: Home
  link: /
- name: About
  link: /about.html
- name: Blog
  link: /blog.html
- name: Staff
  link: /staff.html
EOF

cat << EOF > _layouts/author.html
---
layout: default
---
<h1>{{ page.name }}</h1>
<h2>{{ page.position }}</h2>

{{ content }}
EOF
~~~

访问http://localhost:4000。显示如下。

![1571733380267](image/1571733380267.png)

下面把blog和author连接起来。

~~~shell
cat << EOF > _layouts/author.html
---
layout: default
---
<h1>{{ page.name }}</h1>
<h2>{{ page.position }}</h2>

{{ content }}

<h2>Posts</h2>
<ul>
  {% assign filtered_posts = site.posts | where: 'author', page.short_name %}
  {% for post in filtered_posts %}
    <li><a href="{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>
EOF

cat << EOF > _layouts/post.html
---
layout: default
---
<h1>{{ page.title }}</h1>

<p>
  {{ page.date | date_to_string }}
  {% assign author = site.authors | where: 'short_name', page.author | first %}
  {% if author %}
    - <a href="{{ author.url }}">{{ author.name }}</a>
  {% endif %}
</p>

{{ content }}
EOF

~~~

访问http://localhost:4000

## 10. Deployment

## Plugins

三个常用的官方插件

- [jekyll-sitemap](https://github.com/jekyll/jekyll-sitemap) - Creates a sitemap file to help search engines index content
- [jekyll-feed](https://github.com/jekyll/jekyll-feed) - Creates an RSS feed for your posts
- [jekyll-seo-tag](https://github.com/jekyll/jekyll-seo-tag) - Adds meta tags to help with SEO

Gemfile内容如下：

~~~
source 'https://rubygems.org'

gem 'jekyll'

group :jekyll_plugins do
  gem 'jekyll-sitemap'
  gem 'jekyll-feed'
  gem 'jekyll-seo-tag'
end
~~~

`_config.yml`添加如下内容

~~~
plugins:
  - jekyll-feed
  - jekyll-sitemap
  - jekyll-seo-tag
~~~

