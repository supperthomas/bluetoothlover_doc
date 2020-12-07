# BLE_Advertising

本节内容介绍了 mbed os 里 BLE_Advertising 例程里关于打广播的内容。尽可能地从宏观上去了解 mbed os 里 BLE 协议栈是如何打广播的，因此需要充分理解函数名，变量名等与 BLE 广播之间的联系。关于细节部分以后再添加。

## example 介绍

### BatteryDemo 接口

BatteryDemo 类声明里 public 类型的成员只有一个构造函数和一个 `start()` 方法，因此接口就只有 `start()`，可以在 main 函数里看见创建一个 BatteryDemo 对象后就直接调用了 `start()` 方法。

```C
void start()
{
    /* mbed will call on_init_complete when when ble is ready */
    _ble.init(this, &BatteryDemo::on_init_complete);

    /* this will never return */
    _event_queue.dispatch_forever();
}
```

第 4 行初始化 BLE 协议栈，通过注释可以知道 BLE 协议栈初始化完成后会调用 `on_init_complete` 这个成员函数。第 7 行涉及到 mbed os 里的事件机制，我还没弄懂，而且这对我们理解 BLE 没有影响，在这里就不介绍了。

### on_init_complete

```C
/** Callback triggered when the ble initialization process has finished */
void on_init_complete(BLE::InitializationCompleteCallbackContext *params)
{
    if (params->error != BLE_ERROR_NONE) {
        print_error(params->error, "Ble initialization failed.");
        return;
    }

    print_mac_address();

    start_advertising();
}
```

这个函数首先打印了设备的 mac 地址，这个地址可以在抓包的时候用于过滤使用。

之后就开始打广播了。

### start_advertising

这个函数里内容挺多的，可以分成设置广播参数、设置广播数据、设置扫描回复数据、开始广播这四个部分。

#### 设置广播参数

```C
/* create advertising parameters and payload */

ble::AdvertisingParameters adv_parameters(
    /* you cannot connect to this device, you can only read its advertising data,
             * scannable means that the device has extra advertising data that the peer can receive if it
             * "scans" it which means it is using active scanning (it sends a scan request) */
    ble::advertising_type_t::SCANNABLE_UNDIRECTED,
    ble::adv_interval_t(ble::millisecond_t(1000))
);

ble_error_t error = _ble.gap().setAdvertisingParameters(
    ble::LEGACY_ADVERTISING_HANDLE,
    adv_parameters
);

if (error) {
    print_error(error, "_ble.gap().setAdvertisingParameters() failed");
    return;
}
```

这里设置了一个广播参数 `adv_parameters`，其中广播包类型为 `SCANNABLE_UNDIRECTED` ，即可扫描、不定向包，也就是 ADV_SCAN_IND 这个包。然后又设置了发送间隔时间为 1000ms 。

之后将该广播参数通过 `_ble.gap().setAdvertisingParameters` 设置到 BLE 协议栈里。

#### 设置广播数据

```C
_adv_data_builder.setFlags();
_adv_data_builder.setName(DEVICE_NAME);

/* we add the battery level as part of the payload so it's visible to any device that scans */
_adv_data_builder.setServiceData(GattService::UUID_BATTERY_SERVICE, {&_battery_level, 1});

error = _ble.gap().setAdvertisingPayload(
    ble::LEGACY_ADVERTISING_HANDLE,
    _adv_data_builder.getAdvertisingData()
);

if (error) {
    print_error(error, "_ble.gap().setAdvertisingPayload() failed");
    return;
}
```

在 BatteryDemo 类里定义了一个私有成员 `ble::AdvertisingDataBuilder _adv_data_builder;` ，通过名字可以看出用于构建广播数据包。

然后开始构建广播数据包，也就是那 31 个字节。

- 调用 `setFlags()` ，
  - 此时是在构建 AD Type 为 0x01 - «Flags» 的 AD Structure ，
  - 其 AD Data 默认为 `BREDR_NOT_SUPPORTED | LE_GENERAL_DISCOVERABLE` ，
  - Length 字段会自动设置。
- 调用 `setName()`，
  - 此时是在构建 AD Type 为 0x09 - «Complete Local Name» 的 AD Structure，
  - 其 AD Data 为 `DEVICE_NAME` ，在文件最开始处有定义 `const static char DEVICE_NAME[] = "BATTERY";` ，
  - Length 字段会自动设置。
