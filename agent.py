import util

def duplicateSnake(snake):
    body_lst = []
    for item in snake.snakebody:
        body_lst.append(item)
    snake_new = util.Snake([snake.snakehead[0], snake.snakehead[1]], body_lst, snake.width, snake.height)
    return snake_new

def DepthFirstSearch(problem):
    lst = []
    visited = []
    parent_lst = {}
    snake = problem.snake
    start_state = snake.snakehead
    snake_current = 0
    stack = util.Stack()
    stack.push(snake)
    found = False
    while not stack.isEmpty():
        snake_current = stack.pop()
        visited.append(snake_current.snakehead)
        if snake_current.snakehead == problem.apple:
            problem.printLog('FOUND')
            found = True
            break

        for move in snake_current.checkMove():
            snake_new = duplicateSnake(snake_current)
            snake_new.move(move)
            if snake_new.snakehead in visited:
                continue
            parent_lst[str(snake_new.snakehead)] = [snake_current.snakehead, move]
            stack.push(snake_new)
    if found:
        current_pos, move = parent_lst[str(snake_current.snakehead)]
        while current_pos != start_state:
            lst.append(move)
            current_pos, move = parent_lst[str(current_pos)]
        lst.append(move)
        lst.reverse()
        return lst
    else:
        problem.printLog("NOT FOUND")
        return []
def findtail(snake):
    visited = []
    parent_lst = {}
    tail= (snake.snakebody)[0]
    start_state = snake.snakehead
    snake_current = 0
    queue = util.Queue()
    queue.push(snake)
    found = False
    while not queue.isEmpty():
        snake_current = queue.pop()
        #visited.append(snake_current.snakehead)
        if snake_current.snakehead == tail:
            found = True
            break

        for move in snake_current.checkMove():
            snake_new = duplicateSnake(snake_current)
            snake_new.move(move)
            if str(snake_new.snakehead) in parent_lst:
                continue
            parent_lst[str(snake_new.snakehead)] = [snake_current.snakehead, move]
            queue.push(snake_new)
    
    return found
def chooseFartestpoint(problem):
    farest_dis= 0
    lst=[]
    choice = ""
    flag = True
    snake=problem.snake
    for move in snake.checkMove():
        snake_new = duplicateSnake(snake)
        snake_new.move(move)
        if findtail(snake_new):
            dis= manhattanDistance(problem.apple,snake_new.snakehead)
            if (dis >farest_dis):
                farest_dis = dis
                choice = move
                flag = False
    if flag:
        return []
    lst.append(choice)
    return lst
def manhattanDistance( point1,point2):
    return abs(point1[0]-point2[0])+abs(point1[1]-point2[1])
def BreadthFirstSearch(problem):
    lst = []
    visited = []
    parent_lst = {}
    snake = problem.snake
    start_state = snake.snakehead
    snake_current = 0
    queue = util.Queue()
    queue.push(snake)
    found = False
    while not queue.isEmpty():
        snake_current = queue.pop()
        if snake_current.snakehead == problem.apple:
            problem.printLog('FOUND')
            found = True
            break
        for move in snake_current.checkMove():
            snake_new = duplicateSnake(snake_current)
            snake_new.move(move)
            if str(snake_new.snakehead) in parent_lst:
                continue
            parent_lst[str(snake_new.snakehead)] = [snake_current.snakehead, move]
            queue.push(snake_new)
    if found:
        canfindtail = findtail(snake_current)
        if (canfindtail):
            current_pos, move = parent_lst[str(snake_current.snakehead)]
            while current_pos != start_state:
                lst.append(move)
                current_pos, move = parent_lst[str(current_pos)]
            lst.append(move)
            lst.reverse()
            return lst
        else:
            problem.printLog("CAN'T FOUND TAIL")
            return []
        
    else:
        problem.printLog("NOT FOUND")
        return []


def aStarSearch(problem):
    """Search the node that has the lowest combined cost and heuristic first."""
    snake= problem.snake
    start_state= snake.snakehead
    map_pri_q=  util.PriorityQueue()

    map_pri_q.push(snake,0+manhattanDistance(start_state,problem.apple))
    parent_dict={}
    priority={}
    priority[str(start_state)]=0
    passed_point=[]
    route_dict={}
    snake_current = 0
    lst=[]
    while not map_pri_q.isEmpty():
        snake_current = map_pri_q.pop()
        if (snake_current.snakehead == problem.apple):
            problem.printLog('FOUND')
            found = True
            break

        for move in snake_current.checkMove():
            snake_new = duplicateSnake(snake_current)
            snake_new.move(move)
            if str(snake_new.snakehead) not  in passed_point:
                if(str(snake_new.snakehead) in  parent_dict) : 
                    if(priority[str(snake_new.snakehead)] >priority[str(snake_current.snakehead)]+1):
                        priority[str(snake_new.snakehead)] =priority[str(snake_current.snakehead)]+1
                        parent_dict[str(snake_new.snakehead)] = [snake_current.snakehead,move]
                        map_pri_q.push(snake_new,priority[str(snake_new.snakehead)]+manhattanDistance(snake_new.head,problem.apple))
                else:
                    priority[str(snake_new.snakehead)] =priority[str(snake_current.snakehead)]+1
                    parent_dict[str(snake_new.snakehead)] = [snake_current.snakehead,move]
                    map_pri_q.push(snake_new,priority[str(snake_new.snakehead)]+manhattanDistance(snake_new.snakehead,problem.apple))
        '''
        for n in successors : 

            if (n[0] not in passed_point):
                if (n[0] in parent_dict ):
                    if priority[n[0]] > priority[node[0]] + n[2]:
                        priority[n[0]] =  priority[node[0]] + n[2]
                        parent_dict[n[0]] = node[0]
                        route_dict[n[0]]= n[1]
                        map_pri_q.push(n,priority[n[0]]+heuristic(n[0],problem))
                else:
                    parent_dict[n[0]]=node[0]
                    route_dict[n[0]]=n[1]
                    priority[n[0]]=priority[node[0]]+n[2]
                    map_pri_q.push(n,priority[n[0]]+heuristic(n[0],problem))
        '''
    if found:
        canfindtail = findtail(snake_current)
        if (canfindtail):
            current_pos, move = parent_dict[str(snake_current.snakehead)]
            while current_pos != start_state:
                problem.printLog((current_pos,start_state))
                lst.append(move)
                current_pos, move = parent_dict[str(current_pos)]
            lst.append(move)
            lst.reverse()

            return lst
        else:
            problem.printLog("CAN'T FOUND TAIL")
            return []
        
    else:
        problem.printLog("NOT FOUND")
        return []
        
