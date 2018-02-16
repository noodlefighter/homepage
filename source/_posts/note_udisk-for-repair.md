title: 制作一个能从各种ISO镜象启动的U盘
description: 
date: 2018-02-16
layout: post
comments: ture
categories:
- 笔记
tags: 
- boot
---

装机要用到各种工具u盘，手上只有一个u盘的时候总得费事格式化，如果直接把ISO镜象拖到U盘里按需选用就能方便很多。

于是试着弄了个能灵活加载各种ISO镜象的U盘，这里记录一下过程。

<!--more-->

---

## grub2-filemanager

https://github.com/a1ive/grub2-filemanager

国人做的一个基于GRUB2的启动器，能启动各类Linux发行版的Live CD，也能用memdisk方式启动其他类型的ISO。

![img](/i/note_udisk-for-repair/grub2filem.jpg)

![img](/i/note_udisk-for-repair/grub2filem2.png)

先得想办法把它启动起来，这里用grub2做bootloader。

## 分区、格式化

用fdisk或者其他工具格式化u盘，这里就只弄了个fat32的分区：

![img](/i/note_udisk-for-repair/partition.jpg)

## 安装gurb2

`/media/r/31E4-2D04`是分区的挂载点，`/dev/sdb`是u盘，请根据实际情况替换。

```
grub-install --no-floppy --root-directory=/media/r/31E4-2D04 /dev/sdb
```

![img](/i/note_udisk-for-repair/grub2install.jpg)

安装好之后，根目录下多出个`boot/gurb`文件夹，此时u盘已经能做引导了，但是现在它只有一个简陋的命令行界面。

## 获取grub2-filemanager
[获取grubfm-zh_CN.7z](https://github.com/a1ive/grub2-filemanager/releases)解压到`boot`目录下。

![img](/i/note_udisk-for-repair/fm-put.jpg)

三个文件分别对应x86架构下的3种启动方式: 非UEFI/EFI32/EFI64，按需选用。

## 配置grub2

获取用于在非UEFI下启动的memdisk（linux用户可以直接从`/usr/lib/syslinux/memdisk`复制），下载[syslinux](https://www.kernel.org/pub/linux/utils/boot/syslinux/)，提取`bios/memdisk/memdisk`文件，放到`boot`目录下。

![img](/i/note_udisk-for-repair/memdisk.jpg)

新建文件`boot/grub/grub.cfg`:

```none
set timeout=10
insmod fat
set default=0
loadfont /boot/grub2/fonts/unicode.pf2

menuentry 'grub2-filemanager'{    
    linux16 /boot/memdisk iso raw
    initrd16 /boot/grubfm.iso
}

menuentry 'grub2-filemanager(UEFI64)'{    
    chainloader /boot/grubfmx64.efi
}

menuentry 'grub2-filemanager(UEFI32)'{    
    chainloader /boot/grubfmia32.efi
}

```

制作完成。

## 使用方法

只需要把iso文件copy到U盘里，在grub2-filemanager的图形界面下以适当的方式启动即可，比如winpe（比如pe工具盘，win安装盘）用grub2dos方式；linux的cd则直接能被识别、引导。
