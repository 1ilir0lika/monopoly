import pygame
import sys
from pygame.locals import *
import random
import classi
import functions
import set_board
# Initialize Pygame
pygame.init()
width_game, height_game = 1400, 1400
width_window, height_window = 3000, 1500
# Set the caption for the game window
pygame.display.set_caption("Monopoly")
# Load the image from the specified file path
board = pygame.image.load('bg.png')
board = pygame.transform.scale(board, (width_game, height_game))
# Open screen as full screen
screen = pygame.display.set_mode((width_window, height_window), pygame.FULLSCREEN)
# Flag to control the game loop
game_running = True
# Function that displays the stats of the board.players aligning their names even if they have different lengths
def display_stats():
    font = pygame.font.Font('freesansbold.ttf', 90)
    for i in range(len(set_board.players)):
        name = set_board.players[i].name
        cash = set_board.players[i].cash
        #flag of the player use png with the name of the flag
        flag = pygame.image.load(set_board.players[i].flag + '.png')
        flag = pygame.transform.scale(flag, (150, 100))
        screen.blit(flag, (width_game + width_window / 5, 400 + 200 * i))
        text = font.render(name + " " + str(cash) + " ", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (width_game + width_window / 5, 400 + 200 * i)
        screen.blit(text, text_rect)

# Function that displays the players
def display_players():
    for i in range(len(set_board.players)):
        player = pygame.image.load(set_board.players[i].flag + '.png')
        player = pygame.transform.scale(player, (100, 70))
        screen.blit(player, set_board.players[i].flag_position())
# Main game loop
while game_running:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Set background color
    screen.fill((0, 128, 0), (0, 0, width_window, height_window))
    # Display the game board
    screen.blit(board, (25, 25))
    #add image it.png inside the game window
    it = pygame.image.load('it.png')
    it = pygame.transform.scale(it, (100, 70))
    screen.blit(it, (100,1300))
    # Display the title of the game
    font = pygame.font.SysFont('Times New Roman', 150)
    text = font.render('MONOPOLY', True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (width_game + width_window / 5, 150)
    screen.blit(text, text_rect)
    display_players()
    # Update the display
    display_stats()
    pygame.display.update()
    # Clear the screen for the next iteration
    screen.fill((0, 128, 0), (0, 0, width_window, height_window))
    # Add 500 to Elon Musk jr every second
    set_board.players[0].cash += 500
    # Move the player
    functions.move_player(set_board.players[0])
    # Delay for 500 milliseconds
    pygame.time.delay(1000)  # Use pygame.time.delay instead of time.sleep
