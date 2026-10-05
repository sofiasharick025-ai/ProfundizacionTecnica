import pygame
import sys
import math
import random
from array import array

# ============================================================
# INICIAR PYGAME
# ============================================================

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


# ============================================================
# SONIDOS
# ============================================================

def sonido(buf):
    if not AUDIO_OK:
        return None
    return pygame.mixer.Sound(buffer=buf.tobytes())


def tono(freq, dur, vol=0.4, tipo="square", decay=True, slide=0):
    n = int(RATE * dur)
    buf = array("h")
    fase = 0

    for i in range(n):
        fase += (freq + slide * (i / n)) / RATE

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
    salida = array("h")

    for b in bufs:
        salida.extend(b)

    return salida


def melodia(notas, dur=0.22, tipo="sine"):
    return sonido(
        unir(
            *[
                tono(f, dur, 0.25, tipo)
                for f in notas
            ]
        )
    )


SND_BOMBA = sonido(
    tono(300, 0.08, 0.4, "square", slide=-120)
)

SND_EXPLO = sonido(
    ruido(0.5, 0.7)
)

SND_MUERTE = sonido(
    tono(500, 0.6, 0.4, "saw", slide=-420)
)

SND_PASO = sonido(
    tono(120, 0.03, 0.15, "square")
)

SND_VICTORIA = sonido(
    unir(
        tono(523, 0.15),
        tono(659, 0.15),
        tono(784, 0.15),
        tono(1047, 0.35)
    )
)

MUSICA1 = melodia(
    [262, 330, 392, 330, 294, 349, 440, 349,
     262, 330, 392, 523, 392, 330, 294, 196]
)

MUSICA2 = melodia(
    [220, 262, 330, 262, 247, 294, 370, 294,
     220, 330, 440, 330, 392, 330, 262, 165],
    0.20,
    "square"
)

MUSICA3 = melodia(
    [196, 247, 294, 247, 220, 262, 330, 262,
     196, 294, 392, 294, 349, 294, 247, 147],
    0.21,
    "saw"
)


def reproducir(s):
    if s:
        s.play()


# ============================================================
# MAPA 1
# ============================================================

NIVEL1 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,1,3,2,3,1,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,4,3,3,3,3,1,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,3,2,3,2,3,2,3,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,3,3,4,3,3,4,4,3,3,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,4,2,3,2,4,2,3,2,3,2,3,1,0,0,0,0,0,0],
    [0,0,0,0,0,1,3,4,3,3,4,3,3,3,3,3,4,3,3,1,0,0,0,0,0],
    [0,0,0,0,1,3,2,3,2,3,2,4,2,4,2,3,2,3,2,3,1,0,0,0,0],
    [0,0,0,1,4,4,3,4,3,3,4,3,3,3,4,4,3,4,3,4,3,1,0,0,0],
    [0,0,1,4,2,3,2,3,2,4,2,4,2,3,2,4,2,3,2,4,2,4,1,0,0],
    [0,1,5,4,4,4,4,4,3,3,4,3,3,3,3,3,4,3,3,3,4,4,5,1,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]


# ============================================================
# MAPA 2
# ============================================================

NIVEL2 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [0,1,5,4,4,3,4,4,3,3,4,4,3,3,3,3,3,3,3,4,4,4,5,1,0],
    [0,0,1,4,2,3,2,3,2,3,2,4,2,4,2,4,2,3,2,3,2,4,1,0,0],
    [0,0,0,1,3,3,3,4,3,3,4,3,4,3,3,3,3,3,3,4,3,1,0,0,0],
    [0,0,0,0,1,4,2,3,2,4,2,4,2,4,2,4,2,3,2,4,1,0,0,0,0],
    [0,0,0,0,0,1,3,3,4,3,4,4,3,3,3,3,4,3,3,1,0,0,0,0,0],
    [0,0,0,0,0,0,1,3,2,4,2,4,2,3,2,3,2,3,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,4,3,3,3,4,3,3,3,4,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,3,2,3,2,3,2,3,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,3,4,4,3,4,1,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,1,4,2,4,1,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0]
]


# ============================================================
# MAPA 3
# ============================================================

