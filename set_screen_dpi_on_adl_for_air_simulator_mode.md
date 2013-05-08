[在AIR模拟器模式中设置Screen DPI属性](http://zengrong.net/post/1844.htm)

Set Screen DPI on ADL for air simulator mode

在使用AIR开发移动应用程序的时候，我们可以利用AIR Debug Launcher (ADL)在PC上进行调试，这样测试效率更高，速度也更快。

但是，PC的DPI值（72）与移动设备（160、252、362……）不同，这将导致某些依赖设备分辨率的框架和程序，在PC上的表现与移动设备不同。

如果使用Flash Builder 4.7开发，在一般情况下，不会遇到分辨率问题。因为Flash Builder会自动进行DPI的设置。从下面的设置界面中，我们可以看到，在选择一个模拟器配置的时候，这个配置是包含DPI设置的。<!--more-->

<img src="/wp-content/uploads/2013/04/flashbuilder_device_configuration.png" alt="flashbuilder_device_configuration" width="894" height="467" class="aligncenter size-full wp-image-1845" />

在启动参数中，我们也可以看到，这个DPI设置是有效的。

<img src="/wp-content/uploads/2013/04/custom_launch_parameter.png" alt="custom_launch_parameter" width="775" height="712" class="aligncenter size-full wp-image-1846" />

在模拟器启动之后，通过检查 `Capabitilities.screenDPI` 的值，我们可以知道，这个设置确实是有效的。

Flash Builder是调用ADL来以模拟器模式启动应用的。那么对于其他IDE来说，是否也能通过ADL的启动参数来进行这样的设置呢？

遗憾的是，我找遍了 ADL 的文档，都没有看到关于分辨率的设置。受到上面第二张图的启发，我也尝试了这样的语法

	adl -screensize NexusOne -DPI 252 application.xml bin

ADL直接报错了。显然，这个参数不能这么用。

我查看了FlashDevelop中关于移动设备项目的 `Run.bat` 脚本，他们也没有解决这个问题。[论坛](http://www.flashdevelop.org/community/viewtopic.php?p=43117#p43117)上有人提到过这个问题，但没有得到正面的回答。

那么，Flash Builder是怎么做到的？

其实，我刚才的尝试已经接近成功了。隐藏的参数确实存在，只是和我使用的参数名称不同而已。上面的代码，写成这样，就OK了。

	adl -screensize NexusOne -XscreenDPI 252 application.xml bin

我可以更新一下FlashDevelop的Run.bat脚本了。

**参考文章：**

* <http://youtrack.jetbrains.com/issue/IDEA-89860>
* [AIR Debug Launcher](http://help.adobe.com/en_US/air/build/WSfffb011ac560372f-6fa6d7e0128cca93d31-8000.html#WS5b3ccc516d4fbf351e63e3d118666ade46-7f65)
* [Scale Too Small](http://forum.starling-framework.org/topic/scale-too-small)
