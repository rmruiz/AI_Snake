from random import randint

from settings import *

class SnakeGame:
    def __init__(self):
        #self.snake = [[int(BOARD_SIZE/2)+1, int(BOARD_SIZE/2)+1]] #starting point (x,y) (horizontal, vertical)
        self.snake = [ [9, 12], [9, 11], [9, 10], [10, 10] ]
        self.apple_position = None
        self.new_fruit()
        self.alive = True
        self.apples_eaten = 0
        self.steps_util_death = MAX_STEPS_WITHOUT_FOOD
        self.total_steps = 0
        self.direction = Direction.NORTH

    def get_snake_head_pos(self):
        return self.snake[-1]
    
    def new_fruit(self):
        while True:
            new_pos = [randint(1, BOARD_SIZE), randint(1, BOARD_SIZE)]
            if new_pos not in self.snake:
                self.apple_position = new_pos
                break

    def print_board(self):
        print(self.snake)
        print(self.apple_position)
        board = [[" " for x in range(BOARD_SIZE + 2)] for y in range(BOARD_SIZE + 2)]
        for x in range(BOARD_SIZE + 2):
            for y in range(BOARD_SIZE + 2):
                if x == 0 or y == 0 or x == BOARD_SIZE + 1 or y == BOARD_SIZE + 1:
                    board[y][x] = "#"
        for piece in self.snake:
            board[piece[1]][piece[0]] = "S"

        board[self.get_snake_head_pos()[1]][self.get_snake_head_pos()[0]] = "H"
    
        board[self.apple_position[1]][self.apple_position[0]] = "F"
        
        for row in board:
            for cell in row:
                print(cell, end='')
            print('')

    #1 touching north, -1 touching south, 0 in the middle
    def distance_to_north_south_wall(self):
        x=self.get_snake_head_pos()[0]
        m=(-2.0)/(BOARD_SIZE-1.0)
        b=1-m
        y=m*x+b
        return y
    def distance_to_west_east_wall(self):
        x=self.get_snake_head_pos()[1]
        m=(-2.0)/(BOARD_SIZE-1.0)
        b=1-m
        y=m*x+b
        return y 

    #TODO: return how far snake is on each direction
    def have_snake_on_north(self):
        if north(self.get_snake_head_pos()) in self.snake:
            return 1.0
        return -1.0
    def have_snake_on_south(self):
        if south(self.get_snake_head_pos()) in self.snake:
            return 1.0
        return -1.0
    def have_snake_on_west(self):
        if west(self.get_snake_head_pos()) in self.snake:
            return 1.0
        return -1.0
    def have_snake_on_east(self):
        if east(self.get_snake_head_pos()) in self.snake:
            return 1.0
        return -1.0

    def have_wall_on_north(self):
        if is_wall(north(self.get_snake_head_pos())):
            return 1.0
        return -1.0
    def have_wall_on_south(self):
        if is_wall(south(self.get_snake_head_pos())):
            return 1.0
        return -1.0
    def have_wall_on_west(self):
        if is_wall(west(self.get_snake_head_pos())):
            return 1.0
        return -1.0
    def have_wall_on_east(self):
        if is_wall(east(self.get_snake_head_pos())):
            return 1.0
        return -1.0

    def get_fruit_north_distance(self):
        if self.apple_position[1] >= self.get_snake_head_pos()[1]:
            return -1.0
        else:
            return abs(self.get_snake_head_pos()[1]-self.apple_position[1])/(BOARD_SIZE-1)

    def get_fruit_south_distance(self):
        if self.apple_position[1] <= self.get_snake_head_pos()[1]:
            return -1.0
        else:
            return abs(self.get_snake_head_pos()[1]-self.apple_position[1])/(BOARD_SIZE-1)

    def get_fruit_west_distance(self):
        if self.apple_position[0] >= self.get_snake_head_pos()[0]:
            return -1.0
        else:
            return abs(self.get_snake_head_pos()[0]-self.apple_position[0])/(BOARD_SIZE-1)

    def get_fruit_east_distance(self):
        if self.apple_position[0] <= self.get_snake_head_pos()[0]:
            return -1.0
        else:
            return abs(self.get_snake_head_pos()[0]-self.apple_position[0])/(BOARD_SIZE-1)

    def get_fruit_horizontal_distance(self):
        return (self.apple_position[0]-self.get_snake_head_pos()[0])/(BOARD_SIZE-1)

    def get_fruit_vertical_distance(self):
        return (self.apple_position[1]-self.get_snake_head_pos()[1])/(BOARD_SIZE-1)

    def move_snake(self, turn, print_test=False):
        if print_test:
            print(f"have:{self.direction}")
            print(f"Got:{turn} {Output(turn)}")
        if turn == Output.LEFT.value:
            self.direction = Direction((self.direction.value - 1)%4)
        elif turn == Output.RIGHT.value:
            self.direction = Direction((self.direction.value + 1)%4)
        if print_test:
            print(f"result:{self.direction}")

        next_head_position = []
        if self.direction == Direction.NORTH:
            next_head_position = north(self.get_snake_head_pos())
        elif self.direction == Direction.SOUTH:
            next_head_position = south(self.get_snake_head_pos())
        elif self.direction == Direction.EAST:
            next_head_position = east(self.get_snake_head_pos())
        elif self.direction == Direction.WEST:
            next_head_position = west(self.get_snake_head_pos())

        #check for apple
        got_apple = False
        if self.apple_position == next_head_position:
            self.apples_eaten = self.apples_eaten + 1
            self.steps_util_death = MAX_STEPS_WITHOUT_FOOD + 1
            got_apple = True
            if print_test:
                print(" apple eaten!")

        #check for wall or body part
        elif is_wall(next_head_position):
            self.alive = False
            if print_test:
                print(" me is dead :( - hit a wall")
            return

        elif next_head_position in self.snake:
            self.alive = False
            if print_test:
                print(" me is dead :( - hit myself")
                #print(next_head_position)
                #print(self.snake)                
            return

        #move snake
        self.snake.append(next_head_position)
        
        if got_apple:
            self.new_fruit()
        else:
            self.snake.pop(0) #removes tail
        
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
        #return self.total_steps*self.apples_eaten**2 # + self.apples_eaten * MAX_STEPS_WITHOUT_FOOD
        #return int(10000/(self.total_steps+1)*self.apples_eaten**2)
        return self.total_steps*((self.apples_eaten+1)**2)

    def get_current_input(self):
        return [    [self.have_wall_on_north()], # No:-1, Yes:1
                    [self.have_wall_on_south()],
                    [self.have_wall_on_east()],
                    [self.have_wall_on_west()],
                    [(self.direction.value - 1.5)/1.5],
                    [self.distance_to_north_south_wall()],
                    [self.distance_to_west_east_wall()],
                    [self.have_snake_on_north()],
                    [self.have_snake_on_south()],
                    [self.have_snake_on_east()],
                    [self.have_snake_on_west()],
                    [self.get_fruit_horizontal_distance()],
                    [self.get_fruit_vertical_distance()],
                    #[self.get_fruit_north_distance()],
                    #[self.get_fruit_south_distance()],
                    #[self.get_fruit_west_distance()],
                    #[self.get_fruit_east_distance()], 
                    ]

def north(pos):
    return [pos[0],pos[1]-1]
def south(pos):
    return [pos[0],pos[1]+1]
def west(pos):
    return [pos[0]-1,pos[1]]
def east(pos):
    return [pos[0]+1,pos[1]]

def is_wall(pos):
    return pos[0] == 0 or pos[1] == 0 or pos[0] == BOARD_SIZE+1 or pos[1] == BOARD_SIZE+1