title: 《UNIX环境高级编程》读书笔记
description: 
date: 2018-03-18
layout: post
comments: ture
categories:
- 嵌入式软件
tags: 
- 笔记
- linux
---

《UNIX环境高级编程 第3版》补漏笔记，只记录自己在意的知识。
(Working)

<!--more-->

## 第一章 UNIX基础知识

### 1.9 信号
头文件`signal.h`提供一个`singal`函数允许注册回调，信号产生时可以捕捉信号进行一些处理。
比如`SIGINT`由shell中按Ctrl+C产生（中断键），如果程序没捕捉这个信号，则默认的行为是退出程序，如果捕捉了就可以根据需要自行处理这个信号了。

### 1.10 时间值
日历时间：用`time_t`保存。
进程时间：用`clock_t`保存，包括时钟时间(wall clock time)、用户CPU时间、系统CPU时间。

shell中获取进程时间:

```bash
$ cd /usr/include
$ time -p grep _POSIX_SOURCE */*.h
```

### 1.11 系统调用和库函数

系统调用就是系统内核空间的入口点，UNIX中以C函数定义系统调用。
实现方法是，在标准C库中设置一个相同名字的函数，函数用系统所要求的技术调用相应的内核服务。
系统调用一般只是最小接口，标准C库中丰富的函数通过调用这些系统调用来实现。

<unistd.h>中定义大量系统调用封装（POSIX的）。

## 第二章 UNIX标准及实现

### 2.2 UNIX标准化

`ISO C`由C程序设计语言国际标准工作组维护，它定义了C语言的语法语义、标准库。

`POSIX`一开始由IEEE维护，Portable Operating System Interface，目的是提升应用程序在各种UNIX系统环境之间的可移植性，规定了POSIX兼容系统必须提供的各种服务，如pthread、异步IO等等。

`SUS`，Single UNIX Specification，单一UNIX规范，POSIX.1的超集。

### 2.5 限制

<limits.h>中有各种限制，包括：

`ISO C限制`：典型：`CHAR_BIT`  `CHAR_MAX` `UINT_MAX`,在给定的系统中不变。

`POSIX限制`： `_POSIX_XXXX_MAX` 是POSIX要求的最小值。具体数值，有的在编译时可用（宏），有的需要运行时确定，通过`sysconf` `pathconf` `fpathconf`之一获取。

### 2.8 基本系统数据类型

POSIX要求在`<sys/types.h>`中定义，比如下面这些：

```
clock_t     进程时间
dev_t       设备号
size_t      (不带符号)对象长度
ssize_t     带符号的对象长度
```

## 第三章 文件I/O

POSIX定义在`<unistd.h>`中，相关函数：
```none
open        打开文件
openat      允许用相对路径打开文件，同时是一种原子操作，fd为AT_FDCWD表示相对于工作目录
creat       创建文件，用open代替，因为open可以实现“若文件不存在则创建文件并打开”的原子操作
close       关闭文件
lseek       long seek，改变当前文件偏移量，SEEK_SET/SEEK_CUR/SEEK_END分别相对与首部/当前/尾部；`lssek(fd, 0, SEEK_CUR)`返回-1说明文件无法设定偏移（比如FIFO）
read        无缓冲读
write       无缓冲写
pread       原子操作，先lseek后读
pwrite      原子操作，先lseek后写
fcntl       设置文件属性
sync        将修改过的块缓冲区排入队列后返回，不等待
fsync       对指定fd的文件执行sync，等待写操作结束后返回
fdatasync   fsync类似，但只影响数据部分，不更新文件属性
dup         复制fd号
dup2        复制到指定的fd号
```

启用`O_APPEND`标志，可以用lseek再read，但是write时会自动把offset设置到文件末尾再写。

### 3.10 文件共享

os允许一个文件同时被几个应用程序打开，用到了共享机制：各自持有文件状态、偏移量，但使用相同的v-node/i-node包含文件所有者、长度、指向实际硬盘中数据块位置等信息。


### 3.11 原子操作

* 打开文件时使用O_APPEND标志
* pread/pwrite，先lseek再操作的原子操作函数
* 使用open实现代替先判断文件是否存在后创建文件的原子操作

### 3.12 dup和dup2

`dup`/`dup2`用于复制现有的文件描述符(fd)，后者能指定目标fd号，如果指定的fd号已经打开了文件，则先将它关闭。

### 3.14 fcntl

POSIX定义在`<fcntl.h>`中，改变文件属性。

```c
int fcntl (int fd, int cmd, ...);
```

