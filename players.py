from game import *
import random as rand
import math
class RandomPlayer:
    def __init__(self,i):
        self.i=i

    def get_move(self,board,snake):
        r=rand.randint(0,3)
        return MOVES[r]


class Player:
    def __init__(self,population_size,no_gen,no_trails,window_size,hidden_size,board_size,mut_chance=0.1,mut_size=0.1):
        self.population_size=population_size
        self.no_gen=no_gen
        self.no_trails=no_trails
        self.window_size=window_size
        self.hidden_size=hidden_size
        self.board_size=board_size
        self.mut_chance=mut_chance
        self.mut_size=mut_size

        self.display=False

        # Brain selected that plays the game
        self.current_brain=None
        self.population=[self.generate_new_brain(self.window_size**2,self.hidden_size,len(MOVES)) for _ in range(self.population_size)]

    def generate_new_brain(self,input_size,hidden_size,output_size):
        hidden_layer1=np.array([[rand.uniform(-1,1) for _ in range(input_size+1)] for _ in range(hidden_size)])
        hidden_layer2 = np.array([[rand.uniform(-1, 1) for _ in range(hidden_size + 1)] for _ in range(hidden_size)])
        output_layer = np.array([[rand.uniform(-1, 1) for _ in range(hidden_size + 1)] for _ in range(output_size)])
        return [hidden_layer1,hidden_layer2,output_layer]

    def get_move(self,board,snake):
        input_vector=self.process_board(board,snake[-1][0],snake[-1][1],snake[-2][0],snake[-2][1])
        hidden_layer1=self.current_brain[0]
        hidden_layer2=self.current_brain[1]
        output_layer=self.current_brain[2]

        # Forward propagate
        result1 = np.array([math.tanh(np.dot(input_vector,hidden_layer1[i])) for i in range(hidden_layer1.shape[0])]+[1])
        result2 = np.array([math.tanh(np.dot(result1, hidden_layer2[i])) for i in range(hidden_layer2.shape[0])] + [1])
        output_result = np.array([np.dot(result2, output_layer[i]) for i in range(output_layer.shape[0])])
        max_index=np.argmax(output_result)
        return MOVES[max_index]

    def process_board(self,board,x1,y1,x2,y2):
        # x,y position of the snake
        input_vector=[[0 for _ in range(self.window_size)] for _ in range(self.window_size)]
        for i in range(self.window_size):
            for j in range(self.window_size):
                ii=x1+i-self.window_size//2
                jj=y1+j-self.window_size//2
                if ii<0 or jj<0 or ii>=self.board_size or jj>=self.board_size:
                    input_vector[i][j] = -1
                elif board[ii][jj]==FOOD_SCORE:
                    input_vector[i][j] = 1
                elif board[ii][jj] == EMPTY_SCORE:
                    input_vector[i][j] = 0
                else:
                    input_vector[i][j] = -1

        if self.display:
            print(np.array(input_vector))

        input_vector=list(np.array(input_vector).flatten())+[1]
        return np.array(input_vector)

    def reproduce(self, top25):
        new_population=[]
        for p in top25:
            new_population.append(p)

        for b in top25:
            new_brain=self.mutation(b)
            new_population.append(new_brain)
        for _ in range(self.population_size//2):
            new_population.append(self.generate_new_brain(self.window_size**2,self.hidden_size,len(MOVES)))
        return new_population

    def mutation(self,brain):
        new_brain=[]
        for layer in brain:
            new_layer=np.copy(layer)
            for i in range(new_layer.shape[0]):
                for j in range(new_layer.shape[1]):
                    if rand.uniform(0,1)<self.mut_chance:
                        new_layer[i][j]+=rand.uniform(-1,1)*self.mut_size
            new_brain.append(new_layer)
        return new_brain

    def one_generation(self):
        scores=[0 for _ in range(self.population_size)]
        max_score=0
        for i in range(self.population_size):
            for j in range(self.no_trails):
                self.current_brain=self.population[i]
                game=Game(self.board_size,1,[self])
                outcome=game.play(False,termination=True)
                score=len(game.snakes[0]) #single player mode
                scores[i]+=score
                if outcome==0:
                    print("Snake ",i,"made it to the last turn")
                if score>max_score:
                    max_score=score
                    print(max_score,"with id ",i)

        top25_indexes=list(np.argsort(scores))[3*(self.population_size//4):self.population_size]
        print(scores)
        top25=[self.population[i] for i in top25_indexes][::-1]
        self.population=self.reproduce(top25)

    def evolve_pop(self):
        for i in range(self.no_gen):
            self.one_generation()
            print("Gen ",i)

        key=input("enter any char to display board")
        for brain in self.population:
            self.display=True
            self.current_brain=brain
            game=Game(self.board_size,1,[self],display=True)
            gui=GUI(game=game,size=800)
            game.play(True,termination=True)
            print("Snake len ",len(game.snakes[0]))
