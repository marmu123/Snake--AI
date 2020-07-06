from players import *
from game import *

board_size = 10
no_snakes = 1
players=[RandomPlayer(0)]
gsize=800

population_size=50
no_gen=1000
no_trails=1
window_size=7
hidden_size=15

gen_player=Player(population_size,no_gen,no_trails,window_size,hidden_size,board_size,mut_chance=0.1,mut_size=0.1)
gen_player.evolve_pop()
# g=Game(board_size, no_snakes, players)
# gui=GUI(game=g,size=gsize)
# g.play(True,termination=False)