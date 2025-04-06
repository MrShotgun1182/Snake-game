import tkinter
from snake_class import Snake
from food_class import Food
from wall_class import Wall
from collect_data import Collector

def snake_collision(window: tkinter.Tk, snake: Snake, wall: Wall, collector: Collector):
    if  snake.coordinates[0] in snake.coordinates[1:] or \
        snake.coordinates[0] in wall.coordinates:
        collector.save_rows()
        close_game(window, 2)
        return True
    
    return False

def eat_food(food: Food, snake: Snake, canvas: tkinter.Canvas, text_score,):
    snake.snake_score += food.score
    canvas.itemconfig(text_score, text=f"Score1: {snake.snake_score}")
    
    canvas.delete(food.food_id)
    food.new_food(canvas)

def food_collision(snake: Snake, food: Food, canvas: tkinter.Canvas, text_score):
    if snake.coordinates[0] == food.coordinates:
        return eat_food(food, snake, canvas, text_score), True
    return False

def close_game(window:tkinter.Tk, senario):
    if window.winfo_exists():
        for widget in window.winfo_children():
            widget.destroy()
        window.destroy()
    window = tkinter.Tk()
    window.geometry("400x50")
    window.title("end game")
    label = tkinter.Label(window, text=F"player {senario} win!!!", font=20)
    label.pack()
    window.mainloop()