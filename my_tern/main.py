import tkinter 
import json
import os
from snake_class import Snake
from food_class import Food

WINDOW_WIDTH: int
WINDOW_HEIGHT: int
BACKGROUND_COLOR: str

def get_data():
    global WINDOW_WIDTH, WINDOW_HEIGHT, BACKGROUND_COLOR
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "data.json")
    with open(data_path, 'r') as f:
        data = json.load(f)
        WINDOW_WIDTH = data["window"]["window_width"]
        WINDOW_HEIGHT = data["window"]["window_height"]
        BACKGROUND_COLOR = data["canvas"]["background_color"]
        
def window_setup(window: tkinter.Tk):
    window.title("Snake Game")
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    x = int((screenwidth/2)-(WINDOW_WIDTH/2))
    y = int((screenheight/2)-(WINDOW_HEIGHT/2))
    window.geometry(F"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
    

def main():
    window = tkinter.Tk()

    get_data()
    window_setup(window)
    canvas = tkinter.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=BACKGROUND_COLOR)
    canvas.pack()
    food = Food(canvas)
    snake = Snake(canvas)
    
    window.mainloop()

main()