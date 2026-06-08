import asyncio
import pygame
import sys
from pygame.locals import *
import functions
import set_board

pygame.init()
clock = pygame.time.Clock()

async def main():
    while set_board.game_running:
        for player in set_board.players:
            pygame.event.clear()

            functions._base_redraw(player)
            pygame.display.update()

            await asyncio.sleep(0.35)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit(); sys.exit()
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit(); sys.exit()

            await functions.move_player(player)

            functions._base_redraw(player)
            pygame.display.update()

            await asyncio.sleep(0.5)

            print(f"{player.name} | pos={player.position} | "
                  f"cash={player.cash} | props={player.properties}")

        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
