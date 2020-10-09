# Client and Server relationship in GATT
GATT 通信的双方是 C/S 关系。

外设作为 GATT 服务端（Server），它维持了 ATT 的查找表以及 service 和 characteristic 的定义。

中心设备是 GATT 客户端（Client），它向 Server 发起请求。

需要注意的是，所有的通信事件，都是由客户端（也叫主设备，Master）发起，并且接收服务端（也叫从设备，Slave）的响应。

