[Cygwin的包管理器：apt-cyg](http://zengrong.net/post/1792.htm)

Cygwin的包管理工具[setup.exe](http://cygwin.com/setup.exe)实在是难用的让人蛋碎。于是就有了这样一个[apt-cyg](http://jungels.net/projects/apt-cyg/)，可以提供类似于 apt-get 的体验。

apt-cyg使用bash编写，所以连编译都省了。<!--more-->

## 安装apt-cyg

<pre lang="BASH">
wget http://apt-cyg.googlecode.com/svn/trunk/apt-cyg
chmod +x apt-cyg
mv apt-cyg /usr/local/bin/
</pre>

## 安装包

<pre lang="BASH">
apt-cyg install bc
</pre>

## 查找包

<pre lang="BASH">
apt-cyg find php
</pre>

## 设置下载站点和缓存目录
<pre lang="BASH">
apt-cyg -c /cygdrive/d/downloads/cygwin -m http://mirrors.163.com/cygwin/ find php
</pre>

也可以把默认的缓存和下载站点存到文件中，编辑apt-cyg，找到68行：

<pre lang="BASH">
#mirror=ftp://mirror.mcs.anl.gov/pub/cygwin
#cache=/setup
mirror=http://mirrors.163.com/cygwin
cache=/cygdrive/d/downloads/cygwin
</pre>

当然，PHP在cygwin的官方源中是不存在的，我们可以使用cygwinports提供的源：

<pre lang="BASH">
$ apt-cyg -m ftp://ftp.cygwinports.org/pub/cygwinports find php
Working directory is /cygdrive/d/downloads/software/cygwin
Mirror is ftp://ftp.cygwinports.org/pub/cygwinports
--2013-01-08 12:08:07--  ftp://ftp.cygwinports.org/pub/cygwinports/setup.bz2 => “.listing”
正在解析主机 ftp.cygwinports.org (ftp.cygwinports.org)... 209.132.180.131
正在连接 ftp.cygwinports.org (ftp.cygwinports.org)|209.132.180.131|:21... 已连接。
正在以 anonymous 登录 ... 登录成功！
==> SYST ... 完成。   ==> PWD ... 完成。
==> TYPE I ... 完成。 ==> CWD (1) /pub/cygwinports ... 完成。
==> PASV ... 完成。   ==> LIST ... 完成。

    [ <=>                                                         ] 966         --.-K/s 用时 0.01s

2013-01-08 12:08:12 (95.4 KB/s) - “.listing” 已保存 [966]

已删除 “.listing”。
--2013-01-08 12:08:12--  ftp://ftp.cygwinports.org/pub/cygwinports/setup.bz2
           => “setup.bz2”
==> 不需要 CWD。
==> PASV ... 完成。   ==> RETR setup.bz2 ... 完成。
长度：580198 (567K)

100%[============================================================>] 580,198     52.2K/s 用时 16s

2013-01-08 12:08:29 (35.5 KB/s) - “setup.bz2” 已保存 [580198]

Updated setup.ini

Searching for installed packages matching php:
php
php-Archive_Tar
php-Console_Getopt
php-PEAR
php-Structures_Graph
# 以下省略
......
</pre>