参数cmd对应5种功能：
* 复制已有文件描述符（fd）：`F_DUPFD`，`F_DUPFD_CLOEXEC`
* 获取/设置文件描述符标志：`F_GETFD`,`F_SETFD`
* 获取/设置文件状态标志：`F_GETFL`,`F_SETFL`，其中包含访问方式（ACCMODE，比如只读、只写等等）、当前状态（`O_SYNC`等待写完成、`O_RSYNC`同步读和写）
* 获取/设置异步I/O所有权: `F_GETOWN`,`F_SETOWN`，设置和获取接受`SIGIO`和`SIGURG`信号的进程或进程组ID（用于实现异步IO）
* 获取/设置记录锁: `F_GETLK`,`F_SETLK`,`F_SETLKW`

dup2其实就是重定向。

todo: 
* 不明白GETFD/SETFD用途，这里有篇文章https://www.cnblogs.com/xuyh/p/3273082.html

### 3.15 ioctl

SUS标准的扩展部分，I/O操作的杂物箱，用来进行很多杂项设备的操作，`<sys/ioctl.h>`。

每个设备驱动程序都可以定义它自己专用的一组ioctl命令，比如终端设备。

### 3.16 /dev/fd

不是POSIX的组成部分，目的是方便shell使用。

打开`/dev/fd/n`等效为复制描述符n：

```c
fd  = open("/dev/fd/0", mode);
fd = dup(0);
//大多数系统忽略打开时的mode，所以以上两句等效
```

注意Linux例外，因为实现成了文件的符号链接，所以可以更改打开属性。

## 第四章 文件和目录

相关函数在`<sys/stat.h>`中：

```none
stat        根据路径获取属性
fstat       根据fd号获取属性
fstatat     相对路径获取属性，类比openat
lstat       根据路径获取属性，与stat的区别在于它能察觉到符号链接文件

umask       为进程设置文件模式创建屏蔽字，也就是设置open/create里的mode参数的位屏蔽（shell命令umask）
chmod       更改文件访问权限
fchmod      同上
fchmodat    同上，相对路径，参数flag为AT_SYMLINK_NOFOLLOW时不跟随符号链接

futimens    修改文件的访问和修改时间
utimensat   同上
utimes      同上（XSI扩展）

mkdir       创建目录
mkdirat     同上
rmdir       删除目录
```

相关函数在`<unistd.h>`中：

```none
access      以"实际UID/GID"测试文件访问权限
faccessat   类似access，但可以使用相对fd号的路径，还可以通过flag改变行为成检查"有效UID/GID"访问权限

chown       更改文件所有者，注意权限
fchown      更改指定fd所有者
fchownat    ...
lchown      ...

truncate    截断或扩展文件长度
ftruncate   同上

link        通过已存在的路径，建立新的硬链接，也就是建立目录项
linkat      同上

unlink      删除目录项
unlinkat    同上

symlink     创建符号链接
symlinkat   同上
readlink    读取符号链接
readlinkat  同上

chdir       改变工作目录
fchdir      同上
getcwd      获取当前工作目录绝对路径

chroot      修改应用程序根目录，用于安全和构造一个新的根目录环境（像pyenv?），需要root权限
```

一组用于读目录的函数定义在`<dirent.h>`中：

```none
opendir     打开目录
fdopendir   通过文件描述符fd转换成目录处理函数需要的DIR结构体
readdir     逐条读目录
rewinddir   重置DIRP的当前位置，重头开始读目录
closedir    关闭目录
telldir     返回DIRP的当前位置
seekdir     设置DIRP的当前位置
```

ISO C定义相关函数在`<stdio.h>`中：
```c
remove      删除文件或目录
rename      重命名
renameat    同上    
```

todo:
* 读p105实现ftw的源码，以及学习<ftw.h>，递归降序遍历目录

### 4.2 函数stat/fstat/fstatat/lstat

stat结构包含文件信息：
* 文件type、mode(permissions)
* i节点号
* 设备号
* 特殊文件设备号
* links数量
* 拥有者uid
* 拥有者gid
* 普通文件的size in bytes
* 最后访问、修改、文件状态改变的时间
* 最佳I/O block大小(blksize_t)
* 占用磁盘块数量

功能类比`ls -ls`命令。

### 4.3 文件类型

* 普通文件
* 目录文件
* 块特殊文件(block special file)：提供对设备（如disk）带缓冲的访问，每次访问以固定长度为单位进行
* 字符特殊文件(character special file): 提供对设备不带缓冲的访问，每次访问长度可变。
* FIFO：用于进程间通信，也叫命名管道(named pipe)
* 套接字(socket)：进程间网络通信
* 符号链接(symbolic link): 指向另一个文件

