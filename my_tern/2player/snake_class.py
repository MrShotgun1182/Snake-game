import tkinter
import json
import os

class Snake:
    def __init__(self, canvas: tkinter.Canvas, snake_number):
        self.squares = list()
        self.coordinates = list()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, "data.json")
        with open(data_path, 'r') as f:
            data = json.load(f)
            self.snake_color = data[F"snake{snake_number}"]["snake_color"]
            self.snake_size = data[F"snake{snake_number}"]["snake_size"]
            self.pixel_size = data["canvas"]["pixel_size"]
            self.snake_direction = data[F"snake{snake_number}"]["snake_direction"]
            self.snake_position = data[F"snake{snake_number}"]["snake_position"]
        
        for i in range(self.snake_size):
            self.coordinates.append([self.pixel_size*self.snake_position[0], self.pixel_size*self.snake_position[1]])
            
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x+self.pixel_size, y+self.pixel_size, fill=self.snake_color)
            self.squares.append(square)
        