# RT-Thread BSP支持dist功能

根据[RT-Thread文档说明](https://docs.rt-thread.org/#/rt-thread-version/rt-thread-standard/application-note/setup/standard-project/an0017-standard-project?id=%e6%90%ad%e5%bb%ba%e9%a1%b9%e7%9b%ae%e6%a1%86%e6%9e%b6)，可以在BSP目录下运行`scons -—dist` 命令。该命令会在BSP目录下生成dist目录，该目录下包含了RT-Thread在内的当前BSP的依赖文件，可以拷贝到任意地方进行开发。

但是目前有一些BSP是不支持该功能的，下面由本文介绍一下如何让BSP支持dist功能。

## 一、代码分析

提供dist功能的是位于`rt-thread/tools` 目录的[`mkdist.py`](http://mkdist.py/) 脚本文件，在文件的`MkDist` 函数中[调用了](https://github.com/RT-Thread/rt-thread/blob/08a4de57e2f5e2f0d770b569690616599eaaf5fe/tools/mkdist.py#L340)来自BSP的`dist_handle` 函数。然后会将rt-thread的`components` 等目录拷贝到BSP下的dist目录。

这个`dist_handle` 由板级支持包在[`rtconfig.py`](http://rtconfig.py/) 中定义。在运行`scons -—dist` 命令时，`building.py` 内的`EndBuilding` 函数在`rtconfig`内寻找`dist_handle` 函数，并放入全局变量`Env` 中，[点击查看](https://github.com/RT-Thread/rt-thread/blob/08a4de57e2f5e2f0d770b569690616599eaaf5fe/tools/building.py#L892)。

## 二、方案说明

所以BSP需要定义`dist_handle` 函数将BSP所需要用到的`libraries` 拷贝到dist目录。而一般BSP根目录下会有多个BSP，如`nrf5x/nrf52832` 、`nrf5x/nrf52840` ，这些BSP又需要引用同样的`libraries` ，所以很多开发板的支持包会在BSP根目录下创建一个`tools/sdk_dist.py` 脚本文件用来实现文件拷贝，再在`rtconfig.py` 内调用tools下面的脚本。

## 三、操作示例

这里使用`nrf5x/nrf52832` 为例子介绍如何添加dist功能支持。

在nrf5x目录下创建`toos/sdk_dist.py` 文件：

```bash
import os
import sys
import shutil
cwd_path = os.getcwd()
sys.path.append(os.path.join(os.path.dirname(cwd_path), 'rt-thread', 'tools'))

# BSP dist function
def dist_do_building(BSP_ROOT, dist_dir):
    from mkdist import bsp_copy_files
    import rtconfig

    library_dir  = os.path.join(dist_dir, 'libraries')

    print("=> copy nrf52 bsp libraries")
    library_path = os.path.join(os.path.dirname(BSP_ROOT), 'libraries')

    bsp_copy_files(library_path, library_dir)
```

文件内`dist_do_building` 的方法内定义具体的`libraries` 复制操作，需要根据不同的开发板自己定义。

然后在`nrf5x/nrf52832/rtconfig.py`内添加前面提到的`dist_handle`方法：

```bash
def dist_handle(BSP_ROOT, dist_dir):
    import sys
    cwd_path = os.getcwd()
    sys.path.append(os.path.join(os.path.dirname(BSP_ROOT), 'tools'))
    from sdk_dist import dist_do_building
    dist_do_building(BSP_ROOT, dist_dir)
```

这个方法会动态导入刚刚创建的`toos/sdk_dist.py` 脚本，并调用`dist_do_building` 函数进行拷贝。

完成这两处修改之后在开发板目录下运行`scons -—dist` 即可创建dist目录，将dist目录拷贝到任何地方，然后尝试进行编译，如果可以正常编译就说明该BSP已经成功支持dist功能。