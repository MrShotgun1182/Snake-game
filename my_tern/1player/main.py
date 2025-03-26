import tkinter 
import json
import os
from snake_class import Snake
from food_class import Food
from wall_class import Wall
from keys_class import Keys
from function import *

WINDOW_WIDTH: int
WINDOW_HEIGHT: int
PIXEL_SIZE: int
BACKGROUND_COLOR: str
GAME_SPEED: int
KEY_QUEUE = []

def get_data():
    global WINDOW_WIDTH, WINDOW_HEIGHT, BACKGROUND_COLOR, PIXEL_SIZE, GAME_SPEED
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "data.json")
    with open(data_path, 'r') as f:
        data = json.load(f)
        WINDOW_WIDTH = data["window"]["window_width"]
        WINDOW_HEIGHT = data["window"]["window_height"]
        BACKGROUND_COLOR = data["canvas"]["background_color"]
        PIXEL_SIZE = data["canvas"]["pixel_size"]
        GAME_SPEED = 500 - (25 * data["game"]["game_speed"])
        
def window_setup(window: tkinter.Tk):
    window.title("Snake Game")
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    x = int((screenwidth/2)-(WINDOW_WIDTH/2))
    y = int((screenheight/2)-(WINDOW_HEIGHT/2))
    window.geometry(F"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
    window.resizable(False, False)
    
def next_turn(window: tkinter.Tk, snake: Snake, food: Food, wall: Wall, canvas: tkinter.Canvas, keys: Keys):
    if keys.KEY_QUEUE:
        keys.handel_key(snake)
    
    snake.new_head(canvas)

    food, status = food_collision(snake, food, canvas, text_score)
    if  not snake_collision(window, snake, wall) and not status:
        snake.delete_tail(canvas)
    
    window.after(GAME_SPEED, next_turn, window, snake, food, wall, canvas, keys)
    
def main():
    global text_score

    window = tkinter.Tk()
    
    get_data()
    window_setup(window)
    
    canvas = tkinter.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=BACKGROUND_COLOR)
    canvas.pack()
    
    text_score = canvas.create_text(PIXEL_SIZE, PIXEL_SIZE, anchor="nw", text=f"Score1: {0}", font=("Helvetica", 16))
    
    food = Food(canvas)
    snake = Snake(canvas, 1, [(WINDOW_WIDTH/PIXEL_SIZE)-2, 1])
    wall = Wall()
    wall.near_wall(canvas)
    keys = Keys(window)

    next_turn(window, snake, food, wall, canvas, keys) 
    
    window.mainloop()

main()