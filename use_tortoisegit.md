[使用Git、Git GUI和TortoiseGit笔记](http://zengrong.net/post/1722.htm)

<span style="color:red;">2012-12-26更新</span>：在TortoiseGit中使用SSH host
<span style="color:red;">2012-12-30更新</span>：在安装的时候选择TortoiseGit使用的SSH客户端
<hr>

**注意：** 本文不讲解任何关于Git提交、合并等等使用细节和语法，只记录作者在使用Git相关工具中碰到的问题和选择的经验。本文只是个人意见的集中，不代表适合所有人。如果你是 “被惯坏了的那批”，请不要介意。:-)

### 关于命令行

我一直建议在命令行中使用Git或者SVN。因为这样可能更加了解他们的工作方式，也不容易遗漏重要的问题和提醒。

在Windows习惯的驱使下，大多数人是不会看弹出的对话框中有什么信息的，一般都是直接关掉。但是，版本库给我们的提示信息都是非常重要的，有的是冲突，有的是提交失败，等等，这些都被略过了。

我碰到的关于版本库使用问题主要包括下面这些：

* 没有获取到最新版本就编译程序  
出现这个问题的原因，主要是忽略了文件的冲突。有的是从不看版本库给的提示，有的是太依赖Windows资源管理器中指示冲突的图标覆盖。众所周知，Windows系统的图标缓存一直都有那么点问题。
* 用删除文件的方式解决冲突  
许多程序猿并不知道如何解决冲突，也看不懂版本库在文件中加入的解决冲突的提示。
* 用删除文件代替revert  
至于为什么大家都这么用，我还搞不懂……
* 强行覆盖提交  
碰到冲突后，备份自己修改的文件，然后恢复版本库中最新文件，再用自己的文件覆盖版本库中的文件然后提交。 *哥哥诶～～你干的好事！*

其实如果在命令行中使用Git或者SVN，以上的问题应该都不会存在。因为命令行会事无巨细的给我们提示，尤其是Git的命令行，会非常聪明的猜测我们的意图并给我们提示。
使用者要正确的使用命令行，就必须去仔细阅读版本库的文档。这样就能进一步了解版本库的工作原理，减少在使用中的错误。

另外，Git的很多功能，尤其是高级功能，只有命令行能实现。

但并非所有程序猿都愿意使用命令行工具，尤其是被Windows惯坏了的那批。

所以，有了TortoiseSVN和TortoiseGit。

### Git GUI

Git自带GUI界面。使用 `git gui` 命令可以打开它。在这个界面中可以完成commit、merge、push、pull等等常用操作。

![gitgui](/wp-content/uploads/2012/11/gitgui.png)

使用 `gitk` 可以打开查看Git版本库历史，在 `git gui` 中也有菜单可以打开它。

![gitk](/wp-content/uploads/2012/11/gitk.png)

个人以为，完全可以不用安装TortoiseGit，对于绝大多数程序猿来说，这个界面已经足够了。

但是，和“关于命令行”中说的那句话一样，并非所有的程序猿都愿意使用这个 **界面简陋到丑陋** 的工具，尤其是被TortoiseSVN惯坏了的那批。

那些从SVN转换过来的程序猿，绝大多数都只用过TortoisSVN。那么好吧，就让界面、名字都完全一样的TortoiseGit登场吧！

### 安装TortoiseGit

#### TortoiseGit没有集成Git

