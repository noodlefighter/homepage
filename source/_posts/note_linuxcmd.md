title: linux命令/工具
description: 
date: 2015-7-29
updated: 2018-5-29
layout: post
comments: ture
categories:
- 笔记
tags: 
- 笔记
- linux
- 命令
---

linux工具命令笔记

<!--more-->

## 一般
mkdir 创建目录
cp 拷贝
cat 输出文件内容
stat 查看文件属性
ll 罗列当前目录内容（-h 以K,M,G单位表示文件大小）
chmod 修改权限，常用开关-R递归，例子 chmod -R a+wr *
mv 移动文件
rm 删除,常用开关-f强制-r递归
ps 查看进程 常用开关-aux
kill 杀进程
nohup 后台运行进程 nohup ./xx.sh >output 2>&1 &
find /home -name "abc.txt"
tail 查看指定文件末尾几行
which 获取指定文件的完整路径（$PATH中的）
shred 粉碎文件
tail 看文件尾部 -f参数看实时日志
lsusb 查看usb设备
file 查看文件类型（比如ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), dynamically linked, interpreter /lib/ld-uClibc.so.0, not stripped）
htop 查看哪个程序占用了cpu/ram资源
iotop 查看哪个程序阻塞了io资源

whereis 找二进制文件、其帮助文档的位置

hexdump 16进制查看（-C参数增加ASCII文本显示）

man 使用手册
info 比使用手册更详细的“电子书”

resize2fs   收缩img文件到文件系统占用的实际大小
e4defrag    清理碎片（e2fsprogs工具包）

## 桌面软件

深度截图
https://www.deepin.org/en/original/deepin-screenshot/

https://www.freedesktop.org/wiki/Software/

terminator终端图形化分栏
https://gnometerminator.blogspot.com/

图形化文件管理器（可sftp）
https://krusader.org/

对比工具kdiff3

视力保护redshift

番茄钟gnome-shell-pomodoro   https://gnomepomodoro.org/
## 组合
```
> 输出到
& 后台运行, 如 echo abc &
|more和|less 用管道把上一条命令导过来显示，方便查看，比如一屏看不完的时候可以用上

用../source.txt批量覆盖找到的a.txt
find -name "a.txt"|xargs -I{} cp -f ../source.txt {}

|grep 根据关键词获取到某行内容
|awk 'NR==3 {print $1}' 获取第3行的第1个“参数”
```

## 工具

nano 文本编辑器
ssh 远程登入工具
tar 解压压缩
proxychanins 走代理的工具
redsocks 全局代理 教程copy到后面
nc 瑞士军刀netcat
msttcorefonts 微软字体
wqy-microhei wqy-zenhei 文泉驿字体
tree 打印树型目录结构，常用工具
squid 正向、反向代理，web缓存
archivemount 利用FUSE（用户层文件系统框架）将归档文件mount到文件系统中
gdb-multiarch   多架构gdb, 工具链中的gdb有问题的时候可以用

## 备忘
如果是开机马上执行的脚本，可以将脚本写到rc.local中；
如果是用户登录后自动执行脚本，可以将脚本写到相应的用户目录下“～/.bash_profile”，若脚本“～/.bash_profile”不存在，可以直接拷贝“/etc/profile”命名为“～/.bash_profile”；
如果是要任一用户登录后自动执行脚本，可以将脚本写到“/etc/profile”中。

## redsocks教程

