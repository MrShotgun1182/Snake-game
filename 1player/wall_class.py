import tkinter
import json
import os
import random


class Wall:
    def __init__(self):
        self.coordinates = []
        self.squares = []
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, 'data.json')
        with open(data_path, 'r') as f:
            data = json.load(f)
            self.wall_color = data['wall']['wall_color']
            self.window_width = data["window"]["window_width"]
            self.window_height = data["window"]["window_height"]
            self.pixel_size = data["canvas"]["pixel_size"]
            self.wall_locations = data['wall']['wall_locations']
    
    def near_wall(self, canvas: tkinter.Canvas):
        x = 0
        y = int(self.window_height-self.pixel_size)
        for i in range(0, int(self.window_width/self.pixel_size)):
            self.coordinates.append([x, 0])
            square = canvas.create_rectangle(x, 0, x+self.pixel_size, self.pixel_size, fill=self.wall_color, )
            self.squares.append(square)
            self.coordinates.append([x, y])
            square = canvas.create_rectangle(x, y, x+self.pixel_size, y+self.pixel_size, fill=self.wall_color)
            self.squares.append(square)
            x += self.pixel_size
        
        x = int(self.window_width-self.pixel_size)
        y = 0
        for i in range(0, int(self.window_height/self.pixel_size)):
            self.coordinates.append([0, y])
            square = canvas.create_rectangle(0, y, self.pixel_size, y+self.pixel_size, fill=self.wall_color)
            self.squares.append(square)
            self.coordinates.append([x, y])
            square = canvas.create_rectangle(x, y, x+self.pixel_size, y+self.pixel_size, fill=self.wall_color)
            self.squares.append(square)
            y += self.pixel_size

        # current_dir = os.path.dirname(os.path.abspath(__file__))
        # data_path = os.path.join(current_dir, 'wall.json')
        # try:
        #     with open(data_path, 'r') as f:
        #         data = json.load(f)
        # except FileNotFoundError:

        # data["wall"] = self.coordinates

        # with open(data_path, 'w') as f:
        #     json.dump(data, f, indent=4)
    
    def mid_wall(self, canvas: tkinter.Canvas):
        for x, y in self.wall_locations:
            self.coordinates.append([x*self.pixel_size,y*self.pixel_size])
            square = canvas.create_rectangle(x*self.pixel_size, y*self.pixel_size, (x*self.pixel_size)+self.pixel_size, (y*self.pixel_size)+self.pixel_size, fill=self.wall_color)
            self.squares.append(square)

    # def random_wall(self, count):
    #     for _ in range(count):
    #         x = random.randint(0, int((self.window_width/self.pixel_size))-1) * self.pixel_size
    #         y = random.randint(0, int((self.window_height/self.pixel_size))-1) * self.pixel_size