系统中的设备，只可能是块特殊文件或字符特殊文件。

### 4.4 "设置用户ID"和"设置组ID"

```none
实际UID/实际GID             我们实际是谁
---
有效UID/有效GID/附属GID     用于文件访问权限检查
---
保存的设置UID/GID           由exec函数保存
```

进程维护着"设置用户ID"和"设置组ID"，stat结构的`st_uid`、`st_gid`的为文件拥有者的uid/gid，这两个值与进程对文件的操作权限有关。

### 4.10 粘着位

当一个目录设置了粘着位(S_ISVTX)，需要满足其中一个条件才能重命名该目录下的文件：
* 拥有此文件
* 拥有此目录
* 是超级用户

### 4.14 文件系统

章节介绍UFS文件系统，一个柱面组中包含i节点数组、目录块和文件块；i节点是一些文件信息，指向文件块；目录块中包含文件名及i节点的编号，允许多个目录块指向同一i节点。

所谓硬链接就是建立一个指向i节点的目录块。

i节点会对硬链接计数，当计数为0的i节点会被清除。

### 4.15 link/linkat/unlink/unlinkat/remove

link可以创建硬连接，硬链接可能导致路径形成循环。

如果i节点的link计数为0，但文件被打开，它不会被立即清除，而是等文件关闭后，这一特性用于建立即使程序崩溃也能被删除的临时文件。

### 4.17 符号链接

硬链接要求文件处于同一文件系统中，而符号链接（软链接）没这要求。
以路径使用操作文件的函数时，得注意符号链接的情况，有的函数会处理符号链接本身，而不是指向的文件。

使用shell命令`ln`可以创建符号链接。

### 4.19 文件的时间

`st_atim` 文件数据最后的访问时间，如read操作，`ls -u`
`st_mtim` 文件数据最后的修改时间，如write操作
`st_ctim` i节点状态最后更改时间，如chmod操作, `ls -c`

### 4.24 设备特殊文件

文件的`st_dev`是文件系统的设备号。
字符特殊文件和块特殊文件才有`st_rdev`，为实际设备的设备号。
使用`<sys/type.h>`提供的`major`和`minor`宏获得主次设备号。
主设备号标识设备驱动程序、外设板；次设备号标识特定的子设备。比如一个磁盘驱动器上的几个文件系统，主设备号相同，但次设备号不同。
比如，在我的linux环境下，`/dev/tty0`的dev=0/6,rdev=4/0，而`/dev/tty1`的dev=0/6,rdev=4/1。

## 第五章 标准I/O库

标准I/O库是ISO C定义的，SUS对它进行了一些扩充。

定义在`<stdio.h>`中的相关函数：
```none
setbuf      对指定fp设置或关闭缓冲
setvbuf     同上，更精确的控制比如指定缓冲区大小和类型
fflush      冲洗一个流，fp为NULL时冲洗所有流

fopen       路径打开文件
freopen     在指定的的流(fp)上打开指定路径的文件
fdopen      通过fd打开流（POSIX），通常用于管道、网络通信管道
fclose      关闭文件

fmemopen    打开内存流，在内存buffer中读写，仅方便做字符串操作，因为通过NULL判断尾部
open_memstream
            创建面向字节的内存流，适合创建字符串，只写打开，缓冲区会自增长（所以获取缓冲区大小和地址需要先fclose或fflush）
open_wmemstream
            创建面向宽字节的内存流，其他同上

ferror      获取错误值，否则返回0(假)
feof        尾部时返回真
clearerr    清除出错和文件结束标志

fileno      获取指定流(fp)关联的文件描述符(fd)

tmpnam      生成不同的路径字符串，最多可以调用TMP_MAX次（不建议使用因为获取字符串后再创建文件会有一个窗口期而其他程序可能先建立了同名的文件）
tmpfile     创建一个临时文件，返回fp

---------------一次一个字符
fgetc       文件读一个字符，出错或到尾部均返回EOF
getc        同上，但可能是宏，性能可能好一点，但应注意表达式可能被计算多次
getchar     从stdin中读一个字符
ungetc      将字符重新压回流的缓冲区中
fputc       文件中写一个字符
putc        同上
putchar     向stdout中写一个字符

---------------一次一行
fgets       从流中读一行（保留换行符）
gets        从stdin读一行（因为可能造成缓冲区溢出问题被弃用）
fputs       向流写一行
puts        向stdout写一行，会自己加上换行符（不推荐使用）

---------------一次一块（二进制I/O）
fread       读
fwrite      向

---------------定位流
ftell       获取当前位置
fseek       设置当前位置
rewind      重置当前位置
ftello      获取当前位置，类型为off_t
fseeko      设置当前位置，类型为off_t
fgetpos     ISO C提供的函数，引入fpos_t存放位置
fsetpos     ISO C提供的函数，还原位置

---------------格式化I/O
printf      格式化数据写入stdout
fprintf     格式化数据写入指定流(fp)
dprintf     格式化数据写入指定文件描述符(dp)
sprintf     格式化数据写入buf
snprintf    同上，多了buf长度限制
vprintf     printf变体
vfprintf    fprintf变体，变参
vdprintf    dprintf变体
vsprintf    sprintf变体
vsnprintf   snprintf变体

scanf       从stdin格式化输入数据
fscanf      从指定流（fp）格式化输入数据
sscanf      从buf格式化输入数据
vscanf      scanf变体，变参
vfscanf     fscanf变体
vsscanf     sscanf变体
```