```

严格意义上来说，proxychains不算自动的全局代理，有没有像Proxifier这样，开了之后自动让所有启动的程序都走系统代理呢？答案就是redsocks。
首先安装Ubuntu编译环境和必要的库：
sudo apt-get install autoconf automake libtool libevent-dev g++
下载源代码，然后编译安装：
./mkauto.sh
cp redsocks /usr/local/bin/
配置文件为：
base { 
// debug: connection progress & client list on SIGUSR1 
log_debug = off;
// info: start and end of client session 
log_info = off;
/* possible `log' values are: 
* stderr 
* file:/path/to/file 
* syslog:FACILITY facility is any of "daemon", "local0"..."local7" 
*/ 
log = "file:/dev/null"; 
// log = stderr; 
// log = "file:/path/to/file"; 
// log = "syslog:local7";
// detach from console 
daemon = on;
/* Change uid, gid and root directory, these options require root 
* privilegies on startup. 
* Note, your chroot may requre /etc/localtime if you write log to syslog. 
* Log is opened before chroot & uid changing. 
*/ 
// user = nobody; 
// group = nobody; 
// chroot = "/var/chroot";
/* possible `redirector' values are: 
* iptables - for Linux 
* ipf - for FreeBSD 
* pf - for OpenBSD 
* generic - some generic redirector that MAY work 
*/ 
redirector = iptables; 
}
redsocks { 
/* `local_ip' defaults to 127.0.0.1 for security reasons, 
* use 0.0.0.0 if you want to listen on every interface. 
* `local_*' are used as port to redirect to. 
*/ 
local_ip = 127.0.0.1; 
local_port = 12345;
// `ip' and `port' are IP and tcp-port of proxy-server 
ip = 127.0.0.1; 
port = 7070;
// known types: socks4, socks5, http-connect, http-relay 
type = socks5;
// login = "foobar"; 
// password = "baz"; 
}
redudp { 
// `local_ip' should not be 0.0.0.0 as it's also used for outgoing 
// packets that are sent as replies - and it should be fixed 
// if we want NAT to work properly. 
local_ip = 127.0.0.1; 
local_port = 10053;
// `ip' and `port' of socks5 proxy server. 
ip = 10.0.0.1; 
port = 1080; 
login = username; 
password = pazzw0rd;
// kernel does not give us this information, so we have to duplicate it 
// in both iptables rules and configuration file. By the way, you can 
// set `local_ip' to 127.45.67.89 if you need more than 65535 ports to 
// forward ;-) 
// This limitation may be relaxed in future versions using contrack-tools. 
dest_ip = 8.8.8.8; 
dest_port = 53;
udp_timeout = 30; 
udp_timeout_stream = 180; 
}
dnstc { 
// fake and really dumb DNS server that returns "truncated answer" to 
// every query via UDP, RFC-compliant resolver should repeat same query 
// via TCP in this case. 
local_ip = 127.0.0.1; 
local_port = 5300; 
}
// you can add more `redsocks' and `redudp' sections if you need.
这里的配置没有配置udp的代理部分，只是配置了tcp即redsocks部分。监听端口是12345。日志关闭了，因为好像我下载的当前版本无论怎么样都产生一堆调试日志，不知道以后会不会修复这点。
启动关闭脚本redsocks.sh为（via）：
#! /bin/bash
SSHHOST=creke 
SSHPORT=22 
SSHUSR=creke 
SSHPWD=creke
SSHDAEMON=/usr/local/bin/plink 
SSHPIDFILE=/var/run/sshtunnel.pid
start_ssh() 
{ 
    echo "Start SSH Tunnel Daemon: " 
    start-stop-daemon -b -q -m -p $SSHPIDFILE --exec $SSHDAEMON -S \ 
    -- -N -D 127.0.0.1:7070 -P $SSHPORT -pw $SSHPWD $SSHUSR@$SSHHOST 
    echo "SSH Tunnel Daemon Started." 
}
stop_ssh() 
{ 
    #ps aux|grep "ssh -NfD 1234"|awk '{print $2}'|xargs kill 
    if [ -f $SSHPIDFILE ]; then 
    PID=$(cat $SSHPIDFILE) 
    kill $PID 
    while [ -d /proc/$PID ]; 
    do 
    sleep 1 
    done 
    fi 
    rm -rf $SSHPIDFILE 
    echo "SSH Tunnel Daemon Stoped." 
}
case "$1" in 
  start) 
    start_ssh 
    cd /usr/local/redsocks 
    if [ -e redsocks.log ] ; then 
      rm redsocks.log 
    fi 
    ./redsocks -p /usr/local/redsocks/redsocks.pid #set daemon = on in config file 
    # start redirection 
    # iptables -t nat -A OUTPUT -p tcp --dport 80 -j REDIRECT --to 12345 
    # iptables -t nat -A OUTPUT -p tcp --dport 443 -j REDIRECT --to 12345 
    # Create new chain 
    iptables -t nat -N REDSOCKS
    # Ignore LANs and some other reserved addresses. 
    iptables -t nat -A REDSOCKS -d 0.0.0.0/8 -j RETURN 
    iptables -t nat -A REDSOCKS -d 10.0.0.0/8 -j RETURN 
    iptables -t nat -A REDSOCKS -d 127.0.0.0/8 -j RETURN 
    iptables -t nat -A REDSOCKS -d 169.254.0.0/16 -j RETURN 
    iptables -t nat -A REDSOCKS -d 172.16.0.0/12 -j RETURN 
    iptables -t nat -A REDSOCKS -d 192.168.0.0/16 -j RETURN 
    iptables -t nat -A REDSOCKS -d 224.0.0.0/4 -j RETURN 
    iptables -t nat -A REDSOCKS -d 240.0.0.0/4 -j RETURN
    # Anything else should be redirected to port 12345 
    iptables -t nat -A REDSOCKS -p tcp -j REDIRECT --to-ports 12345 
    # Any tcp connection should be redirected. 
    iptables -t nat -A OUTPUT -p tcp -j REDSOCKS 
    ;;
  stop) 
    stop_ssh 
    cd /usr/local/redsocks 
    if [ -e redsocks.pid ]; then 
      kill `cat redsocks.pid` 
      rm redsocks.pid 
    else 
      echo already killed, anyway, I will try killall 
      killall -9 redsocks 
    fi 
    # stop redirection 
    iptables -t nat -F OUTPUT 
    iptables -t nat -F REDSOCKS 
    iptables -t nat -X REDSOCKS 
    ;;
  start_ssh) 
    start_ssh 
    ;;
  stop_ssh) 
    stop_ssh 
    ;;
  clean_dns) 
    # iptables -A INPUT -p udp --sport 53 -m state --state ESTABLISHED -m you-know-who -j DROP -m comment --comment "drop you-know-who dns hijacks" 
    echo this function not finished 
    ;;
  *) 
    echo "Usage: redsocks start|stop|start_ssh|stop_ssh|clean_dns" >&2 
    exit 3 
    ;; 
