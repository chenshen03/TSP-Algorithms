# TSP-Algorithms

利用模拟退火算法、遗传算法等解决旅行商问题。

因为用于解决TSP问题的算法有很多种，遂将其整合成一个代码框架。

## Directory structure

```
├─ datas             数据集
│  ├─ ChinaCitys.txt 中国34个城市的经纬度数据
│  ├─ __init__.py    
│  └─ citydata.py    包含多个城市数据集
├─ methods
│  ├─ GA.py          遗传算法
│  ├─ SA.py          模拟退火算法
│  ├─ Hopfield.py    Hopfield神经网络
│  └─ __init__.py
├─ tools             工具
│  ├─ __init__.py
│  └─ plot.py        作图工具
├─ README.md
└─ TSP.py            旅行商问题
```

## Usage

```
python TSP.py
```
