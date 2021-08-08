

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

- 没有硬件防篡改

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

这个是mcuboot里面的用到的一种加密算法



## MCUBOOT 的使用情况

目前mcuboot支持的平台

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

实际上你可能会有一种感觉，mcuboot什么都没有做，实际上它解决的是安全问题。

## MCUBOOT大小

MCUBOOT大小实际上不是很大，但是有一块加密这块，如果没有对应的硬件实现的话，软件实现的medlt，代码会比较大，差不多不带mbedtls的话会<64KB左右，如果用软件实现加密的话可能会大于64KB左右。这个对嵌入式里面来说的话，还是比较大的，所以有些小型的MCU例如M0之类的就不用考虑这个MCUBOOT了，直接上BootLoader了。至少你的FLASH 256KB以上。
一般MCUBOOT 设置为0x20000是保险的，一般不会超过128KB。




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

###  覆盖模式 OVERWRITE	

这种模式无法恢复到primary之前的状态，直接将secondary直接覆盖替换

- MCUBOOT_OVERWRITE_ONLY 覆盖模式，更新的时候，通常使用的就是这个模式

### 交换模式

这种模式对源版本是一种保护，将primary的先放到SWAP区域，然后再用secondary替换primary，如果失败则从SWAP降级到源版本。这个对FLASH需求会大一些，同样对FLASH的使用次数也是成倍的上升，如果没有特别需求，可以不用这个模式。

- MCUBOOT_SWAP_USING_MOVE

这个模式主要是会把primary先保存到SWAP区域，然后更新代码，之后如果运行不了，会再次将SWAP里面的代码更新回来。

## 加密部分
MCUboot 没有实现自己的加密库。Tinycrypt和Mbed TLS有可用的默认端口，可以分别使用MCUBOOT_USE_TINYCRYPT和MCUBOOT_USE_MBED_TLS标志启用它们。

如果有可用的硬件加速器，也可以实现一个端口来利用它。NRF 平台加密引擎已经有一个实现，可以使用MCUBOOT_USE_CC310。

nordic的硬件代码实现在ext/nrf/cc310_glue.c文件中，该硬件实现了P256和ECDSA。这边加密部分我并没有去深究太深，感觉也是一块比较通用的模块。

该MCUBOOT_VALIDATE_PRIMARY_SLOT标志控制是否在每次启动时验证映像。默认（和推荐）设置是在每次启动时验证。如果您的映像很大或您的 MCU 时钟很慢，则硬件加密加速器可能会对您的启动时间产生显着差异。

对于初始移植，我建议从软件加密库之一开始，测量引导和升级时间的样子，并根据这些结果决定是否需要硬件加速器。



## Nordic MCUBOOT 的使用

如果你手上有一块nordic 52840的开发板，恭喜你，你可以比较完整的运行mcuboot，并且在硬件上运行起来。

这边我可以提供3个bin文件。

是根据官方生成的mcuboot.bin、signed-hello1.bin、signed-hello2.bin

mcuboot.bin是BootLoader， 烧入地址是0x0

signed-hello1.bin是app1在primary中，烧入的FLASH偏移是0xc000 size是67000

signed-hello2.bin是app2在secondary，烧入的FLASH偏移是0x73000  size是67000

 

### BIN文件如何生成

