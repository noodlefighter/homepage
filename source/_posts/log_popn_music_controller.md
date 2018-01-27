title: 自制Pop'n Music 控制器制作资料(手台)
description: 
date: 
layout: post
comments: ture
categories:
- 工作日志
tags: 
- 键盘
- popn
- 音游
---

## 台子

某宝Popn手台含邮1200往上走 于是就有了自己动手做个料足好使的台子的想法

![IMG_20170930_222520.jpg](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=8023Z_OUqy0U_FNbRaoI0EeWGvni9YnlzcbRAvW5JsLGuwwjv9oWgc6SaCAvreM_1tQMA1LU_-S4OxBMTUCRxOkogdLgs4mtmXQiYZgEAMx3_sRFkkE8EVAblFNmmeNZXt8&file_name=/IMG_20170930_222520.jpg)

![IMG_20170930_222436.jpg](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=6287HPuX_p5x8qDRr-ZTR4zWuzTIBq0Zn_GbdYgNUxiH-JXbQ2hZGM1Q-YkuEC8ymJoYAAMaTc3ihDgCntzyg5f50h9BLhrd3iSlYAkjxCn9xgsTCE0ZSc4YaAUreJp5ZRA&file_name=/IMG_20170930_222436.jpg)

## 制作资料

这里就只放制作资料 供动手能力强的人参考

### 物料单
外壳及连接件 
1. 订制木框(木板厚15mm)
2. 亚克力顶板*2 + 底板*1
3. 内外牙预埋M4*8螺母*24个+平头手拧M4*16螺丝*24个

按钮及改造用元件
1. 某仿三和90g弹簧*9
2. OMRON V-10-1A4 *9
3. 国产按钮*9

电路板部分
1. STM32F103C8T6最小系统板*1 (主控 烧上TMK的固件就能用) + 适合长度的micro-usb线*1
2. 双面喷锡洞洞板*1
3. 预做好的4P的XH2.54电子端子线*9条+6.3mm插簧接线端子(带硅胶保护头)*36只
4. 20p的2.54mm排针*1
5. 4P的XH2.54直插座*9

附件/耗材/用到的工具:
1. 带背胶的硅胶脚垫12.7*6mm*6个
2. 240/400/600目砂纸 用于调教国产按钮
3. 润滑膏
4. 尖嘴钳 用于做线

### 外壳制作
这里的外壳方案为双层面板+木框+单层底板, 使用M4的预埋螺母+手拧螺丝, 其实可以把木框的底部封了, 可以省下底板的费用同时更省事.

设计参考dwg: [下载](../i/log_popn_music_controller/shell_recover.zip)

![IMG_20170930_122727.jpg](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=e37ezUG0P-hWCupc1-la2qi8rMzVGcjZIQdSeZospeu8bFer7p90qeE7Tv6kpoofYPFryyfDrwC75AchphMU0vDnwVnxJbqjoLQbyAcXEZDmlFaB8bhpHxSLSrdGHQe_hJQ&file_name=/IMG_20170930_122727.jpg)![IMG_20170930_124903.jpg](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=af16t4svKw1nCPrQd3IreyHyFJY7e49wdwbjL1mf4N4pifrkOmpaRPvjEJL8svarqB8SbCsGDVRynYWMUOJvGtK4BXI0XO4_FGI-xe-D6xvCIF3OTXNfQr3gsqEn7m4cxNA&file_name=/IMG_20170930_124903.jpg)

### 关于主控板
为了省事就没设计专门的PCB 直接用现成的核心板+洞洞板来怼 灯光也直接常亮

