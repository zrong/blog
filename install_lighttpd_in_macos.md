[在 Mac OS X 上安装lighttpd](http://zengrong.net/post/2127.htm)

Install lighttpd in Mac OS X

在Windows上，我使用的是XAMPP套件。

Mac上我还没有安装HTTP服务器。我的VPS上使用的是lighttpd（[从Apache到Lighttpd][3]），因此在工作电脑上也希望使用它。

## 安装

<pre lang="shell">
-> % brew search lighttpd
lighttpd
-> % brew install lighttpd
</pre>

安装过程中，有几个重点需要提醒：<!--more-->

### 1. 下载失败

lighttpd 的源托管在 github 上，github 在国内访问并不稳定，多试几次或者拨vpn；

### 2. 安装后无法链接文档

安装成功后提示无法链接 `man` 文档，并要求重新执行 `brew link lighttpd` 。

这可能是由于你安装 `homebrew` 的时候，并没有使用 `root` 权限。执行下面的命令把你的 `brew` 的 `owner` 改为 `root`。

<pre lang="shell">
sudo chown root $(which brew)
</pre>

## 配置

配置文件默认在这个路径： `/usr/local/etc/lighttpd/lighttpd.conf`。

document root 默认在这里： `/usr/local/var/www/htdocs` 。

默认端口是 8080 ，如果希望使用 80 端口，则需要用 sudo 启动 lighttpd。

为了本地调试方便，我会在配置文件中加上这两个属性：

<pre lang="shell">
# 允许跟踪符号链接
server.follow-symlink= "enable"
# 目录中没有index文件时直接显示目录内容
server.dir-listing = "enable"
</pre>


## 启动和重新启动

lighttd安装后是不会自动启动的，但Mac又没有类似CenOS的 `service start lighttpd` 这种用法。

我们可以使用这条命令来简单测试：

<pre lang="shell">
lighttpd -Df /usr/local/etc/lighttpd/lighttpd.conf
</pre>

当然最好还是使用 Mac 提供的工具 `launchctl` 来启动：

<pre lang="shell">
ln -sfv /usr/local/opt/lighttpd/*.plist ~/Library/LaunchAgents
launchctl load ~/Library/LaunchAgents/homebrew.mxcl.lighttpd.plist
</pre>

`launchctl` 是一个与 `crontab` 类似的工具，它使用 plist 作为配置文件。详细介绍可以看这里：[launchctl][1] 和 [launchd][2] 。

有时候我们修改了conf之后，需要重启lighttpd使其生效，为了避免大量输入，我写了一个 `restarthttpd` 脚本放在bin中，内容如下：

<pre lang="shell">
launchctl unload ~/Library/LaunchAgents/homebrew.mxcl.lighttpd.plist
launchctl load ~/Library/LaunchAgents/homebrew.mxcl.lighttpd.plist
</pre>

然后可以测试一下：

<pre lang="shell">
ln -s ~/docs /usr/local/var/www/htdocs/docs
# 访问 http://localhost:8080/docs 试试看？
</pre>

## 没效果？

1. 检查配置文件是否出错：`lighttpd -tf /usr/local/etc/lighttpd/lighttpd.conf` ；
2. 是否配置了80端口但没有使用root用户运行？
3. 是否没有启动 lighttpd ？

[1]: https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man1/launchctl.1.html
[2]: https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man8/launchd.8.html
[3]: http://zengrong.net/post/1786.htm