首先需要了解下[zephyr 的nordic52840](https://docs.zephyrproject.org/latest/boards/arm/nrf52840dk_nrf52840/doc/index.html)如何运行，比如跑一个hello world

之后根据Nordic的[nrf_MCUBOOT官方文档](https://developer.nordicsemi.com/nRF_Connect_SDK/doc/latest/mcuboot/wrapper.html)

根据[NRF_编译步骤](https://developer.nordicsemi.com/nRF_Connect_SDK/doc/latest/mcuboot/readme-zephyr.html) 这个可以搭建环境

再根据nordic的[test plan](https://developer.nordicsemi.com/nRF_Connect_SDK/doc/latest/mcuboot/testplan-zephyr.html)

可以生成mcuboot.bin、signed-hello1.bin、signed-hello2.bin

需要提醒的是，官方给的sample是`make test-good-rsa `

实际上通过实践证明，其实我们如果想要烧入hello2之后可以执行hello2的话，需要使用命令`make test-overwrite`

之后的烧入命令`make flash_boot` 是烧入mcuboot

`make flash_hello1` 是烧入hello1这个烧完之后会直接运行hello1的代码。

`make flash_hello2` 这个是烧入hello2这个烧完之后reset会从hello2的代码进行运行。

从Makefile里面的代码可以看出来

```
flash_boot:
        $(PYOCD) flash -a 0 mcuboot.bin --target nrf52840

flash_hello1:
        $(PYOCD) flash -a 0xc000 signed-hello1.bin --target nrf52840

flash_hello2:
        $(PYOCD) flash -a 0x73000 signed-hello2.bin --target nrf52840

flash_full:
        $(PYOCD) flash -e chip -a 0 full.bin --target nrf52840
```



### BIN头部

IMAGE头部有部分版本信息

```
struct image_version {
    uint8_t iv_major;
    uint8_t iv_minor;
    uint16_t iv_revision;
    uint32_t iv_build_num;
};

/** Image header.  All fields are in little endian byte order. */
struct image_header {
    uint32_t ih_magic;
    uint32_t ih_load_addr;
    uint16_t ih_hdr_size;           /* Size of image header (bytes). */
    uint16_t ih_protect_tlv_size;   /* Size of protected TLV area (bytes). */
    uint32_t ih_img_size;           /* Does not include header. */
    uint32_t ih_flags;              /* IMAGE_F_[...]. */
    struct image_version ih_ver;
    uint32_t _pad1;
};
```

image_header 仔细数下，差不多是8*4个字节（32个字节）。 差不多是0x20个字节下面我们dump出signed-hello1.bin的头部

```
0000000 b83d 96f3 0000 0000 0200 0000 3e54 0000
0000010 0000 0000 0201 0000 0000 0000 0000 0000
0000020 0000 0000 0000 0000 0000 0000 0000 0000
*
0000200 0b60 2000 d2f9 0000 f68d 0000 d34d 0000
```

从中间你可以读出以下信息

```
=ih_magic=96f3b83d=====
=ih_load_addr=0=====
=ih_hdr_size=200=====
=ih_protect_tlv_size=0=====
=ih_img_size=3e54=====
=ih_flags=0=====
Image version:01.02 (Rev: 0, Build: 0)
=pad=0=====
```

这边ih_hdr_size设定了是0x200。所以前0x200都是头部。头部信息就差不多这么多。

### SLOT尾部

SLOT其实是你插槽的最后部分，并不是image大小的最后部分，这部分的内容是固定位置的。

```
     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    ~                                                               ~
    ~    Swap status (BOOT_MAX_IMG_SECTORS * min-write-size * 3)    ~
    ~                                                               ~
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                 Encryption key 0 (16 octets) [*]              |
    |                                                               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                 Encryption key 1 (16 octets) [*]              |
    |                                                               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                      Swap size (4 octets)                     |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |   Swap info   |           0xff padding (7 octets)             |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |   Copy done   |           0xff padding (7 octets)             |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |   Image OK    |           0xff padding (7 octets)             |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                       MAGIC (16 octets)                       |
    |                                                               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

尾部有以下信息比较重要MAGIC、copy_done、swap_info、image_ok、

在函数`boot_read_swap_state_by_id` 中有读取这些信息的代码

在函数`boot_swap_type_multi`中有校验这些信息的代码

这里的计算SWAP_TYPE的内容尤为重要，因为这个决定你的BootLoader如何做下一步动作，之前我就是因为嫌弃hello2.bin比较大，修改了以下，导致这里计算SWAP_TYPE出了问题。 SWAP_TYPE_NONE就是什么动作都不会做。



```
   for (i = 0; i < BOOT_SWAP_TABLES_COUNT; i++) {
        table = boot_swap_tables + i;

        if (boot_magic_compatible_check(table->magic_primary_slot,
                                        primary_slot.magic) &&
            boot_magic_compatible_check(table->magic_secondary_slot,
                                        secondary_slot.magic) &&
            (table->image_ok_primary_slot == BOOT_FLAG_ANY   ||
                table->image_ok_primary_slot == primary_slot.image_ok) &&
            (table->image_ok_secondary_slot == BOOT_FLAG_ANY ||
                table->image_ok_secondary_slot == secondary_slot.image_ok) &&
            (table->copy_done_primary_slot == BOOT_FLAG_ANY  ||
                table->copy_done_primary_slot == primary_slot.copy_done)) {
            BOOT_LOG_INF("Swap type: %s",
                         table->swap_type == BOOT_SWAP_TYPE_TEST   ? "test"   :
                         table->swap_type == BOOT_SWAP_TYPE_PERM   ? "perm"   :
                         table->swap_type == BOOT_SWAP_TYPE_REVERT ? "revert" :
                         "BUG; can't happen");
            if (table->swap_type != BOOT_SWAP_TYPE_TEST &&
                    table->swap_type != BOOT_SWAP_TYPE_PERM &&
                    table->swap_type != BOOT_SWAP_TYPE_REVERT) {
                return BOOT_SWAP_TYPE_PANIC;
            }
            return table->swap_type;
        }
    }

```

这部分内容如果想要彻底理解的话需要查看内容

[image-trailers](https://www.mcuboot.com/documentation/design/#image-trailers)

```
const uint32_t boot_img_magic[] = { 
    0xf395c277,
    0x7fefd260,
    0x0f505235,
    0x8079b62c,
};

```

以下是image-hello2.bin的尾部应该从0x4054之后就是对应的一些信息

```
0004050 0000 0000 

6907 0150 

0010 0020 
653e 02df 5f24 8f46 07b5 440b 05e6 e3b6 e434 ab01 9d23 a56c 168f de43 1421 6a6c 

0001 0020 
57fc dc01 3561 32e1 4738 c4bd 040f e5d2 e5be 3b83 c223 939f 3d59 0100 fa8c 9499

0020 0100 
bf7e 8362 f93e eab7 2e7e 0998
00040b0 1e5a 69e2 e126 13b9 854e b19e e2bd d6a6
00040c0 4c90 3eef e89f 3a62 7337 9cc8 3a76 2e4e
00040d0 b33d 2962 d2c4 5e47 d40d 44b9 196f 4791
00040e0 e159 ff9b 4a0b e592 d65d 76fa bd8e 1a15
00040f0 1708 b271 eeea e1de 18f2 0ab7 9173 d92f
0004100 9651 3d5a d432 eca0 653a cd5c 8766 f255
0004110 fc1d 87ca 23e1 28d2 537a bd61 a7bf 7b12
0004120 f786 5a7e 3cad e9a8 8c36 d68a b11c 910a
0004130 cf3f 7c96 9ca6 51a1 6e2a 7d07 92ea 0117
0004140 7adc d048 efab 0d7d b47d 2253 be28 a662
0004150 d52d 0539 eab4 b18d 6e27 5959 17e7 94c5
0004160 03d5 6b23 a0e4 9092 7eb5 21c6 bf1a 1f39
0004170 f627 276d 2927 300b d497 a5a2 d7aa efca
0004180 a259 1c8e 61d1 cee5 425e c47c 8a85 e0c3
0004190 95f9 76cc b871 2a3e b934 7093 b148 7ec9
00041a0 e87f 6ffa ffff ffff ffff ffff ffff ffff
00041b0 ffff ffff ffff ffff ffff ffff ffff ffff
*
0066ff0 c277 f395 d260 7fef 5235 0f50 b62c 8079
0067000
```

### BIN 尾部tlv

紧接着image之后的是一个bin tlv等信息，这个里面会有对应的加密信息，这部分位置是随着image大小而变化的。

这里的实现主要在函数`bootutil_img_validate` 在文件  `boot/bootutil/src/image_validate.c`里面

有以下信息

1. image  image_tlv_info  4个字节

```
struct image_tlv_info {
    uint16_t it_magic;
    uint16_t it_tlv_tot;  /* size of TLV area (including tlv_info header) */
};
offset: 4054

data: 6907 0150 

#define IMAGE_TLV_INFO_MAGIC        0x6907
#define IMAGE_TLV_PROT_INFO_MAGIC   0x6908

```

2. tlv 信息

```
struct image_tlv {
    uint8_t  it_type;   /* IMAGE_TLV_[...]. */
    uint8_t  _pad;
    uint16_t it_len;    /* Data length (not including TLV header). */
};
这里也是先读4个字节，然后读后面的it_len

0010 0020 IMAGE_TLV_SHA256    这个hash检查
653e 02df 5f24 8f46 07b5 440b 05e6 e3b6 e434 ab01 9d23 a56c 168f de43 1421 6a6c 

0001 0020   IMAGE_TLV_KEYHASH  这个是ky
57fc dc01 3561 32e1 4738 c4bd 040f e5d2 e5be 3b83 c223 939f 3d59 0100 fa8c 9499

0020 0100 IMAGE_TLV_RSA2048_PSS   这个是签名验证
bf7e 8362 f93e eab7 2e7e 0998。。。

/*
 * Image trailer TLV types.
 */
#define IMAGE_TLV_KEYHASH           0x01   /* hash of the public key */
#define IMAGE_TLV_SHA256            0x10   /* SHA256 of image hdr and body */
#define IMAGE_TLV_RSA2048_PSS       0x20   /* RSA2048 of hash output */
#define IMAGE_TLV_ECDSA224          0x21   /* ECDSA of hash output */
#define IMAGE_TLV_ECDSA256          0x22   /* ECDSA of hash output */
#define IMAGE_TLV_RSA3072_PSS       0x23   /* RSA3072 of hash output */
#define IMAGE_TLV_ED25519           0x24   /* ED25519 of hash output */
#define IMAGE_TLV_ENC_RSA2048       0x30   /* Key encrypted with RSA-OAEP-2048 */
#define IMAGE_TLV_ENC_KW128         0x31   /* Key encrypted with AES-KW-128 */
#define IMAGE_TLV_ENC_EC256         0x32   /* Key encrypted with ECIES-P256 */
#define IMAGE_TLV_ENC_X25519        0x33   /* Key encrypted with ECIES-X25519 */
#define IMAGE_TLV_DEPENDENCY        0x40   /* Image depends on other image */
#define IMAGE_TLV_SEC_CNT           0x50   /* security counter */

```



###  imgtool.py

生成通常的image之后，需要加头加尾，这个主要在这个`script\imgtool.py`中实现的。这个里面的细节就不去研究了，这个还有很多参数

这边就不展开了

```
hello1: check
        (mkdir -p $(BUILD_DIR_HELLO1) && \
                cd $(BUILD_DIR_HELLO1) && \
                cmake -DFROM_WHO=hello1 \
                        -G"Ninja" \
                        -DBOARD=$(BOARD) \
                        $(SOURCE_DIRECTORY)/hello-world && \
                ninja)
        $(IMGTOOL) sign \
                --key $(SIGNING_KEY) \
                --header-size $(BOOT_HEADER_LEN) \
                --align $(FLASH_ALIGNMENT) \
                --version 1.2 \
                --slot-size 0x67000 \
                $(BUILD_DIR_HELLO1)/zephyr/zephyr.bin \
                signed-hello1.bin
hello2: check
        (mkdir -p $(BUILD_DIR_HELLO2) && \
                cd $(BUILD_DIR_HELLO2) && \
                cmake -DFROM_WHO=hello2 \
                        -G"Ninja" \
                        -DBOARD=$(BOARD) \
                        $(SOURCE_DIRECTORY)/hello-world && \
                ninja)
        $(IMGTOOL) sign \
                --key $(SIGNING_KEY) \
                --header-size $(BOOT_HEADER_LEN) \
                --align $(FLASH_ALIGNMENT) \
                --version 1.3 \
                --slot-size 0x67000 \
                --pad \
                $(BUILD_DIR_HELLO2)/zephyr/zephyr.bin \
                signed-hello2.bin


```

主要之前有个--pad这个好像是填充，之前因为感觉烧入太慢，被我去掉了，导致后面一系列的问题，但是同样解决问题也是学习的最好的方法，通过解决这个问题，基本理解mcuboot里面的运行机制。

## MCUBOOT 运行流程及注意事项

运行流程

在主函数里面

```
boot_go(struct boot_rsp *rsp)
{
    fih_int fih_rc = FIH_FAILURE;
    FIH_CALL(context_boot_go, fih_rc, &boot_data, rsp);
    FIH_RET(fih_rc);
}
```

boot_go=> context_boot_go

然后进入到`boot_prepare_image_for_update` 这个函数，这个函数比较重要

这个函数里面

`boot_read_image_headers`   这个是读出头部信息

接下来

```
1632             if (bs->swap_type == BOOT_SWAP_TYPE_NONE) {
1634                 BOOT_SWAP_TYPE(state) = boot_validated_swap_type(state, bs);
1635             } else {
```

这里会去读取SLOT尾部信息，判断是否需要更新然后计算出SWAP_TYPE

接下来

boot_validate_slot这个是验证image的有效性的。

之后就开始更新代码

回到context_boot_go

进行更新替换。



在secondary烧入到primary之后，还需要注意mcuboot会擦除掉一些信息，让下次不会再去校验头部和尾部。

erase fa_id=2,fa_off=73000 off=0, len=1000
erase fa_id=2,fa_off=73000 off=66000, len=1000
烧完secondary之后，会擦除头部和尾部。




## SWAP类型

SWAP类型决定了是否启动的关键

BOOT_SWAP_TYPE_NONE：“通常”或“不升级”的情况；尝试引导主插槽的内容。

BOOT_SWAP_TYPE_TEST：通过交换映像来引导辅助插槽的内容。除非交换是永久性的，否则在下次启动时恢复。

BOOT_SWAP_TYPE_PERM：永久交换镜像，并启动升级后的镜像固件。

BOOT_SWAP_TYPE_REVERT：之前的测试交换不是永久性的；交换回旧image，其数据现在位于辅助插槽中。如果旧映像在启动时将自身标记为“OK”，则下次启动将具有交换类型BOOT_SWAP_TYPE_NONE。

BOOT_SWAP_TYPE_FAIL: 交换失败，因为要运行的图像无效。

BOOT_SWAP_TYPE_PANIC: 交换遇到不可恢复的错误。



##  参考文档

[MCUboot Walkthrough and Porting Guide](https://interrupt.memfault.com/blog/mcuboot-overview?query=from%20zero%20to%20main)



[MCUBOOT官方主页](https://mcuboot.com)

[MCUBOOT官方文档](https://www.mcuboot.com/documentation/)

[MCUBOOT 官方设计文档](https://www.mcuboot.com/documentation/design/)

[加密相关](https://www.mcuboot.com/documentation/encrypted-images/)

[imgtool工具命令使用](https://www.mcuboot.com/documentation/imgtool/)

签名设计文档：

https://www.mcuboot.com/documentation/ecdsa/               EC256 签名

https://www.mcuboot.com/documentation/signed-images/



[MCUBOOTgithub主分支](https://github.com/mcu-tools/mcuboot)

[nrf-connect MCUBOOT相关文档](https://github.com/nrfconnect/sdk-mcuboot.git)

[Nordic MCUBOOT的参考文档](https://developer.nordicsemi.com/nRF_Connect_SDK/doc/latest/mcuboot/wrapper.html)

ZEPHYR操作系统：

https://github.com/zephyrproject-rtos/zephyr

[zephyr mcuboot nrf52840 测试计划](https://developer.nordicsemi.com/nRF_Connect_SDK/doc/latest/mcuboot/testplan-zephyr.html)

[编译mcuboot nrf52840](https://developer.nordicsemi.com/nRF_Connect_SDK/doc/latest/mcuboot/readme-zephyr.html)

[zephyr笔记 5.3.1 Zephyr 版本 MCUboot 的编译和使用](https://blog.csdn.net/iotisan/article/details/80167804)

[Zephyr应用笔记：mcuboot引导程序简单介绍](https://blog.csdn.net/u010018991/article/details/79483899)