`<stdlib.h>`中定义：
```none
mkdtemp     创建临时目录，成功返回目录名并修改输入的template字符串，不会自动删除目录
mkstemp     创建临时文件，成功返回fd并修改输入的template字符串，不会自动删除文件
```

标准I/O效率不佳，因为一次操作涉及两次数据复制，替代：`快速IO: fio`，`sfio`，`储存映射文件mmap函数`。

todo:
* 发生flush的条件没看明白
* 习题5.7答案没看

### 5.2 流和FILE对象

用标准I/O库打开一个文件时，实际上就是把一个流和文件关联了起来。

使用`<wchar.h>`中提供的`fwide`函数可以改变流的定向(stream's orientation)，它决定了流的宽度，用于国际字符集。

### 5.3 标准输入、标准输出、标准错误

`<stdio.h>`中定义了`stdin` `stdout` `stderr`文件指针。

### 5.4 缓冲

标准I/O提供缓冲的目的是让程序减少调用read/write原语的次数，3种类型：
* 全缓冲：填满缓冲区后才执行I/O操作
* 行缓冲：遇到换行符执行I/O操作
* 不缓冲

### 5.11 格式化I/O

格式化输出format string:

```none
%[flags].[fldwidth][precision][lenmodifier]convtype

flags:
 '      将整数按千分位分组字符
 -      在字段内左对齐输出
 +      总是显示带符号转换的正负号
 (空格) 如果第一个字符不是正负号，前面加空格
 #      指定另一种转换格式（例如，对于十六进制格式加0x前缀）
 0      前面补0
 
fldwidth:   最小字段宽度，可以是非负整数或*

precision:  整型最少输出多少数字位数、浮点小数最少位数、字符串最大字节数，可以是*

lenmodifier:
 hh     char长度
 h      short长度
 l      long长度
 ll     long long长度
 j      intmax_t长度
 z      size_t长度
 t      ptrdiff_t长度
 L      long double长度

convtype:
 d i    有符号十进制
 o      无符号八进制
 u      无符号十进制
 x X    无符号十六进制
 f F    双精浮点数
 e E    指数个数双精浮点数
 g G    根据转换后的值解释为f F e E
 a A    十六进制指数格式双精浮点数
 c      字符
 s      字符串
 p      void*指针
 n      将目前printf输出的字符数目输出到指针所指向的int变量中
 C      宽字符，XSI扩展，同lc
 S      宽字符串，XSI扩展，同ls
 
```

格式化输出format string:
```none
%[*][fldwidth][m][lenmodifier]convtype

可选的星号:     抑制转换，按照转换说明的其余部分进行转换，但转换结果不放到参数中；也就是说读取但不保存

fldwidth:       最大字符数

convtpye:       和printf的差不多，以下为不一样的地方
 [    匹配列出的字符序列，以]结束
 [^   匹配除列出字符以外的所有字符，以]结束
```

## 第十章 信号

信号是软件中断，相关头文件`<signal.h>`，在Linux中信号编号被定义在`<bits/signum.h>`中：

```c
#define	SIGHUP		1	/* Hangup (POSIX).  */
#define	SIGINT		2	/* Interrupt (ANSI).  */
#define	SIGQUIT		3	/* Quit (POSIX).  */
#define	SIGILL		4	/* Illegal instruction (ANSI).  */
#define	SIGTRAP		5	/* Trace trap (POSIX).  */
#define	SIGABRT		6	/* Abort (ANSI). */
#define	SIGIOT		6	/* IOT trap (4.2 BSD).  */
#define	SIGBUS		7	/* BUS error (4.2 BSD). */
#define	SIGFPE		8	/* Floating-point exception (ANSI).  */
#define	SIGKILL		9	/* Kill, unblockable (POSIX).  */
#define	SIGUSR1		10	/* User-defined signal 1 (POSIX).  */
#define	SIGSEGV		11	/* Segmentation violation (ANSI).  */
#define	SIGUSR2		12	/* User-defined signal 2 (POSIX).  */
#define	SIGPIPE		13	/* Broken pipe (POSIX).  */
#define	SIGALRM		14	/* Alarm clock (POSIX). */
#define	SIGTERM		15	/* Termination (ANSI).  */
#define	SIGSTKFLT	16	/* Stack fault.  */
#define	SIGCLD		SIGCHLD	/* Same as SIGCHLD (System V).  */
#define	SIGCHLD		17	/* Child status has changed (POSIX). */
#define	SIGCONT		18	/* Continue (POSIX).  */
#define	SIGSTOP		19	/* Stop, unblockable (POSIX).  */
#define	SIGTSTP		20	/* Keyboard stop (POSIX).  */
#define	SIGTTIN		21	/* Background read from tty (POSIX).  */
#define	SIGTTOU		22	/* Background write to tty (POSIX).  */
#define	SIGURG		23	/* Urgent condition on socket (4.2 BSD).  */
#define	SIGXCPU		24	/* CPU limit exceeded (4.2 BSD).  */
#define	SIGXFSZ		25	/* File size limit exceeded (4.2 BSD).  */
#define	SIGVTALRM	26	/* Virtual alarm clock (4.2 BSD).  */
#define	SIGPROF		27	/* Profiling alarm clock (4.2 BSD).  */
#define	SIGWINCH	28	/* Window size change (4.3 BSD, Sun).  */
#define	SIGPOLL		SIGIO	/* Pollable event occurred (System V).  */
#define	SIGIO		29	/* I/O now possible (4.2 BSD).  */
#define	SIGPWR		30	/* Power failure restart (System V).  */
#define SIGSYS		31	/* Bad system call.  */
#define SIGUNUSED	31
```

相关函数在`<signal.h>`中定义：
```none
signal      监听某信号，为其指定handler（语义与实现有关，跨平台时应该自行用sigaction实现其功能）

sigaction   检查、修改与指定信号相关的处理handler

kill        给指定pid发信号，pid为0时发送给同进程组所有进程，pid小于0发送给pid的绝对值的进程组，pid为-1时发送给所有进程
raise       给自身发信号
alarm       设置产生SIGALRM信号的定时器（信号默认行为是终止程序）
pause       挂起程序直到捕捉到信号

sigemptyset     初始化信号集，清空所有信号
sigemptyfill    初始化信号集，包括所有信号
sigaddset       信号集中加入信号
sigdelset       信号集中除去信号
sigismember     测试信号集中是否存在指定信号

sigprocmask     设置进程的信号屏蔽字
sigpending      检查进程中处于pending状态的信号（如被sigprocmask阻塞的信号）
sigsuspend      先设置屏蔽字后休眠（pause）进程，用于等待信号
```

相关函数在`<setjmp.h>`中定义：
```none
sigsetjmp       考虑到sig机制的setjmp
siglongjmp      考虑到sig机制的longjmp
```

相关函数在`<stdlib.h>`中定义：
```none
abort       给自己发送一个SIGABRT信号
```

todo：
* 10.4介绍了之前的信号如何不可靠但是没说现在是怎么解决的
* 10.6中有longjmp和siglongjmp可重入性的讨论，没仔细看
* 10.7没看SIGCHLD语义问题因为Linux中没这问题
* 没看10.10中使用alarm实现sleep函数
* 没看sigaction的用法
* 没看abort实现

### 10.5 中断的系统调用

早期UNIX将系统调用分为低速和高速，高速不会阻塞，而阻塞期间如果来了信号，不同的UNIX实现可能有不同的表现：有的会重启动系统调用的工作，有的返回EINTR错误。这也是跨平台应用不推荐直接用signal函数的原因。（Linux默认会重新启动被中断的系统调用）

### 10.6 可重入函数

使用信号机制时应当注意其handler调用的函数的可重入性，可能会影响被打断的程序的执行，尤其注意：
* 已知使用静态数据结构
* 标准I/O很多实现不可重入
* malloc或free
* 涉及到errno应先保存后恢复

### 10.13 函数sigpending

使用sigprocmask可以屏蔽指定信号，而sigpending函数可以查看被阻塞的状态。

如果解除屏蔽，阻塞的信号会投递到进程中。




















