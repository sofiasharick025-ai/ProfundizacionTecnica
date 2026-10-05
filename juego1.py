import pygame
import sys
import math
import random
from array import array

# ---------- Audio (se genera por código, sin archivos) ----------
try:
    pygame.mixer.pre_init(22050, -16, 1, 512)
except Exception:
    pass
pygame.init()
AUDIO_OK = True
try:
    pygame.mixer.init(22050, -16, 1, 512)
except Exception:
    AUDIO_OK = False

RATE = 22050


def _sonido(buf):
    if not AUDIO_OK:
        return None
    return pygame.mixer.Sound(buffer=buf.tobytes())


def tono(freq, dur, vol=0.4, tipo="square", decay=True, slide=0.0):
    n = int(RATE * dur)
    buf = array("h")
    fase = 0.0
    for i in range(n):
        f = freq + slide * (i / n)
        fase += f / RATE
        if tipo == "square":
            v = 1 if (fase % 1) < 0.5 else -1
        elif tipo == "saw":
            v = 2 * (fase % 1) - 1
        else:
            v = math.sin(2 * math.pi * fase)
        env = (1 - i / n) if decay else 1
        buf.append(int(v * vol * env * 32767))
    return buf


def ruido(dur, vol=0.6):
    n = int(RATE * dur)
    buf = array("h")
    for i in range(n):
        env = (1 - i / n) ** 2
        buf.append(int(random.uniform(-1, 1) * vol * env * 32767))
    return buf


def unir(*bufs):
    out = array("h")
    for b in bufs:
        out.extend(b)
    return out


SND_BOMBA = _sonido(tono(300, 0.08, 0.4, "square", slide=-120))
SND_EXPLO = _sonido(ruido(0.5, 0.7))
SND_MUERTE = _sonido(tono(500, 0.6, 0.4, "saw", slide=-420))
SND_PASO = _sonido(tono(120, 0.03, 0.15, "square"))
SND_VICTORIA = _sonido(unir(tono(523, 0.15), tono(659, 0.15), tono(784, 0.15), tono(1047, 0.35)))

# Música de fondo en bucle
_melodia = [262, 330, 392, 330, 294, 349, 440, 349, 262, 330, 392, 523, 392, 330, 294, 196]
_musica = unir(*[tono(f, 0.22, 0.25, "sine", decay=True) for f in _melodia])
MUSICA = _sonido(_musica)


def reproducir(s):
    if s:
        s.play()


# ===== LEYENDA DE LA MATRIZ =====
# 0 = vacío   1 = muro   2 = pilar indestructible
# 3 = bloque destructible   4 = piso libre   5 = inicio de jugador
NIVEL = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 2, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4, 3, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 2, 3, 2, 3, 2, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 4, 3, 3, 4, 4, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 4, 2, 3, 2, 4, 2, 3, 2, 3, 2, 3, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 3, 4, 3, 3, 4, 3, 3, 3, 3, 3, 4, 3, 3, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 3, 2, 3, 2, 3, 2, 4, 2, 4, 2, 3, 2, 3, 2, 3, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 4, 4, 3, 4, 3, 3, 4, 3, 3, 3, 4, 4, 3, 4, 3, 4, 3, 1, 0, 0, 0],
    [0, 0, 1, 4, 2, 3, 2, 3, 2, 4, 2, 4, 2, 3, 2, 4, 2, 3, 2, 4, 2, 4, 1, 0, 0],
    [0, 1, 5, 4, 4, 4, 4, 4, 3, 3, 4, 3, 3, 3, 3, 3, 4, 3, 3, 3, 4, 4, 5, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

TAM = 40
FILAS = len(NIVEL)
COLUMNAS = len(NIVEL[0])
ALTO_HUD = 40

COLOR_FONDO = (16, 24, 32)
COLORES = {
    1: (74, 74, 74),
    2: (43, 43, 43),
    3: (46, 158, 31),
    4: (244, 244, 244),
}
COLOR_BORDE = (40, 40, 40)

TIEMPO_BOMBA = 2.2      # segundos hasta explotar
DURACION_EXPLO = 0.5    # segundos que dura el fuego
ALCANCE = 2             # casillas de alcance
RETARDO_MOV = 0.14      # segundos entre pasos

pantalla = pygame.display.set_mode((COLUMNAS * TAM, FILAS * TAM + ALTO_HUD))
pygame.display.set_caption("Nivel 1 - Triángulo verde")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 22, bold=True)
fuente_grande = pygame.font.SysFont("arial", 44, bold=True)


