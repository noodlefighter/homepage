buildroot笔记

使用release版本buildroot-2019.02.1

## 构建流程

构建出来的目录：

```
r@r-work ~/osp/buildroot-2019.02.1/output $ tree -L 2
.
├── build
│   ├── buildroot-config
│   ├── buildroot-fs
 。。。略去一堆包的构建目录和build相关log。。。
│   ├── toolchain-external
│   └── toolchain-external-custom
├── host
│   ├── arm-buildroot-linux-uclibcgnueabi
│   ├── bin
│   ├── etc
│   ├── include
│   ├── lib
│   ├── lib64 -> lib
│   ├── share
│   └── usr -> .
├── images
│   ├── rootfs.tar
│   └── rootfs.tar.gz
├── staging -> /home/r/osp/buildroot-2019.02.1/output/host/arm-buildroot-linux-uclibcgnueabi/sysroot
└── target
    ├── bin
    ├── dev
    ├── etc
    ├── lib
    ├── lib32 -> lib
    ├── media
    ├── mnt
    ├── opt
    ├── proc
    ├── root
    ├── run
    ├── sbin
    ├── sys
    ├── THIS_IS_NOT_YOUR_ROOT_FILESYSTEM
    ├── tmp
    └── usr
```

文件夹功能：
```
build   存放packages的源码、构建log
host    存放交叉编译中宿主（host）依赖的相关工具：比如automake、m4；此外还有交叉编译工具链，比如这里的“arm-buildroot-linux-uclibcgnueabi”
target  目标根文件系统的中间产品
images  最终产品，比如编译好的系统内核、打包好的根文件系统（镜象、归档）
```


流程大概是：

1. 构建交叉编译工具链：如果配置由buildroot来构建工具链，则编译后安装到host目录；如果配置了外部工具链（external-toolchain），则会将工具链按照一定规则copy到host目录中
1. 构建宿主工具
1. 构建目标packages：下载、打patch、编译、安装到target目录中
1. 打包


## 处理与buildroot不相容的工具链

配置使用外部工具链后，buildroot将从指定路径copy工具链到host目录中，主要是一些libs，这个步骤导致一些目录结构比较奇葩的工具链无法用于buildroot。

这里有几个解决思路，难度依次递增：

1. 放弃使用外部工具链，使用buildroot构建
2. 使用Crosstool-NG等工具构建，buildroot兼容这些常见工具构建出的工具链
3. 尝试修改buildroot源码

## 使用buildroot用于进行开发过程

SDK：
https://blog.csdn.net/dongkun152/article/details/81741982

> Buildroot的正常操作是下载源码包，解压缩，配置，编译和安装源码包中的软件。源代码在`output/build/<package>-<version>`中提取，这是一个临时目录：每当使用`make clean`时，该目录将被完全删除，并在下一次make调用时重新创建。即使使用Git或Subversion存储库作为包源代码的输入，Buildroot也会创建一个源码包，然后像上文说的流程使用它。
> 当Buildroot主要用作集成工具时，这种行为非常适合构建、集成嵌入式Linux系统的组件。但是，如果在系统的某些组件的开发过程中使用Buildroot，这种行为不是很方便：当需要对一个包的源代码做一点小的改动，并且能够使用Buildroot快速重建系统时。直接在`output/build/<package>-<version>`中进行更改不是一个合适的解决方案，因为在`make clean`时会删除目录。 
> 因此，Buildroot为此用例提供了一种特定的机制：`<pkg> _OVERRIDE_SRCDIR`机制。Buildroot读取OVERRIDE文件，用户通过它告诉Buildroot一些源码包的位置。默认情况下，此覆盖文件名为`local.mk`，位于Buildroot源树的顶级目录中，但可以通过`BR2_PACKAGE_OVERRIDE_FILE`配置选项指定其他位置。
> 来自：https://buildroot.org/downloads/manual/manual.html#_using_buildroot_during_development

todo：

## 设备节点

todo：

buildroot的使用
https://blog.csdn.net/flfihpv259/article/details/51996204

解释了几种/dev
http://lists.busybox.net/pipermail/buildroot/2011-December/048057.html

mdev是busybox上类似udev的实现，看help和`/etc/init.d/S10mdev`就能大概了解用法。（这还有[mdev文档](https://git.busybox.net/busybox/plain/docs/mdev.txt)）

```bash
# mdev
BusyBox v1.29.3 (2019-04-10 20:07:42 CST) multi-call binary.

Usage: mdev [-s]

mdev -s is to be run during boot to scan /sys and populate /dev.

Bare mdev is a kernel hotplug helper. To activate it:
        echo /sbin/mdev >/proc/sys/kernel/hotplug

It uses /etc/mdev.conf with lines
        [-][ENV=regex;]...DEVNAME UID:GID PERM [>|=PATH]|[!] [@|$|*PROG]
where DEVNAME is device name regex, @major,minor[-minor2], or
environment variable regex. A common use of the latter is
to load modules for hotplugged devices:
        $MODALIAS=.* 0:0 660 @modprobe "$MODALIAS"

If /dev/mdev.seq file exists, mdev will wait for its value
to match $SEQNUM variable. This prevents plug/unplug races.
To activate this feature, create empty /dev/mdev.seq at boot.

If /dev/mdev.log file exists, debug log will be appended to it.
```

## 额外的平台软件包

需要添加自定义软件包时，无需直接修改buildroot目录，它提供了一个机制方便在目录外添加额外包、配置等：

文档https://github.com/fabiorush/buildroot/blob/master/docs/manual/customize-outside-br.txt


### 添加软件包时的依赖问题

Kconfig中需要用select/depends on来描述软件包依赖，但这并不会自动地在构建中确定构建顺序，需要手动地在.mk中描述依赖关系。

比如当创建一个[generic-package](https://buildroot.org/downloads/manual/manual.html#_infrastructure_for_packages_with_specific_build_systems)时，.mk文件中的`LIBFOO_DEPENDENCIES`指定了依赖关系。
