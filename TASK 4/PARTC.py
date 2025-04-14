from tkinter import *
import random

GAME_WIDTH = 1000
GAME_HEIGHT = 600
SPEED = 200
SPACE_SIZE = 40
BODY_SIZE = 3
SNAKE_COLOUR = "#00FF00"
FOOD_COLOUR = "#FF0000"
BACKGROUND_COLOUR = "#000000"

class Snake:
    
    def __init__(self):
        self.body_Size = BODY_SIZE
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_SIZE):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOUR, tag = "snake")
            self.squares.append(square)

class Food:

    def __init__(self):

        x = random.randint(0, (GAME_WIDTH//SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE)-1) * SPACE_SIZE 

        self.coordinates = [x, y]

        canvas.create_oval(x,y,x+SPACE_SIZE, y+SPACE_SIZE, fill =FOOD_COLOUR, tag = "food")

def next_turn(snake, food):
    
    x, y = snake.coordinates[0]

    if dir == "up":
        y-=SPACE_SIZE
    elif dir == "down":
        y+=SPACE_SIZE
    elif dir == "left":
        x-=SPACE_SIZE
    elif dir == "right":
        x+=SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill = SNAKE_COLOUR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()

    else:
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food)

def change_dir(new_dir):
    
    global dir

    if new_dir == 'left':
        if dir != 'right':
            dir = new_dir
    elif new_dir == 'right':
        if dir != 'left':
            dir = new_dir
    elif new_dir == 'up':
        if dir != 'down':
            dir = new_dir
    elif new_dir == 'down':
        if dir != 'up':
            dir = new_dir

def check_collisions(snake):
    
    x, y = snake.coordinates[0]

    if x < 0 or x>=GAME_WIDTH:
        print("Game Over")
        return True
    
    elif y < 0 or y>=GAME_HEIGHT:
        print("Game Over")
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("Game Over")
            return True
        

def game_over():

    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('consolas', 70), text="Game Over", fill = "red", tag="gameover")

window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
dir = 'down'

label = Label(window, text = "Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOUR, height = GAME_HEIGHT, width = GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event : change_dir('left'))
window.bind('<Right>', lambda event : change_dir('right'))
window.bind('<Up>', lambda event : change_dir('up'))
window.bind('<Down>', lambda event : change_dir('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()