#### 固件
我这里用[TMK的固件](https://github.com/tmk/tmk_keyboard/tree/master/tmk_core):
https://github.com/noodlefighter/popn_controller
Release里有编译好的HEX格式固件, 直接用烧录工具烧写进去即可...
比如用串口方式..只需要一个USB-TTL线配合Flash_Loader_Demonstrator工具即可完成烧写.. 自行搜索"stm32 串口下载"

固件效果就是把GPIO的PA0-PA7, PB0, PB1共9个IO口变成按键输入的管脚, 电平拉低时表示按钮按被下, 通过固件实现的标准的USB-HID免驱键盘设备发送到电脑上(对应按键ASDFGHJKL)

### 按键的调整
好的按键价格很高 建议买一般的国产按键自己调整:
1. 更换合适的微动开关
2. 更换合适的弹簧, 重新上润滑油
3. 处理卡键问题, 差的按键做工不好, 容易卡键, 得用砂纸从低目到高目慢慢处理..

![IMG_20170827_143440.jpg](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=fb0787OkqyKWEvcf2GE_y0Q2uq3qKFBmt05D2VVfpZFglUjmHZKPb2-rdQ5ZR6ECG-kJ6yp_zxKyJsryHY88tdtZd8kCe-L0Y3R1tix_kRoYomSLu-azElRjQiUI25XQAnE&file_name=/IMG_20170827_143440.jpg)
![IMG_20170827_140653.jpg](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=7b3aR7PiUOjq69T5TBP5hcZbgNWdhF_xodDyGipJ7F9LUp8ljg3PKUOvOxhBfcXndh28nFisz1HylNZuaCBHOwXa9gqGen5ybDEI5ivzH6XwLJA4mHMN2tFRSvcbPKMBZdo&file_name=/IMG_20170827_140653.jpg)


#### 硬件
板子制作起来很简单 就是把核心板上的IO引出到直插接插件上 方便接线
![IMG_20170910_125356.jpg](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=fa05FQCRuCWm2hPeweeE-hlOuUv5GSDvkduVp09XUbXX6ozV5Is39E1LkFTjszPEJlrNoarwXNvFEkOvtUF0nnZrF7gEsT5yDiF_hMokBJWS4IM76-8A6qInOHXAmRXcy8c&file_name=/IMG_20170910_125356.jpg)
![IMG_20170910_142908.jpg](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=5fe6YeMidz4lmuMmy3aBYmBDNiXg4ABQ6NiKCPKtDqnogrndcl-t8sQv8QCz5LNCtpTxNiWfSJYBoOhnrZIG7G6ib-BIr1encnv5d5Ffk1nHN-tirAjinCMIb3Yly7C4AmQ&file_name=/IMG_20170910_142908.jpg)
![IMG_20170910_142122.jpg](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=cb20cC-XGvsAzWMEDT7b_2gkCreARRaIOY2v-psgNka7GBW9kPjVqTeNnH4STHfBoZ8E9nGlIlntS3Ya-bntHAh9ebad1uoEqtVSPVu5Sz7rZ19-yzDkYj6zUIJs9qBFJhQ&file_name=/IMG_20170910_142122.jpg)
![IMG20170910175610.jpg](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=8380ufprSFImHfEvIu0ME_3bkdMGD3n4Zp4LBS7EQ-X-p_Akser8PfiezkSV-hf6cixdoDX5ZgxFNt2XiIKVy-L5dublAj9rpwtVKexHRoyvWZ8f9HksKfCfNdUsUJwv&file_name=/IMG20170910175610.jpg)

![IMG_20170910_175048.jpg](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=e311o_1CNmGlPaKlYRO9TUD09yBk7hoQrM4iLFpPqUyuiq3TPmfWYnsnQIZHopeoxHZQcBBDWRMbSWv6O0HSH_x2QSCT1ZL-2lAgfdewauuY4JFUb1sD3JlBraVHeRplkvs&file_name=/IMG_20170910_175048.jpg)
![IMG_20170930_220102.jpg](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=8684MC4ngIeXf7bySvc5TL1zAT92ZFX1qF5r6ALjMZ-ccAqutCNka2h-H1amQNiVog5EuptY2iELGoekKvCFvVm1dt45vx22tZGkz-qbf6wZRR3de6IqQu53asulsmKpa3o&file_name=/IMG_20170930_220102.jpg)


## 于是
我也是有手台的人了(溜..)
![IMG20170924000132.jpg](http://lolipan.noodlefighter.com/index.php?user/publicLink&fid=93a0to7nhqc6pwm2dGjNDiT2jsAXvi5jUa6RhM1-KL-UUbxVRjjUAQW8skyxfI3Y3VSYqJfn1Da_pBtAjrq3XNQBU1NqW624TP1qBaU5zTaTIjy-rsz7RJpbaliBnLfA&file_name=/IMG20170924000132.jpg)