date: 2020-11-27
tags: 

- 工具
- 桌面软件

---

[Barrier](https://github.com/debauchee/barrier)可以让多台桌面计算机共享同一套鼠标，从[synergy-core](https://github.com/symless/synergy-core)项目fork而来，基于QT，支持主流桌面操作系统。

这篇文章记录Barrier的使用方法，包括编译、安装、配置。

<!--more-->

## 安装

如果需要安装在Windows/MacOS上，github的[release页](https://github.com/debauchee/barrier/releases)中能找到开箱即用的exe/dmg文件。

如果需要安装在Linux下



## 配置



## 编译

因为各大系统都有编译好的程序，大多数情况都不需要自己编译，所以这章放到了最后。

笔者在Nvidia的jetson(ARMv8)平台下，软件源中没有预编译好的程序所以需要自己编译，系统是`Ubuntu 18.04.5 LTS`。

先下载解压源码包（建议先github网页中的Release里找到最新的版本），执行cmake：

```
$ wget https://github.com/debauchee/barrier/releases/download/v2.3.3/barrier-2.3.3-release.tar.gz
$ tar -xzvf barrier-2.3.3-release.tar.gz
$ cd barrier-2.3.3-release
$ mkdir build && cd build
$ cmake ..
```

执行cmake后，可能遇到的问题：
- 报错`Could NOT find CURL (missing: CURL_LIBRARY CURL_INCLUDE_DIR)`，解决方法是安装`libcurl4-openssl-dev`
- 报错`No package 'avahi-compat-libdns_sd' found`，解决方法是安装`libavahi-compat-libdnssd-dev`
- 报错`Missing library: Xtst`，解决方法是安装`libxtst-dev`
- 报错`By not providing "FindQt5.cmake" in CMAKE_MODULE_PATH`解决方法是安装`qt5-default`

一切顺利的话，输出会是这样的：

```
...
...
-- Full Barrier version string is '2.3.3-release-release'
-- Configuring directory /home/mpc/barrier/barrier-2.3.3-release/build/rpm
-- Configuring file barrier.spec
-- Configuring done
-- Generating done
-- Build files have been written to: /home/mpc/barrier/barrier-2.3.3-release/build
```

这就表示cmake执行成功了，根据当前环境生成了可用的Makefile，接下来执行编译：

```
$ make -j3
```

编译可能会失败ake可能遇到的问题：

- 报错`fatal error: openssl/ssl.h: No such file or directory`，解决方法是安装`libssl-dev`

编译成功后，执行安装，就可以算打完收工了：

```
$ sudo make install
```

