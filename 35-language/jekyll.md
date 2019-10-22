Jekyll 是一个简单的博客形态的静态站点生产机器。它有一个模版目录，其中包含原始文本格式的文档，通过一个转换器（如 [Markdown](http://daringfireball.net/projects/markdown/)）和我们的 [Liquid](https://github.com/Shopify/liquid/wiki) 渲染器转化成一个完整的可发布的静态网站，你可以发布在任何你喜爱的服务器上。Jekyll 也可以运行在 [GitHub Page](http://pages.github.com/) 上，也就是说，你可以使用 GitHub 的服务来搭建你的项目页面、博客或者网站，而且是**完全免费**的。

# 1. 入门

## 1.1 安装

### 1.11 Jekyll

#### [手动安装](https://www.jekyll.com.cn/docs/)

1. 安装一个完整的 [Ruby 开发环境](ruby.md) 

2. 安装 Jekyll 和[bundler](https://www.jekyll.com.cn/docs/ruby-101/#bundler) [gems](https://www.jekyll.com.cn/docs/ruby-101/#gems)

   ```
   gem install jekyll bundler  --http-proxy $http_proxy
   ```

3. 在./myblog目录下创建一个全新的 Jekyll 网站

   ```
   jekyll new myblog
   ```

4. 进入新创建的目录

   ```
   cd myblog
   if [ ! -f _config.yml.template ]; then
     cp _config.yml _config.yml.template
   fi
   
   cp _config.yml.template _config.yml
   cat << EOF >> _config.yml
   host: 0.0.0.0 
   port: 4000 
   defaults:
     - 
       scope:
         path: ""
         type: "posts"
       values:
           layout: "post"
           title: "Default Title"
           
   EOF
   ```

5. 构建网站并启动一个本地 web服务

   ```
   bundle exec jekyll serve
   ```

6. 在浏览器中打开 [http://localhost:4000](http://localhost:4000/) 网址

#### [Docker安装](https://github.com/envygeeks/jekyll-docker/blob/master/README.md)

~~~
mkdir -p docker-myblog
mkdir -p docker-myblog/vendor/bundle
cd docker-myblog
echo host: 0.0.0.0 > _config.yml
echo port: 4000    >> _config.yml

docker run  \
  --volume="$PWD:/srv/jekyll" \
  --volume="$PWD/vendor/bundle:/usr/local/bundle" \
  -it jekyll/jekyll:latest \
  jekyll build
  
docker run -d \
  --volume="$PWD:/srv/jekyll" \
  --volume="$PWD/vendor/bundle:/usr/local/bundle" \
  -it jekyll/jekyll:latest \
  jekyll build  
~~~

## [Tutorial](https://jekyllrb.com/tutorials/home/)



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







