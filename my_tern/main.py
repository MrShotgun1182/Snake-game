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
SNAKE_COLOR: str
GAME_SPEED: int

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
    square = canvas.create_rectangle(x, y, x+PIXEL_SIZE, y+PIXEL_SIZE, fill=snake.snake_color)
    snake.squares.insert(0, square)
    
    if [x, y] in snake.coordinates[1:]:
        close_game()
        return
    elif [x,y] in wall.coordinates:
        close_game()
        return
    elif [x, y] == food.coordinates:
        food = eat_food(food, canvas)
    else:
        canvas.delete(snake.squares[-1])
        del snake.coordinates[-1]
        del snake.squares[-1]
    
    window.after(GAME_SPEED, next_turn, snake, food, wall, canvas)
    
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
    direction = 'down'
    food = Food(canvas)
    snake = Snake(canvas)
    wall = Wall()
    wall.near_wall(canvas)
    next_turn(snake, food,wall, canvas)
    window.bind("<Up>", move_up)
    window.bind("<Down>", move_down)
    window.bind("<Right>", move_right)
    window.bind("<Left>", move_left)
    window.bind("<Escape>", close_game)
    window.mainloop()

main()