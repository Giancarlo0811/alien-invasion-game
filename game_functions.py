import sys
import pygame

def check_events():
    # eventos del teclado y mouse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


def update_screen(ai_settings, screen, ship):
    """Actualizar imagenes en la pantalla y cambiar a nueva pantalla"""
    # Redibujar la pantalla
    screen.fill(ai_settings.bg_color)
    ship.blitme()

    # Hacer que la pantalla dibujada mas reciente sea visible
    pygame.display.flip()