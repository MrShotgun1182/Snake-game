import tkinter
from snake_class import Snake
from food_class import Food
from wall_class import Wall

def snake_collision(window: tkinter.Tk, snake: Snake, snake2: Snake, wall: Wall):
    if  snake.coordinates[0] in snake.coordinates[1:] or \
        snake.coordinates[0] in snake2.coordinates or \
        snake.coordinates[0] in wall.coordinates:
        close_game(window, 2)
        return True
    
    if  snake2.coordinates[0] in snake2.coordinates[1:] or \
        snake2.coordinates[0] in snake.coordinates or \
        snake2.coordinates[0] in wall.coordinates:
        close_game(window, 1)
        return True
    
    if snake.coordinates[0] == snake2.coordinates[0]:
        close_game(window, 0)
        return True
    
    return False

def food_collision(snake: Snake, snake2: Snake, food: Food, canvas: tkinter.Canvas, text_score, text_score2):
    if snake.coordinates[0] == food.coordinates:
        snake2.delete_tail(canvas)
        return eat_food(food, snake, canvas, 1, text_score, text_score2), True
    elif snake2.coordinates[0] == food.coordinates:
        snake.delete_tail(canvas)
        return eat_food(food, snake2, canvas, 2, text_score, text_score2), True
    return food, False

def eat_food(food: Food, snake: Snake, canvas: tkinter.Canvas, snake_number, text_score, text_score2):
    snake.snake_score += 1
    if snake_number == 1:
        canvas.itemconfig(text_score, text=f"Score1: {snake.snake_score}")
    else:
        canvas.itemconfig(text_score2, text=F"Score2: {snake.snake_score}")
    
    canvas.delete(food.food_id)
    del food
    return Food(canvas)

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