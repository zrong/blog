[Ubuntu Server挂载swap文件](http://zengrong.net/post/1763.htm)

我在为[服务器](http://zengrong.net/post/1761.htm)安装系统的时候，并没有挂载swap分区。把博客转过来之后，发现[MySQL时不时就罢工](http://zengrong.net/post/1762.htm)，原因就是内存不足。看来必须要挂载一个swap分区才好。

但是，我在对数据盘进行分区的时候，把整个磁盘都用上了，并没用预留空间。swap分区是行不通了，只能试试swap文件。<!--more-->

## 建立一个有连续空间的空白文件

服务器的物理内存是512MB，按照1.5~2倍原则，我将swap文件设置为1GB。

<pre lang="BASH">
#root@aliyun:/srv# dd if=/dev/zero of=SWAPFILE bs=1024 count=1048576
1048576+0 records in
1048576+0 records out
1073741824 bytes (1.1 GB) copied, 59.7957 s, 18.0 MB/s
</pre>

## 使用swap文件

使用 `swapon` 命令让系统使用这个文件作为swap文件。但是这个文件不能直接使用，否则会报错：

<pre lang="BASh">
root@aliyun:/srv# swapon swapfile
swapon: /srv/swapfile: read swap header failed: Invalid argument
</pre>

必须先使用 `mkswap` 将文件格式化成swap格式（不知道为什么会少了4KB）：

<pre lang="BASH">
root@aliyun:/srv# mkswap SWAPFILE 1048576
Setting up swapspace version 1, size = 1048572 KiB
no label, UUID=1aaed031-33ef-479b-a9a4-2f008a7bbb2f
</pre>

使用格式化完毕的文件：

<pre lang="BASH">
root@aliyun:/srv# swapon SWAPFILE
</pre>

查看文件使用情况：

<pre lang="BASH">
root@aliyun:/srv# swapon -s
Filename                                Type            Size    Used    Priority
/srv/SWAPFILE                           file            1048572 95852   -1
</pre>

## 加入自动启用

为避免重启后swapfile生效，可以将启用swap的代码加入启动文件中，对于ubuntu server，编辑 `/etc/rc.local` 文件，加入以下内容（具体文件路径自定）：

<pre lang="BASH">
swapon /srv/SWAPFILE
</pre>

**或者**

修改 `/etc/fstab` 文件，加入以下内容：

<pre lang="BASH">
/srv/SWAPFILE   swap    swap    defaults        0       0
</pre>

