title: OpenSSH秘钥默认路径、权限设置、文件格式参考
description: 
date: 2018-6-13
updated: 2018-6-13
layout: post
comments: ture
categories:
- 笔记
tags: 
- 笔记
- linux
---

自用openssh快速笔记。

<!--more-->

更详细的信息，这有篇很好的参考： https://blog.csdn.net/u010187139/article/details/51984169

## openssh工具集

```
# 服务端
sshd            SSH 服务端程序
sftp-server     SFTP服务端程序
ssh-agent       ssh代理程序

# 客户端
ssh             SSH协议的客户端程序，用来登入远程系统或远程执行命令
slogin          ssh的别名
scp             文件传输客户端
sftp            交互式sftp-server客户端，用法和ftp命令一样。

# 秘钥管理
ssh-add         SSH代理相关程序，用来向SSH代理添加dsa　key
ssh-keygen      生成ssh公私钥
ssh-keyscan     从其他主机上收集公钥
```

## 存放目录

目录为`~/.ssh`，权限700。

## 私钥

私钥大概长这样，权限600。

```none
-----BEGIN RSA PRIVATE KEY-----
MIIEoQIBAAKCAQEAiAbdVhzD0c+sWV2nMFIH9vA1z/zCTlti3EDoWFG9lGjyCjL2
....
wZMCgYBTglrAaucwtSgkPEuLXfiTIVGuobR3eQxOD19T+0uC16ddXsXiBSYOGH+w
xgc+HU3ShNo9N1jIusuXJatXWL+MyUjpOWUtSre748duWd531UAHOIXPAHBdv5o2
zgtiENtUwccic/HDVMl8i2K7cYocFE9Iem8wXoYz/eI/QM9vSA==
-----END RSA PRIVATE KEY-----
```

默认路径：
```c
mv ssh_private_key ~/.ssh/id_dsa
```

## 公钥

位置在`~/.ssh/authorized_keys`，权限700。

大概长这样
```none
ssh-rsa AAAAB3Nza.....F1Yatzmw==
ssh-rsa AAAAB3Nza.....1+tinL1aWB/XgJQ==
```
