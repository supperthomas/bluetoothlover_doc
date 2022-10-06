# 使用Eclipse CDT build tools之后导致makefile环境错乱的问题

本人是windows开发环境，最近在搭建Eclipse CDT环境编译RiscV环境，然后使用了Eclipse的build tools环境，奇怪的是本地有很多makefile环境的c代码，会编译异常。

为了专门做了一些实验进行测试。

本例程所有相关代码在GitHub上，请自行下载。[bobwenstudy/test_makefile_shell_env (github.com)](https://github.com/bobwenstudy/test_makefile_shell_env)



## 问题说明及验证

### 测试程序

为了说明发生什么，特意写了一个测试程序，以便对此问题进行分析。

`main.c`

```c
#include <stdio.h>
int main()
{
    printf("hello, world\n");
    return 0;
}
```



`Makefile`，通过`TEST_OS`来区分不同测试环境，第8行打印当前的`SHELL`和`ComSpec`配置。

通过修改`SHELL`配置，即可调整当前的执行环境。

```makefile
OUTPUT_DIR = output/obj
OBJECTS = $(OUTPUT_DIR)/main.o

MKD := mkdir
RM := del /q /s
FIXPATH = $(subst /,\,$1)

$(warning SHELL, $(SHELL), $(ComSpec))

ifeq ($(TEST_OS),1)
	MKD := mkdir -p
	RM := rm -rf
	FIXPATH = $1
endif

ifeq ($(TEST_OS),2)
	ifdef ComSpec
		WINCMD:=$(ComSpec)
	endif
	ifdef COMSPEC
		WINCMD:=$(COMSPEC)
	endif

	SHELL:=$(WINCMD)
	MKD := mkdir -p
	RM := rm -rf
	FIXPATH = $1
endif


ifeq ($(TEST_OS),3)
	ifdef ComSpec
		WINCMD:=$(ComSpec)
	endif
	ifdef COMSPEC
		WINCMD:=$(COMSPEC)
	endif

	SHELL:=$(WINCMD)
	MKD := mkdir
	RM := del /q /s
	FIXPATH = $(subst /,\,$1)
endif

ifeq ($(TEST_OS),4)
	ifdef ComSpec
		WINCMD:=$(ComSpec)
	endif
	ifdef COMSPEC
		WINCMD:=$(COMSPEC)
	endif

	SHELL:=$(WINCMD)
	MKD := "mkdir" -p
	RM := rm -rf
	FIXPATH = $1
endif

ifeq ($(TEST_OS),5)
	ifdef ComSpec
		WINCMD:=$(ComSpec)
	endif
	ifdef COMSPEC
		WINCMD:=$(COMSPEC)
	endif

	SHELL:=$(WINCMD)
	MKD := mkdir.exe -p
	RM := rm -rf
	FIXPATH = $1
endif

all: $(OBJECTS)
	gcc $^ -o $(OUTPUT_DIR)/main
$(OBJECTS): $(OUTPUT_DIR)/%.o: %.c
	$(MKD) $(call FIXPATH, $(@D))
	gcc -c -o $@ $<
clean:
	$(RM) $(call FIXPATH, $(OUTPUT_DIR))
```



### 干净环境下，使用cygwin编译

#### 环境说明

如下所示，环境只有一个mingw32的make环境。

![image-20221005110846841](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221005110846841.png)



#### 使用windows下的mkdir和del操作

创建目录：`MKD := mkdir`

删除目录：`RM := del /q /s`

调整路径：`FIXPATH = $(subst /,\,$1)`

进行`make all`和`make clean`操作，程序都按照预期进行。

![image-20221005111002220](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221005111002220.png)



#### 使用linux下的mkdir和rm操作

创建目录：`MKD := mkdir -p`

删除目录：`RM := rm -rf`

调整路径：`FIXPATH = $1`

进行`make TEST_OS=1 all`和`make TEST_OS=1 clean`操作，程序都执行失败。mkdir失败是因为路径分隔符不对。rm是没有这个执行文件。

![image-20221005111105536](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221005111105536.png)



#### 总结

这些行为都是符合我预期的，一般我会通过`OS`判断来区分当前的系统，而后选择不同的执行命令。

![image-20220927171410992](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220927171410992.png)





### 使用CDT工具链进行编译

#### 环境搭建

到CDT的官网[Eclipse Embedded CDT | Eclipse Embedded CDT (C/C++ Development Tools)™ (eclipse-embed-cdt.github.io)](https://eclipse-embed-cdt.github.io/)，可以看到其有推荐windows的build tool环境：[The xPack Windows Build Tools | The xPack Build Framework](https://xpack.github.io/windows-build-tools/)

直接下载就行，本地已经下载好了一份，放在路径下`build-tools`。

#### 环境说明

为了方便复现，执行setup.bat脚本来进行环境配置。成功配置后，where make可以看出环境是ok的。

![image-20221005111349315](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221005111349315.png)



#### 使用windows下的mkdir和del操作

创建目录：`MKD := mkdir`

删除目录：`RM := del /q /s`

调整路径：`FIXPATH = $(subst /,\,$1)`

进行`make all`和`make clean`操作，程序都报错了，可以看到这时make的`SHELL`已经指向了build-tools目录下的sh.exe，这时候程序已经工作在linux环境下了，不能再使用windows的mkdir/del行为了。

![image-20221005112420957](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221005112420957.png)



#### 使用linux下的mkdir和rm操作

创建目录：`MKD := mkdir -p`

删除目录：`RM := rm -rf`

调整路径：`FIXPATH = $1`

进行`make TEST_OS=1 all`和`make TEST_OS=1 clean`操作，程序都执行成功了。整个环境就是linux的环境了。

![image-20221005112638507](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221005112638507.png)





#### 使用linux下的mkdir和rm操作+SHELL指定为windows

创建目录：`MKD := mkdir -p`

删除目录：`RM := rm -rf`

调整路径：`FIXPATH = $1`

进行`make TEST_OS=2 all`和`make TEST_OS=2 clean`操作，`mkdir`执行失败了，**rm确没报错**。因为这时候`rm.exe`已经在`build-tools`有提供了，那为什么这时候没有使用`build-tools`目录下的`mkdir.exe`呢？

![image-20221005112759518](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221005112759518.png)





#### 使用windows下的mkdir和del操作+SHELL指定为windows

创建目录：`MKD := mkdir`

删除目录：`RM := del /q /s`

调整路径：`FIXPATH = $(subst /,\,$1)`

进行`make TEST_OS=3 all`和`make TEST_OS=3 clean`操作，这时候又都执行成功了。

![image-20221005113203635](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221005113203635.png)





#### 总结

从上面的测试程序可以看到一个情况，当使用CDT的`build-tools`时，程序make行为不确定了。测试程序中，我们是通过`setup.bat`来配置PATH参数，只影响当前编译环境，但是通常我们会直接配置系统的环境变量`PATH`。这时系统make环境可能就出现错乱了，本人就遇到了这个问题。





## 解决办法

在使用CDT工具链情况下，SHELL指定为windows时，由于这时候mkdir和windows环境的命令相同（[Windows 命令 | Microsoft Learn](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/windows-commands)），windows命令的优先级更高。

### 使用linux下的mkdir和rm操作+SHELL指定为windows+双引号

通过`双引号""`强制指定不使用Windows的命令，而是用build-tools中提供的mkdir.exe。由于rm没冲突，所以不需要加调整。

创建目录：`MKD := "mkdir" -p`

删除目录：`RM := rm -rf`

调整路径：`FIXPATH = $1`

进行`make TEST_OS=4 all`和`make TEST_OS=4 clean`操作，`mkdir`和`rm`都能正常执行了。

![image-20221006123002833](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221006123002833.png)



### 使用linux下的mkdir和rm操作+SHELL指定为windows+exe指定

通过`.exe`强制指定不使用Windows的命令，而是用build-tools中提供的mkdir.exe。由于rm没冲突，所以不需要加调整。

创建目录：`MKD := mkdir.exe -p`

删除目录：`RM := rm -rf`

调整路径：`FIXPATH = $1`

进行`make TEST_OS=5 all`和`make TEST_OS=5 clean`操作，`mkdir`和`rm`都能正常执行了。

![image-20221006123233670](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20221006123233670.png)



### 总结

本质CDT提供的是linux下的build环境，当将CDT的build-tools作为默认编译环境时，就会出现make操作执行时，认为是linux环境，当想进行mkdir操作是，会和windows命令冲突，这时候如果系统中还有别的工程时，就会有冲突了。

只要理解本质原因，就可以根据各种情况针对性处理了。







