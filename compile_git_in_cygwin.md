[在Cygwin中编译Git](http://zengrong.net/post/1817.htm)

## 概述

我一直在Cygwin中以命令行的方式使用git。但是Cygwin源中的git版本比较老（v1.7.9），而自 1.7.10以来，git增加了许多新的特性，尤其是对中文用户特别有用的 `使用UTF-8编码保存文件名` 等等。为了使用这些新特性，我们只能自己编译Git。

>如果希望了解我上面说的“对中文用户特别有用的特性”，可以看这篇文章：[git乱码解决方案汇总](http://zengrong.net/post/1249.htm)。

## 下载源码

在这里下载最新的Git源码，我下载的是 v1.8.1.4:

<http://code.google.com/p/git-core/downloads/list>

解压缩源码和手册：

<pre lang="BASH">
tar xvf git-1.8.1.4.tar.gz -C /usr/src
mkdir /usr/local/man
tar xvf git-manpages-1.8.1.4.tar.gz -C /usr/local/man
</pre>

## 编译过程

1. 使用Cygwin提供的setup.exe工具将其升级到最新版本；
2. 如果你安装了git包，卸载它；
3. 安装以下包：
	* zlib
	* openssh
	* openssl
	* perl
	* subversion-perl (如果希望使用 git-svn，需要安装这个包)
	* curl
	* libcurl-devel
	* expat
	* tcltk
	* make
	* gcc
	* ncurses (如果希望使用 clear 命令，需要安装这个包。更多内容可参考这里：[Cygwin，那些不知道在哪里的命令](http://zengrong.net/post/1812.htm)
	* python
4. 编译和安装  
<pre lang="BASH">
./configure --prefix=/usr/local
make && make install
</pre>


## 检测

<pre lang="BASH">
cd ~
which git
</pre>

## 错误解决

如果在安装过程中出现下面的错误，一般是由于 Cygwin目录权限设置有问题所致。

<pre lang="BASH">
make: execvp: gcc: Permission denied
make: install -d -m 755 '/usr/local/bin'
</pre>

要解决 Cygwin 在Windows下的权限问题，有这样几个途径：

1. 如果是 Windows7或者Vista系统，用管理员来执行Cygwin；
2. 修改makefile文件，查找 `-d -m 755` 字样，将其删除；
3. 安装到自己的主目录中，然后移动到 `/usr` 目录，例如：
<pre lang="BASH">
make install DESTDIR=/tmp/myinst/
cp -va /tmp/myinst/ /
</pre>

##参考

* [Why do I get permission denied when I try use “make” to install something?](http://stackoverflow.com/questions/9106536/why-do-i-get-permission-denied-when-i-try-use-make-to-install-something)
* [make: execvp: /usr/bin: Permission denied](https://bbs.archlinux.org/viewtopic.php?id=57631)
* [How to install git on windows](http://blog.laranjee.com/how-to-install-git-on-windows/)
* [使用cygwin编译git v1.8.0源码报错](http://bbs.csdn.net/topics/390254119)
