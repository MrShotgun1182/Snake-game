import tkinter 
import json
import os
from snake_class import Snake
from food_class import Food
from wall_class import Wall
from keys_class import Keys

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
        
def window_setup():
    window.title("Snake Game")
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    x = int((screenwidth/2)-(WINDOW_WIDTH/2))
    y = int((screenheight/2)-(WINDOW_HEIGHT/2))
    window.geometry(F"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
    window.resizable(False, False)
    
def eat_food(food: Food, snake: Snake, canvas: tkinter.Canvas, snake_number):
    if snake_number == 1:
        snake.snake_score += 1
        canvas.itemconfig(text_score, text=f"Score: {snake.snake_score}")
    else:
        snake.snake_score += 1
        canvas.itemconfig(text_score2, text=F"Score: {snake.snake_score}")
    
    canvas.delete(food.food_id)
    del food
    return Food(canvas)

def food_collision(snake: Snake, snake2: Snake, food: Food, canvas: tkinter.Canvas):
    if snake.coordinates[0] == food.coordinates:
        snake2.delete_tail(canvas)
        return eat_food(food, snake, canvas, 1), True
    elif snake2.coordinates[0] == food.coordinates:
        snake.delete_tail(canvas)
        return eat_food(food, snake2, canvas, 2), True
    return food, False
    

def snake_collision(snake: Snake, snake2: Snake, wall: Wall):
    if  snake.coordinates[0] in snake.coordinates[1:] or \
        snake.coordinates[0] in snake2.coordinates or \
        snake.coordinates[0] in wall.coordinates:
        close_game()
        return True
    
    if  snake2.coordinates[0] in snake2.coordinates[1:] or \
        snake2.coordinates[0] in snake.coordinates or \
        snake2.coordinates[0] in wall.coordinates:
        close_game()
        return True
    
    if snake.coordinates[0] == snake2.coordinates[0]:
        close_game()
        return True
    
    return False
    
def next_turn(snake: Snake, snake2:Snake, food: Food, wall: Wall, canvas: tkinter.Canvas, keys: Keys):
    global KEY_QUEUE

    if keys.KEY_QUEUE:
        keys.handel_key(snake, snake2)
    
    snake.new_head(canvas)
    snake2.new_head(canvas)

    food, status = food_collision(snake, snake2, food, canvas)
    if  not snake_collision(snake, snake2, wall) and \
        not status:
        snake2.delete_tail(canvas)
        snake.delete_tail(canvas)
    
    window.after(GAME_SPEED, next_turn, snake, snake2, food, wall, canvas, keys)
    
def close_game(event=None):
    global window
    if window.winfo_exists():
        for widget in window.winfo_children():
            widget.destroy()
        window.destroy()
    
def main():
    global window
    global text_score, text_score2

    window = tkinter.Tk()
    
    get_data()
    window_setup()
    
    canvas = tkinter.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=BACKGROUND_COLOR)
    canvas.pack()
    
    text_score = canvas.create_text(WINDOW_WIDTH - (PIXEL_SIZE*5), PIXEL_SIZE, anchor="nw", text=f"Score: {0}", font=("Helvetica", 16))
    text_score2 = canvas.create_text(PIXEL_SIZE, PIXEL_SIZE, anchor="nw", text=f"Score: {0}", font=("Helvetica", 16))
    
    food = Food(canvas)
    snake = Snake(canvas, 1, [(WINDOW_WIDTH/PIXEL_SIZE)-2, 1])
    snake2 = Snake(canvas, 2, [1,1])
    wall = Wall()
    wall.near_wall(canvas)
    keys = Keys(window)

    window.bind("<Escape>", close_game)

    next_turn(snake, snake2, food, wall, canvas, keys) 
    

    window.mainloop()

main()