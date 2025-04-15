import pygame
import sys
import random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False

        self.head_up=pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down=pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right=pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left=pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up=pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down=pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right=pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left=pygame.image.load('Graphics/tail_left.png').convert_alpha()

        
        self.body_vertical=pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal=pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr=pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl=pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br=pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl=pygame.image.load('Graphics/body_bl.png').convert_alpha()

        self.crunch_sound=pygame.mixer.Sound('Crunch.wav')
    
    def draw_snake(self):
        for index, block in enumerate(self.body):
            body_rect = pygame.Rect(block.x *cell_size, block.y*cell_size, cell_size, cell_size)
            if index !=0: previous_block = self.body[index-1] - block
            if index !=len(self.body)-1: next_block = self.body[index+1] - block
            if index == 0:
                if main_game.snake.direction == Vector2(1, 0):
                    screen.blit(self.head_right, body_rect)
                elif main_game.snake.direction == Vector2(-1, -0):
                    screen.blit(self.head_left, body_rect)
                elif main_game.snake.direction == Vector2(0, 1):
                    screen.blit(self.head_down, body_rect)
                elif main_game.snake.direction == Vector2(0, -1):
                    screen.blit(self.head_up, body_rect)
                else:
                    screen.blit(self.head_right, body_rect)
            elif index == len(self.body)-1:
                if self.body[-2]-self.body[-1] == Vector2(-1, 0):
                    screen.blit(self.tail_right, body_rect)
                elif self.body[-2]-self.body[-1] == Vector2(1, 0):
                    screen.blit(self.tail_left, body_rect)
                elif self.body[-2]-self.body[-1] == Vector2(0, -1):
                    screen.blit(self.tail_down, body_rect)
                elif self.body[-2]-self.body[-1] == Vector2(0, 1):
                    screen.blit(self.tail_up, body_rect)
            else:
                previous_block = self.body[index-1] - block
                next_block = self.body[index+1] - block
                if previous_block.y == -1 and next_block.x == 1 or previous_block.x == 1 and next_block.y == -1:
                    screen.blit(self.body_tr, body_rect)
                elif previous_block.y == -1 and next_block.x == -1 or previous_block.x == -1 and next_block.y == -1:
                    screen.blit(self.body_tl, body_rect)
                elif previous_block.y == 1 and next_block.x == 1 or previous_block.x == 1 and next_block.y == 1:
                    screen.blit(self.body_br, body_rect)
                elif previous_block.y == 1 and next_block.x == -1 or previous_block.x == -1 and next_block.y == 1:
                    screen.blit(self.body_bl, body_rect)
                elif previous_block - next_block == Vector2(2, 0) or previous_block - next_block == Vector2(-2, -0):
                    screen.blit(self.body_horizontal, body_rect)
                elif previous_block - next_block == Vector2(0, 2) or previous_block - next_block == Vector2(0, -2):
                    screen.blit(self.body_vertical, body_rect)
    
    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0]+self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0]+self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction=Vector2(0,0)

class FRUIT:
    def __init__(self):
        self.randomize()
        self.pos = Vector2(self.x, self.y)
    
    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class WALL:
    def __init__(self):
        self.pos = None
    
    def draw_wall(self):
        wall_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        screen.blit(wall_image, wall_rect)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.walls = []
        self.apples_eaten = 0
        self.move_interval = 150
    
    def update(self):
        self.snake.move_snake()
        self.check_collisions()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        for wall in self.walls:
            wall.draw_wall()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collisions(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
            self.apples_eaten += 1

            empty_positions = [
                    Vector2(x, y)
                    for x in range(cell_number)
                    for y in range(cell_number)
                    if Vector2(x, y) not in self.snake.body
                    and Vector2(x, y) != self.fruit.pos
                    and Vector2(x, y) not in [w.pos for w in self.walls]
                ]
            if empty_positions: 
                    new_wall = WALL()
                    new_wall.pos = random.choice(empty_positions)
                    self.walls.append(new_wall)
                
            if self.apples_eaten % 3 == 0:
                    self.move_interval = max(50, self.move_interval - 10)
                    pygame.time.set_timer(SCREEN_UPDATE, self.move_interval)

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0<=self.snake.body[0].y < cell_number:
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

        for wall in self.walls:
            if wall.pos == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()
        self.walls = []
        self.apples_eaten = 0
        self.move_interval = 150
        pygame.time.set_timer(SCREEN_UPDATE, self.move_interval)

    def draw_grass(self):
        grass_color=(167,209,61)
        for row in range(cell_number):
            if row %2 ==0:
                for col in range(cell_number):
                    if col %2 ==0:
                        grass_rect = pygame.Rect(col*cell_size,row*cell_size,cell_size, cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            else:
                for col in range(cell_number):
                    if col %2 !=0:
                        grass_rect = pygame.Rect(col*cell_size,row*cell_size,cell_size, cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body)-3)
        score_surface = game_font.render(score_text,True,(56,74,12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width+score_rect.width+6,apple_rect.height)
        
        pygame.draw.rect(screen,(167,209,61),bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(apple,apple_rect)
        pygame.draw.rect(screen,(56,74,12),bg_rect,2)

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_size = 40
cell_number = 18
screen = pygame.display.set_mode((cell_size*cell_number, cell_size*cell_number))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
wall_image = pygame.image.load('Graphics/wall.jpg').convert_alpha()
game_font = pygame.font.SysFont('Calibri', 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if not main_game.snake.direction == Vector2(0, 1):
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if not main_game.snake.direction == Vector2(0, -1):
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_RIGHT:
                if not main_game.snake.direction == Vector2(-1, 0):
                    main_game.snake.direction = Vector2(1,0)
            if event.key == pygame.K_LEFT:
                if not main_game.snake.direction == Vector2(1, 0):
                    main_game.snake.direction = Vector2(-1,0)      

    screen.fill((150,190,15))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)