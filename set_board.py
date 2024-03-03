import classi
import pygame
width_game, height_game = 1400, 1400
width_window, height_window = 3000, 1500
# Set the caption for the game window
pygame.display.set_caption("Monopoly")
# Load the image from the specified file path
board = pygame.image.load('bg.png')
board = pygame.transform.scale(board, (width_game, height_game))
# Open screen as full screen
screen = pygame.display.set_mode((width_window, height_window), pygame.FULLSCREEN)
#screen = pygame.display.set_mode((width_window, height_window))
# Set background color
screen.fill((0, 128, 0), (0, 0, width_window, height_window))
# Display the game board
screen.blit(board, (25, 25))
pygame.display.update()
button_si=classi.Button(300,300,150,100,"sí")
button_no=classi.Button(1000,300,150,100,"no")
button_si.process()
button_no.process()
# Flag to control the game loop
game_running = True
# Function that displays the stats of the board.players aligning their names even if they have different lengths
players=[
            classi.Player("Elon Musk jr", 20000,0,"us"),
            classi.Player("Roberto Dettobene", 7000,0,"it"),
            classi.Player("Ilir Lika", 500,0,"al"),
            classi.Player("Lee Shang", 40,0,"nk"),
            classi.Player("Abu Bakr", 5,0,"bur"),
        ]
board_positions = [
    classi.Property("Via", 0, 0,0),
    classi.Property("Vicolo Corto", 60, 2,1),
    classi.Property("Imprevisto", 0, 0,2),
    classi.Property("Vicolo Stretto", 60, 4,3),
    classi.Property("Tassa Patrimoniale", 200, 0,4),
    classi.Property("Stazione Sud", 200, 25,5),
    classi.Property("Bastioni Gran Sasso", 100, 6,6),
    classi.Property("Probabilita", 0, 0,7),
    classi.Property("Viale Monterosa", 100, 6,8),
    classi.Property("Viale Vesuvio", 120, 8,9),
    classi.Jail("Prigione", 10),
    classi.Property("Via Accademia", 140, 10,11),
    classi.Property("Corso Ateneo", 150, 10,12),
    classi.Property("Stazione Ovest", 200, 25,13),
    classi.Property("Viale Colombo", 140, 10,14),
    classi.Property("Imprevisto", 0, 0,15),
    classi.Property("Viale Costantino", 160, 12,16),
    classi.Property("Piazza Universita", 180, 14,17),
    classi.Property("Stazione Nord", 200, 25,18),
    classi.Property("Corso Raffaello", 180, 14,19),
    classi.Property("Piazza Dante", 200, 16,20),
    classi.Property("Probabilita", 0, 0,21),
    classi.Property("Via Marco Polo", 220, 18,22),
    classi.Property("Viale dei Giardini", 220, 18,23),
    classi.Property("Stazione Est", 200, 25,24),
    classi.Property("Largo Colombo", 240, 20,25),
    classi.Property("Largo Augusto", 260, 22,26),
    classi.Property("Acqua Potabile", 150, 0,27),
    classi.Property("Viale dei Fiori", 260, 22,28),
    classi.Jail("In Prigione", 29),
    classi.Property("Corso Magellano", 280, 24,30),
    classi.Property("Via Dei Gigli", 300, 26,31),
    classi.Property("Stazione Centrale", 200, 25,32),
    classi.Property("Lungomare", 300, 26,33),
    classi.Property("Probabilita", 0, 0,34),
    classi.Property("Viale Costanzo", 320, 28,35),
    classi.Property("Viale Traiano", 350, 35,36),
    classi.Property("Imprevisto", 0, 0,37),
    classi.Property("Corso Impero", 400, 50,38),
    classi.Property("Tassa di Lusso", 100, 0,39),
    ]
