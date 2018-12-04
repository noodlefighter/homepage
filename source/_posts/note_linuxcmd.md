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

## 组合
```
> 输出到
& 后台运行, 如 echo abc &
|more和|less 用管道把上一条命令导过来显示，方便查看，比如一屏看不完的时候可以用上

用../source.txt批量覆盖找到的a.txt
find -name "a.txt"|xargs -I{} cp -f ../source.txt {}

|grep 筛选

```

## 工具

nano 文本编辑器
ssh 远程登入工具
tar 解压压缩
proxychanins 走代理的工具
redsocks 全局代理 教程copy到后面
nc 瑞士军刀netcat
msttcorefonts 微软字体
tree 打印树型目录结构，常用工具

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

## GIT

```bash
# 检出分支到本地新分支、覆盖工作区
git checkout -f -B Crane2 remotes/origin/Crane2 --
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
