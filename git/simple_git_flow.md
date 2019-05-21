本流程主要参考了[Simple Git workflow is simple](<https://www.atlassian.com/blog/archives/simple-git-workflow-simple>).  这个流程比较简单, 但对于公司内部的项目来说, 大多应该够用了. 

![img](image/bg2015122301-1558321591814.png)

## 原则

1. 只有一个长期分支master.  master分支总是production-like和deployable. 

2. 本地开发不能在master分支直接进行, 只能在feature或者bug-fix上进行. 

> 在同一时间, 一个feature/bug-fix建议由一个人完成. 


## 步骤
当有了新的feature或者需要做bug-fix时, 可以按照如下步骤来操作. 
1. 更新master分支.  

    ~~~
    git checkout master
    git fetch origin
    git merge origin/master
    ~~~

2. 创建feature/bug-fix, 或者checkout远程feature/bug-fix.  

    - 创建feature/bug-fix: 

        ~~~
        git checkout -b feature-name 
        ~~~

    - checkout远程feature/bug-fix.: 多人协作开发时, feature/bug-fix可能已经由其他成员创建了.

        ~~~
        git checkout -b feature-name origin/feature-name 
        ~~~

3. 在该分支上进行开发, 根据需要进行提交. 

    ~~~
    git commit 
    ~~~

    每次提交要有一定的完整性, 要有一定意义的,  保持合适的提交粒度. 

    - 避免过于琐碎的提交. 粒度不要太细
    - 避免积累大量修改内容后提交. 粒度不要太粗
   > 建议在开发时, 就控制好提交粒度. 也可以通过`git rebase -i`来调节已经提交的内容. 
   
   提交commit时，必须给出完整扼要的提交信息，下面是一个范本。
   
   > ```bash
   > Present-tense summary under 50 characters
   > 
   > * More information about commit (under 72 characters).
   > * More information about commit (under 72 characters).
   > 
   > http://project.management-system.com/ticket/123
   > ```
   
   第一行是不超过50个字的提要，然后空一行，罗列出改动原因、主要变动、以及需要注意的问题。最后，提供对应的网址(比如bug或issue网址). 
   
4. 全部功能完成和测试通过后, 更新远程库.  

    ~~~shell
    # 当前分支是 feature-name. 
    # 更新分支
    git fetch origin
    # 在多人协作feature开发时需要的. 如果是新创建的feature, 远程还没有这个feature, 所以请忽略下面这条命令.
    git rebase origin/feature-name    
    git rebase origin/master
     
    git push -u origin feature-name   
    ~~~
    
5. 合并到master分支.  到此feature的开发完成了.   本步骤可以由开发人员来做, 但建议指派专人来做, 这种情况下, 开发人员通过邮件或聊天工具提出合并的请求.  

    ~~~shell
    # 获取分支内容
    git fetch origin
    git checkout -b feature-name origin/feature-name  
    
    # 更新master
    git checkout master
    git merge origin/master
    
    # 合并分支feature name到master分支
    git merge --no-ff feature-name   
    git push origin master            
    ~~~

     当需要发布release时, 可以打上版本号. 

    ~~~shell
    git tag -a v1.1.0    
    git push origin v1.1.0
    ~~~

### 关于Pull Request

上面流程中并没有包含`pull request`, 这是由于公司项目中, 项目成员都有repository的write权限, 成员数量一般在2-5人之内,  成员之间有很好的面对面和在线沟通, 所以`pull request`并非绝对必要. 当然, 如果采用`pull request`的流程来替换第5步也可以的.  

### 和其他git开发流程的比较

目前, 比较主流的git开发流程有:

- git flow:  有些复杂, 要求开发人员, 对于各个分支的作用都非常清楚.   多分支之前的merge比较多, 要求大家严格遵循规范来进行. 
  - 默认工作分支是 develop，但是大部分版本管理工具默认分支都是 master，开始的时候总是需要切换很麻烦。
  - Hotfix 和 Release 分支在需要版本快速迭代的项目中，几乎用不到，因为刚开发完就直接合并到 master 发版，出现问题 develop 就直接修复发布下个版本了。
  - Hotfix 和 Release 分支，一个从 master 创建，一个从 develop 创建，使用完毕，需要合并回 develop 和 master。而且在实际项目管理中，很多开发者会忘记合并回 develop 或者 master。
- github flow:  最大的优势是简单. 本流程基本和github flow相同, 区别是, 在merge过程中, 不强制使用`pull requst`.  
- gitlab flow: 兼顾了以上两个流程的特点, 应该说是适合大多数项目单的. 

个人认为,  git flow有些过时了. 大多数项目可以从github flow(当然包括本流程)开始,  但如果有以下的情况,  gitlab flow更好.  

- 版本的延迟发布（例如 iOS 应用审核到通过中间，可能也要在 master 上推送代码）

- 不同环境的部署 （例如：测试环境，预发环境，正式环境）

- 不同版本发布与修复 （是的，只有一个 master 分支真的不够用）

  在很多系统中, 需要维护多个版本, 每个版本都有用户使用. 

## 总结

大多数项目可以从github flow(当然包括本流程)开始.  在实际项目中, 我们可以根据项目的特点, 选择适合的流程, 也可以对这些标准流程做一些适当裁剪.  

## 参考

- [Understanding the GitHub flow](<https://guides.github.com/introduction/flow/index.html>)
- [Simple Git workflow is simple](<https://www.atlassian.com/blog/archives/simple-git-workflow-simple>)
-  [Git-rebase 黑魔法之打磨 commit 颗粒度](https://drprincess.github.io/2018/02/27/Git-rebase打造喜欢的commit颗粒感/#more)
-  [Git 使用规范流程](<http://www.ruanyifeng.com/blog/2015/08/git-use-process.html>)
-  [Git 工作流程](<http://www.ruanyifeng.com/blog/2015/12/git-workflow.html>) : 阮一峰出品, 比较了Git Flow, Github Flow和GitLab Flow. 
- [Git三大特色之WorkFlow(工作流)](<https://drprincess.github.io/2017/12/26/Git%E4%B8%89%E5%A4%A7%E7%89%B9%E8%89%B2%E4%B9%8BWorkFlow(%E5%B7%A5%E4%BD%9C%E6%B5%81)/>)
- [Understanding the GitHub flow](<https://guides.github.com/introduction/flow/index.html>)
- [Git工作流指南：Pull Request工作流](<http://blog.jobbole.com/76854/>)