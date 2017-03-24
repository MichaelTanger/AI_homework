from GameState import GameState,Directions
from Stack import Stack
import numpy as np
import queue
map="layouts/small.lay"
gamestate=GameState(map)
def test():
    start_position = gamestate.get_current_state()
    start_info = gamestate.query_successor(start_position)  # 起点周围的信息
    print(start_position)
    print(start_info[1][0])
    print(np.any(start_position==start_info[1][0]))
_queue=queue.Queue()
print(_queue)
_queue.put(1)
print(_queue)
print(_queue.get())
print(_queue.get())






