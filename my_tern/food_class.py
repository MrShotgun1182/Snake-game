import tkinter
import json
import os
import random

class Food:
    def __init__(self ,canvas: tkinter.Canvas):
        curent_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(curent_dir, 'data.json')
        with open(data_path, 'r') as f:
            data = json.load(f)
            self.food_color = data['food']['food_color']
            self.pixel_size = data["canvas"]["pixel_size"]
            x = random.randint(0, int((data["window"]["window_width"]/self.pixel_size))-1) * self.pixel_size
            y = random.randint(0, int((data["window"]["window_height"]/self.pixel_size))-1) * self.pixel_size
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x+self.pixel_size, y+self.pixel_size, fill=self.food_color)
            
        