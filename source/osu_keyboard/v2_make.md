title: Nooldefighter osu Keyboard v2.1 制作方法
layout: page
categories: 
---

{% img /osu_keyboard/v2_make/v2.jpg 600 %}

# 介绍

* 造价: 约45RMB
* 樱桃MX系列机械按键
* 扫描频率1000Hz
* 实测传输延迟：6-10ms
* 三个键均可设置成预置的按键（ESC/F1/F2/F8/F12/space/enter，zx zc as ad PageUp/down 上下 左右）
* 可变色LED作为手速指示器
* 闲置15sec，可变色LED变为闲置背景色，背景色可方便的设置
* 4个可设置的按键灯工作状态（一直亮/一直灭/按下时点亮/按下时熄灭）

# 制作材料、所需工具清单

{% img /osu_keyboard/v2_make/material1.jpg 500 %}
{% img /osu_keyboard/v2_make/material2.jpg 500 %}
{% img /osu_keyboard/v2_make/material3.jpg 500 %}

## 电子元件

Name|封装|标号|数量|说明
----|----|----|----|----
PCB|5*5cm|/|1|见“关于pcb”
Atmega48PA|32PIN TQFP|U1|1|主控芯片
MINI USB Female|B-TYPE 5P 90degree|USB|1| 
zener diode 3.6v|1206|D1 D2|2|稳压管
resistance 271（270Ω）|0805|R7 R8 R9|3|电阻
resistance 102（1000Ω）|0805|R5|1|电阻
resistance 680（68Ω）|0805|R3 R4|2|电阻
resistance 471（470Ω）|0805|R1 R2|2|电阻
capacitance 220 （22pf）|0805|C1 C2|2|电容
capacitance 104 （0.1uf）|0805|C4|1|电容
capacitance 227 (220uf)|6032|C3|1|钽电容
RGBLED|5050|RGBLED|1|三基色彩色led
microswitch 普通微动开关|6*6*8MM|BT3|1| 
CHERRY MX Switch|/|BT1 BT2|2|樱桃按键
3mm LED|3mm| |2|BT1,BT2的可选按键灯
无源晶振|20Mhz|Y1|1| 

## 外壳相关
Picture|Name|count|说明
-------|----|-----|----
{% img /osu_keyboard/v2_make/material4.jpg 60 %}|screw M3*12mm|4|螺丝 固定外壳
{% img /osu_keyboard/v2_make/material5.jpg 60 %}|nut M3|4|普通螺母 固定外壳
{% img /osu_keyboard/v2_make/material6.jpg 60 %}|screw M3*10mm|4|螺丝 固定pcb
{% img /osu_keyboard/v2_make/material7.jpg 60 %}|Non-slip nuts M3|4|防滑螺母 固定pcb

## 其他

Name|count|说明
----|-----|----
cherry mx switch keycap R3|2|樱桃轴键帽，R3高度
microswitch keycap	|1|微动按键键帽
silicone gasket 2mm	|1|防滑硅胶垫 带背胶 粘贴于底部用于防滑


## 必要的工具

Name|count|说明
----|-----|----
AtmelISP|1|烧录程序用
screwdriver|1|十字螺丝刀 组装用
plier|1|钳子 装防滑螺母时需要用到

---

{% img /osu_keyboard/v2_make/pcb1.jpg 600 %}
{% img /osu_keyboard/v2_make/pcb2.jpg 600 %}

# 关于PCB

键盘usb通讯部分的实现方法是使用V-USB开源库（http://www.obdev.at/products/vusb/）。
这里提供Altium Designer 10的pcb文件（"PCB\OSUpcb.PcbDoc"）以及生成好的GERBER文件("PCB\GERBER\")
你需要联系pcb厂商生产该电路板。
元件清单在“制作材料、所需工具清单”中。

---

{% img /osu_keyboard/v2_make/shell.jpg 600 %}

# 关于外壳

外壳由亚克力板激光切割制成，请将矢量图文件（"Shell\standard.dwg",AutoCAD2000文件，文件中图形单位为mm）送交工厂。
注意：图样需要分别使用3mm/2mm厚压克力板雕刻，请注意矢量图里的标注。
P.S.关于mini外壳（"Shell\mini.dwg"）:这个类型的外壳在这个版本尚未完善，外壳强度不高，请谨慎使用。

---

# 其他的材料

1. 硅胶带背胶防滑垫
2. 樱桃轴获得方法：
* 向OEM商购买流出的少量按键
* 从旧键盘上拆下樱桃按键

---

{% img /osu_keyboard/v2_make/burn1.jpg 350 %}
(atmelISP)
{% img /osu_keyboard/v2_make/burn2.jpg 350 %}
（Fuse）
{% img /osu_keyboard/v2_make/burn3.jpg 350 %}
（ISP Define）

# 关于avr芯片上的程序

编译好的hex文件："Prog\m48key.hex"
ISP口为精简的6PIN ISP，请参考图“ISP Define”
熔丝位设置：
* CKDIV8=1
* CKSEL=1110
* SUT=10

P.S.这个程序参照了一个叫C64 Keyboard的开源键盘.向原作者致敬！

---

# 组装方法

{% img /osu_keyboard/v2_make/assemble_chs.jpg 600 %}

组装可参考工程包里的“assemble_chs_eng.doc”（中/英文）

也参考组装演示视频（中文字幕） http://www.tudou.com/programs/view/sbXESmsUZPg

* 以下为硅胶防滑垫贴的推荐贴法
{% img /osu_keyboard/v2_make/assemble_post_method.jpg %}

---

# 设置说明

# 直接设置项目
设置保存在键盘内部，不会由于断电或更换电脑而消失。
设置过程中，为方便查看效果，需要使用一个免费工具Keyboard Test Utility.
上方两颗键为“BT1 BT2”，将下方一颗键称为“BT3”，长按的意思为“按下0.5sec”

BT3设置方法——先同时按下BT1 BT2，再长按BT3
BT1/2设置方法——先同时按下BT2 BT3，再长按BT1
闲置时背景光设置方法——先同时按下BT1 BT3，再长按BT2

可参考视频(中文字幕) http://www.tudou.com/programs/view/mSUck6N8cYk

# PCB上设置项目

JP（pcb跳线）两端接通为1，断开为0.

JP2|JP1|按键光
---|---|------
0|0|常暗，按下变亮（默认）
0|1|常亮
1|0|常亮，按下变暗
1|1|不亮

注意
关于按键灯的安装方向：从pcb顶端来看，LED正极（长脚）应该在左手边，焊接led前请先烧程序测试，测试led是否正常工作。

---

# 美化方式

{% img /osu_keyboard/v2_make/beautiful1.jpg 300 %}
{% img /osu_keyboard/v2_make/beautiful2.jpg 300 %}

透明的亚克力板很单调吧，这里推荐2种美化方案：
1. 使用彩色亚克力板
2. 水转印图样（水转移纸：中文wiki 英文wiki），喷上油漆固定