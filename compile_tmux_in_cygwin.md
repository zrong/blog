[在Cygwin下编译tmux（失败）](http://zengrong.net/post/1823.htm)

tmux是GNU Screen的替代者，本文是我在Cygwin下编译tmux的失败经历，记录在案，方便以后重新尝试编译。
本文假设你已经在Cygwin下配置好了编译环境。

要了解tmux，可以看这篇文章：http://linuxtoy.org/archives/from-screen-to-tmux.html
要了解GNU Screen，可以看这两篇文章：

* [linux 技巧：使用 screen 管理你的远程会话](http://www.ibm.com/developerworks/cn/linux/l-cn-screen/)
* [对话 UNIX: 使用 Screen 创建并管理多个 shell](http://www.ibm.com/developerworks/cn/aix/library/au-gnu_screen/)

Cygwin的源中是包含GNU Screen的，但是没有tmux，在 [Cygwin ports](http://sourceware.org/cygwinports/) 中也没有。想要在Cygwin使用tmux，需要自行编译。

## 1. 安装libevent包

tmux编译需要依赖libevent包，但是Cygwin的官方源不包含这个包。不过，我们可以在 [Cygwin Ports](http://sourceware.org/cygwinports/) 找到她。

下面的代码使用apt-cyg安装libevent包。关于apt-cyg用法，可以看这里：[Cygwin的包管理器：apt-cyg](http://zengrong.net/post/1792.htm) 。

<pre lang="BASH">
apt-cyg install libevent-devel --mirror ftp://ftp.cygwinports.org/pub/cygwinports
</pre>

如果你更喜欢源码编译安装，可以在这里下载libevent源码：http://libevent.org/

<pre lang="BASH">
tar xzvf libevent-2.0.21-stable.tar.gz -C /usr/src
cd /usr/src/libevent-2.0.21
./configuare
make && make install
</pre>

## 2. 安装ncurses包

tmux编译需要依赖ncurses包，Cygwin的官方源中就有这个包。

<pre lang="BASH">
apt-cyg install libncurses-devel --mirror http://mirrors.163.com/cygwin
</pre>

但是，这样安装的libncurses包，在编译tmux的时候，始终报错找不到 `ncurses.h`文件，因此我卸载了 `ncurses` 包，改用编译安装。

在这里下载ncurses源码：<http://ftp.gnu.org/pub/gnu/ncurses/>，我下载的是最新的5.9。

编译和安装的方式与 `libevent` 相同，这里不再重复。

## 3. 下载mtux源码

在这里下载tmux源码：<http://tmux.sourceforge.net/>，可能需要翻墙，目前最新版本为1.7。

虽然上面解决了依赖问题，但编译过程中依然遇到了编译错误，无法解决。

就此打住，依然使用 [GNU Screen](http://www.gnu.org/software/screen/) 。
