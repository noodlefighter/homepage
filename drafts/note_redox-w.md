

## 接收器

### pro micro部分



编译[QMK固件](https://github.com/mattdibi/qmk_firmware/tree/redox_wireless/keyboards/redox_w)

windows下用arduino自带的avr-gcc
linux下装avr-libc和avr-gcc

```
make redox_w:default
```

烧录

这货复位后有8s时间在boot里,或者一些boot快速双击rst键就能进boot.

```
# 官方例子
make redox_w/rev1:default:avrdude

# 但应该是这样才能编译，但没成功，提示avrdude的conf文件没找到
make redox_w:default:avrdude

# 最后这样成功了，而且得在cmd.exe里才行，不然串口硬件匹配不到
a:\arduino-1.8.5\hardware\tools\avr\bin\avrdude -p atmega32u4 -c avr109 -U flash
:w:redox_w_default.hex -P //./COM13 -C"A:\arduino-1.8.5\hardware\tools\avr\etc\avrdude.conf"
```

修改配列
https://config.qmk.fm/#/redox_w/LAYOUT

linux下烧固件
```
sudo avrdude -p atmega32u4 -c avr109 -U :w:redox_w_redox_w_layout_mine.hex -P /dev/ttyUSB0
```