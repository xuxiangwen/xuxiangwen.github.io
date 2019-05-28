###  1. 常见命令

#### [What's the difference between HEAD^ and HEAD~ in Git?](https://stackoverflow.com/questions/2221658/whats-the-difference-between-head-and-head-in-git)

在版本树中, 对于某一个节点, 我们可以用^或者~定位其上游的节点. 逻辑如下图所示

```
G   H   I   J
 \ /     \ /
  D   E   F
   \  |  / \
    \ | /   |
     \|/    |
      B     C
       \   /
        \ /
         A
         
A =      = A^0
B = A^   = A^1     = A~1
C = A^2  = A^2
D = A^^  = A^1^1   = A~2
E = B^2  = A^^2
F = B^3  = A^^3
G = A^^^ = A^1^1^1 = A~3
H = D^2  = B^^2    = A^^^2  = A~2^2
I = F^   = B^3^    = A^^3^
J = F^2  = B^3^2   = A^^3^2
```

#### [删除敏感数据](https://help.github.com/en/articles/removing-sensitive-data-from-a-repository)

有的时候不小心把一些敏感信息发不到了GitHub上, 即使把这些信息除去，在文件的历史版本，还是可以看到。这种情况下，我们有两个方法。

##### [Using the BFG](<https://rtyley.github.io/bfg-repo-cleaner/>)

下载BFG包到本地. 

~~~
wget https://repo1.maven.org/maven2/com/madgag/bfg/1.13.0/bfg-1.13.0.jar -O bfg.jar
~~~

开始清理. 

~~~
url=git@github.com:xuxiangwen/aws-dms-wisdom.git
delete_files=dms.conf

# clone to local
git clone --mirror $url

# 清除一些文件. 默认情况下, BFG不会修改`master` (or '`HEAD`') branch的最后提交的内容, 而只会清除之前的提交. 
java -jar bfg.jar --strip-blobs-bigger-than 20M $(basename $url)   #删除超过20M的文件
java -jar bfg.jar --delete-files id_{dsa,rsa} $(basename $url)     #删除私钥
java -jar bfg.jar --delete-files ${delete_files:-un_exist_file}  $(basename $url)   #删除指定文件

# 把passwords.txt中所有的文本(支持正则表达式),替换为***REMOVED***.
cat << EOF > passwords.txt
XXXXXX
EOF

java -jar bfg.jar --replace-text passwords.txt --no-blob-protection $(basename $url)

# 
cd $(basename $url)
git reflog expire --expire=now --all && git gc --prune=now --aggressive     
git push   

# 
~~~

##### [Using filter-branch](https://help.github.com/en/articles/removing-sensitive-data-from-a-repository#using-filter-branch)

略, 总体复杂的多. 默认就用BFG啦. 

##### 如何避免类似的泄密事件发生

- 使用可视化工具来提交, 这样可以更加容易看到哪些文件被添加, 修改和删除了.
- 避免`git add .` and `git commit -a`
- 使用`git add --interactive` 来review每个文件的 stage changes.
- 使用 `git diff --cached` 来review  the changes that you have staged for commit

#### 处理push大文件（超过100m）的文件

~~~shell
git rm --cached giant_file   # Stage our giant file for removal, but leave it on disk
git commit --amend -CHEAD   # Amend the previous commit with your change   
# Simply making a new commit won't work, as you need# to remove the file from the unpushed history as well
git push   # Push our rewritten, smaller commit
~~~
#### 设置用户和邮箱

~~~shell
#global configuration
git config --global user.name "eipi10"
git config --global user.email "eipi10@qq.com"
~~~

#### 查看设定

~~~shell
git config --list          #列出所有 Git当时能找到的配置
git config user.name
git config http.proxy
~~~

#### 设置代理

~~~shell
git config --global  http.proxy proxy-server:port
~~~

#### 移除文件

```shell
git rm PROJECTS.md            # 删除工作区和暂存区文件
git rm --cached PROJECTS.md   # 删除暂存区文件。对文件不再trace
```

#### 显示所有分支

~~~
git branch -a    #包括本地和远程.
git branch -vv   #显示本地分支和远程分支的关系
~~~

