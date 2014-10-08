[Python 虚拟环境](http://zengrong.net/post/2167.htm)

python virtual enviorments

为了解决包依赖、安装权限和 python 版本问题，程序员们制造了许多工具。我把它们做一个汇总，便于查找。

这里介绍的工具都是当前流行的，不会包含已经不再维护的工具。<!--more-->

## virtualenv

[virtualenv][2] 是目前最流行的 python 虚拟环境配置工具。它不仅同时支持 python2 和 python3，而且可以为每个虚拟环境指定 python 解释器，并选择不继承基础版本的包。

## virtualenvwrapper

顾名思义，[virtualenvwrapper][6] 是对 [virtualenv][2] 的一个封装，目的是使后者更好用。但由于它基于 shell 开发，在 Windows 系统上，不能使用标准版本，而应使用针对 Windows batch shell 的 [virtualenvwrapper-win][7]。

关于为什么使用 shell 脚本开发，作者专门 [进行了解释][9] 。

virtualenvwrapper 还有针对 vim 用户和 emacs 用户的 [扩展][8] 。

## venv

Python 从3.3 版本开始，自带了一个虚拟环境 [venv][1]，在 [PEP-405][3] 中可以看到它的详细介绍。它的很多操作都和 virtualenv 类似。

因为是从 3.3 版本开始自带的，这个工具也仅仅支持 python 3.3 和以后版本。所以，要在 python2 上使用虚拟环境，依然要利用 [virtualenv][2] 。

在 *nix 系统上，可以直接执行 `pyvenv /path/to/new/virtual/enviorment` 来创建一个虚拟环境，在 Windows 系统上，则可以使用 `python -m venv myenv` 来创建。

## pyenv

我们可以用许多方法让不同的 Python 版本在系统上共存。

例如在 OS X 上，如果使用官方提供的 DMG 版本安装，那么自带的 python2 和新安装的 python3 是可以共存的。python3 可以使用 `python3` 来调用，甚至 `pip` 都可以使用 `pip3` 来调用。

但如果还有其它小版本需要共存么？我要记忆多少命令呢？

[pyenv][5] 用来解决这类问题。它可以安装、卸载、编译、管理多个 python 版本，并随时将其中一个设置为工作环境。

将 pyenv 和 virtual enviorment 结合使用，可以完美解决 python 多版本环境的问题。

[1]: https://docs.python.org/3/library/venv.html
[2]: http://www.virtualenv.org/
[3]: http://legacy.python.org/dev/peps/pep-0405/
[5]: https://github.com/yyuu/pyenv
[6]: https://bitbucket.org/dhellmann/virtualenvwrapper
[7]: https://pypi.python.org/pypi/virtualenvwrapper-win
[8]: http://virtualenvwrapper.readthedocs.org/en/latest/extensions.html
[9]: http://virtualenvwrapper.readthedocs.org/en/latest/design.html
