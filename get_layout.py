from GameState import GameState,Directions
from Stack import Stack
from Position import Position_node
import numpy as np
from collections import deque
from Stree import StreeNode
map="layouts/test.lay"#此处更改地图文件路径
gamestate=GameState(map)
def get_direction(agent_position,next_position):#根据前后坐标判断action的方向
    agent_x,agent_y=agent_position
    next_x,next_y=next_position
    direct=(next_x-agent_x,next_y-agent_y)
    if direct==(0,1):
        return Directions.UP
    elif direct==(0,-1):
        return Directions.DOWN
    elif direct==(1,0):
        return Directions.RIGHT
    else:
        return Directions.LEFT

#DFS搜索目标位置
def DFS(game_state=gamestate):
    debug_count=0
    positions=Stack()
    directions=Stack()
    start_position=tuple(game_state.get_current_state())
    flags={}
    flags1={}
    flags[start_position]=True#
    flags1[start_position]=True
    positions.push(start_position)
    getgoal=False
    start_info=game_state.query_successor(start_position)
    for i in range(4):
        if start_info[i][0]!=start_position:
            positions.push(start_info[i][0])
            directions.push(i)
            flags[start_info[i][0]]=True
            if start_info[i][2]==True:
                getgoal=True
                break
    if getgoal==True:
        game_state.step([directions.top()])
        positions.clear()
        positions.push(start_position)
    if  directions.empty()==False:
        game_state.step([directions.top()])
    while positions.size()!=1:
        debug_count+=1
        print('Loop=',debug_count)
        count=0
        loop=False
        agent_position=tuple(game_state.get_current_state())
        print(agent_position)
        if flags1.get(agent_position,False)==False:
            loop=True
            agent_info = game_state.query_successor(agent_position)
            for i in range(4):
                if agent_info[i][0] != agent_position and flags.get(agent_info[i][0], False) == False:
                    positions.push(agent_info[i][0])
                    directions.push(i)
                    flags[agent_info[i][0]]=True
                    # --------------------
                    count += 1
                    if agent_info[i][2] == True:
                        getgoal = True
                        break
        flags1[agent_position]=True
        if count==0 and loop==True:
            positions.pop()
            #------------------
            last_action=directions.pop()
            directions.push((last_action+2)%4)
            game_state.step([directions.pop()])
        else:
            if getgoal==True:
                game_state.step([directions.top()])
                break
            if positions.top()!=agent_position:
                game_state.step([directions.top()])
            elif positions.top()==agent_position:
                positions.pop()
                # ------------------
                last_action = directions.pop()
                directions.push((last_action + 2) % 4)
                game_state.step([directions.pop()])
#BFS搜索目标位置
def BFS(game_state=gamestate):
    positions=deque()
    #directions=deque()
    #reverse_directions=deque()#用来记录返回的方向
    goal_direction=deque()
    flags={}
    getgoal=False
    goal_node=StreeNode()
    depth=0#bfs树的层数
    start_position=tuple(game_state.get_current_state())#开始点的信息
    positions.append(start_position)
    insert_list=[]
    insert_list_1=[]
    root=StreeNode(start_position)
    insert_list.append([root])
    root.set_depth(1)
    root_branchs=0
    depth+=1
    flags[start_position]=True
    start_info=game_state.query_successor(start_position)
    #将根节点及其周围节点信息存入搜索树中
    for i in range(4):
        if start_info[i][0]!=start_position:
            _node=StreeNode(start_info[i][0])
            _node.set_depth(2)
            positions.append(start_info[i][0])
            root.children.append(_node)
            _node.set_parent(root)
            root_branchs+=1
            insert_list_1.append(_node)
            flags[start_info[i][0]]=True
            if  start_info[i][2]==True:
                getgoal=True
                goal_direction.append(i)
                break
    if getgoal==True:
        game_state.step([goal_direction.popleft()])
    root.set_childnum(root_branchs)
    positions.popleft()#节点队列中删去根节点
    insert_list.append(insert_list_1)
    depth+=1#此时depth=2
    while len(insert_list[depth-1])!=0 and getgoal==False:#BFS逐层循环
        insert_list_any=[]#存储第k层各节点
        for agent_node in insert_list[depth-1]:
            agent_branch = 0  # 记录子节点个数
            agent_info = game_state.query_successor(agent_node.get_position())
            for i in range(4):
                if agent_info[i][0] != agent_node.get_position() and flags.get(agent_info[i][0], False) == False:
                    node = StreeNode(agent_info[i][0])
                    node.set_parent(agent_node)
                    agent_node.children.append(node)
                    agent_branch+=1
                    node.set_depth(depth+1)
                    agent_branch+=1
                    insert_list_any.append(node)
                    flags[agent_info[i][0]]=True
                    if agent_info[i][2]==True:
                        getgoal=True
                        goal_node=node
                        break
            agent_node.set_childnum(agent_branch)
            if getgoal==True:
                break
        depth+=1
        insert_list.append(insert_list_any)
    if getgoal==True:
        print(goal_node.get_position())
        direct_info=Stack()
        p_node=goal_node
        while p_node!=root:
            direct=get_direction(p_node.get_position(),p_node.get_parent().get_position())
            direct_info.push((direct+2)%4)
            p_node=p_node.get_parent()
        actionlist=[]
        while not direct_info.empty():
            actionlist.append(direct_info.pop())
        game_state.step(actionlist)
