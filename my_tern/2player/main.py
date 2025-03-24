import tkinter 
import json
import os
import random
from snake_class import Snake
from food_class import Food
from wall_class import Wall

WINDOW_WIDTH: int
WINDOW_HEIGHT: int
PIXEL_SIZE: int
BACKGROUND_COLOR: str
GAME_SPEED: int
KEY_QUEUE = []
KEY_QUEUE2 = []

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
    
def eat_food(food: Food, canvas: tkinter.Canvas):
    global score
    score += 1
    canvas.itemconfig(text_score, text=f"Score: {score}")
    canvas.delete(food.food_id)
    del food
    return Food(canvas)
    
def next_turn(snake: Snake, snake2:Snake, food: Food, wall: Wall, canvas: tkinter.Canvas):
    global KEY_QUEUE, KEY_QUEUE2

    if KEY_QUEUE:
        next_direction = KEY_QUEUE.pop(0) 
        if (next_direction == "Right" and snake.snake_direction != "Left") or \
           (next_direction == "Left" and snake.snake_direction != "Right") or \
           (next_direction == "Up" and snake.snake_direction != "Down") or \
           (next_direction == "Down" and snake.snake_direction != "Up"):
            snake.snake_direction = next_direction

    if KEY_QUEUE2:
        next_direction = KEY_QUEUE2.pop(0) 
        if (next_direction == "d" and snake2.snake_direction != "a") or \
           (next_direction == "a" and snake2.snake_direction != "d") or \
           (next_direction == "w" and snake2.snake_direction != "s") or \
           (next_direction == "s" and snake2.snake_direction != "w"):
            snake2.snake_direction = next_direction

    x, y = snake.coordinates[0]
    if snake.snake_direction == "Up":
        y -= PIXEL_SIZE
    elif snake.snake_direction == "Down":
        y += PIXEL_SIZE
    elif snake.snake_direction == "Right":
        x += PIXEL_SIZE
    elif snake.snake_direction == "Left":
        x -= PIXEL_SIZE
        
    a, b = snake2.coordinates[0]
    if snake2.snake_direction == "w":
        b -= PIXEL_SIZE
    elif snake2.snake_direction == "s":
        b += PIXEL_SIZE
    elif snake2.snake_direction == "d":
        a += PIXEL_SIZE
    elif snake2.snake_direction == "a":
        a -= PIXEL_SIZE

    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x+PIXEL_SIZE, y+PIXEL_SIZE, fill=snake.snake_color)
    snake.squares.insert(0, square)
    
    snake2.coordinates.insert(0, [a, b])
    square = canvas.create_rectangle(a, b, a+PIXEL_SIZE, b+PIXEL_SIZE, fill=snake2.snake_color)
    snake2.squares.insert(0, square)
    
    if [x, y] in snake.coordinates[1:]:
        close_game()
        return
    elif [x, y] in wall.coordinates:
        close_game()
        return
    elif [a, b] in snake2.coordinates[1:]:
        close_game()
        return
    elif [a,b] in wall.coordinates:
        close_game()
        return
    elif [x, y] == food.coordinates:
        food = eat_food(food, canvas)
        
        canvas.delete(snake2.squares[-1])
        del snake2.coordinates[-1]
        del snake2.squares[-1]
    elif [a, b] == food.coordinates:
        food = eat_food(food, canvas)

        canvas.delete(snake.squares[-1])
        del snake.coordinates[-1]
        del snake.squares[-1]
    else:
        canvas.delete(snake.squares[-1])
        del snake.coordinates[-1]
        del snake.squares[-1]
        
        canvas.delete(snake2.squares[-1])
        del snake2.coordinates[-1]
        del snake2.squares[-1]
    
    window.after(GAME_SPEED, next_turn, snake, snake2, food, wall, canvas)
    
def press_key(event=None):
    global KEY_QUEUE, KEY_QUEUE2
    if event.keysym in ["Right", "Left", "Up", "Down"] and (len(KEY_QUEUE) == 0 or KEY_QUEUE[-1] != event.keysym):
        KEY_QUEUE.append(event.keysym)
    if event.keysym in [ "w", "a", "s", "d"] and (len(KEY_QUEUE) == 0 or KEY_QUEUE[-1] != event.keysym):
        KEY_QUEUE2.append(event.keysym)
    
def close_game(event=None):
    global window
    if window.winfo_exists():
        for widget in window.winfo_children():
            widget.destroy()
        window.destroy()
    
def main():
    global window
    global score, text_score
    score = 0

    window = tkinter.Tk()
    
    get_data()
    window_setup()
    
    canvas = tkinter.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=BACKGROUND_COLOR)
    canvas.pack()
    
    text_score = canvas.create_text(PIXEL_SIZE, PIXEL_SIZE, anchor="nw", text=f"Score: {score}", font=("Helvetica", 16))
    
    food = Food(canvas)
    snake = Snake(canvas, 1, [1,1])
    snake2 = Snake(canvas, 2, [WINDOW_WIDTH/PIXEL_SIZE-1, 1])
    wall = Wall()
    wall.near_wall(canvas)
    
    for key in ["<Up>", "<Down>", "<Right>", "<Left>", "w", "a", "s", "d"]:
        window.bind(key, press_key)

    next_turn(snake, snake2, food, wall, canvas)

    window.mainloop()

main()