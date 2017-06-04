# -*- coding: UTF-8 -*-
import copy

origin = {0:[0,0],1:[1,-1],2:[2,-1],3:[2,-1],4:[4,-1]
         ,5:[1,-1],6:[3,-1],7:[3,-1],8:[1,-1],9:[1,-1]
         ,10:[5,-1],11:[4,-1],12:[3,-1],13:[5,-1],14:[0,-1]
         ,15:[5,-1],16:[2,-1],17:[1,-1],18:[5,-1],19:[0,-1]
         ,20:[2,-1],21:[1,-1],22:[0,-1],23:[0,-1],24:[4,-1]}
#原始数据点 keys is location; value[0] is color; value[1] is group

def group(origin):       #处理原始数据
    k = 1
    for number in range(0, 5):
        for number1 in range(0, 4):               #计算每一行中相邻之间是否有同一类的
            temp = number * 5 + number1
            if origin[temp][1] == -1:
                origin[temp][1] = k
                k = k + 1
            if origin[temp][0] == origin[temp + 1][0]:
                origin[temp + 1][1] = origin[temp][1]
        if origin[number * 5 + 4][1] == -1:
            origin[number * 5 + 4][1] = k
            k = k + 1
    for number in range(0, 4):                   #计算每一列中相邻之间是否有同一类的
        for number1 in range(0, 5):
            temp = number * 5 + number1
            if origin[temp][0] == origin[temp + 5][0]:
                origin[temp + 5][1] = origin[temp][1]


grouped = [0]  # 已分组的初始值是 左上角，已分组


def sonOfGroup(origin,grouped):
    grouping =[] # 与已分组相邻的位置 ，所有待分组的位置集合
    grouping_color = []  # 待分组中颜色的类别，下一次变换颜色的选择
    grouping_color_same = []  # 最终的子集合
    for number in grouped :
        if(number %5 !=4):         #边缘的右边一位
            if(number+1 not in grouped):
                grouping.append(number+1)
        if(number <20):             #边缘的下方一位
            if(number+5 not in grouped):
                grouping.append(number+5)
    grouping = list(set(grouping))
                  #重复例如 [1,5]和[5,1]的颜色一样会出现两边
    flag = []     #flog去标记为在grouping已经寻找过的元素
    for location in grouping:    #去寻找grouping中颜色一样的元素，在变化颜色时一次性可以改变多个位置
        if location not in flag:
            temp =[]
            temp.append(location)
            for location1 in grouping:      #会存在 location == loaction1的情况 temp会有重复元素
                if origin[location][0]==origin[location1][0]:
                    if(location1 not in flag):
                        temp.append(location1)
                        flag.append(location)
                        flag.append(location1)

            temp = list(set(temp))
            grouping_color.append(temp)
            #grouping_color means grouping中颜色一样的元素 like [[],[],[]]
    for same_group in grouping_color:
        same_group_temp = copy.deepcopy(same_group)
        for same_group1 in same_group:
            for number in range(0, 24):
                if origin[number][1] == origin[same_group1][1]:
                    same_group_temp.append(number)
        same_group_temp = list(set(same_group_temp))
        grouping_color_same.append(same_group_temp)

    # print grouping_color    #下一次变换颜色的选择
    # print grouping        #所有待分组的位置集合
    # print grouping_color_same #下一次变换颜色的所有产生的子集合
    return grouping_color_same


def h(grouped):#启发函数
    q = copy.deepcopy(grouped)       # 已分组
    w = sonOfGroup(origin, q)        #下一次变换颜色的所有产生的子集合
    flag = 0  # 计数
    while len(q)<25 :
        for same_group in w:
            for same_group1 in same_group:
                q.append(same_group1)       #不区分颜色，全部作为下一跳结点
        flag = flag + 1
        # print q
        w = sonOfGroup(origin, q)
    return flag



def choose_nextgroup(group_color_same):  #从子集合中选择最优的下一跳
    k=0
    min =0
    temp = 10000000
    for groupi in group_color_same:
        q = copy.deepcopy(grouped)  # 已分组
        for number in groupi:
            q.append(number)       #假设groupi为下一跳把它加入已分组的 去分析h(n)
        if(h(q)<temp):
            temp = h(q)
            min = k
        k = k+1
    print group_color_same[min]
    return group_color_same[min]    #返回启发函数最小的分组

g = 0
def A_star(group_chosen):
    global g
    color = origin[group_chosen[0]][0]
    for number in grouped:      #变化已分组的颜色
        origin[number][0] = color
    for number in group_chosen:     #扩展已分组序号
        origin[number][1] = 0
        grouped.append(number)
    g = g+1
    print "当前已分组结点："
    print grouped
    # print origin
    return g

group(origin)
while len(grouped) <25:
    w = sonOfGroup(origin,grouped)
    print A_star(choose_nextgroup(w))





