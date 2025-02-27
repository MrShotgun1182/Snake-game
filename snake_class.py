class Snake():
    def __init__(self, BODY_PARTS, SPACE_SIZE, canvas, SNAKE_COLOR):
        self.__snake_color__ = SNAKE_COLOR
        self.__body_size__ = BODY_PARTS
        self.__space_size__ = SPACE_SIZE
        self.coordinates = list()
        self.squares = list()
        
        for i in range(self.__body_size__):
            self.coordinates.append([0, 0])
            
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + self.__space_size__, y + self.__space_size__, fill=self.__snake_color__ ,tag='snake')
            self.squares.append(square)