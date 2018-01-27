title: Libembed
description: 
date: 2016-10-12
categories: project
---

(Working...)
[github](https://github.com/noodlefighter/libembed)

<!--more-->

---

之前瞎搞了个__nframe__
回过头来看思路不太对 推掉改做个通用工具包形式的

https://github.com/noodlefighter/libembed

__理由__
..一个坏习惯 做事情之前总得给自己找个合适的理由、
从搞嵌入式软件这块开始 就一直在寻找着优雅的开发软件的方式。

比如，一个新开始一个项目的时候，通常需要先把调试串口给做出来——
编写串口程序，重定向putchar，写串口中断、发送的循环缓冲区……
嗯 枯燥的工作...作为一个独立开发者，有没有办法让它变得简单些？
方法1. 使用现成的软件平台，它们通常会有各种外设的抽象层，甚至已经帮你写好了这部分程序；
方法2. 利用原厂或第三方提供的驱动包，自己完成剩下的工作



__目标__

平台无关的小工具集 ANSI-C 主要做些基础部件 方便裸机开发或是作为RTOS的补充

{% post_link log_libembed 开发日志 %}