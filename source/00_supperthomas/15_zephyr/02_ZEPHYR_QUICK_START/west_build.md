# Zephyr 构建流程

## 简介

刚开始，一定有小伙伴疑惑`west build` 之后到底做了哪些事情呢？

当然如果你只关心如何写应用层，可以不用关心编译构建相关的东西，

这篇文章介绍了zephyr如何从`west build`之后具体做了哪些东西。

### west build

首先是west 执行build之后，其实执行的是scripts/west_commands/build.py

这里面运行的是`do_run`

这里如果想打印所有log的话，只要加上这样一句话：

```
        log.VERBOSE = 4;
```

即可：

接下来我们看看完整的log， 执行命令`west -v build -p always -b nucleo_l496zg samples/hello_world`

```
args: Namespace(help=None, zephyr_base=None, verbose=1, command='build', board='nucleo_l496zg', source_dir=None, build_dir=None, force=False, cmake=False, cmake_only=False, domain=None, target=None, test_item=None, build_opt=[], dry_run=False, snippets=[], sysbuild=False, no_sysbuild=False, pristine='always') remainder: ['samples/hello_world']
source_dir: samples/hello_world cmake_opts: None
setting up build directory
setting up source directory
config dir-fmt: build
build is a zephyr build directory
build dir: build
pristine: always auto_pristine: False
/home/thomas/zephyrproject/zephyr/build is a zephyr build directory
-- west build: making build dir /home/thomas/zephyrproject/zephyr/build pristine
/home/thomas/zephyrproject/zephyr/build is a zephyr build directory
cmake version 3.22.1 is OK; minimum version is 3.13.1
Running CMake: /usr/bin/cmake -DBINARY_DIR=/home/thomas/zephyrproject/zephyr/build -DSOURCE_DIR=/home/thomas/zephyrproject/zephyr/samples/hello_world -P /home/thomas/zephyrproject/zephyr/cmake/pristine.cmake
setting up source directory
sanity checking the build
/home/thomas/zephyrproject/zephyr/samples/hello_world is NOT a valid zephyr build directory
-- west build: generating a build system
cmake version 3.22.1 is OK; minimum version is 3.13.1
Running CMake: /usr/bin/cmake -DWEST_PYTHON=/home/thomas/zephyrproject/.venv/bin/python3 -B/home/thomas/zephyrproject/zephyr/build -GNinja -DBOARD=nucleo_l496zg -S/home/thomas/zephyrproject/zephyr/samples/hello_world
Re-run cmake no build system arguments
Loading Zephyr default modules (Zephyr base).
-- Application: /home/thomas/zephyrproject/zephyr/samples/hello_world
-- CMake version: 3.22.1
-- Found Python3: /home/thomas/zephyrproject/.venv/bin/python3.10 (found suitable exact version "3.10.6") found components: Interpreter 
-- Cache files will be written to: /home/thomas/.cache/zephyr
-- Zephyr version: 3.4.99 (/home/thomas/zephyrproject/zephyr)
-- Found west (found suitable version "1.1.0", minimum required is "0.14.0")
-- Board: nucleo_l496zg
-- ZEPHYR_TOOLCHAIN_VARIANT not set, trying to locate Zephyr SDK
-- Found host-tools: zephyr 0.16.1 (/home/thomas/zephyr-sdk-0.16.1)
-- Found toolchain: zephyr 0.16.1 (/home/thomas/zephyr-sdk-0.16.1)
-- Found Dtc: /home/thomas/zephyr-sdk-0.16.1/sysroots/x86_64-pokysdk-linux/usr/bin/dtc (found suitable version "1.6.0", minimum required is "1.4.6") 
-- Found BOARD.dts: /home/thomas/zephyrproject/zephyr/boards/arm/nucleo_l496zg/nucleo_l496zg.dts
-- Generated zephyr.dts: /home/thomas/zephyrproject/zephyr/build/zephyr/zephyr.dts
-- Generated devicetree_generated.h: /home/thomas/zephyrproject/zephyr/build/zephyr/include/generated/devicetree_generated.h
-- Including generated dts.cmake file: /home/thomas/zephyrproject/zephyr/build/zephyr/dts.cmake
/home/thomas/zephyrproject/zephyr/build/zephyr/zephyr.dts:704.10-711.5: Warning (simple_bus_reg): /soc/clocks: missing or empty reg/ranges property
Parsing /home/thomas/zephyrproject/zephyr/Kconfig
Loaded configuration '/home/thomas/zephyrproject/zephyr/boards/arm/nucleo_l496zg/nucleo_l496zg_defconfig'
Merged configuration '/home/thomas/zephyrproject/zephyr/samples/hello_world/prj.conf'
Configuration saved to '/home/thomas/zephyrproject/zephyr/build/zephyr/.config'
Kconfig header saved to '/home/thomas/zephyrproject/zephyr/build/zephyr/include/generated/autoconf.h'
-- Found GnuLd: /home/thomas/zephyr-sdk-0.16.1/arm-zephyr-eabi/bin/../lib/gcc/arm-zephyr-eabi/12.2.0/../../../../arm-zephyr-eabi/bin/ld.bfd (found version "2.38") 
-- The C compiler identification is GNU 12.2.0
-- The CXX compiler identification is GNU 12.2.0
-- The ASM compiler identification is GNU
-- Found assembler: /home/thomas/zephyr-sdk-0.16.1/arm-zephyr-eabi/bin/arm-zephyr-eabi-gcc
-- Configuring done
-- Generating done
-- Build files have been written to: /home/thomas/zephyrproject/zephyr/build
sanity checking the build
/home/thomas/zephyrproject/zephyr/samples/hello_world is NOT a valid zephyr build directory
-- west build: building application
cmake version 3.22.1 is OK; minimum version is 3.13.1
Running CMake: /usr/bin/cmake --build /home/thomas/zephyrproject/zephyr/build -- -v
[1/154] cd /home/thomas/zephyrproject/zephyr/build/zephyr && /usr/bin/cmake -E echo
```

输入命令`export VERBOSE=1` 这个可以让cmake的命令全部打出来。

这边发下一个bug， verbose如果build里面是-v的话是1， 但是不管verbose是1还是0，build log都打不开。

这里不是bug，实际上是`west -v -v -v build -p always -b nucleo_l496zg samples/hello_world` 需要这样玩。

具体可以参考

https://github.com/zephyrproject-rtos/west/blob/main/src/west/app/main.py

