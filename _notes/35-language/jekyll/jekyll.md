Jekyll 是一个简单的博客形态的静态站点生产机器。它有一个模版目录，其中包含原始文本格式的文档，通过一个转换器（如 [Markdown](http://daringfireball.net/projects/markdown/)）和我们的 [Liquid](https://github.com/Shopify/liquid/wiki) 渲染器转化成一个完整的可发布的静态网站，你可以发布在任何你喜爱的服务器上。Jekyll 也可以运行在 [GitHub Page](http://pages.github.com/) 上，也就是说，你可以使用 GitHub 的服务来搭建你的项目页面、博客或者网站，而且是**完全免费**的。

## 技巧

### 1.1 `bundle update`， `bundle install`区别

- bundle update

  会去相应的源检查Gemfile里gem的更新，然后对比Gemfile.lock文件，如果Gemfile里没有指定版本或是指定是>=的版本，就会去相应的源下载并安装新版本的gem，然后更新Gemfile.lock文件。

- bundle install

  会先检查Gemfile.lock文件以及里边的相关依赖，然后为本地系统安装Gemfile.lock文件中指定的版本，接着去检查Gemfile中有而Gemfile.lock中没有的，然后安装。bundle install好像不会去检查相关源中Gem版本的更新。

## 例子

- [入门](example/myblog/README.md) 
-  [Docker](example/docker-myblog/README.md) 

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

## Jekyii的目录结构

https://jekyllcn.com/docs/structure/

一个基本的 Jekyll 网站的目录结构一般是像这样的：

```
.
├── _config.yml
├── _drafts
|   ├── begin-with-the-crazy-ideas.textile
|   └── on-simplicity-in-technology.markdown
├── _includes
|   ├── footer.html
|   └── header.html
├── _layouts
|   ├── default.html
|   └── post.html
├── _posts
|   ├── 2007-10-29-why-every-programmer-should-play-nethack.textile
|   └── 2009-04-26-barcamp-boston-4-roundup.textile
├── _site
├── .jekyll-metadata
└── index.html
```

来看看这些都有什么用：

| 文件 / 目录                                          | 描述                                                         |
| ---------------------------------------------------- | ------------------------------------------------------------ |
| `_config.yml`                                        | 保存[配置](https://jekyllcn.com/docs/configuration/)数据。很多配置选项都可以直接在命令行中进行设置，但是如果你把那些配置写在这儿，你就不用非要去记住那些命令了。 |
| `_drafts`                                            | drafts（草稿）是未发布的文章。这些文件的格式中都没有 `title.MARKUP` 数据。学习如何 [使用草稿](https://jekyllcn.com/docs/drafts/). |
| `_includes`                                          | 你可以加载这些包含部分到你的布局或者文章中以方便重用。可以用这个标签 `{% include file.ext %}` 来把文件 `_includes/file.ext` 包含进来。 |
| `_layouts`                                           | layouts（布局）是包裹在文章外部的模板。布局可以在 [YAML 头信息](https://jekyllcn.com/docs/frontmatter/)中根据不同文章进行选择。 这将在下一个部分进行介绍。标签 `{{ content }}` 可以将content插入页面中。 |
| `_posts`                                             | 这里放的就是你的文章了。文件格式很重要，必须要符合: `YEAR-MONTH-DAY-title.MARKUP`。 [永久链接](https://jekyllcn.com/docs/permalinks/) 可以在文章中自己定制，但是数据和标记语言都是根据文件名来确定的。 |
| `_data`                                              | 格式化好的网站数据应放在这里。jekyll 的引擎会自动加载在该目录下所有的 yaml 文件（后缀是 `.yml`, `.yaml`, `.json` 或者 `.csv` ）。这些文件可以经由 ｀site.data｀ 访问。如果有一个 `members.yml` 文件在该目录下，你就可以通过 `site.data.members` 获取该文件的内容。 |
| `_site`                                              | 一旦 Jekyll 完成转换，就会将生成的页面放在这里（默认）。最好将这个目录放进你的 `.gitignore` 文件中。 |
| `.jekyll-metadata`                                   | 该文件帮助 Jekyll 跟踪哪些文件从上次建立站点开始到现在没有被修改，哪些文件需要在下一次站点建立时重新生成。该文件不会被包含在生成的站点中。将它加入到你的 `.gitignore` 文件可能是一个好注意。 |
| `index.html` and other HTML, Markdown, Textile files | 如果这些文件中包含 [YAML 头信息](https://jekyllcn.com/docs/frontmatter/) 部分，Jekyll 就会自动将它们进行转换。当然，其他的如 `.html`, `.markdown`, `.md`, 或者 `.textile` 等在你的站点根目录下或者不是以上提到的目录中的文件也会被转换。 |
| Other Files/Folders                                  | 其他一些未被提及的目录和文件如 `css` 还有 `images` 文件夹， `favicon.ico` 等文件都将被完全拷贝到生成的 site 中。这里有一些[使用 Jekyll 的站点](https://jekyllcn.com/docs/sites/)，如果你感兴趣就来看看吧。 |