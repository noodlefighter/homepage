date: 2021-01-18
tags:

- 应用笔记

---

工作需要为USB设备适配MacOS，手头没mac设备，总借同事的也不是个办法，于是打算自己装个。

上github搜了一下，果然有现成的脚本，用它成功安装了MacOS虚拟机，这里记录一下过程。

![VirtualBox_macOS_18_01_2021_13_25_36](_assets/MacOS-Vitrualbox%E8%99%9A%E6%8B%9F%E6%9C%BA%E5%AE%89%E8%A3%85%E5%B0%8F%E8%AE%B0/VirtualBox_macOS_18_01_2021_13_25_36.png)

<!--more-->


## 前期准备

```
The following dependencies should be available through a package manager:
bash coreutils gzip unzip wget xxd dmg2img virtualbox
```

根据文档先装依赖：

```
$ sudo pacman -S bash coreutils gzip unzip wget xxd dmg2img virtualbox
```

## 运行脚本

脚本会在当前目录下创建虚拟机文件，所以在合适的路径clone。

```
$ git clone https://github.com/myspaghetti/macos-virtualbox.git
$ cd macos-virtualbox
$ ./macos-guest-virtualbox.sh
```

这个脚本会帮自动下载镜象、在virtualbox中自动创建虚拟机，安装完成后会自动启动装好的机器。贴一下脚本输出：

```
~/git/macos-virtualbox (master ✘)✹ ᐅ ./macos-guest-virtualbox.sh

Push-button installer of macOS on VirtualBox

This script installs only open-source software and unmodified Apple binaries,
and requires about 50GB of available storage, of which 25GB are for temporary
installation files that may be deleted when the script is finished.

The script interacts with the virtual machine twice, please do not interact
with the virtual machine manually before the script is finished.

Documentation about optional configuration, iCloud and iMessage connectivity,
resuming the script by stages, and other topics can be viewed with the
following command:

  ./macos-guest-virtualbox.sh documentation | less -R

Press enter to review the script configuration

vm_name="macOS"
macOS_release_name="Catalina"    # install "HighSierra" "Mojave" "Catalina"
storage_size=80000               # VM disk image size in MB. minimum 22000
storage_format="vdi"             # VM disk image file format, "vdi" or "vmdk"
cpu_count=4                      # VM CPU cores, minimum 2
memory_size=4096                 # VM RAM in MB, minimum 2048
gpu_vram=128                     # VM video RAM in MB, minimum 34, maximum 128
resolution="1280x800"            # VM display resolution

These values may be customized as described in the documentation.

Press enter to continue, CTRL-C to exit

The command "VBoxManage list extpacks" either does not list the Oracle VM
VirtualBox Extension Pack, or lists one or more extensions as unusable.
The virtual machine will be configured without USB xHCI controllers.

Catalina selected to be downloaded and installed

stage: prompt_delete_existing_vm

stage: create_vm

stage: check_default_virtual_machine

Checking that VirtualBox starts the virtual machine without errors.

Checking that VirtualBox uses hardware-supported virtualization.

stage: prepare_macos_installation_files

Downloading Apple macOS Catalina software update catalog
Catalina_sucatalog                                          100%[===========================================================================================================================================>]   6.52M  12.0MB/s  用时 0.5s
Trying to find macOS Catalina InstallAssistant download URL
Catalina_sucatalog_00_InstallAssistantAuto.smd              100%[===========================================================================================================================================>]  40.05K  --.-KB/s  用时 0.003s
Found download URL: http://swcdn.apple.com/content/downloads/26/37/001-68446/r1dbqtmf3mtpikjnd04cq31p4jk91dceh8/

Downloading macOS installation files from swcdn.apple.com
Catalina_BaseSystem.chunklist                               100%[===========================================================================================================================================>]   1.97K  --.-KB/s  用时 0s
Catalina_InstallInfo.plist                                  100%[===========================================================================================================================================>]   1.55K  --.-KB/s  用时 0s
Catalina_AppleDiagnostics.dmg                               100%[===========================================================================================================================================>]   3.00M  6.77MB/s  用时 0.4s
Catalina_AppleDiagnostics.chunklist                         100%[===========================================================================================================================================>]     328  --.-KB/s  用时 0s
Catalina_BaseSystem.dmg                                     100%[===========================================================================================================================================>] 475.53M  7.31MB/s  用时 65s
Catalina_InstallESDDmg.pkg                                    100%[====>]12.2MB/s  剩Catalina_Ins 100%   7.21G  12.3MB/s  用时 10m 28s

Splitting the several-GB InstallESDDmg.pkg into 1GB parts because
VirtualBox hasn't implemented UDF/HFS VISO support yet and macOS
doesn't support ISO 9660 Level 3 with files larger than 2GB.
正在创建文件 'Catalina_InstallESD.part00'
正在创建文件 'Catalina_InstallESD.part01'
正在创建文件 'Catalina_InstallESD.part02'
正在创建文件 'Catalina_InstallESD.part03'
正在创建文件 'Catalina_InstallESD.part04'
正在创建文件 'Catalina_InstallESD.part05'
正在创建文件 'Catalina_InstallESD.part06'
正在创建文件 'Catalina_InstallESD.part07'

Downloading open-source APFS EFI drivers used for VirtualBox 6.0 and 5.2
...even though VirtualBox version 6.1 or higher is detected.
AppleSupport-v2.0.4-RELEASE.zip                             100%[===========================================================================================================================================>]  42.20K   269KB/s  用时 0.2s
Archive:  AppleSupport-v2.0.4-RELEASE.zip
  inflating: ApfsDriverLoader.efi
  inflating: AppleImageLoader.efi
  inflating: AppleUiSupport.efi

stage: create_nvram_files

stage: create_macos_installation_files_viso
Creating EFI startup script

Creating VirtualBox 6 virtual ISO containing the
installation files from swcdn.apple.com


stage: configure_vm

stage: populate_basesystem_virtual_disk
Converting BaseSystem.dmg to BaseSystem.img

dmg2img v1.6.7 (c) vu1tur (to@vu1tur.eu.org)

Catalina_BaseSystem.dmg --> Catalina_BaseSystem.img


decompressing:
opening partition 0 ...             100.00%  ok
opening partition 1 ...             100.00%  ok
opening partition 2 ...             100.00%  ok
opening partition 3 ...             100.00%  ok
opening partition 4 ...             100.00%  ok
opening partition 5 ...             100.00%  ok
opening partition 6 ...             100.00%  ok
opening partition 7 ...             100.00%  ok

Archive successfully decompressed as Catalina_BaseSystem.img
Converting from raw image file="Catalina_BaseSystem.img" to file="Catalina_BaseSystem.vdi"...
Creating dynamic image with size 2138558464 bytes (2040MB)...

stage: create_bootable_installer_virtual_disk
Creating Catalina installation media virtual disk image.
0%...10%...20%...30%...40%...50%...60%...70%...80%...90%...100%
Medium created. UUID: 00a0e882-771d-4a9f-b2fb-9eebd21942dc

stage: populate_bootable_installer_virtual_disk

Creating VirtualBox 6 virtual ISO containing macOS Terminal script
for partitioning and populating the bootable installer virtual disk.


Starting virtual machine "macOS".
This should take a couple of minutes. If booting fails, exit the script by
pressing CTRL-C then see the documentation for information about applying
different CPU profiles in the section CPU profiles and CPUID settings.

Until the script completes, please do not manually interact with
the virtual machine.

Press enter when the Language window is ready.^C
```

