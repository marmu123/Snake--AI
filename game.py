import numpy as np
import time
UP=(-1,0)
DOWN=(1,0)
LEFT=(0,-1)
RIGHT=(0,1)

MOVES=[UP,DOWN,LEFT,RIGHT]

EMPTY_SCORE=0
FOOD_SCORE=99


class Game:
    def __init__(self, board_size, no_snakes, players, gui=None, display=False, max_turns=1000):
        self.board_size = board_size
        self.no_snakes = no_snakes
        self.players = players
        self.gui = gui
        self.display = display
        self.max_turns = max_turns

        self.no_food = 4
        self.current_turn = 0
        self.snake_size = 3

        self.snakes=[[((j+1) * self.board_size // (2 * self.no_snakes), self.board_size // 2 + i) for i in range(self.snake_size)] for j in range(self.no_snakes)]
        self.food=[(self.board_size // 4, self.board_size // 4), (3 * self.board_size // 4, self.board_size // 4), (self.board_size // 4, 3 * self.board_size // 4), (3 * self.board_size // 4, 3 * self.board_size // 4)]
        self.players_ids=[i for i in range(self.no_snakes)]
        self.board=np.zeros([self.board_size, self.board_size])
        for i in self.players_ids:
            for tup in self.snakes[i]:
                self.board[tup[0]][tup[1]]=i+1
        for tup in self.food:
            self.board[tup[0]][tup[1]] = FOOD_SCORE

        self.food_index=0
        self.food_coord = [(2, 2), (1, 3), (1, 0), (4, 2), (8, 4), (2, 4), (4, 0), (8, 9), (7, 0), (1, 2), (6, 8), (4, 5), (0, 5), (8, 5), (1, 0), (9, 1), (0, 3), (7, 2), (3, 9), (3, 6), (1, 9), (6, 3), (3, 2), (3, 1), (7, 9), (1, 7), (5, 4), (3, 8), (5, 2), (8, 0), (8, 9), (9, 9), (6, 8), (6, 4), (7, 9), (3, 3), (6, 5), (3, 1), (8, 0), (7, 9), (1, 4), (0, 4), (1, 5), (2, 5), (8, 6), (1, 2), (3, 8), (3, 9), (4, 0), (9, 3), (0, 5), (1, 1), (9, 7), (3, 1), (7, 5), (3, 2), (0, 4), (3, 8), (0, 5), (1, 2), (3, 3), (6, 1), (9, 3), (2, 5), (9, 3), (4, 4), (1, 8), (6, 3), (6, 8), (4, 6), (2, 4), (0, 0), (1, 4), (3, 9), (8, 8), (5, 2), (0, 5), (6, 7), (9, 0), (8, 7), (9, 3), (7, 6), (1, 3), (2, 1), (7, 2), (6, 4), (9, 9), (5, 8), (9, 6), (7, 8), (9, 9), (0, 1), (6, 4), (8, 0), (2, 6), (7, 4), (3, 9), (8, 4), (2, 6), (4, 1), (1, 0), (7, 4), (7, 8), (9, 7), (5, 2), (9, 2), (1, 9), (1, 0), (0, 2), (4, 9), (4, 9), (9, 0), (9, 0), (6, 3), (6, 7), (0, 1), (9, 6), (7, 2), (9, 3), (9, 5), (0, 9), (6, 0), (6, 6), (5, 2), (3, 6), (3, 6), (4, 8), (4, 8), (3, 6), (1, 3), (1, 7), (2, 4), (5, 0), (1, 6), (1, 7), (6, 5), (7, 1), (5, 4), (7, 4), (6, 7), (1, 7), (8, 8), (6, 8), (4, 0), (1, 6), (0, 8), (1, 8), (6, 5), (4, 2), (4, 1), (4, 3), (3, 9), (8, 6), (1, 1), (1, 3), (3, 9), (8, 4), (7, 6), (6, 9), (9, 8), (8, 0), (8, 5), (6, 6), (9, 7), (7, 8), (7, 2), (3, 8), (3, 9), (3, 4), (4, 8), (5, 2), (2, 2), (8, 5), (7, 0), (5, 5), (8, 1), (8, 0), (3, 7), (6, 6), (5, 8), (4, 4), (2, 2), (2, 8), (4, 1), (8, 3), (0, 3), (1, 5), (7, 0), (8, 9), (5, 9), (1, 9), (1, 5), (1, 4), (7, 6), (8, 7), (9, 7), (8, 6), (3, 1), (9, 9), (4, 9)]

    def move(self):
        moves = []
        for i in self.players_ids:
            # Head move
            curr_snake=self.snakes[i]
            move=self.players[i].get_move(self.board,curr_snake)
            moves.append(move)
            new_position=(curr_snake[-1][0]+move[0],curr_snake[-1][1]+move[1])
            curr_snake.append(new_position)
        for i in self.players_ids:
            head=self.snakes[i][-1]
            if head not in self.food:
                # Snake did not eat
                self.board[self.snakes[i][0][0]][self.snakes[i][0][1]]=EMPTY_SCORE
                self.snakes[i].pop(0)
            else:
                # Snake eat
                self.food.remove(head)

        for i in self.players_ids:
            # Out of board
            head=self.snakes[i][-1]
            if head[0] >= self.board_size or head[1] >= self.board_size or head[0] < 0 or head[1] < 0:
                # Player dies
                self.players_ids.remove(i)
            else:
                self.board[head[0]][head[1]] = i + 1

        for i in self.players_ids:
            # Collision with obstacle or another snake
            head=self.snakes[i][-1]
            for j in range(self.no_snakes):
                if i==j:
                    if head in self.snakes[i][:-1]:
                        self.players_ids.remove(i)
                else:
                    if head in self.snakes[j]:
                        self.players_ids.remove(i)

        while len(self.food) < self.no_food:
            # Generate new food
            x = self.food_coord[self.food_index][0]
            y = self.food_coord[self.food_index][1]
            while self.board[x][y] != EMPTY_SCORE:
                self.food_index += 1
                x = self.food_coord[self.food_index][0]
                y = self.food_coord[self.food_index][1]
            self.food.append((x,y))
            self.board[x][y]=FOOD_SCORE
            self.food_index += 1
        return moves

    def play(self,display,termination=False):
        if display:
            self.display_board()
        while True:
            if termination:
                for i in self.players_ids:
                    if len(self.snakes[0])- self.current_turn/20 <= 0:
                        self.players_ids.remove(i)
                        return -2
            if len(self.players_ids) == 0:
                return -1
            if self.current_turn > self.max_turns:
                return 0
            moves=self.move()
            self.current_turn+=1
            if display:
                for move in moves:
                    if move == UP:
                        print("UP")
                    elif move == DOWN:
                        print("DOWN")
                    elif move == RIGHT:
                        print("RIGHT")
                    else:
                        print("LEFT")
                self.display_board()
                if self.gui is not None:
                    self.gui.update()
                time.sleep(0.3)

    def display_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == EMPTY_SCORE:
                    print("|_",end="")
                elif self.board[i][j] == FOOD_SCORE:
                    print("|#",end="")
                else:
                    print("|"+str(int(self.board[i][j])),end="")
            print("|")

import tkinter as tk
class GUI:
    def __init__(self,game,size):
        self.game=game
        self.game.gui=self
        self.size=size
        self.ratio= self.size / self.game.board_size
        self.app=tk.Tk()
        self.canvas=tk.Canvas(self.app,width=self.size,height=self.size)
        self.canvas.pack()
        for i in range(len(self.game.snakes)):
            color='#'+'{0:03X}'.format((i+1)*500)
            snake=self.game.snakes[i]
            self.canvas.create_rectangle(self.ratio*(snake[-1][1]),self.ratio*(snake[-1][0]),self.ratio*(snake[-1][1]+1),self.ratio*(snake[-1][0]+1),fill=color)

            for j in range(len(snake)-1):
                color = '#' + '{0:03X}'.format((i + 1) * 123)
                self.canvas.create_rectangle(self.ratio * (snake[j][1]), self.ratio * (snake[j][0]),
                                             self.ratio * (snake[j][1] + 1), self.ratio * (snake[j][0] + 1),
                                             fill=color)
        for food in self.game.food:
            self.canvas.create_rectangle(self.ratio*(food[1]),self.ratio*(food[0]),self.ratio*(food[1]+1),self.ratio*(food[0]+1),fill='#000000000')


    def update(self):
        self.canvas.delete("all")
        for i in range(len(self.game.snakes)):
            color = '#' + '{0:03X}'.format((i + 1) * 500)
            snake = self.game.snakes[i]
            self.canvas.create_rectangle(self.ratio * (snake[-1][1]), self.ratio * (snake[-1][0]),
                                         self.ratio * (snake[-1][1] + 1), self.ratio * (snake[-1][0] + 1), fill=color)

            for j in range(len(snake) - 1):
                color = '#' + '{0:03X}'.format((i + 1) * 123)
                self.canvas.create_rectangle(self.ratio * (snake[j][1]), self.ratio * (snake[j][0]),
                                             self.ratio * (snake[j][1] + 1), self.ratio * (snake[j][0] + 1),
                                             fill=color)
        for food in self.game.food:
            self.canvas.create_rectangle(self.ratio * (food[1]), self.ratio * (food[0]), self.ratio * (food[1] + 1),
                                         self.ratio * (food[0] + 1), fill='#000000000')
        self.canvas.pack()
        self.app.update()