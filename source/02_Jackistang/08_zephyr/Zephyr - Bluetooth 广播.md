int `bt_enable`([bt_ready_cb_t](https://docs.zephyrproject.org/latest/reference/bluetooth/gap.html#c.bt_ready_cb_t)*cb*)

Enable Bluetooth.

Enable Bluetooth. Must be the called before any calls that require communication with the local Bluetooth hardware.

- **Return**

  Zero on success or (negative) error code otherwise.

- **Parameters**

  `cb`: Callback to notify completion or NULL to perform the enabling synchronously.



## API

### bt_enable

```C
typedef void (*bt_ready_cb_t)(int err);

int bt_enable(bt_ready_cb_t cb);
```

`bt_enable` 用于初始化 bluetooth 协议栈。

- **返回值**：
  - 0 表示成功，或者一个错误码（负数）。
- **参数**：
  - `cb` ：一个 `bt_ready_cb_t` 类型的函数指针，协议栈初始化完成后会回调 `cb` ，并传入结果 `err` （0 表示成功，负的错误码表示失败），此时 `bt_enable` 立即返回（异步）；若传入 NULL 则该函数在协议栈初始化完成后返回（同步）。

### bt_le_adv_start

```C
int bt_le_adv_start(const struct bt_le_adv_param *param,
		    const struct bt_data *ad, size_t ad_len,
		    const struct bt_data *sd, size_t sd_len)
```

开启广播，并同时设置广播数据和扫描回复数据。

- **返回值**：
  - 0 表示成功，负的错误码表示失败。
  - 错误码含义参考：[bt_le_adv_start](https://docs.zephyrproject.org/latest/reference/bluetooth/gap.html#group__bt__gap_1gad2e3caef88d52d720e8e4d21df767b02) 。

- **参数**：
  - `param`：广播参数，表明该广播的类型，传统广播 or 扩展广播，可连接 or 定向 or 可扫描。
  - `ad`, `ad_len`：广播数据，是一个 `bt_data` 类型的数据，用 `BT_DATA` 宏可快速构成。
  - `sd`, `sd_len` : 扫描回复数据。