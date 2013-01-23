[小内存服务器MySQL出现Out of memory错误的问题](http://zengrong.net/post/1762.htm)

使用阿里云服务器的第二天，我就收到阿里云的提醒短信，说网站挂掉了。

上网站一看，提示数据库连接错误，重启MySQL了事。

没想到11点钟的时候MySQL再次挂掉了，上服务器一看，原来是MySQL进程被Kill了，原因是 `Out of memory`。

>Dec 14 11:38:02 aliyun kernel: [69756.532361] Out of memory: Kill process 11168 (mysqld) score 114 or sacrifice child
>Dec 14 11:38:02 aliyun kernel: [69756.532430] Killed process 11168 (mysqld) total-vm:821140kB, anon-rss:57004kB, file-rss:0kB

我的服务器内存只有512MB，而且没有配置SWAP分区，看来是MySQL占用的太多内存。找到 `/etc/mysql/my.cnv` 配置进行修改（注意备份）：

<pre>
key_buffer = 16K
max_allowed_packet = 1M
thread_stack = 64K
thread_cache_size = 4
sort_buffer = 64K
net_buffer_length = 2K
#max_connections = 100
#table_cache = 64
#thread_concurrency = 10
</pre>

同时也修改Apache的配置

<pre lant="XML">
Timeout 45
KeepAlive On
MaxKeepAliveRequests 200
KeepAliveTimeout 3
<IfModule mpm_prefork_module>
	StartServers          5
	MinSpareServers       5
	MaxSpareServers      10
	MaxClients          30
	MaxRequestsPerChild   2000
</IfModule>
</pre>

重启Apache 和 MySQL
<pre lang="BASH">
service apache2 restart
service mysql restart
</pre>

**参考资料：**

* <http://forum.slicehost.com/index.php?p=/discussion/3629/out-of-memory-kill-process/p1>
* <http://www.chrisjohnston.org/tech/configuring-a-lightweight-apache-mysql-install-on-debian-ubuntu>
