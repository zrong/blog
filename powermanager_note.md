[PowerManager使用注意事项](http://zengrong.net/post/1738.htm)

Android SDK中的PowerManager用来管理设备电源、重启、锁定休眠状态、唤醒等等操作。我已经把PowerManager的功能加入到了[ANEToolkit](http://zengrong.net/anetoolkit)中，这里记录一下开发过程中遇到的几个要注意的东东。

## 关于权限

PowerManager的所有功能，需要以下三类权限

* android.permission.DEVICE_POWER isScreenOn需要这个权限
* android.permission.WAKE_LOCK WakeLock类中的方法需要这个权限
* android.permission.REBOOT reboot方法需要这个权限

## PowerManager.WakeLock

使用acquire方法可以锁定自动休眠。

例如在下载大文件的时候，自动休眠会中断WIFI信号导致下载失败。为了避免这种情况，可以使用acquire方法来保持设备为不休眠状态。

`acquire` 有两种调用方式：

* acquire(long timeout)
	超时后取消锁。中断休眠一段时间，时间到了就自动取消中断。应该多采用这种方式。
* acquire()
	永久性锁。必须调用release才能解锁。
	
使用acquire锁定休眠有计数锁和计数锁两种机制，使用 `setReferenceCounted (boolean value)` 可以设置是否使用计数锁。默认使用的是计数锁。

这两种机制的区别在于，前者无论 `acquire()` 了多少次，只要通过一次 `release()` 即可解锁。而后者正真解锁是在 `(--count == 0)` 的时候，同样当 `(count == 0)` 的时候才会去申请加锁。

## reboot

即使是你为应用加入了REBOOT权限，在调用reboot方法的时候，依然会遇到异常，告知你没有权限执行这个方法。

>11-13 18:30:28.409: W/System.err(11290): java.lang.SecurityException: Neither user 10150 nor current process has android.permission.REBOOT.

这是因为 `REBOOT` 权限，只有系统程序才可以获得，用户程序无法获取这个权限。

## 参考资料

* http://stackoverflow.com/questions/3456467/why-does-my-app-throw-an-android-permission-reboot-securityexception
* [PowerManager.WakeLock源码解读(By DADA)](http://yueguc.iteye.com/blog/1125435)