NIVEL3 = [
    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,5,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,4,2,3,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,4,4,4,3,4,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,4,2,4,2,3,2,4,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,3,3,4,3,3,4,4,3,3,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,3,2,3,2,3,2,4,2,3,2,4,1,1,0,0,0,0,0,0,0,0,0,0,0],
    [1,4,3,4,3,3,4,3,3,4,4,3,3,3,1,1,0,0,0,0,0,0,0,0,0],
    [1,3,2,3,2,3,2,3,2,3,2,3,2,3,2,3,1,1,0,0,0,0,0,0,0],
    [1,4,4,4,3,3,3,3,3,3,3,3,3,4,3,3,3,3,1,1,0,0,0,0,0],
    [1,4,2,4,2,3,2,3,2,3,2,3,2,4,2,3,2,4,2,4,1,1,0,0,0],
    [1,5,4,4,3,3,3,4,4,3,3,3,3,3,3,4,3,3,4,4,4,5,1,1,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]


# ============================================================
# CONFIGURACIÓN DE LOS 3 NIVELES
# ============================================================

NIVELES = [

    {
        "titulo": "Nivel 1 - Triángulo verde",
        "matriz": NIVEL1,
        "fondo": (16,24,32),
        "colores": {
            1:(74,74,74),
            2:(43,43,43),
            3:(46,158,31),
            4:(244,244,244)
        },
        "jugadores": [
            (255,210,0),
            (60,160,255)
        ],
        "musica": MUSICA1
    },

    {
        "titulo": "Nivel 2 - Triángulo invertido",
        "matriz": NIVEL2,
        "fondo": (26,16,48),
        "colores": {
            1:(91,61,143),
            2:(58,38,96),
            3:(243,156,18),
            4:(253,243,224)
        },
        "jugadores": [
            (0,229,255),
            (255,80,160)
        ],
        "musica": MUSICA2
    },

    {
        "titulo": "Nivel 3 - Triángulo rectángulo",
        "matriz": NIVEL3,
        "fondo": (11,42,46),
        "colores": {
            1:(140,28,28),
            2:(94,16,16),
            3:(31,181,181),
            4:(232,247,247)
        },
        "jugadores": [
            (255,230,0),
            (200,80,255)
        ],
        "musica": MUSICA3
    }
]


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

TAM = 40
ALTO_HUD = 45

TIEMPO_BOMBA = 2.2
DURACION_EXPLO = 0.5
ALCANCE = 2
RETARDO_MOV = 0.14

NIVEL_ACTUAL = 0

FILAS = len(NIVELES[0]["matriz"])
COLUMNAS = len(NIVELES[0]["matriz"][0])

pantalla = pygame.display.set_mode(
    (COLUMNAS * TAM, FILAS * TAM + ALTO_HUD)
)

reloj = pygame.time.Clock()

fuente = pygame.font.SysFont(
    "arial",
    20,
    bold=True
)

fuente_grande = pygame.font.SysFont(
    "arial",
    44,
    bold=True
)


# ============================================================
# JUGADOR
# ============================================================

class Jugador:

    def __init__(self, nombre, teclas):

        self.nombre = nombre
        self.teclas = teclas

        self.fila = 0
        self.col = 0

        self.color = (255,255,255)

        self.vivo = True
        self.cooldown = 0


    def reset(self, posicion, color):

        self.fila = posicion[0]
        self.col = posicion[1]

        self.color = color

        self.vivo = True
        self.cooldown = 0


# ============================================================
# BOMBA
# ============================================================

class Bomba:

    def __init__(self, fila, col, dueno):

        self.fila = fila
        self.col = col

        self.dueno = dueno

        self.t = TIEMPO_BOMBA

        self.pasables = {dueno}


# ============================================================
# JUGADORES
# ============================================================

j1 = Jugador(
    "Jugador 1",
    (
        pygame.K_w,
        pygame.K_s,
        pygame.K_a,
        pygame.K_d,
        pygame.K_SPACE
    )
)

j2 = Jugador(
    "Jugador 2",
    (
        pygame.K_UP,
        pygame.K_DOWN,
        pygame.K_LEFT,
        pygame.K_RIGHT,
        pygame.K_RETURN
    )
)

jugadores = [j1, j2]


# ============================================================
# VARIABLES DEL JUEGO
# ============================================================

grid = []

bombas = []

fuegos = {}

ganador = None

fin = False

cambio_nivel = False

