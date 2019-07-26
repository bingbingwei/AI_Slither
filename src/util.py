from multiprocessing import Queue# initialize the module
import slither
import heapq
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
    def printLog(self,msg):
        self.queue_communicate.put(msg)
class Snake:
    def __init__(self,snakehead,snakebody, width, height):
        self.snakehead = snakehead
        self.snakebody = snakebody
        self.snake_length = 1
        self.width = width
        self.height = height
    def checkMove(self):
        legal_move = []
        position = [self.snakehead[0]-20, self.snakehead[1]]
        if position not in self.snakebody and position[0]>=0:
            legal_move.append('left')
        position = [self.snakehead[0]+20, self.snakehead[1]]
        if position not in self.snakebody and position[0]<self.width:
            legal_move.append('right')
        position = [self.snakehead[0], self.snakehead[1]-20]
        if position not in self.snakebody and position[1]>=0:
            legal_move.append('up')
        position = [self.snakehead[0], self.snakehead[1]+20]
        if position not in self.snakebody and position[1]<self.height:
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
        if len(self.snakebody) > self.snake_length:
            del self.snakebody[0]


class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)

