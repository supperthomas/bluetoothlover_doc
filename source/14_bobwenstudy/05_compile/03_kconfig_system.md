# 从零到一搭建Kconfig配置系统



## 背景说明

最早接触到`Kconfig`是在`zephyr`项目中，之后陆续知道`linux`和`RT-Thread`等项目都是用`Kconfig`来管理编译的，而自己也陆续有大型项目开发需要，了解过后对其使用愈发感兴趣起来。

在实际项目开发中，通常会有需要去使能/关闭一些代码模块或者修改一些配置参数。

项目代码都放在GitHub上，[bobwenstudy/test_kconfig_system (github.com)](https://github.com/bobwenstudy/test_kconfig_system)

### 代码管理

使能或者关闭代码，可以通过`#define+#ifdef`就可以实现这一目的。

```c
#define CONFIG_TEST_ENABLE

#ifdef CONFIG_TEST_ENABLE
	... ... ...
#endif
```

调整配置参数，直接通过`#define`就可以实现这一目的。

```c
#define CONFIG_TEST_SHOW_STRING "Test 123"
#define CONFIG_TEST_SHOW_INT (123)
```

但是通过这个方式有个问题，就是不直观，如果就几个参数还好，但是当参数越来越多，并之前存在先后关系时，管理难度会呈指数上升。

如下面的例子，`CONFIG_TEST_SUB_1_ENABLE`的开启前提是`CONFIG_TEST_TOP_ENABLE`开启，当`CONFIG_TEST_SUB_0_ENABLE`和`CONFIG_TEST_SUB_1_ENABLE`都开启的情况下`CONFIG_TEST_SHOW_INT = 123`，否则`CONFIG_TEST_SHOW_INT = 456`。

这些宏之间的关系都用代码来描述，需要开发人员熟悉所有代码行为，才能很好的配置这些功能。

```c
#define CONFIG_TEST_TOP_ENABLE
#define CONFIG_TEST_SUB_0_ENABLE

#ifdef CONFIG_TEST_TOP_ENABLE
#define CONFIG_TEST_SUB_1_ENABLE
#endif

#if defined(CONFIG_TEST_SUB_0_ENABLE) && defined(CONFIG_TEST_SUB_1_ENABLE)
#define CONFIG_TEST_SHOW_SUB_INT (123)
#else
#define CONFIG_TEST_SHOW_SUB_INT (456)
#endif
```



### 预编译管理

除了在代码中配置外，也可以通过-D预编译来管理，然后编译全局都有这些配置参数了，对应代码中的宏定义。

```c
gcc xxx -DCONFIG_TEST_ENABLE -DCONFIG_TEST_SHOW_INIT=123

#define CONFIG_TEST_ENABLE
#define CONFIG_TEST_SHOW_INIT (123)
```



### 问题

如果是小型项目通过上述两种方式管理都还好，当项目越来越大时，所需配置的参数越来越多时，希望有一个工具专门来管理这些配置参数，并且能够可视化这些编译配置。

而Kconfig就是这样一个通用的工具来解决这一问题。



## 环境搭建

`Kconfig`是一个配置描述文件，而其配置界面程序需要通过GUI来完成，不然看到的只是一些文本文件，并且这个文件并不能被c所识别。

这里推荐用python的[kconfiglib · PyPI](https://pypi.org/project/kconfiglib/)库来使用。

### Kconfiglib安装

直接python安装即可。由于要使用menuconfig，在windows环境下还需要安装`windows-curses`。

```python
python -m pip install windows-curses
python -m pip install kconfiglib
```



安装完成后，会在python路径下生成`menuconfig.exe`执行程序。输入`menuconfig -h`，出现下面的信息说明已经安装好了。

![image-20221021154103835](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221021154103835.png)



### c头文件生成脚本-kconfig.py

使用`Kconfiglib`生成的是`.config`文件，而c代码要使用，必须要提供头文件。其实生成功能主要还是依靠`kconfiglib`中提供的`class Kconfig`中的`write_autoconf`方法，但是也需要一个脚本来调用这个库。

源码所在路径为：[Kconfiglib/kconfiglib.py at master · ulfalizer/Kconfiglib (github.com)](https://github.com/ulfalizer/Kconfiglib/blob/master/kconfiglib.py)

![image-20221021174305501](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221021174305501.png)

[kconfig 实例1: 基于 python 的 kconfig 系统 - 简书 (jianshu.com)](https://www.jianshu.com/p/25237ab0bf66)这个里面提供了一个简单的实现版本，但是有点太简单了，不符合我们实际项目的需要。

![image-20221021173111119](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221021173111119.png)

这里还是推荐用zephyr项目的版本：[zephyr/kconfig.py at main · zephyrproject-rtos/zephyr (github.com)](https://github.com/zephyrproject-rtos/zephyr/blob/main/scripts/kconfig/kconfig.py)。这个使用需要输入如下参数：

- kconfig_file，顶层的Kconfig配置文件路径
- config_out，输出.config文件路径
- header_out，输出c头文件路径
- kconfig_list_out，日志文件
- configs_in，1个或多个输入.config文件

![image-20221021173232502](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221021173232502.png)



### GCC安装

这里调试用的是windows环境，直接自行下载msys2+mingw即可。

https://blog.csdn.net/qq_31985307/article/details/114235846







## Kconfig基本概念&语法

### Kconfig简介

`Kconfig`语言定义了一套完整的规则来表述配置项及配置项间的关系。

之前安装的`Kconfiglib`只是用来显示Kconfig的，实际工程中通常会包含`Kconfig`和`.config`文件。

- **Kconfig**，是配置项的描述文件，支持设置配置项及其默认值，依赖关系等等，该文件还会继续依赖各个模块的**Kconfig**文件。
- **.config**，产品配置文件，提供配置项及在产品中这些配置项的设置值，可能和**Kconfig**配置项的默认取值不一致，属于产品对配置项的定制。这些配置文件在可以在**makefile**文件中使用。
- **autoconfig.h**，生成的C语言头文件，提供配置项的宏定义版，在C语言程序中使用。

### Kconfig语法

由于本文重点是讲Kconfig环境的搭建，所以语法就不展开。

linux的原版可以看这个：[Kconfig Language — The Linux Kernel documentation](https://www.kernel.org/doc/html/latest/kbuild/kconfig-language.html#introduction)

zephyr项目的介绍：[Configuration System (Kconfig) — Zephyr Project Documentation](https://docs.zephyrproject.org/latest/build/kconfig/index.html)

中文的一些说明：

[Kconfig 语法 - fluidog - 博客园 (cnblogs.com)](https://www.cnblogs.com/fluidog/p/15176680.html)

[kconfig语法整理 - 简书 (jianshu.com)](https://www.jianshu.com/p/aba588d380c2)



## Kconfig实战

这里围绕实际使用的几个场景来进行说明

### 直接配置版本

#### 准备

需要提供main.c，Makefile，Kconfig。下面分别进行描述：

![image-20221021175825950](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221021175825950.png)

##### Kconfig

这里我们将最开始背景说明中的宏定义配置改成Kconfig写法。

```python
mainmenu "Kconfig Demo"

menu "Test Params setting"
config TEST_ENABLE
    bool "Enable test work"
    default n
    help
        Will print debug information if enable.

config TEST_SHOW_STRING
    string "The show string info"
    default "Test 123"

config TEST_SHOW_INT
    int "The show int info"
	range 0 255
    default 123


config TEST_TOP_ENABLE
	bool "Test Top Func"
    default n
    help
        Function Test Top

config TEST_SUB_0_ENABLE
	bool "Test Sub 0 Func"
    default n
    help
        Function Test Sub 0

config TEST_SUB_1_ENABLE
	bool "Test Sub 1 Func"
    default n
    depends on TEST_TOP_ENABLE
    help
        Function Test Sub 1

config TEST_SHOW_SUB_INT
    int
    default 456 if TEST_SUB_0_ENABLE && TEST_SUB_1_ENABLE
    default 123


endmenu
```



##### Makefile

相比于传统的makefile，加入了`autoconfig.h`、`.config`和`menuconfig`编译目标。

**menuconfig**，用于显示menuconfig页面，让用户通过GUI选择当前配置参数。

**.config**，如果用户第一次没有`.config`文件时，调用`menuconfig`来配置`Kconfig`并生成`.config`。

**autoconfig.h**，如果`.config`有更新就需要执行，实际是调用`kconfig.py`脚本来生成`autoconfig.h`头文件。

```makefile
all: main.o
	gcc main.o -o main
main.o: main.c autoconfig.h
	gcc main.c -c -o main.o
clean:
	del main.o main.exe

autoconfig.h:.config
	python ../scripts/kconfig.py Kconfig .config autoconfig.h log.txt .config
.config:
	menuconfig
menuconfig:
	menuconfig
```



##### main.c

比较简单，一个是引用生成的autoconfig.h头文件，然后再根据不同的配置打印当前的信息

```c
#include <stdio.h>
#include "autoconfig.h"
int main()
{
    printf("hello, world\n");
#ifdef CONFIG_TEST_ENABLE
    printf("CONFIG_TEST_ENABLE\n");
#endif
	printf("CONFIG_TEST_SHOW_STRING: %s\n", CONFIG_TEST_SHOW_STRING);
	printf("CONFIG_TEST_SHOW_INT: %d\n", CONFIG_TEST_SHOW_INT);
#ifdef CONFIG_TEST_TOP_ENABLE
    printf("CONFIG_TEST_TOP_ENABLE\n");
#endif
#ifdef CONFIG_TEST_SUB_0_ENABLE
    printf("CONFIG_TEST_SUB_0_ENABLE\n");
#endif
#ifdef CONFIG_TEST_SUB_1_ENABLE
    printf("CONFIG_TEST_SUB_1_ENABLE\n");
#endif
	printf("CONFIG_TEST_SHOW_SUB_INT: %d\n", CONFIG_TEST_SHOW_SUB_INT);
    return 0;
}
```



#### 首次编译

直接键入`make all`，由于初始环境没有.config文件，会调用menuconfig进行配置生成.config文件。

如下图配置完成后输入**Q**，会提示保存`.config`文件，直接保存即可。

![image-20221021171934216](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221021171934216.png)



有`.config`文件后，就会执行**python**脚本生成`autoconfig.h`文件，最后调用`gcc`生成`main.exe`。

![image-20221021180323871](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221021180323871.png)



执行编译之后，生成的`autoconfig.h`文件信息如下。如上图所示，`main.exe`的执行结果和锁配置的`autoconfig.h`参数相同。

```c
#define CONFIG_TEST_ENABLE 1
#define CONFIG_TEST_SHOW_STRING "Test 567"
#define CONFIG_TEST_SHOW_INT 123
#define CONFIG_TEST_TOP_ENABLE 1
#define CONFIG_TEST_SHOW_SUB_INT 123
```



生成的`.config`文件如下，可以看到默认值通过`#`注释了，其他就是我们在`menuconfig`所指定的值。

```python

#
# Test Params setting
#
CONFIG_TEST_ENABLE=y
CONFIG_TEST_SHOW_STRING="Test 567"
CONFIG_TEST_SHOW_INT=123
CONFIG_TEST_TOP_ENABLE=y
# CONFIG_TEST_SUB_0_ENABLE is not set
# CONFIG_TEST_SUB_1_ENABLE is not set
CONFIG_TEST_SHOW_SUB_INT=123
# end of Test Params setting

```



如上图所示的执行完程序之后，生成了很多中间文件，和目标文件。真正有用的是`.config`和`autoconfig.h`文件。

![image-20221021200109412](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221021200109412.png)



#### 调整参数

第一次编译完毕以后，之后我们想修改参数可以通过输入`make menuconfig`进配置页面，**需要注意的是，这时候打开时，不再是默认值，而是我们之前调整后的值**。

按照如下配置后。

![image-20221021201439203](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221021201439203.png)



修改后，再键入`make all`，由于`autoconfig.h`所依赖的`.config`变化了，会触发再次运行**python**脚本生成`autoconfig.h`，再生成`main.exe`。

![image-20221021202232194](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221021202232194.png)



生成的`autoconfig.h`文件如下所示，从上图的执行结果可以看出行为一致。

```c
#define CONFIG_TEST_ENABLE 1
#define CONFIG_TEST_SHOW_STRING "Test 567"
#define CONFIG_TEST_SHOW_INT 78
#define CONFIG_TEST_TOP_ENABLE 1
#define CONFIG_TEST_SUB_0_ENABLE 1
#define CONFIG_TEST_SUB_1_ENABLE 1
#define CONFIG_TEST_SHOW_SUB_INT 456
```

生成的`.config`文件如下所示，和我们GUI配置的参数一致。

```python

#
# Test Params setting
#
CONFIG_TEST_ENABLE=y
CONFIG_TEST_SHOW_STRING="Test 567"
CONFIG_TEST_SHOW_INT=78
CONFIG_TEST_TOP_ENABLE=y
CONFIG_TEST_SUB_0_ENABLE=y
CONFIG_TEST_SUB_1_ENABLE=y
CONFIG_TEST_SHOW_SUB_INT=456
# end of Test Params setting
```



#### 总结

上述的方案算是一个最常用的方式了，发布的时候只提供`Kconfig`，`.config`为默认值生成的，用户需要改的时候自己通过`make menuconfig`来修改，以便生成不同的应用程序。

这个方式已经可以满足绝大数应用场景的需要了。





### Zephyr提出的持久化版本/多应用版本

虽然上述版本已经满足大多数场景需要了，但是对于像Zephyr这种项目，项目非常大，有多个驱动，并且其会提供很多例程，这些例程都是预先配置好参数给客户直接编译下载的。

不同例程之间所使用的参数各不相同，而且还想让客户可以通过GUI调整某个例程的参数信息，这时候如何管理呢。

这对应芯片厂来讲是一个很普遍的需求，芯片厂所提供的SDK一般包含多个例程，不同例程公用驱动库，只是所使用参数不同。

Zephyr原文：[Configuration System (Kconfig) — Zephyr Project Documentation](https://docs.zephyrproject.org/latest/build/kconfig/index.html)

Zephyr持久化方案实现代码：[zephyr/kconfig.cmake at main · zephyrproject-rtos/zephyr (github.com)](https://github.com/zephyrproject-rtos/zephyr/blob/main/cmake/modules/kconfig.cmake)

![image-20221022173355536](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221022173355536.png)

好的Zephyr Kconfig使用思路文档：

- [Zephyr Devicetree 与 Kconfig 配置指南 — PAN1080 DK Documentation (panchip.com)](https://docs.panchip.com/pan1080dk-doc/0.5.0/04_dev_guides/zephyr_configuration_guidance.html#)
- [Zephyr-系统配置(Kconfig)_只想.静静的博客-CSDN博客_zephyr如何配置](https://blog.csdn.net/u011638175/article/details/121339581)

Zephyr项目有点大，他的一些理念可以学习，但本文会给大家准备一个精简版的例程，借鉴其思路来实现类似其工作效果（学习zephyr可以参考下）。



#### 准备

假定有2个例程，每个例程有一个main函数，共同使用一个模块Test。Makefile通过APP参数来指定不同的编译目标，每个应用有其配置参数。项目的目录结构如下图所示。

- **app**，应用路径，下面包含2个例程，分别为test1和test2。每个应用有其独立的配置参数prj.conf。

- **driver**，公用的驱动路径，例程会调用这个驱动。

- **output**，输出路径，生成的一些文件都放在这，.o为了省事就不放了。
- **Kconfig**，kconfig的配置文件，和上一个一样。
- **Makefile**，makefile文件。

![image-20221022153835669](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221022153835669.png)



#### 代码分析-app

##### test1

main.c文件比较简单，就是打印一个printf，而后就是调用驱动库的函数。

```c
#include <stdio.h>
#include "driver_test.h"
int main()
{
    printf("hello, test1\n");
	test_driver();
    return 0;
}
```

prj.conf文件设定了针对test1的配置参数

```python
CONFIG_TEST_ENABLE=y
CONFIG_TEST_SHOW_STRING="Test 444"
```



##### test2

`main.c`文件比较简单，就是打印一个printf（**注意**：输出是`hello, test2`），而后就是调用驱动库的函数。

```c
#include <stdio.h>
#include "driver_test.h"
int main()
{
    printf("hello, test2\n");
	test_driver();
    return 0;
}
```

`prj.conf`文件设定了针对test2的配置参数

```python
CONFIG_TEST_TOP_ENABLE=y
CONFIG_TEST_SUB_0_ENABLE=y
CONFIG_TEST_SUB_1_ENABLE=n
```



#### 代码分析-driver

##### driver_test.c

其实和上一个例程差不多，就是将配置参数打印出来。

```c
#include <stdio.h>
#include "autoconfig.h"
void test_driver()
{
#ifdef CONFIG_TEST_ENABLE
    printf("CONFIG_TEST_ENABLE\n");
#endif
	printf("CONFIG_TEST_SHOW_STRING: %s\n", CONFIG_TEST_SHOW_STRING);
	printf("CONFIG_TEST_SHOW_INT: %d\n", CONFIG_TEST_SHOW_INT);
#ifdef CONFIG_TEST_TOP_ENABLE
    printf("CONFIG_TEST_TOP_ENABLE\n");
#endif
#ifdef CONFIG_TEST_SUB_0_ENABLE
    printf("CONFIG_TEST_SUB_0_ENABLE\n");
#endif
#ifdef CONFIG_TEST_SUB_1_ENABLE
    printf("CONFIG_TEST_SUB_1_ENABLE\n");
#endif
	printf("CONFIG_TEST_SHOW_SUB_INT: %d\n", CONFIG_TEST_SHOW_SUB_INT);
}
```

##### driver_test.h

没什么东西，就是一个函数声明罢了。

```c
#ifndef _DRIVER_TEST_H_
#define _DRIVER_TEST_H_
void test_driver(void);
#endif //_DRIVER_TEST_H_
```



#### 代码分析-Kconfig

和之前一模一样，就不重复占页数了。



#### 代码分析-Makefile

整个文件如下所示，相比上一个东西多了不少，需要大家具备一定的makefile的功底，下面简单进行分析。

```makefile
APP ?= app/test1
OUTPUT_PATH := output

INCLUDE_PATH := -I$(APP) -Idriver -I$(OUTPUT_PATH)

# define user .config setting
USER_CONFIG_SET := 
USER_CONFIG_SET += $(APP)/prj.conf

# define menuconfig .config path
DOTCONFIG_PATH := $(OUTPUT_PATH)/.config

# define user merged path
USER_RECORD_CONFIG_PATH := $(OUTPUT_PATH)/user_record.conf

# define autoconfig.h path
AUTOCONFIG_H := $(OUTPUT_PATH)/autoconfig.h

#define Kconfig path
KCONFIG_ROOT_PATH := Kconfig


#For windows work.
FIXPATH = $(subst /,\,$1)


all: $(APP)/main.o driver/driver_test.o
	gcc $^ -o $(OUTPUT_PATH)/main.exe
$(APP)/main.o: $(APP)/main.c
	gcc $< $(INCLUDE_PATH) -c -o $@
driver/driver_test.o: driver/driver_test.c $(AUTOCONFIG_H)
	gcc $< $(INCLUDE_PATH) -c -o $@

clean:
	del /q /s $(call FIXPATH, $(APP)/main.o driver/driver_test.o $(OUTPUT_PATH))

$(AUTOCONFIG_H):$(DOTCONFIG_PATH)
	python ../scripts/kconfig.py $(KCONFIG_ROOT_PATH) $(DOTCONFIG_PATH) $(AUTOCONFIG_H) $(OUTPUT_PATH)/log.txt $(DOTCONFIG_PATH)

$(USER_RECORD_CONFIG_PATH): $(USER_CONFIG_SET)
	@echo Using user config.
#	create user_record.conf to record current setting.
	@copy $(call FIXPATH, $^) $(call FIXPATH, $@)
#	create .config by user config setting.
	python ../scripts/kconfig.py --handwritten-input-configs $(KCONFIG_ROOT_PATH) $(DOTCONFIG_PATH) $(AUTOCONFIG_H) $(OUTPUT_PATH)/log.txt $(USER_CONFIG_SET)

export KCONFIG_CONFIG=$(DOTCONFIG_PATH)
$(DOTCONFIG_PATH):$(USER_RECORD_CONFIG_PATH)
	@echo .config updated

menuconfig:$(DOTCONFIG_PATH)
#	set KCONFIG_CONFIG=$(DOTCONFIG_PATH)
	menuconfig $(KCONFIG_ROOT_PATH)
```



##### 编译应用部分

将生成`autoconfig.h`的部分给删除掉，可以看到还是比较清晰的。由于**APP**可能不一样，默认选中`app/test1`，后续可以调用make的时候调整。

- **all**，依赖2个.o文件，最终生成`main.exe`。
- **main.o**，依赖`main.c`，最终生成`main.o`。
- **driver_test.o**，依赖`driver_test.c`和**`autoconfig.h`**，最终生成`driver_test.o`。
- **clean**，删除中间文件

```makefile
APP ?= app/test1
OUTPUT_PATH := output

INCLUDE_PATH := -I$(APP) -Idriver -I$(OUTPUT_PATH)

# define autoconfig.h path
AUTOCONFIG_H := $(OUTPUT_PATH)/autoconfig.h

#For windows work.
FIXPATH = $(subst /,\,$1)

all: $(APP)/main.o driver/driver_test.o
	gcc $^ -o $(OUTPUT_PATH)/main.exe
$(APP)/main.o: $(APP)/main.c
	gcc $< $(INCLUDE_PATH) -c -o $@
driver/driver_test.o: driver/driver_test.c $(AUTOCONFIG_H)
	gcc $< $(INCLUDE_PATH) -c -o $@

clean:
	del /q /s $(call FIXPATH, $(APP)/main.o driver/driver_test.o $(OUTPUT_PATH))

```



##### autoconfig.h部分

生成`autoconfig.h`相关的代码也不少，先对基本的参数做一些说明。

**USER_CONFIG_SET**，用户定义的初始化`prj.conf`，不同例程配置的参数各不相同，当然也可以分成多个文件，这里只使用一个。

**DOTCONFIG_PATH**，配置用户`menuconfig`和`kconfig.py`来使用的文件，`.h`文件的生成都是用这个文件进行的。

**USER_RECORD_CONFIG_PATH**，记录用户定义的config参数，本质就是为了利用`makefile`的文件依赖关系，来记录`USER_CONFIG_SET`有没有改变，如果有改变，就记录改变后的文件，并基于这些配置生成新的`.config`文件。

**AUTOCONFIG_H**，最终要生成的`autoconfig.h`文件路径。

**KCONFIG_ROOT_PATH**，`Kconfig`的路径。

**FIXPATH**，windows的**反斜杠**相关问题处理。

**$(AUTOCONFIG_H):$(DOTCONFIG_PATH)**，要生成`autoconfig.h`，就会去看`.config`目标是否存在或更新，最终调用`kconfig.py`使用`.config`来生成`autoconfig.h`。

**$(USER_RECORD_CONFIG_PATH): $(USER_CONFIG_SET)**，利用`makefile`的规则来记录用户配置的config文件是否有更新，如果有更新会利用windows的**copy**指令记录当前用户的config配置，并调用`kconfig.py`，将用户的config组合生成最终用于生成`autoconfig.h`的`.config`。**--handwritten-input-configs**是`zephyr`项目`kconfig.py`的配置参数，一些检查**overwrite**相关的处理。

**export KCONFIG_CONFIG=$(DOTCONFIG_PATH)**，`menuconfig`所需的参数，如果要修改`.config`的路径，必须配置该环境变量。

**$(DOTCONFIG_PATH):$(USER_RECORD_CONFIG_PATH)**，主要就是为了看用户config是否有修改，如果有就重新生成`.config`。当然如果刚使用时，没有默认的`.config`，就用用户config来生成`.config`。

**menuconfig:$(DOTCONFIG_PATH)**，调用`menuconfig`来临时配置参数。之前没写这个依赖，是因为所有的配置都是用`menuconfig`生成和管理的。而在这里所有的配置参数需要围绕于用户配置参数来进行，所以第一次打开没有`.config`时需要用用户当前配置作为`menuconfig`的显示参数，要临时修改也要基于当前应用配置来调整。

```makefile
OUTPUT_PATH := output

# define user .config setting
USER_CONFIG_SET := 
USER_CONFIG_SET += $(APP)/prj.conf

# define menuconfig .config path
DOTCONFIG_PATH := $(OUTPUT_PATH)/.config

# define user merged path
USER_RECORD_CONFIG_PATH := $(OUTPUT_PATH)/user_record.conf

# define autoconfig.h path
AUTOCONFIG_H := $(OUTPUT_PATH)/autoconfig.h

#define Kconfig path
KCONFIG_ROOT_PATH := Kconfig

#For windows work.
FIXPATH = $(subst /,\,$1)

$(AUTOCONFIG_H):$(DOTCONFIG_PATH)
	python ../scripts/kconfig.py $(KCONFIG_ROOT_PATH) $(DOTCONFIG_PATH) $(AUTOCONFIG_H) $(OUTPUT_PATH)/log.txt $(DOTCONFIG_PATH)

$(USER_RECORD_CONFIG_PATH): $(USER_CONFIG_SET)
	@echo Using user config.
#	create user_record.conf to record current setting.
	@copy $(call FIXPATH, $^) $(call FIXPATH, $@)
#	create .config by user config setting.
	python ../scripts/kconfig.py --handwritten-input-configs $(KCONFIG_ROOT_PATH) $(DOTCONFIG_PATH) $(AUTOCONFIG_H) $(OUTPUT_PATH)/log.txt $(USER_CONFIG_SET)

export KCONFIG_CONFIG=$(DOTCONFIG_PATH)
$(DOTCONFIG_PATH):$(USER_RECORD_CONFIG_PATH)
	@echo .config updated

menuconfig:$(DOTCONFIG_PATH)
#	set KCONFIG_CONFIG=$(DOTCONFIG_PATH)
	menuconfig $(KCONFIG_ROOT_PATH)
```



#### autoconfig.h生成分析

上面讲了一堆的参数，相信大家有点晕了，那回到我们的主题，设计这个复杂的`makefile`最终的目的的参考`zephyr`的持久化版本以及解决多应用版本的需要。

- 一方面，我们希望多个例程之间有不同的配置参数，是在`Kconfig`的初始值基础上的不同配置。
- 另一方面，我们希望用户可以直接通过`menuconfig`看当前的应用最终的配置参数，并且可以通过`menuconfig`来基于当前应用配置参数进行调整。

为了解决上述功能需要才设计了上述那么复杂的东西。

简单来讲，`autoconfig.h`总的有两个修改路径。

- 一个是直接修改用户config文件，这个是**持久化修改方案**，此时再编译会冲刷掉`menuconfig`修改的值。
- 一个是通过`menuconfig`修改`.config`文件，这个是**临时修改方案**，只对当前编译结果有效，会被用户配置给冲刷掉。

| 目标文件     | 依赖               | 备注                                                         |
| ------------ | ------------------ | ------------------------------------------------------------ |
| autoconfig.h | $(APP)/prj.conf    | 先生成merge.conf，而后用kconfig.py生成.config，最后再使用kconfig.py利用生成的.config生成autoconfig.h |
| autoconfig.h | menuconfig直接修改 | 1. 没有.config，先用prj.conf输入kconfig.py生成.config；2. GUI呈现.config的信息，调整后更新.config；3. 使用kconfig.py利用生成的.config生成autoconfig.h |



#### 编译

##### 首次编译

直接`make all`。默认选中的是test1例程，编译过程如下。

由于刚开始没有`.config`文件，会使用`prj.conf`文件生成`.config`文件，而后再用生成`.config`文件来生成`autoconfig.h`（**注意**，从图中可以看到，之前就已经生成好了autoconfig.h，后面并没有改变。这里是因为笔者暂时没办法将第一步只做merge动作并生成.config文件，所以只能这样了）。

![image-20221022170159780](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221022170159780.png)

执行结果如下，会产生一些中间文件，直接使用的是test1的配置。

![image-20221022170852961](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221022170852961.png)

![image-20221022171040160](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221022171040160.png)



##### 通过menuconfig修改参数

直接`make menuconfig`。显示的配置参数就是默认test1的当前配置。

![image-20221022171315724](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221022171315724.png)

尝试调整值如下，输入**Q**，会提示保存.config，保存即可。

![image-20221022171347634](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221022171347634.png)

这时候编译结果如下，可以看出和我们GUI配置的参数一致。

![image-20221022171716523](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221022171716523.png)



##### 修改user.prj的参数

直接文本操作，将test1目录下的prj.conf进行修改，修改后再通过`make all`编译，过程如下图。

可以看出刚刚通过menuconfig配置的.config被覆盖了，使用的是最新的用户配置参数，结果如下所示。

![image-20221022172313117](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221022172313117.png)



#### 不同应用编译

test1的编译结果如上，clean完工程后，我们输入`make all APP=app\test2`。得到的结果如下：

可以看出这时候用的是test2的配置参数，执行结果也符合预期。

![image-20221022172640410](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221022172640410.png)



#### 生成持久化所需的prj.conf

从上面的分析可以看出，之后发布给客户的时候不同应用就有其独特的配置了。

但是问题来了，要如何生成`prj.conf`文件呢，`menuconfig`提供了一个保存差异的功能，进入GUI修改完参数后，可以输入**D**就可以输出差异配置了，这个差异配置放到`prj.conf`中即可。

**注意**：这里生成的是相对于`Kconfig`的差异文件，并不是基于当前配置的差异。

![image-20221022173021662](https://img-blog.csdnimg.cn/img_convert/b5feb8a856375104c3726cca9bf68523.png)























