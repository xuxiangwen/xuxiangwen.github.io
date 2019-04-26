## Git 基础

### 获取 Git 仓库

#### 在现有目录中初始化仓库

```console
git init
git add *.c
git add LICENSE
git commit -m 'initial project version'
```

#### 克隆现有的仓库

```console
git clone https://github.com/libgit2/libgit2
git clone https://github.com/libgit2/libgit2 mylibgit
```

### 记录每次更新到仓库

![Git 下文件生命周期图。](https://progit.bootcss.com/images/lifecycle.png)

*Figure 8. 文件的状态变化周期*

#### 检查当前文件状态

```console
git status
On branch master
nothing to commit, working directory clean

```

#### 状态简览

`git status` 命令的输出十分详细，但其用语有些繁琐。使用 `git status -s` 命令或 `git status --short` 命令，你将得到一种更为紧凑的格式输出。

```console
git status -s
 M README
MM Rakefile
A  lib/git.rb
M  lib/simplegit.rb
?? LICENSE.txt
```

新添加的未跟踪文件前面有 `??` 标记，新添加到暂存区中的文件前面有 `A` 标记，修改过的文件前面有 `M` 标记。 你可能注意到了 `M` 有两个可以出现的位置，出现在右边的 `M` 表示该文件被修改了但是还没放入暂存区，出现在靠左边的 `M` 表示该文件被修改了并放入了暂存区。 例如，上面的状态报告显示： `README` 文件在工作区被修改了但是还没有将修改后的文件放入暂存区,`lib/simplegit.rb` 文件被修改了并将修改后的文件放入了暂存区。 而 `Rakefile` 在工作区被修改并提交到暂存区后又在工作区中被修改了，所以在暂存区和工作区都有该文件被修改了的记录。

#### 忽略文件

文件 `.gitignore` 的格式规范如下：

- 所有空行或者以 `＃` 开头的行都会被 Git 忽略。
- 可以使用标准的 glob 模式匹配。
- 匹配模式可以以（`/`）开头防止递归。
- 匹配模式可以以（`/`）结尾指定目录。
- 要忽略指定模式以外的文件或目录，可以在模式前加上惊叹号（`!`）取反。

所谓的 glob 模式是指 shell 所使用的简化了的正则表达式。 星号（`*`）匹配零个或多个任意字符；`[abc]` 匹配任何一个列在方括号中的字符（这个例子要么匹配一个 a，要么匹配一个 b，要么匹配一个 c）；问号（`?`）只匹配一个任意字符；如果在方括号中使用短划线分隔两个字符，表示所有在这两个字符范围内的都可以匹配（比如 `[0-9]` 表示匹配所有 0 到 9 的数字）。 使用两个星号（`*`) 表示匹配任意中间目录，比如`a/**/z` 可以匹配 `a/z`, `a/b/z` 或 `a/b/c/z`等。

GitHub 有一个十分详细的针对数十种项目及语言的 `.gitignore` 文件列表，你可以在 <https://github.com/github/gitignore> 找到它.

#### 查看已暂存和未暂存的修改

```console
git diff            # 比较工作区和暂存区
git diff --staged   # 比较暂存区和git仓库
git diff --cached   # 同上
```

#### 提交更新

```console
git commit -m "Story 182: Fix benchmarks for speed"
```

#### 跳过使用暂存区域

Git 提供了一个跳过使用暂存区域的方式， 只要在提交的时候，给 `git commit` 加上 `-a` 选项，Git 就会自动把所有已经跟踪过的文件暂存起来一并提交，从而跳过 `git add` 步骤：

```console
git commit -a -m 'added new benchmarks'
```

#### 移除文件

```console
git rm PROJECTS.md            # 删除工作区和暂存区文件
git rm --cached PROJECTS.md   # 删除暂存区文件。对文件不再trace
```

使用glob模式，删除多个文件。

```console
git rm log/\*.log
```

#### 移动文件

