[在Eclipse中使用Vim](http://zengrong.net/post/1602.htm)

目前我知道的比较好用的，有3种方法：

1.[Vrapper](http://vrapper.sourceforge.net/)

建议使用<http://vrapper.sourceforge.net/update-site/unstable>来安装，虽然是不稳定版，但用起来感觉比稳定版还要稳定。 :wink:
vrapper的Bug不少，和中文输入法也会有一些冲突，但总之还是为我带了来效率的提升。
最困扰我的问题在于，Esc键经常会不起作用，由于Eclipse中经常会有多层次的代码提示，而按一次Esc键之后，只会消除一层代码提示。如果此时立即开始Vim编辑，则会将代码提示的内容自动加入到源码中，最后不得不一条条删除它们，这点很让然很烦躁。
注意：如果希望使用Ctrl+D快捷键实现翻页，就必须将Eclipse中的Ctrl+D屏蔽掉。因为Ctrl+D在Eclipse中是删除一行，如果你经常在Vim中Ctrl+D的话，你就杯具了……<!--more-->

2.[Eclim](http://www.eclim.org/)

这个就太强大了，它并不是在Eclipse中模仿Vim的习惯，而是直接把Vim嵌入到Eclipse中来。同样的，在Vim中也可以使用Eclipse中的代码提示等功能。
但是，如果你在Vim或者Eclipse中定义了相同的热键，这些热键会冲突，这又是一件纠结的事情，Eclipse中提高效率的就是热键，如果连热键都不能用了，那效率也太低了。
反过来说，在Vim中提供Eclipse的功能，我觉得没有什么必要。Vim有自已的一套方法，配置的好的话，甚至比Eclipse更好用。话说回来，如果只是开发JAVA的话，完全没有必要用Vim，Eclipse已经完美了。

3.[viplugin](http://www.viplugin.com/)

我从[paddy.w](http://paddy-w.iteye.com/blog/969366)看到这个插件。这是个收费插件，目前要15欧。我正在试用中，感觉比Vrapper要稳定。[paddy.w](http://paddy-w.iteye.com/blog/969366)也提供了注册的方法，大家可以去看看，不知道怎么弄的也可以联系我。
