import tkinter
import json
import os
import random

class Food:
    def __init__(self ,canvas: tkinter.Canvas):
        self.score = 1
        self.color: str
        curent_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(curent_dir, 'data.json')
        with open(data_path, 'r') as f:
            data = json.load(f)
            self.food_color = data['food']['food_color']
            self.food_score = data['food']['food_score']
            self.pixel_size = data["canvas"]["pixel_size"]
            self.window_width = data["window"]["window_width"]
            self.window_height = data["window"]["window_height"]
            self.special_food_color = data['food']['special_food_color']
            self.special_food_score = data['food']['special_food_score']
            self.special_food_chans = data['food']['special_food_chans']
        self.new_food(canvas)

    def __select_food(self):
        if random.random() > self.special_food_chans:
            self.score = self.food_score
            self.color = self.food_color
        else:
            self.score = self.special_food_score
            self.color = self.special_food_color


    def new_food(self, canvas):
        self.__select_food()
        x = random.randint(1, int((self.window_width/self.pixel_size))-2) * self.pixel_size
        y = random.randint(1, int((self.window_height/self.pixel_size))-2) * self.pixel_size
        self.coordinates = [x, y]
        self.food_id = canvas.create_oval(x, y, x+self.pixel_size, y+self.pixel_size, fill=self.color)