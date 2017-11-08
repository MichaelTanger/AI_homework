class Stack:
    def __init__(self):
        self.items=[]
    def push(self,item):
        self.items.append(item)
    def pop(self):
        return self.items.pop()
    def clear(self):
        del self.items[:]
    def size(self):
        return len(self.items)
    def empty(self):
        return self.size()==0
    def top(self):
        return self.items[self.size()-1]
