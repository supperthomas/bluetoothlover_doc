# MCUBOOT

## 什么是MCUBOOT

[mcuboot](https://mcuboot.com) 和常用的BootLoader有一些区别，实际上mcuboot相当于一个安全的引导程序，（注意这里的mcuboot只关注于安全引导，像我们常用的BootLoader的传输啊什么之类的，并不在mcuboot定义范围内）

mcuboot有以下功能

- 固件更新的安全性检查，固件签名
- 标准的FLASH MAP分配规则
- 移植起来比较方便

还可以通过添加config的方式添加如下功能：
- 加解密固件二进制
- 容错升级（意外重启之后恢复）
- 恢复系统

参考链接

[MCUBOOT 官网](https://mcuboot.com)

[MCUBOOT 文档](https://www.mcuboot.com/documentation/)

[MCUBOOT 设计文档](https://www.mcuboot.com/documentation/design/)

[MCUBOOT GITHUB](https://github.com/mcu-tools/mcuboot)


## 固件签名

通常BootLoader基本不会涉及到固件签名，那什么是固件签名呢？通常理解可以理解为银行卡签名，只要你的固件firmware的bin里面一个字节改动了，都无法获取相同的签名，意思是签名很难伪造，比如有时候有些人把固件反汇编一下，改了里面某个初始化值，那签名就要重新签，通常如果没有签名，就可以直接用了，但是如果有签名，会发现固件有改动。主要为了防止不法分子来修改firmware
生成签名就要密钥生成。

## 为什么要签名固件

首先防止攻击者修改固件，或者替换为自己的固件，窥探固件中的信息，并且修改。 签名是安全中的重要组成部分，固件签名不能做什么？

- 并不能防止反汇编
- 没有硬件放篡改
- JTAG防止调试
这些mcuboot都是没有的。

签名有公钥和私钥，应该保密，公钥可以自由分发用于验证签名

## ECDSA

Elliptic Curve Digital Signature Algorithm

椭圆曲线数字签名算法

这个是签名算法，签名算法有很多，比如RSA、DSA、ECDSA。

这个算法其实在很多场景中会用到，蓝牙，加密传输等等。

想深入了解可以参考这篇文章

[Understanding-how-ECDSA-protects-your-data](https://www.instructables.com/Understanding-how-ECDSA-protects-your-data/)

[一文读懂ECDSA算法如何保护数据](https://zhuanlan.zhihu.com/p/97953640)



# MCUBOOT 的使用情况

支持的OS

- Zephyr
- Mynewt
- RIOT
- MBED-OS
- Simulator

支持的开发板
- zephyr里面的nrf52840 等基本开发板都可以使用
- cypress PSoC 6 芯片

从目前的来看，运行的最好的硬件平台是zephyr+nRF52840-DK


## MCUBOOT依赖情况

实际上MCUBOOT并不完全依赖OS，MCUBOOT依赖以下驱动

- FLASH驱动（这个读写FLASH需要使用到）
- UART驱动（这个主要用来调试和打log）
- 加密模块（这个用硬件软件都可以实现）
- MCU启动APP和初始化部分（这部分依赖于平台相关的内容）

## MCUBOOT大小

MCUBOOT大小实际上不是很大，但是有一块加密这块，如果没有对应的硬件实现的话，软件实现的medlt，差不多不带mbedtls的话会<64KB左右，如果用软件实现加密的话可能会大于64KB左右。这个对嵌入式里面来说的话，还是比较大的，所以有些小型的MCU例如M0之类的就不用考虑这个MCUBOOT了，直接上BootLoader了。至少你的FLASH 256KB以上。
一般MCUBOOT 设置为0x20000是保险的，一般不会超过128KB


## MCUBOOT支持的软件加密模块

MCUBOOT提供两种软件加密的方式

- MBEDTLS
- TINYCRYPT


##  MCUBOOT 配置

带有MCUBOOT_头部的
./build/zephyr/include/generated/autoconf.h 这个文件会生成所有的zephyr的相关的配置，这些都是根据boot/Kconfig里面的配置生成的

## MCUBOOT 一些概念

- images 这个指固件，对于trustzone还分为安全固件和非安全固件

- slots 每个固件都可以保存在`primary` 或者 `secondary`的slot（插槽）里面。`primary`就是执行的程序，`secondary`可以用来更新程序

## MCUBOOT 更新方式

###  覆盖模式

这种模式无法恢复到primary之前的状态，直接将secondary直接覆盖替换

- MCUBOOT_OVERWRITE_ONLY 覆盖模式，更新的时候，

### 交换模式

这种模式对源版本是一种保护，将primary的先放到SWAP区域，然后再用secondary替换primary，如果失败则从SWAP降级到源版本。这个对FLASH需求会大一些，同样对FLASH的使用次数也是成倍的上升，如果没有特别需求，可以不用这个模式。

- MCUBOOT_SWAP_USING_MOVE

## 加密部分
MCUboot 没有实现自己的加密库。Tinycrypt和Mbed TLS有可用的默认端口，可以分别使用MCUBOOT_USE_TINYCRYPT和MCUBOOT_USE_MBED_TLS标志启用它们。

如果有可用的硬件加速器，也可以实现一个端口来利用它。NRF 平台加密引擎已经有一个实现，可以使用MCUBOOT_USE_CC310.

该MCUBOOT_VALIDATE_PRIMARY_SLOT标志控制是否在每次启动时验证映像。默认（和推荐）设置是在每次启动时验证。如果您的映像很大或您的 MCU 时钟很慢，则硬件加密加速器可能会对您的启动时间产生显着差异。

对于初始移植，我建议从软件加密库之一开始，测量引导和升级时间的样子，并根据这些结果决定是否需要硬件加速器。



## Nordic MCUBOOT 的使用








##  参考文档

[MCUboot Walkthrough and Porting Guide](https://interrupt.memfault.com/blog/mcuboot-overview?query=from%20zero%20to%20main)


```C
int main(void) {
  // ...
  struct boot_rsp rsp;
  int rv = boot_go(&rsp);

  if (rv == 0) {
    // 'rsp' contains the start address of the image
    your_platform_do_boot(&rsp);
  }
```
