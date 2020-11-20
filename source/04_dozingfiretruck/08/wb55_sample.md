# wb55_sample演示

## 前言

前文提过stm32wb55官方软件包，里面有许多demo，本文会选取一些sample进行演示。

## BLE_Beacon演示

### 运行要求

该应用程序需要无线协处理器上运行STM32WB5X_BLE_STACK_FULL_FW.bin二进制文件。
如果固件不是STM32WB5X_BLE_STACK_FULL_FW.bin，则需要使用STM32CubeProgramme刷写固件。刷写过程见前文STM32WB环境搭建。

### 刷写过程

工程在软件包STM32CubeWB\Projects\P-NUCLEO-WB55.Nucleo\Applications\BLE\BLE_Beacon目录下，打开工程编译下载重启开发版。

### 历程验证

手机打开Beacon Scanner ，可看到相关信息。![](doc/beacon.jpg)

## BLE_BloodPressure演示

### 运行要求

该应用程序需要无线协处理器上运行STM32WB5X_BLE_STACK_FULL_FW.bin二进制文件。
如果固件不是STM32WB5X_BLE_STACK_FULL_FW.bin，则需要使用STM32CubeProgramme刷写固件。刷写过程见前文STM32WB环境搭建。

### 刷写过程

工程在软件包STM32CubeWB\Projects\P-NUCLEO-WB55.Nucleo\Applications\BLE\BLE_BloodPressure目录下，打开工程编译下载重启开发版。

### 历程验证

手机打开ST BLE Profile 连接BPSTM设备，可看到相关信息。

![](doc/BLE_BloodPressure.jpg)

## BLE_HealthThermometer演示

### 运行要求

该应用程序需要无线协处理器上运行STM32WB5X_BLE_STACK_FULL_FW.bin二进制文件。
如果固件不是STM32WB5X_BLE_STACK_FULL_FW.bin，则需要使用STM32CubeProgramme刷写固件。刷写过程见前文STM32WB环境搭建。

### 刷写过程

工程在软件包STM32CubeWB\Projects\P-NUCLEO-WB55.Nucleo\Applications\BLE\BLE_HealthThermometer目录下，打开工程编译下载重启开发版。

### 历程验证

手机打开ST BLE Profile连接设备HTSTM ，可看到相关信息。

![](doc/BLE_HealthThermometer.jpg)

## BLE_HeartRate演示

### 运行要求

该应用程序需要无线协处理器上运行STM32WB5X_BLE_STACK_FULL_FW.bin二进制文件。
如果固件不是STM32WB5X_BLE_STACK_FULL_FW.bin，则需要使用STM32CubeProgramme刷写固件。刷写过程见前文STM32WB环境搭建。

### 刷写过程

工程在软件包STM32CubeWB\Projects\P-NUCLEO-WB55.Nucleo\Applications\BLE\BLE_HeartRate目录下，打开工程编译下载重启开发版。

### 历程验证

手机打开ST BLE Sensor 连接设备HRSTM ，可看到相关信息。

![](doc/BLE_HeartRate1.jpg)

手机打开ST BLE Profile连接设备HRSTM ，可看到相关信息。

![](doc/BLE_HeartRate2.jpg)

## BLE_Ota演示

### 运行要求

该应用程序需要无线协处理器上运行STM32WB5X_BLE_STACK_FULL_FW.bin二进制文件。
如果固件不是STM32WB5X_BLE_STACK_FULL_FW.bin，则需要使用STM32CubeProgramme刷写固件。刷写过程见前文STM32WB环境搭建。

### 刷写过程

工程在软件包STM32CubeWB\Projects\P-NUCLEO-WB55.Nucleo\Applications\BLE\BLE_Ota目录下，打开工程编译下载重启开发版。

### 历程验证

手机打开ST BLE Sensor 连接设备STM_OTA。

![](doc/BLE_Ota1.jpg)

![](doc/BLE_Ota2.jpg)

之后点击SELECT FILE选择OTA的bin文件，这里用BLE_HeartRate_ota进行展示，bin文件在STM32CubeWB\Projects\P-NUCLEO-WB55.Nucleo\Applications\BLE\BLE_HeartRate_ota\Binary目录下，因程序起始在 0x0800 7000所以地址我们填写0x7000

![](doc/BLE_Ota3.jpg)

点击下载等待结束

![BLE_Ota4](doc/BLE_Ota4.jpg)

之后自动重启，设备搜索显示HRSTM证明OTA成功

![](doc/BLE_Ota5.jpg)

点击验证效果正常

![](doc/BLE_Ota6.jpg)

至此OTA结束。