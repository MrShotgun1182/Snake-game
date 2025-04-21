import torch
import torch.nn as nn 
import torch.optim as optim
import os
import pandas as pd
import numpy as np

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.line1 = nn.Linear(5,16)
        self.relu1 = nn.ReLU()
        self.line2 = nn.Linear(16,32)
        self.relu2 = nn.ReLU()
        self.line3 = nn.Linear(32,64)
        self.relu3 = nn.ReLU()
        self.output = nn.Linear(64,4)
        self.drop_out = nn.Dropout(0.3)
        self.set_df()
    
    def set_df(self):
        # preprocessing
        self.df = self.__make_df()
        self.df = self.__hot_one_encode(columns=['direction'])
        # self.__check_and_update_distance()
        self.__add_distance()
        self.__normaliz()

    def forward(self, x):
        x = self.relu1(self.line1(x))
        x = self.drop_out(x)
        x = self.relu2(self.line2(x))
        x = self.drop_out(x)
        x = self.relu3(self.line3(x))
        x = self.output(x)
        return x
    
    def learning_loop(self, model:nn.Module):
        x, y = self.__make_x_y()
        x = torch.tensor(x, dtype=torch.float32)
        y = torch.tensor(y, dtype=torch.float32)

        loss_fn = nn.CrossEntropyLoss()
        opt = optim.Adam(model.parameters(), lr=1e-4)

        model.train()

        for t in range(5000):
            y_pred = model(x) # its mean model.forward(x), in pytorch we can write this model(x)

            loss = loss_fn(y_pred, y)
            if t % 100 == 99:
                print(t, loss.item())
            
            # backprop
            opt.zero_grad()
            loss.backward()

            # update weght
            opt.step()
        model.eval()

        with torch.no_grad():
            y_pred = torch.sigmoid(model(x))
            y_pred_classes = y_pred.round()
            accuracy = (y_pred_classes == y).float().mean()
            print(f"Accuracy: {accuracy.item()}")

    def model_output(self, x, model):
        with torch.no_grad():
            x = torch.tensor(x, dtype=torch.float32)
            output = torch.sigmoid(model(x))
            output_index = torch.argmax(output)
            column = ["Down", "Left", "Right", "Up"]
            return column[output_index]



    # private methods:

    def __make_df(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, "data_set_snake_game.csv")
        df = pd.read_csv(data_path)
        return df

    def __hot_one_encode(self, columns):
        return pd.get_dummies(self.df, columns=columns)
    
    def __check_and_update_distance(self):
        before_distance = int(np.sqrt(np.pow(self.df.loc[0]['food_x'] - self.df.loc[0]['head_x'],2) + np.pow(self.df.loc[0]['food_y'] - self.df.loc[0]['head_y'],2)))
        for i in range(1,len(self.df)-1):
            current_distance = int(np.sqrt(np.pow(self.df.loc[i]['food_x'] - self.df.loc[i]['head_x'],2) + np.pow(self.df.loc[i]['food_y'] - self.df.loc[i]['head_y'],2)))
            if current_distance >= before_distance:
                # print("current_distance: %s, before_distance: %s, between distance: %s" %(current_distance, before_distance, before_distance-current_distance))
                # if current_distance - before_distance == 0:
                    # print("head: ",df.loc[i]['head_x'], df.loc[i]['head_y'],"food: ", df.loc[i]['food_x'], df.loc[i]['food_y'], "distance: ", current_distance-before_distance)
                    # print(np.pow(df.loc[i]['food_x'] - df.loc[i]['head_x'],2))
                    # print(np.pow(df.loc[i]['food_y'] - df.loc[i]['head_y'],2))
                    # print(np.pow(df.loc[i]['food_x'] - df.loc[i]['head_x'],2) + np.pow(df.loc[0]['food_y'] - df.loc[0]['head_y'],2))
                    # print(np.sqrt(np.pow(df.loc[i]['food_x'] - df.loc[i]['head_x'],2) + np.pow(df.loc[i]['food_y'] - df.loc[i]['head_y'],2)))
                    # print(int(np.sqrt(np.pow(df.loc[i]['food_x'] - df.loc[i]['head_x'],2) + np.pow(df.loc[i]['food_y'] - df.loc[i]['head_y'],2))))
                    # print(before_distance)
                    # print("*"*20)
                self.df = self.df.drop(index=i)
            before_distance = current_distance
        self.df.reset_index()
        print(self.df[['direction_Down',	'direction_Left','direction_Right',	'direction_Up']].sum())
        self.df.to_csv("clean.csv")

    def __add_distance(self):
        self.df["distance_to_food"] = self.df["distance_to_food"] = np.sqrt((self.df['food_x'] - self.df['head_x'])**2 + (self.df['food_y'] - self.df['head_y'])**2)

    def __normaliz(self):
        self.df[['head_x' ,'head_y', 'food_x', 'food_y']] /= self.df[['head_x' ,'head_y', 'food_x', 'food_y']].max()

    def __make_x_y(self):
        x = self.df[['head_x' ,'head_y', 'food_x', 'food_y', 'distance_to_food']].values.astype('float32')
        y = self.df[['direction_Down',	'direction_Left','direction_Right',	'direction_Up']].values.astype('float32')
        return x, y
    
    def weights_init(self,m):
        if isinstance(m, nn.Linear):
            nn.init.xavier_normal_(m.weight)

    def test(self):
        # محاسبه کوارتایل‌ها
        Q1 = self.df.quantile(0.25)
        Q3 = self.df.quantile(0.75)
        IQR = Q3 - Q1  # محدوده بین چارکی (Interquartile Range)
        
        # حذف داده‌های پرت
        self.df = self.df[~((self.df < (Q1 - 1.5 * IQR)) | (self.df > (Q3 + 1.5 * IQR))).any(axis=1)]



if __name__ == "__main__":
    model = Model()
    # model.test()
    # print(model.df)
    # model.apply(model.weights_init)
    model.learning_loop(model)
    
    

