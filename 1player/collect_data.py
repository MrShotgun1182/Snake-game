import os
import csv

class Collector:
    rows = []

    def collect(self, snake, food):
        data = {
            "head_snake": snake.coordinates[0],
            # "body_snake": snake.coordinates[1:],
            "food": food.coordinates,
            "direction": snake.snake_direction
        }
        self.rows.append(data)

    def save_rows(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, 'data_set_snake_game.csv')

        # file_exists = os.path.exists(data_path)

        with open(data_path, mode='a', newline='') as file:
            writer = csv.writer(file)

            # if not file_exists:
            #     writer.writerow(["head_snake", "body_snake", "food", "direction"])

            for row in self.rows[:-1]:
                writer.writerow([
                    row["head_snake"],
                    # row["body_snake"],
                    row["food"],
                    row["direction"] 
                ])

        self.rows.clear()