class Jugador:
    def __init__(self, nombre, pos, color, teclas):
        self.nombre = nombre
        self.inicio = pos
        self.color = color
        self.teclas = teclas  # (arriba, abajo, izq, der, bomba)
        self.reset()

    def reset(self):
        self.fila, self.col = self.inicio
        self.vivo = True
        self.cooldown = 0.0
        self.max_bombas = 1


class Bomba:
    def __init__(self, fila, col, dueno):
        self.fila, self.col = fila, col
        self.dueno = dueno
        self.t = TIEMPO_BOMBA
        # el dueño puede salir de la casilla aunque la bomba sea sólida
        self.pasables = {dueno}


def cargar_nivel():
    grid = [f[:] for f in NIVEL]
    inicios = []
    for r in range(FILAS):
        for c in range(COLUMNAS):
            if grid[r][c] == 5:
                inicios.append((r, c))
                grid[r][c] = 4
    return grid, inicios


grid, inicios = cargar_nivel()
j1 = Jugador("Jugador 1", inicios[0], (255, 210, 0),
             (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_SPACE))
j2 = Jugador("Jugador 2", inicios[1], (60, 160, 255),
             (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN))
jugadores = [j1, j2]
bombas = []
fuegos = {}  # (fila, col) -> tiempo restante
ganador = None
fin = False


def reiniciar():
    global grid, bombas, fuegos, ganador, fin
    grid, _ = cargar_nivel()
    bombas = []
    fuegos = {}
    ganador = None
    fin = False
    for j in jugadores:
        j.reset()


def bomba_en(fila, col):
    for b in bombas:
        if b.fila == fila and b.col == col:
            return b
    return None


def libre(fila, col, jugador):
    if not (0 <= fila < FILAS and 0 <= col < COLUMNAS):
        return False
    if grid[fila][col] != 4:
        return False
    b = bomba_en(fila, col)
    if b and jugador not in b.pasables:
        return False
    return True


def mover(j, df, dc):
    nf, nc = j.fila + df, j.col + dc
    if libre(nf, nc, j):
        j.fila, j.col = nf, nc
        reproducir(SND_PASO)


def poner_bomba(j):
    activas = sum(1 for b in bombas if b.dueno is j)
    if activas >= j.max_bombas or bomba_en(j.fila, j.col):
        return
    bombas.append(Bomba(j.fila, j.col, j))
    reproducir(SND_BOMBA)


def explotar(b):
    if b in bombas:
        bombas.remove(b)
    reproducir(SND_EXPLO)
    fuegos[(b.fila, b.col)] = DURACION_EXPLO
    for df, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        for paso in range(1, ALCANCE + 1):
            f, c = b.fila + df * paso, b.col + dc * paso
            if not (0 <= f < FILAS and 0 <= c < COLUMNAS):
                break
            v = grid[f][c]
            if v in (0, 1, 2):
                break
            if v == 3:
                grid[f][c] = 4  # bloque destruido
                fuegos[(f, c)] = DURACION_EXPLO
                break
            fuegos[(f, c)] = DURACION_EXPLO
            otra = bomba_en(f, c)
            if otra:
                otra.t = 0  # reacción en cadena


def actualizar(dt):
    global ganador, fin
    # bombas
    for b in bombas[:]:
        b.t -= dt
        # el dueño pierde el permiso al salir de la casilla
        for j in list(b.pasables):
            if (j.fila, j.col) != (b.fila, b.col):
                b.pasables.discard(j)
        if b.t <= 0 and b in bombas:
            explotar(b)
    # fuego
    for k in list(fuegos):
        fuegos[k] -= dt
        if fuegos[k] <= 0:
            del fuegos[k]
    # muertes
    for j in jugadores:
        if j.vivo and (j.fila, j.col) in fuegos:
            j.vivo = False
            reproducir(SND_MUERTE)
    vivos = [j for j in jugadores if j.vivo]
    if not fin and len(vivos) <= 1:
        fin = True
        ganador = vivos[0] if vivos else None
        if ganador:
            reproducir(SND_VICTORIA)


