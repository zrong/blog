"=========== Meta ============
"StrID : 1691
"Title : vimpress使用解惑
"Cats  : 技术
"Status: publish
"Preview: http://zengrong.net/?p=1691
"Tags  : Python, vim, WordPress
"========== Content ==========
写了9年博客，尝试过多种博客写作工具，但一直没有持续用下去，原因是使用博客写作工具会弄乱HTML代码，另外一些插件的语法在这些写作工具中并不支持。

但WordPress提供的编辑器并不好用，这几年来我一直都是用Vim以<a href="http://daringfireball.net/projects/markdown/">MarkDown</a>格式写博客。写完后将内容粘贴到WordPress的在线编辑器中发布。

一直都知道有Vimpress这类插件，可以直接使用xmlrpc在Vim中发布博文，这几天终于付诸于实践，把它装上了。

在Vim的官方网站上，这类插件主要有下面几个：

<ul>
<li><a href="http://www.vim.org/scripts/script.php?script_id=1953">Vimpress</a>
这是最早的一个，但2007年就停止更新了；</li>
<li><a href="http://www.vim.org/scripts/script.php?script_id=3475">Vim Blog</a>
这个是在Vimpress的基础上进行修改的一个版本；</li>
<li><a href="http://www.vim.org/scripts/script.php?script_id=3510">VimRepress</a>
这个也是基于Vimpress的修改，但修改得更彻底，加入了许多功能；</li>
<li><a href="http://www.vim.org/scripts/script.php?script_id=2582">blogit.vim</a>
从帮助看，这个比VimRepress更强大，而且并不是基于Vimpress修改的。</li>
</ul>

这些插件都需要Python支持，如何让自己的Vim支持Python，可以看这篇文章：<a href="http://zengrong.net/post/1690.htm">不重新编译，让官方网站下载的Vim支持Python</a>

<!--more-->
我一一使用了上面的插件。VimRepress和blogit.vim我始终无法调试成功。不知道是不是配置错误。

我目前使用的，是<a href="http://www.vim.org/scripts/script.php?script_id=3475">Vim Blog</a>。虽然功能少点，但也足够用了。

使用方法在插件的源文件里面已经说的非常清楚了，相关文章在Google上一搜一堆，我这里不再介绍。

但是关于中文乱码的问题，网上的文章都没做过介绍。这里讲一下解决方案。

如果使用<code>:BlogList</code>得到的中文文章标题乱码，可以使用<code>set encoding=utf-8</code>来解决。这样设置后，可能会导致你的软件界面出现乱码，但这并不影响使用。写完博客之后，在使用<code>set encoding=chinese</code>把设置改回来就可以了。

如果希望了解Vim的编码选项(也就是弄懂上面为什么这么写)，可以看这篇文章：<a href="http://zengrong.net/post/1023.htm">VIM中与编码有关的选项</a>
