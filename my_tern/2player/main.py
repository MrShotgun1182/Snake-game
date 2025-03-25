import tkinter 
import json
import os
from multiprocessing import Process
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

def delete_tail(snake: Snake, canvas: tkinter.Canvas):
    canvas.delete(snake.squares[-1])
    del snake.coordinates[-1]
    del snake.squares[-1]

def food_collision(snake: Snake, snake2: Snake, food: Food, canvas: tkinter.Canvas):
    if snake.coordinates[0] == food.coordinates:
        delete_tail(snake2, canvas)
        return eat_food(food, snake, canvas, 1), True
    elif snake2.coordinates[0] == food.coordinates:
        delete_tail(snake, canvas)
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

# def handel_key(snake: Snake, snake2: Snake):
#     global KEY_QUEUE
#     next_direction = KEY_QUEUE.pop(0) 
#     if next_direction == "Right" and snake.snake_direction != "Left":
#         snake.snake_direction = next_direction
#     elif next_direction == "d" and snake2.snake_direction != "a":
#         snake2.snake_direction = next_direction
#     elif next_direction == "Left" and snake.snake_direction != "Right":
#         snake.snake_direction = next_direction
#     elif next_direction == "a" and snake2.snake_direction != "d":
#         snake2.snake_direction = next_direction
#     elif next_direction == "Up" and snake.snake_direction != "Down":
#         snake.snake_direction = next_direction
#     elif next_direction == "w" and snake2.snake_direction != "s":
#         snake2.snake_direction = next_direction
#     elif next_direction == "Down" and snake.snake_direction != "Up":
#         snake.snake_direction = next_direction
#     elif next_direction == "s" and snake2.snake_direction != "w":
#         snake2.snake_direction = next_direction
    
def next_turn(snake: Snake, snake2:Snake, food: Food, wall: Wall, canvas: tkinter.Canvas):
    global KEY_QUEUE

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
    square2 = canvas.create_rectangle(a, b, a+PIXEL_SIZE, b+PIXEL_SIZE, fill=snake2.snake_color)
    snake2.squares.insert(0, square2)

    food, status = food_collision(snake, snake2, food, canvas)
    if  not snake_collision(snake, snake2, wall) and \
        not status:
        delete_tail(snake, canvas)
        delete_tail(snake2, canvas)
    
    window.after(GAME_SPEED, next_turn, snake, snake2, food, wall, canvas)
    
# def press_key(event=None):
#     global KEY_QUEUE
#     if event.keysym in ["Right", "Left", "Up", "Down", "w", "a", "s", "d"] and (len(KEY_QUEUE) == 0 or KEY_QUEUE[-1] != event.keysym):
#         KEY_QUEUE.append(event.keysym)
    
# def fun_key_thread(snake, snake2):
#     global KEY_QUEUE
#     while True:
#         if KEY_QUEUE:
#             handel_key(snake, snake2)
    
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
    
    # for key in ["<Up>", "<Down>", "<Right>", "<Left>", "w", "a", "s", "d"]:
    #     window.bind(key, press_key)

    window.bind("<Escape>", close_game)
    
    next_turn(snake, snake2, food, wall, canvas)

    window.mainloop()

main()