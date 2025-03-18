import tkinter 
import json
import os
from snake_class import Snake
from food_class import Food

WINDOW_WIDTH: int
WINDOW_HEIGHT: int
PIXEL_SIZE: int
BACKGROUND_COLOR: str
FOOD_COLOR: str
SNAKE_COLOR: str
GAME_SPEED: int

def get_data():
    global WINDOW_WIDTH, WINDOW_HEIGHT, BACKGROUND_COLOR, PIXEL_SIZE, FOOD_COLOR, SNAKE_COLOR, GAME_SPEED
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "data.json")
    with open(data_path, 'r') as f:
        data = json.load(f)
        WINDOW_WIDTH = data["window"]["window_width"]
        WINDOW_HEIGHT = data["window"]["window_height"]
        BACKGROUND_COLOR = data["canvas"]["background_color"]
        PIXEL_SIZE = data["canvas"]["pixel_size"]
        SNAKE_COLOR = data["snake"]["snake_color"]
        FOOD_COLOR = data["food"]["food_color"]
        GAME_SPEED = 500 - (25 * data["game"]["game_speed"])
        
def window_setup():
    window.title("Snake Game")
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    x = int((screenwidth/2)-(WINDOW_WIDTH/2))
    y = int((screenheight/2)-(WINDOW_HEIGHT/2))
    window.geometry(F"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
    window.resizable(False, False)
    
def next_tern(snake: Snake, food: Food, canvas: tkinter.Canvas):
    x, y = snake.coordinates[0]
    if direction == "up":
        y -= PIXEL_SIZE
    elif direction == "down":
        y += PIXEL_SIZE
    elif direction == "right":
        x += PIXEL_SIZE
    elif direction == "left":
        x -= PIXEL_SIZE

    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x+PIXEL_SIZE, y+PIXEL_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)
    
    canvas.delete(snake.squares[-1])
    del snake.coordinates[-1]
    del snake.squares[-1]
    
    window.after(GAME_SPEED, next_tern, snake, food, canvas)
    
def move_up(event=None):
    global direction
    if direction != 'down':
        direction = 'up'

def move_down(event=None):
    global direction
    if direction != 'up':
        direction = 'down'

def move_left(event=None):
    global direction
    if direction != 'right':
        direction = 'left'

def move_right(event=None):
    global direction
    if direction != 'left':
        direction = 'right'
    
def close_game(event=None):
    window.destroy()
    
def main():
    global window 
    global direction
    window = tkinter.Tk()
    get_data()
    window_setup()
    canvas = tkinter.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=BACKGROUND_COLOR)
    canvas.pack()
    direction = 'down'
    food = Food(canvas)
    snake = Snake(canvas)
    next_tern(snake, food, canvas)
    window.bind("<Up>", move_up)
    window.bind("<Down>", move_down)
    window.bind("<Right>", move_right)
    window.bind("<Left>", move_left)
    window.bind("<Escape>", close_game)
    window.mainloop()

main()