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
    #match the type of the position and do the corresponding action
    match type(set_board.board_positions[player.position]):
        case classi.Property:
            if set_board.board_positions[player.position].owner == None:
                print("Vuoi comprare "+set_board.board_positions[player.position].name+" per "+str(set_board.board_positions[player.position].price)+"?")
                answer = input("si/no")
                if answer == "si":
                    set_board.board_positions[player.position].buy(player)
            else:
                print("Devi pagare "+str(set_board.board_positions[player.position].rent)+" a "+set_board.board_positions[player.position].owner)
                for i in range(len(set_board.players)):
                    if set_board.players[i].name == set_board.board_positions[player.position].owner:
                        set_board.players[i].cash += set_board.board_positions[player.position].rent
                        player.cash -= set_board.board_positions[player.position].rent
        case classi.Imprevisto:
            print("Hai pescato una carta imprevisto")
        case classi.Probabilita:
            print("Hai pescato una carta probabilità")
        case classi.Tax:
            print("Devi pagare "+str(set_board.board_positions[player.position].amount)+" di tasse")
            player.cash -= set_board.board_positions[player.position].amount
        case classi.Jail:
            print("Sei in prigione")
            player.jail = True
            player.position = 10
        case _:
            print("Non é possibile fare nulla")
