import random
import pygame
import sys
from pygame.locals import *
import classi
import set_board

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
PLAYER_COLORS = [
    (220, 60,  60),   # red
    (60, 130, 220),   # blue
    (220, 180,  40),  # yellow
    (60, 200, 100),   # green
    (180,  80, 200),  # purple
]

# ASCII-only card icons (no Unicode emoji – Linux SDL2 can't render them)
CARD_ICON = {
    'imprevisto':  '?!',
    'probabilita': '>>',
    'tax':         '$$',
    'jail':        '[]',
    'buy':         '+',
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sf(pt, ref=1400):
    """Scale font pt proportionally to board size."""
    return max(10, int(pt * set_board.board_size / ref))


def _wrap(text, font, max_w):
    words, lines, cur = text.split(), [], []
    for w in words:
        if font.size(' '.join(cur + [w]))[0] <= max_w:
            cur.append(w)
        else:
            if cur: lines.append(' '.join(cur))
            cur = [w]
    if cur: lines.append(' '.join(cur))
    return lines


def _rr(surf, color, rect, r=12, alpha=None):
    """Draw rounded rect, optionally transparent."""
    if alpha is not None:
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(s, (*color[:3], alpha), s.get_rect(), border_radius=r)
        surf.blit(s, rect.topleft)
    else:
        pygame.draw.rect(surf, color, rect, border_radius=r)


def _base_redraw(current_player=None):
    """Redraw background + board + players + sidebar (no display.update)."""
    set_board.screen.fill((0, 90, 45))
    set_board.screen.blit(set_board.board_img,
                          (set_board.board_x, set_board.board_y))
    display_players()
    _draw_sidebar(current_player)


# ---------------------------------------------------------------------------
# Button helpers – feed ALL events to ALL active buttons each loop tick
# ---------------------------------------------------------------------------

def _pump_buttons(*buttons):
    """
    Process the pygame event queue and feed each event to the given buttons.
    Returns True if the user closed the window (caller should exit).
    """
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit(); sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit(); sys.exit()
        for btn in buttons:
            btn.handle_event(event)
    return False


# ---------------------------------------------------------------------------
# Overlay card (Imprevisto / Probabilita / Tax / Jail)
# ---------------------------------------------------------------------------

def draw_overlay_card(title, body, accent=(200, 60, 40), icon_txt='?!'):
    bx, by = set_board.board_x, set_board.board_y
    bw     = set_board.board_size

    pad    = int(bw * 0.06)
    cw     = int(bw * 0.84)
    ch     = int(bw * 0.60)
    cx     = bx + (bw - cw) // 2
    cy     = by + (bw - ch) // 2

    # Reposition button below card
    bw2 = max(160, int(bw * 0.20))
    bh2 = max(50, int(bw * 0.06))
    set_board.button_fatto.reposition(cx + cw // 2 - bw2 // 2,
                                       cy + ch + 16, bw2, bh2)

    title_font = pygame.font.SysFont('DejaVu Sans', _sf(46), bold=True)
    body_font  = pygame.font.SysFont('DejaVu Sans', _sf(28))
    icon_font  = pygame.font.SysFont('DejaVu Sans', _sf(64), bold=True)
    body_lines = _wrap(body, body_font, cw - pad * 2)
    line_h     = body_font.get_linesize() + 2

    clock = pygame.time.Clock()
    while True:
        _pump_buttons(set_board.button_fatto)

        _base_redraw()

        # Scrim
        _rr(set_board.screen, (0,0,0),
            pygame.Rect(bx, by, bw, bw), r=0, alpha=155)

        # Card shadow
        _rr(set_board.screen, (0,0,0),
            pygame.Rect(cx+5, cy+5, cw, ch), r=16, alpha=100)

        # Card body
        _rr(set_board.screen, (248, 244, 228),
            pygame.Rect(cx, cy, cw, ch), r=16)

        # Accent header band
        hh = int(ch * 0.18)
        _rr(set_board.screen, accent, pygame.Rect(cx, cy, cw, hh), r=16)
        # fill bottom half of header so top border-radius doesn't poke through
        pygame.draw.rect(set_board.screen, accent,
                         pygame.Rect(cx, cy + hh // 2, cw, hh // 2))

        # Icon circle in header
        ic_r = hh // 2 - 4
        pygame.draw.circle(set_board.screen, (255,255,255),
                           (cx + ic_r + 12, cy + hh // 2), ic_r)
        ic = icon_font.render(icon_txt, True, accent)
        set_board.screen.blit(ic, ic.get_rect(
            center=(cx + ic_r + 12, cy + hh // 2)))

        # Title in header
        ts = title_font.render(title, True, (255,255,255))
        set_board.screen.blit(ts, ts.get_rect(
            midleft=(cx + ic_r * 2 + 24, cy + hh // 2)))

        # Body lines
        text_y = cy + hh + 14
        for line in body_lines:
            ls = body_font.render(line, True, (30, 20, 10))
            set_board.screen.blit(ls, ls.get_rect(
                centerx=cx + cw // 2, y=text_y))
            text_y += line_h

        set_board.button_fatto.draw(set_board.screen)
        pygame.display.update()

        if set_board.button_fatto.Pressed:
            pygame.time.wait(120)
            set_board.button_fatto.Pressed = False
            break

        clock.tick(60)


# ---------------------------------------------------------------------------
# Buy-property prompt
# ---------------------------------------------------------------------------

def draw_buy_prompt(prop, player):
    bx, by = set_board.board_x, set_board.board_y
    bw     = set_board.board_size

    cw = int(bw * 0.80)
    ch = int(bw * 0.46)
    cx = bx + (bw - cw) // 2
    cy = by + (bw - ch) // 2

    can_afford = player.cash >= prop.price

    btn_w = max(140, int(cw * 0.28))
    btn_h = max(50, int(bw * 0.06))
    btn_y = cy + ch - btn_h - 18
    set_board.button_si.reposition(cx + cw // 4 - btn_w // 2, btn_y, btn_w, btn_h)
    set_board.button_no.reposition(cx + 3*cw // 4 - btn_w // 2, btn_y, btn_w, btn_h)

    # Style Sì differently when player can't afford
    if can_afford:
        set_board.button_si.color_normal = (30, 120, 55)
        set_board.button_si.color_hover  = (50, 160, 80)
        set_board.button_si.color_press  = (20, 80, 40)
    else:
        set_board.button_si.color_normal = (80, 80, 80)
        set_board.button_si.color_hover  = (80, 80, 80)
        set_board.button_si.color_press  = (80, 80, 80)

    hdr_font   = pygame.font.SysFont('DejaVu Sans', _sf(44), bold=True)
    name_font  = pygame.font.SysFont('DejaVu Sans', _sf(34), bold=True)
    price_font = pygame.font.SysFont('DejaVu Sans', _sf(52), bold=True)
    small_font = pygame.font.SysFont('DejaVu Sans', _sf(28))

    accent = (30, 120, 55)
    clock  = pygame.time.Clock()

    while True:
        # Only accept Sì click if player can actually afford it
        _pump_buttons(set_board.button_no,
                      *([] if not can_afford else [set_board.button_si]))

        _base_redraw(player)
        _rr(set_board.screen, (0,0,0),
            pygame.Rect(bx, by, bw, bw), r=0, alpha=150)

        # Shadow + card
        _rr(set_board.screen, (0,0,0),
            pygame.Rect(cx+5, cy+5, cw, ch), r=16, alpha=100)
        _rr(set_board.screen, (248, 244, 228),
            pygame.Rect(cx, cy, cw, ch), r=16)

        # Header band
        hh = int(ch * 0.20)
        _rr(set_board.screen, accent, pygame.Rect(cx, cy, cw, hh), r=16)
        pygame.draw.rect(set_board.screen, accent,
                         pygame.Rect(cx, cy + hh // 2, cw, hh // 2))

        # "Vuoi comprare?" header
        hs = hdr_font.render("Vuoi comprare?", True, (255, 255, 255))
        set_board.screen.blit(hs, hs.get_rect(center=(cx + cw // 2, cy + hh // 2)))

        # Property name
        ns = name_font.render(prop.name, True, (20, 60, 20))
        set_board.screen.blit(ns, ns.get_rect(
            centerx=cx + cw // 2, y=cy + hh + 12))

        # Price
        ps = price_font.render(f"{prop.price} $", True, (20, 100, 40))
        set_board.screen.blit(ps, ps.get_rect(
            centerx=cx + cw // 2, y=cy + hh + 12 + name_font.get_height() + 6))

        # Rent
        rs = small_font.render(f"Affitto: {prop.rent} $", True, (100, 60, 20))
        set_board.screen.blit(rs, rs.get_rect(
            centerx=cx + cw // 2,
            y=cy + hh + 12 + name_font.get_height() + price_font.get_height() + 10))

        # "Non puoi permettertelo" warning
        if not can_afford:
            wf = pygame.font.SysFont('DejaVu Sans', _sf(26), bold=True)
            ws = wf.render("Non puoi permettertelo!", True, (200, 50, 50))
            set_board.screen.blit(ws, ws.get_rect(
                centerx=cx + cw // 2, y=btn_y - wf.get_height() - 8))

        set_board.button_si.draw(set_board.screen)
        set_board.button_no.draw(set_board.screen)
        pygame.display.update()

        if set_board.button_si.Pressed or set_board.button_no.Pressed:
            pygame.time.wait(120)
            result = set_board.button_si.Pressed and can_afford
            set_board.button_si.Pressed = False
            set_board.button_no.Pressed = False
            # Reset button colours
            set_board.button_si.color_normal = (44, 110, 73)
            set_board.button_si.color_hover  = (74, 158, 110)
            set_board.button_si.color_press  = (26, 74, 50)
            return result

        clock.tick(60)


# ---------------------------------------------------------------------------
# Player tokens on board
# ---------------------------------------------------------------------------

def display_players():
    bs     = set_board.board_size
    radius = max(12, bs // 65)

    # Build a dict: position -> list of (player, global_index)
    from collections import defaultdict
    cell_groups = defaultdict(list)
    for i, player in enumerate(set_board.players):
        cell_groups[player.position].append((i, player))

    for pos, group in cell_groups.items():
        for slot, (i, player) in enumerate(group):
            px, py = player.flag_position(
                set_board.board_x, set_board.board_y, bs, slot=slot)

            col = PLAYER_COLORS[i % len(PLAYER_COLORS)]
            # Drop shadow
            pygame.draw.circle(set_board.screen, (0, 0, 0),
                               (px + 2, py + 2), radius)
            # Token
            pygame.draw.circle(set_board.screen, col, (px, py), radius)
            # White ring
            pygame.draw.circle(set_board.screen, (255, 255, 255),
                               (px, py), radius, 2)
            # Initial
            f   = pygame.font.SysFont('DejaVu Sans', max(9, radius - 3), bold=True)
            lbl = f.render(player.name[0].upper(), True, (20, 20, 20))
            set_board.screen.blit(lbl, lbl.get_rect(center=(px, py)))


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

def _draw_sidebar(current_player):
    sx = set_board.sidebar_x
    sw = set_board.sidebar_width
    sh = set_board.height_window

    # --- Background ---
    bg = pygame.Surface((sw, sh), pygame.SRCALPHA)
    bg.fill((0, 55, 28, 210))
    set_board.screen.blit(bg, (sx, 0))

    # --- Title ---
    tf = pygame.font.SysFont('DejaVu Sans', _sf(62, 1400), bold=True)
    ts = tf.render('MONOPOLY', True, (255, 210, 50))
    tr = ts.get_rect(centerx=sx + sw // 2, y=22)
    set_board.screen.blit(ts, tr)

    sep_y = tr.bottom + 14
    pygame.draw.line(set_board.screen, (255, 210, 50),
                     (sx + 16, sep_y), (sx + sw - 16, sep_y), 2)

    # --- Layout: divide remaining height equally among players ---
    n        = len(set_board.players)
    spacing  = 10
    card_x   = sx + 16
    card_w   = sw - 32
    total_h  = sh - sep_y - 18 - spacing   # total available
    card_h   = (total_h - spacing * (n - 1)) // n  # equal height per card
    start_y  = sep_y + 18

    # Fixed font sizes that must fit inside card_h
    # name + cash = 2 fixed rows; rest of space goes to properties
    name_pt  = _sf(24, 1400)
    cash_pt  = _sf(20, 1400)
    nf = pygame.font.SysFont('DejaVu Sans', name_pt, bold=True)
    cf = pygame.font.SysFont('DejaVu Sans', cash_pt)

    # How many pixels the fixed rows consume
    FIXED_H  = 8 + nf.get_height() + 3 + cf.get_height() + 6  # pad_top + name + gap + cash + gap
    prop_area = card_h - FIXED_H - 8   # remaining pixels for property lines

    dot_r      = max(7, nf.get_height() // 2)
    text_x_off = dot_r * 2 + 14
    max_text_w = card_w - text_x_off - 8

    for i, player in enumerate(set_board.players):
        is_cur  = (player == current_player)
        cy      = start_y + i * (card_h + spacing)

        bg_col  = (45, 130, 65) if is_cur else (18, 72, 36)
        brd_col = (255, 210, 50) if is_cur else (55, 110, 65)

        _rr(set_board.screen, bg_col,  pygame.Rect(card_x, cy, card_w, card_h), r=10)
        pygame.draw.rect(set_board.screen, brd_col,
                         pygame.Rect(card_x, cy, card_w, card_h), 2, border_radius=10)

        # Colour dot aligned with name row
        dot_cy = cy + 8 + nf.get_height() // 2
        pygame.draw.circle(set_board.screen, PLAYER_COLORS[i % len(PLAYER_COLORS)],
                           (card_x + dot_r + 6, dot_cy), dot_r)

        text_x = card_x + text_x_off
        row_y  = cy + 8

        # Name
        label = player.name + (" <" if is_cur else "")
        ns = nf.render(label, True, (255, 255, 255))
        set_board.screen.blit(ns, (text_x, row_y))
        row_y += nf.get_height() + 3

        # Cash
        cs = cf.render(f"{player.cash:,} $", True, (170, 255, 170))
        set_board.screen.blit(cs, (text_x, row_y))
        row_y += cf.get_height() + 6

        # --- Properties or jail, scaled to fill remaining space ---
        if player.jail:
            js_pt = max(10, min(cash_pt, prop_area))
            jf    = pygame.font.SysFont('DejaVu Sans', js_pt)
            js    = jf.render("[IN PRIGIONE]", True, (255, 110, 80))
            set_board.screen.blit(js, (text_x, row_y))

        elif player.properties and prop_area > 10:
            n_props = len(player.properties)
            # Pick font size so all lines fit vertically
            line_h_budget = prop_area // n_props
            prop_pt = max(9, min(cash_pt - 2, line_h_budget - 2))
            pf2 = pygame.font.SysFont('DejaVu Sans', prop_pt)

            for prop_name in player.properties:
                line = "- " + prop_name
                # Truncate horizontally if needed
                while pf2.size(line + "...")[0] > max_text_w and len(line) > 2:
                    line = line[:-1]
                if line != "- " + prop_name:
                    line = line + "..."
                surf = pf2.render(line, True, (210, 240, 210))
                set_board.screen.blit(surf, (text_x, row_y))
                row_y += pf2.get_height() + 2


def display_stats(current_player):
    _draw_sidebar(current_player)


# ---------------------------------------------------------------------------
# Dice animation (ASCII faces, no Unicode)
# ---------------------------------------------------------------------------

_DICE = [
    # face 1-6 drawn as text
    ' 1 ', ' 2 ', ' 3 ', ' 4 ', ' 5 ', ' 6 ',
]

def _animate_dice(result):
    bx, by = set_board.board_x, set_board.board_y
    bs     = set_board.board_size
    size   = int(bs * 0.17)
    cx     = bx + bs // 2
    cy     = by + bs // 2
    font   = pygame.font.SysFont('DejaVu Sans', int(size * 0.55), bold=True)

    for frame in range(20):
        face_idx = random.randint(0, 5) if frame < 16 else (result - 1)
        r        = pygame.Rect(cx - size//2, cy - size//2, size, size)

        # Redraw board area (dice sits on top)
        clip = r.inflate(10, 10)
        set_board.screen.blit(set_board.board_img,
                              (bx, by), area=pygame.Rect(
                                  clip.x - bx, clip.y - by,
                                  clip.width, clip.height).clip(
                                  pygame.Rect(0, 0, bs, bs)))

        _rr(set_board.screen, (252, 248, 232), r, r=12)
        pygame.draw.rect(set_board.screen, (30,30,30), r, 3, border_radius=12)
        face = font.render(str(face_idx + 1), True, (20, 20, 20))
        set_board.screen.blit(face, face.get_rect(center=r.center))
        pygame.display.update(r.inflate(10, 10))
        pygame.time.wait(45 if frame < 16 else 110)


# ---------------------------------------------------------------------------
# Move player
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Card effect definitions
# Each imprevisto/probabilita card has a matching effect entry.
# Effects are dicts with keys:
#   move     : int  – relative steps (+forward, -back)
#   goto     : int  – go directly to this board position
#   jail     : bool – send to jail (position 29, skip turn)
#   skip     : bool – skip next turn
#   cash_pct : float – lose this fraction of cash (e.g. 0.10)
#   cash_abs : int  – lose/gain this fixed amount (negative = lose)
#   candy_per_prop: int – lose N "candies" (= €) per property owned
# ---------------------------------------------------------------------------

IMPREVISTO_EFFECTS = [
    {"skip": True},                   # 0 – Senegal, salta un turno
    {"move": -2},                     # 1 – Vulcano, indietro 2
    {"move": -1},                     # 2 – Libia, indietro 1
    {"jail": True},                   # 3 – Locuste, prigione 1 turno
    {"skip": True},                   # 4 – Inondazione, bloccato 1 turno
    {"cash_pct": -0.10},              # 5 – Goldman, perde 10%
    {"skip": True},                   # 6 – Virus, salta un turno
    {"move": -3},                     # 7 – Golpe, indietro 3
    {"jail": True},                   # 8 – Calais, prigione 2 turni (jail flag basta)
    {"skip": True},                   # 9 – Traffico, fermo 1 turno
    {"cash_pct": -0.10},              # 10 – TARI, dai 10% alla cassa
    {"candy_per_prop": -1},           # 11 – Energia, 1 caramella/proprietà
    {"jail": True},                   # 12 – Divorzio, prigione 1 turno
    {"cash_abs": -10},                # 13 – Gas, paga 10 caramelle
    {"cash_abs": -10},                # 14 – Grano, paga 10 caramelle
]

PROBABILITA_EFFECTS = [
    {},                               # 0 – sfida narrativa, nessun effetto meccanico
    {"move": 2},                      # 1 – Pioggia PM10, avanza 2
    {"move": 2},                      # 2 – Protezione internazionale, avanza 2
    {},                               # 3 – Gates WC, sfida narrativa
    {},                               # 4 – Banca, sfida narrativa
    {},                               # 5 – Borsa, sfida matematica
    {"move": 3},                      # 6 – Borsa di studio, avanza 3
    {},                               # 7 – Colloquio inglese, sfida narrativa
    {},                               # 8 – Atletica, sfida fisica
    {},                               # 9 – Avvocato, sfida narrativa
]


def _apply_card_effect(player, effect):
    """Apply a card effect dict to the player. Returns a summary string."""
    if not effect:
        return ""

    msgs = []

    if effect.get("jail"):
        player.jail = True
        msgs.append("Vai in prigione! Salti il prossimo turno.")

    if effect.get("skip") and not effect.get("jail"):
        player.jail = True          # reuse jail flag as "skip next turn"
        msgs.append("Salti il prossimo turno.")

    if effect.get("move"):
        steps = effect["move"]
        old = player.position
        player.position = (player.position + steps) % len(set_board.board_positions)
        # Check passing GO (only on positive moves)
        if steps > 0 and player.position < old:
            player.cash += 200
            msgs.append("+200$ per aver superato il Via!")
        direction = "Avanza" if steps > 0 else "Torna indietro"
        msgs.append(f"{direction} di {abs(steps)} caselle → {set_board.board_positions[player.position].name}.")

    if effect.get("goto") is not None:
        player.position = effect["goto"]
        msgs.append(f"Vai direttamente a {set_board.board_positions[player.position].name}.")

    if effect.get("cash_pct"):
        amount = int(player.cash * abs(effect["cash_pct"]))
        if effect["cash_pct"] < 0:
            player.cash -= amount
            msgs.append(f"Perdi il {int(abs(effect['cash_pct'])*100)}% del tuo denaro: -{amount}$.")
        else:
            player.cash += amount
            msgs.append(f"Guadagni il {int(effect['cash_pct']*100)}% in più: +{amount}$.")

    if effect.get("cash_abs"):
        amount = effect["cash_abs"]
        player.cash += amount
        if amount < 0:
            msgs.append(f"Perdi {abs(amount)}$.")
        else:
            msgs.append(f"Guadagni {amount}$.")

    if effect.get("candy_per_prop"):
        n     = len(player.properties)
        total = effect["candy_per_prop"] * n
        player.cash += total
        msgs.append(f"Perdi {abs(effect['candy_per_prop'])} caramella × {n} proprietà = {abs(total)}$.")

    return " ".join(msgs)


# ---------------------------------------------------------------------------
# Move player
# ---------------------------------------------------------------------------

def move_player(player):
    if player.jail:
        player.jail = False
        return

    dice = random.randint(1, 6)

    _base_redraw(player)
    pygame.display.update()
    _animate_dice(dice)

    old_pos = player.position
    player.position = (player.position + dice) % len(set_board.board_positions)
    if player.position < old_pos and dice > 0:   # passed GO
        player.cash += 200
        print(f"{player.name} ha superato il Via! +200$")

    _base_redraw(player)
    pygame.display.update()
    pygame.time.wait(250)

    cell = set_board.board_positions[player.position]

    match type(cell):
        case classi.Property:
            if cell.owner is None and cell.price > 0:
                if draw_buy_prompt(cell, player):
                    cell.buy(player)
                    player.properties.append(cell.name)
                    _base_redraw(player)
                    pygame.display.update()
            elif cell.owner is not None and cell.owner != player.name:
                for p in set_board.players:
                    if p.name == cell.owner:
                        p.cash += cell.rent
                player.cash -= cell.rent

        case classi.Imprevisto:
            idx  = random.randint(0, len(set_board.imprevisti) - 1)
            card = set_board.imprevisti[idx]
            effect_msg = _apply_card_effect(player, IMPREVISTO_EFFECTS[idx])
            body = card + (f"\n\n[ {effect_msg} ]" if effect_msg else "")
            draw_overlay_card("IMPREVISTO", body, accent=(200, 65, 40), icon_txt='?!')
            _base_redraw(player)
            pygame.display.update()

        case classi.Probabilita:
            idx  = random.randint(0, len(set_board.probabilita) - 1)
            card = set_board.probabilita[idx]
            effect_msg = _apply_card_effect(player, PROBABILITA_EFFECTS[idx])
            body = card + (f"\n\n[ {effect_msg} ]" if effect_msg else "")
            draw_overlay_card("PROBABILITA'", body, accent=(50, 110, 210), icon_txt='>>')
            _base_redraw(player)
            pygame.display.update()

        case classi.Tax:
            player.cash -= cell.amount
            draw_overlay_card("TASSA", f"Hai pagato {cell.amount}$ di tasse.",
                              accent=(160, 50, 50), icon_txt='$$')

        case classi.Jail:
            player.jail = True
            draw_overlay_card("PRIGIONE", "Sei finito in prigione! Salti il prossimo turno.",
                              accent=(70, 55, 190), icon_txt='[]')

        case _:
            pass
