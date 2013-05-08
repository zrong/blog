[改变AIR for Android的消息通知栏图标](http://zengrong.net/post/1681.htm)

如果从愤怒的角度来说，这个勉强可以算作AIR的BUG，但我知道不是。估计这事儿也只有我能碰上。且听我细细道来……

##show notification in Android

在Android中显示消息通知，是个很简单的事情，见下面的代码：

<pre lang="JAVA">
Intent __activityIntent = _context.getPackageManager().getLaunchIntentForPackage(_setting.getPackageName());
if(__activityIntent == null) throw new NullPointerException("无法获取到名称为【"+_setting.getPackageName()+"】的Intent!");
Notification __msg = new Notification(R.drawable.ic_launcher, $ticket, System.currentTimeMillis());
ApplicationInfo __info = _context.getApplicationInfo();
__activityIntent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
PendingIntent __intent = PendingIntent.getActivity(_context, getRequestCode(), __activityIntent, PendingIntent.FLAG_UPDATE_CURRENT);
__msg.ledARGB = $color;
__msg.ledOnMS = 300;
__msg.ledOffMS = 1000;
__msg.flags |= Notification.FLAG_SHOW_LIGHTS;
__msg.flags |= Notification.FLAG_AUTO_CANCEL;
__msg.defaults |= Notification.DEFAULT_SOUND;
__msg.setLatestEventInfo(_context, $title, $msg, __intent);
NotificationManager __nm = (NotificationManager) _context.getSystemService(Context.NOTIFICATION_SERVICE);
__nm.notify(0, __msg);
</pre>

上面的代码基于Android 2.2，Android 3.0以后有更好的方法，google也不推荐使用这样的方法。但我们为了兼容旧设备，只能这么用。

将这段代码编译后打包成ANE，在AS中调用，在Android设备中调试运行，就可以弹出一个通知栏，显示的图标是AIR的程序配置文件中配置的图标。

>想要知道如何打包ANE，可以参考[Adobe的官方教程（中文）](http://help.adobe.com/zh_CN/air/extensions/index.html)

但是本文讲的不是这么简单的东西，本文讲的是一个相当纠结的问题。

##问题出现

这个方法在我的设备中一直运行得很好，直到有一天，当我要发布它的时候，出问题了。

显示在Notification bar区域的图标，变成了AIR的红色图标，而不是我的应用的图标了。就像下面这样：

![AIR的默认图标](image/change_notification_icon_in_air_for_android/air_icon.png)

而我的应用的图标，原本是这样的：

![正确的图标](image/change_notification_icon_in_air_for_android/sg_icon.png)

这个问题让我百思不得其解，为什么在调试的时候正常，在正式的发布版之后就不正常了么？郁闷的寻找了一段时间之后，一个偶然的机会让我发现了该问题的原因。

##问题原因

我们知道，AIR在打包成Android apk文件的时候，可以选择AIR运行时的处理方式。我们可以选择“共享AIR运行时(apk)”和“运行时绑定(apk-captive-runtime)”两种方式。

在调试的时候，Flash Builder会直接将apk打包成共享AIR运行时版本。而在发布的时候，我们一般都会选择运行时绑定。至于原因，你懂的。

而这两种运行时打包方式对于图标的处理方式是不一样的。我解压了同一个项目的“共享运行时”和“运行时绑定”apk文件，发现他们的`res/drawable`目录中的图像文件不同。在“共享运行时”的apk文件中，该目录只有一个alert形式的半透明图标，而“运行时绑定”的apk文件中，则多出了一个AIR的默认图标。

![比较解压文件](image/change_notification_icon_in_air_for_android/res_drawable.png)

看完这张图，出现AIR默认图标的原因已经找到了，下面是分析。

##问题的分析

由于应用需要支持多种分辨率，Notification bar的图标并不是使用一个图标文件来指定的，而是使用一个编号。也就是上面代码中的`R.drawable.ic_launcher`。这是一个int类型的值。

在ANE的代码中指定的这个常量，其实和AIR项目并没有什么关系，ANE项目是没有界面的，所使用的资源与AIR项目的资源也完全不同。将ANE打包到AIR项目中之后，就会改用AIR项目的资源。

但为什么在ANE中指定的图标编号值，在AIR项目中依然有作用呢（仅限“共享AIR运行时”）？

为了弄清这个问题，我创建了一个原生的Android项目。我发现默认情况下，它使用的图标也指向`R.drawable.ic_launcher`，而且这个常量的值与ANE项目中的值完全相同，都是`0x7f020000`。

我可以这样认为，这是Android项目的默认程序图标常量值。既然是这样，那么AIR也会遵循这个常量值。因此，在ANE中指定的图标常量值正好和AIR中的图标常量值相同，这是个“正确的巧合”。

在“共享AIR运行时”的时候，因为apk的`res/drawable`目录中没有其他的系统图标，Notification会自动去`res/drawable-hdpi；res/drawable-ldpi;res/drawable-mdpi`3个图标文件夹下寻找匹配的图标。这3个文件夹中保存的就是我们在AIR程序配置文件中指定的程序图标。

在“运行时绑定”的APK文件中，由于AIR添加了一个默认图标，Notification显示的时候就直接中又直接调用了`res/drawable`中的这个图标，因此显示的就是默认图标了。

##问题解决

有了上面的分析，我只要在指定Notification图标的时候，指定一个图标资源的对应常量值，就能够得到正确的图标了。但可惜的是，除了我自己要求AIR包含的文件外，我并不知道AIR在打包的时候将哪些图标文件放在了APK包中，也不知道它们的常量是什么。

在使用Android SDK开发的应用中，这些常量都在SDK自动生成的R类中，我很容易得到他们。但AIR并没有告诉我怎么得到这些资源。

看来我只能自己想办法。

我发现，Android SDK自动生成的R.java文件中的常量值是有规律的，比如`drawable`资源都以`0x7f02`开头；`string` 资源都以`0x7f04`开头；而`id`资源都已0x7f07`开头，然后就是从`0000`开始顺号排列。如下所示：

<pre lang="JAVA">
public final class R {
    public static final class attr {
    }
    public static final class drawable {
        public static final int ic_action_search=0x7f020000;
        public static final int ic_launcher=0x7f020001;
    }
    public static final class id {
        public static final int menu_settings=0x7f070002;
        public static final int textView1=0x7f070000;
        public static final int toggleButton1=0x7f070001;
    }
    public static final class layout {
        public static final int activity_main=0x7f030000;
    }
    public static final class menu {
        public static final int activity_main=0x7f060000;
    }
    public static final class string {
        public static final int app_name=0x7f040000;
        public static final int hello_world=0x7f040001;
        public static final int menu_settings=0x7f040002;
        public static final int title_activity_main=0x7f040003;
    }
    public static final class style {
        public static final int AppTheme=0x7f050000;
    }
}
</pre>

我可以这样认为，`0x7f020000`就是第一个图标文件的常量值，而第二个图标文件应该是`0x7f020001`，第三个是`0x7f020002`，第四个……唔，没有第四个，如果使用`0x7f020003`，AIR会直接崩溃退出。

测试证明，我的猜想是正确的。至此问题解决。

##感受

和Adobe打交道这么多年，已经被无数的BUG折磨得“百度不亲”。Flex的BUG因为有源码，可以自己动手解决。而[Flash Player和AIR的BUG就只能想办法绕过](http://zengrong.net/post/1390.htm)。现在做AIR for mobile开发也有一段时间了，[碰到了不少棘手的调试问题](http://zengrong.net/post/1654.htm)，忍受了ipa那乌龟一般的编译速度和iTunes那烂到无敌的用户体验，最后在这个不是BUG的问题上纠结了2天时间，彻底无语了……

从Adobe的角度看，在自己的产品中保留一个自己的默认图标，好像也无可厚非。从我的角度看，既然选择用AIR技术，碰到这样的问题，只能怪我手贱。

AIR for mobile给我的感觉，就像是一个保险箱，在我往里面放东西的时候，非常顺手。但我要修理它的时候，却发现我没有工具、没有手册、也没有指导。

当然，个人能力有限，也许我对Android更加了解之后，这个问题根本就不是问题了。

**有哪位Android专家能给点建议么？**
