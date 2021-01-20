# RTTHREAD贡献TODO目录

这边简单想一下RTTHREAD做贡献可能可以做的事情。

## 提交还没有板子的BSP

如果你手上有开发板RTTHREAD还完全没有的时候，可以提交对应的软件包。

## 提交外设驱动

如果发现某个bsp，有某个外设驱动没有porting的，可以提交维护一部分driver

例如，SPI, IIC, CAN, GPIO, ADC, DAC

## 提交软件包

发现一个比较好的开源软件包，可以移植到RTT的软件包的列表里面，可以提交对应的软件包

## 维护某个软件包里面的比较常用的sample

软件包里面的功能进行维护或者添加sample等。

## 参与社区其他工作

参加提交社区项目的相关文档。

## 动态加载

https://www.rt-thread.org/document/site/programming-manual/dlmodule/dlmodule/





## 具体相关事项

###  抓包btsnoopy研究

1. art-pi上实现抓btsnoopy包，并用menuconfig来进行配置
2. btsnoopy包内部抓包情况解析
3. 如何实现用mcu直接HCI uart抓包



##  BLE PROFILE研究

1. art-pi上实现心率服务的example 并成功用手机连接，并抓到相应的btsnoopy包进行分析讲解
2. 完善art-pi上面btstack的menuconfig选项的配置。
   - UART_DEVCIE可以选择像console一样
   - chipset可以选择
   - uart工作波特率可以选择
   - 蓝牙地址可以选择修改
   - firmware文件路径可以选择修改
   - 选择哪一个sample
   - bt_disable_pin可以选择哪个pin脚
3. 

