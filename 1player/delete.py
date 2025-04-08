import os
import csv

current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, "data_set_snake_game.csv")
with open(data_path, 'r') as f:
    x = []
    y = []
    reader = csv.reader(f)
    for row in reader:
        temp = row[0]
        temp = temp[2:-2]
        temp = temp.split(',')
        temp = [int(temp[0]), int(temp[1])]
        row_data = [temp[0], temp[1]]
        temp = row[1]
        temp = temp[2:-2]
        temp = temp.split(',')
        temp = [int(temp[0]), int(temp[1])]
        row_data.append(temp[0])
        row_data.append(temp[1])
        x.append(row_data)
        y.append(row[2])
