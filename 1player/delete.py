import torch
import torch.nn as nn 
import torch.optim as optim
import os
import csv
import pandas as pd

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.line1 = nn.Linear(4, 16)
        self.line2 = nn.Linear(16, 1)
    
    def make_df(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, "data_set_snake_game.csv")
        df = pd.read_csv(data_path)
        df.columns = ["1","2","3"]
        print(df['1'].type())
        

model = Model()
model.collect_data_model()