import torch
import torch.nn as nn 
import torch.optim as optim
import os
import pandas as pd
import numpy as np

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.line1 = nn.Linear(4,16)
        self.relu1 = nn.ReLU()
        self.line2 = nn.Linear(16,16)
        self.relu2 = nn.ReLU()
        self.output = nn.Linear(16,4)
    
    def set_df(self):
        # preprocessing
        self.df = self.__make_df()
        self.df = self.__hot_one_encode(columns=['direction'])
        self.__check_and_update_distance()
    
    def learning_loop(self, model:nn.Module):
        x, y = self.ــmake_x_y()
        x = torch.tensor(x, dtype=torch.float32)
        y = torch.tensor(y, dtype=torch.float32)

        loss_fn = nn.BCEWithLogitsLoss()
        opt = optim.Adam(model.parameters(), lr=1e-3)

        model.train()

        for t in range(2000):
            y_pred = model(x) # its mean model.forward(x), in pytorch we can write this model(x)

            loss = loss_fn(y_pred, y)
            if t % 100 == 99:
                print(t, loss.item())
            
            # backprop
            opt.zero_grad()
            loss.backward()

            # update weght
            opt.step()

    def forward(self, x):
        x = self.relu1(self.line1(x))
        x = self.relu2(self.line2(x))
        x = self.output(x)
        return x

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

    def __make_x_y(self):
        x = self.df[['head_x' ,'head_y', 'food_x', 'food_y']].values.astype('float32')
        y = self.df[['direction_Down',	'direction_Left','direction_Right',	'direction_Up']].values.astype('float32')
        return x, y

    