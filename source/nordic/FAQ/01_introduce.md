# Nordic FAQ

### 1. 如何修改Nordic的蓝牙mac地址

```
API:sd_ble_gap_addr_set
```

如何修改：

```
  ble_gap_addr_t local_addr;
        
   ret_code_t  err_code = sd_ble_gap_addr_get(&local_addr);
   NRF_LOG_INFO("LOCAL ADDRESS:%x:%x:%x:%x:%x:%x",local_addr.addr[0],local_addr.addr[1],local_addr.addr[2],local_addr.addr[3],local_addr.addr[4],local_addr.addr[5] );
   APP_ERROR_CHECK(err_code);

// Increase the BLE address by one when advertising openly.
    local_addr.addr[0] = 0x01;
    local_addr.addr[1] = 0x02;
    local_addr.addr[2] = 0x03;
    local_addr.addr[3] = 0x04;
    local_addr.addr[4] = 0x05;
    //local_addr.addr[5] = 0x06; the addr[5] couldn't changed easy
   err_code = sd_ble_gap_addr_set(&local_addr);
   APP_ERROR_CHECK(err_code);
```



## 2. 