# 2020 MCM/ICM Problem D Project
![](https://img.shields.io/badge/language-python3.7-green.svg)![](https://img.shields.io/badge/author-Shuai_Li-black.svg)   
给女友写的2020美赛D题代码，只有一个main函数。
## 安装
```angular2
pip install -r requirements.txt
```    
## 函数解释
* draw_graph()  
`根据passingevents.csv文件画出每场比赛双方的传球图`  
* draw_full_events_ball_count(draw_pic=False,analysis=True)  
`根据fullevents.csv统计每一场比赛按照时间推进，球的轨迹以及控球双方的情况，根据一方连续控球期间，控球球员的集合元素个数，来判断是哪种模型`  
* conduct_new_passing_tables()
`根据passingevents.csv，总结出每场比赛的Node表和Edge表`  
* conduct_degree()  
`根据passingevents.csv，总结出每场比赛的每个球员的出入度以及所有比赛哈士奇队的出入度`  
## 其他就不会了
![image](img/hh.jpg)  
结束