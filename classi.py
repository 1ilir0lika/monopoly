from enum import Enum
# Class that represents a player
class Player:
    def __init__(self, name, age,cash,position,flag):
        self.name = name
        self.age = age
        self.cash = cash
        self.position = position
        self.flag = flag
        self.properties = []
        self.jail = False
    # Function that returns the position of the flag on the board    
    def flag_position(self):  
        if self.position < 10:
            x = 100
            y = 1300 - 100 * self.position
        elif self.position < 20:
            x = 100 + 100 * (self.position - 10)
            y = 100
        elif self.position < 30:
            x = 1300
            y = 100 + 100 * (self.position - 20)
        else:
            x = 1300 - 100 * (self.position - 30)       
            y = 1300
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

