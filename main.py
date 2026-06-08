import pygame
import sys
from pygame.locals import *
import functions
import set_board

pygame.init()
clock = pygame.time.Clock()

while set_board.game_running:
    for player in set_board.players:
        # Flush any stale events before each player's turn
        pygame.event.clear()

        # Base redraw
        functions._base_redraw(player)
        pygame.display.update()

        # Small pause so the board is visible before the move
        pygame.time.wait(350)

        # Handle quit events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit(); sys.exit()

        # Do the move (handles all sub-prompts internally)
        functions.move_player(player)

        # Final redraw after move resolves
        functions._base_redraw(player)
        pygame.display.update()
        pygame.time.wait(500)

        print(f"{player.name} | pos={player.position} | "
              f"cash={player.cash} | props={player.properties}")

    clock.tick(60)

pygame.quit()