但无法启动，卡在了这里：

![image-20210118120928722](_assets/MacOS-Vitrualbox%E8%99%9A%E6%8B%9F%E6%9C%BA%E5%AE%89%E8%A3%85%E5%B0%8F%E8%AE%B0/image-20210118120928722.png)

（进入vbox可以看到配置好的机器）：

![深度截图_选择区域_20210118114342](_assets/MacOS-Vitrualbox%E8%99%9A%E6%8B%9F%E6%9C%BA%E5%AE%89%E8%A3%85%E5%B0%8F%E8%AE%B0/%E6%B7%B1%E5%BA%A6%E6%88%AA%E5%9B%BE_%E9%80%89%E6%8B%A9%E5%8C%BA%E5%9F%9F_20210118114342.png)

## 修复无法启动的问题

虚拟机无法启动，脚本打印出的提示，让修改cpuid（大概是因为宿主是AMD平台的原因）：

```
This should take a couple of minutes. If booting fails, exit the script by
pressing CTRL-C then see the documentation for information about applying
different CPU profiles in the section CPU profiles and CPUID settings.
```

输入`./macos-guest-virtualbox.sh documentation |less -R`查文档，说：

```
macOS does not supprort every CPU supported by VirtualBox. If the macOS Base
System does not boot, try applying different CPU profiles to the virtual
machine with the VBoxManage commands described below. First, while the
VM is powered off, set the guest's CPU profile to the host's CPU profile, then
try to boot the virtual machine:
    VBoxManage modifyvm "${vm_name}" --cpu-profile host
    VBoxManage modifyvm "${vm_name}" --cpuidremoveall
If booting fails, try assigning each of the preconfigured CPU profiles while
the VM is powered off with the following command:
    VBoxManage modifyvm "${vm_name}" --cpu-profile "${cpu_profile}"
Available CPU profiles:
  "Intel Xeon X5482 3.20GHz"  "Intel Core i7-2635QM"  "Intel Core i7-3960X"
  "Intel Core i5-3570"  "Intel Core i7-5600U"  "Intel Core i7-6700K"
```

安装这个提示，输入：

```
$ VBoxManage modifyvm "macOS" --cpu-profile "Intel Xeon X5482 3.20GHz"
```

再启动机器，成功，看到了配置语言的界面：

