import tkinter
from snake_class import Snake
from food_class import Food
from wall_class import Wall
from collect_data import Collector
import time

def snake_collision(window: tkinter.Tk, snake: Snake, wall: Wall, collector: Collector):
    if  snake.coordinates[0] in snake.coordinates[1:] or \
        snake.coordinates[0] in wall.coordinates:
        collector.save_rows()
        close_game(window)
        return True
    
    return False

def eat_food(food: Food, snake: Snake, wall: Wall, canvas: tkinter.Canvas, text_score,):
    snake.snake_score += food.score
    
    canvas.itemconfig(text_score, text=f"Score: {snake.snake_score}")
    
    canvas.delete(food.food_id)

    food.new_food(snake, wall, canvas)

def food_collision(snake: Snake, food: Food, wall: Wall, canvas: tkinter.Canvas, text_score):
    if snake.coordinates[0] == food.coordinates:
        return eat_food(food, snake, wall, canvas, text_score), True
    return False

def close_game(window:tkinter.Tk):
    time.sleep(2)
    for widget in window.winfo_children():
        widget.destroy()
    window.destroy()