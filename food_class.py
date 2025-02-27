import random
class Food():
    def __init__(self, GAME_HEIGHT, GAME_WIDTH, SPACE_SIZE, FOOD_COLOR, canvas):
        self.__game_height__ = GAME_HEIGHT
        self.__game_width__ = GAME_WIDTH
        self.__space_size__ = SPACE_SIZE
        self.__food_color__ = FOOD_COLOR
        x = random.randint(0,int((self.__game_width__ / self.__space_size__)-1)) * self.__space_size__
        y = random.randint(0,int((self.__game_height__ / self.__space_size__)-1)) * self.__space_size__
        self.coordonates = [x, y]
        canvas.create_oval(self.coordonates[0], self.coordonates[1], self.coordonates[0] + SPACE_SIZE, self.coordonates[1] + SPACE_SIZE, fill=FOOD_COLOR, tag="food")
        