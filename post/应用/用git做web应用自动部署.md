date: 2017-03-04
tags: 

- linux
---

准备要把shabao.io弄起来
用git往web server上push来迭代挺方便的 
参考了网上的文章还是踩了些坑 这里简要记一下步骤(服务器用的ubuntu)

<!--more-->

本文只是简单的应用步骤介绍 前置知识请自行古哥 "ssh密钥" "git仓库" "git hooks"等

花点时间写了相关脚本放到gayhub上:
https://github.com/noodlefighter/sh/tree/master/gitserver

---

1.git用户配置
==============

直接写了个bash脚本..
ssh权限设置要求比较严格..折腾了好久
把ssh-ras公钥放authorized_keys里

git_adduser.sh
```
#!/bin/sh 

# 安装git
# sudo apt-get install git

# 添加git用户
adduser git

# ssh 一行一个公钥,格式:"ssh-rsa xxxx",一行一个
mkdir /home/git/.ssh
echo "" > /home/git/.ssh/authorized_keys

# 权限设置 权限设置不对sshd不认..
chown git:git /home/git
chmod 755 /home/git

chown git:git /home/git/.ssh
chmod 700 /home/git/.ssh

chown git:git /home/git/.ssh/authorized_keys
chmod 400 /home/git/.ssh/authorized_keys

# 顺便如果sshd不好使 sshd打开10000端口调试模式看看debug log 
# /usr/sbin/sshd -p 10000 -d

# 禁用git用户shell登录
# 出于安全考虑，第二步创建的git用户不允许登录shell，这可以通过编辑/etc/passwd文件完成。找到类似下面的一行：
# git:x:1001:1001:,,,:/home/git:/bin/bash
# 改为：
# git:x:1001:1001:,,,:/home/git:/usr/bin/git-shell
sed -i '/^git:*/s;/bin/bash;/usr/bin/git-shell;' /etc/passwd
```

---

2.建git仓库
-----------

这里也直接写了个脚本:
1. 建git仓库
2. 建发布目录, 设置适当权限: 目录开启执行权限, .git目录禁止其他用户访问(防止源码暴露)
3. 复制hooks脚本到仓库的hooks文件夹, 改写发布目录, 开启执行权限

顺便hooks是git的一种类似回调的机制 特定事件发生时执行对应脚本 资料很多 这里就不细说

git_autodeploy.sh
``` 
#!/bin/sh 

# 建git仓库(参数1) 并设置hook fetch时自动发布到指定目录(参数2)
if [ "$1" = "" ]; then 
    echo "folder error"
    exit
fi
if [ "$2" = "" ]; then 
    echo "deploy folder error"
    exit
fi

DIR="$( cd "$( dirname "$0"  )" && pwd  )"

# 建仓库
sudo git init --bare $1

# 建立发布目录 禁止其他用户访问.git
rm -R $2
git clone $1 $2
chown -R git:git $2
chmod -R 755 $2
chmod -R 700 $2/.git

# 创建发布hook 设置执行权限
cp $DIR/_hook_post-receive.txt $1/hooks/post-receive
sed -i "s;DeployPath=\"/var/web\";DeployPath='$2';" $1/hooks/post-receive
chmod 755 $1/hooks/post-receive
sudo chown -R git:git $1



```

_hook_post-receive.txt
```
#!/bin/sh  
   
#author: embbnux  
#Blog of Embbnux: http://www.embbnux.com  
   
#判断是不是远端仓库  
IS_BARE=$(git rev-parse --is-bare-repository)  
if [ -z "$IS_BARE" ]; then  
echo >&2 "fatal: post-receive: IS_NOT_BARE"  
exit 1  
fi  
   
unset GIT_DIR  
DeployPath="/var/web"  
   
echo "==============================================="  
cd $DeployPath  
echo "deploying the test web"  
   
＃git stash  
#git pull origin master  
git fetch --all  
git reset --hard origin/master  
git pull
   
time=`date`  
echo "web server pull at webserver at time: $time."  
echo "================================================"  
```

3.测试
===========

此时在客户端上git push
若成功部署则 回显上文hooks脚本中的提示信息
