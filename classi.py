from enum import Enum
import pygame
# Class that represents a player
class Player:
    def __init__(self, name,cash,position,flag):
        self.name = name
        self.cash = cash
        self.position = position
        self.flag = flag
        self.properties = []
        self.jail = False
    # Function that returns the position of the flag on the board    
    def flag_position(self):  
        #max=1300
        #min=100
        if self.position < 10:
            x = 1300 - 100 * self.position
            y = 1300
        elif self.position < 20:
            x = 100
            y = 1300 - 100 * (self.position - 10)
        elif self.position < 30:
            x = 100 + 100 * (self.position - 20)
            y = 100
        else:
            x = 1300   
            y = 100 + 100 * (self.position - 30)
        #print(x,y)
        return (x,y)

# Class that represents a property
class Property:
    def __init__(self, name, price, rent,position):
        self.name = name
        self.price = price
        self.rent = rent
        self.position = position
        self.owner = None
    # Function lets the player buy the property
    def buy(self, player):
        if player.cash >= self.price and self.owner == None:
            player.cash -= self.price
            self.owner  = player.name
            return True
        else:
            return False
        

#Class that represents a chance
class Imprevisto:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        #di quanto andare avanti o indietro
        #self.rel_position=rel_position
        ##dove andare
        #self.absolute_position=absolute_position
        ##somma relativa di soldi tolti o aggiunti
        #self.rel_money=rel_money
        ##somma assoluta di soldi tolti o aggiunti
        #self.abs_money=abs_money
        ##vai in prigione
        #self.jail=jail
#Class that represents a community chest
class Probabilita:
    def __init__(self, name, position):
        self.name = name
        self.position = position
#Class that represents a tax
class Tax:
    def __init__(self, name, amount, position):
        self.name = name
        self.amount = amount
        self.position = position
#Class that represents a jail
class Jail:
    def __init__(self, name, position):
        self.name = name
        self.position = position


# Enum that represents a board position,it can be a property, probabilita,imprevisto, a tax or a jail
class BoardPosition(Enum):
    PROPERTY = "PROPERTY"
    TAX = "TAX"
    JAIL = "JAIL"
    IMPREVISTO = "IMPREVISTO"
    PROBABILITA = "PROBABILITA" 


class Button():
    def __init__(self, x, y, width, height, buttonText):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.Pressed = False
        self.buttonText = buttonText

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonSurface.fill(self.fillColors['normal'])
        self.buttonRect = self.buttonSurface.get_rect(topleft=(self.x, self.y))
        screen.blit(self.buttonSurface, self.buttonRect)
        text = pygame.font.Font(None, 36).render(self.buttonText, True, (0, 0, 0))
        textRect = text.get_rect(center=self.buttonRect.center)
        screen.blit(text, textRect)
        pygame.draw.rect(screen, (0, 0, 0), self.buttonRect, 2)
        self.process()
        
    # Function that makes the button change color when the mouse is over it and change the value of the Pressed attribute
    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            pygame.display.update()
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                pygame.display.update()
                self.Pressed = True