tiempo_cambio = 0


# ============================================================
# CARGAR NIVEL
# ============================================================

def cargar_nivel(numero):

    global NIVEL_ACTUAL
    global grid
    global bombas
    global fuegos
    global ganador
    global fin
    global cambio_nivel
    global tiempo_cambio

    NIVEL_ACTUAL = numero

    cfg = NIVELES[NIVEL_ACTUAL]

    grid = [
        fila[:]
        for fila in cfg["matriz"]
    ]

    inicios = []

    for f in range(len(grid)):

        for c in range(len(grid[f])):

            if grid[f][c] == 5:

                inicios.append((f,c))

                grid[f][c] = 4


    # Por seguridad: exactamente dos jugadores
    if len(inicios) >= 2:

        inicio1 = inicios[0]
        inicio2 = inicios[-1]

    else:

        inicio1 = (1,1)
        inicio2 = (1,COLUMNAS-2)


    j1.reset(
        inicio1,
        cfg["jugadores"][0]
    )

    j2.reset(
        inicio2,
        cfg["jugadores"][1]
    )


    bombas = []

    fuegos = {}

    ganador = None

    fin = False

    cambio_nivel = False

    tiempo_cambio = 0


    pygame.display.set_caption(
        cfg["titulo"]
    )


    # Música
    if AUDIO_OK:

        pygame.mixer.stop()

        if cfg["musica"]:

            cfg["musica"].set_volume(0.25)

            cfg["musica"].play(
                loops=-1
            )


# ============================================================
# BUSCAR BOMBA
# ============================================================

def bomba_en(fila, col):

    for b in bombas:

        if b.fila == fila and b.col == col:

            return b

    return None


# ============================================================
# COMPROBAR CASILLA LIBRE
# ============================================================

def libre(fila, col, jugador):

    if not (
        0 <= fila < len(grid)
        and
        0 <= col < len(grid[0])
    ):
        return False


    if grid[fila][col] != 4:

        return False


    b = bomba_en(fila,col)


    if b and jugador not in b.pasables:

        return False


    return True


# ============================================================
# MOVER
# ============================================================

def mover(jugador, df, dc):

    nf = jugador.fila + df
    nc = jugador.col + dc


    if libre(nf,nc,jugador):

        jugador.fila = nf
        jugador.col = nc

        reproducir(SND_PASO)


# ============================================================
# PONER BOMBA
# ============================================================

def poner_bomba(jugador):

    if any(
        b.dueno is jugador
        for b in bombas
    ):

        return


    if bomba_en(
        jugador.fila,
        jugador.col
    ):

        return


    bombas.append(
        Bomba(
            jugador.fila,
            jugador.col,
            jugador
        )
    )

    reproducir(SND_BOMBA)


# ============================================================
# EXPLOSIÓN
# ============================================================

def explotar(bomba):

    if bomba in bombas:

        bombas.remove(bomba)


    reproducir(SND_EXPLO)


    fuegos[
        (bomba.fila,bomba.col)
    ] = DURACION_EXPLO


    direcciones = [
        (1,0),
        (-1,0),
        (0,1),
        (0,-1)
    ]


    for df,dc in direcciones:

        for paso in range(
            1,
            ALCANCE + 1
        ):

            f = bomba.fila + df * paso
            c = bomba.col + dc * paso


            if not (
                0 <= f < len(grid)
                and
                0 <= c < len(grid[0])
            ):

                break


            valor = grid[f][c]


            # Muro
            if valor in (0,1,2):

                break


            # Bloque destruible
            if valor == 3:

                grid[f][c] = 4

                fuegos[
                    (f,c)
                ] = DURACION_EXPLO

                break


            # Piso
            fuegos[
                (f,c)
            ] = DURACION_EXPLO


            otra = bomba_en(f,c)


            if otra:

                otra.t = 0


# ============================================================
# ACTUALIZAR JUEGO
# ============================================================

