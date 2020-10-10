# STM32WB简介

## 架构和外设

### 什么是STM32WB？

![1-1](doc/1-1.png)

STM32WB MCU系列采用与超低功耗[STM32L4](https://www.st.com/zh/microcontrollers-microprocessors/stm32l4-series.html)微控制器相同的开发技术，提供相同的数字和模拟外设，适用于需要延长电池寿命和复杂功能的应用。

- STM32WBx5无线微控制器（有多种封装和不同的内存大小可选），为用户提供了增强的性能和灵活性，以应对不同级别的复杂性。
- STM32WBx0超值系列侧重于基本配置，为开发人员提供功能优化且经济划算的解决方案。

### 关于STM32WB

![1-2](doc/1-2.png)

STM32WB无线微控制器基于运行于64 MHz的Arm® Cortex®‐M4核心（应用处理器）和运行于32 MHz的Arm® Cortex®‐M0+核心（网络处理器），支持Bluetooth™ 5.0和IEEE 802.15.4无线标准（比如ZigBee 3.0和OpenThread）。

两个完全独立的核心使该创新型架构针对实时执行（与无线电相关的软件处理）进行了优化，依靠灵活的资源使用和电源管理，实现了更低的BOM成本和更好的用户体验。

- [STM32WBx5系列](https://www.st.com/content/st_com/zh/products/microcontrollers-microprocessors/stm32-32-bit-arm-cortex-mcus/stm32-wireless-mcus/stm32wb-series/stm32wbx5.html)具有很多种通信功能，包括实用的无晶振USB 2.0 FS接口、音频支持、LCD驱动、触摸感应、多达72个GPIO、用于优化功耗的集成SMPS和多种低功耗模式以最大限度地延长电池寿命。
- [STM32WBx0 超值系列](https://www.st.com/content/st_com/zh/products/microcontrollers-microprocessors/stm32-32-bit-arm-cortex-mcus/stm32-wireless-mcus/stm32wb-series/stm32wbx0-value-line.html)面向入门级解决方案，提供基本的外设组合降低了温度范围。

该产品系列使STM32生态系统趋于完整，提供了从产品定义到原型设计阶段，再到最终平台定义的全面灵活性。

### 为何选择双核？

STM32WB采用双核结构，Cortex®‐M4用于应用处理，Cortex®‐M0用于协议栈处理。

![1-3](doc/1-3.png)

- 用户无需管理Cortex®‐M0（协议栈部分），节省开发时间
- 应用于协议栈分开更利于实时性处理，方便调试
- Cortex®‐M4与Cortex®‐M0分开更便于低功耗处理

## 连接能力

### 通信技术概览

![1-4](doc/1-4.png)

STM32WB应用于低功耗、低速率，短距离应用场景

### 多协议和开放射频

![1-5](doc/1-5.png)



### BLE+Thread多协议并发

![1-6](doc/1-6.png)

### STM32WB多协议占用

![1-7](doc/1-7.png)

用户需关注最新协议栈发布大小

**注意：用户如果使用OTA形式更新协议栈，需要在Cortex®‐M4管理内存区保留一份协议栈空间用作备份协议栈，大小与协议栈大小相同**

## 安全和低功耗

### 软件安全架构

![1-8](doc/1-8.png)

内存空间分为安全区与非安全区，使得整体架构更安全

### STM32W的攻击防御措施

STM32WB同时提供多种攻击防御措施。

![1-9](doc/1-9.png)



### 应用固件更新

![1-10](doc/1-10.png)

### 多种低功耗模式

STM32WB同时实现了多种低功耗模式，增加了电源管理的灵活性

![1-11](doc/1-11.png)

**注意：如果需要保存RF功能，系统不能进入不带RAM保持的STANDBY模式**

## 生态

### 硬件开发工具

![1-12](doc/1-12.png)

开发板布局如下

![1-13](doc/1-13.png)

![1-14](doc/1-14.png)

![1-15](doc/1-15.png)

### 协议栈版本查看

![1-16](doc/1-16.png)

除此两种方法还可以使用[STM32CubeProgrammer](https://www.st.com/content/st_com/zh/products/development-tools/software-development-tools/stm32-software-development-tools/stm32-programmers/stm32cubeprog.html)软件进行查看与更新固件，使用GUI图形化更利于操作。

### 协议栈版本更新

![1-17](doc/1-17.png)

**注意：升级不能跨版本，也不能降级**

### 软件开发工具

![1-18](doc/1-18.png)

所有ST软件都可在[STM中文官网](https://www.st.com/content/st_com/zh.html)下载

#### CubeMX

![1-19](doc/1-19.png)



![1-20](doc/1-20.png)

#### STM32CubeMonitor-RF

![1-21](doc/1-21.png)



![1-22](doc/1-22.png)

### 智能手机软件

![1-23](doc/1-23.png)