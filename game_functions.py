import sys
import pygame


def check_keydown_events(event, ship):
    """Eventos al presionar teclado"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True


def check_keyup_events(event, ship):
    """Eventos al soltar teclado"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ship):
    # eventos del teclado y mouse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def update_screen(ai_settings, screen, ship):
    """Actualizar imagenes en la pantalla y cambiar a nueva pantalla"""
    # Redibujar la pantalla
    screen.fill(ai_settings.bg_color)
    ship.blitme()

    # Hacer que la pantalla dibujada mas reciente sea visible
    pygame.display.flip()