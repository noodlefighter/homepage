title: ARM BKPT指令和半主机(Semi-hosting)模式实现的研究
description: 
date: 2017-08-09
layout: post
comments: ture
categories:
- 嵌入式软件
---

今日排虫遇到了BKPT指令, 研究发现它和调试器有很大关系, 简单研究研究.

<!--more-->

起因
==============

今日排虫遇到了这个BKPT指令
调试点对点无线通讯 然而只有一台J-Link调试器 所以需要在两台目标板间不断切换
插拔插拔 
问题突然就来了 一板子跑着跑着就死掉了
于是重新接上调试器 想查看它死在了哪里 
发现程序停在了一个曾经下过断点的位置
对应的指令为

```
BKPT 0x0000
```

经过各种调查研究 发现它和调试器的"Flash breakpoints"功能有关,先给出结论: 
J-Link的这个Flash breakpoints功能是通过BKPT指令实现的, 使能一个Flash断点, 调试器就在对应的目标程序地址的指令改写成BKPT, 踩到该指令后程序停止运行, 用户继续运行时将指令还原, 恢复现场继续运行.

这里记录一下探索过程和BKPT相关知识

BKPT啥玩意儿
==============

查看[ARM汇编参考手册](http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.dui0489i/Cihbiggi.html)得到以下信息:
```
BKPT
    Breakpoint.
Syntax
    BKPT #imm
where:
    imm
        is an expression evaluating to an integer in the range:
            0-65535 (a 16-bit value) in an ARM instruction
            0-255 (an 8-bit value) in a 16-bit Thumb instruction.
Usage
    The BKPT instruction causes the processor to enter Debug state. Debug tools can use this to investigate system state when the instruction at a particular address is reached.
    In both ARM state and Thumb state, imm is ignored by the ARM hardware. However, a debugger can use it to store additional information about the breakpoint.
    BKPT is an unconditional instruction. It must not have a condition code in ARM code. In Thumb code, the BKPT instruction does not require a condition code suffix because BKPT always executes irrespective of its condition code suffix.
    
Architectures
    This ARM instruction is available in ARMv5T and above.
    This 16-bit Thumb instruction is available in ARMv5T and above.
    There is no 32-bit version of this instruction in Thumb.
```

总之BKPT就是个ARMv5T之后加入的中断指令: 当程序运行到这个指令所在的地址时 处理器进入Debug状态 调试工具可以利用这个指令调查此时的系统情况.

了解到指令和调试器的断点相关之后 顺着设置面板找到了这个"Flash breakpoints"功能:

![img](/i/em_bkpt_instruct/20170726230109.jpg)

```
Flash breakpoints allows setting of an unlimited number of breakpoints even if the user application is not located in RAM. The generated command is 'monitor flash breakpoints 1'

Flash breakpoints功能允许无数量上限的断点, 即使程序不在RAM中. 生成的命令是"monitor flash breakpoints 1"
```

于是J-Link是怎么实现不限数量的断点的呢
================================================

https://www.segger.com/products/debug-probes/j-link/technology/flash-breakpoints/

(todo: )

BKPT与Semihosting(半主机模式)
===================================

在[Cortex-M3的手册](http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.dui0552a/BABHCHGB.html#)中还多了个Note:
``` 
    ARM does not recommend the use of the BKPT instruction with an immediate value set to 0xAB for any purpose other than Semi-hosting.
```

嗯 由此看来Semihosting也是利用这个指令来实现和片子和调试器交互的
这里顺便研究一下半主机模式

什么是半主机
-------------------
[ARM RealView手册](http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.dui0203ic/Bgbjjgij.html)里对半主机的介绍:

```
8.1.1. 什么是半主机？
    半主机是用于 ARM 目标的一种机制，可将来自应用程序代码的输入/输出请求传送至运行调试器的主机。 例如，使用此机制可以启用 C 库中的函数，如 printf() 和 scanf()，来使用主机的屏幕和键盘，而不是在目标系统上配备屏幕和键盘。
    这种机制很有用，因为开发时使用的硬件通常没有最终系统的所有输入和输出设备。 半主机可让主机来提供这些设备。
    半主机是通过一组定义好的软件指令（如 SVC）来实现的，这些指令通过程序控制生成异常。 应用程序调用相应的半主机调用，然后调试代理处理该异常。 调试代理提供与主机之间的必需通信。
```

```
Note
    ARMv7 之前的 ARM 处理器使用 SVC 指令（以前称为 SWI 指令）进行半主机调用。 但是，如果要为 ARMv6-M 或 ARMv7-M（如 Cortex™-M1 或 Cortex-M3 处理器）进行编译，请使用 BKPT 指令来实现半主机。
```


https://community.nxp.com/message/630895

(todo: )

---

md懒癌 先丢出来吧..