esac
iptables的规则是让所有的TCP包都发送到redsocks监听的端口12345。本脚本还整合了ssh的daemon启动，使用start-stop-daemon来实现。
启动和关闭：
将启动关闭脚本中的开头的几个变量配置好
启动命令：sudo ./redsocks.sh start
关闭命令：sudo ./redsocks.sh stop
```

## 源码编译安装时，自动生成deb包方便管理

使用auto-apt 和 checkinstall，具体命令如下
```
#安装auto-apt和checkinstallapt install auto-apt checkinstall
#在源码目录中auto-apt run ./configure
make
checkinstall
```

这样会生成一个deb包，卸载和重新安装就非常方便了

```
#完全卸载 (packagename具体的名字在checkintall完成之后会有提示）
dpkg -r packagename
```

```
#用生成的deb包重新安装
dpkg -i ***.deb
```

更多实用的命令
```
# 列出包中安装的文件位置
dpkg -L packagename
# 检查是否安装成功
dpkg -l | grep packagename
# 同上
apt list --installed | grep packagename
```
作者：Kevin Li
链接：https://www.zhihu.com/question/20092756/answer/329753869
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

## gparted

图形化的分区管理工具，易用。

## 动态链接库

配置动态链接库目录的地方`/etc/ld.so.conf`，提示找不到库的时候修改。

```none
# 刷新动态库高速缓存，安装新库之后找不到.so文件时执行
sudo ldconfig
# 打印缓存中的内容
ldconfig -p
```

## 改善字体

https://stackoverflow.com/questions/17510099/ugly-fonts-in-java-applications-on-ubuntu

```
# Install both infinality and fontfix'ed JDK.
sudo add-apt-repository ppa:no1wantdthisname/ppa
sudo add-apt-repository ppa:no1wantdthisname/openjdk-fontfix
sudo apt-get update
sudo apt-get install fontconfig-infinality openjdk-7-jdk
# Apply a font style that looks good.
sudo /etc/fonts/infinality/infctl.sh setstyle linux
# And reboot the system.
sudo reboot
```

### gnome下字体改善
安装gnome-tweak
思源字体adobe-source

## GIT相关

图形界面:
gitkraken   据说好用的git图形界面


```bash
# 检出分支到本地新分支、覆盖工作区
git checkout -f -B branchabc remotes/origin/branchabc --

# 添加gpg签名密钥
git config --global user.signingkey 0A46826A
```

### 无法显示中文问题

```
git config --global core.quotepath false
```

### tig

tig是git的文字GUI，中文需要安装依赖。

```
sudo apt install libncursesw5 libncursesw5-dev
git clone https://github.com/jonas/tig.git
cd tig
git checkout -t origin/release
make configure
./configure --prefix=/usr
make
sudo make install install-release-doc
```

### icdiff

改善git diff体验, 双栏
https://github.com/jeffkaufman/icdiff

```
git config --global icdiff.options '--highlight --line-numbers'
git difftool --extcmd icdiff

```

### git flow

https://danielkummer.github.io/git-flow-cheatsheet/
gitflow插件及bash自动完成脚本
```
yay -S gitflow-avh gitflow-bashcompletion-avh
```

"next release"分支即开发分支


### crlf设置

```
AutoCRLF
#提交时转换为LF，检出时转换为CRLF <在win下编辑时好用>
git config --global core.autocrlf true

#提交时转换为LF，检出时不转换 <在linux下编辑时好用>
git config --global core.autocrlf input

#提交检出均不转换
git config --global core.autocrlf false

SafeCRLF
#拒绝提交包含混合换行符的文件
git config --global core.safecrlf true

#允许提交包含混合换行符的文件
git config --global core.safecrlf false

