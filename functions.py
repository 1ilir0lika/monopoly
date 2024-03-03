import random
from pygame.locals import *
import classi
import set_board
import pygame
# Function that displays the players
def display_players():
    for i in range(len(set_board.players)):
        player = pygame.image.load(set_board.players[i].flag + '.png')
        player = pygame.transform.scale(player, (100, 70))
        set_board.screen.blit(player, set_board.players[i].flag_position())
# Function that move the player based on a random dice roll
def move_player(player):
    dice = random.randint(1, 6)
    print("il dado ha fatto "+str(dice))
    player.position += dice
    if player.position >= len(set_board.board_positions):
        player.position -= len(set_board.board_positions)
        player.cash += 200
    pygame.display.update()
    pygame.time.delay(1000)
    print("la posizione é "+str(player.position))
    display_players()
    pygame.display.update()
    #match the type of the position and do the corresponding action
    match type(set_board.board_positions[player.position]):
        case classi.Property:
            print("Sei su "+set_board.board_positions[player.position].name)
            if set_board.board_positions[player.position].owner == None:
                #ask wheter the player wants to buy the property using the buy method graphically
                text= "Vuoi comprare "+set_board.board_positions[player.position].name+" per "+str(set_board.board_positions[player.position].price)+"?"
                font = pygame.font.Font('freesansbold.ttf', 90)
                text = font.render(text, True, (0, 0, 0))
                set_board.screen.blit(text, (50, 100))
                #ask input by creating 2 cliccable buttons
                button_si=classi.Button(100,300,100,100,"sí")
                button_no=classi.Button(500,300,100,100,"no")
                button_si.draw(set_board.screen)
                button_no.draw(set_board.screen)
                button_si.process()
                button_no.process()
                pygame.display.update()
                #if the player clics on the yes button buy the property
                while True:
                    if button_si.Pressed:
                        player.buy(set_board.board_positions[player.position])
                    #if the player clics on the no button do nothing
                    if button_no.Pressed:
                        pass
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
    # Delay 
    pygame.time.delay(1000)  # Use pygame.time.delay instead of time.sleep
# Function that displays the stats of the board.players aligning their names even if they have different lengths
def display_stats():
    font = pygame.font.Font('freesansbold.ttf', 90)
    for i in range(len(set_board.players)):
        name = set_board.players[i].name
        cash = set_board.players[i].cash
        #flag of the player use png with the name of the flag
        flag = pygame.image.load(set_board.players[i].flag + '.png')
        flag = pygame.transform.scale(flag, (150, 100))
        set_board.screen.blit(flag, (set_board.width_game + set_board.width_window / 5, 400 + 200 * i))
        text = font.render(name + " " + str(cash) + " ", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (set_board.width_game + set_board.width_window / 5, 400 + 200 * i)
        set_board.screen.blit(text, text_rect)
        pygame.display.update()
