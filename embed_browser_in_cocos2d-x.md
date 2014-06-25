[在 cocos2d-x 中嵌入浏览器](http://zengrong.net/post/2123.htm)

Embeds a browser in cocos2d-x

在游戏中嵌入网页是很常见的需求，cocos2d-x 引擎官方并没有提供这个功能。

我在网上转了一圈，把找到的资料做了一些修改，将其集成到我们使用的 [quick-cocos2d-x][1] 引擎中。

主要代码来自：[CCXWebview][2]，[这里][3] 还有一篇专门讲解Android嵌入浏览器的文章，可以参考。

集成的类叫做 CCWebView，位于 extensions 之中。

效果如下：<!--more-->

![CCWebView in ios simulator][10]

## 做什么？

在游戏中，我们需要显示系统公告，或者制作一些需要复杂图文混排的界面，这些东西如果用 cocos2d-x 来做，未免太过麻烦。嵌入一个网页就简单的多。

现在的修改能满足这样一些简单的使用：

* 显示一个指定地址的网页，设定网页的大小和位置；
* 更新一个已经显示的网页的内容；
* 关闭已经显示的网页。

然后，就没有了。因为目前的项目不需要和浏览器交互，所以希望用 CCWebView 来实现一个商城的话可能会比较难办，要做一些扩展。

在 Android 中，浏览器与 Game 并不在一个线程，因此也没有提供把让cocos2d-x 来控制增加浏览器的关闭按钮之类的功能。如果要实现这些，最好的方法是浏览器不做全屏，然后用cocos2d-x实现一些按钮放在浏览器之上，点击按钮调用 CCWebView 的关闭函数。

## 怎么做？

这里只放出lua代码，C++请脑补。

创建内嵌浏览器并显示一个网站：

<pre lang="LUA">
-- 创建一个CCWebView，同时设置ActivityName为主Activity的包（后面会详述）
self._webview = CCWebView:create("us/t1201/testplayer/Testplayer")
self._webview:retain()
-- 显示一个网页，坐标20，20（左上角为0，0），宽度1000， 高度500
self._webview:showWebView("http://zengrong.net", 20, 20, 1000, 500)
-- 显示包名
print("getActivityName:", self._webview:getActivityName())
</pre>

更新已有浏览器中显示的网址，移除并销毁浏览器：

<pre lang="LUA">
self._webview:updateURL("http://zengrong.net/post/2112.htm")
self._webview:removeWebView();
self._webview:release()
self._webview = nil
</pre>

## 跨平台

目前内嵌浏览器仅支持 iOS 和Android 平台。以下是一些需要注意的地方：

### Android 平台

在创建CCWebView的时候必须提供你的项目的主Activity的包路径和类名。CCWebView 需要结合主Activity中提供的一些方法才能工作。这些方法我已经添加到项目模板中。

注意写包路径和类名的格式与JAVA的习惯不同，需要把点 `.` 替换成斜线 `/` 。

使用 `getActivityName()` 方法可以返回传入的包名。

### iOS 平台

iOS不需要提供包名，因此可以直接使用不带参数的 `create()` 方法来创建 CCWebView 。但为了避免判断平台使用不同的创建方法，也可以直接传入 Android 中需要的包名。iOS平台下的代码不会记录和处理这个值。

使用 `getActivityName()` 方法将总是返回空字符串。

在iOS平台上，浏览器的分辨率设定是个问题。对于高清设备，你传递的值其实是真实值的一半。例如在iPhone5上调用这句：

<pre lang="LUA">
showWebView("http://zengrong.net", 20, 20, 1000, 500)
</pre>

那么最终显示的效果是浏览器宽度超出屏幕。因为这里的宽度1000其实等于2000。

而在标清设备上（例如iPad2），传递的宽度就是真实的宽度。

### Mac OS X 平台

在 quick-x 的 Mac 模拟器中，调用 CCWebView 的方法将不会有任何作用。

### Windows 平台

目前可能无法编译 quick-x Windows 模拟器，我正在安装 Virtual Box 来解决这个问题。

[1]: https://github.com/zrong/quick-cocos2d-x
[2]: https://github.com/go3k/CCXWebview
[3]: http://blog.csdn.net/jackystudio/article/details/17576995
[10]: /wp-contents/uploads/2014/06/webview.png
