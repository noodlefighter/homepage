
date: 2016-08-21
---

购入CMSIS-DAP仿真器 摸索摸索（抛弃盗版Jlink的日子要来了..
这里记录win下使用eclipse+openOCD+cmsis_dap调试arm程序的配置方法 

<!--more-->

![00](_assets/在eclipse中使用openOCD+CMSIS_DAP进行ARM在线调试/00.jpg)

---

## Step.0 准备原料
* CMSIS-DAP标准的仿真器
* [openOCD](https://sourceforge.net/projects/openocd/files/openocd/0.9.0/)

## Step.1 安装eclipse+gnuarmeclipse插件
请参考之前的[这一篇文章](http://noodlefighter.com/%E5%B5%8C%E5%85%A5%E5%BC%8F%E8%BD%AF%E4%BB%B6/em_eclipse_arm/)的前半部分


## Step.2 编译openOCD
eLinux有篇wiki供参考
http://elinux.org/Compiling_OpenOCD_Win7

笔者是直接用网友编译好的
![01](_assets/在eclipse中使用openOCD+CMSIS_DAP进行ARM在线调试/01.jpg)

## Step.3 设置openOCD路径
eclipse中 Window - Preferences - Run/Debug - OpenOCD
填入文件名和路径 例如:
```
Executable: openocd-0.8.0.exe
Folder: A:\cli_tools\openocd-0.8.0\bin
```

## Step.4 调试设置
进入Debug Configurations 双击"GDB OpenOCD Debugging"创建新的debug设置 

Debugger选项卡 OpenOCD Setup中的Config options设为:
```
-f ${openocd_path}/../scripts/interface/cmsis-dap.cfg  -f ${openocd_path}/../scripts/target/stm32f1x.cfg
```
这里得根据openOCD的目录结构来稍微改一下 总之得把调试器和目标配置cfg文件用上(这里以stm32f1x为例)
可以先自己在命令行中试试

在Startup选项卡 Run/Restart Commands中 取消Pre-run/Restart.复选框

这是我的配置, 仅供参考 

![02](_assets/在eclipse中使用openOCD+CMSIS_DAP进行ARM在线调试/02.jpg)

![03](_assets/在eclipse中使用openOCD+CMSIS_DAP进行ARM在线调试/03.jpg)

![04](_assets/在eclipse中使用openOCD+CMSIS_DAP进行ARM在线调试/04.jpg)

## Step.5 尝试调试
若成功调试则万事大吉
若调试失败 
请注意检查工程配置中C/C++ Build - Settings - Tool Settings - Debugging中调试等级有没有打开

![05](_assets/在eclipse中使用openOCD+CMSIS_DAP进行ARM在线调试/05.jpg)
