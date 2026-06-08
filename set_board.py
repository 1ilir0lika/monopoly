import classi
import pygame

# ---------------------------------------------------------------------------
# Display setup – auto-detect screen resolution
# ---------------------------------------------------------------------------
pygame.init()
info = pygame.display.Info()
width_window  = info.current_w
height_window = info.current_h

# Board occupies the left portion; sidebar takes the rest
board_margin   = 20
board_size     = min(height_window - board_margin * 2, int(width_window * 0.60))
board_x        = board_margin
board_y        = (height_window - board_size) // 2

sidebar_x      = board_x + board_size + board_margin * 2
sidebar_width  = width_window - sidebar_x - board_margin
width_game     = board_size   # kept for legacy compat

pygame.display.set_caption("Monopoly")

board_img = pygame.image.load('bg.png')
board_img = pygame.transform.scale(board_img, (board_size, board_size))

screen = pygame.display.set_mode((width_window, height_window), pygame.FULLSCREEN)
screen.fill((0, 100, 50))
screen.blit(board_img, (board_x, board_y))
pygame.display.update()

# ---------------------------------------------------------------------------
# Buttons – positioned relative to board/sidebar
# ---------------------------------------------------------------------------
btn_w, btn_h = max(160, sidebar_width // 3), 55
btn_y_base   = height_window // 2

button_si    = classi.Button(board_x + board_size // 4 - btn_w // 2,  btn_y_base, btn_w, btn_h, "Sí  ✓")
button_no    = classi.Button(board_x + 3 * board_size // 4 - btn_w // 2, btn_y_base, btn_w, btn_h, "No  ✗")
button_fatto = classi.Button(board_x + board_size // 2 - btn_w // 2,  btn_y_base + 80, btn_w, btn_h, "Fatto ✓")

game_running = True

# ---------------------------------------------------------------------------
# Players
# ---------------------------------------------------------------------------
players = [
    classi.Player("Elon Musk jr",       20000, 0, "us"),
    classi.Player("Roberto Dettobene",   7000, 0, "it"),
    classi.Player("Ilir Lika",            500, 0, "al"),
    classi.Player("Lee Shang",             40, 0, "nk"),
    classi.Player("Abu Bakr",               5, 0, "bur"),
]

# ---------------------------------------------------------------------------
# Board positions
# ---------------------------------------------------------------------------
board_positions = [
    classi.Property("Via",                     0,   0,  0),
    classi.Property("Vicolo Corto",           60,   2,  1),
    classi.Imprevisto("Imprevisto",               2),
    classi.Property("Vicolo Stretto",         60,   4,  3),
    classi.Tax("Tassa Patrimoniale",         200,      4),
    classi.Property("Stazione Sud",          200,  25,  5),
    classi.Property("Bastioni Gran Sasso",   100,   6,  6),
    classi.Probabilita("Probabilita",             7),
    classi.Property("Viale Monterosa",       100,   6,  8),
    classi.Property("Viale Vesuvio",         120,   8,  9),
    classi.Jail("Prigione",                      10),
    classi.Property("Via Accademia",         140,  10, 11),
    classi.Property("Corso Ateneo",          150,  10, 12),
    classi.Property("Stazione Ovest",        200,  25, 13),
    classi.Property("Viale Colombo",         140,  10, 14),
    classi.Imprevisto("Imprevisto",              15),
    classi.Property("Viale Costantino",      160,  12, 16),
    classi.Property("Piazza Universita",     180,  14, 17),
    classi.Property("Stazione Nord",         200,  25, 18),
    classi.Property("Corso Raffaello",       180,  14, 19),
    classi.Property("Piazza Dante",          200,  16, 20),
    classi.Probabilita("Probabilita",            21),
    classi.Property("Via Marco Polo",        220,  18, 22),
    classi.Property("Viale dei Giardini",    220,  18, 23),
    classi.Property("Stazione Est",          200,  25, 24),
    classi.Property("Largo Colombo",         240,  20, 25),
    classi.Property("Largo Augusto",         260,  22, 26),
    classi.Property("Acqua Potabile",        150,   0, 27),
    classi.Property("Viale dei Fiori",       260,  22, 28),
    classi.Jail("In Prigione",                   29),
    classi.Property("Corso Magellano",       280,  24, 30),
    classi.Property("Via Dei Gigli",         300,  26, 31),
    classi.Property("Stazione Centrale",     200,  25, 32),
    classi.Property("Lungomare",             300,  26, 33),
    classi.Probabilita("Probabilita",            34),
    classi.Property("Viale Costanzo",        320,  28, 35),
    classi.Property("Viale Traiano",         350,  35, 36),
    classi.Imprevisto("Imprevisto",              37),
    classi.Property("Corso Impero",          400,  50, 38),
    classi.Tax("Tassa di Lusso",             200,      39),
]

# ---------------------------------------------------------------------------
# Card texts  (note: swapped from original – imprevisti = Chance,
# probabilita = Community Chest)
# ---------------------------------------------------------------------------
imprevisti = [
    "Vivi in Senegal e il Presidente ha annullato le elezioni democratiche. "
    "Dakar è in subbuglio, il 4G non funziona e non puoi muoverti. Salti un turno.",

    "Il vulcano Grindavick è eruttato mentre ti trovi nei paraggi. "
    "Indietreggia di 2 caselle per evitare la lava!",

    "Arrivato in Libia nascosto su un camion, vieni scoperto e espulso. "
    "Torni indietro di 1 casella.",

    "Uno sciame di locuste ha distrutto il tuo raccolto. "
    "Non puoi pagare i debitori: vai in prigione per un turno.",

    "Un'improvvisa inondazione ha allagato le strade. Sei bloccato per un turno.",

    "Goldman Sachs ha abbassato il rating delle tue azioni. "
    "Perdi il 10% del loro valore.",

    "Un virus emergente ha fatto spillover in Thailandia. "
    "Si prospetta un'emergenza sanitaria: salta un turno.",

    "Un colpo di stato in Turkmenistan blocca le frontiere. "
    "Devi cambiare strada: torna indietro di 3 caselle.",

    "Sei un sans-papier al porto di Calais e vieni fermato dalla Gendarmerie. "
    "Vai in prigione per due turni.",

    "Blocco del traffico per qualità dell'aria pessima. Stai fermo un turno.",

    "Hanno aumentato la TARI. Dai il 10% del tuo patrimonio alla cassa.",

    "Hanno aumentato la tassa sull'energia. "
    "Dai 1 caramella per ogni proprietà che possiedi.",

    "Tua moglie ha chiesto il divorzio. "
    "Non puoi saldare il contratto prematrimoniale: finisci in prigione per un turno.",

    "Una guerra improvvisa limita il gas. "
    "Aumentano i prezzi: devi pagare 10 caramelle come tassa.",

    "La guerra fa aumentare il prezzo del grano. "
    "Il mercato nero raddoppia: paghi 10 caramelle.",
]

probabilita = [
    "Un compagno complottista sostiene che il cambiamento climatico sia un'invenzione dei potenti. "
    "Convincilo che esiste davvero e va affrontato subito!",

    "Ha piovuto dopo mesi, abbassando il PM10. "
    "Vai veloce in bicicletta: avanza di 2 caselle!",

    "Vieni riconosciuto titolare di protezione internazionale. "
    "Ottieni i documenti e nuovi diritti: vai avanti di 2 caselle.",

    "La Melissa & Bill Gates Foundation chiede di finanziare la tua idea di WC senz'acqua. "
    "Come la presenti?",

    "La banca vuole finanziarti ma hai solo 100€, nessuna proprietà e una laurea in economia. "
    "Come la convinci?",

    "Vuoi giocare in Borsa e devi dimostrare le tue qualità matematiche. Risolvi!",

    "Hai vinto una borsa di studio grazie ai tuoi meriti. Avanza di 3 caselle.",

    "Un colloquio di lavoro: devi convincere in inglese il cliente delle potenzialità dei pannelli fotovoltaici.",

    "Ti hanno notato per le tue qualità atletiche. "
    "Per entrare nella squadra olimpionica devi fare 40 flessioni in 60 secondi.",

    "Come avvocato, devi difendere la tesi: ogni uomo e donna è uguale davanti alla legge "
    "e deve avere le stesse opportunità.",
]
