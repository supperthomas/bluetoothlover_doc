# VirtualBox 安装 Ubuntu 20.04



## 前置条件

- VirtualBox 6.1
- [Ubuntu 20.04 ISO 镜像](https://developer.aliyun.com/mirror/)（PC 版）

## 安装流程

### 创建 Ubuntu 虚拟机

在“工具”条目选择“新建”，在弹出的对话框里输入“虚拟机名称”，以及虚拟机安装的“文件夹”，然后“类型”选择 Linux，“版本”选择 Ubuntu (64-bit)，点击下一步。

![](images/image-20210126144738482.png)

将虚拟机的内存大小设置为 2048MB，点击下一步。

![](images/image-20210126145001736.png)

选择“现在创建虚拟硬盘”，点击“创建”。

![](images/image-20210126145051708.png)

选择“VDI”类型，点击“下一步”。

![](images/image-20210126145115772.png)

选择“动态分配”，点击“下一步”。

![](images/image-20210126145144199.png)

这里将虚拟硬盘的大小调节为 30GB，然后点击“创建”即可。

![](images/image-20210126145328554.png)

### 安装 Ubuntu

安装 Ubuntu 之前**需要将虚拟机的网断掉**，否则在安装过程中会试图使用 apt 安装软件，国内会特别慢。在“设置 - 网络”里。

![](images/image-20210126145441037.png)

然后点击启动，选择启动盘为我们自己的镜像文件，点击启动。

![](images/image-20210126145536625.png)

直接点击“Install Ubuntu”，

![](images/image-20210126145727628.png)

然后继续点击“Continue”，

![](images/image-20210126145746861.png)

由于我们虚拟机内主要是跑程序，不需要 office, games, media players 这些工具，因此选择 "Minimal installation"，然后点击 "Continue"。

![](images/image-20210126145939287.png)

点击 "Install Now"。

![](images/image-20210126150004904.png)

在弹出的对话框里选择 “Continue" 开始安装，

![](images/image-20210126150034525.png)

选择时区为 "Shanghai"，点击 "Continue"。

![](images/image-20210126150111903.png)

输入用户名和密码，点击 "Continue"，开始安装。

![](images/image-20210126150228737.png)

安装完后选择重启，并按 "Enter" 即可。

### 更换国内源

退出虚拟机，打开虚拟机的网络开关，这里由于我的路由器能够自主分配 IP，因此选择 NAT 模式。

![](images/image-20210126150708164.png)

启动 Ubuntu 虚拟机，在“开始中心”里找到 “Software & Updates"，紫色的那一个。

![](images/image-20210126150925442.png)

然后在 "Ubuntu Software" 选项下的 "Download from" 处，点击 "Server for China"，

![](images/image-20210126151105785.png)

在弹出的菜单项里选择 "Other..."，

![image-20210126151131595](images/image-20210126151131595.png)

在弹出的 "Choose a Download Server" 里找到 China，选择阿里云源，点击 "Choose Server"。

![](images/image-20210126151232640.png)

输入用户名密码，

![](images/image-20210126151328862.png)

打开终端，输入 `sudo apt update` 更新源即可。

## 安装 VirtualBox 增强功能

首先安装依赖环境，

```shell
sudo apt-get install build-essential gcc make perl dkms
```

然后选择 “设备 - 安装增强功能“，

![](images/image-20210126151933129.png)

在弹出的界面里选择 "Run" ，然后输入密码。

![image-20210126152255552](images/image-20210126152255552.png)

等待安装完成后重启虚拟机。

![](images/image-20210126152402275.png)

## VirtualBox USB 设备使用

在进行嵌入式开发时，不可避免要使用串口与设备通信，使用调试器调试设备，这些设备目前都是通过 USB 接入物理机的，虚拟机可以配置后直接使用物理机的 USB 设备。

这里我接入一个 STM32 的 ST-Link 调试器，可以选择 ”设备 - USB - STMicroelectronics STM32 STLink [01000]“ 里直接将 ST-Link 接入到虚拟机，虚拟机里的工具链就可以下载调试该 STM32 了。

![](images/image-20210126152747339.png)

## VirtualBox 共享文件夹设置

**前提**：必须成功安装 VirtualBox 增强功能。

点击 "设备 - 共享文件夹 - 共享文件夹"，

![](images/image-20210126153056839.png)

点击右上角的 `+` 号，

![](images/image-20210126153143669.png)

在弹出的对话框里输入下述信息，点击 OK 。

![image-20210126153300172](images/image-20210126153300172.png)

- 共享文件夹路径：这个是 Windows（物理机）上的文件夹路径（绝对路径）。
- 共享文件夹名称：这个也是 Windows 上的文件夹名称。
- 挂载点：这个是 Ubuntu 里的目录（与 Windows 共享）。

也就是说，VirtualBox 将物理机的 "共享文件夹路径" 与虚拟机的 "挂载点" 联系起来了，两者之间的文件都是共享的。

这是在 /home/jackis 目录下就能够看到 shared 共享目录了。

```shell
jackis@jackis-VirtualBox:~$ pwd
/home/jackis
jackis@jackis-VirtualBox:~$ ls -l | grep "shared"
drwxrwx--- 1 root   vboxsf    0 1月  26 15:39 shared
```

可以看出 shared 目录属性如下：

- 所有者：root，权限：7
- 所属组：vboxsf，权限：7
- 其他人权限：0

这个时候是不能够进入 shared 目录的，因为当前普通用户没有权限，需要将当前用户加入 vboxsf 组内。

```shell
sudo gpasswd -a ${USER} vboxsf
newgrp - vboxsf
```

这样就能够进入 /home/jackis/shared 目录了，也能够操纵共享的文件。

```shell
jackis@jackis-VirtualBox:~/shared$ ls
tmp.txt
```

## VirtualBox 设置共享粘贴板

**前提**：必须成功安装 VirtualBox 增强功能。

我们在使用虚拟机时，难免会需要虚拟机与物理机相互复制粘贴，这时就需要共享粘贴板了。

选择 "设备 - 共享粘贴板 - 双向" 即可。

![](images/image-20210126155248655.png)

## Ubuntu 常用配置

### 增加鼠标滚轮的速度

Ubuntu 里鼠标滚轮的默认速度太慢了，浏览代码简直不能忍受，因此在网上找了种方法增加 Ubuntu 里滚轮滑动的速度。

安装 imwheel：

```
sudo apt-get install imwheel
```

然后编辑文件 `sudo vim ~/.imwheelrc`，添加内容如下：

```
".*"
None,      Up,   Button4, 5
None,      Down, Button5, 5
Control_L, Up,   Control_L|Button4
Control_L, Down, Control_L|Button5
Shift_L,   Up,   Shift_L|Button4
Shift_L,   Down, Shift_L|Button5
```

前两行就分别对应滚轮上滚和下滚的速度，设置为 5 比较合适。

启动 imwheel，

```
killall imwheel
imwheel
```

鼠标侧键与 VSCode 绑定。

https://blog.csdn.net/zhanghm1995/article/details/88876092

## VirtualBox 常见错误

### vmware 启动失败 VERR_SSM_LOAD_CONFIG_MISMATCH

打开虚拟机时报错：

![](images/336252-20210115144014778-1583596993.png)

此时虚拟机处于休眠状态，点击清除虚拟机状态。重启就好。