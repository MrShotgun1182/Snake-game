import tkinter
import threading
import json
import os
from snake_class import Snake

class Keys:
    def __init__(self, window:tkinter.Tk):
        self.window = window
        self.KEY_QUEUE = []
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, "data.json")
        with open(data_path, 'r') as f:
            data = json.load(f)
            self.snake_keys = data["snake1"]["snake_keys"]
            self.snake2_keys = data["snake2"]["snake_keys"]

        for key in self.snake_keys:
            window.bind(key, self.press_key)

        for key in self.snake2_keys:
            window.bind(key, self.press_key)
    
    def press_key(self, event=None):
        if event.keysym in ["Right", "Left", "Up", "Down", "w", "a", "s", "d"] and (len(self.KEY_QUEUE) == 0 or self.KEY_QUEUE[-1] != event.keysym):
            self.KEY_QUEUE.append(event.keysym)
            
    def handel_key(self, snake: Snake, snake2: Snake):
        next_direction = self.KEY_QUEUE.pop(0) 
        if next_direction == "Right" and snake.snake_direction != "Left":
            snake.snake_direction = next_direction
        elif next_direction == "d" and snake2.snake_direction != "a":
            snake2.snake_direction = next_direction
        elif next_direction == "Left" and snake.snake_direction != "Right":
            snake.snake_direction = next_direction
        elif next_direction == "a" and snake2.snake_direction != "d":
            snake2.snake_direction = next_direction
        elif next_direction == "Up" and snake.snake_direction != "Down":
            snake.snake_direction = next_direction
        elif next_direction == "w" and snake2.snake_direction != "s":
            snake2.snake_direction = next_direction
        elif next_direction == "Down" and snake.snake_direction != "Up":
            snake.snake_direction = next_direction
        elif next_direction == "s" and snake2.snake_direction != "w":
            snake2.snake_direction = next_direction
    
    def fun_key_thread(self, snake: Snake, snake2: Snake):
        if self.KEY_QUEUE:
            self.handel_key(snake, snake2)
        self.window.after(50, self.fun_key_thread, snake, snake2)
        