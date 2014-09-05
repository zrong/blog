[Redmine安装过程疑难杂症](http://zengrong.net/post/1936.htm)

Redmine diagnoses on installations.

**2014-09-05 更新：**增加一些疑难杂症。

Redmine的安装，看 [RedmineInstall][install] 就可以搞定。但由于我对Ruby不熟悉，还是碰到了一些问题，下面是个记录。

2014-09-05，进行了一次服务器搬迁，将原来位于香港的服务器搬回内地机房，redmine也要搬过来。因此增加了一些记录。

## 安装平台的选择

Redmine 明确标注了可以使用哪几个版本的 Ruby 。但并没有说哪个版本比较好。我的感受是 1.9.3 好像比较靠谱。

* Ubuntu 12.04 LTS/CentOS 6.3
* Ruby 2.0.0/Ruby 1.9.3
* Redmine 2.3.3

## Ruby on Rails安装

[如何使用RVM在Ubuntu 12.04 LTS上安装Ruby on Rails][rvm]

## gem --version

如果在使用gem的时候碰到这样的提示：

<pre lang="bash">
gem --version
# /usr/local/lib/ruby/1.9.1/yaml.rb:84:in `<top (required)>':
# It seems your ruby installation is missing psych (for YAML output).
# To eliminate this warning, please install libyaml and reinstall your ruby.
</pre>

这是在编译安装 ruby 的时候没有先安装 libyaml 所致。但是，即使是你安装 libyaml 之后重新安装 ruby ，这个问题还是不能解决。

正确的方法，是安装 libyam-devel 库。下面是在 CentOS 6.3 上安装：

<pre lang="bash">
yum install libyaml-devel
</pre>

然后，找到你先前编译 ruby 的目录，进入 `ext/psych/` 文件夹，执行：

<pre lang="bash">
ruby extconf.rb make make install
# checking for yaml.h... yes
# checking for yaml_get_version() in -lyaml... yes
# creating Makefile
</pre>

然后再执行一次 `make install` 。如果你已经 clean 了原来的编译内容，那么则需要重新编译。

<pre lang="bash">
make install
# compiling to_ruby.c
# compiling parser.c
# compiling psych.c
# compiling emitter.c
# compiling yaml_tree.c
# linking shared-object psych.so
# /usr/bin/install -c -m 0755 psych.so /usr/local/lib/ruby/site_ruby/1.9.1/x86_64-linux
# installing default psych libraries
</pre>

再次执行 `gem -v` ，发现 warning 已经消失了。

## bundle install

**如果碰到 mysql2 问题，就像这样：** <!--more-->

>Installing mysql2 (0.3.11) with native extensions 
>Gem::Installer::ExtensionBuildError: ERROR: Failed to build gem native extension.
>        /Users/rarneson/.rvm/rubies/ruby-1.9.3-p125/bin/ruby extconf.rb 
>checking for rb_thread_blocking_region()... yes
>checking for rb_wait_for_single_fd()... yes
>checking for mysql_query() in -lmysqlclient... no
>checking for main() in -lm... yes
>checking for mysql_query() in -lmysqlclient... no
>checking for main() in -lz... yes
>checking for mysql_query() in -lmysqlclient... no
>checking for main() in -lsocket... no
>checking for mysql_query() in -lmysqlclient... no
>checking for main() in -lnsl... no
>checking for mysql_query() in -lmysqlclient... no
>checking for main() in -lmygcc... no
>checking for mysql_query() in -lmysqlclient... no
>*** extconf.rb failed ***

安装这几个包以解决 mysql2 问题：

<pre lang="bash">
apt-get install mysql-client libmysqlclient-dev
</pre>

**如果碰到 pg 问题，就像这样：**

>Installing pg (0.17.0)
>Gem::Installer::ExtensionBuildError: ERROR: Failed to build gem native extension.
>    /usr/local/rvm/rubies/ruby-2.0.0-p247/bin/ruby extconf.rb
>checking for pg_config... no
>No pg_config... trying anyway. If building fails, please try again with
> --with-pg-config=/path/to/pg_config
>checking for libpq-fe.h... no
>Can't find the 'libpq-fe.h header
>*** extconf.rb failed ***

安装这个包（我没拼错，就是libpq，不是libpg）：
<pre lang="bash">
apt-get install libpq-dev
</pre>

**如果碰到 rmagick 问题，就像这样：**

>Installing rmagick (2.13.2)
>Gem::Installer::ExtensionBuildError: ERROR: Failed to build gem native extension.
>    /usr/local/rvm/rubies/ruby-2.0.0-p247/bin/ruby extconf.rb
>checking for Ruby version >= 1.8.5... yes
>checking for gcc... yes
>checking for Magick-config... no
>Can't install RMagick 2.13.2. Can't find Magick-config in /usr/local/rvm/gems/ruby-2.0.0-p247/bin:/usr/local/rvm/gems/ruby-2.0.0-p247@global/bin:/usr/local/rvm/rubies/ruby-2.0.0-p247/bin:/usr/local/rvm/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games
>*** extconf.rb failed ***

安装这个几个包解决它：
<pre lang="bash">
apt-get install imagemagick libmagickwand-dev
</pre>

**碰到上面两个问题，也可以不必安装相关的库，而是在安装的时候忽略它们：**

<pre lang="bash">
bundle install --without postgresql rmagick
</pre>

如果上面的代码不管用，可能是在配置文件中指定了它们。你可以打开 `config/database.yml` 中有相关配置，例如我的：

<pre lang="yml">
#test_pgsql:
#  adapter: postgresql
#  database: redmine_test
#  host: localhost
#  username: postgres
#  password: "postgres"
#
#test_sqlite3:
#  adapter: sqlite3
#  database: db/test.sqlite3
</pre>

那么，可以同样忽略它们： `--without test_pgsql test_sqlite3` 。我的方法更简单粗暴（像上面），就是注释它们。

**如果使用ruby 1.8.7，安装 redcarpet 出错**

默认安装的redcarpet是3.0，如果出错可以选择安装2.0版本：
<pre lang="bash">
gem install redcarpet -v 2.0
</pre>

## 使用测试服务器正常，但 Apache 不能访问

你使用下面的代码，可以在 `http://localhost:3000/` 正常访问 redmine.

<pre lang="bash">
ruby script/rails server webrick -e production
</pre>

但是，你使用 Apache 却不行，这一般是因为你被 SELinux 给禁止了。

例如我在 CentOS 6.3 下碰到的情况是：

<pre>
8084 type=AVC msg=audit(1409905240.973:788834): avc:  denied  { execute_no_trans } for  pid=27260 comm="httpd" path="/usr/local/l     ib/ruby/gems/1.9.1/gems/passenger-4.0.50/buildout/agents/PassengerWatchdog" dev=dm-0 ino=1578438 scontext=unconfined_u:syste     m_r:httpd_t:s0 tcontext=unconfined_u:object_r:lib_t:s0 tclass=file
</pre>

这些 log 可以在 `/var/log/audit/audit.log` 中查到。

最简单的方法是禁用 SELinux ，执行 `setenforce 0` 在系统运行状态取消，这样不必重启系统。

然后编辑 `/etc/sysconfig/selinux` 保证系统重启后也处于禁用状态：

<pre>
# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
#SELINUX=enforcing
SELINUX=disabled
# SELINUXTYPE= can take one of these two values:
#     targeted - Targeted processes are protected,
#     mls - Multi Level Security protection.
SELINUXTYPE=targeted
</pre>

然后重启 Apache 即可生效。

当然，如果愿意折腾 SELinux（毕竟比较安全） ，那么可以安装 audit2allow 来允许模块通过。

在 CentOS 上找一下这个模块在哪里：

<pre>
yum provides \*/audit2allow
</pre>

在 CentOS 上安装 audit2allow ：

<pre>
yum install policycoreutils-python
</pre>

然后，参考下面的文章自己折腾吧！

* [SELinux 的 audit2allow 工具程序][2]
* [selinux阻止服务器启动解决方法(需要安装audit2allow) ][3]
* [利用 audit2allow 创建自定 SELinux 政策模块][4]
* [Redmine Error: Phusion Passenger Watchdog Failed to Start][6]

## 进入 Administration-Settings 报 HTTP 500 错误

我将 redmine 整体从另一台服务器搬迁过来之后，终于配置成功。进入后台正常，但进入管理员的设置界面则出现下面的提示：

	Internal error

	An error occurred on the page you were trying to access.
	If you continue to experience problems please contact your Redmine administrator for assistance.

	If you are the Redmine administrator, check your log files for details about the error.

解决方法：

查看 redmine 的 `tmp/cache` 目录，查看目录结构应该如下所示：

<pre lang="bash">
[root@localhost redmine]# tree tmp/cache
tmp/cache
└── 900
    └── 0F0
        └── i18n%2Flanguages_options
</pre>

停止 redmine，然后删除 `tmp/cache` 目录下的所有文件，再启动 redmine 。

然后 管理员设置界面 Administration-Settings 就可以进入了。

这时查看 `tmp/cache` 目录结构，会发现先前删除的文件和文件夹自动被创建了。

## 参考

* [SELinux permission denied to Phusion Passenger for redmine][1]
* [Wang Zhe Blog][5]
* [How do I install Ruby with libyaml on Ubuntu 11.10?][7]
* [Install Ruby 1.9.3 with libyaml on CentOS][8]
* [Internal Error 500 on "settings"][9]


[rvm]: http://zengrong.net/post/1933.htm
[install]: http://www.redmine.org/projects/redmine/wiki/RedmineInstall
[1]: http://stackoverflow.com/questions/19400980/selinux-permission-denied-to-phusion-passenger-for-redmine
[2]: http://linux.chinaunix.net/techdoc/system/2008/06/01/1008504.shtml
[3]: http://blog.chinaunix.net/uid-12087380-id-3074698.html
[4]: http://www.uddtm.com/os/centos/1013.html
[5]: http://wangzhe.me/tags/redmine
[6]: http://www.tuicool.com/articles/goto?id=aiqa6bb
[7]: http://stackoverflow.com/questions/8410885/how-do-i-install-ruby-with-libyaml-on-ubuntu-11-10
[8]: http://collectiveidea.com/blog/archives/2011/10/31/install-ruby-193-with-libyaml-on-centos/
[9]: http://www.redmine.org/issues/12861
