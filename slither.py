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
    def __init__(self, width, height):
        self.display_width = width
        self.display_height = height
        self.block_size = 20
        self.apple_thickness = 20
        self.FPS = 1000
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

    def runGame(self, method):
        def console(request):
            while True:
                if not request.empty():
                    print(request.get())

        thread_console = threading.Thread(target=console, args=(self.queue,))
        thread_console.daemon = True
        thread_console.start()
        self.gameIntro()
        self.game_loop(method)

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
    def printLog(self,msg):
        self.queue.put(msg)
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
        if self.direction == "idle":
            head = self.img
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
    def game_loop(self, method):
        self.direction = "right"
        game_exit = False
        game_over = False
        # Will be the leader of the #1 block of the snake
        snake_list = [[self.display_width/2, self.display_height/2]]
        #snake_length = 1
        ## My Code Here
        self.snake = util.Snake([self.display_width/2, self.display_height/2], snake_list, self.display_width, self.display_height)
        apple = self.rand_apple_gen(self.snake)
        problem = util.Problem(self.snake ,apple, self.queue)
        lst = method(problem)
        idx = 0
        ##My Code Here
        while not game_exit:
            if game_over is True:
                self.message_to_screen("Game Over", Color().red, y_displace=-50, size="large")
                self.message_to_screen("Press C to play again or Q to quit", Color().black,
                                  y_displace=50, size="medium")
                pygame.display.update()

            while game_over is True:
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
                            self.game_loop(method)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self. direction = "left"
                    elif event.key == pygame.K_RIGHT:
                        self.direction = "right"
                    elif event.key == pygame.K_UP:
                        self.direction = "up"
                    elif event.key == pygame.K_DOWN:
                        self.direction = "down"
                    elif event.key == pygame.K_p:
                        self.pause()

            if idx<len(lst):
                self.direction = lst[idx]
                idx += 1
            else:
                self.direction = 'idle'

            # Define GAMEOVER Situation
            if self.snake.snakehead[0] >= self.display_width or  self.snake.snakehead[0] < 0 or  self.snake.snakehead[1] >= self.display_height\
                    or  self.snake.snakehead[1] < 0:
                game_over = True
            for each_segment in snake_list[:-1]:
                if each_segment == self.snake.snakehead:
                    game_over = True

            if self.direction != 'idle':
                self.snake.move(self.direction)

            self.gameDisplay.fill(Color().white)
            self.gameDisplay.blit(self.img2, [apple[0], apple[1], self.apple_thickness,
                                     self.apple_thickness])

            self.snakeMove(self.snake.snakebody)
            self.printScore(len(self.snake.snakebody) - 1)
            pygame.display.update()

            # Define the steps you wanna take next time TOMLIAO
            if self.snake.snakehead == apple:
                apple = self.rand_apple_gen(self.snake)
                self.snake.snake_length += 1
                problem = util.Problem(self.snake,apple, self.queue)
                lst = method(problem)
                idx = 0
            else:
                if idx == len(lst):
                    problem = util.Problem(self.snake, apple, self.queue)
                    lst = agent.BreadthFirstSearch(problem)
                    if len(lst) == 0:
                        lst = agent.chooseFartestpoint(problem)
                    idx = 0
            # Specify FPS
            self.clock.tick(self.FPS)
        pygame.quit()
        quit()


