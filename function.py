def next_turn(snake, food, SPACE_SIZE, direction, window, SPEED, canvas, SNAKE_COLOR):
    x, y = snake.coordinates[0]
    
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
        
    snake.coordinates.insert(0, (x, y))
    
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    
    snake.squares.insert(0, square)
    
    del snake.coordinates[-1]
    canvas.delete(snake.squares[-1])

    del snake.squares[-1]
            
    window.after(SPEED, next_turn, snake, food, SPACE_SIZE, direction, window, SPEED, canvas, SNAKE_COLOR)

def change_direction(new_direction):
    from main import direction
    if new_direction == "left":
        if direction != "rigth":
            direction = new_direction
    elif new_direction == "rigth":
        if direction != "left":
            direction = new_direction
    elif new_direction == "down":
        if direction != "up":
            direction = new_direction
    elif new_direction == "up":
        if direction != "down":
            direction = new_direction
    
def check_collisions():
    pass

def game_over():
    pass