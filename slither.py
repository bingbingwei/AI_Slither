# import the modules
import pygame
import random
import threading
import util
import agent
from multiprocessing import Queue# initialize the module

class Color:
    def __init__(self):
        self.white = (0, 0, 0)
        self.black = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 155, 0)
class Slither:
    def __init__(self):
        self.display_width = 400
        self.display_height = 400
        self.block_size = 20
        self.apple_thickness = 20
        self.FPS = 4000
        self.clock = ''
        self.gameDisplay = ''
        self.img = ''
        self.img2 = ''
        self.small_font = ''
        self.med_font = ''
        self.large_font = ''
        self.queue = Queue()
        self.snake = ''
        self.direction = ''

    def initGame(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        self.img = pygame.image.load('snakehead.png')
        self.img2 = pygame.image.load('apple.png')
        self.small_font = pygame.font.SysFont("comicsansms", 25)
        self.med_font = pygame.font.SysFont("comicsansms", 50)
        self.large_font = pygame.font.SysFont("comicsansms", 80)
        pygame.display.set_caption("Slither")
        icon = pygame.image.load("apple.png")
        pygame.display.set_icon(icon)
        pygame.display.flip()
        self.clock = pygame.time.Clock()

    def gamePause(self):
        paused = True
        self.message_to_screen("Paused", Color().black, -100, "large")
        self.message_to_screen("Press C to continue or Q to quit.", Color().black, 25)
        pygame.display.update()
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()
            self.clock.tick(5)

    def runGame(self):
        def console(request):
            while True:
                if not request.empty():
                    print(request.get())

        thread_console = threading.Thread(target=console, args=(self.queue,))
        thread_console.daemon = True
        thread_console.start()
        self.gameIntro()
        self.game_loop()

    def check_available_point(self,snake):
        available_point=[]
        for i in range(0,self.display_width - self.apple_thickness,self.apple_thickness):
            for j in range(0,self.display_height - self.apple_thickness, self.apple_thickness):
                tmp=[]
                tmp.append(i)
                tmp.append(j)
                if tmp not in snake.snakebody:
                    available_point.append(tmp)
        return available_point
    def printScore(self, score):
        text = self.small_font.render("Score: " + str(score), True, Color().black)
        self.gameDisplay.blit(text, [0, 0])

    def rand_apple_gen(self, snake):
        available_point = self.check_available_point(snake)
        rand_apple = random.choice(available_point)
        rand_apple_x = rand_apple[0]
        rand_apple_y = rand_apple[1]

        return [rand_apple_x, rand_apple_y]
    def gameIntro(self):
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        intro = False
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()

            self.gameDisplay.fill(Color().white)
            self.message_to_screen("Welcome to Slither", Color().green, -100, "large")
            self.message_to_screen("The objective of the game is to eat red apples",
                              Color().black, -30)
            self.message_to_screen("The more apples you eat, the longer you get", Color().black,
                              10)
            self.message_to_screen("If you run into yourself or the edges, you die!",
                              Color().black, 50)
            self.message_to_screen("Press C to play, P to pause, or Q to quit.", Color().black,
                              180)
            pygame.display.update()
            self.clock.tick(5)
    def snakeMove(self, snake_list):
        if self.direction == "right":
            head = pygame.transform.rotate(self.img, 270)
        if self.direction == "left":
            head = pygame.transform.rotate(self.img, 90)
        if self.direction == "up":
            head = self.img
        if self.direction == "down":
            head = pygame.transform.rotate(self.img, 180)
        self.gameDisplay.blit(head, (snake_list[-1][0], snake_list[-1][1]))

        for XnY in snake_list[:-1]:
            pygame.draw.rect(self.gameDisplay, Color().green,
                             [XnY[0], XnY[1], self.block_size - 2, self.block_size - 2])

    def text_objects(self, text, color, size):
        if size == "small":
            text_surface =  self.small_font.render(text, True, color)
        elif size == "medium":
            text_surface =  self.med_font.render(text, True, color)
        elif size == "large":
            text_surface =  self.large_font.render(text, True, color)
        return text_surface, text_surface.get_rect()
    def message_to_screen(self,msg, color, y_displace=0, size="small"):
        text_surf, text_rect = self.text_objects(msg, color, size)
        text_rect.center = (self.display_width / 2), (self.display_height / 2) + y_displace
        self.gameDisplay.blit(text_surf, text_rect)
    def game_loop(self):
        self.direction = "right"
        game_exit = False
        game_over = False
        # Will be the leader of the #1 block of the snake
        lead_x = self.display_width / 2
        lead_y = self.display_height / 2
        snake_list = [[lead_x,lead_y]]
        snake_length = 1

        ## My Code Here
        self.snake = util.Snake([lead_x,lead_y], snake_list)
        apple = self.rand_apple_gen(self.snake)
        problem = util.Problem(self.snake,apple, self.queue)
        self.queue.put('Start DFS')
        lst = agent.BreadthFirstSearch(problem)
        idx = 0
        ##My Code Here
        while not game_exit:
            if game_over is True:
                self.message_to_screen("Game Over", Color().red, y_displace=-50, size="large")
                self.message_to_screen("Press C to play again or Q to quit", Color().black,
                                  y_displace=50, size="medium")
                pygame.display.update()

            while game_over is True:
                #request_q.put((lead_x_change, lead_y_change))
                lst = []
                idx = 0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_exit = True
                        game_over = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_exit = True
                            game_over = False
                        if event.key == pygame.K_c:
                            self.game_loop()

            lead_x_change = 0
            lead_y_change = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self. direction = "left"
                        lead_x_change = -self.block_size
                        lead_y_change = 0
                    elif event.key == pygame.K_RIGHT:
                        self.direction = "right"
                        lead_x_change = self.block_size
                        lead_y_change = 0
                    elif event.key == pygame.K_UP:
                        self.direction = "up"
                        lead_y_change = -self.block_size
                        lead_x_change = 0
                    elif event.key == pygame.K_DOWN:
                        self.direction = "down"
                        lead_y_change = self.block_size
                        lead_x_change = 0
                    elif event.key == pygame.K_p:
                        self.pause()

            if idx<len(lst):
                self.direction = lst[idx]
                if self.direction == 'left':
                    lead_x_change = -self.block_size
                    lead_y_change = 0
                elif self.direction == 'right':
                    lead_x_change = self.block_size
                    lead_y_change = 0
                elif self.direction == 'up':
                    lead_y_change = -self.block_size
                    lead_x_change = 0
                elif self.direction == 'down':
                    lead_y_change = self.block_size
                    lead_x_change = 0
                idx += 1



            # Creates the boundaries for the game
            if lead_x >= self.display_width or lead_x < 0 or lead_y >= self.display_height\
                    or lead_y < 0:
                game_over = True


            # Adds or subtracts from lead_x
            lead_x += lead_x_change
            lead_y += lead_y_change
            snake_head = [lead_x, lead_y]

            # Sets background to white
            self.gameDisplay.fill(Color().white)

            # Draw a rectangle (where, color, [dimensions])
            # pygame.draw.rect(gameDisplay, red, [rand_apple_x, rand_apple_y,
            # apple_thickness, apple_thickness])
            self.gameDisplay.blit(self.img2, [apple[0], apple[1], self.apple_thickness,
                                     self.apple_thickness])

            # creates the snake and will make it longer by appending last known
            # place
            if [lead_x_change,lead_y_change] != [0,0]:
                snake_list.append(snake_head)

                if len(snake_list) > snake_length:
                    del snake_list[0]

            for each_segment in snake_list[:-1]:
                if each_segment == snake_head:
                    game_over = True

            #Define how the snake moves
            self.snakeMove(snake_list)
            self.printScore(snake_length - 1)

            self.snake = util.Snake(snake_head, snake_list)

            pygame.display.update()

            if [lead_x, lead_y] == apple:
                apple = self.rand_apple_gen(self.snake)
                snake_length += 1
                problem = util.Problem(self.snake,apple, self.queue)
                lst = agent.BreadthFirstSearch(problem)
                idx = 0
            else:
                if idx == len(lst):
                    self.queue.put("find far point")
                    problem = util.Problem(self.snake, apple, self.queue)
                    lst = agent.BreadthFirstSearch(problem)
                    if len(lst) == 0:
                        lst = agent.chooseFartestpoint(problem)
                    idx = 0
                    self.queue.put(lst)
            # Specify FPS
            self.clock.tick(self.FPS)
        pygame.quit()
        quit()


