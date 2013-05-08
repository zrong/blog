<span style="color:red;">2012-11-04更新：</span>官方的“终极”解决方案：msysGit1.7.10开始使用UTF-8编码保存文件名。
<span style="color:red;">2011-10-24更新：</span> 从<a href="http://giftdotyoung.blogspot.com/2011/03/blog-post_31.html" title="宽容那些与我们不同的人" target="_blank">一篇链接到本篇文章的文章(我对这篇文章提出的与windows患者的相处之道深感赞同)</a>找到了一个“终极”解决方案，但我没有测试。

<hr />
我一直是在cygwin下使用git，辅以TortoiseGit。使用上没什么问题，但今天在处理一个有中文文件名的项目时却出现文件名乱码的问题。

## 情况重现

<ol>
	<li>在一个使用cygwin的bash提交的git项目中，已经完成了所有的提交，但使用TortoiseGit查看的时候，却发现仍有文件没有提交，甚至是有文件还处于未暂存的状态。于是使用TortoiseGit提交；</li>
	<li>再次用cygwin下的git status查看，这次又发现了未提交的情况。再次用git commit命令行提交；</li>
	<li>回到TortoiseGit下查看，问题又出现了！此时准备返回两次提交前的版本，却因为文件名乱码的问题，无法返回了！</li>
</ol>

## 乱码原因

搜索一番，发现git文件名、log乱码，是普遍问题，这其中有编码的原因，也有跨平台的原因。主要原因是Windows 系统中的Git对中文文件名采用不同的编码保存所致。

Windows系统中使用的msysGit，采用的是系统编码来保存文件名；而Cygwin中的Git默认采用UTF-8编码来保存文件名。如果两个软件同时对一个版本库进行操作，且都认为对方是使用自己使用的编码来保存文件，就会导致文件名编码混乱，无法识别。

这就导致，如果一直使用TortoiseGit（实际调用MsysGit）提交，那么中文文件名没问题；一直使用cygwin提交，中文文件名也没问题。<strong>但一定不能交叉使用。</strong>

分别设置L<strong>ANG、LC_CTYPE、LC_ALL</strong>参数为同样的编码，问题依旧。

cygwin官方网站提到了非拉丁语文件名的问题，也许研究后能解决该吧：<a href="http://www.cygwin.com/cygwin-ug-net/setup-locale.html" target="_blank">Chapter 2. Setting Up Cygwin</a>

这里还有一篇讲解Linux系统编码文章：<a href="http://jmut.bokee.com/6874378.html" target="_blank">locale的设定及其LANG、LC_ALL、LANGUAGE环境变量的区别</a>

## 官方终极解决方案

这个问题的官方终极解决方案，就是更新到msysGit1.7.10或更新版本。这个版本之后，msysGit和Git for Windows已经采用了UTF-8编码来保存文件名，不会再出现乱码的情况。安装和使用可参考这篇文章：[使用Git、Git GUI和TortoiseGit](http://zengrong.net/post/1722.htm)

不幸的是，对于使用老版本msysGit提交的版本库，升级到msysGit1.7.10或者更高会出现编码问题。

有两篇文章介绍了这个问题的解决办法：
* [升級到 msysgit 1.7.10 的檔名亂碼處理方式（需要翻墙）](http://jiichen.blogspot.tw/2012/04/msysgit-1710.html)
* [upgrading to msysGit 1.7.10 (or higher)](http://blog.syntevo.net/2012/04/24/1335271500000.html)

<!--more-->

<hr>
<span style="font-size:12pt;color:red;">下面的文章，是历史遗留，可以不看。若希望知其所以然，则不妨观之。</span>

## 乱码情景对号入座和解决方案
### 乱码情景1
在cygwin中，使用git add添加要提交的文件的时候，如果文件名是中文，会显示形如274\232\350\256\256\346\200\273\347\273\223.png的乱码。
<strong>解决方案：</strong>
在bash提示符下输入：
<pre>git config --global core.quotepath false</pre>
core.quotepath设为false的话，就不会对0x80以上的字符进行quote。中文显示正常。

### 乱码情景2
在MsysGit中，使用git log显示提交的中文log乱码。
<strong>解决方案：</strong>
设置git gui的界面编码
<pre>git config --global gui.encoding utf-8</pre>

设置 commit log 提交时使用 utf-8 编码，可避免服务器上乱码，同时与linux上的提交保持一致！
<pre>git config --global i18n.commitencoding utf-8</pre>

使得在 $ git log 时将 utf-8 编码转换成 gbk 编码，解决Msys bash中git log 乱码。
<pre>git config --global i18n.logoutputencoding gbk</pre>

使得 git log 可以正常显示中文（配合i18n.logoutputencoding = gbk)，在 /etc/profile 中添加：
<pre>export LESSCHARSET=utf-8</pre>

### 乱码情景3

在MsysGit自带的bash中，使用ls命令查看中文文件名乱码。cygwin没有这个问题。
<strong>解决方案：</strong>
使用 `lls --show-control-chars` 命令来强制使用控制台字符编码显示文件名，即可查看中文文件名。

为了方便使用，可以编辑 `/etc/git-completion.bash` ，新增一行 `alias ls="ls --show-control-chars"`

## 终极解决方案

终极的解决方案是通过修改git和TortoiseGit源码实现，有网友这么做了：<a href="http://www.cnblogs.com/tinyfish/archive/2010/12/17/1909463.html" target="_blank">让Windows下Git和TortoiseGit支持中文文件名/UTF-8</a>，也可以直接访问这个开源的Google项目：<a href="http://code.google.com/p/utf8-git-on-windows">utf8-git-on-windows</a>。

如果不抗拒命令行的话，直接用Cygwin来提交Git库。因为Cygwin其实是一个在Windows平台上的模拟器，它完全模拟GNU/Linux的方式运行，所以Cygwin中的Git是采用UTF-8编码来保存中文的。

## <del>又一个“终极”解决方案（<a href="http://giftdotyoung.blogspot.com/2011/03/blog-post_31.html" target="_blank">来自</a>）</del>（msysGit1.7.10之后，不再推荐此方案）

在操作git时，把区域设置修改为 中文GBK。这之后就可以进行git相关操作了。

<strong>在终端中跟windows保持一致</strong>

<pre lang="bash">
export LC_ALL=zh_CN.GBK; export LANG=zh_CN.GBK
terminal -> set charactor encoding -> gbk
</pre>

<strong>切换回linux默认</strong>

<pre lang="bash">
export LC_ALL=en_US.utf8; export LANG=en_US.utf8
terminal -> set charactor encoding -> unicode(utf-8)
</pre>

<strong>改变文件名的编码</strong>

如果已经造成乱码的恶果，还可以在utf8和gbk之间切换文件名。真的修改，而不是像上面那样修改显示的（解码的）效果。

<pre lang="bash">
convmv <filename> -f utf8 -t gbk
</pre>

例外：convmv在fat32的U盘上运行无效，估计是fat32不允许非法编码。

## 本文参考链接
<ul>
	<li><a href="http://topic.csdn.net/u/20110113/19/b0d5d506-4307-428b-a61d-7974aa66a2da.html" target="_blank">搞定Git中文乱码、用TortoiseMerge实现Diff/Merge</a></li>
	<li><a href="http://topic.csdn.net/u/20110106/20/f11ef8dd-44ec-478e-b78a-73240bcdde43.html" target="_blank">MsysGit乱码与跨平台版本管理</a></li>
	<li><a href="http://bbs.et8.net/bbs/showthread.php?t=942185" target="_blank">git中文文件名、目录名乱码应该怎么解决？</a></li>
</ul>

