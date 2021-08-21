date: 2018-02-16
tags:

- boot
---

装机要用到各种工具u盘，手上只有一个u盘的时候总得费事格式化，如果直接把ISO镜象拖到U盘里按需选用就能方便很多。于是试着弄了个能灵活加载各种ISO镜象的U盘，这里记录一下过程。

<!--more-->

```
变更记录：
2018-02-16 初版
2019-06-14 改用UEFI
2021-08-07 推荐使用Ventoy
```

---

**！！注意！！**
**！！注意！！**

文章已经过期，现在**强烈建议把`grub2-filemanager`换成 `Ventoy`，它们的功能类似，但后者对 Windows 的 ISO 更友好，安装过程对于一般用户来说也相对简单，请直接参考[Ventoy的使用指南](https://www.ventoy.net/cn/doc_start.html)。**



## ~~grub2-filemanager~~

https://github.com/a1ive/grub2-filemanager

国人做的一个基于GRUB2的启动器，能启动各类Linux发行版的Live CD，也能用memdisk方式启动其他类型的ISO。

![grub2filem](_assets/制作一个能从各种ISO镜象启动的U盘/grub2filem.jpg)

![grub2filem2](_assets/制作一个能从各种ISO镜象启动的U盘/grub2filem2.png)

### 启动U盘制作方法

这里制作UEFI引导方式的U盘。

先将分区表格式为设为GUID，建EFI分区，可以用DiskGenius：

![1560447568154.png](_assets/制作一个能从各种ISO镜象启动的U盘/1560447568154.png)

快速分区功能建EFI分区：

![1560447642813.png](_assets/制作一个能从各种ISO镜象启动的U盘/1560447642813.png)

[获取grubfm-zh_CN.7z](https://github.com/a1ive/grub2-filemanager/releases)，把`grubfmx64.efi`复制到`(EFI分区)/efi/boot/bootx64.efi`。完毕

### 使用方法

只需要把iso文件copy到U盘里，在grub2-filemanager的图形界面下以适当的方式启动即可，比如winpe（比如pe工具盘，win安装盘）用grub2dos方式；linux的cd则直接能被识别、引导。
