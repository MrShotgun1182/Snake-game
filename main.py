from tkinter import *
from snake_class import Snake
from food_class import Food
from function import *


GAME_WIDTH = 700
GAME_HEIGHT  = 700
SPEED = 50
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


window = Tk()
window.title('snake game')
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

# set window in center screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('Left', direction=direction))
window.bind('<Down>', lambda event: change_direction('Down', direction=direction))
window.bind('<Right>', lambda event: change_direction('Right', direction=direction))
window.bind('<Up>', lambda event: change_direction('Up', direction=direction))

snake = Snake(BODY_PARTS=BODY_PARTS, canvas=canvas, SPACE_SIZE=SPACE_SIZE, SNAKE_COLOR=SNAKE_COLOR)
food = Food(GAME_HEIGHT=GAME_HEIGHT, GAME_WIDTH=GAME_WIDTH, SPACE_SIZE=SPACE_SIZE, FOOD_COLOR=FOOD_COLOR, canvas=canvas)
next_turn(snake, food, SPACE_SIZE, direction, window, SPEED, canvas, SNAKE_COLOR)


window.mainloop()

