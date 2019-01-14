title: Newifi-d2路由器折腾笔记
description: 
date: 2019-1-14
updated: 2019-1-14
layout: post
comments: true
categories:
- 笔记
tags: 
- 笔记
- linux
---

朋友推荐了个适合当开发机的路由，某宝80多元的二手，MT7621AT@880MHz，512MB DDR3，32MB Flash，ROM和RAM都够大，那就开始折腾。

<!--more-->

## 相关资料

感谢恩山论坛上高手们的大量资料参考，去翻热门贴子会有很多tip。

## 上手

第一件事当然是直接SSH上去，很好connection refuse。

进WEB页面设置root用户的密码，看网上有说要安装SSH的插件，但我这没法刷出在线的插件列表，只得靠搜索找到了SSH开启方法：

```
访问http://192.168.99.1/newifi/ifiwen_hss.html
提示success说明成功
```

好，SSH能登上了。

## 备份

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

这时候已经能随便刷固件了。


## 编译LEDE

https://github.com/coolsnowwolf/lede

lean大的仓库，带了不少本地化的东东，跟着README编译就好。

Newifi-d2的配置：

```none
Target System (MediaTek Ralink MIPS)
Subtarget (MT7621 based boards)
Target Profile (Newifi D2)
```

编译过程中需要下载不少东西，根据国内的网络情况，代理是少不了的，这里用的proxychains，比如：

```bash
proxychains make -j V=s
```

编译结果如下：

```none
r@r-work ~/lede_lean/bin/targets/ramips/mt7621 $ tree -L 1
.
├── config.seed
├── openwrt-ramips-mt7621-device-d-team-newifi-d2.manifest
├── openwrt-ramips-mt7621-device-d-team-newifi-d2-rootfs.tar.gz
├── openwrt-ramips-mt7621-d-team_newifi-d2-initramfs-kernel.bin
├── openwrt-ramips-mt7621-d-team_newifi-d2-squashfs-sysupgrade.bin
├── packages
└── sha256sums
```

其中`openwrt-ramips-mt7621-d-team_newifi-d2-squashfs-sysupgrade.bin`是可以直接刷进路由的二进制文件，直接烧上，成功了：

{% asset_img openwrt-status.jpg %}

好了东西全了，可以按需折腾自己的应用了。
