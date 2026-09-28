import pygame
import sys

pygame.init()

# ===== LEYENDA DE LA MATRIZ =====
# 0 = vacío (fuera del triángulo)   1 = muro
# 2 = pilar indestructible          3 = bloque destructible
# 4 = piso libre                    5 = inicio de jugador
NIVEL = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 5, 4, 4, 3, 4, 4, 3, 3, 4, 4, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 5, 1, 0],
    [0, 0, 1, 4, 2, 3, 2, 3, 2, 3, 2, 4, 2, 4, 2, 4, 2, 3, 2, 3, 2, 4, 1, 0, 0],
    [0, 0, 0, 1, 3, 3, 3, 4, 3, 3, 4, 3, 4, 3, 3, 3, 3, 3, 3, 4, 3, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 4, 2, 3, 2, 4, 2, 4, 2, 4, 2, 4, 2, 3, 2, 4, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 3, 3, 4, 3, 4, 4, 3, 3, 3, 3, 4, 3, 3, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 3, 2, 4, 2, 4, 2, 3, 2, 3, 2, 3, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 4, 3, 3, 3, 4, 3, 3, 3, 4, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 2, 3, 2, 3, 2, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 4, 4, 3, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4, 2, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

TAM = 40  # tamaño de cada celda en píxeles

# Colores (R, G, B)
COLOR_FONDO = (26, 16, 48)
COLORES = {
    1: (91, 61, 143),   # muro
    2: (58, 38, 96),   # pilar
    3: (243, 156, 18),   # bloque destructible
    4: (253, 243, 224),  # piso
    5: (253, 243, 224),  # piso (con jugador encima)
}
COLOR_JUGADOR = (0, 229, 255)
COLOR_BORDE = (40, 40, 40)

pygame.init()
FILAS = len(NIVEL)
COLUMNAS = len(NIVEL[0])
pantalla = pygame.display.set_mode((COLUMNAS * TAM, FILAS * TAM))
pygame.display.set_caption("Nivel 2 - Triángulo invertido")


def dibujar_mapa():
    pantalla.fill(COLOR_FONDO)
    # Recorremos la matriz con dos for: filas y columnas
    for fila in range(FILAS):
        for col in range(COLUMNAS):
            valor = NIVEL[fila][col]
            if valor == 0:
                continue  # fuera del triángulo, no se dibuja
            x = col * TAM
            y = fila * TAM
            pygame.draw.rect(pantalla, COLORES[valor], (x, y, TAM, TAM))
            pygame.draw.rect(pantalla, COLOR_BORDE, (x, y, TAM, TAM), 1)
            if valor == 5:
                pygame.draw.circle(pantalla, COLOR_JUGADOR, (x + TAM // 2, y + TAM // 2), TAM // 2 - 8)


corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
    dibujar_mapa()
    pygame.display.flip()

pygame.quit()