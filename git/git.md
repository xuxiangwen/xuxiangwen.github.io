

###  1. 常见命令

#### 移除文件

```shell
git rm PROJECTS.md            # 删除工作区和暂存区文件
git rm --cached PROJECTS.md   # 删除暂存区文件。对文件不再trace
```

#### 查看已暂存和未暂存的修改

```shell
git diff            # 比较工作区和暂存区
git diff --staged   # 比较暂存区和git仓库
git diff --cached   # 同上
```

#### 查看远程仓库

~~~shell
git status -s    # 一种更为紧凑的格式输出 
~~~

#### 查看已暂存和未暂存的修改

~~~shell
git diff            # 比较工作区和暂存区
git diff --staged   # 比较暂存区和git仓库
git diff --cached   # 同上
~~~

#### 查看日志

~~~shell
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
git lg -p 5         # 显示最近5次的提交结果
git log --oneline --decorate --graph --all -p 5    # 上面的命令，内容和颜色都很丰富，下面的更简明
~~~



### 2. Git 原理

### 提交对象

每次提交都会生成提交对象。见下图黄色部分。它包括：

- 树对象：指向暂存内容快照的指针。即下图绿色的部分。
- 作者的姓名和邮箱
- 提交时输入的信息
- 指向它的父对象的指针

![提交对象及其父对象。](https://progit.bootcss.com/images/commits-and-parents.png)

### Git 的分支（branch）

其实本质上仅仅是指向提交对象的可变指针。

![两个指向相同提交历史的分支。](https://progit.bootcss.com/images/two-branches.png)

####  HEAD 

是个指向当前所在的分支的特殊指针。当提交的时候，当前分支会移动，指向最新提交的对象，而HEAD总是指向当前分支。

**开始**

![HEAD 指向当前所在的分支。](https://progit.bootcss.com/images/head-to-testing.png)

​           **提交后**

   ![HEAD 分支随着提交操作自动向前移动。](https://progit.bootcss.com/images/advance-testing.png)

#### 提交信息
