title: windows下eclipse的zephyr开发环境搭建
date: 2017-12-07
layout: post
comments: ture
categories:
- 嵌入式软件
tags: 
- eclipse
- zephyr
---

win的Linux子系统下搭建zephyr编译环境, 在eclipse中开发.

<!--more-->

![zephyr-logo.png](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=dafcGlfIGBlL5VNPUAvRd2MQVCBRRvleSNE2-lA-S4_mV5hyY-OyyzRYGa5hKuPTNibdzBLhtx6WChgHyVUF1MhZL-pqXVbuO3RXCRDaVtx61g&file_name=/zephyr-logo.png)

Zephyr是linux基金会的rtos项目([官方网站](https://www.zephyrproject.org/)), Apache License, 2016年年底我开始关注这个项目, 它的成长速度令人激动.

Zephyr使用Kconfig+Makefile(1.10.0之后改为CMake)构建, 在win10周年版之后, Windows加入了一个WSL(Windows Subsystem for Linux), 在WSL下搭建zephyr开发环境就像在Linux下一样方便, 习惯在win开发的人也可以用它来尝尝鲜.

---

笔者部分软件版本信息
```none
windows 10 1709 16299.64
Zephyr Kernel v1.10.0-rc2
Zephyr SDK 0.9.2
Python 3.5.2
cmake version 3.10.0
```

文中的目标板是ARM平台M3内核的stm32_min_dev.

---

## ``Step0 更新系统``

win+R执行``winver``, 确认系统版本win10为1607之后, 如果版本未达到要求请先升级系统.

![img.png](/i/em_zephyr_windows/1.png)

---

## ``Step1 启用WSL 安装Ubuntu On Windows``

该步骤可以参考[微软的文档](https://msdn.microsoft.com/en-us/commandline/wsl/install-win10)以及[Zephyr文档](http://docs.zephyrproject.org/getting_started/installation_win.html#using-windows-10-wsl-windows-subsystem-for-linux).

进入``控制面板 - 程序 - 程序和功能 - 开启或关闭Windows功能``, 勾选``适用于Linux的Windows子系统``, 确定后WSL开启.
![img.png](/i/em_zephyr_windows/2.png)
 
进入``Microsoft Store``, 搜索``ubuntu``, 下载即可得到一个Ubuntu子系统.

启动它的方法有几种:
* 开始菜单中输入ubuntu, 启动
* win+R, 输入``wsl``或``bash``或``ubuntu``

启动了熟悉(陌生?)的bash, 就可以把它当做ubuntu一样操作了. 

![img.png](/i/em_zephyr_windows/3.png)

这里提供一些信息:
* 根文件系统大致位置在 ``C:\Users\r\AppData\Local\Packages\CanonicalGroupLimited.UbuntuonWindows_(??)\LocalState\rootfs``你可以直接在windows中浏览它, 但最好不要直接编辑它, 因为会把文件的权限弄乱, 如果不小心弄乱了权限, 请使用``chmod``命令重新设置文件权限.
* wsl可以直接访问windows中的文件, 各盘符被挂载在``/mnt``下, 如C盘为``/mnt/c``
* 更多信息可以[浏览开发者博客](https://blogs.msdn.microsoft.com/commandline/)

---

## ``Step2 搭建Zephyr开发环境``
该步骤在[Zephyr的文档](http://docs.zephyrproject.org/getting_started/installation_linux.html#installation-linux)中已经描述清楚了, 这里不重复陈述, 但有一些要注意的地方.

### 更换国内更新源
国内访问默认更新源贼慢, 所以请先为ubuntu的apt更换源, 推荐阿里的源, 具体请百度``ubuntu更换源``.

### 下载缓慢/无法下载的问题
国内因为一些不可描述的原因, 在下载Github的Release中的压缩包时可能缓慢或无法访问, 请自备代理或者选择从其他渠道获取.

---

## ``Step3 尝试编译zephyr``
### ``Step3.1 获取Zephyr源码包``
#### ``方法1``
[Github Release](https://github.com/zephyrproject-rtos/zephyr/releases)直接获取压缩包

#### ``方法2``
使用git clone, 此时请注意关闭git的"AutoCrlf"功能, 在windows下, 该功能会将unix风格的换行符自动转换成windows风格, unix系工具无法正确处理win风格的换行符.

### ``Step3.2 编译Hello World程序``
参考[Zephyr手册](http://docs.zephyrproject.org/getting_started/getting_started.html), 编译hello world:

```
# 进入zephyr源码目录
$ cd zephyr

# source命令 配置必要的环境变量
$ source zephyr-env.sh

# 进入hello world目录
$ cd $ZEPHYR_BASE/samples/hello_world

# 创建并进入build目录 
$ mkdir -p build & cd build

# 使用cmake生成makefile 目标为qemu模拟器
$ cmake -DBOARD=qemu_cortex_m3 ..

# 使用cmake生成的makefile进行构建并执行
$ make run
```

如果环境搭建无误, 应该能看到下图的结果:
![Snipaste_2017-12-06_16-22-19.png](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=d642O1erw_zg39sSpdXw0OIzf89J5b829WsQP3B0FmSOHjUIOZOcDVtZ-hTbOmB2uYwWVmFPv5YWfUwOEXZ7ciXLCZq3srhL5sPgIuSsWuvIQ_43tH0XEE-NsGXjUWRGKoUG&file_name=/Snipaste_2017-12-06_16-22-19.png)

---

## ``Step4 搭建Eclipse ARM开发环境``
使用IDE是为了更方便的编写和调试应用程序, 请参考我的另一篇blog[windows中eclipse的arm开发环境的搭建方法](http://noodlefighter.com/%E5%B5%8C%E5%85%A5%E5%BC%8F%E8%BD%AF%E4%BB%B6/em_eclipse_arm)搭建环境.

---

## ``Step5 使用Eclipse编译Zephyr``

### ``Step5.1 应用程序项目的目录树设计``
Zephyr使用[CMake](https://cmake.org/)构建系统, 可以很灵活地设计目录树, 这里为作演示, 简单地把``zephyr/samples/hello_world``中的文件拷贝到与zephyr同级的目录下, 这级目录作为工程的根目录, 如图所示:
![Snipaste_2017-12-06_17-25-41.png](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=c239lUPpomlQsO9Kr9cCcHQEbXfSfOpAmBccHJWQkep34aHAn7sDbHOCYZlpcxGVJ0JJr1VSOwRK1QS6W7aQor2TBq-VXooQxJ7urtCaxNBbXsNrsMtgxtamhTTxAEYBHNht&file_name=/Snipaste_2017-12-06_17-25-41.png)

### ``Step5.2 新建Eclipse工程``
在Eclipse中新建Makefile工程
![Snipaste_2017-12-06_17-30-55.png](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=c882Krjl921O7wVxlLETWzdFBzzAPAss581f3waLDBOw_9gLwrVsp0kWxZnFI11NBuxB5gjjZaN5osAEuddu2HVw1ntmbUt3fQM0SHdyWpLhr096D0iiky1avz2bu3TGFMtB&file_name=/Snipaste_2017-12-06_17-30-55.png)

### ``Step5.3 调用WSL环境构建程序``

由于IDE中的调试功能由插件提供, 我们需要做的仅是利用WSL进行构建, 根据官方blog [A Guide to Invoking WSL](https://blogs.msdn.microsoft.com/commandline/2017/11/28/a-guide-to-invoking-wsl/) 可得知调用WSL的方法:

```
bash -c command
```

### ``Step5.4 编写供IDE使用的辅助构建脚本``

Eclipse中常用的操作就是build/clean, 这里示范通过在WSL中调用一个自行编写的脚本``build.sh``实现这两个操作:

```sh
#!/bin/bash

build_dir="build"
zephyr_dir="zephyr"
cmake_options="-DBOARD=stm32_min_dev"
make_options="-j8"

if [ $1 == "build" ] ; then 
    echo "Command: build"
    
    if [ ! -d $build_dir ] ; then
        echo "$build_dir not exist, create one"
        mkdir $build_dir
    fi
    
    # zephyr environment variable
    source $zephyr_dir/zephyr-env.sh
    
    # Entry $build_dir dir
    cd $build_dir
    
    # if Makefile not exist
    if [ ! -f "Makefile" ] ; then
        echo "Makefile not exist, call CMake"
        cmake $cmake_options ..
    fi
    
    echo "Call Make"
    make all $make_options
    
elif [ $1 == "clean" ] ; then    
    echo "Command: clean"
    echo "delete all files in $build_dir dir"
    rm -rf $build_dir/* 
else
    echo "USAGE: $0 build or $0 clean"
fi
```

该脚本实现多线程增量编译, 将该脚本保存在工程目录下, 命名``build.sh``, 脚本用法:
```
# 执行build操作 当Makefile不存在时调用CMake生成Makefile 并执行make操作
$ ./build.sh build

# 执行clean 直接清空build目录
$ ./build.sh clean
```

### ``Step5.5 IDE工程中关联辅助构建脚本``

接下来对CDT工程的``C/C++ Build``进行设置:

1. 打开工程设置(Alt+Enter), ``C/C++ Build``, ``Builder Settings``选项卡
2. 取消``Use default build command``, ``Build command``中填入``bash``
2. 进入``Behavior``选项卡
3. ``Build on resource save``及``Build``中填写``-c "./build.sh build"``
4. ``Clean``填写``-c "./build.sh clean"``

![build1.png](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=ff50ddAEhyFUNBjP_YXaPrHmah0rG337e8hHvn8IfnRFvrEXc_CG0Yr_SwPBEuHqJrt6FiA9omsFiHKdcIhqyOBAdN22WTVx2nh7E4g&file_name=/build1.png)

![build2.png](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=3738LBmzMq9BIKtyGv1pKQb5fH-HrhF6LNe2d65IzZK32NlBJ55I9ro8rn8I8n3YOeNot25aw5An4fzy6L9cwlR7Vb_a9YIz_JOIBg4&file_name=/build2.png)

设置好后就可以在IDE中编译工程了:

![build_gif.gif](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=0fe1sTXoRaYGrdslYEIPE8k-CbZftrxo6I1oS52PLT_KYKvm1dAdBtxnNKbbqbB6iM33DRrgNXZYPxiAGKV1Fmmg3ZUaW0NhSDtP8xFWkJM&file_name=/build_gif.gif)

---

## ``Step6 IDE中调试``

这里演示使用J-Link连接STM32F103C8最小系统板, 其他编译器和目标硬件大同小异, 均是在Eclipse中使用gnu-mcu-eclipse插件提供的调试功能, 它将通过打开一个调试器工具包提供的gdb server(这里是``JLinkGDBServerCL.exe``), 再通过编译工具链中的gdb(这里是``arm-none-eabi-gdb``)连接gdb server进行调试.

![debug_jlink.png](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=c1cbyalDMrae3IZcZdTxcndtM3fk3BW45N9VYW9GoLvlDWpOxt3gvAZJSEWUBxnF35XjGqVgCYHX-UX2EfJIYnhm4bHUurlgDS7BdCyuxZ3T6w&file_name=/debug_jlink.png)

### ``Step6.1 配置调试项``

进入调试设置

![debug1.png](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=94aeOG8cWxxyp1otIO8Bd1JyvnifVzIkpu86FLABVLfLzqfk7vSm-vzNW8SpIutDxKCGIcJJ3imppjsUDF1KELop3mxEkNzvCOfZq1A&file_name=/debug1.png)

新建调试项, 指定ELF文件.

![debug2.png](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=36b3M1W0wvzrUDTF1wKdrivFEO22R6QQbq7HmAyi-mhvzsJLTlfzADjmu78s0Vqm03Th-q2Ayv6rRKy5f_N-cp6VXroz6op-05CwPao&file_name=/debug2.png)

切换到Debugger选项卡, 设置设备名(Device Name); 由于编译过程在WSL中完成, 而调试信息使用的是绝对路径, 所以gdb在调试过程中无法对应上相应的source file, 这里在gdb client的命令中新加一条:

```
set substitute-path "WSL工程路径" "WIN工程路径"
```

举个例子, 当WIN工程路径为 "b:\abc" 时 对应的WSL工程路径为 "/mnt/b/abc", 起到路径重定向的作用.

![debug3.png](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=d08eP4W6P_ZysWHmeGcqOaeuaAEyn7YBs-pyfICTWMbR4vpa-a68_FujWeLsvo1xzUdkOSOrxF7MNGRHQcXj_CeocaViin3YbyZh3bw&file_name=/debug3.png)

P.S. 笔者猜测使用绝对路径和cmake有关, 因为cmake中的一个使用相对路径的变量``CMAKE_USE_RELATIVE_PATHS``在v3.4中取消了, 原因是"仅部分实现, 且之前的实现不可靠", 知道具体原因的朋友麻烦告知一下..

### ``Step6.2 配置环境变量``
由于建立的是Makefile Project, Eclipse不会帮我们在执行gdb时引入对应的工具链PATH, 需要手动设置: 打开``Window - Preference``, 进入``C/C++ - Build - Environment``, 添加``PATH`` 加入工具链的bin文件夹, 也就是``arm-none-eabi-gdb``所在的文件夹.

![debug_env.png](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=79666HGqjrx38PofnmkanfS94_600Rah84GxIt57rS6D0BOjYbbNWvO21_GOdHvuZGsE46GoCk3dQcrnuP_zbK8OG831wiccvtG7ZFLQs0w&file_name=/debug_env.png)

P.S. 工具链在Step5搭建Eclipse开发环境时应该已经安装好了, 这里仅用它的gdb来调试.

### ``Step6.3 尝试调试``

进入调试.

![debug4.png](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=1b8dSu_0QAJq1rR3DcKpUg7DmgDrdeca70h1DKRHuvuN_8Zj4w_fqZj_xcSmzT7XLvcnLf_J6Vp6XgUanPaLtwGQiQXNd3awY8ZJH0o&file_name=/debug4.png)

如果配置无误, 现在应该就能正常调试了:
![debug_gif.gif](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=e818a1PMIrDvVfA5s6oCUg59SMglNDaf5Wznxkw4HtaK3tzJtYeZ8WkNP3E2ZDwx__Eek_aYkhfqPUaEjNvPaq3DMup3PUaG0OuNFwdrqns&file_name=/debug_gif.gif)

---

## ``Step7 结束``

Zephyr是个好东西, 祝大家玩的开心.
