# Zephyr - BLE 链路地址

```C
/** Bluetooth Device Address */
typedef struct {
	uint8_t  val[6];
} bt_addr_t;

/** Bluetooth LE Device Address */
typedef struct {
	uint8_t      type;
	bt_addr_t a;
} bt_addr_le_t;


int bt_addr_le_from_str(const char *str, const char *type, bt_addr_le_t *addr);
static inline int bt_addr_le_to_str(const bt_addr_le_t *addr, char *str,
				    size_t len);
```

Zephyr 里的 BLE 地址类型只有



[蓝牙协议分析(6)_BLE地址类型](http://www.wowotech.net/bluetooth/ble_address_type.html)