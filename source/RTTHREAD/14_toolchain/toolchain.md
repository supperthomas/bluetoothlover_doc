# 嵌入式TOOLchain工具 梳理

## 简介

本文总结和梳理一下一些toolchain的规则和原理，方便后续跨平台的时候，给大家使用toolchain做一个参考。

解释如何理解`arm-none-eabi-gcc`等含义，以及如何一看就知道该用什么编译器。

当然如果有哪里写的不是很正确的，欢迎评论区纠正，大家讨论讨论看看自己用的编译器什么含义。

## toolchain命名规则

首先我们根据最熟悉的`arm-none-eabi-gcc`  来理解命名规则，最后的gcc是工具，可能是gdb啥其他的，前面的

命名规则为：arch [-vendor] [-os] [-(gnu)eabi]

- arch - 体系架构，如ARM，MIPS
- vendor - 工具链提供商（这里如果没有厂商名称常用的是none和Unkonwn)
- os - 目标操作系统(这里可能是linux，或者其他OS平台等)
- eabi - 嵌入式应用二进制接口（Embedded Application Binary Interface）

仔细看这个命名规则,可以看到中间的os其实是可选项

第一个参数是arch架构，具体有哪些待会介绍。

第二个参数是`vendor` 这个具体厂商自己编译的toolchain 我们就不讲了，一般很多小公司会自己定义toolchain，

重点介绍常见的`none`和`unknown`  

- none： 通常指特别指明没有特定厂商， 通用的编译器
- unknown: 这里表示目标平台的 **操作系统未知** 或 **没有特定的操作系统** 这个是代码中的默认指，应该是即可能指没有os，也可能指没有厂商（很多可能自己编译，没有设置特定的值，就是该值）

`arm-linux-gnueabi-gcc` 

看这个参数就带了linux的参数代表基于linux平台的编译器，通常用来编译liunx操作系统相关的bin。

## GCC源码

所有这些呢都来自于GCC源码：

https://gcc.gnu.org/git/gcc.git

我们来看下`arm-none-eabi-gcc`

官网

https://developer.arm.com/downloads/-/gnu-rm

官网中有介绍

```
Features:
All GCC 10.3 features.
```

![image-20250402215008859](images/image-20250402215008859.png)

所以大概率是基于10.3.0 的版本进行编译

另外从要下载的内容中可以看到最后一个参数是平台的相关参数，代表你要在windows上跑exe还是在linux上跑非exe的包，这里你要知道你的操作系统，windows只要下载win32即可。linux根据笔记本或者电脑芯片是ARM的还是x86的选择对应的，macos也有。

![image-20250402215128926](images/image-20250402215128926.png)



我们下载执行一下`-v`命令

![image-20250402215641681](images/image-20250402215641681.png)

这里有很多内容，具体哪里是我们需要参考的呢，这里有很多，大都是在用gcc编译的时候的参数