def dibujar():
    pantalla.fill(COLOR_FONDO)
    off = ALTO_HUD
    for f in range(FILAS):
        for c in range(COLUMNAS):
            v = grid[f][c]
            if v == 0:
                continue
            x, y = c * TAM, f * TAM + off
            pygame.draw.rect(pantalla, COLORES[v], (x, y, TAM, TAM))
            pygame.draw.rect(pantalla, COLOR_BORDE, (x, y, TAM, TAM), 1)
            if v == 3:
                pygame.draw.rect(pantalla, (30, 120, 20), (x + 6, y + 6, TAM - 12, TAM - 12), 2)

    for (f, c) in fuegos:
        x, y = c * TAM, f * TAM + off
        pygame.draw.rect(pantalla, (255, 120, 0), (x + 2, y + 2, TAM - 4, TAM - 4))
        pygame.draw.rect(pantalla, (255, 230, 80), (x + 10, y + 10, TAM - 20, TAM - 20))

    for b in bombas:
        x, y = b.col * TAM + TAM // 2, b.fila * TAM + off + TAM // 2
        pulso = 3 * math.sin(pygame.time.get_ticks() / 100)
        pygame.draw.circle(pantalla, (20, 20, 20), (x, y), int(TAM // 2 - 7 + pulso))
        pygame.draw.circle(pantalla, (255, 60, 60), (x + 5, y - 8), 3)

    for j in jugadores:
        if not j.vivo:
            continue
        x, y = j.col * TAM + TAM // 2, j.fila * TAM + off + TAM // 2
        pygame.draw.circle(pantalla, j.color, (x, y), TAM // 2 - 7)
        pygame.draw.circle(pantalla, (0, 0, 0), (x, y), TAM // 2 - 7, 2)
        pygame.draw.circle(pantalla, (0, 0, 0), (x - 5, y - 3), 2)
        pygame.draw.circle(pantalla, (0, 0, 0), (x + 5, y - 3), 2)

    # HUD
    t1 = fuente.render("J1: WASD + ESPACIO  " + ("VIVO" if j1.vivo else "MUERTO"), True, j1.color)
    t2 = fuente.render("J2: FLECHAS + ENTER  " + ("VIVO" if j2.vivo else "MUERTO"), True, j2.color)
    pantalla.blit(t1, (10, 8))
    pantalla.blit(t2, (pantalla.get_width() - t2.get_width() - 10, 8))

    if fin:
        velo = pygame.Surface(pantalla.get_size(), pygame.SRCALPHA)
        velo.fill((0, 0, 0, 150))
        pantalla.blit(velo, (0, 0))
        msg = f"¡Gana {ganador.nombre}!" if ganador else "¡Empate!"
        m = fuente_grande.render(msg, True, (255, 255, 255))
        s = fuente.render("Presiona R para reiniciar", True, (220, 220, 220))
        cx = pantalla.get_width() // 2
        cy = pantalla.get_height() // 2
        pantalla.blit(m, (cx - m.get_width() // 2, cy - 40))
        pantalla.blit(s, (cx - s.get_width() // 2, cy + 20))


def main():
    if MUSICA:
        MUSICA.set_volume(0.25)
        MUSICA.play(loops=-1)
    while True:
        dt = reloj.tick(60) / 1000
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    reiniciar()
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if not fin:
                    for j in jugadores:
                        if j.vivo and e.key == j.teclas[4]:
                            poner_bomba(j)

        if not fin:
            teclas = pygame.key.get_pressed()
            for j in jugadores:
                if not j.vivo:
                    continue
                j.cooldown -= dt
                if j.cooldown <= 0:
                    arr, aba, izq, der, _ = j.teclas
                    if teclas[arr]:
                        mover(j, -1, 0)
                    elif teclas[aba]:
                        mover(j, 1, 0)
                    elif teclas[izq]:
                        mover(j, 0, -1)
                    elif teclas[der]:
                        mover(j, 0, 1)
                    else:
                        continue
                    j.cooldown = RETARDO_MOV

        actualizar(dt)
        dibujar()
        pygame.display.flip()


if __name__ == "__main__":
    main()