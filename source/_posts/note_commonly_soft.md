title: 我的常用软件/工作方式
date: 2018-12-03
layout: post
comments: ture
categories:
- 笔记
---

摸鱼写一篇文 记录自己觉得用起来很方便的工具还有工作方式

2015-11-26 初版
2018-12-03 更新

<!--more-->

## 系统环境

因为主业是嵌软开发，大量工具链在windows这边，所以把win作为宿主，linux放虚拟机里跑。

### win下的unix兼容环境msys2

相比cygwin，跑得更快，带包管理器，和arch用的一样pacman。
就这两项，使用起来就要舒服得多。
能用很多unix工具，比如我不会写bat脚本，有这个在win下也能用shell脚本了。

> P.S win10之后出了个WSL子系统，用途类似

### mint linux

![img](mint_in_vm.png)

体验不错的桌面环境，ubuntu的包基本都能用，免折腾。

## 日常工具

### Clover

![image](1.jpg)

~~"给资源管理器加上标签页"~~

> __P.S win8之后稳定性变差，已弃用，改用FreeCommander__

### f.lux

这玩意可以根据日落时间调节屏幕色温 减少眼睛疲劳 是个好东西
看视频的时候暂停掉就好.

### Rolan

![image](2.jpg)

快速启动工具 很好用 (也可以把它装到u盘里, 路径可以设置成自适应的.)

![image](3.jpg)

像这样, 想启动程序的时候, 热键呼出, 输入拼音首字或者英文, 回车就能启动.

有了快速启动工具，就可以放空桌面了，配合的Win+R和everything能完成大多数程序的启动。

![image](4.jpg)

### Alt Drag
按着alt键就能拖动窗口/更改大小/改变透明度之类的...很方便

### win自带的工具

calc.exe mspaint.exe charmap.exe

~~哦 还有一个win7下的截图工具(SnippingTool.exe), 名字太长了, 我把它加在rolan里了.~~

> __P.S 截图工具改用snipaste了__

### FreeCommander

![img](freecommander.png)

易用的文件管理器。

### snipaste

![img](snipaste.png)

免费截图工具，很好用。

特色是贴图功能，能把截到的图暂时“贴”到屏幕上，有时候开发需要参考，或需要把截到的几张图拼起来：

![img](snipaste-paste.png)

### everything

![img](everything.png)

快速找文件的利器，输入文件名字（支持通配符、正则表达式）能快速找到想要的文件。

### 7-zip

免费、开源的压缩解压工具，包括rar格式在内的常用档都能解，值得一提的是7z格式本身就很优秀。

### notepad++

超轻量编辑器，notepad的替代品，语法高亮，宏。

适用场景，临时改点代码。

### Beyond Compare

![image](6.jpg)
这个用来做对比很管用 
有时候需要对比文件夹差异还有手工合并一些文件..
这个能派上大用场 效率工具，是收费软件
