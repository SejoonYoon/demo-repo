# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 22:22:11 2023

@author: bruce
"""
import numpy as np
import matplotlib.pyplot as plt

j= 4 #Unit의 종류
i= 5 #task의 종류
t= 10 # 시간

x_var = np.zeros((j,i,t))
b_var = np.zeros((j,i,t))

#주어진 x_var
for i in range(10):
    x_var[0,0,i]=1
x_var[1,1,0]=1
x_var[1,1,6]=1
x_var[2,1,0]=1
x_var[1,2,2]=1
x_var[1,2,4]=1
x_var[1,2,8]=1
x_var[2,2,2]=1
x_var[2,2,8]=1
for i in range(4):
    x_var[2,3,i+4]=1
x_var[3,4,5]=1
x_var[3,4,8]=1

#주어진 b_var
b_var[0,0,0]=36
b_var[0,0,1]=100
b_var[0,0,2]=1
b_var[0,0,3]=1
b_var[0,0,4]=1
b_var[0,0,5]=1
b_var[0,0,6]=1
b_var[0,0,7]=1
b_var[0,0,8]=1
b_var[0,0,9]=1
b_var[1,1,0]=80
b_var[1,1,6]=74
b_var[2,1,0]=50
b_var[1,2,2]=80
b_var[1,2,4]=80
b_var[1,2,8]=80
b_var[2,2,2]=50
b_var[2,2,8]=50
b_var[2,3,4]=50
b_var[2,3,5]=47
b_var[2,3,6]=50
b_var[2,3,7]=16.25
b_var[3,4,5]=50
b_var[3,4,8]=113.75

print(np.size(x_var, 1))

#tau = np.zeros((j,i)) ## j x i array that stores the processing time of task i in unit j in units of n * delta where n is a positive integer

def ganttchart():
    
    import numpy as np
    color = ['#DBF9DB','#FF5F1F','#DBE9FA','#98F516','#43C6DB', '#C9C0BB' , '#98AFC7', '#C9DFEC', '#57FEFF', '#50C878',
             '#B1FB17', '#FBF6D9', '#FFDF00']
    Unit = []
    Task = []
    Unit_list = []
    Task_list = []
    yt=[]                           # 그래프의 y축에 Unit의 이름을 넣기 위해 필요
    n=int(np.sum(x_var))            # array 내 1의 총 개수 (작성해야하는 막대의 수)
    w=np.where(x_var==1)            # x_var=1이 되는 index를 찾음
    j_list=w[0]                     # x_var=1이 되는 index 중 j 값들의 리스트 (중복)
    i_list=w[1]                     # x_var=1이 되는 index 중 i 값들의 리스트 (중복)
    t_list=w[2]                     # x_var=1이 되는 index 중 t 값들의 리스트 (중복)
    j = max(j_list)+1               # Unit의 개수를 파악
    i = max(i_list)+1               # Task의 개수를 파악
    t = max(t_list)+1               # Time을 파악
    
    for x in range(j):              # Unit의 이름을 받음     
        x=input('Unit의 이름 : ')  
        Unit.append(x)
        
    for x in range(i):               # Task의 이름을 받음
        x=input('Task의 이름 : ')
        Task.append(x)
    
    delta = int(input('시간간격 [h] : '))    # chart에 나타낼 시간 간격을 받음
    
    for i in range(1,j+1):          # Unit의 수에 따라서 yt를 생성
        yt.append(i)
        
        
    for j in j_list:                # 숫자로 받은 Unit에 이름을 붙여줌
        Unit_list.append(Unit[j])
        
    for i in i_list:                # 숫자로 받은 Task에 이름을 붙여줌
        Task_list.append(Task[i])
        
    def bar(x_start, x_ren, y_point, y_width,  color):         # x시작점, 가로길이, y시작점, 세로길이, 색깔에 따른 막대를 그림
        ax.broken_barh([(x_start, x_ren)], (y_point,y_width), facecolors = color, edgecolors='black') 
        
    fig, ax = plt.subplots(figsize=(t,j+4))     # 시간과 Unit 수에 따른 전체적인 chart의 틀을 만듬
    
    for i in range(n):              # 위의 함수를 바탕으로 막대를 그림
        bar(t_list[i], delta , j_list[i]+0.75, 0.5, color[i_list[i]])
        
    for i in range(n):              # 그려진 막대에 Task의 이름을 씀
        ax.text(t_list[i]+0.1,j_list[i]+1.1,Task_list[i], fontsize=10 )
        
    for i in range(n):              # 그려진 막대에 b_var 입력
        ax.text(t_list[i]+0.1,j_list[i]+0.9,b_var[j_list[i],i_list[i],t_list[i]], fontsize=10 )
        
    ax.set_yticks(yt)               # y축에 Unit의 이름을 씀
    ax.set_yticklabels(Unit) 
    ax.set_xlim(0, t+1)               # x축에 시간을 씀
    ax.tick_params(labelsize=20)    # 축의 글자크기를 20으로 지정
    ax.grid(axis = 'x')             # x축 격자 무늬
    
    
    ax.set_title('Gantt Chart',size=30)     # chart의 이름을 써줌

    plt.savefig('Gantt chart.pdf')  # pdf로 저장
    plt.show()

ganttchart()
