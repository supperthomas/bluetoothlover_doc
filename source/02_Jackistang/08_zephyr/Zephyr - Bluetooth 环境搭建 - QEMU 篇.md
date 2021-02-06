# Zephyr - Bluetooth 环境搭建 - QEMU 篇

本篇文章最终的目标是在 Ubuntu 20.04 上使用 QEMU 来运行 Zephyr 的 Bluetooth 例程。

## 前置条件

- Ubuntu 20.04
- [Zephry 环境](./Zephyr 环境搭建)

## 环境搭建

Zephyr 官方提供了 4 种蓝牙运行的硬件方式：

1. Embedded
2. QEMU with an external Controller
3. Native POSIX with an external Controller
4. Simulated nRF52 with BabbleSim

我们这里搭建的是第二种，运用 QEMU 模拟器来操作外部蓝牙控制器（一般是电脑自带的）。环境搭建好后第三种模式也能直接使用。

### 版本确认

在 Linux 系统里，最常用的是 BlueZ 蓝牙协议栈，搭建环境前确保 Ubuntu 20.04 的 Linux 内核版本和 BlueZ 版本满足要求：

- Linux Kernel 4.10+
- BlueZ 4.45+

可用下述命令查看：

```shell
jackis@jackis-zephyr:~$ uname -a
Linux jackis-zephyr 5.8.0-40-generic #45~20.04.1-Ubuntu SMP Fri Jan 15 11:35:04 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux

jackis@jackis-zephyr:~$ dpkg -s bluez |grep ^Version
Version: 5.53-0ubuntu3
```

### 安装 BlueZ 工具

一般 Linux 系统自带安装了 BlueZ，但可能版本不对，或者工具不齐全，因此最好手动安装一下。

首先安装依赖：

```shell
sudo apt install automake libtool libelf-dev elfutils libdw-dev libjson-c-dev libical-dev libreadline-dev
```

添加 Mesh 支持和嵌入式 Linux 支持的 ell 文件，注意 ell 需要与 bluez 在同一个目录下（git clone 时间大约为 3 分钟）。

```
git clone git://git.kernel.org/pub/scm/libs/ell/ell.git

    .
        |--- ell
        |    |--- ell
        |    `--- unit
        `--- bluez
             |--- src
             `--- tools
```

然后使用下述命令更新协议栈版本或获取所有工具：

```shell
git clone https://github.com.cnpmjs.org/bluez/bluez.git
cd bluez
./bootstrap-configure --disable-android --disable-midi
make
```

这样就能看到工具 `btattach`，`btmgt` 和 `btproxy` 在 `tools/` 目录下，`btmon` 在 `monitor/` 目录下。

### 开启 BlueZ 实验性特点

这是为了访问最新的蓝牙功能。

打开 `/lib/systemd/system/bluetooth.service` 文件，然后在里面找到

```
ExecStart=/usr/libexec/bluetooth/bluetoothd
```

这一行，修改成如下形式

```
ExecStart=/usr/libexec/bluetooth/bluetoothd -E
```

然后重新加载并重启这个守护进程

```shell
sudo systemctl daemon-reload
sudo systemctl restart bluetooth
```

## 例程运行

Zephyr QEMU 能够访问主机的蓝牙控制器，是因为用 `btproxy` 这个工具创建了一个用户态可以访问的 socket，并将蓝牙控制器与该 socket 绑定，这样 QEMU 与该 socket 通信即可控制主机的蓝牙控制器。

### btproxy

开启一个终端，

关闭主机的蓝牙控制器

```
sudo systemctl stop bluetooth
```

使用 `btproxy` 工具打开并监听 UNIX socket，

```
cd ~/bluez
sudo tools/btproxy -u -i 0
 -> Listening on /tmp/bt-server-bredrsudo 
```

其中 `-i 0` 表示使用 hci0，可能需要根据实际情况更换，可以 `hciconfig` 查看：

```
jackis@jackis-zephyr:~$ hciconfig
hci0:	Type: Primary  Bus: USB
	BD Address: 58:A0:23:B6:A4:80  ACL MTU: 1021:4  SCO MTU: 96:6
	UP RUNNING 
	RX bytes:2614 acl:0 sco:0 events:123 errors:0
	TX bytes:1548 acl:0 sco:0 commands:133 errors:2
```

### 例程编译运行

以 beacon 例程为例。

```shell
west build -b qemu_x86 samples/bluetooth/beacon
west build -t run
```

现象如下：

```shell
jackis@jackis-zephyr:~/zephyrproject/zephyr/$ west build -t run
-- west build: running target run
[0/1] To exit from QEMU enter: 'CTRL+a, x'[QEMU] CPU: qemu32,+nx,+pae
SeaBIOS (version rel-1.12.1-0-ga5cab58-dirty-20200625_115407-9426dddc0a1f-zephyr
)
Booting from ROM..*** Booting Zephyr OS build zephyr-v2.4.0-8-g9c30e7946974  ***
Starting Beacon Demo
Bluetooth initialized
Beacon started
[00:00:00.420,000] <inf> bt_hci_core: Identity: 58:a0:23:b6:a4:80 (public)
[00:00:00.420,000] <inf> bt_hci_core: HCI: version 5.0 (0x09) revision 0x0100, manufacturer 0x0002
[00:00:00.420,000] <inf> bt_hci_core: LMP: version 5.0 (0x09) subver 0x0100
```

使用 `CTRL+a, x` 即可退出 QEMU 。

### native_posix 运行

创建 `/tmp/bt-server-bredrsudo` socket 后，

编译运行代码

```shell
west build -b native_posix samples/bluetooth/beacon
sudo ./build/zephyr/zephyr.exe --bt-dev=hci0
```

## 常见问题

### err: bt_hci_core: HCI driver open failed (-16)

这种情况是我们程序退出异常，导致 HCI 驱动打开后没有正常关闭，目前的解决办法是将虚拟机的 BLE 设备还给物理机，然后再次导入虚拟机。

--------

参考：

[Samples and Demos - Bluetooth samples](https://docs.zephyrproject.org/latest/samples/bluetooth/bluetooth.html)

[User and Developer Guides - Bluetooth - Bluetooth tools](https://docs.zephyrproject.org/latest/guides/bluetooth/bluetooth-tools.html#)

[Debian 9.3 编译 Bluez 5.49](https://blog.csdn.net/tonyfield2015/article/details/79668445)