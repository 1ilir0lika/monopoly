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
button_fatto=classi.Button(1300,1000,150,100,"fatto")
button_si.process()
button_no.process()
button_fatto.process()
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
    classi.Imprevisto("Imprevisto",2),
    classi.Property("Vicolo Stretto", 60, 4,3),
    classi.Tax("Tassa Patrimoniale",200,4),
    classi.Property("Stazione Sud", 200, 25,5),
    classi.Property("Bastioni Gran Sasso", 100, 6,6),
    classi.Probabilita("Probabilita",7),
    classi.Property("Viale Monterosa", 100, 6,8),
    classi.Property("Viale Vesuvio", 120, 8,9),
    classi.Jail("Prigione", 10),
    classi.Property("Via Accademia", 140, 10,11),
    classi.Property("Corso Ateneo", 150, 10,12),
    classi.Property("Stazione Ovest", 200, 25,13),
    classi.Property("Viale Colombo", 140, 10,14),
    classi.Imprevisto("Imprevisto",15),
    classi.Property("Viale Costantino", 160, 12,16),
    classi.Property("Piazza Universita", 180, 14,17),
    classi.Property("Stazione Nord", 200, 25,18),
    classi.Property("Corso Raffaello", 180, 14,19),
    classi.Property("Piazza Dante", 200, 16,20),
    classi.Probabilita("Probabilita",21),
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
    classi.Probabilita("Probabilita",34),
    classi.Property("Viale Costanzo", 320, 28,35),
    classi.Property("Viale Traiano", 350, 35,36),
    classi.Imprevisto("Imprevisto",37),
    classi.Property("Corso Impero", 400, 50,38),
    classi.Tax("Tassa di Lusso",200,39),
    ]
imprevisti =[
    """Vivi in Senegal e il Presidente ha annullato le elezioni politiche democratiche.
      Si verificano sconvolgimenti politici nella città in cui vivi,
    Dakar, il 4G non funziona, non puoi uscire di casa e non puoi spostarti. Salti un turno.""",
    """Il vulcano Grindavick ha eruttato mentre ti trovi nei paraggi. Indietrreggia di 2 caselle per evitare che la lava ti sommerga",
    "Arrivato in libia con un camion trasporta-merci, vieni scoperto attaccato sotto di esso.
    Vieni espulso dal Paese e riportato nel tuo di origine (in Niger).
    Torni indietro di 1 casella""",
    "Uno sciame di locuste ha distrutto il tuo raccolto e non potrai pagare i tuo debitori vai in prigione per un turno",
    "Una improvvisa inondazione ha completamento allagato le strade sterrate del tuo paese. Sei bloccato per un turno",
    "Goldman Sachs ha abbassato il rating delle quotazioni in borsa delle azioni che possiedi. Perdi il 10 % del loro valore",
    "Un virus emergente ha fatto spillover in Thailandia si prospetta un periodo di emergenza sanitaria salta un turno",
    "Un colpo di stato in Turkmenistan ha portato ad un blocco delle frontiere devi cambiare strada. Torni indietro di tre caselle",
    "Sei un sans papier al porto di Calais e vieni fermato dalla Genarmerie vai in prigione per due turni",
    "La qualità dell'aria è pessima c'è un blocco delle auto. Stai fermo un turno",
    "Hanno aumentato la tassa sulla Tari. Dai il 10% del tuo patrimonio alla cassa",
    "Hanno aumentato la tassa sull'energia. Dai 1 caramella per ogni via in tuo possesso",
    "La tua moglie ha chiesto il divorzio non puoi saldare il contratto prematrimoniale finisci in prigione per un turno",
    "Una improvvisa guerra limita l'accesso al gas. Aumentano i prezzi devi dare come tassa 10 caramelle",
    "Una improvvisa guerra fa aumentare il prezzo del grano. Il prezzo al mercato nero raddoppia. Devi pagare 10 caramelle",
]
probabilita =[
    """Un complottista (compagno) sostiene che il cambiamento climatico sia soltanto un'invenzione dei potenti della terra.
    Convincilo che in realtà il cambiamento climatico esiste davvero e bisogna affrontarlo subito.""",
    """La scorsa settimana ha piovuto dopo diversi mesi, riducendo i livelli di PM10 nell'aria e 
    permettendoti di respirare meglio mentre vai in bicicletta in città.
      Vai veloce e vai avanti di 2 caselle!""",
    "Vieni riconosciuto titolare di protezione internazionale, ottieni i documenti e puoi finalmente avere maggiori diritti sul territorio in cui ti trovi: vai avanti di 2 caselle",
    "Devi convincere la Melissa e Bil Gates Foundation a finanziare la tua idea di wc senza uso di acqua come fai ?",
    "Devi convincere la banca a farti un finanziamento ma hai solo 100 euro, nessuna proprietà ma solo una laurea in economia e la tua giovane età",
    "Vuoi giocare in borsa e devi dimostrare le tue qualità matematiche...risolvi.",
    "Hai vinto grazie ai tuoi meriti una borsa di studio. Avanza di tre caselle",
    "Una nuova opportunità si apre hai un colloquio di lavoro. Devi in inglese convincere il tuo acquirente delle potenzialità dei pannelli fotovoltaici",
    "Hai una possibilità inaspettata. Ti hanno notato per le tue qualità atletiche. Per entrare nella squadra olimpionica devi fare 40 piegamenti sulle braccia in 60 secondi",
    """Devi mostrare la tua bravura come avvocato/ oratore: devi difendere la seguente tesi: 
    ogni uomo e donna è uguale davanti alla legge e deve avere le stesse opportunità""",
]
