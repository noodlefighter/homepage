
RTT(Real-Time Transfer)是JLink提供的

---

## 只是为了打印一些日志

嵌入式软件工程师拿到一个新的硬件平台，一般要做的第一件事就是把异步串口调通，适配一下libc以便接下来的工作中能用printf打印点log帮助调试。
然而现在硬件变得复杂，要折腾个串口驱动也不见得容易，ARM提供了一些方法让目标芯片通过
如果你手头的调试器是JLink，要打印点log就简单多了，使用RTT方式可以直接实现。

## RTT做了什么

简单地说，RTT的工作方式就是把数据直接写到RAM上，由调试器将数据取回，所以有很好的性能表现，不会影响目标的实时性能。

性能表现与类似的semihosting/swo方式对比：
![img](/i/em_jlink_rtt/RTT_SpeedComparison.png)

官方的介绍在[这里](https://www.segger.com/products/debug-probes/j-link/technology/real-time-transfer/about-real-time-transfer/)。

## 如何使用RTT
官方提供了RTT的实现，使用提供的API即可。

## 请注意低功耗操作对RTT的影响
要注意RTT仅能在目标片的内核运行时工作，也就是说一旦cpu halt了，RTT就会暂时罢工直到cpu重新工作，比如执行了WFI指令。
所以使用RTT时，请先将低功耗特性屏蔽，比如一些RTOS在cpu空转时默认会使用WFI指令以节省电能，这时候RTT就好像不工作一样。。如果没法通过一些宏开关屏蔽掉这个特性，注释掉WFI指令就能临时解决这个问题。

P.S. WFI指令使内核暂停工作，直到有中断发生。（似乎WFI就是wait for interrupt?）

## RT