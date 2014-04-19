管理带有子模块的git库（DragonBonesCPP）

Manage a git library with submodules.

[DragonBonesCPP][5] 是一个包含子模块的库，在 clone/commit/push 的时候需要一些额外的操作。

本文将描述这些操作。

## 子模块(submodule)

限(wei)于(le)篇(tou)幅(lan)，请自行学习下面的内容：

* [Git Submodule使用完整教程][1]
* [6.6 Git Tools - Submodules][2]
* [git-submodule(1) Manual Page][3]
* [子模块][4]

## clone DragonBonesCPP

### 蛋碎方法一

<pre lang="shell">
git clone --recursive git@github.com:DragonBones/DragonBonesCPP.git
</pre>

使用这个方法，将会自动 clone 该项目下的所有子模块。这其实是最简单的方法了。

为什么说它令人蛋碎呢？因为 DragoneBones 中包含的 engines/cocos2d-x 子模块也包含子模块。

这样就出现了嵌套子模块，一个 cocos2d-x 的所有历史加起来就超过1G了，再加上子模块的所有历史，这就……。

### 蛋疼方法二

为了避免蛋碎的问题，我们换一个方法，可是蛋疼是免不了了。

<pre lang="shell">
# git clone git@github.com:DragonBones/DragonBonesCPP.git
Cloning into 'DragonBonesCPP'...
remote: Counting objects: 103, done.
remote: Compressing objects: 100% (87/87), done.
remote: Total 103 (delta 18), reused 96 (delta 13)
Receiving objects: 100% (103/103), 88.96 KiB | 47 KiB/s, done.
Resolving deltas: 100% (18/18), done.

# cd DragonBonesCPP
# DragonBonesCPP git:(master) git submodule status
-a7709c35badbd930f98adaf1c172a3251f8c6543 engines/cocos2d-x

# DragonBonesCPP git:(master) git submodule init
Submodule 'cocos2d-x' (git@github.com:DragonBones/cocos2d-x.git) registered for path 'engines/cocos2d-x'

# DragonBonesCPP git:(master) git submodule update
Cloning into 'engines/cocos2d-x'...
remote: Reusing existing pack: 200502, done.
Receiving objects: 100% (200502/200502), 763.78 MiB | 98 KiB/s, done.
Resolving deltas: 100% (133006/133006), done.
Submodule path 'engines/cocos2d-x': checked out 'a7709c35badbd930f98adaf1c172a32      51f8c6543'
</pre>

等待是漫长的，看我的网速就知道这到底花了多长时间。

和蛋碎方法不同的是，这种方法不会clone cocos2d-x 中的子模块（嵌套子模块）。若有需要，可以进入 cocos2d-x 中再次执行蛋疼方法二。

## 提交子模块修改

待续

## 提交 DragonBones 的修改

待续

## 切换分支

待续

[1]: http://www.kafeitu.me/git/2012/03/27/git-submodule.html
[2]: http://git-scm.com/book/en/Git-Tools-Submodules
[3]: http://git-scm.com/docs/git-submodule
[4]: http://gitbook.liuhui998.com/5_10.html
[5]: https://www.github.com/DragonBones/DragonBonesCPP