#提交包含混合换行符的文件时给出警告
git config --global core.safecrlf warn
```

## locate

```
locate(locate) 命令用来查找文件或目录。 locate命令要比find -name快得多，原因在于它不搜索具体目录，而是搜索一个数据库/var/lib/mlocate/mlocate.db 。这个数据库中含有本地所有文件信息。Linux系统自动创建这个数据库，并且每天自动更新一次，
```

https://www.cnblogs.com/xqzt/p/5426666.html

## 内核中可配置的项目

`/sys/kernel`目录下是所以内核中可配置的项目

## 输出个log吧

```bash
exec 2> /tmp/rc.local.log  # send stderr from rc.local to a log file  
exec 1>&2                  # send stdout to the same log file  
set -x                     # tell sh to display commands before execution 

```

## 以别的用户身份执行命令

```
su - username -c "command" 
crontab -e -u username
```

## 守护进程管理工具Supervisor

轻松管理守护进程，就算挂了也可以被拉起来。

例子，`/etc/supervisor/conf.d/ss.conf`
 
```none
[program:ss-server]
command=ss-server -c /etc/shadowsocks-libev/config.json
directory=/home
environment=环境变量A="";环境变量B=""
stdout_logfile_maxbytes=20MB
stdout_logfile=/var/log/supervisor/%(program_name)s.log
stderr_logfile_maxbytes=20MB
stderr_logfile=/var/log/supervisor/%(program_name)s.log
autostart=true
autorestart=true
startsecs=5
priority=1
stopsignal=HUP
stopasgroup=true
killasgroup=true
```



命令

```
superviosrctl 交互式
supervisord 守护程序
```

树莓派

```
raspi-config  便捷配置选单
```

apt解决坏依赖

比如提示
```
The following packages have unmet dependencies:
libpcre3-dev : Depends: libpcre3 (= 1:8.31-2ubuntu2) but 1:8.31-2ubuntu2.1 is to be installed
```

可以强制指定版本
```
sudo apt-get install libpcre3=1:8.31-2ubuntu2 libpcre3-dev=1:8.31-2ubuntu2
```

## 目录快速导航相关

### pushd,popd命令

pushd：当前目录入目录栈，并进入到指定的目录
popd：跳转到目录栈顶部弹出的目录

### bd工具

https://linux.cn/article-8491-1.html

https://github.com/vigneshwaranr/bd

```
bd <需要导航到的目录的前几个字母>

# 比如当前目录是/d/tools/android-sdk-tools/tools/lib/x86
# 想要导航到tools目录，输入：
bd too

# 还可以这样获取路径，比如
ls `bd too`
```

### autojump工具

https://linux.cn/article-5983-1.html

工具会记录下cd过的路径，不用输入完整路径即可快速导航。
```
cd /etc/local/
cd /home
j local
```

## win下给cmd.exe赋予unix系sh补全特性的工具

http://mridgers.github.io/clink/

好像不怎么用得到。。毕竟win下也能用bash

## pandoc生成文档

https://linux.cn/article-10228-1.html
https://linux.cn/article-10179-1.html
比如生成ppt

## here文档

https://linux.cn/article-10224-1.html

方便在sh脚本里将数据写入文件

```
#!/bin/bash
OUT=/tmp/output.txt
echo "Starting my script..."
echo "Doing something..."
cat <<EOF >$OUT
  Status of backup as on $(date)
  Backing up files $HOME and /etc/
EOF
echo "Starting backup using rsync..."
```

## tee 写入文件的同时输出到stdout

https://linux.cn/article-9435-1.html

```
ping google.com | tee output.txt
```
选项
-a 追加

## rsync同步工具

```
# 本地文件夹同步
rsync -av <源目录> <目标目录>
```

## pkg-config
https://blog.csdn.net/liyuanbhu/article/details/72851068
交叉编译
https://blog.csdn.net/xukai871105/article/details/37345857
https://blog.csdn.net/mantis_1984/article/details/52847435
https://blog.csdn.net/kl222/article/details/49705143?utm_source=blogxgwz6

引用库libusb-1.0时，Makefile中取参数例子：
```
# use pkg-config
CFLAGS  += $(shell pkg-config libusb-1.0 --cflags)
LDFLAGS += $(shell pkg-config libusb-1.0 --libs)
```


以live555为例，pkg-config方式安装动态库的例子：

Makefile
```
install_shared_libraries:
	install -d $(DESTDIR)$(LIBDIR)/pkgconfig
	sed "s#@PREFIX@#$(PREFIX)#;s#@LIBDIR@#$(LIBDIR)#;s#@VERSION@#$(VERSION)#" live555.pc.in > $(DESTDIR)$(LIBDIR)/pkgconfig/live555.pc
	chmod 644 $(DESTDIR)$(LIBDIR)/pkgconfig/live555.pc
