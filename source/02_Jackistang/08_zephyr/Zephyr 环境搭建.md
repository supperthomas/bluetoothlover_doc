# Zephyr 环境搭建

我这里 Zephyr 环境搭建在 Ubuntu 20.04 上，Ubuntu 运行在 virtualbox 虚拟机中。

## 前置条件

- Ubuntu 20.04 (virtualbox on win10)

## 环境搭建

首先输入

```shell
sudo apt update
sudo apt upgrade
```

`sudo apt upgrade` 第一次更新的时候可能会失败，再输入一次即可。

### 安装依赖包

需要使用 `apt` 来安装依赖包，最好使用国内源。

```shell
sudo apt install --no-install-recommends git cmake ninja-build gperf \
  ccache dfu-util device-tree-compiler wget \
  python3-dev python3-pip python3-setuptools python3-tk python3-wheel xz-utils file \
  make gcc gcc-multilib g++-multilib libsdl2-dev
```

然后需要检查 cmake 的版本，需要 3.13.1 及以上的版本。

```shell
cmake --version
```

若版本较低，则需要手动更新 cmake 版本，参考[官方手册](https://docs.zephyrproject.org/latest/getting_started/index.html#install-dependencies)。Ubuntu 20.04 一般不会有这个问题。

### 获取 Zephyr 并安装 Python 依赖

1. 安装 `west` Python 脚本工具，并将 `~/.local/bin` 加入 PATH 环境变量。

```shell
pip3 install --user -U west -i https://mirrors.aliyun.com/pypi/simple/
echo 'export PATH=~/.local/bin:"$PATH"' >> ~/.bashrc
source ~/.bashrc
```

这里的 `-i https://mirrors.aliyun.com/pypi/simple/` 表示使用国内源安装。

2. 然后获取 Zephyr 源代码，

```shell
west init ~/zephyrproject -m https://gitee.com/AnswerInTheWind/zephyr/ 
cd ~/zephyrproject
west update
```

这里 `west init` 使用了参数 `-m https://gitee.com/AnswerInTheWind/zephyr/`， 表明从 gitee 上下载源代码，速度更快，而且该仓库已经修改了 `west.yml` 文件，将依赖的模块文件也全部从 github 导向了 gitee，这样在国内安装速度也会很快。

最后使用 `west update` 安装依赖模块。

3. 导出 Zephyr CMake 包，

```shell
west zephyr-export
```

4. 安装 python 依赖环境

```shell
pip3 install --user -r ~/zephyrproject/zephyr/scripts/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

可能会安装失败，多安装几次就会。

### 安装工具链

1. 下载  Zephyr SDK 安装工具

```shell
cd ~
wget https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.11.4/zephyr-sdk-0.11.4-setup.run
```

若嫌速度太慢，可以从企业网盘里下载，然后通过虚拟机共享文件夹到 Ubuntu 。

2. 运行安装工具，将 SDK 安装到 `~/zephyr-sdk-0.11.4`

```shell
chmod +x zephyr-sdk-0.11.4-setup.run
./zephyr-sdk-0.11.4-setup.run -- -d ~/zephyr-sdk-0.11.4
```

3. 建立 udev 规则，允许普通用户下载程序到 Zephyr 支持的大部分开发板。

```shell
sudo cp ~/zephyr-sdk-0.11.4/sysroots/x86_64-pokysdk-linux/usr/share/openocd/contrib/60-openocd.rules /etc/udev/rules.d
sudo udevadm control --reload
```

### 编译下载

使用 samples/hello_world 来测试环境是否搭建成功。

```shell
cd ~/zephyrproject/zephyr
west build -p auto -b qemu_x86 samples/hello_world
west build -t run
```

运行结果如下：

```shell
jackis@jackis-zephyr:~/zephyrproject/zephyr$ west build -t run -d build/qemu_x86/hello_world
-- west build: running target run
[0/1] To exit from QEMU enter: 'CTRL+a, x'[QEMU] CPU: qemu32,+nx,+pae
SeaBIOS (version rel-1.12.1-0-ga5cab58-dirty-20200625_115407-9426dddc0a1f-zephyr
)
Booting from ROM..*** Booting Zephyr OS build zephyr-v2.4.0-8-g9c30e7946974  ***
Hello World! qemu_x86
```



-----



参考：

[搭建zephyr开发环境](https://supperthomas-wiki.readthedocs.io/en/latest/09_answerinthewind/03_zephyr/zephyr_env.html)