#任务二：搜索算法
def Flex_Search(game_state=gamestate):
    debug_count=0
    positions = Stack()
    directions = Stack()
    start_position = tuple(game_state.get_current_state())
    print("start=",start_position)
    flags = {}
    flags1={}
    flags[start_position] = True  #
    flags1[start_position]=True
    positions.push(start_position)
    getgoal = False
    start_info = game_state.query_successor(start_position)

    start_list=[]#根据bonus大小排序action
    start_dir_list=[]#存储相应方向
    for i in range(4):
        if start_info[i][0] != start_position:
            position=Position_node(start_info[i][0],i,start_info[i][1],start_info[i][2])
            start_list.append(position)
    start_list.sort(key=lambda Position_node:Position_node.bonus)

    for start_dir in start_list:
        positions.push(start_dir.get_position())
        directions.push(start_dir.get_direction())
        flags[start_dir.get_position()]=True
        if start_dir.get_getgoal()==True:
            getgoal=True
            break

    if getgoal == True:
        game_state.step([directions.top()])
        positions.clear()
        positions.push(start_position)
    if directions.empty() == False:
        game_state.step([directions.top()])
    while positions.size() != 1:
        debug_count += 1
        print('Loop=', debug_count)
        count = 0
        loop = False
        agent_position = tuple(game_state.get_current_state())
        print(agent_position)
        if flags1.get(agent_position, False) == False:
            loop = True
            agent_info = game_state.query_successor(agent_position)
            agent_dir_list=[]
            for i in range(4):
                if agent_info[i][0] != agent_position and flags.get(agent_info[i][0], False) == False:
                    position1=Position_node(agent_info[i][0],i,agent_info[i][1],agent_info[i][2])
                    #positions.push(agent_info[i][0])
                    #directions.push(i)
                    agent_dir_list.append(position1)
                    # flags[agent_info[i][0]]=True
                    # --------------------
                    #count += 1
                    #if agent_info[i][2] == True:
                        #getgoal = True
                        #break
            agent_dir_list.sort(key=lambda Position_node:Position_node.bonus)
            for agent_dir in agent_dir_list:
                positions.push(agent_dir.get_position())
                directions.push(agent_dir.get_direction())
                flags[agent_dir.get_position()]=True
                count+=1
                if agent_dir.get_getgoal()==True:
                    getgoal=True
                    break
        flags1[agent_position] = True
        if count == 0 and loop == True:
            positions.pop()
            # ------------------
            last_action = directions.pop()
            directions.push((last_action + 2) % 4)
            game_state.step([directions.pop()])
        else:
            if getgoal == True:
                game_state.step([directions.top()])
                break
            if positions.top() != agent_position:
                game_state.step([directions.top()])
            elif positions.top() == agent_position:
                positions.pop()
                # ------------------
                last_action = directions.pop()
                directions.push((last_action + 2) % 4)
                game_state.step([directions.pop()])
#每次调用一个搜索算法，其余的注释掉
#Flex_Search(gamestate)
#DFS(gamestate)
#BFS(gamestate)























