```

live555.pc.in
```
prefix=@PREFIX@
libdir=@LIBDIR@
includedir=${prefix}/include

Name: live555
Description: multimedia RTSP streaming library
Version: @VERSION@
Cflags: -I${includedir}/liveMedia -I${includedir}/groupsock -I${includedir}/BasicUsageEnvironment -I${includedir}/UsageEnvironment
Libs: -L${libdir} -lliveMedia -lgroupsock -lBasicUsageEnvironment -lUsageEnvironment
```


## du命令统计文件夹大小

深度1
```
du --max-depth=1 -h /usr/
```

## samba文件服务配置

/etc/samba/smb.conf   　　　　　　 　　　　　　　　　#samba服务的主要配置文件
/var/log/samba         　　　　　　　　　　　　　　　　#samab服务存放日志文件



## vi

不带格式复制（防复制东西时格式乱掉）
```
:set nosi noai
```

## bash技巧

```
ctrl+u   ctrl+k   光标处往前删除/光标处往后删除
```

## gpg

http://www.ruanyifeng.com/blog/2013/07/gpg.html

```
# 生成密钥
gpg --gen-key

# 罗列密钥
gpg --list-keys

# 导出
gpg --armor --output public-key.txt --export
gpg --armor --output private-key.txt --export-secret-keys 

```

## 给less加高亮显示

1. 装source-highlight
2. 修改`~/.bashrc`:
```
PAGER='less -X -M'
export LESSOPEN="| /usr/share/source-highlight/src-hilite-lesspipe.sh %s"
export LESS=' -R
```
3. 测试 `less -N abc.c`

## 让less颜色不消失的方法

https://qiita.com/mkasahara/items/60049ee20956e835738b

经常要用到例如`ls |less`，但会发现怎颜色消失了

```
ls -al --color=always | less -R
```

文中提到了用expect工具包中的unbuffer能解决，但实际使用发现无效。

## automake

提示缺少build-aux：

```bash
dev@develop:~/workspaces/libnl$ autoreconf
configure.ac:51: error: required file 'build-aux/ar-lib' not found
configure.ac:51:   'automake --add-missing' can install 'ar-lib'
configure.ac:51: error: required file 'build-aux/compile' not found
configure.ac:51:   'automake --add-missing' can install 'compile'
configure.ac:73: error: required file 'build-aux/config.guess' not found
configure.ac:73:   'automake --add-missing' can install 'config.guess'
configure.ac:73: error: required file 'build-aux/config.sub' not found
configure.ac:73:   'automake --add-missing' can install 'config.sub'
configure.ac:49: error: required file 'build-aux/install-sh' not found
configure.ac:49:   'automake --add-missing' can install 'install-sh'
configure.ac:73: error: required file 'build-aux/ltmain.sh' not found
configure.ac:49: error: required file 'build-aux/missing' not found
configure.ac:49:   'automake --add-missing' can install 'missing'
lib/Makefile.am: error: required file 'build-aux/depcomp' not found
lib/Makefile.am:   'automake --add-missing' can install 'depcomp'
parallel-tests: error: required file 'build-aux/test-driver' not found
parallel-tests:   'automake --add-missing' can install 'test-driver'
```

解决方法：
```
automake --add-missing
autoreconf -i
```

## GNU Binutils 以及相关工具

http://www.gnu.org/software/binutils/

ld - the GNU linker. 链接器
as - the GNU assembler. 汇编编译器

addr2line - Converts addresses into filenames and line numbers. 将代码地址转换为对应的程序号
ar - A utility for creating, modifying and extracting from archives. 将目标文件打包成静态库的工具，还能查看、删除其中的模块（object文件）
nm - Lists symbols from object files. 列出目标文件中的符号
objcopy - Copies and translates object files. 翻译二进制文件，比如bin到hex
objdump - Displays information from object files. 查看二进制文件的程序段信息等
ranlib - Generates an index to the contents of an archive. 生成档案（静态库？）的索引
readelf - Displays information from any ELF format object file. 查看elf信息
size - Lists the section sizes of an object or archive file. 列出二进制文件中各段大小
strings - Lists printable strings from files.  查看文件中的字符串
strip - Discards symbols. 用于剔除多余的符号（调试信息）

c++filt - Filter to demangle encoded C++ symbols. 
dlltool - Creates files for building and using DLLs.
gold - A new, faster, ELF only linker, still in beta test.
gprof - Displays profiling information.
nlmconv - Converts object code into an NLM.

windmc - A Windows compatible message compiler.
windres - A compiler for Windows resource files.

ldd命令可以查看程序依赖的动态库：
```bash
$ ldd /bin/ls
/bin/ls: is setuid
        libc.so.0 => /lib//libc.so.0 (0xb6e7e000)
        ld-uClibc.so.1 => /lib/ld-uClibc.so.0 (0xb6f29000)