#### 查看已暂存和未暂存的修改

```shell
git diff            # 比较工作区和暂存区
git diff --staged   # 比较暂存区和git仓库
git diff --cached   # 同上
```

#### 回退修改

~~~
git reset –soft     # 暂存区->工作区
git reset –mixed    # 版本库->暂存区
git reset –hard     # 版本库->暂存区->工作区
~~~

#### 查看远程仓库

~~~shell
git status -s    # 一种更为紧凑的格式输出 
~~~

#### 查看已暂存和未暂存的修改

~~~shell
git diff            # 比较工作区和暂存区
git diff --staged   # 比较暂存区和git仓库. 也可以用git diff --cached 
git diff head       # 比较工作区和版本库(当前)
~~~

#### 查看日志

~~~shell
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
git lg -p 5         # 显示最近5次的提交结果
git log --oneline --decorate --graph --all -p 5    # 上面的命令，内容和颜色都很丰富，下面的更简明
~~~

#### [Git怎样撤销一次分支的合并Merge](https://segmentfault.com/q/1010000000140446)

```shell
git checkout 【merge操作时所在的分支】
git reset --hard 【merge前的版本号】
```



### 2. Git 原理

#### 三大区域

![工作目录、暂存区域以及 Git 仓库。](https://progit.bootcss.com/images/areas.png)

![Git三大区域](image/2429e4d2661e60027537aea0077f6e40.png)

#### 提交对象

每次提交都会生成提交对象。见下图黄色部分。它包括：

- 树对象：指向暂存内容快照的指针。即下图绿色的部分。
- 作者的姓名和邮箱
- 提交时输入的信息
- 指向它的父对象的指针

![提交对象及其父对象。](https://progit.bootcss.com/images/commits-and-parents.png)

#### Git 的分支（branch）

其实本质上仅仅是指向提交对象的可变指针。

![两个指向相同提交历史的分支。](https://progit.bootcss.com/images/two-branches.png)

####  HEAD 

是个指向当前所在的分支的特殊指针。当提交的时候，当前分支会移动，指向最新提交的对象，而HEAD总是指向当前分支。

**开始**

![HEAD 指向当前所在的分支。](https://progit.bootcss.com/images/head-to-testing.png)

​           **提交后**

   ![HEAD 分支随着提交操作自动向前移动。](https://progit.bootcss.com/images/advance-testing.png)

#### 提交信息





### 3. Git GUI

#### GitKrken

尝试了不少软件。感觉GitKrken界面效果很棒，但是linux下proxy无法设置成功，网上也没有找到可以解决的方法。

##### Linux

~~~
# 安装 https://support.gitkraken.com/how-to-install/
wget https://release.gitkraken.com/linux/gitkraken-amd64.rpm
sudo yum install ./gitkraken-amd64.rpm

## 启动
gitkraken --proxy-server=10.200.0.1:8080
~~~

在GitKrken中如果pull，push失败，可能需要[设置代理](#设置代理)。**前看起来还是不行。放弃这个工具了。**

#### GitHub Desktop

##### Linux

官方版本目前不支持linux，但是网上有linux的发布版本：<https://github.com/shiftkey/desktop>。惊喜。

~~~shell
wget https://github.com/shiftkey/desktop/releases/download/release-1.6.6-linux2/GitHubDesktop-linux-1.6.6-linux2.rpm
sudo yum install GitHubDesktop-linux-1.6.6-linux2.rpm
~~~



### Git Flow

Git 作为一个源码管理系统，不可避免涉及到多人协作。

协作必须有一个规范的工作流程，让大家有效地合作，使得项目井井有条地发展下去。"工作流程"在英语里，叫做"workflow"或者"flow"，原意是水流，比喻项目像水流那样，顺畅、自然地向前流动，不会发生冲击、对撞、甚至漩涡。

![img](image/bg2015122301.png)

主要有三种广泛使用的工作流程：

> - Git flow
> - Github flow
> - Gitlab flow



上文摘自[阮一峰](http://www.ruanyifeng.com/)的 [Git 工作流程](http://www.ruanyifeng.com/blog/2015/12/git-workflow.html)。

