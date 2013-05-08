[Android中SharedPreferences的模式](http://zengrong.net/post/1687.htm)

在Android开发中，使用SharedPreferences来共享一些小的配置数据是非常方便的。可是我发现在不同版本上，SharedPreferences的表现并不一样。

我的测试机是Android 2.3.6，程序的写入和读取都正常。但把相同的程序在Android 4.1上运行，就发现虽然写入正常，但刚刚写入的数据不能被读取到。

经过仔细调试，发现在Android 4.1中，读取到的写入的SharedPreference并不在同一个线程中，其实是2个不同的SharedPreference。

找到SDK文档，才发现可以通过设置[Context.getSharedPreferences](http://developer.android.com/reference/android/content/Context.html#getSharedPreferences(java.lang.String, int))的第二个参数解决这个问题。

因为这个方法比较简单，一直没怎么看文档，直接写0代表私有访问模式。没想到这个方法的第二个参数从Android 3.0开始有了变化。

下面是第二个参数mode的说明：

>Operating mode. Use 0 or `MODE_PRIVATE` for the default operation, MODE_WORLD_READABLE and `MODE_WORLD_WRITEABLE` to control permissions. The bit `MODE_MULTI_PROCESS` can also be used if multiple processes are mutating the same SharedPreferences file. `MODE_MULTI_PROCESS` is always on in apps targetting Gingerbread (Android 2.3) and below, and off by default in later versions.

下面是`MODE_MULTI_PROCESS`的说明：

>SharedPreference loading flag: when set, the file on disk will be checked for modification even if the shared preferences instance is already loaded in this process. This behavior is sometimes desired in cases where the application has multiple processes, all writing to the same SharedPreferences file. Generally there are better forms of communication between processes, though.
>This was the legacy (but undocumented) behavior in and before Gingerbread (Android 2.3) and this flag is implied when targetting such releases. For applications targetting SDK versions greater than Android 2.3, this flag must be explicitly set if desired.

也就是说，`MODE_MULTI_PROCESS`这个值是一个标志，在Android 2.3及以前，这个标志位都是默认开启的，允许多个进程访问同一个SharedPrecferences对象。而以后的Android版本，必须通过明确的将`MODE_MULTI_PROCESS`这个值传递给mode参数，才能开启多进程访问。

所以：我们在获得SharedPreferences的时候，需要判断一下SDK的版本号：

<pre lang="JAVA">
int __sdkLevel = Build.VERSION.SDK_INT;
SharedPreferences __sp = $context.getSharedPreferences(SETTING_NAME, (__sdkLevel > Build.VERSION_CODES.FROYO) ? 4 : 0);
</pre>
