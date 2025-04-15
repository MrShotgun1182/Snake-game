import torch
import torch.nn as nn 
import torch.optim as optim
import os
import pandas as pd
import numpy as np

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.line1 = nn.Linear(4, 16)
        self.line2 = nn.Linear(16, 1)
    
    def set_df(self):
        # preprocessing
        self.df = self.__make_df()
        self.df = self.__hot_one_encode(columns=['direction'])
        self.__check_and_update_distance(self.df)
    
    def learning_loop(self, model:nn.Module):
        x = torch.tensor(self.x)
        y = torch.tensor(self.y)
        loss = nn.MSELoss()
        opt = optim.Adam(model.parameters(), lr=1e-3)

        for t in range(2000):
            y_pred = model(x) # its mean model.forward(x), in pytorch we can write this model(x)

            loss_t = loss(y_pred, y)
            if t % 100 == 99:
                print(t, loss_t.item())
            
            # backprop
            opt.zero_grad()
            loss_t.backward()

            # update weght
            opt.step()

    def forward(self, x):
        x = torch.relu(self.line1(x))
        x = self.line2(x)

    # private methods:

    def __make_df(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, "data_set_snake_game.csv")
        df = pd.read_csv(data_path)
        return df

    def __hot_one_encode(self, columns):
        return pd.get_dummies(self.df, columns=columns)
    
    def __check_and_update_distance(self):
        distans = []
        current_distance = 1e+4
        for i in range(1,len(self.df)):
            
            next_distance = int(np.sqrt(np.pow(self.df.loc[i]['head_x'] - self.df.loc[i]['food_x'],2) + np.pow(self.df.loc[i]['head_y'] - self.df.loc[i]['food_y'],2)))
            if current_distance < next_distance:
                # print("current_distance: %s, next_distance: %s" %(current_distance, next_distance))
                self.df = self.df.drop(index=i-1)
            current_distance = next_distance
        self.df.reset_index()
    