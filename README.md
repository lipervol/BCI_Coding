# BCI Coding

## Day One

### 设备调试

**设备**：设备用的是淘宝买的 *OpenBCI Cyton WIFI+蓝牙 16通道 + 16通道电极帽*，拿来做练习用

初步测试了一下输出，看着有些乱，但是大概可以看到在25Hz左右有一个明显的尖峰，也就是有较强的beta波，表明我此时处于一个注意力集中的状态（*看数据ing*）

![数据](https://github.com/lipervol/BCI_Coding/blob/master/image/3528488a43ec2eb33f270e994ce7c2f.png)

![图例](https://github.com/lipervol/BCI_Coding/blob/master/image/1ab91ad2add3f379d61b381f2bf48f7.png)

## Day Two

### 脑电信号特点

* **脑电信号幅度非常微弱，频率范围0.5~50Hz**。一般头皮脑电信号只有±50uV左右，超过±100uV可以认为是噪声
* **脑电信号是一种随机性很强的非平稳信号**。之所以说随机性强，是因为影响它的因素太多，其规律又尚未被认识
* **脑电信号是非线性信号**。生物组织的调节以及自适应能力必然影响到电生理信号，这使得脑电具有典型的非线性的特点。而传统意义上的信号处理方法都是建立在线性系统理论分析基础之上的，因而分析结果是不可避免地丢失了很多原始信号所带的信息。这也是为什么非线性动力学混沌理论发展起来后被迅速运用到脑电的分析研究中的原因。

*在各种伪迹中，眼电对EEG的影响最大，因此通常在脑电测量的同时进行眼电信号的测量，以便可以进行离线的眼电伪迹去除。*

### 刺激选择

根据《*Stimuli design for SSVEP-based brain computer-interface*》一文所述，拟采取蓝色或绿色刺激，刺激频率6-15Hz（低频段），刺激强度的控制信号采用正弦形式。

### 采集部位选择

![10-20系统](https://github.com/lipervol/BCI_Coding/blob/master/image/c7e226b482ebeb313ea802f.jpg)

作用电极一共四个，分别放置在P3、P4以及O1、O2处，参考电极放置在Pz和Oz处（*采用国际标准导联10-20系统*）

### 锁时与锁相

* ERP：event-related Potentials，事件相关电位
* ERSP：event-related spectral perturbation，事件相关谱扰动

* ITC：inter trial coherence，试验间的相干性

* 锁时：同一过程的多个试验中刺激信号对输出的影响出现在相似的时间

* 锁相：同一过程的多个实验中输出信号的相位一致

多次同一过程的单个实验的**ITC如果接近1.0，则说明相位变化小**，也就是锁相，此时可以通过简单的线性方法，如叠加平均得到ERP，否则，**在ITC较低的情况下，则不能直接采取线性方法获得ERP**，只能通过包络检测或功率谱分析等非线性方法获得如ERS（事件相关的电位上升）或ERD（事件相关的电位下降）等特征。

**锁相的前提是锁时**，锁时与锁相的生理机制不同：

* 相对于刺激**锁相的是诱发反应（evoked response）**，如听觉、视觉诱发电位，反应的是自下而上的驱动过程
* 而非锁相的是**诱导反应（induced response）**，ERD/ERS反应的是一个自上而下的调节过程
* **ERP需要锁时锁相**，这是其能够通过叠加平均提取的根本，属于诱发反应；
* **ERSP锁时不锁相**，其反映的是能量值相对于基线的升高或降低，必然是锁时的，属于诱导反应。

## Day Three

初步实现把人眼作为传感器，识别屏幕闪烁频率的功能（在MyBCI/recognition，还挺好玩的），更新了刺激源（目前使用的pygame，之前的刺激源太不准确了），识别算法是典型相关分析（CCA），预处理只做了均值滤波和带通加带阻滤波的组合，效果一般般，后续继续优化，并且计划添加交互功能。

后续准确率提升的方法有两个方面：

1. 硬件上，提高电极采集质量，
2. 软件上，设计更合理的预处理方式和滤波器，测试除传统CCA以外的识别算法。

这是目前的输出，我设置的时间窗是2秒，也就是每2秒获取一次缓冲区里最新的数据然后判断，这个是12hz闪烁的时候的情况，基本都是准的

![12hz](https://github.com/lipervol/BCI_Coding/blob/master/image/0ffa2f500bf16d6464d5b968092a794.png)

## Day Four

简单的做了一下交互功能（在在MyBCI/SSVEP_game，需要屏幕刷新率120Hz以上），屏幕上有一个小幽灵，左边闪烁频率是12Hz，右边是15Hz，你看那边这个小幽灵就会往那边移动，作为展示效果还是可以的。

![game](https://github.com/lipervol/BCI_Coding/blob/master/image/20220122203737.png)

## Day Five

忙了一个月毕设，昨天晚上写了一下，鉴于识别目前方法的准确率不高，做了一个容错率比较高的小游戏，只要及时识别对了方向就可以击中敌机，同样要求屏幕刷新率120Hz，后续可能会尝试一下改成self-attention网络进行识别

![game1](https://github.com/lipervol/BCI_Coding/blob/master/image/game1.png)

![game2](https://github.com/lipervol/BCI_Coding/blob/master/image/game2.png)