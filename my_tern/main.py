import tkinter 
import json
import os
from snake_class import Snake
from food_class import Food
from wall_class import Wall

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
    
def eat_food(food: Food, canvas: tkinter.Canvas):
    global score
    score += 1
    canvas.itemconfig(text_score, text=f"Score: {score}")
    canvas.delete(food.food_id)
    del food
    return Food(canvas)
    
def next_turn(snake: Snake, food: Food, wall: Wall, canvas: tkinter.Canvas):
    global direction, KEY_QUEUE

    if KEY_QUEUE:
        next_direction = KEY_QUEUE.pop(0) 
        if (next_direction == "Right" and direction != "Left") or \
           (next_direction == "Left" and direction != "Right") or \
           (next_direction == "Up" and direction != "Down") or \
           (next_direction == "Down" and direction != "Up"):
            direction = next_direction

    x, y = snake.coordinates[0]
    if direction == "Up":
        y -= PIXEL_SIZE
    elif direction == "Down":
        y += PIXEL_SIZE
    elif direction == "Right":
        x += PIXEL_SIZE
    elif direction == "Left":
        x -= PIXEL_SIZE

    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x+PIXEL_SIZE, y+PIXEL_SIZE, fill=snake.snake_color)
    snake.squares.insert(0, square)
    
    if [x, y] in snake.coordinates[1:]:
        close_game()
        return
    elif [x, y] in wall.coordinates:
        close_game()
        return
    elif [x, y] == food.coordinates:
        food = eat_food(food, canvas)
    else:
        canvas.delete(snake.squares[-1])
        del snake.coordinates[-1]
        del snake.squares[-1]
    
    window.after(GAME_SPEED, next_turn, snake, food, wall, canvas)
    
def press_key(event=None):
    global KEY_QUEUE
    # اضافه کردن کلید به صف اگر از قبل وجود نداشته باشد
    if event.keysym in ["Right", "Left", "Up", "Down"] and (len(KEY_QUEUE) == 0 or KEY_QUEUE[-1] != event.keysym):
        KEY_QUEUE.append(event.keysym)
    
def close_game(event=None):
    global window
    if window.winfo_exists():
        for widgt in window.winfo_children():
            widgt.destroy()
        window.destroy()
    del window
    
def main():
    global window, direction
    global score, text_score
    score = 0
    window = tkinter.Tk()
    get_data()
    window_setup()
    canvas = tkinter.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=BACKGROUND_COLOR)
    canvas.pack()
    text_score = canvas.create_text(PIXEL_SIZE, PIXEL_SIZE, anchor="nw", text=f"Score: {score}", font=("Helvetica", 16))
    direction = 'Down'
    food = Food(canvas)
    snake = Snake(canvas)
    wall = Wall()
    wall.near_wall(canvas)
    next_turn(snake, food, wall, canvas)
    window.bind("<Up>", press_key)
    window.bind("<Down>", press_key)
    window.bind("<Right>", press_key)
    window.bind("<Left>", press_key)
    window.bind("<Escape>", close_game)
    window.mainloop()

main()