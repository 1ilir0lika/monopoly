import pygame
import sys
from pygame.locals import *
import functions
import set_board
# Initialize Pygame
pygame.init()
while set_board.game_running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    # Set background color
    set_board.screen.fill((0, 128, 0), (0, 0, set_board.width_window, set_board.height_window))
    # Display the game board
    set_board.screen.blit(set_board.board, (25, 25))
    # Display the title of the game
    font = pygame.font.SysFont('Times New Roman', 150)
    text = font.render('MONOPOLY', True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (set_board.width_game + set_board.width_window / 5, 150)
    set_board.screen.blit(text, text_rect)
    functions.display_players()
    functions.display_stats(set_board.players[0])
    #functions.move_player(set_board.players[0])
    for player in set_board.players:
        # Set background color
        set_board.screen.fill((0, 128, 0), (0, 0, set_board.width_window, set_board.height_window))
        # Display the game board
        set_board.screen.blit(set_board.board, (25, 25))
        # Display the title of the game
        font = pygame.font.SysFont('Times New Roman', 150)
        text = font.render('MONOPOLY', True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (set_board.width_game + set_board.width_window / 5, 150)
        set_board.screen.blit(text, text_rect)
        functions.display_players()
        functions.display_stats(player)
        functions.move_player(player)
        pygame.time.wait(500)
        pygame.display.update()
        print(player.name + str(player.properties))
pygame.quit()
