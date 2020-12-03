# mbed-os LEDDemo 介绍

## mbed-os如何定义一个 GATT Service

根据对 GATT 的理解，一个 GATT Service 包含多个 Characteristic ，Service 和 Characteristic 都有自己的 UUID 来标识，如下图所示：

<img src="images/image-20201203224720869.png" alt="image-20201203224720869" style="zoom:50%;" />

### GattCharacteristic 

在 mbed-os 里 `GattCharacteristic` 类用来表示 Characteristic 。

为了方便使用，mbed-os 根据对 Characteristic 的读/写属性提供了几个更方便使用的类：

- `ReadOnlyGattCharacteristic`
- `WriteOnlyGattCharacteristic`
- `ReadWriteGattCharacteristic`
- `WriteOnlyArrayGattCharacteristic`
- `ReadOnlyArrayGattCharacteristic`
- `ReadWriteArrayGattCharacteristic`

TODO: 解释带 "Array" 的 Characteristic 。

这些类都是模板类，可以很方便地实现任意类型的 Characteristic Value 值。

#### LEDService

以 mbed-os-example-ble-LED 例程里实现的 LEDService 为例。

先从 Characteristic 介绍：

```C++
class LEDService {
public:
	const static uint16_t LED_STATE_CHARACTERISTIC_UUID = 0xA001;
    ......
private:
    ReadWriteGattCharacteristic<bool> ledState; 
};
```

LEDService 定义了一个 `ReadWriteGattCharacteristic<bool>` 类型的 Characteristic `ledState`，`ledState` 可读可写。 true 表示灯亮状态，false 表示灯灭状态， UUID 自定义为 0xA001 。

### GattService

接下来看看这个 demo 里如何定义一个 GATT Service 。

```C++
class LEDService {
public:
    const static uint16_t LED_SERVICE_UUID              = 0xA000;
    const static uint16_t LED_STATE_CHARACTERISTIC_UUID = 0xA001;

    LEDService(BLEDevice &_ble, bool initialValueForLEDCharacteristic) :
        ble(_ble), ledState(LED_STATE_CHARACTERISTIC_UUID, &initialValueForLEDCharacteristic)
    {
        GattCharacteristic *charTable[] = {&ledState};
        GattService         ledService(LED_SERVICE_UUID, charTable, sizeof(charTable) / sizeof(GattCharacteristic *));

        ble.gattServer().addService(ledService);
    }

    GattAttribute::Handle_t getValueHandle() const
    {
        return ledState.getValueHandle();
    }

private:
    BLEDevice                         &ble;
    ReadWriteGattCharacteristic<bool> ledState; 
};
```

在 LEDService 的构造函数初始化列表里，得到了传入的 BLE 协议栈实例的引用，并且根据 Characteristic 的 UUID 和初始状态值构造了 `ledState` 。

此处的 `BLEDevice` 是为了兼容较老版本的协议栈，新版本协议栈不建议使用，直接使用 `BLE` 即可。官方解释如下：

```C++
/**
 * @deprecated This type alias is retained for the sake of compatibility with
 * older code. This will be dropped at some point.
 */
typedef BLE BLEDevice;
```

第 9，10 行构建了一张 GattCharacteristic 的表，并且用这张表和 UUID 构建了 GATT Service `ledService`，之后就调用接口 `addService()` 将 `ledService` 作为一个 Service 加入了协议栈。

注意，`addService()` 会为 Service 里的所有 attributes 统一分配 Handle 句柄，因此我们编写程序时想要获得一个 attribute 的句柄，只能调用协议栈提供的接口。就比如获取 `ledState` Characteristic Value 的 Handle 句柄，就只能调用 `ledState.getValueHandle();` 来获得，返回类型是 `GattAttribute::Handle_t` 。

## LEDDemo 介绍

TODO

