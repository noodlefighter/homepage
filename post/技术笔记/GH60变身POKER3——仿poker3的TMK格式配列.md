
date: 2018-10-14
categories:
- 笔记 
---

笔者kbt race2入坑 主要看重便携

后来入了poker3 非常喜欢它的初始键位设计和alt+space将右下角的四个键变成方向键的功能

然而由于它的钢板和浇铸外壳 poker3虽小巧但重量感人 
于是笔者下定决心入一块GH60再把配列改成类似poker3的方案
琢磨了一个晚上终于弄好了poker3配列 现在将他分享出来

2016-08-21 初版
2018-10-14 改进方案、增加小键盘布局，增加Github仓库链接

<!--more-->

使用方法就不多说了 关键词"gh60配列"

![image](\i\note_gh60_poker3\1.jpg)

顺手贴出相关工具网址
http://www.keyboard-layout-editor.com/
http://tkg.io/
https://github.com/kairyu/tkg-toolkit/tree/master

---

方案已放到[Github仓库](https://github.com/noodlefighter/gh60_keymap)，今后会在里面更新，Blog里就不贴了。

## 关于windows下烧写

* atmel_dfu驱动,默认win可能会使用libusb作为他的驱动，应该切换到WinUSB（用zadig）
* 避免中文路径，否则显示成功都可能没烧进去（没EEP烧写的进度）
