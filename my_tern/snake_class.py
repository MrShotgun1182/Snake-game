import tkinter
import json
import os

class Snake:
    def __init__(self, canvas: tkinter.Canvas):
        self.squares = list()
        self.coordinates = list()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, "data.json")
        with open(data_path, 'r') as f:
            data = json.load(f)
            self.snake_color = data["snake"]["snake_color"]
            self.snake_size = data["snake"]["snake_size"]
            self.snake_position = data["snake"]["snake_position"]
            self.pixel_size = data["canvas"]["pixel_size"]
        
        for i in range(self.snake_size):
            self.coordinates.append([self.pixel_size*self.snake_position[0], self.pixel_size*self.snake_position[1]])
            
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x+self.pixel_size, y+self.pixel_size, fill=self.snake_color)
            self.squares.append(square)
        