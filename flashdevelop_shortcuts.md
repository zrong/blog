[FlashDevelop的快捷键设置](http://zengrong.net/post/1694.htm)
要高效的使用一个软件，首先需要了解它的快捷键。

我准备深入使用一下FlashDevelop(以下简称FD)，却发现它的快捷键完全与Flash Builder不同。

这让我觉得很不可思议。是有意为之，还是无心之过？

或许这是开源软件的一个不成文的规定？比如 <a href="http://www.gimp.org">GIMP</a> 就和PhotoShop的快捷键完全不同。这可能是为了规避版权风险也未可知。

那么，怎样设置FD的快捷键呢？<!--more-->

在Tools->Keyboard Shortcuts菜单的界面中，可以显示当前的快捷键。但是这个界面只能显示，不能设置。

如果需要设置FD菜单中的快捷键，需要手动编辑<code>FD安装目录/Settings/MainMenu.xml</code>这个文件。这显得略有不便。但是对于FD的使用者来说，这应该不是太大的问题。

但是，前面我特别提到，这个文件只能修改<code>FD标准菜单</code>中的快捷键。部分使用插件实现的功能的快捷键，在这里无法设置。

例如，<code>Search->Find All References</code>这个功能，在MainMenu.xml中就找不到。

因为这个功能是使用插件<code>CodeRefactor</code>来实现的，而对于这类使用插件实现的功能，必须在插件设置界面中来设置快捷键。

遗憾的是，<code>CodeRefactor</code>插件并没有提供快捷键设置功能。

`Find All References`功能对应在Flash Builder中的快捷键是`Ctrl+Shift+G`。这是个非常常用的功能，方便在所有的源码中搜索到一个方法或者变量的引用。如果必须用菜单来操作的话，易用性就大打折扣了。

还有一个常用的快捷键在FD中无法设置：`alt+/`。这个快捷键用来展开自动完成列表。

幸运的是，FlashDevelop爱好者群(257978195)的Freedom修改了`CodeRefactor`和`ASCompletion`两个插件，让它们可以支持快捷键设置。

将这两个插件下载后覆盖到`FD安装目录/Plugins`目录覆盖同名文件，然后重启FD，在`Tools->Program Settings`中找到对应的插件设置快捷键即可。

需要注意的是，这些快捷键必须设置成2键，如果设置成3键将没有效果。