```

objdump工具：
```bash
$ objdump -p ./sample_venc |grep NEEDED
  NEEDED               libc.so.0
  NEEDED               ld-uClibc.so.1

```

查看正在运行中的程序的依赖库：
```bash
$ ps -ef|grep bash
dev      10280 10276  0 14:32 pts/0    00:00:00 -bash
dev      11711 10280  0 16:08 pts/0    00:00:00 grep --color=auto bash
dev@develop:~/workspaces/hi3516a/Hi3516A_SDK_V1.0.7.1/mpp/sample/venc$ pmap 10280 |head
10280:   -bash
0000000000400000    976K r-x-- bash
00000000006f3000      4K r---- bash
00000000006f4000     36K rw--- bash
00000000006fd000     24K rw---   [ anon ]
0000000000b84000   1816K rw---   [ anon ]
00007fee9e033000     44K r-x-- libnss_files-2.23.so
00007fee9e03e000   2044K ----- libnss_files-2.23.so
00007fee9e23d000      4K r---- libnss_files-2.23.so
00007fee9e23e000      4K rw--- libnss_files-2.23.so
```

`readelf`工具和objdump类似，但信息更好读，信息会更全因为objdump会省略部分辅助性的段。

### 把二进制文件用objcopy工具装入一个目标文件

就是把二进制资源变成符号：

```
# objcopy -I binary -O elf32-i386 -B i386 image.jpg image.o
# objdump -ht image.o
```

## DHCP客户端udhcpc

busybox自带个简单的dhcp client，获取到IP后会执行脚本进行配置，编辑`/usr/share/udhcpc/default.script`，记得给+x权限：

```bash
#!/bin/sh

#script edited by Tim Riker <Tim@Rikers.org>

[ -z "$1" ] && echo "Error: should be called from udhcpc" && exit 1

RESOLV_CONF="/etc/resolv.conf"
[ -n "$broadcast" ] && BROADCAST="broadcast $broadcast"
[ -n "$subnet" ] && NETMASK="netmask $subnet"

case "$1" in
  deconfig)
    /sbin/ifconfig $interface 0.0.0.0
    ;;

  renew|bound)
    /sbin/ifconfig $interface $ip $BROADCAST $NETMASK

    if [ -n "$router" ] ; then
      echo "deleting routers"
      while route del default gw 0.0.0.0 dev $interface ; do
        :
      done

      for i in $router ; do
        route add default gw $i dev $interface
      done
    fi

    echo -n > $RESOLV_CONF
    [ -n "$domain" ] && echo search $domain >> $RESOLV_CONF
    for i in $dns ; do
      echo adding dns $i
      echo nameserver $i >> $RESOLV_CONF
    done
    ;;
esac

exit 0
```

执行结果：
```
~ # udhcpc
udhcpc (v1.20.2) started
Sending discover...
Sending select for 192.168.1.68...
Lease of 192.168.1.68 obtained, lease time 86400
deleting routers
route: SIOCDELRT: No such process
adding dns 192.168.2.1
adding dns 192.168.2.1
~ # ifconfig
eth0      Link encap:Ethernet  HWaddr 00:E0:4C:36:04:71
          inet addr:192.168.1.68  Bcast:192.168.3.255  Mask:255.255.252.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:70680 errors:0 dropped:51 overruns:0 frame:0
          TX packets:10 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:4522321 (4.3 MiB)  TX bytes:2728 (2.6 KiB)
```

## nfs

服务器配置：
```
# apt install nfs-kernel-server
# vi 
```

编辑配置`/etc/exports`：
```
/home/dev/workspaces/hi3516a/nfs        (rw,sync,no_subtree_check)
```

尝试挂载：
```
mount -t -o nfs localhost:/home/dev/workspaces/hi3516a/nfs /mnt/nfs
```

错误记录：
```
svc: failed to register lockdv1 RPC service (errno 111)
加个-o nolock
```


## systemctl

>  systemd 是 Linux 下的一款系统和服务管理器，兼容 SysV 和 LSB 的启动脚本。systemd 的特性有：支持并行化任务；同一时候採用 socket 式与 D-Bus 总线式激活服务；按需启动守护进程（daemon）。利用 Linux 的 cgroups 监视进程；支持快照和系统恢复。维护挂载点和自己主动挂载点。各服务间基于依赖关系进行精密控制

systemd的人机交互接口就是systemctl，比如看nfs服务的日志：

```
$ systemctl status nfs-server.service
```

## crontab定时任务

编辑配置：
```
crontab -e
```

内容：
```
# 每天02:06重启
06 2 * * * reboot
```

## 用wget批量下载镜象站

像经常能见到类似`https://mirrors.edge.kernel.org/pub/`的站点，偶尔下几个文件的话，浏览器直接下载就好，但如果想整个下载下来就很费力，可以用wget批量下载：

