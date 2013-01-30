[使用Cygwin在Windows中以服务方式安装Lighttpd](http://zengrong.net/post/1793.htm)

## 缘起

自动前段时间对服务器进行了[从Apache到Lighttp](http://zengrong.net/post/1786.htm)的转换之后，服务器运行异常的稳定。Lighttpd占用内存非常小，配置文件也很简单，这让我萌生了把所有服务器都从Apache转到Lighttpd的想法。

但这毕竟是个浩大的工程，而且运行正稳定的服务器也不必这么折腾。于是先从我的本机开刀。

我的每台工作电脑都会安装[XAMPP](http://www.apachefriends.org/en/xampp.html)套件，主要是用于开发和共享，以及存放一些html格式的文档以方便浏览。

而现在XAMPP可以退休了。

## 系统需求

Lighttpd并没有官方的Windows版本，本文基于[Cygwin](http://www.cygwin.com)来安装Lighttpd。

本文假设你了解Cygwin的基本用法和配置，了解如何使用Cygwin的setup来安装新的包。

如果你不喜欢setup.exe那个界面，可以试试[apt-cyg](http://zengrong.net/post/1792.htm)。

## 安装cygserver

[cygserver](http://cygwin.com/cygwin-ug-net/using-cygserver.html)是为Cygwin作为后台服务运行而设计的，默认安装Cygwin的时候并没有启动它。我们需要打开它，并将它作为Windows的标准服务来安装。<!--more-->

在Cygwin中输入命令：

<pre lang="BASH">
cygserver-config
</pre>

按照界面提示进行cygserver的安装，并同意将其安装为服务。

运行该服务：

<pre lang="BASH">
cygrunsrv --start cygserver
</pre>

cygrunsrv其实是启动的Windows标准服务cygserver，这个命令也可以在Cmd下这样做：

<pre lang="DOS">
net start cygserver
</pre>

或者也可以按下按键 `Windows+R` ，键入 `services.msc` 回车，找到 `CYGWI cygwerver`服务，并启动之。

这三种启动服务的方法的作用都一样，下面统一使用 `cygrunsrv` 的方法。

查看cygserver服务的状态：

<pre lang="BASH">
cygrunsrv --qurey cygserver

# 显示
Service             : cygserver
Display name        : CYGWIN cygserver
Current State       : Running
Controls Accepted   : Stop
Command             : /usr/sbin/cygserver
</pre>

## 测试Lighttpd

安装Lighttpd包，由于 **系统需求** 中提到的假设，安装过程略。

测试Lighttpd的运行：

<pre lang="BASH">
/usr/sbin/lighttpd -D -f /etc/lighttpd/lighttpd.conf
</pre>

如果出现下面这样的报错，需要调整lighttpd.conf中的某些和网络相关的配置。因为Lighttpd是运行在Linux下的，默认的配置在Windows下面是不受支持的。

<pre>
2013-01-11 11:01:59: (/usr/src/ports/lighttpd/lighttpd-1.4.32-2/src/lighttpd-1.4.32/src/configfile.c.1339) the selected event-handler in unknown or not supported: linux-sysepoll 
2013-01-11 11:01:59: (/usr/src/ports/lighttpd/lighttpd-1.4.32-2/src/lighttpd-1.4.32/src/server.c.646) setting default values failed 
2013-01-11 11:07:36: (/usr/src/ports/lighttpd/lighttpd-1.4.32-2/src/lighttpd-1.4.32/src/network.c.260) warning: please use server.use-ipv6 only for hostnames, not without server.bind / empty address; your config will break if the kernel default for IPV6_V6ONLY changes 
2013-01-11 11:07:36: (/usr/src/ports/lighttpd/lighttpd-1.4.32-2/src/lighttpd-1.4.32/src/network.c.802) server.network-backend has a unknown value: linux-sendfile 
2013-01-11 11:11:34: (/usr/src/ports/lighttpd/lighttpd-1.4.32-2/src/lighttpd-1.4.32/src/server.c.915) can't have more connections than fds/2:  1024 256 
</pre>

涉及的配置项如下，将他们全部注释：

* server.event-handler 约在181行
* server.use-ipv6 约在93行
* server.network-backend 约在191行
* server.max-fds 约在207行
* server.max-connections 约在245行

如果在运行的时候提示目录权限之类问题，则可以修改 Lighttpd.conf 中的 16~20 行配置，设置正确的目录和权限。

如果执行正常，那么不会输出任何信息，Lighttpd会一直在前台运行。

此时可以去浏览器中输入 `http://localhost` 测试一下，当然，要看到内容，需要确保你的Lighttpd.conf中的主页地址配置正确，即使你看到的是404错误，其实也说明你的服务器配置成功了，只是没有默认的页面而已。

## 将Lighttpd安装成服务

使用cygrunsrv可以将Lighttpd安装成Windows系统服务

<pre lang="BASH">
cygrunsrv -I lighttpd -d 'CYGWIN lighttpd' -p '/usr/sbin/lighttpd' -a '-D -f /etc/lighttpd/lighttpd.conf'
</pre>

然后运行它

<pre lang="BASH">
cygrunsrv --start lighttpd
</pre>

查询运行状态

<pre lang="BASH">
cygrunsrv --query lighttpd

Service             : lighttpd
Display name        : CYGWIN lighttpd
Current State       : Running
Controls Accepted   : Stop
Command             : /usr/sbin/lighttpd -D -f /etc/lighttpd/lighttpd.conf
</pre>

## 参考

* <http://redmine.lighttpd.net/boards/2/topics/3235>
* <http://www.xker.com/page/e2007/1022/36592.html>
* <http://webcache.googleusercontent.com/search?q=cache:ngnWxnFusY0J:zandyware.com/blog/2010/11/23/install-lighttpd-as-a-service-in-cygwin/&hl=zh-CN&tbo=d&strip=1>
* <http://fabrizioballiano.net/2012/05/02/cygwin-lighttpd-php-mysql-the-perfect-dev-setup-for-windows/>
* <http://linuxzh.3322.org/?p=476>
* <http://guoyoooping.blog.163.com/blog/static/1357051832010101794654132/>
* <http://cygwin.com/cygwin-ug-net/using-cygserver.html>
* <http://ipggi.wordpress.com/2011/07/01/cygwin-walkthrough-and-beginners-guide-is-it-linux-for-windows-or-a-posix-compatible-alternative-to-powershell/>
