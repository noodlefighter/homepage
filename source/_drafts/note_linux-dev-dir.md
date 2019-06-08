

用buildroot构建出了rootfs，配合自己的kernel，发现有些不正常：



## dev相关

> * 内核启动时提示not found /dev/null
> * 有好多/dev/tty，0到63，想知道在哪减少

dev文件夹介绍
http://velep.com/archives/334.html

linux

busybox的mdev文档
https://git.busybox.net/busybox/plain/docs/mdev.txt

别人也有类似问题，有人提出可以用init.d里建脚本删除多余的节点：
http://lists.busybox.net/pipermail/buildroot/2013-January/065655.html
https://unix.stackexchange.com/questions/25021/change-the-number-of-generated-dev-tty-devices

第一个问题，就是内核没创建好/dev/null设备，重新配置内核，增加devtmpfs特性，以及自动挂载dev目录，问题解决。

查阅以上信息，结论就是这些tty设备为内核所创建。

## modprobe的错误提示

```bash
modprobe: can't change directory to '3.18.20': No such file or directory
```

发现是执行modprobe时提示的，查看rcS脚本：
```
# cd /etc/init.d/
# ls
S01syslogd  S10mdev     S40network  rcS
S02klogd    S20urandom  rcK
# cat S10mdev
#!/bin/sh
#
# Start mdev....
#

case "$1" in
  start)
        echo "Starting mdev..."
        echo /sbin/mdev >/proc/sys/kernel/hotplug
        /sbin/mdev -s
        # coldplug modules
        find /sys/ -name modalias -print0 | xargs -0 sort -u | tr '\n' '\0' | \
            xargs -0 modprobe -abq
        ;;
  stop)
        ;;
  restart|reload)
        ;;
  *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
esac

exit $?
```

功能是在启动时，如果/sys有包含`modalias`的设备，就尝试用modprobe挂载对应内核模块（.ko文件），需要做的事情:

1. 内核模块放入/lib/module/`uname -r`；
2. 创建modules.dep。


## tty

linux的虚拟终端
https://blog.csdn.net/astrotycoon/article/details/79001713

linux kernel配置中对虚拟终端的描述：
```
CONFIG_VT:                                                      
                                                                
If you say Y here, you will get support for terminal devices with  
display and keyboard devices. These are called "virtual" because you
can run several virtual terminals (also called virtual consoles) on
one physical terminal. This is rather useful, for example one   
virtual terminal can collect system messages and warnings, another 
one can be used for a text-mode user session, and a third could run
an X session, all in parallel. Switching between virtual terminals 
is done with certain key combinations, usually Alt-<function key>. 

The setterm command ("man setterm") can be used to change the   
properties (such as colors or beeping) of a virtual terminal. The  
man page console_codes(4) ("man console_codes") contains the special
character sequences that can be used to change those properties
directly. The fonts used on virtual terminals can be changed with  
the setfont ("man setfont") command and the key bindings are defined
with the loadkeys ("man loadkeys") command.                     
                                                                   
You need at least one virtual terminal device in order to make use  
of your keyboard and monitor. Therefore, only people configuring an 
embedded system would want to say N here in order to save some      
memory; the only way to log into such a system is then via a serial 
or network connection.
                                 
If unsure, say Y, or else you won't be able to do much with your new
shiny Linux system :-)

如果您在这里说Y，您将获得带有显示和键盘设备的终端设备的支持。这些被称为“虚拟”，因为您可以在一个物理终端上运行多个虚拟终端（也称为虚拟控制台）。这是非常有用的，例如，一个虚拟终端可以收集系统消息和警告，另一个可以用于文本模式用户会话，第三个可以并行运行X会话。使用某些组合键完成虚拟终端之间的切换，通常是Alt-<功能键> 

setterm命令可用于更改虚拟终端的属性（如颜色或蜂鸣声）。Theman page console_codes（4）包含可用于直接更改这些属性的特殊字符序列。可以使用setfont命令更改虚拟终端上使用的字体，并使用loadkeys命令定义键绑定。

您需要至少一个虚拟终端设备才能使用键盘和显示器。因此，只有配置嵌入式系统的人才会想在这里说N以节省一些内存;登录这样一个系统的唯一方法就是通过串行或网络连接。

如果不确定，请说Y，否则你将无法在你的新系统上操作。
```

https://askubuntu.com/questions/377213/why-so-many-virtual-consoles
提到改变tty数量的具体方法——修改内核，但是这对新的内核已经不管用了，`include/linux/*.h`已经拆分部分到`include/uapi/linux/*.h`了，应该修改`include/uapi/linux/vt.h`的`MAX_NR_CONSOLES`，但实际追踪了一下代码，减少这个值并不会带来多少收益。

尝试修改一下吧，重启后立即查看内存使用，修改前：
```
# free
             total       used       free     shared    buffers     cached
Mem:         58516       9628      48888         32          0       1332
-/+ buffers/cache:       8296      50220
Swap:            0          0          0
```

修改后：
```
# free
             total       used       free     shared    buffers     cached
Mem:         58516       9304      49212         32          0       1348
-/+ buffers/cache:       7956      50560
Swap:            0          0          0

```