```console
git mv README.md README
git status
On branch master
Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

    renamed:    README.md -> README
```

其实，运行 `git mv` 就相当于运行了下面三条命令：

```console
mv README.md README
git rm README.md
git add README
```

### 查看提交历史

```console
git log
```

这个命令会列出每个提交的 SHA-1 校验和、作者的名字和电子邮件地址、提交时间以及提交说明。

```console
git log -p -2     # -p:显示每次提交的内容差异; -2:仅显示最近两次提交
git log --stat    #  --stat 选项在每次提交的下面列出额所有被修改过的文件、有多少文件被修改了以及被修改过的文件的哪些行被移除或是添加了
git log --pretty=oneline   # oneline 将每个提交放在一行显示，查看的提交数很大时非常有用
```

[`git log --pretty=format` 常用的选项](https://progit.bootcss.com/#pretty_format) 列出了常用的格式占位符写法及其代表的意义。

*Table 1.* `git log --pretty=format` *常用的选项*

| 选项  | 说明                                        |
| :---- | :------------------------------------------ |
| `%H`  | 提交对象（commit）的完整哈希字串            |
| `%h`  | 提交对象的简短哈希字串                      |
| `%T`  | 树对象（tree）的完整哈希字串                |
| `%t`  | 树对象的简短哈希字串                        |
| `%P`  | 父对象（parent）的完整哈希字串              |
| `%p`  | 父对象的简短哈希字串                        |
| `%an` | 作者（author）的名字                        |
| `%ae` | 作者的电子邮件地址                          |
| `%ad` | 作者修订日期（可以用 --date= 选项定制格式） |
| `%ar` | 作者修订日期，按多久以前的方式显示          |
| `%cn` | 提交者（committer）的名字                   |
| `%ce` | 提交者的电子邮件地址                        |
| `%cd` | 提交日期                                    |
| `%cr` | 提交日期，按多久以前的方式显示              |
| `%s`  | 提交说明                                    |



当 oneline 或 format 与另一个 `log` 选项 `--graph` 结合使用时尤其有用。 这个选项添加了一些ASCII字符串来形象地展示你的分支、合并历史：

```console
git log --pretty=format:"%h %s" --graph
* 2d3acf9 ignore errors from SIGCHLD on trap
*  5e3ee11 Merge branch 'master' of git://github.com/dustin/grit
|\
| * 420eac9 Added a method for getting the current branch.
* | 30e367c timeout code and tests
* | 5a09431 add timeout protection to grit
* | e1193f8 support for heads with slashes in them
|/
* d6016bc require time for xmlschema
*  11d191e Merge branch 'defunkt' into local
```

[`git log` 的常用选项](https://progit.bootcss.com/#log_options) 列出了我们目前涉及到的和没涉及到的选项，以及它们是如何影响 log 命令的输出的：

*Table 2.* `git log` *的常用选项*

| 选项              | 说明                                                         |
| :---------------- | :----------------------------------------------------------- |
| `-p`              | 按补丁格式显示每个更新之间的差异。                           |
| `--stat`          | 显示每次更新的文件修改统计信息。                             |
| `--shortstat`     | 只显示 --stat 中最后的行数修改添加移除统计。                 |
| `--name-only`     | 仅在提交信息后显示已修改的文件清单。                         |
| `--name-status`   | 显示新增、修改、删除的文件清单。                             |
| `--abbrev-commit` | 仅显示 SHA-1 的前几个字符，而非所有的 40 个字符。            |
| `--relative-date` | 使用较短的相对时间显示（比如，“2 weeks ago”）。              |
| `--graph`         | 显示 ASCII 图形表示的分支合并历史。                          |
| `--pretty`        | 使用其他格式显示历史提交信息。可用的选项包括 oneline，short，full，fuller 和 format（后跟指定格式）。 |

还有按照时间作限制的选项，比如 `--since` 和 `--until` 也很有用。 例如，下面的命令列出所有最近两周内的提交：

```console
git log --since=2.weeks
```

另一个非常有用的筛选选项是 `-S`，可以列出那些添加或移除了某些字符串的提交。 比如说，你想找出添加或移除了某一个特定函数的引用的提交，你可以这样使用：

```console
git log -Sfunction_name
```

在 [限制 `git log` 输出的选项](https://progit.bootcss.com/#limit_options) 中列出了常用的选项

| 选项                  | 说明                               |
| :-------------------- | :--------------------------------- |
| `-(n)`                | 仅显示最近的 n 条提交              |
| `--since`, `--after`  | 仅显示指定时间之后的提交。         |
| `--until`, `--before` | 仅显示指定时间之前的提交。         |
| `--author`            | 仅显示指定作者相关的提交。         |
| `--committer`         | 仅显示指定提交者相关的提交。       |
| `--grep`              | 仅显示含指定关键字的提交           |
| `-S`                  | 仅显示添加或移除了某个关键字的提交 |

实际的例子，如果要查看 Git 仓库中，2008 年 10 月期间，Junio Hamano 提交的但未合并的测试文件，可以用下面的查询命令。

```console
git log --pretty="%h - %s" --author=gitster --since="2008-10-01" \
   --before="2008-11-01" --no-merges -- t/
5610e3b - Fix testcase failure when extended attributes are in use
acd3b9e - Enhance hold_lock_file_for_{update,append}() API
f563754 - demonstrate breakage of detached checkout with symbolic link HEAD
d1a43f2 - reset --hard/read-tree --reset -u: remove unmerged new paths
51a94af - Fix "checkout --track -b newbranch" on detached HEAD
b0ad11e - pull: allow "git pull origin $something:$current_branch" into an unborn branch
```

### 撤消操作

- 有时候我们提交完了才发现漏掉了几个文件没有添加，或者提交信息写错了。

```console
git commit --amend    
```

这个命令会将暂存区中的文件提交。 如果自上次提交以来你还未做任何修改（例如，在上次提交后马上执行了此命令），那么快照会保持不变，而你所修改的只是提交信息。最终你只会有一个提交 - 第二次提交将代替第一次提交的结果。

#### 取消暂存的文件

如何操作暂存区域与工作目录中已修改的文件，当然也包括撤销。例如，已经修改了两个文件并且想要将它们作为两次独立的修改提交，但是却意外地输入了 `git add *` 暂存了它们两个。 如何只取消暂存两个中的一个呢？

```console
touch 2.txt
touch 3.txt
git status
git add *
git status
# On branch master
# Changes to be committed:
#   (use "git reset HEAD <file>..." to unstage)
#
#       modified:   2.txt
#       modified:   3.txt
#
```

```console
git reset HEAD 3.txt
git status
# On branch master
# Changes to be committed:
#   (use "git reset HEAD <file>..." to unstage)
#
#       modified:   2.txt
#
# Changes not staged for commit:
#   (use "git add <file>..." to update what will be committed)
#   (use "git checkout -- <file>..." to discard changes in working directory)
#
#       modified:   3.txt
#
```

在调用时加上 `--hard` 选项**可以**令 `git reset` 成为一个危险的命令（译注：可能导致工作目录中所有当前进度丢失！），但本例中工作目录内的文件并不会被修改。 不加选项地调用 `git reset` 并不危险 — 它只会修改暂存区域。

在 [重置揭密](https://progit.bootcss.com/#_git_reset) 中了解 `reset`的更多细节以及如何掌握它做一些真正有趣的事。

#### 撤消对文件的修改

```console
git checkout -- 3.txt
git status 
# On branch master
# Changes to be committed:
#   (use "git reset HEAD <file>..." to unstage)
#
#       modified:   2.txt
#

```

git checkout -- [file]` 是一个危险的命令，这很重要。 你对那个文件做的任何修改都会消失 - 你只是拷贝了另一个文件来覆盖它。 除非你确实清楚不想要那个文件了，否则不要使用这个命令。

### 远程仓库的使用

#### 查看远程仓库

```console
git remote -v
origin  git@github.com:xuxiangwen/git-lab.git (fetch)
origin  git@github.com:xuxiangwen/git-lab.git (push)
```

#### 添加远程仓库

```console
git remote add lab1 https://github.com/xuxiangwen/git-lab1.git
git remote -v
lab1    https://github.com/xuxiangwen/git-lab1.git (fetch)
lab1    https://github.com/xuxiangwen/git-lab1.git (push)
origin  git@github.com:xuxiangwen/git-lab.git (fetch)
origin  git@github.com:xuxiangwen/git-lab.git (push)
```

#### 从远程仓库中抓取与拉取

从远程仓库中获得数据，可以执行：

```console
git fetch lab1   # 为何没有把lab1上新的文件拿下来，fetch和pull区别何在
```

这个命令会访问远程仓库，从中拉取所有你还没有的数据。必须注意 `git fetch` 命令会将数据拉取到你的本地仓库 - 它并不会自动合并或修改你当前的工作，也就是不会影响工作区和缓存区。

#### 推送到远程仓库

当你想分享你的项目时，必须将其推送到上游。

```console
git push origin master
```

#### 查看远程仓库

```console
git remote show origin
```

#### 远程仓库的移除与重命名

```console
git remote rename lab1 lab_1
git remote rm lab_1
```

### 打标签

其他版本控制系统（VCS）一样，Git 可以给历史中的某一个提交打上标签，以示重要。

#### 列出标签

```console
git tag
git tag -l 'v1.8.5*'    #  如果只对 1.8.5 系列感兴趣
```

#### 创建标签

Git 使用两种主要类型的标签：

- 轻量标签（lightweight）: 一个轻量标签很像一个不会改变的分支 - 它只是一个特定提交的引用。

- 附注标签（annotated）

  附注标签是存储在 Git 数据库中的一个完整对象。 它们是可以被校验的；其中包含打标签者的名字、电子邮件地址、日期时间；还有一个标签信息；并且可以使用 GNU Privacy Guard （GPG）签名与验证。 通常建议创建附注标签，这样你可以拥有以上所有信息。

#### 附注标签

```console
git tag -a v1.4 -m 'my version 1.4'
```

#### 轻量标签

轻量标签本质上是将提交校验和存储到一个文件中 - 没有保存任何其他信息。

```console
git tag v1.4-lw
git show v1.4-lw
```

#### 后期打标签

```console
git log --pretty=oneline
git tag -a v1.2 -m 'my version 1.2' f08f3f
git show v1.2
```

#### 共享标签

默认情况下，`git push` 命令并不会传送标签到远程仓库服务器上。 在创建完标签后你必须显式地推送标签到共享服务器上。 这个过程就像共享远程分支一样 - 你可以运行 `git push origin [tagname]`。

```console
git push origin v1.4
git push origin --tags     # 一次性推送很多标签
```

#### 检出标签

在 Git 中你并不能真的检出一个标签，因为它们并不能像分支一样来回移动。 如果你想要工作目录与仓库中特定的标签版本完全一样，可以使用 `git checkout -b [branchname] [tagname]` 在特定的标签上创建一个新分支：

```console
git checkout -b version2 v2.0.0
```

### Git 别名

```console
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
```

```console
git config --global alias.last 'log -1 HEAD'
git last
```

### 总结

我们已经讲完了 Git 分支与合并的基础知识。 你现在应该能自如地创建并切换至新分支、在不同分支之间切换以及合并本地分支。 你现在应该也能通过推送你的分支至共享服务以分享它们、使用共享分支与他人协作以及在共享之前使用变基操作合并你的分支。 下一章，我们将要讲到，如果你想要运行自己的 Git 仓库托管服务器，你需要知道些什么。