```
Configured
with:
/mnt/workspace/workspace/GCC-10-pipeline/jenkins-GCC-10-pipeline-338_20211018_1634516203/src/gcc/configure
--build=x86_64-linux-gnu
--host=i686-w64-mingw32
--target=arm-none-eabi
--prefix=/mnt/workspace/workspace/GCC-10-pipeline/jenkins-GCC-10-pipeline-338_20211018_1634516203/install-mingw
--libexecdir=/mnt/workspace/workspace/GCC-10-pipeline/jenkins-GCC-10-pipeline-338_20211018_1634516203/install-mingw/lib
--infodir=/mnt/workspace/workspace/GCC-10-pipeline/jenkins-GCC-10-pipeline-338_20211018_1634516203/install-mingw/share/doc/gcc-arm-none-eabi/info
--mandir=/mnt/workspace/workspace/GCC-10-pipeline/jenkins-GCC-10-pipeline-338_20211018_1634516203/install-mingw/share/doc/gcc-arm-none-eabi/man
--htmldir=/mnt/workspace/workspace/GCC-10-pipeline/jenkins-GCC-10-pipeline-338_20211018_1634516203/install-mingw/share/doc/gcc-arm-none-eabi/html
--pdfdir=/mnt/workspace/workspace/GCC-10-pipeline/jenkins-GCC-10-pipeline-338_20211018_1634516203/install-mingw/share/doc/gcc-arm-none-eabi/pdf
--enable-languages=c,c++
--enable-mingw-wildcard
--disable-decimal-float
--disable-libffi
--disable-libgomp
--disable-libmudflap
--disable-libquadmath
--disable-libssp
--disable-libstdcxx-pch
--disable-nls
--disable-shared
--disable-threads
--disable-tls
--with-gnu-as
--with-gnu-ld
--with-headers=yes
--with-newlib
--with-python-dir=share/gcc-arm-none-eabi
--with-sysroot=/mnt/workspace/workspace/GCC-10-pipeline/jenkins-GCC-10-pipeline-338_20211018_1634516203/install-mingw/arm-none-eabi
--with-libiconv-prefix=/mnt/workspace/workspace/GCC-10-pipeline/jenkins-GCC-10-pipeline-338_20211018_1634516203/build-mingw/host-libs/usr
--with-gmp=/mnt/workspace/workspace/GCC-10-pipeline/jenkins-GCC-10-pipeline-338_20211018_1634516203/build-mingw/host-libs/usr
--with-mpfr=/mnt/workspace/workspace/GCC-10-pipeline/jenkins-GCC-10-pipeline-338_20211018_1634516203/build-mingw/host-libs/usr
--with-mpc=/mnt/workspace/workspace/GCC-10-pipeline/jenkins-GCC-10-pipeline-338_20211018_1634516203/build-mingw/host-libs/usr
--with-isl=/mnt/workspace/workspace/GCC-10-pipeline/jenkins-GCC-10-pipeline-338_20211018_1634516203/build-mingw/host-libs/usr
--with-libelf=/mnt/workspace/workspace/GCC-10-pipeline/jenkins-GCC-10-pipeline-338_20211018_1634516203/build-mingw/host-libs/usr
--with-host-libstdcxx='-static-libgcc
-Wl,-Bstatic,-lstdc++,-Bdynamic
-lm'
--with-pkgversion='GNU
Arm
Embedded
Toolchain
10.3-2021.10'
--with-multilib-list=rmprofile,aprofile
```

我们用命令`arm-none-eabi-gcc -march=?`

结果如下

```
arm-none-eabi-gcc: error: unrecognized -march target: ?
arm-none-eabi-gcc: note: valid arguments are: armv4 armv4t armv5t armv5te armv5tej armv6 armv6j armv6k armv6z armv6kz armv6zk armv6t2 armv6-m armv6s-m armv7 armv7-a armv7ve armv7-r armv7-m armv7e-m armv8-a armv8.1-a armv8.2-a armv8.3-a armv8.4-a armv8.5-a armv8.6-a armv8-m.base armv8-m.main armv8-r armv8.1-m.main iwmmxt iwmmxt2
arm-none-eabi-gcc: error: missing argument to '-march='
arm-none-eabi-gcc: fatal error: no input files
compilation terminated.
```

大概了解这个支持这么多的架构,当然每种架构的芯片都有很多种，这个目前大部分是

## ARM

刚才的页面是嵌入式单独的页面，下面我们就来上强度，来个全一点的内容：

https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads

这里的toolchain 超级多，会不会有选择困难？理解下面几个概念

架构

- **AArch32**：
  - 是 32 位的 ARM 架构，适用于 ARMv7 及更早版本。
  - 主要用于低功耗、资源受限的嵌入式设备。
- **AArch64**：
  - 是 64 位的 ARM 架构，属于 ARMv8 及更高版本。
  - 提供更大的寻址空间和更高效的指令集。

可执行文件

- **ELF (Executable and Linkable Format)**：
  - 是一种通用的文件格式，用于可执行文件、目标文件和共享库。
  - 适用于多种架构，包括 32 位和 64 位。
- **EABI (Embedded Application Binary Interface)**：
  - 是针对嵌入式系统的二进制接口规范。
  - 定义了数据类型、寄存器使用、堆栈组织等标准。
  - 主要用于 32 位 ARM 架构。

