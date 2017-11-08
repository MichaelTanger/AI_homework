# layout.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import numpy as np
import copy

VISIBILITY_MATRIX_CACHE = {}


class Grid:
    """
    A 2-dimensional array of objects backed by a list of lists.  Data is accessed
    via grid[x][y] where (x,y) are positions on a Pacman map with x horizontal,
    y vertical and the origin (0,0) in the bottom left corner.

    The __str__ method constructs an output that is oriented like a pacman board.
    """

    def __init__(self, width, height, initialValue=False):
        self.width = width
        self.height = height
        self.data = [[initialValue for y in range(height)] for x in range(width)]

    def __getitem__(self, i):
        return self.data[i]

    def __setitem__(self, key, item):
        self.data[key] = item

    def __str__(self):
        if isinstance(self.data[0][0], bool):
            out = [['%' if self.data[x][y] else ' ' for x in range(self.width)] for y in range(self.height)]
        else:
            out = [['%3d' % self.data[x][y] if self.data[x][y] else '   ' for x in range(self.width)] for y in range(self.height)]
        out.reverse()
        return '\n'.join([''.join(x) for x in out])

    def __eq__(self, other):
        if other == None: return False
        return self.data == other.data

    def __hash__(self):
        # return hash(str(self))
        base = 1
        h = 0
        for l in self.data:
            for i in l:
                if i:
                    h += base
                base *= 2
        return hash(h)

    def copy(self):
        g = Grid(self.width, self.height)
        g.data = [x[:] for x in self.data]
        return g

    def deepCopy(self):
        return self.copy()

    def shallowCopy(self):
        g = Grid(self.width, self.height)
        g.data = self.data
        return g

    def count(self, item=True):
        return sum([x.count(item) for x in self.data])

    def asList(self, key=True):
        list = []
        for x in range(self.width):
            for y in range(self.height):
                if self[x][y] == key:
                    list.append((x, y))
        return list


class Layout:
    """
    A Layout manages the static information about the game board.
    """

    def __init__(self, layoutText):
        rewards = [int(i) for i in layoutText[0].split()]
        self.wall_punishment = rewards[0]
        assert self.wall_punishment < 0, 'wall punishment must be negative'
        self.outRange_punishment = rewards[1]
        assert self.outRange_punishment < 0, 'outRange punishment must be negative'
        self.rewards = rewards[2:]
        layoutText = layoutText[1:]
        self.width = len(layoutText[0])
        self.height = len(layoutText)
        self.walls = Grid(self.width, self.height, False)
        self.bonus = Grid(self.width, self.height, 0)
        self.agentPosition = None
        self.goalPosition = None
        self.layoutText = layoutText
        self.processLayoutText(layoutText)

    def __str__(self):
        x, y = self.agentPosition
        layout = copy.deepcopy(self.layoutText)
        layout[self.height-1-y] = layout[self.height-1-y][:x] + 'P' + layout[self.height-1-y][x+1:]
        return "\n".join(layout)

    def processLayoutText(self, layoutText):
        """
        Coordinates are flipped from the input format to the (x,y) convention here
        The shape of the maze.  Each character represents a different type of object.
         % - Wall
         P - agent position
         G - goal
         1,..,n-1 - reward
        """

        maxY = self.height - 1
        for y in range(self.height):
            for x in range(self.width):
                layoutChar = layoutText[maxY - y][x]
                self.processLayoutChar(x, y, layoutChar)

    def processLayoutChar(self, x, y, layoutChar):
        if layoutChar == '%':
            self.walls[x][y] = True
            self.bonus[x][y] = self.wall_punishment
        elif layoutChar == ' ':
            return
        elif layoutChar == 'P':
            assert self.agentPosition is None, 'multiple start position'
            self.agentPosition = np.array((x, y))
            self.layoutText[self.height-1-y] = self.layoutText[self.height-1-y].replace('P', ' ')
        elif layoutChar == 'G':
            assert self.goalPosition is None, 'multiple goal position'
            self.goalPosition = (x, y)
        elif layoutChar in [str(i) for i in range(len(self.rewards))]:
            ind = int(layoutChar)
            self.bonus[x][y] = self.rewards[ind]
        else:
            raise ValueError('Layout char illegal!')


