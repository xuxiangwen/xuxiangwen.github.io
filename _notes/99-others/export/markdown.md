
# 前言

作为一个技术宅，很喜欢来学习一些自己感兴趣的技术，在学习的过程中，深感记笔记非常的重要。笔记记得好，即使过上几年，再次翻看，还能记忆犹新。对于成年人，记忆力比起年轻时候都会有不同程度衰减，由此记笔记尤甚重要。下面介绍一下这方面的心得。

# 笔记

## 笔记种类

从程序员的眼中，根据内容，笔记可以分为：

- 信息。需要记录的内容。比如：服务器地址，账号/密码，知识点等。
- 代码。好的代码易于阅读。代码中，本身也要求添加的足够的描述。有种说法，代码是最好的文档。
- 文档。项目需求，设计，开发，测试文档等。包含了项目的业务知识和实现逻辑。文档主要用于公司或团队内部进行知识交流的。
- 交互文档。混合了代码，报表（可视化）和文档。一般是类似jupyter notebook这种格式，它的特点是交互，体现了在开发过程中，逐步思考的过程。常用于技术学习和数据分析报告。
- 文章。经过自己整理，总结，或者创作出的内容。一般常用wiki，blog等发布。

对于一篇笔记，可以属于多个类别，比如：项目中的文档，可以通过blog单独发布出来，作为一篇文章分享给更多人。

## 什么是好笔记

- 好理解： 好的笔记是容易理解的，对于要分享的笔记，尤其如此。
- 易于复现： 常说，好的代码容易被测试，对于好的笔记，里面的内容也应该是容易被重现的，尤其是对于交互文档和文章中的内容。所以记笔记中，要记录环境如何安装，数据如何准备，程序如何运行，结果如何验证等。
- 持续更新：笔记应该是能被方便的持续的更新的。

## 笔记的安全性

既然要分享，笔记的安全性非常重要。不同的笔记也有不同的发布范围。

- Internet：

  - 公开。没有安全性限制，可以发布到internet上，让所有人访问。一般包括一些wiki，blog，开源代码等。
  - 私有。信息是私有的，但可以授权任意的人员来访问。个人的一些文章，代码，但并不想公开的，而且不含有公司的敏感信息。

- 公司：仅在公司内部网络才可以访问。

  - 公司/部门：信息在公司或部门内部是公开的。比如：公司流程，部门policy等。

  - 项目：信息在项目组内部是公开的，可以授权项目外的同事来访问。比如：项目开发设计文档，源代码等。

  - 私有：信息是私有的，但可以授权公司的同事来访问。比如：个人的一些资料，文档，代码等。

    

# 工具

首先从工具开始说起。任何工具的使用，也是由需求触发的。

## 历史

就个人而言，使用的工具经历了以下的过程。

### 原始社会：文本文件，word，excel文件

![img](images/ximg_5b6e4770e6897.jpg.pagespeed.gp+jp+jw+pj+ws+js+rj+rp+rw+ri+cp+md.ic.tfq1D0waRx.jpg)

最开始大家都是使用这些来记录个人工作生活信息的。最大的问题是，文件分散在计算机的各处，时间长了，放在哪里都忘了，更别提更新了。

### 工业时代：evernote， onenote， 网易云笔记

![img](images/CNHome_Image1_v2.png)

记不得从何时开始，用上了evernote，身边的很多同事也在用onenote。用上这些工具，笔记集中管理，可以多级导航，搜索起来也很方便，应该说效率大大提高 。后来又开始使用网易云笔记，和evernote比起来，它可以编写markdown，笔记分级方便方便，但全文检索能力又不如evernote。

### 信息时代：zeppelin，jupyter notebook + 思维导图

![example notebook of Lorenz differential equations](images/jupyterpreview.png)

