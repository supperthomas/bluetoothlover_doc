# 基于NRF Connect SDK(NCS)平台nRF5340DK上手体验

## 简言

Nordic的SDK有两套，老的是nRF5 SDK ,而新的是nRF Connect SDK (NCS),两套SDK相互独立。nRF51和nRF52系列可使用nRF SDK,Nordic最新系列需使用nRF Connect SDK (NCS),本文主要围绕nRF5340DK评估版介绍nRF Connect SDK (NCS)的开发环境；

## 开发板介绍

### 开发板硬件

![image-20230415124009945](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimage-20230415124009945.png)

### 芯片资源

这颗芯片支持蓝牙低功耗、蓝牙mesh、NFC、Thread和Zigbee的双核蓝牙5.3 SoC，NRF5340的芯片架构是双核Arm® Cortex®-M33。

- 1MB闪存的512 KB RAM，
- 超低功耗网络处理器，
- 64MHz的频率运行，
- 256 KB闪存和64 KB RAM。
- 应用处理器具有8KB 2路关联高速缓存，
- 该高速缓存具有DSP和浮点功能，
- 提供电压和频率缩放选项。
- 集成了功率优化的多协议2.4 GHz无线电，
- TX电流为3.2mA，RX电流为2.6 mA，休眠电流低至1.1uA。

#### 规格

![image-20230415125050526](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimage-20230415125050526.png)

![image-20230415143246704](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimage-20230415143246704.png)

### 官方相关资料链接

1. [nRF5340芯片资源介绍](https://www.nordicsemi.com/Products/nRF5340?lang=zh-CN)
2. [nRF5340 DK评估版介绍](https://www.nordicsemi.com/Products/Development-hardware/nrf5340-dk?lang=zh-CN)

## nRF Connect SDK开发板环境

主要围绕基于VS Code下的使用！！！

1. [NCS官方介绍](https://www.nordicsemi.com/Products/Development-software/nRF-Connect-SDK)

NRF Connect SDK是一个可扩展的统一软件开发工具包，用于基于所有的nRF52、nRF53、nRF70和nRF91系列无线设备构建产品。为开发人员提供了一个可扩展的框架，用于为内存受限的设备构建大小优化的软件，以及为更高级的设备和应用构建功能强大且复杂的软件。它集成了Zephyr RTOS和广泛的例程、应用协议、协议栈、库和硬件驱动程序，并沿用了Zephyr project的编译系统，内嵌Zephyr RTOS。

NCS使用CMake编译系统，SDK存放于Github，包含多个仓库，其主仓库（Manifest）是nrf，同时还包含Zephyr，MCUBoot，mbedtls，nrfxlib等其他仓库。NCS SDK可以同时在Windows，macOS和Linux上运行。

### 安装nRF Connet for Desktop

nRF Connet for Desktop是一个跨平台工具框架，用于协助nRF设备开发，它包含许多应用程序用来测试，监控和测量，优化和编程应用程序。

[nRF Connet for Desktop官方下载地址](https://www.nordicsemi.com/Products/Development-tools/nRF-Connect-for-desktop/Download#infotabs)

![image-20230415145220898](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimage-20230415145220898.png)

![动画8](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/img动画8.gif)

### 安装VS code

[VS code下载地址](https://code.visualstudio.com/)

### 安装nRF Connect Extension Pack

![image-20230415151803587](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimage-20230415151803587.png)

### 安装nRF Command Line Tools

nRF命令行用于开发，编程和调试Nordic的Semiconductor's nRF51, nRF52, nRF53 and nRF91 系列设备.

[nRF Command Line Tools下载地址](https://www.nordicsemi.com/Products/Development-tools/nRF-Command-Line-Tools/Download)

![image-20230415152447993](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimage-20230415152447993.png)

### 安装Ozone

Ozone是一个适用于J-Link 和 J-Trace 的多平台调试器和分析仪

[Ozone下载地址]([Ozone – The Performance Analyzer (segger.com)](https://www.segger.com/products/development-tools/ozone-j-link-debugger/))

网页拉到底选择

![image-20230415153301645](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimage-20230415153301645.png)

![动画9](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/img动画9.gif)

### 安装nRF Connect SDK

基于3.1章节安装的nRF Connet for Desktop，我们将其打开选择Toolchain Manager点击install如下：

![image-20230415154248866](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimage-20230415154248866.png)

![toolchain](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgtoolchain.gif)

安装好后选择open打开，选择settings选择SDK安装目录：

![toolchain](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgtoolchain.gif)

### 基于VS Code下开发NCS

通过Tloolchain Manager打开VS code,也可通过VS Code 直接打开SDK

![image-20230415161630580](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimage-20230415161630580.png)



#### NCS目录结构

v2.3
 ├── bootloader  ------>mcuboot仓库
 ├── modules     ------->nrf驱动
 ├── nrf               ------->NRF主仓库
 ├── nrfxlib        -------->独立于RTOS库、模块
 ├── test
 ├── tools
 └── zephyr       --------->zephy仓库