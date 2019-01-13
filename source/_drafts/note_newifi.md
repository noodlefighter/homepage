
https://github.com/coolsnowwolf/lede

https://www.right.com.cn/forum/thread-341067-1-1.html

https://www.right.com.cn/forum/thread-342918-1-1.html

https://www.right.com.cn/forum/thread-342884-1-1.html

https://www.right.com.cn/forum/thread-344381-1-1.html

https://www.right.com.cn/forum/thread-161906-1-1.html

别人的笔记
https://blog.csdn.net/lhorse003/article/details/73730265


newifi-d2折腾笔记

## 上手

第一件事当然是直接SSH上去，很好connection refuse。

进WEB页面设置root用户的密码，看网上有说要安装SSH的插件，但我这没法刷出在线的插件列表，只得靠搜索找到了SSH开启方法：

```
访问http://192.168.99.1/newifi/ifiwen_hss.html
提示success说明成功
```

好，SSH能登上了。

## 然后备份到本地

```
输入cat /proc/mtd  得到：
mtd0: 00010000 00010000 "u-boot-env"
mtd1: 00010000 00010000 "Factory"
mtd2: 01fb0000 00010000 "firmware"
mtd3: 00146bfa 00010000 "kernel"
mtd4: 01e49406 00010000 "rootfs"
mtd5: 00f40000 00010000 "rootfs_data"
mtd6: 00020000 00010000 "panic_oops"
mtd7: 00010000 00010000 "nvram"

输入
dd if=/dev/mtd0 of=/tmp/u-boot-env.bin
dd if=/dev/mtd1 of=/tmp/Factory.bin
dd if=/dev/mtd2 of=/tmp/firmware.bin
dd if=/dev/mtd3 of=/tmp/kernel.bin
dd if=/dev/mtd4 of=/tmp/rootfs.bin
dd if=/dev/mtd5 of=/tmp/rootfs_data.bin
dd if=/dev/mtd6 of=/tmp/panic_oops.bin
dd if=/dev/mtd7 of=/tmp/nvram.bin
```

## 刷breed

https://breed.hackpascal.net/

下载`breed-mt7621-newifi-d2.bin`，按住复位键插入电源，进入自带的恢复模式，192.168.1.1是它的web页面：

{% asset_img boot-web.png %}

选择这个固件，恢复，会提示失败。喔嚯？
大概是需要所谓的解锁才能随意刷boot？

上恩山论坛逛了下发现breed的作者hackpascal提供了个刷breek方法，通过加载内核模块强行刷掉boot，帖子名“新路由3 (Newifi D2) 免拆机免解锁刷 Breed 教程”。

他提供了一个`newifi-d2-jail-break.ko`，用insmod命令加载，等自动重启后，breed已经刷上了。

> 唔，不清楚如果直接用dd命令恢复会怎么样，不敢试

再进入恢复模式，就能看到breed管理界面了：

{% asset_img boot-breed.png %}