![VirtualBox_macOS_18_01_2021_11_30_19](_assets/MacOS-Vitrualbox%E8%99%9A%E6%8B%9F%E6%9C%BA%E5%AE%89%E8%A3%85%E5%B0%8F%E8%AE%B0/VirtualBox_macOS_18_01_2021_11_30_19.png)

## 安装

这个脚本会帮自动走完安装界面（通过操作键盘的方式），所以这里稍微修改脚本让它能顺利走下去。

修改脚本，在“configure_vm”阶段末尾加上刚才针对cpuid的配置：

```
diff --git a/macos-guest-virtualbox.sh b/macos-guest-virtualbox.sh
index c656069..7457bdb 100755
--- a/macos-guest-virtualbox.sh
+++ b/macos-guest-virtualbox.sh
@@ -673,6 +673,8 @@ VBoxManage setextradata "${vm_name}" \
   "ourhardworkbythesewordsguardedpleasedontsteal(c)AppleComputerInc"
 VBoxManage setextradata "${vm_name}" \
  "VBoxInternal/Devices/smc/0/Config/GetKeyFromRealSMC" 0
+
+VBoxManage modifyvm "${vm_name}" --cpu-profile "Intel Xeon X5482 3.20GHz"
 }

 # Create the macOS base system virtual disk image
```

重新跑一遍脚本，问已经存在虚拟机了是不是要删掉，选择“是”：

![image-20210118120627164](_assets/MacOS-Vitrualbox%E8%99%9A%E6%8B%9F%E6%9C%BA%E5%AE%89%E8%A3%85%E5%B0%8F%E8%AE%B0/image-20210118120627164.png)

启动成功，看到了语言配置界面，然后根据提示，在脚本上按几次回车：

```
Press enter when the Language window is ready.

Press enter when the macOS Utilities window is ready.

Press enter when the Terminal command prompt is ready.
```

完成成功。

![VirtualBox_macOS_18_01_2021_13_25_36](_assets/MacOS-Vitrualbox%E8%99%9A%E6%8B%9F%E6%9C%BA%E5%AE%89%E8%A3%85%E5%B0%8F%E8%AE%B0/VirtualBox_macOS_18_01_2021_13_25_36.png)

## 遇到的问题，限制

- 无法使用摄像头，photo booth无法使用USB UVC摄像头
- 无法安装Guest Additions（参考[爆栈上的回答](https://stackoverflow.com/a/54186352)没装成功）

## 附上宿主环境供参考

```
~ ᐅ screenfetch

 ██████████████████  ████████     r@r-lc
 ██████████████████  ████████     OS: Manjaro 20.2.1 Nibia
 ██████████████████  ████████     Kernel: x86_64 Linux 5.4.85-1-MANJARO
 ██████████████████  ████████     Uptime: 8d 20h 25m
 ████████            ████████     Packages: 1523
 ████████  ████████  ████████     Shell: zsh 5.8
 ████████  ████████  ████████     Resolution: 1920x1080
 ████████  ████████  ████████     DE: GNOME
 ████████  ████████  ████████     WM: i3
 ████████  ████████  ████████     GTK Theme: Adwaita [GTK2/3]
 ████████  ████████  ████████     Icon Theme: Adwaita
 ████████  ████████  ████████     Font: Cantarell 11
 ████████  ████████  ████████     Disk: 782G / 1.1T (77%)
 ████████  ████████  ████████     CPU: AMD Ryzen 5 3400G with Radeon Vega Graphics @ 8x 3.7GHz
                                  GPU: AMD Radeon(TM) Vega 11 Graphics (RAVEN, DRM 3.35.0, 5.4.85-1-MANJARO, LLVM 11.0.0)
                                  RAM: 14983MiB / 30096MiB
~ ᐅ yay -Qi virtualbox
名字           : virtualbox
版本           : 6.1.16-3
描述           : Powerful x86 virtualization for
                 enterprise as well as home use
架构           : x86_64
URL            : https://virtualbox.org/
软件许可       : GPL  custom
组             : 无
提供           : 无
依赖于         : glibc  openssl  curl  gcc-libs  libpng
                 python  sdl  libvpx  libxml2  procps-ng
                 shared-mime-info  zlib  libxcursor
                 libxinerama  libx11  libxext  libxmu
                 libxt  opus  qt5-base  qt5-x11extras
                 VIRTUALBOX-HOST-MODULES
可选依赖       : vde2: Virtual Distributed Ethernet
                 support
                 virtualbox-guest-iso: Guest Additions CD
                 image
                 virtualbox-ext-vnc: VNC server support
                 virtualbox-sdk: Developer kit
依赖它         : 无
被可选依赖     : 无
与它冲突       : virtualbox-ose
取代           : virtualbox-ose
安装后大小     : 160.99 MiB
打包者         : Evangelos Foutras
                 <foutrelis@archlinux.org>
编译日期       : 2020年11月10日 星期二 18时11分31秒
安装日期       : 2021年01月18日 星期一 10时52分20秒
安装原因       : 单独指定安装
安装脚本       : 是
验证者         : 数字签名
```

