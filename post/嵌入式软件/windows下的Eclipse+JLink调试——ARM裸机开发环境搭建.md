date: 2017-12-06
tags: 

- ARM
- eclipse
---

在公司用着eclipse感觉挺不错
调试起来比emblock要舒服
用eclipse+arm-gcc+JLink的人越来越多了吧
仅记录一下配置方法

<!--more-->

另外可以参考这一篇
http://www.emb4fun.de/archive/eclipse/index.html

更新记录
2016/08/21 补上遗漏的"Build tools安装"部分
2017/12/06 gnuarmeclipse已经改名为gnumcueclipse了 而且提供了打包好的"GNU MCU Eclipse IDE for C/C++ Developers" 修改几处不严谨的说法 调试部分

---

## IDE及编译环境搭建

### 0. 国内网络情况的提示
由于你知道的原因, 下载github中的压缩包时可能不顺畅, 请自备代理.

### 1. 安装JRE
http://www.java.com/en/download/manual.jsp
Eclipse需要在JVM下运行
安装完JRE需要配置环境变量 让PATH包含JRE的bin目录


### 2. 下载GNU MCU Eclipse IDE for C/C++ Developers并解压
GNU MCU Eclipse插件使Eclipse支持众多的目标微控制器的开发调试. [这里是它的主页](https://gnu-mcu-eclipse.github.io/)

它的作者整合打包了一份Eclipse, 我们就不用自行安装插件了, 下载地址:
https://github.com/gnu-mcu-eclipse/org.eclipse.epp.packages/releases/

下载压缩包 64位系统建议选择``win32.x86_64`` 32位系统选择``win32.x86`` eclipse选x86或x64必须和JRE相同 否则无法运行
如果提示没有安装JRE 可以尝试重启及检查PATH环境变量有没有包含JRE路径

### 3. 下载arm工具链(GNU ARM Embedded Toolchain)
https://launchpad.net/gcc-arm-embedded
工具链包括编译器(gcc)/调试器(gdb)等一系列目标平台相关的工具, 以实现交叉编译.
这里解释一下工具链名称前缀``arm-none-eabi-``:
```
arm: ARM平台
none: 目标系统, 裸机程序开发用none
eabi: ABI是应用程序二进制接口, EABI是Embedded application binary interface, 是一套规范, 我们只需要知道符合eabi规范的编译器间生成的库能互相连接就足够了.
```

### 4. windows下的Build tools安装

https://github.com/gnu-mcu-eclipse/windows-build-tools/releases

Build Tools主要为windows提供unix中一些构建相关的基本工具, 比如make, 它可以通过读取makefile脚本调用以上工具链来完成编译.

P.S. makefile脚本可以由Eclipse的CDT插件自动生成, 也可以由autotools,cmake等更高级的构建工具生成, 一般不手工编写.
![1](_assets/windows下的Eclipse+JLink调试——ARM裸机开发环境搭建/1.png)

P.S.
如果Build Tools无法在你的环境中正常工作 你可以选择使用MSYS2作为这里的Build Tools.

### 5. Eclipse中的设置
菜单``Windows - Preferences``进入设置.

``MCU - Global Build Tools Path``填入之前安装好的Build Tools路径
``MCU - Global ARM Toolchains Path``填入之前安装好的工具链路径

到这里应该可以正常编译了

### 6. 尝试编译helloworld
新建C Project, 选择
![2](_assets/windows下的Eclipse+JLink调试——ARM裸机开发环境搭建/2.png)

菜单"Build - Build Project"编译, Console中出现以下输出则环境配置成功:
![3](_assets/windows下的Eclipse+JLink调试——ARM裸机开发环境搭建/3.png)

---

## Jlink调试

### 1. 安装jlink软件包
https://www.segger.com/jlink-software.html
``J-Link Software and Documentation Pack``中下载新版驱动
有时候新版本驱动无法很好地和eclipse中调试插件共同工作, 可以尝试使用稍旧的版本.

### 2. Debug设置
进入Debug Configurations 双击"GDB SEGGER J-Link Debugging"创建新的debug设置
这里检查下``C/C++ Application``、``Device name``是否都填上:
```
C/C++ Application: 编译好的ELF文件
Device name: 目标器件名字 可以去这里查找 https://www.segger.com/downloads/supported-devices.php
```
如果你不关心semihosting和swo的用途 建议先把相关选项关掉 比如Debugger中``Allocate console for semihosting and SWO`` Startup中``Enable SWO`` ``Enable semihosting``

### 3. 尝试调试
配置完成后尝试运行调试, 如果配置正确, eclipse会帮你启动一个jlink gdb server以及gdb client, 如果能进行单步调试等操作, 说明配置成功.

P.S. 使用OpenSDA等其他调试器的环境搭建 可以参考[这篇文章](http://noodlefighter.com/%E5%B5%8C%E5%85%A5%E5%BC%8F%E8%BD%AF%E4%BB%B6/em_cmsis_dap_eclipse)
