title: GH60变身POKER3——仿poker3的TMK格式配列
date: 2016-08-21
layout: post
comments: ture
categories:
- 笔记 
---

笔者kbt race2入坑 主要看重便携

后来入了poker3 
非常喜欢它的初始键位设计和alt+space将右下角的四个键变成方向键的功能

然而由于它的钢板和浇铸外壳 poker3虽小巧但重量感人 
于是笔者下定决心入一块GH60再把配列改成类似poker3的方案
琢磨了一个晚上终于弄好了poker3配列 现在将他分享出来
使用方法就不多说了 关键词"gh60配列"

![image](\i\note_gh60_poker3\1.jpg)

顺手贴出相关工具网址
http://www.keyboard-layout-editor.com/
http://tkg.io/

---

这个方案 基于poker3默认方案有如下改动:
* 将Capslock和原Fn位置对调, 右alt改成Fn
* 将Pn换成Menu (虽然觉得多余因为Fn+Z作用相同 但这个键位比较偏 不知改成什么合适)
* 取消Fn+Y打开calc.exe, Fn+A改为Ctrl+Shift+Esc(因为Ctrl+Shift+Esc实际打出的是Ctrl+Shift+~)
* 由于对灯光不感冒 灯控相关功能没加
* Fn+g为'_' Fn+t='=' Fn+v='-', 码代码时方便.. 下划线风格右手小拇指压力大
* 从Fn8开始设置了一些eclipse下的快捷键所以用不着的可以自行删掉

![image](\i\note_gh60_poker3\2.jpg)

```
GH60仿Poker3配列 ver.3 (2016/08/21)

Fn0-Fn7 对应L0-L7
L0	一般					
L1	一般+方向键层		开关式
L2	保留
L3	fn层
L4	fn层+空格为L1层开关

普通功能从Fn8开始
Fn31为Tricky Esc功能, 使Shift+Esc实际按出Shift+~

L0
["Fn31","!\n1","@\n2","#\n3","$\n4","%\n5","^\n6","&\n7","*\n8","(\n9",")\n0","_\n-","+\n=",{w:2},"Backspace"],
[{w:1.5},"Tab","Q","W","E","R","T","Y","U","I","O","P","{\n[","}\n]",{w:1.5},"|\n\\"],
[{w:1.75},"Fn3","A","S","D","F","G","H","J","K","L",":\n;","\"\n'",{w:2.25},"Enter"],
[{w:2.25},"Shift","Z","X","C","V","B","N","M","<\n,",">\n.","?\n/",{w:2.75},"RShift"],
[{w:1.25},"Ctrl",{w:1.25},"Win",{w:1.25},"Alt",{w:6.25},"Space",{w:1.25},"Fn4",{w:1.25},"Caps Lock",{w:1.25},"Menu",{w:1.25},"RCtrl"]

L1 方向键
[{a:7},"","","","","","","","","","","","","",{w:2},""],
[{w:1.5},"","","","","","","","","","","","","",{w:1.5},""],
[{w:1.75},"","","","","","","","","","","","",{w:2.25},""],
[{w:2.25},"","","","","","","","","","","",{a:4,w:2.75},"↑"],
[{a:7,w:1.25},"",{w:1.25},"",{w:1.25},"",{w:6.25},"",{w:1.25},"",{a:4,w:1.25},"←",{w:1.25},"↓",{w:1.25},"→"]

L2 保留
[{a:7},"","","","","","","","","","","","","",{w:2},""],
[{w:1.5},"","","","","","","","","","","","","",{w:1.5},""],
[{w:1.75},"","","","","","","","","","","","",{w:2.25},""],
[{w:2.25},"","","","","","","","","","","",{w:2.75},""],
[{w:1.25},"",{w:1.25},"",{w:1.25},"",{w:6.25},"",{w:1.25},"",{w:1.25},"",{w:1.25},"",{w:1.25},""]


L3 Fn层
["~\n`","F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12",{w:2},"Delete"],
[{a:7,w:1.5},"",{a:4},"Fn8","Fn9","Fn10","Fn11","Fn12","Fn13","PgUp","↑","PgDn","PrtSc","Scroll Lock","Pause\nBreak",{w:1.5},"Fn14"],
[{a:7,w:1.75},"",{a:4},"Fn15","VolDn","VolUp","Mute","Fn16","Home","←","↓","→","Insert","Delete",{a:7,w:2.25},""],
[{w:2.25},"",{a:4},"App","Fn17","Fn18","Fn19","Fn20","End","Fn21","Fn22","Fn23","Fn24",{w:2.75},"RShift"],
[{a:7,w:1.25},"",{w:1.25},"",{w:1.25},"",{a:4,w:6.25},"Space",{a:7,w:1.25},"",{a:4,w:1.25},"Caps Lock",{w:1.25},"Fn2",{w:1.25},"RCtrl"]


L4 Fn层 空格为L1层开关
["~\n`","F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12",{w:2},"Delete"],
[{a:7,w:1.5},"",{a:4},"Fn8","Fn9","Fn10","Fn11","Fn12","Fn13","PgUp","↑","PgDn","PrtSc","Scroll Lock","Pause\nBreak",{w:1.5},"Fn14"],
[{a:7,w:1.75},"",{a:4},"Fn15","VolDn","VolUp","Mute","Fn16","Home","←","↓","→","Insert","Delete",{a:7,w:2.25},""],
[{w:2.25},"",{a:4},"App","Fn17","Fn18","Fn19","Fn20","End","Fn21","Fn22","Fn23","Fn24",{w:2.75},"RShift"],
[{a:7,w:1.25},"",{w:1.25},"",{w:1.25},"",{a:4,w:6.25},"Fn1",{a:7,w:1.25},"",{a:4,w:1.25},"Caps Lock",{w:1.25},"Fn2",{w:1.25},"RCtrl"]

TKG设置:
"1":["ACTION_LAYER_TOGGLE",1],"2":["ACTION_LAYER_ON","2","ON_PRESS"],"3":["ACTION_LAYER_MOMENTARY","3"],"4":["ACTION_LAYER_MOMENTARY","4"],"8":["ACTION_MODS_KEY","LR_LEFT",["MOD_ALT"],"KC_LEFT"],"9":["ACTION_MODS_KEY","LR_LEFT",["MOD_ALT"],"KC_RIGHT"],"10":["ACTION_MODS_KEY","LR_LEFT",["MOD_CTL"],"KC_K"],"11":["ACTION_NO"],"12":["ACTION_KEY","KC_EQUAL"],"13":["ACTION_NO"],"14":["ACTION_NO"],"15":["ACTION_NO"],"16":["ACTION_MODS_KEY","LR_LEFT",["MOD_SFT"],"KC_MINUS"],"17":["ACTION_NO"],"18":["ACTION_NO"],"19":["ACTION_KEY","KC_MINUS"],"20":["ACTION_NO"],"21":["ACTION_NO"],"22":["ACTION_NO"],"23":["ACTION_NO"],"24":["ACTION_NO"],"31":["ACTION_FUNCTION",0,0]

```

