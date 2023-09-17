import pygame
import random
import numpy as np
import pickle

from collections import deque


from enum import Enum
from collections import namedtuple
from game import SnakeGameAI, Direction, Point

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)



class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 20

MAX_MEMORY = 100_000


class SnakeGame:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.file_path = 'experience_replay.pkl'
        
        # init game state
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def retrieveAction(self, direction):
        if self.direction == Direction.UP:
            switch_dict = {
            Direction.UP: [1, 0, 0],
            Direction.LEFT: [0, 0, 1],
            Direction.RIGHT: [0, 1, 0],
            Direction.DOWN: [1, 0, 0],
            # Add more cases as needed
            }
        elif self.direction == Direction.LEFT:
            switch_dict = {
            Direction.UP: [0, 1, 0],
            Direction.LEFT: [1, 0, 0],
            Direction.RIGHT: [1, 0, 0],
            Direction.DOWN: [0, 0, 1],
            # Add more cases as needed
            }

        if self.direction == Direction.DOWN:
            switch_dict = {
            Direction.UP: [1, 0, 0],
            Direction.LEFT: [0, 1, 0],
            Direction.RIGHT: [0, 0, 1],
            Direction.DOWN: [1, 0, 0],
            # Add more cases as needed
            }
        elif self.direction == Direction.RIGHT:
            switch_dict = {
            Direction.UP: [0, 0, 1],
            Direction.LEFT: [1, 0, 0],
            Direction.RIGHT: [1, 0, 0],
            Direction.DOWN: [0, 1, 0],
            # Add more cases as needed
            }

        return switch_dict[direction]
        
    def play_step(self):
        action = []
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.direction != Direction.LEFT:
                        action = [] 

                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        state_old = self.get_state()
        final_move = self.retrieveAction(self.direction)

                
        # 2. move

        self._move(self.direction) # update the head
        self.snake.insert(0, self.head)

        state_new = self.get_state()
        reward = 0
        
        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            reward = -10
            return reward, game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # 6 save experience


        self.remember(state_old, final_move, reward, state_new, game_over)

        


        # 7. return game over and score
        return reward, game_over, self.score

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached
    

    def dumpMemory(self):
        with open(self.file_path, 'wb') as file:
            pickle.dump(self.memory, file)


    def _is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False
        
    def _update_ui(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)


    # def _saveExperience(self, ):
    def get_state(self):
        head = self.head
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)
        
        dir_l = self.direction == Direction.LEFT
        dir_r = self.direction == Direction.RIGHT
        dir_u = self.direction == Direction.UP
        dir_d = self.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and self._is_collision(point_r)) or 
            (dir_l and self._is_collision(point_l)) or 
            (dir_u and self._is_collision(point_u)) or 
            (dir_d and self._is_collision(point_d)),

            # Danger right
            (dir_u and self._is_collision(point_r)) or 
            (dir_d and self._is_collision(point_l)) or 
            (dir_l and self._is_collision(point_u)) or 
            (dir_r and self._is_collision(point_d)),

            # Danger left
            (dir_d and self._is_collision(point_r)) or 
            (dir_u and self._is_collision(point_l)) or 
            (dir_r and self._is_collision(point_u)) or 
            (dir_l and self._is_collision(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            self.food.x < self.head.x,  # food left
            self.food.x > self.head.x,  # food right
            self.food.y < self.head.y,  # food up
            self.food.y > self.head.y  # food down
            ]

        return np.array(state, dtype=int)        


        
            

if __name__ == '__main__':
    game = SnakeGame()
    
    # game loop
    while True:
        reward, game_over, score = game.play_step()
        
        if game_over == True:
            game.dumpMemory()
            break
        
    print('Final Score', score)
        
        
    pygame.quit()