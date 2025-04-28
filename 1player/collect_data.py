import os
import csv
from snake_class import Snake
from food_class import Food
import numpy as np

class Collector:
    rows = []
    last_direction = "Down"

    def collect(self, snake:Snake, food:Food):
        distance = int(np.sqrt(np.pow(snake.coordinates[0][0] - food.coordinates[0],2) + np.pow(snake.coordinates[0][1] - food.coordinates[1],2)))
        data = {
            "head_x": snake.coordinates[0][0],
            "head_y": snake.coordinates[0][1],
            # "body_snake": snake.coordinates[1:],
            "food_x": food.coordinates[0],
            "food_y": food.coordinates[1],
            "body_len": len(snake.coordinates),
            "distance_to_food": distance,
            "last_direction": self.last_direction,
            "direction": snake.snake_direction
        }
        self.rows.append(data)
        self.last_direction = snake.snake_direction

    def save_rows(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, 'data_set_snake_game.csv')

        file_exists = os.path.exists(data_path)

        with open(data_path, mode='a', newline='') as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(["head_x", "head_y", "food_x", "food_y", "body_len","distance_to_food", "last_direction","direction"])

            for row in self.rows[:-1]:
                writer.writerow([
                    row["head_x"],
                    row["head_y"],
                    # row["body_snake"],
                    row["food_x"],
                    row["food_y"],
                    row["body_len"],
                    row["distance_to_food"],
                    row["last_direction"],
                    row["direction"] 
                ])

        self.rows.clear()