def actualizar(dt):

    global ganador
    global fin
    global cambio_nivel
    global tiempo_cambio


    # -------------------------
    # BOMBAS
    # -------------------------

    for b in bombas[:]:

        b.t -= dt


        for jugador in list(
            b.pasables
        ):

            if (
                jugador.fila,
                jugador.col
            ) != (
                b.fila,
                b.col
            ):

                b.pasables.discard(
                    jugador
                )


        if (
            b.t <= 0
            and
            b in bombas
        ):

            explotar(b)


    # -------------------------
    # FUEGO
    # -------------------------

    for posicion in list(fuegos):

        fuegos[posicion] -= dt


        if fuegos[posicion] <= 0:

            del fuegos[posicion]


    # -------------------------
    # MUERTES
    # -------------------------

    for jugador in jugadores:

        if (
            jugador.vivo
            and
            (jugador.fila,jugador.col)
            in fuegos
        ):

            jugador.vivo = False

            reproducir(SND_MUERTE)


    # -------------------------
    # COMPROBAR GANADOR
    # -------------------------

    vivos = [
        jugador
        for jugador in jugadores
        if jugador.vivo
    ]


    if not fin and len(vivos) <= 1:

        fin = True

        ganador = (
            vivos[0]
            if vivos
            else None
        )


        if ganador:

            reproducir(SND_VICTORIA)


        # Esperar antes de pasar al siguiente
        cambio_nivel = True
        tiempo_cambio = 0


    # -------------------------
    # PASAR AL SIGUIENTE NIVEL
    # -------------------------

    if cambio_nivel:

        tiempo_cambio += dt


        if tiempo_cambio >= 2.5:

            if NIVEL_ACTUAL < len(NIVELES) - 1:

                cargar_nivel(
                    NIVEL_ACTUAL + 1
                )

            else:

                # Terminó el nivel 3
                fin = True
                cambio_nivel = False


# ============================================================
# DIBUJAR
# ============================================================