- 调用 `setServiceData()`，
  - 此时是在构建 AD Type 为 0x16 - «Service Data» 的 AD Structure，
  - 其 AD Data 包括 Service UUID 和 Service Data。Service UUID 为 `GattService::UUID_BATTERY_SERVICE` ，也就是 0x180F ，Service Data 就是一个字节的电量 `_battery_level` 。
  - Length 字段会自动设置。

之后通过 `_ble.gap().setAdvertisingPayload` 设置广播包（此处为 ADV_SCAN_IND）的负载数据。

#### 设置扫描回复数据

```C
/* when advertising you can optionally add extra data that is only sent
         * if the central requests it by doing active scanning */
_adv_data_builder.clear();
const uint8_t _vendor_specific_data[4] = { 0xAD, 0xDE, 0xBE, 0xEF };
_adv_data_builder.setManufacturerSpecificData(_vendor_specific_data);

_ble.gap().setAdvertisingScanResponse(
    ble::LEGACY_ADVERTISING_HANDLE,
    _adv_data_builder.getAdvertisingData()
);
```

首先用 `clear()` 清空广播包数据。

调用 `setManufacturerSpecificData()` 构建 AD Structure:

- AD Type 为 0xFF - «Manufacturer Specific Data»
- AD Data 为 `_vendor_specific_data`，在上面有定义，Company ID 为 0xdead，Data 为 0xbeef 。
- Length 字段协议栈自动填充。

然后调用 `_ble.gap().setAdvertisingScanResponse` 设置扫描回复包（SCAN_RSP）的负载数据。

#### 开始广播

```C
/* start advertising */

error = _ble.gap().startAdvertising(ble::LEGACY_ADVERTISING_HANDLE);

if (error) {
    print_error(error, "_ble.gap().startAdvertising() failed");
    return;
}

/* we simulate battery discharging by updating it every second */
_event_queue.call_every(
    1000ms,
    [this]() {
        update_battery_level();
    }
);
```

上述代码就正式开启了广播，同时还定义了每秒执行 `update_battery_level()` 函数的事件。

### update_battery_level

```C
void update_battery_level()
{
    if (_battery_level-- == 10) {
        _battery_level = 100;
    }

    /* update the payload with the new value */
    ble_error_t error = _adv_data_builder.setServiceData(GattService::UUID_BATTERY_SERVICE, make_Span(&_battery_level, 1));

    if (error) {
        print_error(error, "_adv_data_builder.setServiceData() failed");
        return;
    }

    /* set the new payload, we don't need to stop advertising */
    error = _ble.gap().setAdvertisingPayload(
        ble::LEGACY_ADVERTISING_HANDLE,
        _adv_data_builder.getAdvertisingData()
    );

    if (error) {
        print_error(error, "_ble.gap().setAdvertisingPayload() failed");
        return;
    }
}
```

在该函数里，模拟电量每秒减 1，减到 10 时又回到 100，如此往复。

然后又构建了 «Service Data» 的广播包，使用更新过的电量作为 Service Data 。重新设置广播负载数据。

注意之前设置的 «Manufacturer Specific Data» 数据没有在 `_adv_data_builder` 里清空，所以在发送的 ADV_SCAN_IND 的广播包里也能看到 «Manufacturer Specific Data» 这个 AD Structure 。

## mbedos_ble_advertising 抓包文件分析

![](images/image-20201202185438185.png)

可以看见 WB55 周期性的在发送 ADV_SCAN_IND 的包，里面有两个 AD Structure ，其中一个是 Service Data 的类型的包，AD Data 包括 0x180f（Battery Service UUID）和 0x26（电量）。

![](images/image-20201202185756693.png)

当手机端开启扫描模式后，会发现 WB55 发送了 ADV_SCAN_RSP 的包，里面包含了一个 AD Structure，AD Type 为 0xff（Manufacturer Specific）。

WB55 在上电复位的时候也会发送一个广播包，有 3 个 AD Structure ，但那个包我没抓到，就没有写。

## ble::AdvertisingDataBuilder

TODO

## mbed::Span

TODO