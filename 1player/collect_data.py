import os
import csv

class Collector:
    rows = []

    def collect(self, snake, food):
        data = {
            "head_x": snake.coordinates[0][0],
            "head_y": snake.coordinates[0][1],
            # "body_snake": snake.coordinates[1:],
            "food_x": food.coordinates[0],
            "food_y": food.coordinates[1],
            "body_len": len(snake.coordinates),
            "direction": snake.snake_direction
        }
        self.rows.append(data)

    def save_rows(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, 'data_set_snake_game.csv')

        file_exists = os.path.exists(data_path)

        with open(data_path, mode='a', newline='') as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(["head_x", "head_y", "food_x", "food_y", "body_len", "direction"])

            for row in self.rows[:-1]:
                writer.writerow([
                    row["head_x"],
                    row["head_y"],
                    # row["body_snake"],
                    row["food_x"],
                    row["food_y"],
                    row["body_len"],
                    row["direction"] 
                ])

        self.rows.clear()
