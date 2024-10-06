# HFP 

本文基于HFP1.9 pdf，以及一些cfa和ellisys讲解

## 简介

  HFP(Hands-free Profile)，可以让蓝牙设备可以控制电话，如接听、挂断、拒接、语音拨号等，拒接、语音拨号要视蓝牙耳机及电话是否支持。

HFP定义了音频[网关](http://baike.baidu.com/view/807.htm)(Audio Gateway)和免提组件(Hands Free)两个角色：

**AG**–该设备为音频（特别是手机）的输入/输出网关。通常指的是手机

**HF**–该设备作为音频[网关](http://baike.baidu.com/view/807.htm)的远程音频输入/输出机制，并可提供若干遥控功能。通常指的是耳机或者其他免提设备。



| 章节                           | 大概内容            | 备注                      |
| ------------------------------ | ------------------- | ------------------------- |
| 1  Introduce                   | 介绍                | 仔细看完，                |
| 2 Porfile overview             | Profile 大概内容    | 仔细看完，                |
| 3 application layer            | AG和HF需要的feature | 略看                      |
| 4 Hands-Free Control           | AT 命令交互         | 略看，需要的时候要仔细查  |
| 5 AT Command and Results Codes | AT cmd和结果        | 略看，需要的时候仔细查    |
| 6 RFCOMM                       | RFCOMM 交互需求     | 仔细看完，                |
| 7 GAP                          | GAP中的需要内容     | 仔细看完，                |
| 8-9                            | 参考和专业名词      | 不用看                    |
| 10 mSBC技术                    |                     | 需要处理codec的需要仔细看 |
| 11 code ID                     |                     | 仔细看完，                |
| 12 PLC 的实现                  |                     | 需要PLC的仔细看           |
| 13 质量指标                    | 音质质量指标        | 略看                      |
| 14 LC3-SWB 技术                | LC3-SWB 技术指标    | 略看                      |





参考：

