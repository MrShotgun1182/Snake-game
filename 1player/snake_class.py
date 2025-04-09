import tkinter
import json
import os

class Snake:
    def __init__(self, canvas: tkinter.Canvas):
        self.snake_score = 0
        self.squares = list()
        self.coordinates = list()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, "data.json")
        with open(data_path, 'r') as f:
            data = json.load(f)
            self.snake_color = data["snake1"]["snake_color"]
            self.snake_size = data["snake1"]["snake_size"]
            self.pixel_size = data["canvas"]["pixel_size"]
            self.snake_position = data["snake1"]["snake_position"]
            self.snake_direction = data["snake1"]["snake_direction"]
            self.snake_keys = data["snake1"]["snake_keys"]
        
        for i in range(self.snake_size):
            self.coordinates.append([int(self.pixel_size*self.snake_position[0]), self.pixel_size*self.snake_position[1]])
            
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x+self.pixel_size, y+self.pixel_size, fill=self.snake_color)
            self.squares.append(square)
        
    def delete_tail(self, canvas: tkinter.Canvas):
        canvas.delete(self.squares[-1])
        del self.coordinates[-1]
        del self.squares[-1]
        
    def new_head(self, canvas: tkinter.Canvas):
        x, y = self.coordinates[0]
        if self.snake_direction == self.snake_keys[0]:
            y -= self.pixel_size
        elif self.snake_direction == self.snake_keys[1]:
            y += self.pixel_size
        elif self.snake_direction == self.snake_keys[2]:
            x += self.pixel_size
        elif self.snake_direction == self.snake_keys[3]:
            x -= self.pixel_size
            
        self.coordinates.insert(0, [x, y])
        square = canvas.create_rectangle(x, y, x+self.pixel_size, y+self.pixel_size, fill=self.snake_color)
        self.squares.insert(0, square)
            
        
            
        