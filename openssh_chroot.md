[完全使用SFTP替代FTP：Sftp+OpenSSH+Chroot设置详解](http://zengrong.net/post/1616.htm)

由于采用明文传输用户名和密码，FTP协议是不安全的。在同一机房中只要有一台服务器被黑客控制，它就可能获取到其它服务器上的FTP密码，从而控制其它的服务器。

当然，很多优秀的FTP服务器都已经支持加密。但如果服务器上已经开了[SSH](http://zh.wikipedia.org/wiki/SSH)服务，我们完全可以使用[SFTP](http://zh.wikipedia.org/wiki/SFTP)来传输数据，何必要多开一个进程和端口呢？

下面，我就从账户设置、SSH设置、权限设置这三个方面来讲讲如何使用SFTP完全替代FTP。本教程基于CentOS5.4。

## 范例

本文要实现以下功能：

SFTP要管理3个目录：

* homepage
* blog
* pay

权限配置如下：

* 账户www，可以管理所有的3个目录；
* 账户blog，只能管理blog目录；
* 账户pay，只能管理pay目录。

## 账户设置

SFTP的账户直接使用Linux操作系统账户，我们可以用`useradd`命令来创建账户。

首先建立3个要管理的目录：

<pre lang="BASH">
mkdir /home/sftp/homepage
mkdir /home/sftp/blog
mkdir /home/sftp/pay
</pre>

创建sftp组和www、blog、pay账号，这3个账号都属于sftp组：

<pre lang="BASH">
groupadd sftp 
useradd -M -d /home/sftp -G sftp www
useradd -M -d /home/sftp/blog -G sftp blog
useradd -M -d /home/sftp/pay -G sftp pay
#设置3个账户的密码密码
passwd www
passwd blog
passwd pay
</pre>

至此账户设置完毕。

## SSH设置

首先要升级OpenSSH的版本。只有4.8p1及以上版本才支持Chroot。

CentOS 5.4的源中的最新版本是4.3，因此需要升级OpenSSH。

指定新的源：

<pre lang="BASH">
vim /etc/yum.repos.d/test.repo
#输入如下内容
[centalt]
name=CentALT Packages for Enterprise Linux 5 - $basearch
baseurl=http://centos.alt.ru/repository/centos/5/$basearch/
enabled=0
gpgcheck=0
# wq保存
</pre>

执行升级：

<pre lang="BASH">
yum --enablerepo=centalt update -y openssh* openssl*
# 重启服务
service sshd restart
# 重看版本
ssh -V
# OpenSSH_5.8p1, OpenSSL 0.9.8e-fips-rhel5 01 Jul 2008
</pre>

升级成功后，设置sshd_config。通过Chroot限制用户的根目录。

<pre lang="BASH">
vim /etc/ssh/sshd_config
#注释原来的Subsystem设置
Subsystem	sftp	/usr/libexec/openssh/sftp-server
#启用internal-sftp
Subsystem       sftp    internal-sftp
#限制www用户的根目录
Match User www
	ChrootDirectory /home/sftp
	ForceCommand	internal-sftp
#限制blog和pay用户的根目录
Match Group sftp
	ChrootDirectory /home/%u
	ForceCommand	internal-sftp
</pre>

完成这一步之后，尝试登录SFTP：

<pre lang="BASH">
sftp www@abc.com
#或者
ssh www@abc.com
#如果出现下面的错误信息，则可能是目录权限设置错误，继续看下一步
#Connection to abc.com closed by remote host.
#Connection closed
</pre>

## 权限设置

要实现Chroot功能，**目录权限的设置非常重要**。否则无法登录，给出的错误提示也让人摸不着头脑，无从查起。我在这上面浪费了很多时间。

目录权限设置上要遵循2点：

1. ChrootDirectory设置的目录权限及其所有的上级文件夹权限，属主和属组必须是root；
2. ChrootDirectory设置的目录权限及其所有的上级文件夹权限，只有属主能拥有写权限，也就是说权限最大设置只能是755。

如果不能遵循以上2点，即使是该目录仅属于某个用户，也可能会影响到所有的SFTP用户。

<pre lang="BASH">
chown root.root /home/sftp /home/sftp/homepage /home/sftp/blog /home/sftp/pay
chmod 755 /home/sftp /home/sftp/homepage /home/sftp/blog /home/sftp/pay
</pre>

由于上面设置了目录的权限是755，因此所有非root用户都无法在目录中写入文件。我们需要在ChrootDirectory指定的目录下建立子目录，重新设置属主和权限。以homepage目录为例：

<pre lang="BASH">
mkdir /home/sftp/homepage/web
chown www.sftp /home/sftp/homepage/web
chmod 775 /home/sftp/homepage/web
</pre>

至此，我们已经实现了所有需要的功能。

<hr>
参考资料：
* <http://www.mike.org.cn/articles/centos-sftp-chroot/>
* <http://www.mike.org.cn/articles/centos-install-openssh/>
* <http://www.ctohome.com/FuWuQi/29/554.html>
* <http://rainbird.blog.51cto.com/211214/275162/>
* <http://www.debian-administration.org/articles/590>
