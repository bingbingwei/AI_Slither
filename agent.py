import util
def duplicateSnake(snake):
    body_lst = []
    for item in snake.snakebody:
        body_lst.append(item)
    snake_new = util.Snake([snake.snakehead[0], snake.snakehead[1]], body_lst)
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
            problem.printDebug('FOUND')
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
        problem.printDebug("NOT FOUND")
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
    choice = 'up'
    for move in snake.checkMove():
        snake_new = duplicateSnake(snake)
        snake_new.move(move)
        if canfindtail(snake_new):
            dis= manhattanDistance(problem.apple,snake_new.snakehead)
            if (dis >farest_dis):
                farest_dis = dis
                choice = move
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
        #visited.append(snake_current.snakehead)
        if snake_current.snakehead == problem.apple:
            problem.printDebug('FOUND')
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
        ##check if can find tail
        ##problem.printDebug('snake')
        ##problem.printDebug(snake_current.snakehead)
        ##problem.printDebug(snake_current.snakebody)
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
            problem.printDebug("CAN'T FOUND TAIL")
            return []
        
    else:
        problem.printDebug("NOT FOUND")
        return []
