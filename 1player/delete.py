import torch
import torch.nn as nn 
import torch.optim as optim
import os
import csv

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.line1 = nn.Linear(4, 16)
        self.line2 = nn.Linear(16, 1)
    
    def update_model(self):
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
            self.x = torch.tensor(x)
            self.y = torch.tensor(y)
    
    def learning_loop(self, model:nn.Module):
        loss = nn.MSELoss()
        opt = optim.Adam(model.parameters(), lr=1e-3)

        for t in range(2000):
            y_pred = model(self.x) # its mean model.forward(x), in pytorch we can write this model(x)

            loss_t = loss(y_pred, self.y)
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

    