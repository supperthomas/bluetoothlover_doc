

# BLE 协议栈初始化

## bt_enable

```C
typedef void (*bt_ready_cb_t)(int err);

int bt_enable(bt_ready_cb_t cb);
```

`bt_enable` 用于初始化 bluetooth 协议栈。

- **返回值**：
  - 0 表示成功，或者一个错误码（负数）。
  
- **参数**：

  - `cb` ：一个 `bt_ready_cb_t` 类型的函数指针。


`bt_enable` 函数有**同步**和**异步**两种行为，

- 异步：若传入的 `cb` 不为 NULL，则该函数立即返回，等待协议栈初始化完成后回调 `cb` 指向的函数，并且将协议栈初始化结果 `err` 作为参数传递。
- 同步：若传入的 `cb` 为 NULL，则该函数会在协议栈初始化完成后才返回，并返回协议栈初始化结果。