def dibujar():

    cfg = NIVELES[NIVEL_ACTUAL]


    pantalla.fill(
        cfg["fondo"]
    )


    offset = ALTO_HUD


    # -------------------------
    # MAPA
    # -------------------------

    for f in range(len(grid)):

        for c in range(len(grid[f])):

            valor = grid[f][c]


            if valor == 0:

                continue


            x = c * TAM
            y = f * TAM + offset


            pygame.draw.rect(
                pantalla,
                cfg["colores"][valor],
                (
                    x,
                    y,
                    TAM,
                    TAM
                )
            )


            pygame.draw.rect(
                pantalla,
                (40,40,40),
                (
                    x,
                    y,
                    TAM,
                    TAM
                ),
                1
            )


            if valor == 3:

                pygame.draw.rect(
                    pantalla,
                    (0,0,0),
                    (
                        x + 6,
                        y + 6,
                        TAM - 12,
                        TAM - 12
                    ),
                    2
                )


    # -------------------------
    # FUEGO
    # -------------------------

    for f,c in fuegos:

        x = c * TAM
        y = f * TAM + offset


        pygame.draw.rect(
            pantalla,
            (255,120,0),
            (
                x + 2,
                y + 2,
                TAM - 4,
                TAM - 4
            )
        )


        pygame.draw.rect(
            pantalla,
            (255,230,80),
            (
                x + 10,
                y + 10,
                TAM - 20,
                TAM - 20
            )
        )


    # -------------------------
    # BOMBAS
    # -------------------------

    for b in bombas:

        x = (
            b.col * TAM
            + TAM // 2
        )

        y = (
            b.fila * TAM
            + offset
            + TAM // 2
        )


        pulso = (
            3 *
            math.sin(
                pygame.time.get_ticks()
                / 100
            )
        )


        pygame.draw.circle(
            pantalla,
            (20,20,20),
            (x,y),
            int(TAM // 2 - 7 + pulso)
        )


        pygame.draw.circle(
            pantalla,
            (255,60,60),
            (x + 5,y - 8),
            3
        )


    # -------------------------
    # JUGADORES
    # -------------------------

    for jugador in jugadores:

        if not jugador.vivo:

            continue


        x = (
            jugador.col * TAM
            + TAM // 2
        )

        y = (
            jugador.fila * TAM
            + offset
            + TAM // 2
        )


        pygame.draw.circle(
            pantalla,
            jugador.color,
            (x,y),
            TAM // 2 - 7
        )


        pygame.draw.circle(
            pantalla,
            (0,0,0),
            (x,y),
            TAM // 2 - 7,
            2
        )


        pygame.draw.circle(
            pantalla,
            (0,0,0),
            (x - 5,y - 3),
            2
        )


        pygame.draw.circle(
            pantalla,
            (0,0,0),
            (x + 5,y - 3),
            2
        )


    # -------------------------
    # HUD
    # -------------------------

    texto1 = fuente.render(
        "J1: WASD + ESPACIO "
        + (
            "VIVO"
            if j1.vivo
            else "MUERTO"
        ),
        True,
        j1.color
    )


    texto2 = fuente.render(
        "J2: FLECHAS + ENTER "
        + (
            "VIVO"
            if j2.vivo
            else "MUERTO"
        ),
        True,
        j2.color
    )


    texto_nivel = fuente.render(
        f"NIVEL {NIVEL_ACTUAL + 1} / 3",
        True,
        (255,255,255)
    )


    pantalla.blit(
        texto1,
        (10,10)
    )


    pantalla.blit(
        texto_nivel,
        (
            pantalla.get_width()
            // 2
            - texto_nivel.get_width()
            // 2,
            10
        )
    )


    pantalla.blit(
        texto2,
        (
            pantalla.get_width()
            - texto2.get_width()
            - 10,
            10
        )
    )


    # -------------------------
    # PANTALLA FINAL DEL NIVEL
    # -------------------------

    if fin:

        velo = pygame.Surface(
            pantalla.get_size(),
            pygame.SRCALPHA
        )

        velo.fill(
            (0,0,0,170)
        )

        pantalla.blit(
            velo,
            (0,0)
        )


        if NIVEL_ACTUAL < 2:

            if ganador:

                mensaje = (
                    f"¡{ganador.nombre} ganó!"
                )

            else:

                mensaje = "¡Empate!"


            mensaje2 = (
                "Preparando siguiente nivel..."
            )


        else:

            mensaje = "¡GANASTE LOS 3 NIVELES!"

            mensaje2 = (
                "Presiona R para volver a jugar"
            )


        texto = fuente_grande.render(
            mensaje,
            True,
            (255,255,255)
        )


        texto2_final = fuente.render(
            mensaje2,
            True,
            (220,220,220)
        )


        cx = pantalla.get_width() // 2
        cy = pantalla.get_height() // 2


        pantalla.blit(
            texto,
            (
                cx - texto.get_width() // 2,
                cy - 45
            )
        )


        pantalla.blit(
            texto2_final,
            (
                cx - texto2_final.get_width() // 2,
                cy + 20
            )
        )


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    cargar_nivel(0)


    while True:

        dt = reloj.tick(60) / 1000


        # -------------------------
        # EVENTOS
        # -------------------------

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()


            if evento.type == pygame.KEYDOWN:

                # ESC = salir
                if evento.key == pygame.K_ESCAPE:

                    pygame.quit()
                    sys.exit()


                # R = reiniciar
                if evento.key == pygame.K_r:

                    cargar_nivel(
                        NIVEL_ACTUAL
                    )

                    continue


                # Bombas
                if not fin:

                    for jugador in jugadores:

                        if (
                            jugador.vivo
                            and
                            evento.key
                            == jugador.teclas[4]
                        ):

                            poner_bomba(
                                jugador
                            )


        # -------------------------
        # MOVIMIENTO
        # -------------------------

        if not fin:

            teclas = pygame.key.get_pressed()


            for jugador in jugadores:

                if not jugador.vivo:

                    continue


                jugador.cooldown -= dt


                if jugador.cooldown <= 0:

                    arriba = jugador.teclas[0]
                    abajo = jugador.teclas[1]
                    izquierda = jugador.teclas[2]
                    derecha = jugador.teclas[3]


                    if teclas[arriba]:

                        mover(
                            jugador,
                            -1,
                            0
                        )


                    elif teclas[abajo]:

                        mover(
                            jugador,
                            1,
                            0
                        )


                    elif teclas[izquierda]:

                        mover(
                            jugador,
                            0,
                            -1
                        )


                    elif teclas[derecha]:

                        mover(
                            jugador,
                            0,
                            1
                        )


                    else:

                        continue


                    jugador.cooldown = RETARDO_MOV


        # -------------------------
        # ACTUALIZAR
        # -------------------------

        actualizar(dt)


        # -------------------------
        # DIBUJAR
        # -------------------------

        dibujar()


        pygame.display.flip()


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":

    main()