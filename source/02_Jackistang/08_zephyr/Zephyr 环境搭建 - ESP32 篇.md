 # Zephyr 环境搭建 - ESP32 篇

本篇环境搭建的前提是 Zephyr 的基本环境已经搭建好，下述为与 ESP32 相关的环境搭建，最终的结果为使用 `west` 成功编译 `hello_world` 例程并下载到 ESP32 开发板上。Zephyr 基本环境搭建参考 [Zephyr 环境搭建](./Zephyr 环境搭建)。

## 前置条件

- Ubuntu 20.04 (virtualbox on win10)
- Zephyr (v2.4-branch)
- ESP32-DevKitC V4 (WROVER-E)

 ## 环境搭建

### 获取 ESP-IDF

```Shell
mkdir ~/esp
cd ~/esp
git clone -b v4.2 --recursive https://github.com/espressif/esp-idf.git
```

### 安装 xtensa-esp32-elf 工具链

由于 Zephyr SDK 并不支持 ESP32，因此我们需要安装第三方 ESP32 工具链 `xtensa-esp32-elf`，可以手动下载该[工具](https://docs.espressif.com/projects/esp-idf/en/v4.2/esp32/api-guides/tools/idf-tools.html#xtensa-esp32-elf)，这里我选择使用 ESP-IDF 提供的脚本来自动下载工具链。

```shell
cd ~/esp/esp-idf
./install.sh
```

注意此时需要有 python 环境，即

```shell
jackis@jackis-zephyr:~/zephyrproject/zephyr$ python --version
Python 3.8.5
```

若没有则需要手动安装 python 3.8，并[更新 python 执行 python 3.8](https://blog.csdn.net/u014775723/article/details/85213793)， 如下所示

```shell
ln -s /usr/bin/python3.8 /usr/bin/python
```

此时默认安装的工具链在 `$HOME/.espressif` 目录下，建议不要修改工具链的安装路径。

```shell
jackis@jackis-zephyr:~$ ls .espressif/
dist  python_env  tools
```

ESP-IDF 还提供了配置环境变量的脚本文件 `export.sh`，其执行命令为：

```shell
. $HOME/esp/esp-idf/export.sh
```

注意 `.` 和 `$HOME` 之间有空格，该命令在后面会用到。

### 切换 Zephyr 为 v2.4-branch 版本

Zephyr master 分支编译 ESP32 会报错，切换为分支 v2.4-branch 即可，该分支为最新的发布版本。命令如下：

```she
cd ~/zephyrproject/zephyr
git checkout v2.4-branch
```

### 配置 Zephyr 的构建环境变量

此处一共需要配置三个环境变量：

- `ZEPHYR_TOOLCHAIN_VARIANT`：用于构建 Zephyr 当前工具链的名称。
- `ESPRESSIF_TOOLCHAIN_PATH`：espressif 工具链的路径。
- `ESP_IDF_PATH`：git clone [esp-idf](###获取 ESP-IDF) 的路径。

在配置环境变量前需运行 ESP-IDF 的脚本文件 export.sh，完整命令如下：

```shell
. ~/esp/esp-idf/export.sh
export ZEPHYR_TOOLCHAIN_VARIANT=espressif
export ESPRESSIF_TOOLCHAIN_PATH=${HOME}/.espressif/tools/xtensa-esp32-elf/esp-2020r3-8.4.0/xtensa-esp32-elf
export ESP_IDF_PATH=${IDF_PATH}
```

此处需要注意 `ESPRESSIF_TOOLCHAIN_PATH` 环境变量里的工具链路径一定要是系统里安装的工具链真实路径，该工具链版本不一致时该路径也会不一致。

### 编译下载

此处编译例程 hello_world，请确保 zephyr 目录下没有 build 子目录，否则会报错。

```shel
cd ~/zephyrproject/zephyr
west build -b esp32 samples/hello_world
west flash
```

将物理机的 [USB](./Virtualbox 安装 Ubuntu 20.04.md) 转串口接入虚拟机。

由于 ESP32 下载程序通常使用串口下载，因此 `west flash` 需要能访问 ubuntu 的串口，普通用户不能直接操作串口，需要将当前用户添加到串口设备所属的组中。

首先查看 `/dev/ttyUSB0` 的权限

```shell
jackis@jackis-VirtualBox:~/zephyrproject/zephyr$ ls -l /dev/ttyUSB0
crw-rw---- 1 root dialout 188, 0 Jan 26 16:52 /dev/ttyUSB0
```

- 所有者：root，可读可写
- 所属组：dialout，可读可写
- 其他用户：无权限

修改 udev 规则，让普通用户也能使用串口

```shell
sudo vi /etc/udev/rules.d/70-ttyusb.rules
```

添加下述内容，

```shell
KERNEL=="ttyUSB[0-9]*",MODE="0666"
```

然后重新插入 USB 转串口即可。

按住 ESP32 的 boot 按钮，输入 `west flash` 下载程序，松开 boot 按钮即可开始下载程序。

用 `minicom -D /dev/ttyUSB0` 打开串口观察到数据。

```shell
rst:0x1 (POWERON_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)
configsip: 0, SPIWP:0xee
clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
mode:DIO, clock div:2
load:0x3ffb0000,len:116
load:0x3ffb0074,len:140
load:0x3ffb0100,len:704
load:0x40080000,len:1024
load:0x40080400,len:72
load:0x40080448,len:256
load:0x40080548,len:13132
entry 0x400807b0
*** Booting Zephyr OS build zephyr-v2.4.0-8-g9c30e7946974  ***
Hello World! esp32
```

参考：

[Zephyr Supported Boards - ESP32](https://docs.zephyrproject.org/latest/boards/xtensa/esp32/doc/index.html)

[ESP32 Toolchain - xtensa-esp32-elf](https://docs.espressif.com/projects/esp-idf/en/v4.2/esp32/api-guides/tools/idf-tools.html#xtensa-esp32-elf)

[Zephyr Issues - Setting esp-idf path to match Espressif's documentation](https://github.com/zephyrproject-rtos/zephyr/issues/24844)

[ubuntu安装python3.7，并更新python默认指向为python3.7](https://blog.csdn.net/u014775723/article/details/85213793)