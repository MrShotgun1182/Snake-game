import tkinter
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

        for key in self.snake_keys:
            key = "<" + key + ">"
            window.bind(key, self.press_key)
    
    def press_key(self, event=None):
        if event.keysym in self.snake_keys and (len(self.KEY_QUEUE) == 0 or self.KEY_QUEUE[-1] != event.keysym):
            self.KEY_QUEUE.append(event.keysym)
            
    def handel_key(self, snake: Snake):
        next_direction = self.KEY_QUEUE.pop(0) 
        if next_direction == self.snake_keys[2] and snake.snake_direction != self.snake_keys[3]:
            snake.snake_direction = next_direction
        elif next_direction == self.snake_keys[3] and snake.snake_direction != self.snake_keys[2]:
            snake.snake_direction = next_direction
        elif next_direction == self.snake_keys[0] and snake.snake_direction != self.snake_keys[1]:
            snake.snake_direction = next_direction
        elif next_direction == self.snake_keys[1] and snake.snake_direction != self.snake_keys[0]:
            snake.snake_direction = next_direction
        