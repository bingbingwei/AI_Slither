from multiprocessing import Queue# initialize the module
class Stack:
    def __init__(self):
        self.list = []

    def push(self,item):
        self.list.append(item)

    def pop(self):
        return self.list.pop()

    def isEmpty(self):
        return len(self.list) == 0

class Queue:
    def __init__(self):
        self.list = []

    def push(self,item):
        self.list.insert(0,item)

    def pop(self):
        return self.list.pop()

    def isEmpty(self):
        return len(self.list) == 0
class Problem:
    def __init__(self, snake, apple, queue):
        self.snake = snake
        self.apple = apple
        self.queue_communicate = queue
    def printDebug(self,msg):
        self.queue_communicate.put(msg)
class Snake:
    def __init__(self,snakehead,snakebody):
        self.snakehead = snakehead
        self.snakebody = snakebody
    def checkMove(self):
        legal_move = []
        position = [self.snakehead[0]-20, self.snakehead[1]]
        if position not in self.snakebody and position[0]>=0:
            legal_move.append('left')
        position = [self.snakehead[0]+20, self.snakehead[1]]
        if position not in self.snakebody and position[0]<=800:
            legal_move.append('right')
        position = [self.snakehead[0], self.snakehead[1]-20]
        if position not in self.snakebody and position[1]>=0:
            legal_move.append('up')
        position = [self.snakehead[0], self.snakehead[1]+20]
        if position not in self.snakebody and position[1]<=600:
            legal_move.append('down')
        return legal_move
    def move(self, direction):
        if direction == 'up':
            self.snakehead = [self.snakehead[0],self.snakehead[1]-20]
        elif direction == 'down':
            self.snakehead = [self.snakehead[0],self.snakehead[1]+20]
        elif direction == 'left':
            self.snakehead = [self.snakehead[0]-20,self.snakehead[1]]
        elif direction == 'right':
            self.snakehead = [self.snakehead[0]+20,self.snakehead[1]]
        self.snakebody.append(self.snakehead)
        del self.snakebody[0]

