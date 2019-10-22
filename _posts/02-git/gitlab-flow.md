虽然很早开始使用Git, 但对于Git Flow却不是很了解, 之前听同事讲过一次, 觉得很不错. 自己项目中实行时, 对Git的整个机制发生兴趣, 在花了一些时间学习之后, 真的深深被大神[Linus Torvalds](<https://en.wikipedia.org/wiki/Linus_Torvalds>)对Git简洁而强大的设计所折服. 再次回去看Git Flow, 发现除了这个流程外, Git还有其他的工作流程, 比如Git Flow, GitLab Flow.

在经过比较之后, 发现Git Flow似乎有些繁琐了, 感觉GitLab Flow更加适合我们的项目. GitLab flow](http://doc.gitlab.com/ee/workflow/gitlab_flow.html) 是 Git flow 与 Github flow 的综合。它吸取了两者的优点，既有适应不同开发环境的弹性，又有单一主分支的简单和便利。

在介绍GitLab Flow之前. 首先我们来看看其他流程的一些问题.

## 1. Git Flow和Github Flow的问题

当 Git Flow 出现后，它解决了之前项目管理的很让人头疼的分支管理，但是实际使用过程中，也暴露了很多问题：

- 默认工作分支是 develop，但是大部分版本管理工具默认分支都是 master，开始的时候总是需要切换很麻烦。
- Hotfix 和 Release 分支在需要版本快速迭代的项目中，几乎用不到，因为刚开发完就直接合并到 master 发版，出现问题 develop 就直接修复发布下个版本了。
- Hotfix 和 Release 分支，一个从 master 创建，一个从 develop 创建，使用完毕，需要合并回 develop 和 master。而且在实际项目管理中，很多开发者会忘记合并回 develop 或者 master。对开发人员的要求明显更高. 

GitHub Flow 的出现，非常大程度上简化了 Git Flow ，因为只有一个长期分支 master，并且提供 GUI 操作工具，一定程度上避免了上述的几个问题，然而在一些实际问题面前，仅仅使用 master 分支显然有点力不从心，例如：

- 版本的延迟发布（例如 iOS 应用审核到通过中间，可能也要在 master 上推送代码）
- 不同环境的部署 （例如：测试环境，预发环境，正式环境）
- 不同版本发布与修复 （是的，只有一个 master 分支真的不够用）

## 2. GitLab Flow原则: 上游优先

GitLab flow 的最大原则叫做"上游优先"（upsteam first），即只存在一个主分支`master`，它是所有其他分支的"上游"。只有上游分支采纳的代码变化，才能应用到其他分支。

### 2.2 开发流程

Gitlab flow 分成两种情况，适应不同的开发流程。

- ### 持续发布

- ### 版本发布



### 持续发布

![img](image/bg2015122306.png)

对于"持续发布"的项目，它建议在`master`分支以外，再建立不同的环境分支。比如，"开发环境"的分支是`master`，"预发环境"的分支是`pre-production`，"生产环境"的分支是`production`。

开发分支是预发分支的"上游"，预发分支又是生产分支的"上游"。代码的变化，必须由"上游"向"下游"发展。比如，生产环境出现了bug，这时就要新建一个功能分支，先把它合并到`master`，确认没有问题，再`cherry-pick`到`pre-production`，这一步也没有问题，才进入`production`。



### 版本发布

![img](image/bg2015122307.png)

对于"版本发布"的项目，建议的做法是每一个稳定版本，都要从`master`分支拉出一个分支，比如`2-3-stable`、`2-4-stable`等等。

以后，只有修补bug，才允许将代码合并到这些分支，并且此时要更新小版本号。



## 参考

- [Git 工作流程](<http://www.ruanyifeng.com/blog/2015/12/git-workflow.html>) : 阮一峰出品, 比较了Git Flow, Github Flow和GitLab Flow. 
- [Git三大特色之WorkFlow(工作流)](<https://drprincess.github.io/2017/12/26/Git%E4%B8%89%E5%A4%A7%E7%89%B9%E8%89%B2%E4%B9%8BWorkFlow(%E5%B7%A5%E4%BD%9C%E6%B5%81)/>)
- [Understanding the GitHub flow](<https://guides.github.com/introduction/flow/index.html>)
- [A successful Git branching model](http://nvie.com/posts/a-successful-git-branching-model/) :  介绍了Git Flow.
- [Simple Git workflow is simple](<https://www.atlassian.com/blog/archives/simple-git-workflow-simple>)
- [Introduction to GitLab Flow](<https://docs.gitlab.com/ee/workflow/gitlab_flow.html>)
- [git cherry-pick 使用指南](<https://www.jianshu.com/p/08c3f1804b36>)
- [Git工作流指南：Pull Request工作流](<http://blog.jobbole.com/76854/>)