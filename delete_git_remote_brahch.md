[Git查看、删除远程分支](http://zengrong.net/post/1746.htm)

## 查看远程分支

加上-a参数可以查看远程分支，远程分支会用红色表示出来（如果你开了颜色支持的话）：
<pre lang="BASH">
# git branch -a
  master
  remote
  tungway
  v1.52
* zrong
  remotes/origin/master
  remotes/origin/tungway
  remotes/origin/v1.52
  remotes/origin/zrong
</pre>

## 删除远程分支

在Git v1.7.0 之后，可以使用这种语法删除远程分支：

<pre lang="BASH">
git push origin --delete <branchName>
</pre>
<!--more-->
否则，可以使用这种语法，推送一个空分支到远程分支，其实就相当于删除远程分支：

<pre lang="BASH">
git push origin :<branchName>
</pre>

两种语法作用完全相同。

## 删除不存在对应远程分支的本地分支

假设这样一种情况：
1. 我创建了本地分支b1并pull到远程分支 `origin/b1`；
2. 其他人在本地使用fetch或pull创建了本地的b1分支；
3. 我删除了 `origin/b1` 远程分支；
4. 其他人再次执行fetch或者pull并不会删除这个他们本地的 `b1` 分支，运行 `git branch -a` 也不能看出这个branch被删除了，如何处理？

使用下面的代码查看b1的状态：

<pre lang="BASH">
# git remote show origin
* remote origin
  Fetch URL: git@github.com:xxx/xxx.git
  Push  URL: git@github.com:xxx/xxx.git
  HEAD branch: master
  Remote branches:
    master                 tracked
    refs/remotes/origin/b1 stale (use 'git remote prune' to remove)
  Local branch configured for 'git pull':
    master merges with remote master
  Local ref configured for 'git push':
    master pushes to master (up to date)
</pre>

这时候能够看到b1是stale的，使用 `git remote prune origin` 可以将其从本地版本库中去除。

更简单的方法是使用这个命令，它在fetch之后删除掉没有与远程分支对应的本地分支：

<pre lang="BASH">
git fetch -p
<pre>

## 参考文章
* <https://makandracards.com/makandra/621-git-delete-a-branch-local-or-remote>
* <http://stackoverflow.com/questions/2003505/how-do-i-delete-a-git-branch-both-locally-and-in-github>
* <http://www.cnblogs.com/deepnighttwo/archive/2011/06/18/2084438.html>
