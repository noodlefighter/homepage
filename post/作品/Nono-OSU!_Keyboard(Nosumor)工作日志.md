
date: 2014-07-20
tags: 
- 键盘
- 电子
- 嵌入式软件
---

osu!键盘nono v3的工作日志

<!--more-->

> 2015-07-30 将原日志转至新网站并拆分成两篇文章

---

### 2014/07/20

发现原来的程序有些bug 防抖没写好（放开时抖动未消除）..表现为放开时会多按一次。。致命啊。晚点就更新程序。

v3计划 增加特性:

* 感光，自动条件灯光强度
* 按键定义
* 防抖时间调节
* 感光灵敏度调节
* 按键灯亮度调节
* 亚克力钢板（同时兼容铝板）
* 侧发光RGBLEDx4
* 整体倾斜
* 灯光模式设置（按键光模式 背景光模式）
* 附加按键由1个增加到3个 
* 改善硬度（增加电路板弹性）
* 为配合量产，将贴片元件放置于底层
* 更换构架至stm32平台（改善延迟）
* pc端设置同步显示程序
* 支持外接外设（待考虑）

---

### 2014/08/04

v3大致设计已经确定下来了
![140804_1](_assets/Nono-OSU!_Keyboard(Nosumor)工作日志/140804_1.jpg)

新的pcb大致面貌 全板大概5*5

* 简单说一下当前能实现的特性
* 6个全彩LED 分布在左右两边
* 总共五个用户可完全自定义的按键（2个樱桃轴，3个微动）
* 1ms-2ms的传输延迟
* 1000Hz以上的按键扫描频率
* 加了光敏电阻电阻，自动条件光强，晚上不再瞎眼
* 外壳设计支持倾斜角,可加钢板（铝制钢板/亚克力钢板）
* 预计不加倾斜支架的本体大小5*5*1.1cm 

批量电路板造价算上各种元件/按键 大概30以内

目前正在将v2的程序（AVR）移植到v3（STM32）上.

---

### 09/17

各种忙 日志也懒得写了

放点图好了

详细情报在 http://tieba.baidu.com/p/3244858972

画师RE;为v3键盘鼓捣了只****nono作为虚拟形象...嘛..要问为啥是这个样子的..只能说是个人喜好问题啦ww

![140917_1](_assets/Nono-OSU!_Keyboard(Nosumor)工作日志/140917_1.jpg)

（开发中的设置程序界面）

![140917_2](_assets/Nono-OSU!_Keyboard(Nosumor)工作日志/140917_2.jpg)

（铝壳版的试制 超级叫了设计的外壳）

边侧灯的效果不佳 还需要换元件

停工了两周..比赛补考课设.今天重新开工

---

### 2015/04/06

总结一下吧

#### 2014年10月中旬
Nosumor实现了预期功能
(除了外壳倾斜)

#### 10月下旬
在osu!吧发帖寻求测试志愿者，制作了５０只
(相关帖子:【Nono盘】蜀黍快来领养我吧（Nono盘公测成员招募） tieba.baidu.com/p/3379722471 )

![140406_1](_assets/Nono-OSU!_Keyboard(Nosumor)工作日志/140406_1.jpg)

![140406_2](_assets/Nono-OSU!_Keyboard(Nosumor)工作日志/140406_2.jpg)

#### 12月初

公开测试的反响不错，开放第一批预定并制作200只
(相关帖子: 【Nono盘】Nono盘预售贴！ tieba.baidu.com/p/3443273887)

![140406_3](_assets/Nono-OSU!_Keyboard(Nosumor)工作日志/140406_3.jpg)

![140406_4](_assets/Nono-OSU!_Keyboard(Nosumor)工作日志/140406_4.jpg)

#### 开发过程

时间顺序为从左到右，从上到下
![140406_5](_assets/Nono-OSU!_Keyboard(Nosumor)工作日志/140406_5.jpg)
PCB打样五次：

* 第一次 的形状是为了进行一次倾斜件的实验(也就是上面的第三张图，嗯...以失败告终，组合度太差)
* 第二次 改回了pcb外形，丰富了下载方式（从只支持SWD，增加了串口烧录支持）
* 第三次 改了usb口封装，由埋板mini-usb变更为贴片mirco-usb；由于设计了定制接插件，轴的焊盘也做了改变
* 第四次 第三次打样的usb口强度低，容易损坏，改成部分插件式，心血来潮想看看白色pcb效果，结果就是——用在全透明的全亚克力壳上很好看，但是金属面板外壳上看着就蛋疼）这一次基本可用了。
* 第五次 试制50只版本，颜色改回黑色，沉金，将所有焊盘改大以适应批量手工焊接

试制亚克力板子们
![140406_6](_assets/Nono-OSU!_Keyboard(Nosumor)工作日志/140406_6.jpg)
没派上用场的试制倾斜组件
![140406_7](_assets/Nono-OSU!_Keyboard(Nosumor)工作日志/140406_7.jpg)
背面
![140406_8](_assets/Nono-OSU!_Keyboard(Nosumor)工作日志/140406_8.jpg)

