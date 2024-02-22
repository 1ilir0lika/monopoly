import random
from pygame.locals import *
import classi
import set_board
# Function that move the player based on a random dice roll
def move_player(player):
    dice = random.randint(1, 6)
    print("il dado ha fatto "+str(dice))
    player.position += dice
    if player.position >= len(set_board.board_positions):
        player.position -= len(set_board.board_positions)
        player.cash += 200
    print("la posizione é "+str(player.position))