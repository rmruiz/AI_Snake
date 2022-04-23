from random import randint
from pandas import *
from enum import Enum

BOARD_SIZE = 5
MAX_STEPS_WITHOUT_FOOD = 2 * BOARD_SIZE * BOARD_SIZE

class BoardCell(Enum):
    EMPTY = 0
    WALL = 1
    SNAKE = 2
    FRUIT = 3

class SnakeGame:
    def __init__(self):
        self.body = [[3, 3]] #starting point (x,y) (horizontal, vertical)
        self.fruit = self.new_fruit()
        self.direction = 0 #0N, 1E, 2S, 3W
        self.new_board()
        self.alive = True
        self.apples_eaten = 0
        self.steps_util_death = MAX_STEPS_WITHOUT_FOOD
        self.total_steps = 0
    
    def new_fruit(self):
        while True:
            fruit_pos = [randint(1, BOARD_SIZE), randint(1, BOARD_SIZE)]
            if fruit_pos not in self.body:
                return fruit_pos
            #else:
            #    print("retry")

    def new_board(self):
        self.board = [[BoardCell.EMPTY.value for x in range(BOARD_SIZE + 2)] for y in range(BOARD_SIZE + 2)]
        for x in range(BOARD_SIZE + 2):
            for y in range(BOARD_SIZE + 2):
                if x == 0 or y == 0 or x == BOARD_SIZE + 1 or y == BOARD_SIZE + 1:
                    self.board[y][x] = BoardCell.WALL.value
        for piece in self.body:
            self.board[piece[1]][piece[0]] = BoardCell.SNAKE.value
        
        self.board[self.fruit[1]][self.fruit[0]] = BoardCell.FRUIT.value

    def print_board(self):
        #print(DataFrame(self.board)) 
        pass

    def have_wall_on_north(self):
        x, y = self.body[0] #head
        if self.board[y-1][x] == BoardCell.WALL.value:
            return 1
        return 0
    def have_wall_on_south(self):
        x, y = self.body[0] #head
        if self.board[y+1][x] == BoardCell.WALL.value:
            return 1
        return 0
    def have_wall_on_west(self):
        x, y = self.body[0] #head
        if self.board[y][x-1] == BoardCell.WALL.value:
            return 1
        return 0
    def have_wall_on_east(self):
        x, y = self.body[0] #head
        if self.board[y][x+1] == BoardCell.WALL.value:
            return 1
        return 0

    def get_fruit_horizontal_distance(self):
        return self.fruit[0]-self.body[0][0]

    def get_fruit_vertical_distance(self):
        return self.fruit[1]-self.body[0][1]

    def move_snake(self, direction):
        #print(f"starting move in {direction=} [steps={self.steps_util_death}]")
        #print(" the snake:")
        #print(self.body)
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

        new_head_position = [self.body[0][0]+x,self.body[0][1]+y]
        #print(f"{new_head_position=}")
        #check for apple
        got_apple = False
        if self.fruit == new_head_position:
            self.apples_eaten = self.apples_eaten + 1
            self.steps_util_death = MAX_STEPS_WITHOUT_FOOD
            got_apple = True
            #print(" apple eaten!")

        #check for wall or body part
        if self.board[new_head_position[1]][new_head_position[0]] == BoardCell.WALL.value:
            self.alive = False
            #print(" me is dead :( - hit a wall")
            return

        if self.board[new_head_position[1]][new_head_position[0]] == BoardCell.SNAKE.value:
            self.alive = False
            #print(" me is dead :( - hit myself")
            return

        #move snake
        self.body.append(new_head_position)
        #print(" the snake (with new head):")
        #print(self.body)

        #body.pop(0) -> removes tail
        if got_apple:
            #new apple
            self.fruit = self.new_fruit()
        else:
            self.body.pop(0) #removes tail
        
        #print(" the snake (at last):")
        #print(self.body)

        self.steps_util_death = self.steps_util_death - 1
        if self.steps_util_death == 0:
            #print(" me is dead :( - no food found!")
            self.alive = False
        
        self.total_steps = self.total_steps + 1
        #print(f"total steps: {self.total_steps}")
        return
    
    def get_fitness_score(self):
        return self.total_steps + self.apples_eaten * MAX_STEPS_WITHOUT_FOOD