[my example](http://15.15.165.218:18888/notebooks/eipi10/xuxiangwen.github.io/base/model_evaluation.ipynb)

![1557381669838](images/1557381669838.png)

evernote，onenote等工具很强大，但无法执行程序代码。在学习Spark的时候，第一次接触了zeppelin，它是Web笔记形式的交互式数据查询分析工具，可以用scala和sql等语言展示数据，也可以用markdown来编写文档。这种代码，报表（可视化）和文档混合的方式，真的感觉耳目一新。jupyter notebook也是如此，支持python, r, julia, and scala等40多种语言。

思维导图，则另辟蹊径，它是表达发散性思维的有效图形思维工具，它运用图文并重的技巧，把各级主题的关系用相互隶属与相关的层级图表现出来，把主题关键词与图像、颜色等建立记忆链接。

### 互联时代：  github(pages, wiki) + typora(markdown) + jupyter notebook + pandoc ...

**[GitHub Pages](<https://pages.github.com/>)** is a static site hosting service designed to host your personal, organization, or project pages directly from a GitHub repository. 

[![What is GitHub Pages?](http://img.youtube.com/vi/2MsN8gpT6jY/0.jpg)](http://www.youtube.com/watch?v=2MsN8gpT6jY "What is GitHub Pages?")

GitHub Pages  Example

- [Projects using GitHub Pages](https://github.com/showcases/github-pages-examples)

- [Open source organizations using GitHub Pages](https://github.com/showcases/open-source-organizations)

  

**[Typora](<https://typora.io/>)** will give you a seamless experience as both a reader and a writer. 

- markdown
- image enhanced

![1557385341070](images/1557385341070.png)

 [example eigenvector-singular.md](..\math\eigenvector-singular.md) 

**Markdown vs. Word**

- 内容与形式分离 vs 所见即所得（内容与形式融合）

  - 专注内容书写：Markdown 胜
  - 调整排版：Markdown 胜
  - 文档发布和阅读：Markdown 胜

- 源码输入 vs 所见即所得

  - 严谨性：Markdown 胜

  - 功能：Word 胜

    - 图片支持： Word 略胜
    - 表格支持： Word 胜

  - 显示和上手难度： Word 胜

  - 书写流畅性： Markdown 胜

    

**Pandoc**是一个标记语言转换工具，可实现不同标记语言间的格式转换，堪称该领域中的“瑞士军刀”。

由于工具的强大，记笔记的效率很高，这使得我们记录了太多的笔记，这反而造成了信息的泛滥，如何保证信息的价值呢？而且，学习时记笔记，开发写文档，项目管理，team活动也有产生很多文档，这些内容如何能用统一的方式来维护呢？

这些问题的答案或许是——分享。多记笔记是第一步，接下来还需要高质量的笔记，这些笔记是真正（自己）的知识，这些知识非常适合来分享。当我们需要分享知识的时候，一般都会花上一些心思，这使得知识更加有价值，易于理解。开发文档和项目文档又何尝不是如此，传统的方式，文档很少有持续维护，内容枯燥，大家也不愿意看。采用wiki或者blog等方式，生产高质量，易于理解的内容。在分享过程中，知识贡献者和知识使用者都能各取所需，这也是开源的精神所在。

采用typora可以在本地非常方便的编写markdown文档，然后用github可以很容易分享给其他人。 在公司内部，其实我们一直有信息交流，分享的平台，但问题是，功能和性能很难得到非常有效的保证。有的时候，性能很慢，打开一个文档需要10秒；有的时候同步很慢；有的时候编辑麻烦，格式不支持，很无奈。总而言之，这是一种基于中心化管理的方式，位于中心的服务承载了太多的职责，而每一项往往都很难做的很好。而github不同，它代表的是一种分布式的管理方式，所有的编辑都可以在本地来做，我们可以用自己喜欢的工具，速度飞快，畅快随心。github只是你本地库的一种同步，这种同步先天支持很好的分享和协同。

以上这些工具，我们都会混合使用，没有一种工具可以解决所有的问题。

## 工具的要求

下面对工具的要求，并不是对单一工具的，而是对于我们所用的工具的总和来说的。

- 简单易用。

  不能太复杂了。

- 支持多种格式

   简单信息，文档，表格，代码，图表都能支持。

- 编辑方便

  编辑越方便越好。jupyter notebook是一种web笔记形式，可以运行代码，很方便浏览，但在记笔记的时，如果要添加大量图片，将会非常辛苦。以前年，公司的SharePoint等工具，打开文档很慢，编辑不方便。目前看OneNote的同步好像还是不是很快。

- 快速检索

  高效，快速的搜索功能必不可少。之前也提到， 网易云笔记在搜索的时候，不是很好用 ，它的搜索默认路径是当前目录，而不是全局，这个逻辑真的有些奇怪，实际中，所以经常不得不在搜索前去选择根目录。

- 易于分享

  很容易分享到各个层次，有些知识可以分享到项目，有些可以到部门，有些可以到 公司，有些可以到互联网。

以上这些工具，我们都会混合使用，没有一种工具可以解决所有的问题。

## github + typora vs. teams + onenote ...

|              | teams + onenote ... | github + typora ... | description                                                  |
| ------------ | :------------------ | ------------------- | ------------------------------------------------------------ |
| 简单易用     | 5                   | 3                   | 后者复杂的多。                                               |
| 支持多种格式 | 4                   | 4                   | 前者对代码的支持不够好。后面的扩展性非常好。                 |
| 编辑方便     | 5                   | 4                   | 前者功能强大方便，但后者善于精细化的控制。                   |
| 快速检索     | 4                   | 5                   | 因为是纯文本和开放性，理论上可以实现超强的搜索功能           |
| 易于分享     | 4                   | 5                   | 前者适合公司内部分享，后者都适合，而且同一个文档可以发不到多个平台 |

个人观点，总体上两套工具集合都。前者最大的特点是简单易用，后者最大特点在于开放自由。对于程序员来说，后面的方案更有诱惑性。

## 参考

- [学习编程用什么做笔记比较好？](https://www.zhihu.com/question/21438053)
- [反思Markdown：Markdown的长与短](https://sspai.com/post/37340)
- [关于 Markdown 的一些奇技淫巧](https://mazhuang.org/2017/09/01/markdown-odd-skills)
- [Typora - 不要太棒的Markdown编辑器](https://zhuanlan.zhihu.com/p/44998516)
- [Cmd Markdown 编辑阅读器](https://www.zybuluo.com/mdeditor) : 在线Markdown编辑器。首页有markdown的语法展示，非常好！
- [Producing slide shows with pandoc](https://pandoc.org/MANUAL.html#producing-slide-shows-with-pandoc)

