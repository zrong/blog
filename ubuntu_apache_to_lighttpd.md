[从Apache到Lighttpd](http://zengrong.net/post/1786.htm)

购买了[阿里云服务器之后](http://zengrong.net/post/1761.htm)，由于内存过小，[MySQL经常挂掉](http://zengrong.net/post/1761.htm)。[挂载了虚拟内存之后](http://zengrong.net/post/1763.htm)，MySQL倒是不挂了，但Apache总是占用过多内存，导致磁盘频繁读取（阿里云服务器的磁盘性能就那就一个弱啊），服务器响应缓慢，甚至远程登录都无法完成，只能通过网页控制台重启服务器。

Google了一堆优化512MB内存服务器的资料，设置后都没什么用处，服务器依然是每天挂2～3次。

别以为我的服务器访问量有多么的大，整个服务器上只放了一个博客程序，IP访问量每天几百次。当然，这个博客程序就是臭名昭著的各大主机商都痛恨的WordPress。

今天下决心把Apache换成Lighttpd，希望能解决内存不够的老大难问题。

以下是从Apache到Lighttpd转换过程中遇到的几个新手小白问题。这不是教程，只是解决方案，因此略去了安装等基本过程。<!--more-->

## 403 forbidden
**问题：**
按照 <http://wiki.ubuntu.org.cn/Lighttpd> 的说明装好Lighttpd并启动之后，在访问php页面的时候，提示403 forbidden，html页面正常。

**解决**
这个403错误其实是误报，并非没有权限访问php文件，而是没有权限访问php-cgi模块。
Lighttpd安装后，默认只启用了一个mod，就是fastcgi，但没有启用php支持。必须手动启用fastcgi-php模块才支持php访问：

<pre lang="BASH">
lighty-enable-mod fastcgi-php
service lighttpd force-reload
</pre>

Ubuntu英文官方Wiki说得很清楚： <https://wiki.ubuntu.com/Lighttpd+PHP>。

## 启用PHP-FPM
**问题**
按照上面的方式启用的php运行在fast-cgi模式。如何启用PHP-FPM？

**解决**
建立 `/etc/lighttpd/conf-availeable/10-fastcgi-fpm.conf` 文件，写入如下内容：
<pre lang="BASH">
server.modules += ("mod_fastcgi")
fastcgi.server = ( ".php" =>
  ((
      "host" => "127.0.0.1",
      "port" => "9000"
   ))
)
</pre>

禁用fastcgi模块和fastcgi的php支持，使用刚才建立的 `fastcgi-fpm` 模块同时支持两者。
<pre lang="BASH">
lighty-disable-mod fastcgi
lighty-disable-mod fastcgi-php
lighty-enable-mod fastcgi-fpm
service lighttpd force-reload
</pre>

查看phpinfo，可以看到已经是FPM支持了：

<img src="/wp-content/uploads/2013/01/lighttpd-php-fpm.png" alt="lighttpd-php-fpm" width="600" height="416" class="aligncenter size-full wp-image-1787" />

## WordPress的rewrite规则不起作用
**问题**
WordPress中设定的固定链接不起作用，访问的时候显示404

**解决**
WordPress启用了固定链接功能后，会自动在网页根目录建立.htaccess文件，并在其中写入rewrite规则。Apache会读取这个规则，从而实现固定链接。
但是Lighttpd并不兼容Apache制订的rewrite规则。因此，需要为WordPress制订Lighttpd能够支持的rewrite规则。
我使用的规则如下：
<pre lang="BASH">
url.rewrite = (
	"^/(wp-.+).*/?" => "$0",
	"^/(sitemap.xml)" => "$0",
	"^/(xmlrpc.php)" => "$0",
	"^/(.+)/?$" => "/index.php/$1"
)
</pre>

或者这个：

<pre lang="BASH">
url.rewrite-final = (
	# Exclude some directories from rewriting
	"^/(wp-admin|wp-includes|wp-content|gallery2)/(.*)" => "$0",
	# Exclude .php files at root from rewriting
	"^/(.*.php)" => "$0",
	# Handle permalinks and feeds
	"^/(.*)$" => "/index.php/$1"
)
</pre>

## 参考

* [URL rewriting for wordparess and lighttpd](http://emil.haukeland.name/webservers/2010/url-rewriting-for-wordpress-and-lighttpd/)
* [url.rewrite for WordPress on Lighttpd](http://blog.forret.com/2007/03/urlrewrite-for-wordpress-on-lighttpd/)
* [Migrating from Apache to lighty](http://redmine.lighttpd.net/projects/lighttpd/wiki/MigratingFromApache#mod_rewrite)
* [URL Rewrites](http://redmine.lighttpd.net/projects/1/wiki/Docs_ModRewrite)
* [lighttpd虚拟主机的配置](http://blog.gsywx.com/read.php/73.htm)
* [Lighttpd, PHP with PHP-FPM, and MySQL Under Ubuntu Maverick](http://serversreview.net/lighttpd-php-with-php-fpm-and-mysql-under-ubuntu-maverick)
