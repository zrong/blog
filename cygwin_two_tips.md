[cygwin技巧2则：whereis和updatedb](http://zengrong.net/post/1807.htm)

##使用 updatedb

在cygwin中使用 `locate` 命令的时候，它提示我数据库太旧需要更新，但执行 `updatedb` 时，却提示 `Permission denied` 导致更新总是不成功。

这种情况下，需要使用 `--prunepaths` 来限制不更新某些特权目录。

例如我就不处理C盘和 `/proc`：

<pre lang="BASH">
updatedb  --prunepaths='/proc /cygdrive/c'
</pre>

##获取 whereis

cygwin中没有包含 `whereis` 和 `more`，要得到这些命令，可以安装 `util-linux` 包。

util-linux中包含的所有程序如下：

>addpart, agetty, blockdev, cal, cfdisk, chfn, chkdupexe, chrt, chsh, col, colcrt, colrm, column, ctrlaltdel, cytune, ddate, delpart, display-services, dmesg, elvtune, fastboot, fasthalt, fdformat, fdisk, flock, fsck.cramfs, fsck.minix, getopt, halt, hexdump, hwclock, initctl, ionice, ipcrm, ipcs, isosize, kill, last, line, logger, login, look, losetup, mcookie, mesg, mkfs, mkfs.bfs, mkfs.cramfs, mkfs.minix, mkswap, more, mount, namei, need, newgrp, partx, pg, pivot_root, provide, ramsize, raw, rdev, readprofile, reboot, rename, renice, reset, rev, rootflags, script, scriptreplay, setsid, setterm, sfdisk, shutdown, simpleinit, swapoff, swapon, taskset, tailf, tunelp, ul, umount, vidmode, vipw, wall, whereis, and write

如果不喜欢cygwin的setup.exe工具，可以试试用 `apt-cyg` 来安装：

<pre lang="BASH">
apt-cyg install util-linux
</pre>

##其他

* locate 和 whereis 都是linux中的查找命令，它们的区别和用法可以看这里：[Linux的五个查找命令](http://zengrong.net/post/1604.htm)
* 更详细的updatedb排除列表，可以看这里（自行跨墙）：[Getting updatedb on cygwin to prune paths with spaces](http://bookweevil.wordpress.com/2008/03/28/getting-updatedb-on-cygwin-to-prune-paths-with-spaces/)
