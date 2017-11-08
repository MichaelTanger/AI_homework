class Position_node:
    def __init__(self,_position=(-1,-1),_direction=-1,_bonus=-1,_getgoal=False):
        self.position=_position
        self.direction=_direction
        self.bonus=_bonus
        self.getgoal=_getgoal
    def get_position(self):
        return self.position
    def get_direction(self):
        return self.direction
    def get_bonus(self):
        return self.bonus
    def get_getgoal(self):
        return self.getgoal
    def set_position(self,_position):
        self.position=_position
    def set_direction(self,_direction):
        self.direction=_direction
    def set_bonus(self,_bonus):
        self.bonus=_bonus
    def set_getgoal(self,_getgoal):
        self.getgoal=_getgoal