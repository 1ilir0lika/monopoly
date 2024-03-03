import random
from pygame.locals import *
import classi
import set_board
import pygame 
import sys
# Function that displays the players
def display_players():
    for i in range(len(set_board.players)):
        player = pygame.image.load(set_board.players[i].flag + '.png')
        player = pygame.transform.scale(player, (100, 70))
        set_board.screen.blit(player, set_board.players[i].flag_position())
# Function that move the player based on a random dice roll
def move_player(player):
    if player.jail:
        player.jail = False
        #if the player is in jail he can't move
        return
    dice = random.randint(1, 6)
    print("il dado ha fatto "+str(dice))
    player.position += dice
    if player.position >= len(set_board.board_positions):
        player.position -= len(set_board.board_positions)
        player.cash += 200
    pygame.display.update()
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
                set_board.button_si.draw(set_board.screen)
                set_board.button_no.draw(set_board.screen)
                pygame.display.update()
                #ask input by creating 2 cliccable buttons
                #if the player clics on the yes button buy the property
                while True:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                    set_board.button_si.process()
                    set_board.button_no.process()
                    if set_board.button_si.Pressed or set_board.button_no.Pressed:
                        #if not added it takes the input multiple times
                        pygame.time.wait(250)
                        break
                if set_board.button_si.Pressed:
                    #print("é stato premuto il bottone sí")
                    set_board.board_positions[player.position].buy(player)
                    player.properties.append(set_board.board_positions[player.position].name)
                    set_board.button_si.Pressed = False
                    pass
                    #if the player clics on the no button do nothing
                elif set_board.button_no.Pressed:
                    #print("é stato premuto il bottone no")
                    set_board.button_no.Pressed = False
                    pass
            else:
                print("Devi pagare "+str(set_board.board_positions[player.position].rent)+" a "+set_board.board_positions[player.position].owner)
                for i in range(len(set_board.players)):
                    if set_board.players[i].name == set_board.board_positions[player.position].owner:
                        set_board.players[i].cash += set_board.board_positions[player.position].rent
                        player.cash -= set_board.board_positions[player.position].rent
        case classi.Imprevisto:
            print("Hai pescato una carta imprevisto")
            probabilita = set_board.probabilita[random.randint(1, len(set_board.probabilita))]
            font = pygame.font.Font('freesansbold.ttf', 90)
            text = font.render(probabilita, True, (0, 0, 0))
            #set background and show the text
            set_board.screen.fill((0, 128, 0), (0, 0, set_board.width_window, set_board.height_window))
            set_board.screen.blit(text, (50, 800))
            set_board.button_fatto.draw(set_board.screen)
            pygame.display.update()
            while True:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                    set_board.button_fatto.process()
                    if set_board.button_fatto.Pressed:
                        #if not added it takes the input multiple times
                        pygame.time.wait(250)
                        set_board.button_fatto.Pressed = False
                        break
            pygame.display.update()
        case classi.Probabilita:
            print("Hai pescato una carta probabilità")
            imprevisto = set_board.imprevisti[random.randint(1, len(set_board.imprevisti))]
            font = pygame.font.Font('freesansbold.ttf', 90)
            text = font.render(imprevisto, True, (0, 0, 0))
            #set background and show the text
            set_board.screen.fill((0, 128, 0), (0, 0, set_board.width_window, set_board.height_window))
            #wrap the text
            set_board.screen.blit(text, (50, 800))
            set_board.screen.draw
            set_board.button_fatto.draw(set_board.screen)
            pygame.display.update()
            while True:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                    set_board.button_fatto.process()
                    if set_board.button_fatto.Pressed:
                        #if not added it takes the input multiple times
                        pygame.time.wait(250)
                        set_board.button_fatto.Pressed = False
                        break
            pygame.display.update()
        case classi.Tax:
            print("Devi pagare "+str(set_board.board_positions[player.position].amount)+" di tasse")
            player.cash -= set_board.board_positions[player.position].amount
        case classi.Jail:
            print("Sei in prigione")
            player.jail = True
        case _:
            print("Non é possibile fare nulla")
# Function that displays the stats of the board.players aligning their names even if they have different lengths
def display_stats(current_player):
    font = pygame.font.Font('freesansbold.ttf', 90)
    for i in range(len(set_board.players)):
        name = set_board.players[i].name
        if set_board.players[i] == current_player:
            print("ora sta giocando "+current_player.name)
            name = name + "*"
        cash = set_board.players[i].cash
        #flag of the player use png with the name of the flag
        flag = pygame.image.load(set_board.players[i].flag + '.png')
        flag = pygame.transform.scale(flag, (100, 70))
        set_board.screen.blit(flag, (set_board.width_game + set_board.width_window / 5, 450 + 200 * i))
        text = font.render(name + " " + str(cash)+"$" + " ", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (set_board.width_game + set_board.width_window / 5, 400 + 200 * i)
        set_board.screen.blit(text, text_rect)
        pygame.display.update()
