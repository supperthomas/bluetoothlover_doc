# 在VS Code上使用GCC开发嵌入式应用

***资源总汇***

- [VS Code](https://code.visualstudio.com/Download)
- [CMake](https://cmake.org/download/)
- [Arm GUN 工具链](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads)
- [nRF5 SDK](https://www.nordicsemi.com/Software-and-tools/Software/nRF5-SDK/Download#infotabs)
- [nRF Command Line Tools](https://www.nordicsemi.com/Software-and-tools/Development-Tools/nRF-Command-Line-Tools/Download#infotabs)
- [SEGGER J-Link software](https://www.segger.com/downloads/jlink/#J-LinkSoftwareAndDocumentationPack)

这篇文章基于nrf52832介绍如何在VS Code上面使用GCC进行单片机的编译、烧录和调试，其实很多单片机都可以采用类似的方式进行开发，希望读者可以触类旁通。

在开始之前，请先前往<https://code.visualstudio.com/Download>下载适合你电脑操作系统的VS Code版本，并进行安装。

## 编译

### 安装工具链

安装[CMake](https://cmake.org/download/)。

下载适合你操作系统的[Arm GUN 工具链](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads)，然后解压到你平时安装软件的地方。

如：```/usr/local/gcc-arm-none-eabi-9-2019-q4-major```

### 下载配置nRF5 SDK

下载[nRF5 SDK](https://www.nordicsemi.com/Software-and-tools/Software/nRF5-SDK/Download#infotabs)并解压，作为演示这里解压到```/home/jiy/nRF5_SDK_16.0.0_98a08e2```目录，实际操作时请修改为实际路径。

打开```/home/jiy/nRF5_SDK_16.0.0_98a08e2/components/toolchain/gcc/Makefile.posix```文件，并且更改```GNU_INSTALL_ROOT```为GNU工具链所在位置：（注意bin和后面的斜杆不要漏了！）

例如：

```text
GNU_INSTALL_ROOT ?= /usr/local/gcc-arm-none-eabi-9-2019-q4-major/bin/
GNU_VERSION ?= 7.3.1
GNU_PREFIX ?= arm-none-eabi
```

### 编译测试

使用命令行工具进入```/home/jiy/nRF5_SDK_16.0.0_98a08e2/examples/peripheral/blinky/pca10040/s132/armgcc```目录，这是官方提供的一个闪灯的小例子，在SDK的```examples```目录下还有更加全面的SDK使用案例。

执行```make```命令，你可以看到程序开始编译。

```bash
cd /home/jiy/nRF5_SDK_16.0.0_98a08e2/examples/peripheral/blinky/pca10040/s132/armgcc
make
```

## 烧录

下载安装[nRF Command Line Tools](https://www.nordicsemi.com/Software-and-tools/Development-Tools/nRF-Command-Line-Tools/Download#infotabs)，这个工具用于烧录擦除nRF芯片的```nrfjprog```、合并hex文件的```mergehex```命令，Windows的安装文件中还附带了[SEGGER J-Link software](https://www.segger.com/downloads/jlink/#J-LinkSoftwareAndDocumentationPack)。

下面简单介绍烧录命令，详细文档请输入```nrfjprog --help```命令查看帮助信息：

```bash
# 擦除flash
nrfjprog -f nrf52 --eraseall

# 烧录程序并预先擦除所占位置flash扇区
nrfjprog -f nrf52 --program _build/nrf52832_xxaa.hex --sectorerase

# 重启芯片
nrfjprog -f nrf52 --reset
```

如果你有nrf52832的开发板，在烧录程序并重启之后，就可以看到led闪起来了。

## 调试

### 安装SEGGER J-Link software

如果你是Windows用户，在烧录步骤安装```nRF Command Line Tools```的时候已经安装过[SEGGER J-Link software](https://www.segger.com/downloads/jlink/#J-LinkSoftwareAndDocumentationPack)了，请前往安装目录找到相应的路径。

如果你是Linux或者Mac OS用户，请下载安装[SEGGER J-Link software](https://www.segger.com/downloads/jlink/#J-LinkSoftwareAndDocumentationPack)，并找到路径。

### 安装VS Code插件

在VS Code中搜索插件```C/C++ Extension Pack```并点击安装，这是VS Code的C语言开发扩展，居家旅行必备。

同样的，在VS Code搜索安装```Cortex-Debug```插件，这是一款强大的Arm调试插件。

### 项目配置

使用VS Code打开```/home/jiy/nRF5_SDK_16.0.0_98a08e2/examples/peripheral/blinky```目录，还是刚刚的点灯例子。

创建```.vscode```目录，然后在里面创建```settings.json```文件，配置调试信息：

```json
{
    "cortex-debug.armToolchainPath": "/usr/local/gcc-arm-none-eabi-9-2019-q4-major/bin/",
    "cortex-debug.armToolchainPrefix": "arm-none-eabi",
    "cortex-debug.JLinkGDBServerPath": "/Applications/SEGGER/JLink/JLinkGDBServer"
}
```

请把```cortex-debug.armToolchainPath```和```cortex-debug.JLinkGDBServerPath```对应的内容修改为你电脑上实际的```工具链```和```JLinkGDBServer```的路径。

继续创建```launch.json```文件，写入以下内容：

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "cortex-debug",
            "request": "launch",
            "servertype": "jlink",
            "cwd": "${workspaceRoot}",
            "executable": "pca10040/s132/armgcc/_build/nrf52832_xxaa.out",
            "name": "Cortex Debug",
            "device": "nrf52",
            "interface": "swd"
        }
    ]
}
```

选择VS Code左侧的Debug菜单点击启动按钮，不出意外的话你就可以使用```Cortex-Debug```插件和```GDB```工具开始调试了。
