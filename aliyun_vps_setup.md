[阿里云经济A型服务器配置](http://zengrong.net/post/1761.htm)

[双11抢了一台阿里云的服务器](http://zengrong.net/post/1735.htm)，一直到今天才有时间来配置，把自己的博客迁了过来。下面是配置过程。

## 服务器配置

* CPU: Xeon 2.26GHz 单核
* 内存：512M
* 硬盘：20GB系统盘 + 20GB数据盘
* 系统：ubuntu 12.04 64位

## 挂载数据盘

数据盘默认是没有挂载的，因此需要先初始化数据盘。
我将数据盘挂载到了 `/srv` 目录中，用它来存放网站文件。
<pre lang="BASH">
#查看所有硬盘
fdisk -l
#创建一个主分区，使用数据盘所有空间，创建过程略
fdisk /dev/xvdb
#格式化刚刚创建的分区为ext4格式
mkfs -t ext4 /dev/xvdb1
#修改fstab，将/dev/xvdb1挂载到/srv
vim fstab
#加入下面一行
/dev/xvdb1      /srv    ext4    defaults        0       0
#自动挂载
mount -a
</pre>

## 配置Apache+PHP+MySQL

安装必须的组件。`php5-mcrypt` 是PHPMyAdmin必须的组件，所以这里一起安装了。
<pre lang="BASH">
apt-get install apache2 mysql-server php5 php5-mysql libapache2-mod-php5 php5-mcrypt
</pre>

启动Apache和MySQL
<pre lang="BASH">
/etc/init.d/apache2 restart
/etc/init.d/mysql restart
#或
service apache2 restart
service mysql restart
</pre>

## 配置虚拟主机

Ubuntu的虚拟主机配置很简单，它将虚拟主机分配到 `/etc/apache2/sites-available/` 和 `/etc/apache2/sites-enabeld` 两个目录，前者用于放置可用站点的配置，后者放置已经启用的站点。
复制默认的配置文件，将其修改成我需要的配置，然后启用它。
<pre lang="BASH">
cp /etc/apache2/sites-available/default /etc/apache2/sites-available/zengrong.net
#a2ensite脚本会自动在 `/etc/apache2/sites-enabled` 下建立一个同名的符号链接
a2ensite zengrong.net
#重启apache使配置生效
service apache2 restart
</pre>
如果希望暂时停止站点，可以使用：
<pre lang="BASH">
a2dissite 站点名
</pre>

## 配置模块

使用 `a2enmod` 和 `a2dismod` 可以启用和禁用模块。可用的模块放在 `/etc/apache2/mods-avalable` 中，已经启用的模块放在 `/etc/apache2/modes-enabled` 中。
<pre lang="BASH">
#启动rewrite模块
a2enmod rewrite
</pre>

## 参考文章

* <http://wiki.ubuntu.com.cn/Apache>
* <http://wiki.ubuntu.com.cn/Apache%E8%99%9A%E6%8B%9F%E4%B8%BB%E6%9C%BA%E6%8C%87%E5%8D%97>
