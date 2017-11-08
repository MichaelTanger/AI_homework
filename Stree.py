#搜索树节点类
class StreeNode:
    def __init__(self,position=(-1,-1)):
        self.position=position
        self.parent=0
        self.children=[]
        self.children_num=0
        self.depth=1
    def get_position(self):
        return self.position
    def get_parent(self):
        return self.parent
    def get_children(self):
        return self.children
    def get_depth(self):
        return self.depth
    def set_position(self,position):
        self.position=position
    def set_parent(self,parent):
        self.parent=parent
    def append_child(self,child):
        self.children.append(child)
        #self.children_num+=1
    def set_depth(self,_depth):
        self.depth=_depth
    def set_childnum(self,num):
        self.children_num=num


