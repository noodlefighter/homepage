title: Nosumor 制作方法
layout: page
categories: 
---

>施工中………………

---

## 注意

* *本页对应版本为v3(Nono osu! keyboard、Nosumor)*

* *本页和资料包的照片中出现的电路板，可能和资料包里的PCB文件中的不同，这对外壳和键盘的功能不构成影响。*

* *制作资料托管在github上:*
{% link Github(Working!!!!) https://github.com/noodlefighter/osu-keyboard-v3 %}

---

## 开发人员
Noodlefighter——电路板及固件
超级叫了——外壳设计

---

## 制作步骤

购买零件
生产PCB，外壳
焊接
烧录程序
组装
 
---

## 购买零件

零件清单，详见"PCB"文件夹中“component.htm”文件

---

## 生产PCB

Garber和钻孔文件详见资料包“PCB”文件夹中“garber”文件夹。

如需要轴可插拔特性,使用与引脚尺寸匹配的毛细铜管即可,可自行更改轴的通孔尺寸重新生成garber文件.

---


## 关于外壳

我们设计了两套方案

TYPE1.铝面板+亚克力版本
{% img /osu_keyboard/v3_make/shell1.jpg 400 %}

Type2亚克力版本
{% img /osu_keyboard/v3_make/shell2.jpg 400 %}


详细制作资料参见资料包 "shell"文件夹。

---

## 烧录程序

一只典型的USB-TTL串口线：
{% img /osu_keyboard/v3_make/burn1.jpg 200 %}

预留的烧录接口支持*串口*、*SWD*等方式下载程序。
最简易的烧录方式为串口烧录，只需要一只USB-TTL电平串口转换器（如PL2303、CP2102）。

串口方式下载，接线图：
{% img /osu_keyboard/v3_make/burn2.jpg 300 %}

烧录工具为[Flash_Loader_Demonstrator](http://www.st.com/web/en/catalog/tools/FM147/CL1794/SC961/SS1533/PF257525?s_searchtype=keyword)，需要用到的引脚VCC/GND/BOOT0/RXD/TXD，BOOT0需要和VCC连在一起，Nosumor上的RXD、TXD分别连接串口的TXD、RXD，请注意VCC为+5v

需要更详细的指导，请转至：
[详细过程参考](http://www.scienceprog.com/flashing-programs-to-stm32-embedded-bootloader/)

---

## 组装

键盘外壳设计简洁，参考“关于外壳”部分的分解图即可。

*关于脚贴*

{% img /osu_keyboard/v3_make/foot.jpg 350 %}

由于键盘重量和体积都较小，脚贴的可靠程度对键盘十分重要。

方案A.防滑硅胶(图左)
适合光滑的桌面(如玻璃桌面)

方案B.粘性的pu胶脚垫(图右)
适合多种桌面表面(如木质桌面)

---

## 配置

{% img /osu_keyboard/v3_make/setting.jpg 450 %}

成功烧写程序后，键盘已经可以正常工作，若需进行个性设置，可尝试以下步骤：
1. 同时按下按键1、按键2，并将键盘重新接入电脑
2. 若可以看见背景灯的蓝灯闪烁，即已进入设置模式。
3. 确认键盘背景灯闪烁后，打开专用设置工具，进行配置，写入配置后，拔除键盘再重新接入电脑即可生效设置。

--- 