```
wget -r -nd -np -l1 https://mirrors.xxxxx.org
```

-nd 不创建目录, wget默认会创建一个目录
-r 递归下载
-l1 (L one) 递归一层,只下载指定文件夹中的内容, 不下载下一级目录中的

## gcc编译相关

### 编译调试

打印更多信息

```
make V=1
```

### 交叉编译

设定库搜索路径
```
make LDFLAGS="-Wl,-rpath,/xxx/xx/libs"
```

```
-Wl,option
Pass option as an option to the linker. If option contains commas, it is split into multiple options at the commas. You can use this syntax to pass an argument to the option. For example, -Wl,-Map,output.map passes  -Map output.map to the linker. When using the GNU linker, you can also get the same effect with `-Wl,-Map=output.map'.

-rpath=dir

Add a directory to the runtime library search path. This is used when linking an ELF executable with shared objects. All -rpath arguments are concatenated and passed to the runtime linker, which uses them to locate shared objects at runtime. The -rpath option is also used when locating shared objects which are needed by shared objects explicitly included in the link;
```

设定sysroot
```
make LDFLAGS="--sysroot=/home/r/osp/buildroot-2019.02.1/output/host/arm-buildroot-linux-uclibcgnueabi/sysroot
```

## 文本编码转换

https://blog.csdn.net/u012724167/article/details/77248919

```
# 转换目录下所有文件到UTF8
enca -L zh_CN -x UTF-8 *
```

但是不成功啊：
```
r@r-work /mnt/hgfs/project/osukb/osu-keyboard-v3/app $ enca -V -L zh_CN -x utf-8 keymap.c
enca: converting `keymap.c': UCS-2/CRLF/21..UTF-8
enca: librecode warning: Conversion leads to ambiguous output in `keymap.c'
```

## 生成patch && 打patch

a为修改前，b为修改后。

单文件生成patch：
```
diff -up a/1.txt b/1.txt > patch
```

多文件生成patch：
```
diff -uprN a/ b/ > patch
```

打patch，需要切换到该目录中，用p1参数忽略第一级目录，因为目录名可能不同：
```
patch -p1 < patch1.diff
```

## 应用挂起、恢复

ctrl+z挂起
命令fg恢复

## archlinux

```
locate:
core/mlocate
```


## sshfs

sshfs可以挂在一个sftp中的目录到本地路径上：

```
mkdir -p /mnt/mysdk
sudo sshfs -o allow_other user@xxx.xxx.xxx.xxx:/home/mpc/workspaces /mnt/mysdk
```

## sshpass

ssh不允许在参数里带密码，sshpass能加个-p参数带上密码。

例子，ssh免输入密码远程执行命令：
```
sshpass -p "123456" ssh root@xxx.xxx.xxx.xxx "pwd;"
```

## memtool

最简单的寄存器修改程序，buildroot里有包。

https://public.pengutronix.de/software/memtool/

## bash中set命令

可以控制bash的行为，比如`set -e`使脚本在错误时退出bash。

查看帮助用`help set`命令：

```
-a allexport
   Flag variables for export when assignments are made to them.

-b notify
   Enable asynchronous notification of background job completion.
        (UNIMPLEMENTED)

-C noclobber
        Do not overwrite existing files with ``>''.

-E emacs
        Enable the built-in emacs(1) command line editor (disables the -V
        option if it has been set).

-e errexit 脚本遇错时退出

-f noglob
        Disable pathname expansion.

-I ignoreeof
        Ignore EOF's from input when in interactive mode.

-i interactive 强制shell表现为交互式的

-m monitor
        Turn on job control (set automatically when interactive).

-n noexec
        If not interactive, read commands but do not execute them.  This
        is useful for checking the syntax of shell scripts.

-P physical
        Change the default for the cd and pwd commands from -L (logical
        directory layout) to -P (physical directory layout).

-p privileged
        Turn on privileged mode.  This mode is enabled on startup if
        either the effective user or group id is not equal to the real
        user or group id.  Turning this mode off sets the effective user
        and group ids to therealuserand=groupids.  When this mode is
        enabled for interactive shells, the file /etc/suid_profile is
        sourced instead of ~/.profile after /etc/profile is sourced, and
        the contents of the ENV variable are ignored.

-s stdin
        Read commands from standard input (set automatically if no file
        arguments are present).  This option has no effect when set after
        the shell has already started running (i.e., when set with the
        set command).

