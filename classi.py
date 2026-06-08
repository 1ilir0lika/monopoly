from enum import Enum
import pygame


class Player:
    def __init__(self, name, cash, position, flag):
        self.name = name
        self.cash = cash
        self.position = position
        self.flag = flag
        self.properties = []
        self.jail = False

    # Normalised (nx, ny) cell centres measured from the actual bg.png image.
    # The board image is 674×674 px; corners are ~90 px, normal cells ~53 px.
    # Multiply by board_size at runtime to get pixel coordinates.
    _CELL_NORM = [
        (0.9251, 0.9251),  # 0  GO
        (0.8160, 0.9251),  # 1
        (0.7359, 0.9251),  # 2
        (0.6565, 0.9251),  # 3
        (0.5772, 0.9251),  # 4
        (0.4970, 0.9251),  # 5
        (0.4169, 0.9251),  # 6
        (0.3368, 0.9251),  # 7
        (0.2574, 0.9251),  # 8
        (0.1780, 0.9251),  # 9
        (0.0712, 0.9251),  # 10 Jail
        (0.0712, 0.8160),  # 11
        (0.0712, 0.7359),  # 12
        (0.0712, 0.6565),  # 13
        (0.0712, 0.5772),  # 14
        (0.0712, 0.4970),  # 15
        (0.0712, 0.4169),  # 16
        (0.0712, 0.3368),  # 17
        (0.0712, 0.2574),  # 18
        (0.0712, 0.1780),  # 19
        (0.0712, 0.0712),  # 20 Free Parking
        (0.1780, 0.0712),  # 21
        (0.2574, 0.0712),  # 22
        (0.3368, 0.0712),  # 23
        (0.4169, 0.0712),  # 24
        (0.4970, 0.0712),  # 25
        (0.5772, 0.0712),  # 26
        (0.6565, 0.0712),  # 27
        (0.7359, 0.0712),  # 28
        (0.8160, 0.0712),  # 29
        (0.9251, 0.0712),  # 30 Go-to-Jail
        (0.9251, 0.1780),  # 31
        (0.9251, 0.2574),  # 32
        (0.9251, 0.3368),  # 33
        (0.9251, 0.4169),  # 34
        (0.9251, 0.4970),  # 35
        (0.9251, 0.5772),  # 36
        (0.9251, 0.6565),  # 37
        (0.9251, 0.7359),  # 38
        (0.9251, 0.8160),  # 39
    ]

    def flag_position(self, board_x, board_y, board_size, slot=0):
        """
        Return the pixel centre for this player's token.

        Uses a normalised lookup table derived from the actual board image so
        the token lands exactly in the middle of each cell regardless of the
        display resolution.

        `slot` (0, 1, 2 …) spreads multiple tokens that share the same cell
        into a small 2-column grid so they never overlap.
        """
        nx, ny = self._CELL_NORM[self.position % 40]
        cx = board_x + nx * board_size
        cy = board_y + ny * board_size

        # Spread: 2-column grid, each cell is (2*r+3) px apart
        token_r = max(10, int(board_size / 65))
        spread  = token_r * 2 + 4
        col_off = (slot % 2) * spread - spread // 2
        row_off = (slot // 2) * spread - spread // 2

        return (int(cx + col_off), int(cy + row_off))


class Property:
    def __init__(self, name, price, rent, position):
        self.name = name
        self.price = price
        self.rent = rent
        self.position = position
        self.owner = None

    def buy(self, player):
        if player.cash >= self.price and self.owner is None:
            player.cash -= self.price
            self.owner = player.name
            return True
        return False


class Imprevisto:
    def __init__(self, name, position):
        self.name = name
        self.position = position


class Probabilita:
    def __init__(self, name, position):
        self.name = name
        self.position = position


class Tax:
    def __init__(self, name, amount, position):
        self.name = name
        self.amount = amount
        self.position = position


class Jail:
    def __init__(self, name, position):
        self.name = name
        self.position = position


class BoardPosition(Enum):
    PROPERTY    = "PROPERTY"
    TAX         = "TAX"
    JAIL        = "JAIL"
    IMPREVISTO  = "IMPREVISTO"
    PROBABILITA = "PROBABILITA"


# ---------------------------------------------------------------------------
# Button – event-driven (no polling), Linux-safe
# ---------------------------------------------------------------------------
class Button:
    def __init__(self, x, y, width, height, text,
                 color_normal=(44, 110, 73),
                 color_hover=(74, 158, 110),
                 color_press=(26, 74, 50)):
        self.text         = text
        self.color_normal = color_normal
        self.color_hover  = color_hover
        self.color_press  = color_press
        self.Pressed      = False   # set to True on MOUSEBUTTONUP inside rect
        self._held        = False   # True while mouse button is held down
        self.rect         = pygame.Rect(x, y, width, height)

    def reposition(self, x, y, width=None, height=None):
        self.rect.x = x
        self.rect.y = y
        if width  is not None: self.rect.width  = width
        if height is not None: self.rect.height = height

    # Call this inside the event loop to feed mouse events
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self._held = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self._held and self.rect.collidepoint(event.pos):
                self.Pressed = True
            self._held = False

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        if self._held and self.rect.collidepoint(mouse):
            color = self.color_press
        elif self.rect.collidepoint(mouse):
            color = self.color_hover
        else:
            color = self.color_normal

        # Shadow
        shadow = self.rect.move(3, 3)
        pygame.draw.rect(screen, (0, 0, 0, 120), shadow, border_radius=10)
        # Body
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        # Border
        border_col = (255, 255, 255) if self.rect.collidepoint(mouse) else (180, 220, 180)
        pygame.draw.rect(screen, border_col, self.rect, 2, border_radius=10)
        # Label
        font = pygame.font.SysFont('DejaVu Sans', 28, bold=True)
        surf = font.render(self.text, True, (255, 255, 255))
        screen.blit(surf, surf.get_rect(center=self.rect.center))

    # Legacy no-op kept so old call-sites don't crash
    def process(self):
        pass
