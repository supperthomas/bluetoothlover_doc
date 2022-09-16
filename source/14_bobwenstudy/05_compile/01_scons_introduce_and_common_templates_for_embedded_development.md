# Scons环境搭建和编译原理概述及嵌入式开发常用模板

Scons是用python实现的一个类似makefile的软件构建工具。其官网是[SCons: A software construction tool - SCons](https://www.scons.org/)，其具有详细的文档来对其使用进行说明[SCons Documentation](https://scons.org/docversions.html)。

Scons是一个软件构建工具，除了能对c/c++/asm进行构建外，也能实现对java等语言进行构建。因为其是用python来实现的，所以其具备跨平台的特性。

本例程所有相关代码在GitHub上，请自行下载。[bobwenstudy/scons_demo (github.com)](https://github.com/bobwenstudy/scons_demo)

## 为什么用Scons

第一次接触Scons是在RTThread中，进一步了解它的特性，渐渐的就喜欢上了，平常自己写一些代码，用Scons可以方便不少。对于我个人来说，主要的好处有：

实际项目中编译工程时，除了要对代码进行编译生成固件外，还需要整合一些其他资源（如编译耳机项目时，需要讲提示音等wav资源打包进代码中；多固件合并打包之类。）之前完成这些动作是用python写的，当然能用makefile调用，但是相比Scons本身就是python，同一套环境调试起来会方便不少。

易读性，相比于makefile这么久远的构建语言，Scons是python写的，其语法和调试起来更方便，函数调用和可读性都比makefile好。

文件依赖，使用makefile时，由于经常编译的时候只将c文件作为依赖，而没有将h文件作为依赖，或其他资源，导致部分h文件更新时，经常要考虑先make clean，再make all。而Scons可以自动将关联的文件作为依赖，并构建依赖树，不用考虑太多就可以自动将相关依赖关系给维护好，当文件更新再次编译时，只编译特定文件。同时可以通过**Depends**指定依赖关系。

缺点也有：

集成度太强：Scons内部做了太多事情，对于我这种掌控欲比较强的程序猿来说，有点脱离掌控了，虽然方便，但是当构建大型项目时，内部一些行为可能导致debug很长时间，需要我们对其原理进行深入分析。

资料较少：毕竟是新语言，现在很多新语言很快的死在沙滩上了，对于新语言，大家或多或少保持观望态度，所以目前资料还是比较少的。遇到bug得自己看官方手册，还是有点麻烦的。



## 环境搭建

从上面描述可知，Scons类似于makefile，但并不是替代了GCC，只是实现了对GCC的使用。按照makefile的逻辑，需要准备如下环境：

GCC环境：笔者是Windows环境，所以需要msys64+mingw工具链。

Scons环境：python环境安装后，再安装scons就行。



### GCC环境

#### PC下的GCC环境安装

参考这个文章安装即可。[Win7下msys64安装mingw工具链 - Milton - 博客园 (cnblogs.com)](https://www.cnblogs.com/milton/p/11808091.html)

安装完以后，键入`gcc -v`，得到如下提示说明环境安装好了，目前笔者用的是mingw32的gcc。

![image-20220912103125415](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220912103125415.png)

#### ARM下的GCC环境安装

从各个芯片产商都可以获取到对应的交叉工具链，笔者的交叉工具链解压缩后，就有gcc环境，一般交叉工具链会有前缀。

安装完以后，键入`arm-none-eabi-gcc -v`，出现如下信息就代表安装成功了。

![image-20220912111316820](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220912111316820.png)







### Scons环境

#### Python安装

Scons是运行在python环境下的，目前新版本的都运行在Python3+的版本上，就不建议安装Python2的环境了（当然也可以用Python2就是了，不过最新的pip已经不支持Python2了，希望大家早点切换）。

网上有很多教程了，[Python安装教程-史上最全_壬杰的博客-CSDN博客_python安装](https://blog.csdn.net/weixin_49237144/article/details/122915089)可以参考这个，当然也可以直接到[Welcome to Python.org](https://www.python.org/)下载。

最终安装结束后，键入`python -V`，能看到python版本，代表环境安装好了。

![image-20220912103922628](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220912103922628.png)

#### Scons安装

使用`python -m pip install scons`即可。当然可以到官网看看[SCons Downloads](https://scons.org/pages/download.html)。

最终安装结束后，键入`scons -v`，能看到如下信息，代表环境安装好了。

![image-20220912104526394](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220912104526394.png)





## 初识Scons

### 基本概述

要讲清楚Scons，需要理解gcc是如何使用的，已经相比于make，scons的行为差异。首先对gcc、make和scons基本概念进行说明。

#### gcc

实际编译c文件的动作都是由gcc来完成的，scons/make等构建语言只是完成了对多个编译文件和编译目标的调度管理，本身不完成编译文件的动作。

**c编译原理**的概念很多大佬已经讲得比较多了，可以参考：[C编译原理_daixiao3636的博客-CSDN博客_c编译原理](https://blog.csdn.net/daixiao3636/article/details/106913843)。当然现在要编译文件也很简单了，一般我们只用2步，一个是通过`gcc -c -o`生成object文件，然后再将object文件`gcc -o`生成目标文件。

#### make

使用的换需要安装make环境，一般安装好mingw的时候，就自动装好了make+gcc环境，需要注意的是，新版装好后没有make.exe，而是：**mingw32-make.exe**，可以复制一份，并修改文件名为**make.exe**，以方便后面使用。

![image-20220912110738208](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220912110738208.png)



make使用可以直接在终端上使用，键入`make -v`，看到如下信息，说明**make**环境安装成功了。

![image-20220912110902820](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220912110902820.png)

执行make，会去寻找文件：GNUmakefile、makefile 和 Makefile。详细可以见：[认识Makefile文件_天糊土的博客-CSDN博客_makefile文件在哪](https://blog.csdn.net/oqqHuTu12345678/article/details/125634958)

![image-20220913100427048](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220913100427048.png)

#### Scons

之前已经安装好了scons环境，要使用scons，和make类似，也需要一个脚本文件，配置要执行的操作。文件名为：**SConstruct**。

![image-20220913100518586](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220913100518586.png)



### 单文件构建

#### gcc编译

单个文件编译，gcc直接命令行操作就行，两行命令就可以搞定（当然1条命令也可以，这里为了统一，都要求先生成object文件，再生成目标文件）。

![image-20220913101553879](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220913101553879.png)

main.c的源码如下：

```c
#include <stdio.h>
int main()
{
    printf("hello, world\n");
    return 0;
}
```

#### make编译

如图所示，第一次编译的时候，编译目标`all`依赖`main.o`，由于没有`main.o`，先对`main.c`进行编译，生成`main.o`，最后生成最终目标。第二次编译时，由于`main.c`没改变，自然`main.o`不需要改变，所以只需要执行`all`所对应的指令，生成目标`main`。

`clean`清除完环境后，再次`make all`，所有的操作都重新来过。

![image-20220913102014649](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220913102014649.png)

Makefile的源码如下：

```makefile
all: main.o
	gcc main.o -o main
main.o: main.c
	gcc main.c -c -o main.o
clean:
	rm main.o main.exe
```

#### Scons编译

如下图所示是一个简易的scons编译行为，可以看到，脚本写的时候只需配置好源文件和目标文件`source=main.c target=main`，直接执行scons就可以，第二次编译的时候，由于什么都没变化scons不执行任何操作。

相比于make，清空环境只需要执行`scons -c`就可以自动清除编译生成的文件，无需像make要指定所有目标。而后再次编译又会重新开始了。

![image-20220913103139409](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220913103139409.png)

scons源码如下：

```python
obj = Object('main.c')
Program('main', obj)
```

#### 总结

gcc直接操作，每次编译都需要输入所有command，不能自动识别文件哪些有改动，只编译所需的文件，对于大型工程来说，编译时间还是很长的，只编译有修改的文件还是很方便的。

make解决了gcc的缺点，每次编译只需要执行`make all`，删除执行`make clean`就可以，但是写`makefile`的人需要知晓所有的中间文件，并了解文件的依赖关系。

scons保留了make的优点，每次编译只需要执行`scons`，删除执行`scons -c`就可以。同时写`Sconstruct`也更为轻松，不需要了解中间文件是什么，也不用专门写一个clean操作。所有的事情交给scons就行。



### 带.h文件的构建

#### gcc编译

多个文件编译的时候，先将2个文件生成object文件，再将2个object文件编译成目标main.exe。

![image-20220913105136107](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220913105136107.png)

main.c的源码如下：

```c
#include <stdio.h>
#include "test.h"
int main()
{
    printf("hello, world\n");
	test_work();
    return 0;
}
```

test.c的源码如下：

```c
#include <stdio.h>
#include "test.h"
void test_work(void)
{
    printf(TEST_PRINT_STRING);
}
```

test.h的源码如下：

```c
#ifndef _TEST_H_
#define _TEST_H_

#define TEST_PRINT_STRING "Test_Origin_0"
void test_work(void);

#endif //_TEST_H_
```



#### make编译

按照流程写好，这里需要注意的是，修改完`test.h`后，再次编译的时候`make`只再次生成了`main.exe`，并没有重新编译`test.o`和`main.o`，并没有达到我们的目标。

这是因为我们的`makefile`没写好，没把`test.h`依赖关系给写好。

![image-20220913105753757](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220913105753757.png)



将makefile修改一下，这时候再次修改`test.h`文件，`make`就知道需要重新编译文件了（大型项目通常通过`-MMD -MP`来生成`.h`的依赖树）。

注意，这个问题是我们写makefile经常遇到的问题，这个还存在更换之类的场景下，依赖关系没写好，导致再次编译的时候没将所有改动给编译进去，通常要先`make clean`再`make all`，完全丧失了make只编译改动的特点，导致编译效率大大降低。

![image-20220913111616496](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220913111616496.png)

Makefile的源码如下：

```makefile
all: main.o test.o
	gcc main.o test.o -o main
main.o: main.c test.h
	gcc main.c -c -o main.o
test.o: test.c test.h
	gcc test.c -c -o test.o
clean:
	rm main.o test.o main.exe
```

#### Scons编译

scons的脚本依然很简单，配置好objects所需的源文件，在配置好目标，执行scons就可以了。需要注意的是，我们并没有显示的声明test.h的依赖关系，当修改test.h后再次编译，scons就能知道文件间的依赖关系，将整个工程正确的重新编译了，这对于写Sconstruct的人要求大大降低。

![image-20220913112536319](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220913112536319.png)

SConstruct源码如下：

```python
objs = Object('main.c')
objs += Object('test.c')
Program('main', objs)
```

#### 总结

在包含.h文件等多种隐示依赖的情况下，scons无需开发人员了解编译的底层原理，只需要将所需编译的主文件配置好，并配置好目标，剩下scons都可以自动搞定，大大节约了工程人员的开发和维护成本。





## Scons原理分析

从上一章的分析可以看出，`scons`保留了make的所有优点，并简化了脚本编译，同时很好的维护了各个文件的隐示依赖关系，避免大家每次都要`make clean`，再`make all`了。

这一章我们简单分析下Scons是如何工作的。

### 脚本如何运行

没时间细看代码，自己也写过一些测试环境之类，大体猜测Scons的运行机制就是将`Sconstruct`文件用`exec`函数来执行，这样才能只写部分代码就可以完成编译工作。

简单搜索了下源码`Sconstruct`，可以看到`_SConstruct_exists`函数会去用这个文件。

![image-20220913125729673](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220913125729673.png)

之后有用python的`exec`函数来执行这个文件。

![image-20220913130153687](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220913130153687.png)



### 如何指导编译

如果学习过`make`的语法，其核心语法就是`目标和依赖`，利用好其基本语法，再借助其强大的工具函数，就可以完成项目的编译管理工作。

scons和make一样，本质并不会去做gcc的工作，更多是管理工程文件如何依次调用gcc进行编译。

要用scons实现大型项目的管理，也必须理解其底层运行机制，这样才能实现各种复杂的行为。直接学习其源码是可以的，但是太累了，直接看其文档也能看到一些，但是也不是特别清楚，所以这里笔者以自己浅显的理解来分析其行为。

从上面的说明例子中，简单的c项目编译，只需要指定`Object`所需的source文件，然后再指定`Program`所需的objs和target对象，剩下都是scons来完成的。那么我们依次拆分其操作行为。

#### 打印环境信息env.Dump()

scons所有的配置参数和信息存储在`Environment`对象中，可以通过`Dump`方法可以打印当前scons的所有配置参数，而后用python的`print`方法就可以打印出来了。

官方手册上也有说明：

![image-20220914115119261](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220914115119261.png)

```python
env = Environment()
print(env.Dump())
```

打印出来的信息如下所示，参数有很多，看不懂咋办。

目前只需要完成嵌入式C开发需要，只要认下面几个关键字：

- C编译：`CC`和`CCCOM`

- ASM编译：`AS`和`ASCOM`

- 链接：`LINK`和`LINKCOM`

```json
scons: Reading SConscript files ...
{ 'AR': 'ar',
  'ARCOM': '$AR $ARFLAGS $TARGET $SOURCES',
  'ARFLAGS': ['rc'],
  'AS': 'as',
  'ASCOM': '$AS $ASFLAGS -o $TARGET $SOURCES',
  'ASFLAGS': [],
  'ASPPCOM': '$CC $ASPPFLAGS $CPPFLAGS $_CPPDEFFLAGS $_CPPINCFLAGS -c -o '
             '$TARGET $SOURCES',
  'ASPPFLAGS': '$ASFLAGS',
  'BUILDERS': { 'CopyAs': <SCons.Builder.BuilderBase object at 0x000001F3D9B0C7F0>,
                'CopyTo': <SCons.Builder.BuilderBase object at 0x000001F3D9B0C7C0>,
                'JarFile': <SCons.Builder.BuilderBase object at 0x000001F3D9B0C910>,
                'JavaClassDir': <SCons.Builder.BuilderBase object at 0x000001F3D9B0CC10>,
                'JavaClassFile': <SCons.Builder.BuilderBase object at 0x000001F3D9B0CB50>,
                'JavaFile': <SCons.Builder.CompositeBuilder object at 0x000001F3D9B0CA60>,
                'Library': <SCons.Builder.BuilderBase object at 0x000001F3D9ACAA10>,
                'LoadableModule': <SCons.Builder.BuilderBase object at 0x000001F3D9ACA680>,
                'M4': <SCons.Builder.BuilderBase object at 0x000001F3D9B0C4C0>,
                'Object': <SCons.Builder.CompositeBuilder object at 0x000001F3D9AC9360>,
                'Program': <SCons.Builder.BuilderBase object at 0x000001F3D9AC9900>,
                'ProgramAllAtOnce': <SCons.Builder.BuilderBase object at 0x000001F3D9B0C6D0>,
                'RES': <SCons.Builder.BuilderBase object at 0x000001F3D9A2ECB0>,
                'RMIC': <SCons.Builder.BuilderBase object at 0x000001F3D9A89930>,
                'SharedLibrary': <SCons.Builder.BuilderBase object at 0x000001F3D9ACA290>,
                'SharedObject': <SCons.Builder.CompositeBuilder object at 0x000001F3D9AC95A0>,
                'StaticLibrary': <SCons.Builder.BuilderBase object at 0x000001F3D9ACAA10>,
                'StaticObject': <SCons.Builder.CompositeBuilder object at 0x000001F3D9AC9360>,
                'Substfile': <SCons.Builder.BuilderBase object at 0x000001F3D9AC8FD0>,
                'Tar': <SCons.Builder.BuilderBase object at 0x000001F3D9A8AB60>,
                'Textfile': <SCons.Builder.BuilderBase object at 0x000001F3D9AC8F70>,
                'Zip': <SCons.Builder.BuilderBase object at 0x000001F3D9A8AEC0>},
  'CC': 'gcc',
  'CCCOM': '$CC -o $TARGET -c $CFLAGS $CCFLAGS $_CCCOMCOM $SOURCES',
  'CCDEPFLAGS': '-MMD -MF ${TARGET}.d',
  'CCFLAGS': [],
  'CCVERSION': '12.1.0',
  'CFILESUFFIX': '.c',
  'CFLAGS': [],
  'CONFIGUREDIR': '#/.sconf_temp',
  'CONFIGURELOG': '#/config.log',
  'COPYSTR': 'Copy file(s): "$SOURCES" to "$TARGETS"',
  'CPPDEFPREFIX': '-D',
  'CPPDEFSUFFIX': '',
  'CPPSUFFIXES': [ '.c',
                   '.C',
                   '.cxx',
                   '.cpp',
                   '.c++',
                   '.cc',
                   '.h',
                   '.H',
                   '.hxx',
                   '.hpp',
                   '.hh',
                   '.F',
                   '.fpp',
                   '.FPP',
                   '.m',
                   '.mm',
                   '.S',
                   '.spp',
                   '.SPP',
                   '.sx'],
  'CXX': 'g++',
  'CXXCOM': '$CXX -o $TARGET -c $CXXFLAGS $CCFLAGS $_CCCOMCOM $SOURCES',
  'CXXFILESUFFIX': '.cc',
  'CXXFLAGS': [],
  'CXXVERSION': '12.1.0',
  'DC': 'dmd',
  'DCOM': '$DC $_DINCFLAGS $_DVERFLAGS $_DDEBUGFLAGS $_DFLAGS -c -of$TARGET '
          '$SOURCES',
  'DDEBUG': [],
  'DDEBUGPREFIX': '-debug=',
  'DDEBUGSUFFIX': '',
  'DFILESUFFIX': '.d',
  'DFLAGPREFIX': '-',
  'DFLAGS': [],
  'DFLAGSUFFIX': '',
  'DINCPREFIX': '-I',
  'DINCSUFFIX': '',
  'DLIB': 'lib',
  'DLIBCOM': '$DLIB $_DLIBFLAGS -c $TARGET $SOURCES $_DLIBFLAGS',
  'DLIBDIRPREFIX': '-L-L',
  'DLIBDIRSUFFIX': '',
  'DLIBFLAGPREFIX': '-',
  'DLIBFLAGSUFFIX': '',
  'DLIBLINKPREFIX': '',
  'DLIBLINKSUFFIX': '.lib',
  'DLINK': '$DC',
  'DLINKCOM': '$DLINK -of$TARGET $DLINKFLAGS $__DRPATH $SOURCES $_DLIBDIRFLAGS '
              '$_DLIBFLAGS',
  'DLINKFLAGS': [],
  'DPATH': ['#/'],
  'DRPATHPREFIX': '-L-rpath=',
  'DRPATHSUFFIX': '',
  'DSUFFIXES': ['.d'],
  'DVERPREFIX': '-version=',
  'DVERSIONS': [],
  'DVERSUFFIX': '',
  'Dir': <SCons.Defaults.Variable_Method_Caller object at 0x000001F3D93C82E0>,
  'Dirs': <SCons.Defaults.Variable_Method_Caller object at 0x000001F3D93C8370>,
  'ENV': { 'COMSPEC': 'C:\\Windows\\system32\\cmd.exe',
           'PATH': 'C:\\Windows\\System32;C:\\msys64\\mingw32\\bin',
           'PATHEXT': '.COM;.EXE;.BAT;.CMD',
           'SystemDrive': 'C:',
           'SystemRoot': 'C:\\Windows',
           'TEMP': 'C:\\Users\\wenbo\\AppData\\Local\\Temp',
           'TMP': 'C:\\Users\\wenbo\\AppData\\Local\\Temp',
           'USERPROFILE': 'C:\\Users\\wenbo'},
  'ESCAPE': <function escape at 0x000001F3D9519B40>,
  'F03': 'gfortran',
  'F03COM': '$F03 -o $TARGET -c $FORTRANCOMMONFLAGS $F03FLAGS $_F03INCFLAGS '
            '$_FORTRANMODFLAG $SOURCES',
  'F03FLAGS': [],
  'F03PPCOM': '$F03 -o $TARGET -c $FORTRANCOMMONFLAGS $F03FLAGS $CPPFLAGS '
              '$_CPPDEFFLAGS $_F03INCFLAGS $_FORTRANMODFLAG $SOURCES',
  'F08': 'gfortran',
  'F08COM': '$F08 -o $TARGET -c $FORTRANCOMMONFLAGS $F08FLAGS $_F08INCFLAGS '
            '$_FORTRANMODFLAG $SOURCES',
  'F08FLAGS': [],
  'F08PPCOM': '$F08 -o $TARGET -c $FORTRANCOMMONFLAGS $F08FLAGS $CPPFLAGS '
              '$_CPPDEFFLAGS $_F08INCFLAGS $_FORTRANMODFLAG $SOURCES',
  'F77': 'gfortran',
  'F77COM': '$F77 -o $TARGET -c $FORTRANCOMMONFLAGS $F77FLAGS $_F77INCFLAGS '
            '$SOURCES',
  'F77FLAGS': [],
  'F77PPCOM': '$F77 -o $TARGET -c $FORTRANCOMMONFLAGS $F77FLAGS $CPPFLAGS '
              '$_CPPDEFFLAGS $_F77INCFLAGS $SOURCES',
  'F90': 'gfortran',
  'F90COM': '$F90 -o $TARGET -c $FORTRANCOMMONFLAGS $F90FLAGS $_F90INCFLAGS '
            '$_FORTRANMODFLAG $SOURCES',
  'F90FLAGS': [],
  'F90PPCOM': '$F90 -o $TARGET -c $FORTRANCOMMONFLAGS $F90FLAGS $CPPFLAGS '
              '$_CPPDEFFLAGS $_F90INCFLAGS $_FORTRANMODFLAG $SOURCES',
  'F95': 'gfortran',
  'F95COM': '$F95 -o $TARGET -c $FORTRANCOMMONFLAGS $F95FLAGS $_F95INCFLAGS '
            '$_FORTRANMODFLAG $SOURCES',
  'F95FLAGS': [],
  'F95PPCOM': '$F95 -o $TARGET -c $FORTRANCOMMONFLAGS $F95FLAGS $CPPFLAGS '
              '$_CPPDEFFLAGS $_F95INCFLAGS $_FORTRANMODFLAG $SOURCES',
  'FORTRAN': 'gfortran',
  'FORTRANCOM': '$FORTRAN -o $TARGET -c $FORTRANCOMMONFLAGS $FORTRANFLAGS '
                '$_FORTRANINCFLAGS $_FORTRANMODFLAG $SOURCES',
  'FORTRANFLAGS': [],
  'FORTRANMODDIR': '',
  'FORTRANMODDIRPREFIX': '-J',
  'FORTRANMODDIRSUFFIX': '',
  'FORTRANMODPREFIX': '',
  'FORTRANMODSUFFIX': '.mod',
  'FORTRANPPCOM': '$FORTRAN -o $TARGET -c $FORTRANCOMMONFLAGS $FORTRANFLAGS '
                  '$CPPFLAGS $_CPPDEFFLAGS $_FORTRANINCFLAGS $_FORTRANMODFLAG '
                  '$SOURCES',
  'FORTRANSUFFIXES': [ '.f',
                       '.for',
                       '.ftn',
                       '.F',
                       '.FOR',
                       '.FTN',
                       '.fpp',
                       '.FPP',
                       '.f77',
                       '.F77',
                       '.f90',
                       '.F90',
                       '.f95',
                       '.F95',
                       '.f03',
                       '.F03',
                       '.f08',
                       '.F08'],
  'FRAMEWORKPATH': [],
  'FRAMEWORKS': [],
  'File': <SCons.Defaults.Variable_Method_Caller object at 0x000001F3D93C83A0>,
  'HOST_ARCH': 'x86_64',
  'HOST_OS': 'win32',
  'IDLSUFFIXES': ['.idl', '.IDL'],
  'IMPLIBNOVERSIONSYMLINKS': True,
  'INCF03PREFIX': '-I',
  'INCF03SUFFIX': '',
  'INCF08PREFIX': '-I',
  'INCF08SUFFIX': '',
  'INCF77PREFIX': '-I',
  'INCF77SUFFIX': '',
  'INCF90PREFIX': '-I',
  'INCF90SUFFIX': '',
  'INCF95PREFIX': '-I',
  'INCF95SUFFIX': '',
  'INCFORTRANPREFIX': '-I',
  'INCFORTRANSUFFIX': '',
  'INCPREFIX': '-I',
  'INCSUFFIX': '',
  'JAR': 'jar',
  'JARCOM': "${TEMPFILE('$_JARCOM','$JARCOMSTR')}",
  'JARFLAGS': ['cf'],
  'JARSUFFIX': '.jar',
  'JAVABOOTCLASSPATH': [],
  'JAVAC': 'javac',
  'JAVACCOM': "${TEMPFILE('$_JAVACCOM','$JAVACCOMSTR')}",
  'JAVACFLAGS': [],
  'JAVACLASSPATH': [],
  'JAVACLASSSUFFIX': '.class',
  'JAVAINCLUDES': [],
  'JAVASOURCEPATH': [],
  'JAVASUFFIX': '.java',
  'LDMODULE': '$SHLINK',
  'LDMODULECOM': <SCons.Action.CommandGeneratorAction object at 0x000001F3D9A2E800>,
  'LDMODULEEMITTER': [ <function lib_emitter at 0x000001F3D93B4AF0>,
                       <function ldmod_symlink_emitter at 0x000001F3D9AE8940>,
                       <function shlib_emitter at 0x000001F3D9A5A290>],
  'LDMODULEFLAGS': '$SHLINKFLAGS',
  'LDMODULENAME': '${LDMODULEPREFIX}$_get_ldmodule_stem${_LDMODULESUFFIX}',
  'LDMODULENOVERSIONSYMLINKS': True,
  'LDMODULEPREFIX': '$SHLIBPREFIX',
  'LDMODULESUFFIX': '$SHLIBSUFFIX',
  'LDMODULEVERSION': '$SHLIBVERSION',
  'LDMODULE_NOVERSION_SYMLINK': '$_get_shlib_dir${LDMODULEPREFIX}$_get_ldmodule_stem${LDMODULESUFFIX}',
  'LDMODULE_SONAME_SYMLINK': '$_get_shlib_dir$_LDMODULESONAME',
  'LIBDIRPREFIX': '-L',
  'LIBDIRSUFFIX': '',
  'LIBLINKPREFIX': '-l',
  'LIBLINKSUFFIX': '',
  'LIBPREFIX': 'lib',
  'LIBPREFIXES': ['$LIBPREFIX'],
  'LIBSUFFIX': '.a',
  'LIBSUFFIXES': ['$LIBSUFFIX'],
  'LINESEPARATOR': '\n',
  'LINK': '$SMARTLINK',
  'LINKCOM': '$LINK -o $TARGET $LINKFLAGS $__RPATH $SOURCES $_LIBDIRFLAGS '
             '$_LIBFLAGS',
  'LINKFLAGS': [],
  'M4': 'm4',
  'M4COM': 'cd ${SOURCE.rsrcdir} && $M4 $M4FLAGS < ${SOURCE.file} > '
           '${TARGET.abspath}',
  'M4FLAGS': ['-E'],
  'MAXLINELENGTH': 2048,
  'NINJA_DEPFILE_PARSE_FORMAT': 'gcc',
  'OBJPREFIX': '',
  'OBJSUFFIX': '.o',
  'PLATFORM': 'win32',
  'PROGPREFIX': '',
  'PROGSUFFIX': '.exe',
  'PSPAWN': <function piped_spawn at 0x000001F3D9519990>,
  'RANLIB': 'ranlib',
  'RANLIBCOM': '$RANLIB $RANLIBFLAGS $TARGET',
  'RANLIBFLAGS': [],
  'RC': 'windres',
  'RCCOM': '$RC $_CPPDEFFLAGS $RCINCFLAGS ${RCINCPREFIX} ${SOURCE.dir} '
           '$RCFLAGS -i $SOURCE -o $TARGET',
  'RCFLAGS': [],
  'RCINCFLAGS': '${_concat(RCINCPREFIX, CPPPATH, RCINCSUFFIX, __env__, RDirs, '
                'TARGET, SOURCE, affect_signature=False)}',
  'RCINCPREFIX': '--include-dir ',
  'RCINCSUFFIX': '',
  'RDirs': <SCons.Defaults.Variable_Method_Caller object at 0x000001F3D93C8430>,
  'RMIC': 'rmic',
  'RMICCOM': '$RMIC $RMICFLAGS -d ${TARGET.attributes.java_lookupdir} '
             '-classpath ${SOURCE.attributes.java_classdir} '
             '${SOURCES.attributes.java_classname}',
  'RMICFLAGS': [],
  'RPATHPREFIX': '-Wl,-rpath=',
  'RPATHSUFFIX': '',
  'SCANNERS': [<SCons.Scanner.ScannerBase object at 0x000001F3D9393C10>],
  'SHCC': '$CC',
  'SHCCCOM': '$SHCC -o $TARGET -c $SHCFLAGS $SHCCFLAGS $_CCCOMCOM $SOURCES',
  'SHCCFLAGS': ['$CCFLAGS'],
  'SHCFLAGS': ['$CFLAGS'],
  'SHCXX': '$CXX',
  'SHCXXCOM': '$SHCXX -o $TARGET -c $SHCXXFLAGS $SHCCFLAGS $_CCCOMCOM $SOURCES',
  'SHCXXFLAGS': ['$CXXFLAGS'],
  'SHDC': '$DC',
  'SHDCOM': '$DC $_DINCFLAGS $_DVERFLAGS $_DDEBUGFLAGS $_DFLAGS -c -fPIC '
            '-of$TARGET $SOURCES',
  'SHDLINK': '$DC',
  'SHDLINKCOM': '$DLINK -of$TARGET $SHDLINKFLAGS $__SHDLIBVERSIONFLAGS '
                '$__DRPATH $SOURCES $_DLIBDIRFLAGS $_DLIBFLAGS',
  'SHDLINKFLAGS': ['$DLINKFLAGS', '-shared', '-defaultlib=libphobos2.so'],
  'SHELL': 'C:\\Windows\\System32\\cmd.exe',
  'SHF03': '$F03',
  'SHF03COM': '$SHF03 -o $TARGET -c $FORTRANCOMMONFLAGS $SHF03FLAGS '
              '$_F03INCFLAGS $_FORTRANMODFLAG $SOURCES',
  'SHF03FLAGS': ['$F03FLAGS'],
  'SHF03PPCOM': '$SHF03 -o $TARGET -c $FORTRANCOMMONFLAGS $SHF03FLAGS '
                '$CPPFLAGS $_CPPDEFFLAGS $_F03INCFLAGS $_FORTRANMODFLAG '
                '$SOURCES',
  'SHF08': '$F08',
  'SHF08COM': '$SHF08 -o $TARGET -c $FORTRANCOMMONFLAGS $SHF08FLAGS '
              '$_F08INCFLAGS $_FORTRANMODFLAG $SOURCES',
  'SHF08FLAGS': ['$F08FLAGS'],
  'SHF08PPCOM': '$SHF08 -o $TARGET -c $FORTRANCOMMONFLAGS $SHF08FLAGS '
                '$CPPFLAGS $_CPPDEFFLAGS $_F08INCFLAGS $_FORTRANMODFLAG '
                '$SOURCES',
  'SHF77': '$F77',
  'SHF77COM': '$SHF77 -o $TARGET -c $FORTRANCOMMONFLAGS $SHF77FLAGS '
              '$_F77INCFLAGS $SOURCES',
  'SHF77FLAGS': ['$F77FLAGS'],
  'SHF77PPCOM': '$SHF77 -o $TARGET -c $FORTRANCOMMONFLAGS $SHF77FLAGS '
                '$CPPFLAGS $_CPPDEFFLAGS $_F77INCFLAGS $SOURCES',
  'SHF90': '$F90',
  'SHF90COM': '$SHF90 -o $TARGET -c $FORTRANCOMMONFLAGS $SHF90FLAGS '
              '$_F90INCFLAGS $_FORTRANMODFLAG $SOURCES',
  'SHF90FLAGS': ['$F90FLAGS'],
  'SHF90PPCOM': '$SHF90 -o $TARGET -c $FORTRANCOMMONFLAGS $SHF90FLAGS '
                '$CPPFLAGS $_CPPDEFFLAGS $_F90INCFLAGS $_FORTRANMODFLAG '
                '$SOURCES',
  'SHF95': '$F95',
  'SHF95COM': '$SHF95 -o $TARGET -c $FORTRANCOMMONFLAGS $SHF95FLAGS '
              '$_F95INCFLAGS $_FORTRANMODFLAG $SOURCES',
  'SHF95FLAGS': ['$F95FLAGS'],
  'SHF95PPCOM': '$SHF95 -o $TARGET -c $FORTRANCOMMONFLAGS $SHF95FLAGS '
                '$CPPFLAGS $_CPPDEFFLAGS $_F95INCFLAGS $_FORTRANMODFLAG '
                '$SOURCES',
  'SHFORTRAN': '$FORTRAN',
  'SHFORTRANCOM': '$SHFORTRAN -o $TARGET -c $FORTRANCOMMONFLAGS '
                  '$SHFORTRANFLAGS $_FORTRANINCFLAGS $_FORTRANMODFLAG $SOURCES',
  'SHFORTRANFLAGS': ['$FORTRANFLAGS'],
  'SHFORTRANPPCOM': '$SHFORTRAN -o $TARGET -c $FORTRANCOMMONFLAGS '
                    '$SHFORTRANFLAGS $CPPFLAGS $_CPPDEFFLAGS $_FORTRANINCFLAGS '
                    '$_FORTRANMODFLAG $SOURCES',
  'SHLIBEMITTER': [ <function lib_emitter at 0x000001F3D93B4AF0>,
                    <function shlib_symlink_emitter at 0x000001F3D9AE8B80>,
                    <function shlib_emitter at 0x000001F3D9A5A290>],
  'SHLIBNAME': '${_get_shlib_dir}${SHLIBPREFIX}$_get_shlib_stem${_SHLIBSUFFIX}',
  'SHLIBNOVERSIONSYMLINKS': True,
  'SHLIBPREFIX': '',
  'SHLIBSONAMEFLAGS': '-Wl,-soname=$_SHLIBSONAME',
  'SHLIBSUFFIX': '.dll',
  'SHLIB_NOVERSION_SYMLINK': '${_get_shlib_dir}${SHLIBPREFIX}$_get_shlib_stem${SHLIBSUFFIX}',
  'SHLIB_SONAME_SYMLINK': '${_get_shlib_dir}$_SHLIBSONAME',
  'SHLINK': '$LINK',
  'SHLINKCOM': <SCons.Action.CommandGeneratorAction object at 0x000001F3D9A2E7A0>,
  'SHLINKCOMSTR': <function shlib_generator at 0x000001F3D9A59630>,
  'SHLINKFLAGS': ['$LINKFLAGS', '-shared'],
  'SHOBJPREFIX': '$OBJPREFIX',
  'SHOBJSUFFIX': '.o',
  'SMARTLINK': <function smart_link at 0x000001F3D93B4A60>,
  'SPAWN': <function spawn at 0x000001F3D9519AB0>,
  'STATIC_AND_SHARED_OBJECTS_ARE_THE_SAME': 1,
  'SUBSTFILEPREFIX': '',
  'SUBSTFILESUFFIX': '',
  'TAR': 'tar',
  'TARCOM': '$TAR $TARFLAGS -f $TARGET $SOURCES',
  'TARFLAGS': ['-c'],
  'TARGET_ARCH': None,
  'TARGET_OS': None,
  'TARSUFFIX': '.tar',
  'TEMPFILE': <class 'SCons.Platform.TempFileMunge'>,
  'TEMPFILEARGESCFUNC': <function quote_spaces at 0x000001F3D9252DD0>,
  'TEMPFILEARGJOIN': ' ',
  'TEMPFILEPREFIX': '@',
  'TEXTFILEPREFIX': '',
  'TEXTFILESUFFIX': '.txt',
  'TOOLS': [ 'default',
             'mingw',
             'gcc',
             'g++',
             'gnulink',
             'ar',
             'gas',
             'gfortran',
             'm4',
             'dmd',
             'filesystem',
             'jar',
             'javac',
             'rmic',
             'tar',
             'zip',
             'textfile'],
  'WINDOWSDEFPREFIX': '',
  'WINDOWSDEFSUFFIX': '.def',
  'WIXCANDLE': 'candle.exe',
  'WIXLIGHT': 'light.exe',
  'ZIP': 'zip',
  'ZIPCOM': <SCons.Action.FunctionAction object at 0x000001F3D9A8ACB0>,
  'ZIPCOMPRESSION': 8,
  'ZIPFLAGS': [],
  'ZIPROOT': [],
  'ZIPSUFFIX': '.zip',
  '_CCCOMCOM': '$CPPFLAGS $_CPPDEFFLAGS $_CPPINCFLAGS',
  '_CPPDEFFLAGS': '${_defines(CPPDEFPREFIX, CPPDEFINES, CPPDEFSUFFIX, __env__, '
                  'TARGET, SOURCE)}',
  '_CPPINCFLAGS': '${_concat(INCPREFIX, CPPPATH, INCSUFFIX, __env__, RDirs, '
                  'TARGET, SOURCE, affect_signature=False)}',
  '_DDEBUGFLAGS': '${_concat(DDEBUGPREFIX, DDEBUG, DDEBUGSUFFIX, __env__)}',
  '_DFLAGS': '${_concat(DFLAGPREFIX, DFLAGS, DFLAGSUFFIX, __env__)}',
  '_DINCFLAGS': '${_concat(DINCPREFIX, DPATH, DINCSUFFIX, __env__, RDirs, '
                'TARGET, SOURCE)}',
  '_DLIBDIRFLAGS': '${_concat(DLIBDIRPREFIX, LIBPATH, DLIBDIRSUFFIX, __env__, '
                   'RDirs, TARGET, SOURCE)}',
  '_DLIBFLAGS': '${_stripixes(DLIBLINKPREFIX, LIBS, DLIBLINKSUFFIX, '
                'LIBPREFIXES, LIBSUFFIXES,  __env__)}',
  '_DRPATH': '${_concat(DRPATHPREFIX, RPATH, DRPATHSUFFIX, __env__)}',
  '_DVERFLAGS': '${_concat(DVERPREFIX, DVERSIONS, DVERSUFFIX, __env__)}',
  '_F03INCFLAGS': '${_concat(INCF03PREFIX, F03PATH, INCF03SUFFIX, __env__, '
                  'RDirs, TARGET, SOURCE, affect_signature=False)}',
  '_F08INCFLAGS': '${_concat(INCF08PREFIX, F08PATH, INCF08SUFFIX, __env__, '
                  'RDirs, TARGET, SOURCE, affect_signature=False)}',
  '_F77INCFLAGS': '${_concat(INCF77PREFIX, F77PATH, INCF77SUFFIX, __env__, '
                  'RDirs, TARGET, SOURCE, affect_signature=False)}',
  '_F90INCFLAGS': '${_concat(INCF90PREFIX, F90PATH, INCF90SUFFIX, __env__, '
                  'RDirs, TARGET, SOURCE, affect_signature=False)}',
  '_F95INCFLAGS': '${_concat(INCF95PREFIX, F95PATH, INCF95SUFFIX, __env__, '
                  'RDirs, TARGET, SOURCE, affect_signature=False)}',
  '_FORTRANINCFLAGS': '${_concat(INCFORTRANPREFIX, FORTRANPATH, '
                      'INCFORTRANSUFFIX, __env__, RDirs, TARGET, SOURCE, '
                      'affect_signature=False)}',
  '_FORTRANMODFLAG': '$( ${_concat(FORTRANMODDIRPREFIX, FORTRANMODDIR, '
                     'FORTRANMODDIRSUFFIX, __env__, RDirs, TARGET, SOURCE)} $)',
  '_JARCOM': '$JAR $_JARFLAGS $TARGET $_JARMANIFEST $_JARSOURCES',
  '_JARFLAGS': <function jarFlags at 0x000001F3D9AB6EF0>,
  '_JARMANIFEST': <function jarManifest at 0x000001F3D9AB6E60>,
  '_JARSOURCES': <function jarSources at 0x000001F3D9AB5990>,
  '_JAVABOOTCLASSPATH': '${_javapathopt("-bootclasspath", '
                        '"JAVABOOTCLASSPATH")} ',
  '_JAVACCOM': '$JAVAC $JAVACFLAGS $_JAVABOOTCLASSPATH $_JAVACLASSPATH -d '
               '${TARGET.attributes.java_classdir} $_JAVASOURCEPATH $SOURCES',
  '_JAVACLASSPATH': '${_javapathopt("-classpath", "JAVACLASSPATH")} ',
  '_JAVASOURCEPATH': '${_javapathopt("-sourcepath", "JAVASOURCEPATH", '
                     '"_JAVASOURCEPATHDEFAULT")} ',
  '_JAVASOURCEPATHDEFAULT': '${TARGET.attributes.java_sourcedir}',
  '_LDMODULESONAME': <function _ldmodule_soname at 0x000001F3D9AE9000>,
  '_LDMODULESOVERSION': <function _ldmodule_soversion at 0x000001F3D9AE8F70>,
  '_LDMODULESUFFIX': '${LDMODULESUFFIX}${_LDMODULEVERSION}',
  '_LDMODULEVERSION': <function _LDMODULEVERSION at 0x000001F3D9AE9090>,
  '_LDMODULEVERSIONFLAGS': '$LDMODULEVERSIONFLAGS -Wl,-soname=$_LDMODULESONAME',
  '_LIBDIRFLAGS': '${_concat(LIBDIRPREFIX, LIBPATH, LIBDIRSUFFIX, __env__, '
                  'RDirs, TARGET, SOURCE, affect_signature=False)}',
  '_LIBFLAGS': '${_stripixes(LIBLINKPREFIX, LIBS, LIBLINKSUFFIX, LIBPREFIXES, '
               'LIBSUFFIXES, __env__)}',
  '_RPATH': '${_concat(RPATHPREFIX, RPATH, RPATHSUFFIX, __env__)}',
  '_SHDLIBVERSIONFLAGS': '$SHDLIBVERSIONFLAGS -L-soname=$_SHLIBSONAME',
  '_SHLIBSONAME': <function _soname at 0x000001F3D9AE8CA0>,
  '_SHLIBSOVERSION': <function _soversion at 0x000001F3D9AE8C10>,
  '_SHLIBSUFFIX': '$SHLIBSUFFIX',
  '_SHLIBVERSION': "${SHLIBVERSION and '.'+SHLIBVERSION or ''}",
  '_SHLIBVERSIONFLAGS': '$SHLIBVERSIONFLAGS -Wl,-soname=$_SHLIBSONAME',
  '__DSHLIBVERSIONFLAGS': '${__libversionflags(__env__,"DSHLIBVERSION","_DSHLIBVERSIONFLAGS")}',
  '__LDMODULEVERSIONFLAGS': '${__libversionflags(__env__,"LDMODULEVERSION","_LDMODULEVERSIONFLAGS")}',
  '__SHLIBVERSIONFLAGS': '${__libversionflags(__env__,"SHLIBVERSION","_SHLIBVERSIONFLAGS")}',
  '__lib_either_version_flag': <function __lib_either_version_flag at 0x000001F3D93B7250>,
  '__libversionflags': <function __libversionflags at 0x000001F3D93B6F80>,
  '_concat': <function _concat at 0x000001F3D93B6CB0>,
  '_defines': <function _defines at 0x000001F3D93B6EF0>,
  '_get_ldmodule_stem': <function _get_ldmodule_stem at 0x000001F3D9AE8EE0>,
  '_get_shlib_dir': <function _get_shlib_dir at 0x000001F3D9AE8DC0>,
  '_get_shlib_stem': <function _get_shlib_stem at 0x000001F3D9AE8D30>,
  '_javapathopt': <class 'SCons.Tool.javac.pathopt'>,
  '_stripixes': <function _stripixes at 0x000001F3D93B6DD0>}
scons: done reading SConscript files.
scons: Building targets ...
scons: `.' is up to date.
scons: done building targets.
```

#### C文件编译行为分析

首先我们调整下编译行为，注释`Program`，只执行`Object`，可以看到其最终执行了`gcc -o main.o -c main.c`，那为什么其知道要使用这个命令呢？如果我需要加一些编译参数，应该如何配置呢？如果要进行嵌入式开发，需要替换gcc为aram-xx-gcc如何处理？

![image-20220913212755986](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220913212755986.png)



从上文可知，scons是通过`CCCOM`来指导c文件编译的。从官网上也可以看出是通过这个来完成对c的源文件编译，生成object文件。

![image-20220914132041877](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220914132041877.png)

通过dump可知，默认配置下，各个参数如下：

- `TARGET`：就是目标文件
- `SOURCES`：就是源文件列表
- `CFLAGS`：通用C配置参数
- `CCFLAGS`：通用C和C++公用的配置参数，因为scons支持多个语言，配置了这个参数，其同时会在C++编译时使用。详细可以参考：`CXXCOM`
- `_CCCOMCOM`： 更多参数配置，如-D或者-I等配置。
  - `CPPFLAGS`：用于预处理相关的配置，既可以用于C编译，同时也被用于ASM编译。
  - `_CPPDEFFLAGS`：用于-D的预编译配置。
  - `_CPPINCFLAGS`：用于-I的include路径配置。

```json
{
  'CC': 'gcc',
  'CCCOM': '$CC -o $TARGET -c $CFLAGS $CCFLAGS $_CCCOMCOM $SOURCES',
  'CCFLAGS': [],
  'CFLAGS': [],
  '_CCCOMCOM': '$CPPFLAGS $_CPPDEFFLAGS $_CPPINCFLAGS',
  'CPPDEFPREFIX': '-D',
  'CPPDEFSUFFIX': '',
  '_CPPDEFFLAGS': '${_defines(CPPDEFPREFIX, CPPDEFINES, CPPDEFSUFFIX, __env__, '
                  'TARGET, SOURCE)}',
  'INCPREFIX': '-I',
  'INCSUFFIX': '',
  '_CPPINCFLAGS': '${_concat(INCPREFIX, CPPPATH, INCSUFFIX, __env__, RDirs, '
                  'TARGET, SOURCE, affect_signature=False)}',
}
```

其实熟悉GCC的基本已经看明白了，其实把gcc编译object的参数全部配置好了，需要的话直接改env对应的参数即可。

在示例中，`obj = Object('main.c')`中`SOURCES = [main.c]`，`TARGET = main.o`，其他参数由于都没开启，所以没显示。最终就是我们看到的gcc操作。

```c
gcc -o main.o -c main.c
```

```python
obj = Object('main.c')
```



假设调整`CCFLAGS`，加入`-g`参数，编译结果如下图所示，可以看出确实是跟着变的，之后我们只要对应改相关的参数，就可以做到修改gcc的目的。

![image-20220914134548062](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220914134548062.png)





#### ASM文件编译行为分析

在PC环境下，基本很少写ASM相关的程序，而在嵌入式环境下，不管是`startup`文件还是一些特殊用途的行为，都需要使用ASM语句进行操作。

类似于C文件的编译过程，由于PC环境所需的汇编指令各不相同，在嵌入式系统下针对对应的芯片，也有不同汇编指令，本节只对相关配置进行说明。

从上文可知，scons是通过`ASCOM`来指导asm文件编译的。从官网上也可以看出是通过这个来完成对c的源文件编译，生成object文件。

![image-20220915091107811](C:/Users/wenbo/AppData/Roaming/Typora/typora-user-images/image-20220915091107811.png)

通过dump可知，默认配置下，各个参数如下：

- `TARGET`：就是目标文件
- `SOURCES`：就是源文件列表
- `ASFLAGS`：通用ASM配置参数

```json
{
  'AS': 'as',
  'ASCOM': '$AS $ASFLAGS -o $TARGET $SOURCES',
  'ASFLAGS': [],
}
```

和gcc类似，实际是使用`as`来对ASM程序进行编译，生成object文件。



#### Link编译行为分析

在完成Object的文件编译后，生成了一个或多个的Object文件。编译的最后一步是将这些Object文件Link为Program程序。

我们保留生成的Object，只执行`Program`，

首先我们调整下编译行为，注释`Program`，只执行`Object`，可以看到其最终执行了`gcc -o main.exe main.o`，那为什么其知道要使用这个命令呢？如果我需要加一些编译参数，应该如何配置呢？如果要进行嵌入式开发，需要替换gcc为aram-xx-ld如何处理？

![image-20220915092157352](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220915092157352.png)



从上文可知，scons是通过`LINKCOM`来指导LINK的。从官网上也可以看出是通过这个来完成对Object文件Link流程的。

![image-20220915092318063](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220915092318063.png)

通过dump可知，默认配置下，各个参数如下，由于LINK实际环境使用的程序各不一样，所以实际是一个python对象：

- `TARGET`：就是目标文件
- `SOURCES`：就是源文件列表
- `LINKFLAGS`：通用ld配置参数
- `_LIBDIRFLAGS`：用于-L的lib路径配置，`LIBPATH`为具体路径
- `_LIBFLAGS`： 用于-l的lib文件配置，`LIBS`为具体lib名称。

```json
{
  'LINK': '$SMARTLINK',
  'LINKCOM': '$LINK -o $TARGET $LINKFLAGS $__RPATH $SOURCES $_LIBDIRFLAGS '
             '$_LIBFLAGS',
  'LINKFLAGS': [],
  'LIBDIRPREFIX': '-L',
  'LIBDIRSUFFIX': '',
  '_LIBDIRFLAGS': '${_concat(LIBDIRPREFIX, LIBPATH, LIBDIRSUFFIX, __env__, '
                  'RDirs, TARGET, SOURCE, affect_signature=False)}',
  'LIBLINKPREFIX': '-l',
  'LIBLINKSUFFIX': '',
  '_LIBFLAGS': '${_stripixes(LIBLINKPREFIX, LIBS, LIBLINKSUFFIX, LIBPREFIXES, '
               'LIBSUFFIXES, __env__)}',
}
```

和GCC一样，Program最终调用的就是这个配置。

假设调整`LINKFLAGS`，加入`-g`参数，编译结果如下图所示，可以看出确实是跟着变的，之后我们只要对应改相关的参数，就可以做到修改link的目的。

![image-20220915093322494](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220915093322494.png)





### 嵌入式开发和Scons模板

默认情况下，c编译是根据具体编译环境来的，scons会自己选定gcc程序、asm程序和Link程序，但是在嵌入式开发时，需要指定交叉编译器，按照之前的所描述的，其实大家已经清楚了，只需要调整相应的配置参数即可。

此外嵌入式开发也有一些特殊的配置，这都需要我们理解并调整配置参数才行。

如下所示，每行都有注释，下面对一些关键参数/函数进行说明：

- `get_path_files`：工具函数，获取路径下所有特定后缀的文件，当然可以用其他方式实现（实现这个函数主要为了写path的时候方便）
- `GCC_ARM_PATH`：交叉工具链路径，scons直接改工作路径不怎么会，直接指定路径
- `PLF`：编译平台，默认使用PC编译，当然嵌入式开发可以选`'arm'`，之后会自动去配置相关参数
- `PREFIX`：嵌入式开发需要，交叉工具链前缀
- `SPEC_LD_FLAGS`：arm交叉工具链开发的时候，LD使用有一些特殊的要求，scons原生的参数不怎么好用，需要在`_LIBFLAGS`参数尾巴拼接上Map信息，其他工具链有特殊要求也可以根据需要调整。

```python
import os


def get_path_files(dirs, file_ext):
    path_files = []
    # print('dir: ' + str(dirs))
    for dir in dirs:
        # print('dir: ' + dir)
        path_files.append(Glob(dir + '/' + file_ext))
    return path_files


GCC_ARM_PATH = 'D:/env/gcc-arm-none-eabi-4_8-2014q3-20140805-win32'

#PLF = 'arm'
PLF = ''

# toolchains
if PLF == 'arm':
    PREFIX = GCC_ARM_PATH + '/bin/arm-none-eabi-'
else:
    PREFIX = ''

CC = PREFIX + 'gcc'
AS = PREFIX + 'as'
AR = PREFIX + 'ar'
CXX = PREFIX + 'g++'
LINK = PREFIX + 'ld'

SIZE = PREFIX + 'size'
OBJDUMP = PREFIX + 'objdump'
OBJCPY = PREFIX + 'objcopy'


TARGET_PATH = 'build/'
TARGET_NAME = 'main'
TARGET_WITHOUT_SUFFIX = TARGET_PATH + TARGET_NAME


###################################################################################
# C source dirs config
C_DIRS = []
#C_DIRS.append('src')

# C source files config
C_FILES = []
#C_FILES.append('main.c')

# Create c sources list
C_SRC_LIST = get_path_files(C_DIRS, '*.c') + C_FILES


###################################################################################
# ASM source dirs config
AS_DIRS = []
#AS_DIRS.append('src')

# ASM source files config
AS_FILES = []
#AS_FILES.append('startup.s')

AS_SRC_LIST = get_path_files(AS_DIRS, '*.s') + AS_FILES


###################################################################################
# -I, Include path config
CPP_PATH = []
#CPP_PATH.append('inc')

# -D, Preprocess Define
CPP_DEFINES = []
#CPP_DEFINES.append('CFG_TEST')

# C generate define
C_FLAGS = []
C_FLAGS.append('-O1')
C_FLAGS.append('-g')
C_FLAGS.append('-std=c99')

# C and C++ generate define
CC_FLAGS = []
CC_FLAGS.append('-Wall')


# ASM generate define
AS_FLAGS = []
AS_FLAGS.append('-g')




# Link Config
LINK_FLAGS = []
#LINK_FLAGS.append('-Wl,–gc-sections')


# lib path.
LIB_PATH = []
#LIB_PATH.append('lib')


# .lib, .a file
LIBS_FILES = []
#LIBS_FILES.append('test')

# spec ld flag. Arm spec.
SPEC_LD_FLAGS = []
if PLF == 'arm':
    SPEC_LD_FLAGS.append('-Map')
    SPEC_LD_FLAGS.append(TARGET_WITHOUT_SUFFIX + '.map')
    SPEC_LD_FLAGS.append('-T' + 'src/map_ram.txt')


env = Environment()

###################################################################################
# Step0: toolchains setting.
if PLF == 'arm':
    env['CC'] = CC
    env['AS'] = AS
    env['AR'] = AR
    env['CXX'] = CXX
    env['LINK'] = LINK

    env['OBJSUFFIX'] = '.o'
    env['LIBPREFIX'] = 'lib'
    env['LIBSUFFIX'] = '.a'
    env['PROGSUFFIX'] = '.elf'

###################################################################################
# Step1: C compile setting. use <print(env.Dump())> for details.
# 'CCCOM': '$CC -o $TARGET -c $CFLAGS $CCFLAGS $_CCCOMCOM $SOURCES'

# Step1.0: General options, like: optim/debug setting. $CFLAGS.
env.Append(CFLAGS=C_FLAGS)

# Step1.1: General options, other setting. $CCFLAGS.
env.Append(CCFLAGS=CC_FLAGS)

# Step1.2: -D, -I, setting. $_CCCOMCOM
# '_CCCOMCOM': '$CPPFLAGS $_CPPDEFFLAGS $_CPPINCFLAGS'
# StepX.2.0: CPPFLAGS setting. --- do nothing.
# StepX.2.1: -D setting. 
# 'CPPDEFPREFIX': '-D'
# '_CPPDEFFLAGS': '${_defines(CPPDEFPREFIX, CPPDEFINES, CPPDEFSUFFIX, __env__, '
#                 'TARGET, SOURCE)}',
env.Append(CPPDEFINES=CPP_DEFINES)
# Step1.2.2: -I setting. 
# 'INCPREFIX': '-I'
# '_CPPINCFLAGS': '${_concat(INCPREFIX, CPPPATH, INCSUFFIX, __env__, RDirs, '
#                 'TARGET, SOURCE, affect_signature=False)}',
env.Append(CPPPATH=CPP_PATH)

###################################################################################
# Step2: ASM compile setting. use <print(env.Dump())> for details.
# 'ASCOM': '$AS $ASFLAGS -o $TARGET $SOURCES'

# Step2.0: General options. $ASFLAGS.
env.Append(ASFLAGS=AS_FLAGS)


###################################################################################
# Step3: LINK setting. use <print(env.Dump())> for details.
# 'LINKCOM': '$LINK -o $TARGET $LINKFLAGS $__RPATH $SOURCES $_LIBDIRFLAGS '
#            '$_LIBFLAGS',

# Step3.0: General options. $LINKFLAGS.
env.Append(LINKFLAGS=LINK_FLAGS)

# Step3.1: Link path setting. $_LIBDIRFLAGS.
# '_LIBDIRFLAGS': '${_concat(LIBDIRPREFIX, LIBPATH, LIBDIRSUFFIX, __env__, '
#                 'RDirs, TARGET, SOURCE, affect_signature=False)}',
env.Append(LIBPATH=LIB_PATH)

# Step3.2: libs setting, like *.a, *.lib. $_LIBFLAGS.
#   '_LIBFLAGS': '${_stripixes(LIBLINKPREFIX, LIBS, LIBLINKSUFFIX, LIBPREFIXES, '
#                'LIBSUFFIXES, __env__)}',
env.Append(LIBS=LIBS_FILES)

# Step3.3: Add some spec params. must append at end.
env.Append(_LIBFLAGS=SPEC_LD_FLAGS)


###################################################################################
# Step4: Compile Object files, use:
#        1. <$CCCOM>: For c code compile
#        2. <$ASCOM>: For asm code compile
c_objs = env.Object(C_SRC_LIST)
as_objs = env.Object(AS_SRC_LIST)



###################################################################################
# Step5: Compile target <.elf>, use <$LINKCOM>.
target = env.Program(target = TARGET_WITHOUT_SUFFIX, source=[c_objs, as_objs])

# Other compile target.
env.Command(TARGET_WITHOUT_SUFFIX + '.bin', target, OBJCPY + ' -v -O binary $SOURCE $TARGET')
env.Command(TARGET_WITHOUT_SUFFIX + '.lst', target, OBJDUMP + ' --source --all-headers --demangle --line-numbers --wide $SOURCE > $TARGET')
env.Command(TARGET_WITHOUT_SUFFIX + '.size', target, SIZE + ' --format=berkeley $SOURCE')

# Dump() env params, if need.
#print(env.Dump())


```









### 模板使用示例

下面举一个例子，还是以PC举例，嵌入式开发自己根据需要配置即可。

有如下的一个多文件结构的C代码，目前要用scons来编译，在根目录下写`SConstruct`配置文件。

![image-20220915220449757](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220915220449757.png)



最终的SConstruct配置如下：

```python
import os


def get_path_files(dirs, file_ext):
    path_files = []
    # print('dir: ' + str(dirs))
    for dir in dirs:
        # print('dir: ' + dir)
        path_files.append(Glob(dir + '/' + file_ext))
    return path_files


GCC_ARM_PATH = 'D:/env/gcc-arm-none-eabi-4_8-2014q3-20140805-win32'

#PLF = 'arm'
PLF = ''

# toolchains
if PLF == 'arm':
    PREFIX = GCC_ARM_PATH + '/bin/arm-none-eabi-'
else:
    PREFIX = ''

CC = PREFIX + 'gcc'
AS = PREFIX + 'as'
AR = PREFIX + 'ar'
CXX = PREFIX + 'g++'
LINK = PREFIX + 'ld'

SIZE = PREFIX + 'size'
OBJDUMP = PREFIX + 'objdump'
OBJCPY = PREFIX + 'objcopy'


TARGET_PATH = 'build/'
TARGET_NAME = 'main'
TARGET_WITHOUT_SUFFIX = TARGET_PATH + TARGET_NAME


###################################################################################
# C source dirs config
C_DIRS = []
C_DIRS.append('app\driver\src')
C_DIRS.append('module1\src')
C_DIRS.append('module2\src')


# C source files config
C_FILES = []
C_FILES.append('app\main.c')

# Create c sources list
C_SRC_LIST = get_path_files(C_DIRS, '*.c') + C_FILES


###################################################################################
# ASM source dirs config
AS_DIRS = []
#AS_DIRS.append('src')

# ASM source files config
AS_FILES = []
#AS_FILES.append('startup.s')

AS_SRC_LIST = get_path_files(AS_DIRS, '*.s') + AS_FILES


###################################################################################
# -I, Include path config
CPP_PATH = []
CPP_PATH.append('app\driver\inc')
CPP_PATH.append('module1\inc')
CPP_PATH.append('module2\inc')

# -D, Preprocess Define
CPP_DEFINES = []
#CPP_DEFINES.append('CFG_TEST')

# C generate define
C_FLAGS = []
C_FLAGS.append('-O1')
C_FLAGS.append('-g')
C_FLAGS.append('-std=c99')

# C and C++ generate define
CC_FLAGS = []
CC_FLAGS.append('-Wall')


# ASM generate define
AS_FLAGS = []
AS_FLAGS.append('-g')




# Link Config
LINK_FLAGS = []
#LINK_FLAGS.append('-Wl,–gc-sections')


# lib path.
LIB_PATH = []
#LIB_PATH.append('lib')


# .lib, .a file
LIBS_FILES = []
#LIBS_FILES.append('test')

# spec ld flag. Arm spec.
SPEC_LD_FLAGS = []
if PLF == 'arm':
    SPEC_LD_FLAGS.append('-Map')
    SPEC_LD_FLAGS.append(TARGET_WITHOUT_SUFFIX + '.map')
    SPEC_LD_FLAGS.append('-T' + 'src/map_ram.txt')


env = Environment()

###################################################################################
# Step0: toolchains setting.
if PLF == 'arm':
    env['CC'] = CC
    env['AS'] = AS
    env['AR'] = AR
    env['CXX'] = CXX
    env['LINK'] = LINK

    env['OBJSUFFIX'] = '.o'
    env['LIBPREFIX'] = 'lib'
    env['LIBSUFFIX'] = '.a'
    env['PROGSUFFIX'] = '.elf'

###################################################################################
# Step1: C compile setting. use <print(env.Dump())> for details.
# 'CCCOM': '$CC -o $TARGET -c $CFLAGS $CCFLAGS $_CCCOMCOM $SOURCES'

# Step1.0: General options, like: optim/debug setting. $CFLAGS.
env.Append(CFLAGS=C_FLAGS)

# Step1.1: General options, other setting. $CCFLAGS.
env.Append(CCFLAGS=CC_FLAGS)

# Step1.2: -D, -I, setting. $_CCCOMCOM
# '_CCCOMCOM': '$CPPFLAGS $_CPPDEFFLAGS $_CPPINCFLAGS'
# StepX.2.0: CPPFLAGS setting. --- do nothing.
# StepX.2.1: -D setting. 
# 'CPPDEFPREFIX': '-D'
# '_CPPDEFFLAGS': '${_defines(CPPDEFPREFIX, CPPDEFINES, CPPDEFSUFFIX, __env__, '
#                 'TARGET, SOURCE)}',
env.Append(CPPDEFINES=CPP_DEFINES)
# Step1.2.2: -I setting. 
# 'INCPREFIX': '-I'
# '_CPPINCFLAGS': '${_concat(INCPREFIX, CPPPATH, INCSUFFIX, __env__, RDirs, '
#                 'TARGET, SOURCE, affect_signature=False)}',
env.Append(CPPPATH=CPP_PATH)

###################################################################################
# Step2: ASM compile setting. use <print(env.Dump())> for details.
# 'ASCOM': '$AS $ASFLAGS -o $TARGET $SOURCES'

# Step2.0: General options. $ASFLAGS.
env.Append(ASFLAGS=AS_FLAGS)


###################################################################################
# Step3: LINK setting. use <print(env.Dump())> for details.
# 'LINKCOM': '$LINK -o $TARGET $LINKFLAGS $__RPATH $SOURCES $_LIBDIRFLAGS '
#            '$_LIBFLAGS',

# Step3.0: General options. $LINKFLAGS.
env.Append(LINKFLAGS=LINK_FLAGS)

# Step3.1: Link path setting. $_LIBDIRFLAGS.
# '_LIBDIRFLAGS': '${_concat(LIBDIRPREFIX, LIBPATH, LIBDIRSUFFIX, __env__, '
#                 'RDirs, TARGET, SOURCE, affect_signature=False)}',
env.Append(LIBPATH=LIB_PATH)

# Step3.2: libs setting, like *.a, *.lib. $_LIBFLAGS.
#   '_LIBFLAGS': '${_stripixes(LIBLINKPREFIX, LIBS, LIBLINKSUFFIX, LIBPREFIXES, '
#                'LIBSUFFIXES, __env__)}',
env.Append(LIBS=LIBS_FILES)

# Step3.3: Add some spec params. must append at end.
env.Append(_LIBFLAGS=SPEC_LD_FLAGS)


###################################################################################
# Step4: Compile Object files, use:
#        1. <$CCCOM>: For c code compile
#        2. <$ASCOM>: For asm code compile
c_objs = env.Object(C_SRC_LIST)
as_objs = env.Object(AS_SRC_LIST)



###################################################################################
# Step5: Compile target <.elf>, use <$LINKCOM>.
target = env.Program(target = TARGET_WITHOUT_SUFFIX, source=[c_objs, as_objs])

# Other compile target.
env.Command(TARGET_WITHOUT_SUFFIX + '.bin', target, OBJCPY + ' -v -O binary $SOURCE $TARGET')
env.Command(TARGET_WITHOUT_SUFFIX + '.lst', target, OBJDUMP + ' --source --all-headers --demangle --line-numbers --wide $SOURCE > $TARGET')
env.Command(TARGET_WITHOUT_SUFFIX + '.size', target, SIZE + ' --format=berkeley $SOURCE')

# Dump() env params, if need.
#print(env.Dump())




```



执行scons操作，可以看到相关参数的编译过程，最后也会生成bin、lst以及code size信息。

```bash
D:\test\sample_4>scons
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
gcc -o app\driver\src\driver1.1.o -c -O1 -g -std=c99 -Wall -Iapp\driver\inc -Imodule1\inc -Imodule2\inc app\driver\src\driver1.1.c
gcc -o app\driver\src\driver2.2.o -c -O1 -g -std=c99 -Wall -Iapp\driver\inc -Imodule1\inc -Imodule2\inc app\driver\src\driver2.2.c
gcc -o app\main.o -c -O1 -g -std=c99 -Wall -Iapp\driver\inc -Imodule1\inc -Imodule2\inc app\main.c
gcc -o module1\src\module1.1.o -c -O1 -g -std=c99 -Wall -Iapp\driver\inc -Imodule1\inc -Imodule2\inc module1\src\module1.1.c
gcc -o module1\src\module1.2.o -c -O1 -g -std=c99 -Wall -Iapp\driver\inc -Imodule1\inc -Imodule2\inc module1\src\module1.2.c
gcc -o module2\src\module2.1.o -c -O1 -g -std=c99 -Wall -Iapp\driver\inc -Imodule1\inc -Imodule2\inc module2\src\module2.1.c
gcc -o module2\src\module2.2.o -c -O1 -g -std=c99 -Wall -Iapp\driver\inc -Imodule1\inc -Imodule2\inc module2\src\module2.2.c
gcc -o build\main.exe app\driver\src\driver1.1.o app\driver\src\driver2.2.o module1\src\module1.1.o module1\src\module1.2.o module2\src\module2.1.o module2\src\module2.2.o app\main.o
objcopy -v -O binary build\main.exe build\main.bin
copy from `build\main.exe' [pei-i386] to `build\main.bin' [binary]
objdump --source --all-headers --demangle --line-numbers --wide build\main.exe > build\main.lst
size --format=berkeley build\main.exe
   text    data     bss     dec     hex filename
  39620    2944    2676   45240    b0b8 build\main.exe
scons: done building targets.

D:\test\sample_4>scons -c
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Cleaning targets ...
Removed app\driver\src\driver1.1.o
Removed app\driver\src\driver2.2.o
Removed app\main.o
Removed module1\src\module1.1.o
Removed module1\src\module1.2.o
Removed module2\src\module2.1.o
Removed module2\src\module2.2.o
Removed build\main.exe
Removed build\main.bin
Removed build\main.lst
scons: done cleaning targets.
```



