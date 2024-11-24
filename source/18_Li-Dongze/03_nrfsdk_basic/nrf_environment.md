# ncs环境搭建问题解决

## ncs介绍

全称**[nRF Connect SDK](https://www.nordicsemi.cn/tools/nrfconnectsdk/)**，是一个可扩展的统一软件开发套件，用于构建基于我们所有 [nRF52](https://www.nordicsemi.cn/tag/nrf52/)、[nRF53](https://www.nordicsemi.cn/tag/nrf53/), [nRF70](https://www.nordicsemi.cn/tag/nrf70/) 和 [nRF91](https://www.nordicsemi.cn/tag/nrf91/) 系列无线设备的产品。它为开发人员提供了一个可扩展的框架，用于为内存受限的设备构建尺寸优化的软件，以及为更高级的设备和应用程序构建强大而复杂的软件。它集成了 [Zephyr RTOS](https://zephyrproject.org/) 和各种示例、应用程序协议、协议栈、库和硬件驱动程序。

**ncs+vscode**是目前官方主推的开发方式，另外早期的nRF Connect SDK还支持Segger embedded studio：https://www.segger.com/downloads/embedded-studio/embeddedstudio_arm_nordic_win_x64（64-bit Windows），**不过从nRF Connect SDK v2.0.0开始，NCS将不再支持SES了。**

## 主要参考文档

- 官方文档： [nRF Connect SDK Fundamentals](https://academy.nordicsemi.com/courses/nrf-connect-sdk-fundamentals/)
- 国内教程：https://www.cnblogs.com/iini/p/14174427.html
- 官方b站：https://www.bilibili.com/video/BV1EM4y1w78v?spm_id_from=333.788.videopod.sections&vd_source=cb3035aabee93b98268db84a2ab962fc

## 安装过程中遇到的困难及解决方案

### 1. ncs网速慢安装失败

原先跟着官方文档一步一步走，官方是直接再vscode中安装ncs的，过程中会从github中clone源码，而整个ncs很大，大约4g左右，导致不管用没用科学上网，都会失败

![image-20241124185718299](https://picture-note-1328988318.cos.ap-nanjing.myqcloud.com/Typora/202411241857417.png)

#### 解决过程

网上的解决方法有三种：

1. 通过nRF Connect桌面版直接GitHub下载
2. 百度网盘下载
3. 设置国内Gitee镜像安装

首先试了第一种用ncs桌面版安装，依然失败，本质和用vscode一样，还是从github下载

![image-20241124190616589](https://picture-note-1328988318.cos.ap-nanjing.myqcloud.com/Typora/202411241906638.png)

接着试了gitee换源，过程太繁琐，失败

最后只能用百度网盘下载，更新到v2.7.0，最新的v2.8.0没有，工具链配置还是从vscode中下载

#### 仍有缺陷

目前只能把ncs放在c盘里才能打开，原因是vscode下载的工具链默认在c盘，还未找到可以在哪里更改下载位置

### 2. 烧录失败

最后一步烧录的过程中总是失败：

`required program JLink.exe not found; install it or add its location to PATH`

#### 解决过程

未选对板子，在配置build时需选对开发板，不能只看芯片

![image-20241124191724586](https://picture-note-1328988318.cos.ap-nanjing.myqcloud.com/Typora/202411241917662.png)

## 总结

后续解决只能装在c盘问题后，会完成完整安装教程

















