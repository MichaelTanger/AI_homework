from layout import Layout
import os
import numpy as np


class Directions:
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3
    action_map = {RIGHT: 'RIGHT',
                  DOWN: 'DOWN',
                  LEFT: 'LEFT',
                  UP: 'UP'}


class GameState:
    """
    this class maintains the game state, and feedback to the search agent
    """
    actions = {Directions.DOWN: np.array((0, -1)),
               Directions.UP: np.array((0, 1)),
               Directions.RIGHT: np.array((1, 0)),
               Directions.LEFT: np.array((-1, 0))}

    def __init__(self, _layout_filename):
        assert os.path.exists(_layout_filename), '_layout file: %s does not exist!' % _layout_filename
        with open(_layout_filename) as f:
            self._layout = Layout([line.strip() for line in f])
        self._query_count = 0
        self._query_limit = self._layout.width * self._layout.height
        self._bonus_count = 0
        self._action_count = 0

    def step(self, action_list):
        """
        step the action list and return bonus collected and state reached
        :param action_list:
        :return: state, bonus collected
        """
        for action in action_list:
            self._action_count += 1
            # step
            xx, yy = self._layout.agentPosition + self.actions[action]
            if -1 < xx < self._layout.width and -1 < yy < self._layout.height:
                if self._layout.walls[xx][yy]:
                    self._bonus_count += self._layout.wall_punishment
                else:
                    self._layout.agentPosition += self.actions[action]
            else:
                self._bonus_count += self._layout.outRange_punishment
            x, y = self._layout.agentPosition
            # bonus
            self._bonus_count += self._layout.bonus[x][y]
            if not self._layout.walls[x][y]:
                self._layout.bonus[x][y] = 0
            # reach goal
            if x == self._layout.goalPosition[0] and y == self._layout.goalPosition[1]:
                try:
                    with open('result_success.txt', 'w') as f:
                        f.write('bonus: %d\nquery: %d\naction steps: %d' %
                                (self._bonus_count, self._query_count, self._action_count))
                except IOError as e:
                    print('Fail to write result.txt')
                    print('reach goal\nbonus: %d\nquery: %d\naction steps: %d' % \
                          (self._bonus_count, self._query_count, self._action_count))
        return self._layout.agentPosition, self._bonus_count

    def query_successor(self, state):
        """increment qeury count
        :param state (x, y) tuple
        :return list of successor (state, bonus, reachGoal) tuple
        """
        if self._query_count < self._query_limit:
            # query limit 10000
            self._query_count += 1
        else:
            try:
                with open('result_fail.txt', 'w') as f:
                    f.write('bonus: %d\nquery: %d\n' % (self._bonus_count, self._query_count))
            except IOError as e:
                print('Fail to write result.txt')
                print('Reach query limit\nbonus: %d\nquery: %d\n' % (self._bonus_count, self._query_count))
            raise ValueError('Reach query limit!')
        x, y = state
        successors = []
        for action in range(4):
            xx, yy = state + self.actions[action]
            if -1 < xx < self._layout.width and -1 < yy < self._layout.height:
                bonus = self._layout.bonus[xx][yy]
                if self._layout.walls[xx][yy]:
                    successors.append(((x, y), bonus, False))
                elif xx == self._layout.goalPosition[0] and yy == self._layout.goalPosition[1]:
                    successors.append(((xx, yy), 0, True))
                else:
                    successors.append(((xx, yy), bonus, False))
            else:
                successors.append(((x, y), self._layout.outRange_punishment, False))
        return successors

    def get_current_state(self):
        return self._layout.agentPosition