简单理解就是： elf搭配aarch64 支持的架构更大，像64bit的寻址，elf的文件类型也更通用，当然需要的资源和编译出来的bin也就更大。

eabi搭配aarch32 则针对嵌入式的小型的32bit的系统寻址，eabi的接口规范编译出来的也更针对嵌入式，编译出来的会小一些，但是也就适合小型的系统。

- arm-none-eabi: 嵌入式的stm32之类的，无os的，32bit的MCU
- arm-none-linux-gnueabihf:  代表工具链生成的可执行文件，是运行在linux操作系统上的。none代表通用
- aarch64-none-elf:  这个支持更大的64bit的MCU，无os运行的，比如RK3588上直接执行裸机程序
- aarch64-none-linux-gnu: 这个是生成在linux上执行的bin文件

### host主机

host主机就是你当前希望编译器在哪颗CPU上运行，就是你电脑的架构

host主机分为以下几种：

- i686： 一种 32 位的 x86 架构，主要用于个人电脑和服务器，例如Pentium Pro、Pentium II、Pentium III、Pentium 4 等, i686 架构已逐渐被 64 位的 x86_64 架构逐步取代,所以不用关心
- x86_x64: 向后兼容 32 位应用程序，同时支持 64 位应用程序，这个是我们常见的intel和amd的cpu架构
- aarch64:  通常也有可能，比如你用RK3588当作小电脑来运行。
- linux/macos/windowns:  接下来就选择你常用的操作系统，通常是windows

所以常用的，就选择windows，ubuntu就选linux

> note 这里我们没有看到unknown字样，实际上我觉得这样理解：出现unknown基本都是山寨的，不是官方或者正常发布toolchain机构发布的

接下来我们就知道当前如果是windows的话，想编译STM32等裸机的话，大概率用下面的编译器

arm-gnu-toolchain-14.2.rel1-mingw-w64-x86_64-arm-none-eabi.zip

如果遇到大型的linux嵌入式，大概率用下面的

arm-gnu-toolchain-14.2.rel1-mingw-w64-x86_64-arm-none-linux-gnueabihf.zip

mingw 主要是为了告诉你是在mingw里面进行编译的toolchain

`MinGW-w64` 是一个开源的编译器工具链，用于在 Windows 平台上开发原生的 C/C++ 程序。 它是 `MinGW`（Minimalist GNU for Windows）项目的扩展，提供了对 64 位和 32 位程序的支持

macos也分为`darwin-x86_64` (intel CPU) 和`darwin-arm64` (arm CPU m1) 

### GNU

另外对于linux平台还有下面的专业术语解释以下：

arm-none-linux-gnueabihf：
使用 硬件浮点（Hard Float），默认浮点运算使用浮点寄存器（-mfloat-abi=hard），性能更好。
aarch64-none-linux-gnu：
默认也支持硬件浮点，但通常不需要显式指定浮点 ABI，因为 AArch64 架构本身支持浮点运算。

gnu种eabihf代表支持硬件浮点，一般FPU,通常linuxarm 32位的话，默认支持硬件浮点寄存器。

GNU什么含义：

GNU 全称：GNU's Not Unix， GNU 提供了一系列用于开发和编译软件的工具，包括 GCC（GNU 编译器集合）、GDB（GNU 调试器）、Binutils（二进制工具集）等，

通常linux后面都跟着gnu， linux-gnu

可以看到下面的toolchain，开头也有gnu字样，代表工具链里面的gcc，gdb等集成工具。

arm-gnu-toolchain-14.2.rel1-mingw-w64-x86_64-arm-none-eabi.zip

### EABI

EABI（Embedded Application Binary Interface，嵌入式应用二进制接口）是由 ARM 公司及其合作伙伴共同开发的标准。它定义了在 ARM 架构上，编译器、汇编器、链接器等工具如何生成目标文件和可执行文件，以确保不同编译器生成的代码可以在 ARM 系统上互操作。

##  RISCV



## 制作和发布toolchain的公司



https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads

http://www.codesourcery.com/  这个已经不存在了，



参考：

[riscv 各种版本GCC](https://www.cnblogs.com/ppqppl/articles/18077030)