v3在开发工程中，前后一共进行了５次pcb打样,2面板的铝板打样.数不清次数的亚克力板打样(钱啊;w;)

### 写在第一批量产后

Nosumor作为v3的代号，不利于记忆，所以将它与nosumor的拟人"nono酱"联系起来，称为"nono盘"。
总结一下第一批量产的收获

小批量生产，元件基本靠人工焊接，而六只在边缘的LED,增加了焊接的难度，这次调试中发现的问题均出现在焊接上
RGBLED颜色不统一的问题，这类元件即使同批次，由于厂家检验标准问题（后来得知是国家标准也比较混乱），也容易出现这个问题

定制零件的问题，定制零件价格问题先放在一旁，第一批键盘在使用中定制零件的表现并不完美
由于樱桃轴的两个脚的大小不一，而定制零件使用了同一规格，导致其中一个脚容易接触不良，需要掰弯一点点（这样做之后就没这问题了，所以实际上没怎么影响到使用）。

感光功能的效用问题
用户反馈，这东西没发挥太大的用处，由于装配的位置，软件上也比较难调整这个功能。

（待补透明版本外壳的nono图）
---

### 2015-07-30

折腾新博客，把工作日志做了搬运、拆分。
v3的开发工作实际上集中在14年8到10月。
今年上半年，在学校里接了一些活，忙得生活不能自理，日志更新也懒了，实际上间间断断地做了挺多工作的，这里再总结一下吧。

#### 开源工作的进度问题
因为私人原因，一直抽不出完整的几天做这事，二月之前闲过一段时间却在犹豫——这个v3到底适不适合个人制作…
我想，为了避免这个问题，以后的工程就直接托管在git之类的平台上吧。

#### 键盘名字的变更
之前提到作为开发代号的Nosumor不好记，所以干脆直接变更使用名称为"Nono osu! Keyboard"了。

#### 关于v3键盘的拟人nono酱
一直没有在这里详细写nono酱的详情，这个拟人也算是键盘工程的一部分，还是记录一下吧。
（待补一张nono图片）
nono酱是画师re;做的人设，大概是去年9月吧，聊天中不经意地提到了键盘拟人，觉得这个好玩，就着按自己的喜好写了文字描述，第二天re;就给出了印象图。
我想说————————真的是很可爱啊，，，于是就把印有她的图案做成了一些周边。
（待补nono酱周边）
最近写了个nono酱的wiki:
[萌娘百科](http://zh.moegirl.org/%E8%AF%BA%E8%AF%BA(OSU!%E4%B8%93%E7%94%A8%E9%94%AE%E7%9B%98%E6%8B%9F%E4%BA%BA))

#### 灯光控制软件部分的重写
其实就是在驱动-应用之间，增加了一个中间层，用来管理灯光效果，避免冲突。
期初灯光效果比较简单，用一些变量来控制发光变化效果就好，后来增加的“闪动模式”，让我有了重构这部分软件的念头。
经常被人问起，蹲着坑不填，怪不好意思的，尽量趁早放出吧。

#### 写在第二批量产后
做第二批的时候，想趁着这个机会做一些改进，其实就是在探索继续改进的可能性。
尝试用硅胶按键替代微动开关，无奈发现硅胶按键手感太软，只好换回。

（待补更改后pcb图）
（待补更改后成品图）
第二批在电路板和特性上做了一些变更
* LED数量由6只变更为1只
* 取消支持可换轴功能的定制零件
* LED驱动电路由5只三极管变更为一只ULN2003
* 稳压器件1117的封装变更为更小尺寸
* 由于轴变得不可插拔，将顶板分成两块，便于维护和改造
* 取消光感部件

有了第一批的经验，第二批的次品率降低了不少，设计也变得更加合理。
可是还是遇上了意想不到的情况——ksc的新批次的按键，手感突然发生变化（同一型号竟变得很硬），这让我们措手不及，但是也找不到其他可替代的按键了…
第二批量产坚定了我继续改进的决心……砍掉这微动开关势在必行。

#### 关于osu!商店
没错nono盘已经登入了osu!商店，希望有更多的人能用上专用的osu!设备！

#### v3的总结
突出的特点
* 小型化，便携型
* 由于桌面软件，可定制性强
* 第一批的可换轴特性真的很方便！
* 华丽的灯光效果
* 键盘各部件之间结合紧密，手感上很固实，区别与整体键盘，在v3已经体现出了一些特点

有待完善的不足
* 正是因为体型太mini，需要粘性脚垫支持，才能确保与桌面不发生位移
* 配置的桌面软件可移植性问题，现配置程序只有win版本，下一版本将会改进
* 与osu!的互动性不足
* 可插拔定制零件需要改进
* 配置步骤过于繁琐，需要插拔连接线
* 配置信息由于写在flash区（寿命短，擦出次数1w次左右），所以软件上，应该有预防某页面损坏，使用其他页面的准备。