-T trapsasync
        When waiting for a child, execute traps immediately.  If this
        option is not set, traps are executed after the child exits, as
        specified in IEEE Std 1003.2 (``POSIX.2'').  This nonstandard
        option is useful for putting guarding shells around children that
        block signals.  The surrounding shell may kill the child or it
        may just return control to the tty and leave the child alone,
        like this:
              sh -T -c "trap 'exit 1' 2 ; some-blocking-program"

-u nounset 展开未定义的变量时，报错退出

-V Vi 启用内置vi

-v verbose 输出详细信息，用于debug

-x 在执行每个命令前，将它打印输出
```


## /dev/shm

一个ramdisk，可以往内存里放需要高速缓存的问题。


## linux访问NTFS盘报错：no object for d-bus interface

```
mount | grep gvfs
sudo umount -fl /run/user/（用户ID数字） gvfs
sudo rm -rf /run/user/（用户ID数字） gvfs
reboot
```

## linux下用罗技m570轨迹球鼠标上的的按钮

https://lovingboth.com/logitech-m570-trackball-buttons-in-linux/

```
cd ~
sudo apt-get install xbindkeys xautomation

Create a file ~/.xbindkeysrc and put

"xte 'key Page_Up'"
b:9

"xte 'key Page_Down'"
b:8

(when 'button 9' is pressed, run the xte program to emulate a 'PgUp' keystroke, and similarly when 'button 8' is pressed, emulate a 'PgDn' keystroke) in it with your favourite text editor. Run

xbindkeys
```
## 虚拟机相关

### 虚拟机使用物理硬盘启动

virtualbox比较好弄，vmware没弄通

linux下 查询硬盘id, 并创建raw映射文件:
```
ls -l /dev/disk/by-id
VBoxManage internalcommands createrawvmdk -filename /path/to/file.vmdk -rawdisk /dev/disk/by-id/xxxxxx
```

win
```
VBoxManage.exe internalcommands createrawvmdk -filename D:\vm\disk500.vmdk -rawdisk \\.\PHYSICALDRIVE1
```

注意给权限，必要时勾选“使用主机I/O缓存”


### linux挂载vmdk

安装vmware-workstation后得到vmware-mount工具

```
sudo vmware-mount mint_work-home2.vmdk /mnt/vmdk
```

### virtualbox命令

```
VBoxManage startvm "VM name" --type 
```
`--type`可以是
* gui：正常模式，关闭gui同时关闭虚拟机
* sdl：
* headless：无界面启动
* separate：分离式启动，关闭gui不会关闭虚拟机

## minicom

minicom linux下好用的串口通讯工具:

```
minicom -D /dev/ttyUSB0
```

## manjaro布置

Archlinux 的灵魂──PKGBUILD、AUR 和 ABS
https://blog.csdn.net/taiyang1987912/article/details/41457333#

一些流行的 Linux 发行版包管理器命令的对应关系
https://wiki.archlinux.org/index.php/Pacman/Rosetta_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)

### 网络命令

```
arp = ip neighbor
ifconfig = ip address, ip link
netstat = ss
route = ip route
```

### ibus配置

配置文件在`~/.config/ibus`

.xprofile：
```
export GTK_IM_MODULE=ibus
export XMODIFIERS=@im=ibus
export QT_IM_MODULE=ibus
ibus-daemon -d -x
```

默认输入法为第一个，顺序在dconf中配置：`desktop/ibus/general/engines-order`。

### 安装字体

aur上有个ttf-consolas-with-yahei

```
mkdir /usr/share/fonts/<font_name>
cd /usr/share/fonts/<font_name>
mkfontscale
mkfontdir
fc-cache -fv
```

### 调优资源调度

https://www.linuxidc.com/Linux/2017-02/141138.htm


## netcat的两个版本

一般发行版仓库里有两个版本:
* bsd-netcat
* gnu-netcat

gnu这个用的时候得注意这样是不行的, 得用-p参数指定端口
```
nc -l 9898
```
很好, 我选择bsd的实现.

## socat - Multipurpose relay

http://www.dest-unreach.org/socat/
http://www.dest-unreach.org/socat/doc/socat.html

“多用途中继”,看着是想代替netcat.

## 缩小镜象

```
# 创建回环设备，但不挂载
losetup /dev/loop0 ./qt.img
# 置零空闲数据
zerofree -v /dev/loop0
# 断开回环设备
losetup -d /dev/loop0
# 文件系统检查
e2fsck -f qt.img
# 缩减空间
resize2fs -M qt.img
```


## ssh保持会话

ServerAliveInterval 60 ＃client每隔60秒发送一次请求给server，然后server响应，从而保持连接

ServerAliveCountMax 3  ＃client发出请求后，服务器端没有响应得次数达到3，就自动断开连接，正常情况下，server不会不响应