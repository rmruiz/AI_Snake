from random import randint, random
from enum import Enum

#random.seed(0)

BOARD_SIZE = 5
MAX_STEPS_WITHOUT_FOOD = 5 * BOARD_SIZE

class BoardCell(Enum):
    EMPTY = 0
    WALL = 1
    SNAKE = 2
    FRUIT = 3

class SnakeGame:
    def __init__(self):
        self.snake = [[3, 3]] #starting point (x,y) (horizontal, vertical)
        self.fruit_position = None
        self.new_fruit()
        #self.direction = 0 #0N, 1E, 2S, 3W
        #self.new_board()
        self.alive = True
        self.apples_eaten = 0
        self.steps_util_death = MAX_STEPS_WITHOUT_FOOD
        self.total_steps = 0

    def get_snake_head_pos(self):
        return self.snake[-1]
    
    def new_fruit(self):
        while True:
            new_pos = [randint(1, BOARD_SIZE), randint(1, BOARD_SIZE)]
            if new_pos not in self.snake:
                self.fruit_position = new_pos
                break

    def print_board(self):
        board = [[" " for x in range(BOARD_SIZE + 2)] for y in range(BOARD_SIZE + 2)]
        for x in range(BOARD_SIZE + 2):
            for y in range(BOARD_SIZE + 2):
                if x == 0 or y == 0 or x == BOARD_SIZE + 1 or y == BOARD_SIZE + 1:
                    board[y][x] = "#"
        for piece in self.snake:
            board[piece[1]][piece[0]] = "S"
    
        board[self.fruit_position[1]][self.fruit_position[0]] = "F"
        
        for row in board:
            for cell in row:
                print(cell, end='')
            print('')

    #def print_board(self):
    #    board = self.build_board()
    #    print(panda.DataFrame(board)) 

    def have_snake_on_north(self):
        x, y = self.get_snake_head_pos()
        if [x, y-1] in self.snake:
            return 1
        return -1
    def have_snake_on_south(self):
        x, y = self.get_snake_head_pos()
        if [x, y+1] in self.snake:
            return 1
        return -1 

    def have_snake_on_west(self):
        x, y = self.get_snake_head_pos()
        if [x-1, y] in self.snake:
            return 1
        return -1 

    def have_snake_on_east(self):
        x, y = self.get_snake_head_pos()
        if [x+1, y] in self.snake:
            return 1
        return -1

    #1 touching north, -1 touching south, 0 in the middle
    def distance_to_north_south_wall(self):
        x=self.get_snake_head_pos()[0]
        m=(-2)/(BOARD_SIZE-1)
        b=1-m
        y=m*x+b
        return y

    def distance_to_west_east_wall(self):
        x=self.get_snake_head_pos()[1]
        m=(-2)/(BOARD_SIZE-1)
        b=1-m
        y=m*x+b
        return y

    def have_wall_on_north(self):
        x, y = self.get_snake_head_pos()
        #if self.board[y-1][x] == BoardCell.WALL.value:
        if y == 1:
            return 1
        return -1
    def have_wall_on_south(self):
        x, y = self.get_snake_head_pos()
        #if self.board[y+1][x] == BoardCell.WALL.value:
        if y == BOARD_SIZE:
            return 1
        return -1
    def have_wall_on_west(self):
        x, y = self.get_snake_head_pos()
        #if self.board[y][x-1] == BoardCell.WALL.value:
        if x == 0:
            return 1
        return -1
    def have_wall_on_east(self):
        x, y = self.get_snake_head_pos()
        #if self.board[y][x+1] == BoardCell.WALL.value:
        if x == BOARD_SIZE:
            return 1
        return -1

    def get_fruit_horizontal_distance(self):
        #print(f"fruit:{self.fruit_position}")
        #print(self.fruit_position[0])
        #print(f"snake:{self.get_snake_head_pos()}")
        #print(self.get_snake_head_pos()[0])
        normalized_x_distance = (self.fruit_position[0]-self.get_snake_head_pos()[0])/(BOARD_SIZE-1)
        #print(f"distance={normalized_x_distance}")
        return normalized_x_distance

    def get_fruit_vertical_distance(self):
        return (self.fruit_position[1]-self.get_snake_head_pos()[1])/(BOARD_SIZE-1)

    def move_snake(self, direction, print_test=False):
        #print(f"starting move in {direction=} [steps={self.steps_util_death}]")
        #print(" the snake:")
        #print(self.snake)
        if print_test:
            print(f"D:{direction}")
        x = 0
        y = 0
        if direction == "north":
            y = -1
        elif direction == "south":
            y = 1
        elif direction == "west":
            x = -1
        elif direction == "east":
            x = 1

        new_head_position = [self.get_snake_head_pos()[0]+x,self.get_snake_head_pos()[1]+y]
        #check for apple
        got_apple = False
        if self.fruit_position == new_head_position:
            self.apples_eaten = self.apples_eaten + 1
            self.steps_util_death = MAX_STEPS_WITHOUT_FOOD
            got_apple = True
            if print_test:
                print(" apple eaten!")

        #check for wall or body part
        #if self.board[new_head_position[1]][new_head_position[0]] == BoardCell.WALL.value:
        if new_head_position[0] == 0 or new_head_position[1] == 0 or new_head_position[0] == BOARD_SIZE+1 or new_head_position[1] == BOARD_SIZE+1:
            self.alive = False
            if print_test:
                print(" me is dead :( - hit a wall")
            return

        if new_head_position in self.snake:
            self.alive = False
            if print_test:
                print(" me is dead :( - hit myself")
                #print(new_head_position)
                #print(self.snake)                
            return

        #move snake
        self.snake.append(new_head_position)
        #print(" the snake (with new head):")
        #print(self.snake)

        if got_apple:
            self.new_fruit()
        else:
            self.snake.pop(0) #removes tail
        
        #print(" the snake (at last):")
        #print(self.snake)

        self.steps_util_death = self.steps_util_death - 1
        if self.steps_util_death == 0:
            if print_test:
                print(" me is dead :( - no food found!")
            self.alive = False
        
        self.total_steps = self.total_steps + 1
        if print_test:
            print(f"total steps: {self.total_steps}, total apples: {self.apples_eaten}")
        return
    
    def get_fitness_score(self):
        return self.total_steps + self.apples_eaten*self.apples_eaten * MAX_STEPS_WITHOUT_FOOD

    def get_current_input(self):
        return [    #self.have_wall_on_north(), # No:-1, Yes:1
                    #self.have_wall_on_south(),
                    #self.have_wall_on_east(),
                    #self.have_wall_on_west(),
                    [self.distance_to_north_south_wall()],
                    [self.distance_to_west_east_wall()],
                    [self.have_snake_on_north()],
                    [self.have_snake_on_south()],
                    [self.have_snake_on_east()],
                    [self.have_snake_on_west()],
                    [self.get_fruit_horizontal_distance()],
                    [self.get_fruit_vertical_distance()]  ]