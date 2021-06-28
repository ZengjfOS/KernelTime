# README

使用Python3 matplotlib绘图，直观显示内核Log时间信息，便于分析内核log，主要是对内核输出的log进行时间分析工具

## 参考文档

* [README.md](docs/README.md)

## 安装依赖包

* pip3 install matplotlib

## 示例

![KernelTime_TimerInterval.png](docs/images/KernelTime_TimerInterval.png)

* 左图：采样点时间轨迹，可以看采样Timer是否大体工作正常，不会出现太大延迟，内核调度正常
* 右图：
  * 紫色：实际采样间隔
  * 绿色：采样最大、最小间隔波动
  * 红色：采样平均间隔

## Example

* [KernelTime.py](KernelTime.py)
  * 根据内核log，分析传感器数据是否正常
* [DateConvert.py](DateConvert.py)
  * MTK内核log加入UTC时间，系统不能休眠，否则时间不准
* [KernelWakeup.py](KernelWakeup.py)
  * 通过内核log分析系统休眠状态下唤醒时间
* [LogcatWakeup.py](LogcatWakeup.py)
  * 通过logcat获取系统休眠唤醒点
* [XYFile.py](XYFile.py)
  * 文件内容XY转换
* [Partition.py](Partition.py)
  * 获取分区信息
