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
