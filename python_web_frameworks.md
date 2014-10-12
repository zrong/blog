[Python web框架的选择](http://zengrong.net/post/2172.htm)

python web frameworks

## 一、缘起网站

大约十多年前（1998年），我做了人生中的第一个网站。那是用的语言是 [ASP][2]，工具是 [FrontPage][3]。

后来（2000~2004年），我做了一段时间网站开发，负责前端到后端、美术到产品的所有内容，使用的语言是 [ASP][2] 和 [PHP][4]，工具是 [Macromedia][6] [Dreamweaver][5] 和 [Editplus][7]。

那时，我已经开始手写 CSS 和 HTML，并使用 `<DIV>` 重构网站了。

再后来，我就没有继续做网站了。

现在，因为众所周知的原因，我必须捡起这个老本行。由于一直都不太喜欢 PHP，我在考虑选择一个 Python Web 框架。<!--more-->

## 二、百花齐放的 Python Web 框架

这里有一个 [不完全的列表][8] 展示了一些 Python Web 框架。我关心的主要是下面几个：

* [Django][31]
* [web.py][34]
* [Tornade][33]
* [Bottle][35]
* [Flask][32]

## 三、相关对比

* [浅谈Python web框架][1]
* [web.py更面向对象，flask更面向过程][10]
* [Python Web 框架哪个入门快？Django、Tornado、web.py？][11]
* [初学web框架，选哪一个好呢？][12]
* [web开发框架的选择(bottle or flask)及为autumn增加多线程支持][13]
* [bottle 和 flask][15]
* [Which is better: Flask vs web.py? Why?][9]
* [Python Flask vs Bottle][14]
* [Bottle vs Flask, who will win?][16]

## 四、我的选择

根据上面的对比，我对这些框架的大致了解如下：

Django 是一个一站式解决方案，提供了所有web开发者需要的东西。它有相对封闭的环境和耦合较紧密的系统，同时提供一个管理员后台。但由于功能全面，学习起来可能需要花费较多的时间。但也是由于功能全面，对于不愿意费劲折腾的人来说，应该是更容易使用。文档方面，Django 做得非常优秀。

web.py 的原作者好像已经出走？Tornade 算是 web.py 的继任者和加强版，同时它还是个服务器。但文档方面貌似比较缺乏。

Bottle 是和 web.py 类似的微型框架，它的设计更加简洁合理，且只有一个 3K 行的 py 文件，可支持多种模板和服务器。文档也足够完善。

Flask 也是微型框架，在使用上和 Bottle 很像。但Flask 是 [Pocoo][17] 团队的作品，在使用上应该更有保障。文档丰富，且有中译本。

**由于我比较爱折腾，所以选择 [Flask][32]。**

[1]: http://feilong.me/2011/01/talk-about-python-web-framework
[2]: http://zh.wikipedia.org/wiki/Active_Server_Pages
[3]: http://zh.wikipedia.org/wiki/Microsoft_FrontPage
[4]: http://zh.wikipedia.org/wiki/PHP
[5]: http://zh.wikipedia.org/wiki/Adobe_Dreamweaver
[6]: http://zh.wikipedia.org/wiki/Macromedia
[7]: http://www.editplus.com/
[8]: wiki.python.org/moin/WebFrameworks
[9]: http://www.quora.com/Which-is-better-Flask-vs-web-py-Why
[10]: http://www.douban.com/group/topic/12998784/
[11]: http://www.oschina.net/question/730461_110905
[12]: http://www.v2ex.com/t/13137
[13]: http://www.vimer.cn/2012/02/web%E5%BC%80%E5%8F%91%E6%A1%86%E6%9E%B6%E7%9A%84%E9%80%89%E6%8B%A9bottle-or-flask%E5%8F%8A%E4%B8%BAautumn%E5%A2%9E%E5%8A%A0%E5%A4%9A%E7%BA%BF%E7%A8%8B%E6%94%AF%E6%8C%81.html
[14]: http://stackoverflow.com/questions/4941145/python-flask-vs-bottle
[15]: http://www.douban.com/group/topic/28666723/
[16]: https://news.ycombinator.com/item?id=4027351
[17]: http://www.pocoo.org/

[31]: http://www.djangoproject.com
[32]: http://flask.pocoo.org/
[33]: http://www.tornadoweb.org
[34]: http://webpy.org/
[35]: http://bottlepy.org
