title: linux驱动开发学习 读LED驱动
description: 
date: 2019-1-8
updated: 2019-1-8
layout: post
comments: true
categories:
- 嵌入式软件
tags:
- linux
- driver
---

Light the LED！

<!--more-->

---

## 资料

首先当然是看手册，[`Documentation\leds\leds-class`](https://github.com/torvalds/linux/blob/master/Documentation/leds/leds-class.txt)里给了很多提示：

（以下为咕哥翻译）

> Linux下的LED控制
> =========================
> 
> 在最简单的形式中，LED类只允许控制用户空间的LED。 LED出现在`/sys/class/leds/`中。 LED的最大亮度在`max_brightness`文件中定义。亮度文件将设置LED的亮度（取值0-max_brightness）。大多数LED没有硬件亮度支持，因此只需打开非零亮度设置。
> 
> 该课程还介绍了LED触发器的可选概念。触发器是基于内核的led事件源。触发器可以是简单的也可以是复杂的。简单的触发器是不可配置的，旨在以最少的附加代码插入现有的子系统。例子是磁盘活动，nand-disk和sharpsl-charge触发器。禁用LED触发器后，代码将被优化掉。
> 
> 所有LED均可使用的复杂触发器具有LED特定功能
> 参数和每个LED工作。定时器触发器就是一个例子。
> 定时器触发器将周期性地改变`LED_OFF`和当前亮度设置之间的LED亮度。 “on”和“off”时间可以通过`/sys/class/leds/<device>/delay_{on，off}`指定，以毫秒为单位。
> 您可以独立于定时器触发器更改LED的亮度值。但是，如果将亮度值设置为LED_OFF，它也将禁用定时器触发器。
> 
> 您可以通过与选择IO调度程序的方式类似的方式更改触发器（通过`/sys/class/leds/<device>/trigger`）。一旦选择了给定的触发器，触发器特定参数可以出现在`/sys/class/leds/<device>`中。
> 
> 
> 设计哲学
> =================
> 
> 基本的设计理念是简单。 LED是简单的设备，目的是保持少量代码提供尽可能多的功能。 建议增强功能时请记住这一点。
> 
> 
> LED设备命名
> =================
> 
> 目前的形式是：
> 
> ```none
> "devicename:colour:function"
> ```
> 
> 已经要求将诸如颜色的LED属性导出为单独的led类属性。 作为一个不会产生太多开销的解决方案，我建议这些成为设备名称的一部分。 如果需要，上面的命名方案留下了进一步属性的范围。 如果名称的部分不适用，请将该部分留空。
> 
> 亮度设置API
> ======================
> 
> LED子系统核心公开以下用于设置亮度的API：
> 
> - `led_set_brightness`：保证不睡觉，传递LED_OFF停止闪烁，
> - `led_set_brightness_sync`：对于需要立即生效的用例 - 它可以阻止调用者访问设备寄存器所需的时间并且可以休眠，传递LED_OFF会停止硬件闪烁，如果启用了软件闪烁回退，则返回-EBUSY。
> 
> 
> LED注册API
> ====================
> 
> 想要注册LED classdev以供其他驱动程序/用户空间使用的驱动程序需要分配和填充`led_classdev`结构，然后调用`[devm_] led_classdev_register`。如果使用非devm版本，驱动程序必须在释放`led_classdev`结构之前从其`remove`函数调用`led_classdev_unregister`。
> 
> 如果驱动程序可以检测硬件启动的亮度变化并因此想要具有`brightness_hw_changed`属性，则必须在注册之前在标志中设置`LED_BRIGHT_HW_CHANGED`标志。在未使用`LED_BRIGHT_HW_CHANGED`标志注册的`classdev`上调用`led_classdev_notify_brightness_hw_changed`是一个错误，将触发`WARN_ON`。
> 
> 硬件加速LED闪烁
> ==================================
> 
> 某些LED可以编程为闪烁而无需任何CPU交互。要支持此功能，LED驱动程序可以选择实现`blink_set()`函数（请参阅<linux/leds.h>）。但是，要将LED设置为闪烁，最好使用API函数`led_blink_set()`，因为它会在必要时检查并实现软件回退。
> 
> 要关闭闪烁，请使用亮度值为`LED_OFF`的API函数`led_brightness_set()`，它应该停止闪烁所需的任何软件定时器。
> 
> 如果使用`*delay_on==0 && *delay_off==0`参数调用`blink_set()`函数，则应选择用户友好的闪烁值。在这种情况下，驱动程序应通过`delay_on`和`delay_off`参数将所选值返回给leds子系统。
> 
> 使用`brightness_set()`回调函数将亮度设置为零应完全关闭LED并取消之前编程的硬件闪烁功能（如果有）。