在[TortoiseGit](http://code.google.com/p/tortoisegit/)官方网站可以下载到它。有32bit和64bit版本，同时也有中文语言包（但我不建议你安装）。

安装完毕之后，如果你没有安装过Git，那么还需要去下载[msysGit](http://msysgit.github.com/)来安装。因为TortoiseGit其实只是一个壳，它需要调用Git命令行才能发挥作用。（现在你知道我为什么推荐你用命令行了么？）

如果你不安装msysGit，那么在运行TortoiseGit的时候会弹出这个提示：

![need_git](/wp-content/uploads/2012/11/need_git.png)

为什么TortoiseGit不像TortoiseSVN一样，把SVN命令行工具集成在安装包中呢？我猜想是以下几点原因：

* Git官方从未出过Windows版本二进制包；
* msysGit和TortoiseGit是两个不同的团队开发的；
* msysGit和TortoiseGit的更新周期差异较大；
* TortoiseGit团队希望安装包更小；
* TortoiseGit团队给用户更灵活的选择Git版本的权利。

#### Git for Windows VS msysGit

[msysGit](http://msysgit.github.com/)的主页提供了两个项目：Git for Windows和msysGit，并写明了它们的详细区别。
个人认为，Git for Windows适合绝大多数程序猿（又见绝大多数 :D）。所以，强烈建议安装Git for Window。
msysGit使用一种很BT也很NB的方式来安装。先安装一个最小的[MinGW/MSYS](http://www.mingw.org/)系统，然后使用git `pull` 所有的源码，调用gcc在本地编译成可执行文件。

#### Cygwin

如果本机安装过[Cygwin](http://zengrong.net/post/tag/Cygwin)，那么在安装msysGit的时候，cygwin的bin目录不能位于PATH环境变量中，否则msysGit会拒绝安装。
其实，如果你不在意Cygwin提供的Git版本比较老，你完全可以不安装Git for Windows或者msysGit，直接在TortoiseGit中设置Git.exe的路径为Cygwin的bin目录即可。

![gitpath](/wp-content/uploads/2012/11/gitexepath.png)

由于Cygwin目前的Git版本较老，在运行TortoiseGit的时候你会得到这个提示：

![gitold](/wp-content/uploads/2012/11/git1710.png)

关于Cygwin、MinGW以及msysGit的关系和选择，可以看这篇文章：[Cygwin与MinGW，如何选择？](http://zengrong.net/post/1557.htm)
还有这篇转载的文章：[Msys/MinGW与Cygwin/gcc](http://zengrong.net/post/1723.htm)

### TortoiseGit的密钥

<del>我认为TortoiseGit最大的问题，就是在于它使用ppk密钥格式，而不是使用OpenSSH密钥格式。

因为linux系统是默认使用OpenSSH的，所以Git在基于命令行的时候是使用OpenSSH格式的密钥。
同理，[gitolite](http://zengrong.net/post/1720.htm)这种服务器端程序使用的是OpenSSH格式的密钥。
所以，必须将原有的OpenSSH密钥转换成PPK密钥才能在TortoiseGit中使用。</del>

在安装TortoiseGit的时候，你可以选择使用Putty还是OpenSSH作为SSH客户端。安装程序中说，Putty和Windows配合得更好。

![gitold](/wp-content/uploads/2012/11/choose_ssh_client.png)

如何选择？我分别给出它们的特点：

**Putty**

1. Putty有GUI界面，可以通过[配置sessions来访问不同的git服务器端口](http://zengrong.net/post/1775.htm)；
2. Putty有GUI程序(Putty Key Generator)来生成密钥；
3. 如果使用Putty作为SSH客户端，那么传输速度可能会比较慢（个人感觉，当然也[有人和我有一样的感觉](http://www.iteye.com/topic/1124117)）；
4. Putty不能直接使用原有的OpenSSH密钥，必须将其转换成PPK密钥才行。

**OpenSSH**

1. OpenSSH是Git命令行程序默认使用的SSH客户端程序；
2. Git for Windows默认就包含了OpenSSH程序；
3. 你可以利用已有的OpenSSH密钥，不用做转换（例如我原来用cygwin的时候积累了一堆OpenSSH密钥，现在只需要在~/.ssh下做一个符号链接就能用了）；
4. GitHub/bitbucket等Host使用的都是OpenSSH密钥；
5. 大多数Linux发行版默认使用OpenSSH作为服务端；
6. 你可以方便的使用命令行程序来实现自动化处理。

看完上面的特点，如果你还是选择了Putty作为客户端的话，那么需要转换原有的OpenSSH密钥（如果有的话）；
如果你依然义无反顾选择了OpenSSH作为客户端的话，我相信你已经知道如何生成、修改、配置SSH了，看来我也不必罗嗦 :D

#### 转换OpenSSH密钥到ppk格式

可以使用TortoiseGit自带的Putty Key Generator来转换原来的OpenSSH密钥到ppk格式。

打开该程序，选择 `Conversions->Import Key` 命令将OpenSSH **私钥** 导入界面中，然后点击 `Save private key` 按钮将密钥保存成ppk格式。建议在 `Key comment` 中输入说明，否则密钥多了很难分辨。至于密码，为了方便可以不设置。

![putty_key_generator](/wp-content/uploads/2012/11/putty_key_generator.png)

#### 生成OpenSSH和ppk格式的密钥

为了同时支持服务端和客户端，我们可以在生成一个密钥的时候，同时生成该密钥的ppk格式和OpenSSH格式。而每个密钥对都包含 **公钥** 和 **私钥**，两对一共是4个文件。这样就可以满足所有情况了。

打开Putty Key Generator，选择 `Generator` 按钮，晃动鼠标生成一个密钥，然后这样处理：

* 点击 `Save private key` 按钮将密钥保存成 **ppk格式私钥**；
* 点击 `Save public key` 按钮将密钥保存成 **ppk格式公钥**；
* 点击 `Conversions->Export OpenSSH Key` 按钮将密钥保存成 **OpenSSH格式私钥**；
* 获取上图红框中的所有文本内容，粘贴到文本编辑软件中，保存为一个单行的文件，这就是 **OpenSSH格式公钥**；

#### 在TortoiseGit中使用SSH host

如果使用Putty作为TortoiseGit的SSH客户端，那么就不能使用OpenSSH的 ~/.ssh/config 来定义使用不同的端口和密钥访问SSH，而是需要使用 PuTTY Session。这篇文章进行了详细讲解：http://zengrong.net/post/1775.htm

### 换行符的问题 autocrlf and safecrlf

Windows(\r\n)、Linux(\n)和MacOS(\r)三个主流系统的换行符各不相同，这样在跨平台合作的时候就容易出现换行符的问题。

Git提供了 `autocrlf` 和 `safecrlf` 两个参数来解决这个问题。但这两个参数如果没用好，就会影响开发。

例如，出现这种情况：

A和B两个开发人员，A使用LF(\n)做换行符，B使用CRLF(\r\n)做换行符，且都没有开启 `autocrlf` 参数，那么A在迁出B的文件，并使用自己的编辑器打开之后就会发现，虽然没有对文件做任何修改，但它的状态是modified。这是由于A的编辑器自动将B的文件中的所有换行符替换成了(LF)，这与版本库中的(CRLF)不同。

让我们来看看 `autocrlf` 参数的作用：

<pre lang="BASH">
# 签出时将换行符转换成CRLF，签入时转换回 LF。
git config --global core.autocrlf true

#签出时不转换换行符，签入时转换回 LF
git config --global core.autocrlf input

#签出签入均不转换
git config --global core.autocrlf false
</pre>

这些选项在TorgoiseGit中也可以设置。

我的建议是在无论在什么系统下编程，都把所有人的编辑器的换行符模式设置成Unix格式，然后把autocrlf设置成false，这样一劳永逸。
毕竟除了Windows记事本这类软件外，已经很少有文本编辑器不支持换行符设置了。

如果你把换行符搞乱了，在一个文件中既包含windows风格的换行符也包含unix风格换行符，那么 `safecrlf` 就可以发挥作用了：

<pre lang="BASH">
# 拒绝提交包含混合换行符的文件
git config --global core.safecrlf true

# 允许提交包含混合换行符的文件
git config --global core.safecrlf false 

# 提交包含混合换行符的文件时候给出警示
git config --global core.safecrlf warn
</pre>

### 文件权限问题 755 and 664

我在Cygwin下以命令行的形式使用Git，同时也使用TortoiseGit。
在使用TortoiseGit签出使用cygwin提交的项目时，发现所有的文件权限都改变了：

<pre lang="BASH">
$ git diff 
diff --git a/launch4j/spritesheet_conterver.xml b/launch4j/spritesheet_conterver.xml
old mode 100755
new mode 100644
</pre>

这是因为msysgit是一个类Unix模拟器，需要拥有Unix形式的文件访问权限。而由于Windows的种种限制，信息不能复原，从而导致原来的755成644了。

解决方法：

<pre lang="BASH">
git config --global core.filemode false
git config core.filemode false
</pre>

这个选择的在TortoiseGit中没有界面来设置，只能用命令行或者手动修改git配置文件。

### 文章参考

* <http://blog.csdn.net/dbzhang800/article/details/6426834>
* <http://ycyuxin.blog.hexun.com/37440972_d.html>
* <http://stackoverflow.com/questions/4181870/git-on-windows-what-do-the-crlf-settings-mean>
* <http://www.360doc.com/content/11/0117/18/2036337_87178762.shtml>
