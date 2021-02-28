# Zephyr - native_posix 运行 socket 例程

native_posix 是 Zephyr 提供的一种使用方式，基于 POSIX 兼容层，它将应用程序与 Zephyr 内核编译成了操作系统里的可执行文件，这样可以使用操作系统平台的 gdb 或其他调试工具调试，十分方便，详细介绍参见：[Native POSIX execution (native_posix)](https://docs.zephyrproject.org/latest/boards/posix/native_posix/doc/index.html#native-posix)。

下面开始介绍如何在 native_posix 上运行 echo_server 例程，需要安装哪些环境。

## 基础环境

- Ubuntu 20.04
- Zephyr

## 下载 Zephyr 的网络工具包

```
git clone https://github.com.cnpmjs.org/zephyrproject-rtos/net-tools.git
```

## 例程运行

运行此例程需打开三个终端：

- 终端1：进入 net-tools 目录（`cd net-tools`）
- 终端2：与通常的应用开发一样，在 Zephry 工程的根目录
- 终端3：连接 Zephyr native_posix 实例（可选）

### 步骤1 - 创建以太网接口

在终端 1 里输入：

```
./net-setup.sh
```

### 步骤2 - 在 native_posix 环境下运行应用程序

在终端 2 里输入：

```
west build -b native_posix samples/net/sockets/echo_server
west build -t run
```

### 步骤3 - 连接网络终端（可选）

在步骤 2 运行应用程序时，会打印出一条类似下述的信息：

```
UART connected to pseudotty: /dev/pts/5
```

注意其中的 `/dev/pts/5`，然后我们就可以使用下述命令连接网络终端

```
screen /dev/pts/5
```

-----

参考：

[Networking with native_posix board](https://docs.zephyrproject.org/latest/guides/networking/native_posix_setup.html#networking-with-native-posix)

[Native POSIX execution (native_posix)](https://docs.zephyrproject.org/latest/boards/posix/native_posix/doc/index.html#native-posix)