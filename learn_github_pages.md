## What is GitHub Pages?

GitHub Pages is a static site hosting service designed to host your personal, organization, or project pages directly from a GitHub repository. 

[![What is GitHub Pages?](http://img.youtube.com/vi/2MsN8gpT6jY/0.jpg)](http://www.youtube.com/watch?v=2MsN8gpT6jY "What is GitHub Pages?")

## GitHub Pages Site类型

- user and organization pages： 个人或组织的门户网站。一个用户或组织只能有一个。
  - repository名称： username.github.io 或 orgname.github.io
  - site url同上
  - 来源
    - `master` branch
- project pages：项目的门户网站，描述项目的内容。一个用户或组织可以有多个。
  - 其他repository
  - site url：username.github.io/projectname 或 orgname.github.io/projectname
  - 来源
    - `master` branch
    - master` branch的/docs目录
    - `gh-pages` branch

## GitHub Pages and Jekyll

[Jekyll](https://github.com/jekyll/jekyll) is a simple, blog-aware, static site generator perfect for personal, project, or organization sites. GitHub Pages和Jekyll深度整合。使用Jekyll的好处是：

- 简化的网站构建过程
- use [Markdown](https://help.github.com/en/articles/markdown-basics) instead of HTML
- 丰富的theme
  - [add a Jekyll theme](https://help.github.com/en/articles/adding-a-jekyll-theme-to-your-github-pages-site) to your site without copying CSS files
  - quickly create a new site using the [Jekyll Theme Chooser](https://help.github.com/en/articles/adding-a-jekyll-theme-to-your-github-pages-site-with-the-jekyll-theme-chooser)
  - use common templates, such as headers and footers, that are shared across files.

### [Jekyll's build process](https://help.github.com/en/articles/about-github-pages-and-jekyll#jekylls-build-process)

- push文件到GitHub
- GitHubPages发布站点

### [Jekyll site examples](https://help.github.com/en/articles/about-github-pages-and-jekyll#jekyll-site-examples)

- [Projects using GitHub Pages](https://github.com/showcases/github-pages-examples)
- [Open source organizations using GitHub Pages](https://github.com/showcases/open-source-organizations)

### Jekyll themes on GitHub

- use  [Jekyll Theme Chooser](https://help.github.com/en/articles/adding-a-jekyll-theme-to-your-github-pages-site-with-the-jekyll-theme-chooser)

- manually editing your site's *_config.yml* file 

  - github officially [supported themes](https://pages.github.com/themes/)
  -  [open source Jekyll theme hosted on GitHub](https://github.com/topics/jekyll-theme)

  

## Reference

- [GitHub Pages](https://pages.github.com)
- [Creating and Hosting a Personal Site on GitHub](http://jmcglone.com/guides/github-pages): 非常好的入门guide
- [hexo](https://hexo.io/zh-cn)：一个快速、简洁且高效博客框架
- [github desktop](https://desktop.github.com)：GitHub客户端工具。支持windows, mac。
- [阿里云](https://home.console.aliyun.com/)：域名购买
- [How to embed youtube video to markdown file, GitHub or GitLab comments](http://sviridovserg.com/2017/05/22/embed-youtube-to-markdown/#)： 把youtube视频放到markdown中
- [YouTube->Markdown](http://embedyoutube.org)：同上