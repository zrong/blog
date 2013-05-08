[安装gitolite](http://zengrong.net/post/1720.htm)

git默认使用SSH协议，在服务器上基本上不用怎么配置就能直接使用。但是如果面向团队服务，需要控制权限的话，还是用gitolite方便些。

本文的大部分内容来自 <https://github.com/sitaramc/gitolite> ，但并不是翻译。

本文面向的版本是gitolite v3；所有的操作基于命令行；服务器为CentOS 6.2 x86_64；客户端使用cygwin。

### gitolite vs gitosis

为什么不用gitosis呢？原因很简单，它已经好几年没有更新了。
gitolite原本是作为gitosis的lite版本出现的，可是现在的功能甚至已经超过gitosis了。
关于gitolite和gitosis的更详细信息，可以看看下面几篇文章：

* [使用gitosis来配置管理git服务器端](http://blog.prosight.me/index.php/2009/07/271)
* [Gitolite and Gitosis in a Nutshell](http://saito.im/note/Gitolite-and-Gitosis-in-a-Nutshell/)
* [从 Gitosis 迁移到 Gitolite](http://hansay.com/2012/07/05/migrating-gitosis-to-gitolite-for-ubuntu-12-dot-04/)
* [Gitolite 2.2 安裝筆記](http://blog.crboy.net/2012/06/gitolite-22-installation.html)

### 系统需求

* 类unix操作系统
* sh
* git 1.6.6+
	* [Installing git on centos 6](http://www.miketmoore.com/blog/2012/02/26/installing-git-on-centos-6/)
	* [Git 1.7.10.2 on CentOS 5.6](http://www.webtatic.com/packages/git17/)
* perl 5.8.8+
* openssh 5.0+
* 一个git用户
* 一个openssh公钥

### 安装

* 登录到git用户。如果没有给git用户设置密码，可以从root用户通过su切换过去。
* 确认 `~/.ssh/authorized_keys` 不存在
* 将公钥放在 `~/YourName.pub`
* 运行下面的命令：
<pre lang="BASH">
# 获取版本库
git clone git://github.com/sitaramc/gitolite
# 创建bin目录，用于存放安装后的文件
mkdir -p ~/bin
# 将gitolite安装到bin目录
gitolite/install -to ~/bin
# 使用YourName.pub公钥初始化版本库
gitolite setup -pk YourName.pub
</pre>

### 管理用户和版本库

不应该手动在服务器端加入新的用户或者版本库。
gitolite使用一个特殊的版本库 `gitolite-admin` 来管理员用户和版本库，只要在这个版本库中修改并 `push`，服务器就会自动根据配置作出修改。

首先在客户端迁出版本库：

<pre lang="BASH">git clone git@host:gitolite-admin</pre>

如果在迁出的过程中询问密码，那么说明配置出了问题。一般情况是密钥配置错误。可以检查客户端的 `~/.ssh` 下有没有 YourName 私钥。如果需要使用不同的密钥连接多个ssh服务器，可以编辑 `~/.ssh/config` 进行配置。

进入 `gitolite-admin` 目录，其中的 `keydir` 目录是用来放置用户公钥的，而 `conf/gitolite.conf` 则是用来配置用户和版本库。

编辑 `conf/gitolite.conf`如下：

<pre>
repo foo
	RW+         =   alice
	RW          =   bob
	R           =   carol
</pre>

上面的配置的含义是：

* 有一个名为 `foo` 的版本库；
* 用户 `alice` 对它有读、写、删除权限；
* 用户 `bob` 对它有读写权限；
* 用户 `carol` 对它仅有只读权限。
* 
另外，需要找 `alice/bob/carol` 用户索要他们的公钥，保存在 `keydir` 目录中，命名为 `alice.pub/bob.pub/carol.pub`，然后提交这些改动， `push` 到服务器。

服务器会自动将公钥加入到 `~/.ssh/authorized_keys` 中，并创建 `foo` 版本库。

`foo` 版本库的访问地址为 `git@host:foo`。

如果希望把 `foo` 版本库放在 `bar` 目录下，可以这样编辑配置文件：

<pre>
repo bar/foo
	RW+         =   alice
	RW          =   bob
	R           =   carol
</pre>

此时`foo` 版本库的访问地址为 `git@host:bar/foo`。

### 更多内容

* <https://github.com/sitaramc/gitolite>
* <http://sitaramc.github.com/gitolite/master-toc.html>
* <https://github.com/sitaramc/gitolite/wiki>

