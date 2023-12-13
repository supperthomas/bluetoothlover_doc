# 概述

蓝牙BLE Host测试需要过认证，传统的方式就是人工打开PTS软件，选择需要认证的case，验证通过就行，这样操作简单直接。

但是PTS测试需要设备配置不同的参数，如配置不同的GATT Service，配对模式等。也就是说跑不同的case，需要根据不同的case写不同的Application，如果这个工作只进行一次还好，但是SPEC一直在演进，协议栈也会一直迭代，认证的流程需要进行多次，继续用人工的方式不仅仅容易出错，工作量还特别大。

PTS本身提供了，auto的支持，可以通过其提供的接口来实现自动完成PTS的认证工作。

![image-20231201171940961](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20231201171940961.png)



既然是自动的，肯定有一套协议来控制协议栈来做不同的动作，设备端只要实现这套协议即可，就可以实现Auto-PTS测试功能。但是PTS提供的接口是一个COM库 (Component Object Model)的API接口，这些API接口是完成和PTS软件进行交互的，并不适合直接将这些接口转发到设备端，所以就需要一个转换接口，将这些API转化为设备好处理的协议。





# auto-pts开源项目介绍

直接去看官方的文档，将COM API转成设备好处理协议工作量很大，网上有开源的auto-pts项目（[GitHub - auto-pts/auto-pts: The Bluetooth PTS automation framework](https://github.com/auto-pts/auto-pts)），里面有BlueZ、Zephyr和Mynewt的实现。

该项目实现了官方COM接口，并提供了BTP(Bluetooth Test Protocol) 协议接口，该接口类似于HCI接口格式，设备可以很好的对这些数据进行处理（相关协议说明在项目的doc目录下，[auto-pts/doc at master · auto-pts/auto-pts · GitHub](https://github.com/auto-pts/auto-pts/tree/master/doc)）。

其支持Linux和Windows模式，但是由于PTS只支持Windows模式，如果设备端是Linux环境的话，需要Windows（PTS）+Linux（设备），然后通过RPC接口进行通信。

![image-20231201174028653](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20231201174028653.png)

![image-20231201174042242](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20231201174042242.png)

其交互主要包含Command、Response和Event三种数据报文格式。

![image-20231201173255924](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20231201173255924.png)

每笔包的数据包格式如下说是，Header有5个字节，后面加具体的Payload内容。

![image-20231201173451096](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20231201173451096.png)

目前Auto-Pts项目支持如下的Service ID，从下图可以看出，目前该项目只支持BLE相关的测试例程，如果是双模设备需要过认证，就得自己参考该项目，将官方的COM API转成新的Service ID的BTP格式（自己实现）。

![image-20231201173642841](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20231201173642841.png)



# Zephyr_polling工作

如上述沟通，要实现Auto-PTS功能，设备端只需要实现BTP相关协议即可。然后物理接口再在Auto-PTS设计实现，参考已有的BlueZ、Zephyr和Mynewt的实现来做即可。

Zephyr_polling参考的是Zephyr项目，可以先参考官方的文档[AutoPTS on Windows 10 with nRF52 board — Zephyr Project Documentation](https://docs.zephyrproject.org/latest/connectivity/bluetooth/autopts/autopts-win10.html)。

Zephyr的Auto-PTS实现在（zephyr/tests/bluetooth/tester/）目录下，支持BTP packets 的收发，用nordic的板子，就可直接用于auto pts 的测试。

Zephyr_polling就是将Zephyr这块代码直接搬过来了。然后通过UART和PC进行BTP交互，Auto-PTS全用github的就行。

相关项目代码已提交：[GitHub - bobwenstudy/RTT_PACKAGE_zephyr_polling: 专用于rtthread package的分支](https://github.com/bobwenstudy/RTT_PACKAGE_zephyr_polling)，代码在example/tester目录下，目前还有些bug。



# Artpi运行实现



## 硬件准备

运行Auto-PTS需要2个硬件设备，一个是待测设备（也就是Artpi），一个是PTS Dongle。

### PTS Dongle

[Bluetooth SIG](https://store.bluetooth.com/)

![image-20231201182529547](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20231201182529547.png)

### ArtPi

另外一个就是Artpi了，官网是：[ART-Pi (gitee.io)](https://art-pi.gitee.io/website/)

![image-20231201182643376](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20231201182643376.png)









## auto-pts环境安装

1. 首先从 https://github.com/auto-pts/auto-pts 安装工程

2. 安装python依赖

   python -m pip install --user wheel
   python -m pip install --user -r autoptsserver_requirements.txt
   python -m pip install --user -r autoptsclient_requirements.txt





## socat安装

下载网址：[Unix Utils ported to Windows - Browse /socat/1.7.3.2 at SourceForge.net](https://sourceforge.net/projects/unix-utils/files/socat/1.7.3.2/)
Auto-pts 通过socat 进行PC 与IUT 之间的交互。
进入网站下载并解压指定软件压缩包，并将socat.exe 所在目录路径添加至环境变量。

确保`where socat`可以找到。



![image-20231201182245167](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20231201182245167.png)









## Artpi-Zephyr_polling环境安装

参考该文章，搭建RTT的Artpi环境。[zephyr_polling rtthread移植平台说明_zephyr 移植-CSDN博客](https://blog.csdn.net/wenbo13579/article/details/129755818)。

目前代码还有问题，通路通了。直接将tester目录下的代码替换到beacon中，然后运行例程，输入zephyr，启动程序。



![image-20231201181616405](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20231201181616405.png)

其中Uart1作为和PC的BTP交互通道。

![image-20231201181648362](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20231201181648362.png)

也就是下图的这两个IO口。

![image-20231201181725776](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20231201181725776.png)

也就是板子的这个位置。

![image-20231201181821143](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20231201181821143.png)



这时通过串口工具，就可以和设备进行BTP交互了。

设备刚上电会上报<00 80 FF 00 00>，注意，这里每次case运行的时候都必须上报。不然auto-pts不会继续运行。

测试发送<00 03 ff 01 00 01>，看设备是否能正常回复<00 03 FF 00 00>，这里通了代表硬件和软件代码ready。

![image-20231201181923573](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20231201181923573.png)







## auto-pts运行

### 启动auto-pts server

将PTS Dongle接入PC，通过sscom确认其串口号。

![image-20231201222013533](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20231201222013533.png)

而后直接在拉取的auto-pts工程下输入，注意调整串口号，这里是COM14。

```
python autoptsserver.py -S 65000 --dongle COM14
```

看到如下显示就是ok了。

注意，这里因为要运行PTS，所以必须要有Sig账号，如果没登录过，这里会提示登录。

![image-20231201222145343](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20231201222145343.png)



### 启动auto-pts client

接着就是要启动IUT设备了，这里直接使用Zephyr的工程，因为其本身就是串口，而且串口交互的就是BTP帧格式，只要串口参数配置对了，直接就可以用Zephyr的工程跑了。

接入Artpi，如下图所示，COM12是Debug口，COM13是引出来和Auto-PTS通信的uart1口。

![image-20231201222751846](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20231201222751846.png)



用RTT的终端接入COM12作为调试口，需要注意，这里暂时别输入zephyr，启动蓝牙。

因为Auto-PTS要求每次运行Case前，需要设备先上报一个Event<00 80 FF 00 00>，该命令是程序一启动就自动上报，且只上报一次。

Zephyr项目通过指定board（-b nrf52）来知道如何该板子是什么，然后通过Jlink下发Reset命令，这里暂时通过手动操作来解决。

![image-20231201222913782](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20231201222913782.png)



而后就运行Auto-PTS的client脚本。命令如下，COM口选13，因为这里只是为了演示需要，所以以简单的DIS相关例程做演示，<-c DIS>指定。

```
python autoptsclient-zephyr.py zephyr-master -t COM13 -S 65000 -C 65001 -c DIS
```

启动后会看到server终端有HTTPS的提示。

![image-20231201223448905](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20231201223448905.png)



然后由于没有做硬件reset，所以需要在case启动后，输入zephyr，启动蓝牙，并上报Event<00 80 FF 00 00>。

之后就能看到日志里打印正常进行BTP通信了。

![image-20231201223738784](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20231201223738784.png)



由于目前还有bug，case都未通过，失败日志可以在auto-pts工程路径下看到。

![image-20231201223925651](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20231201223925651.png)



虽然因为时间仓促，case未运行成功，但是整个通道是打通的，之后按照case要求，解决相关bug即可。





