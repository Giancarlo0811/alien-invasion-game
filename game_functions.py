import sys
import pygame

from bullet import Bullet

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Eventos al presionar teclado"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)


def fire_bullet(ai_settings, screen, ship, bullets):
    # Crear nueva bala y agregarla al grupo
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):
    """Eventos al soltar teclado"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, ship, bullets):
    # eventos del teclado y mouse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def update_screen(ai_settings, screen, ship, bullets):
    """Actualizar imagenes en la pantalla y cambiar a nueva pantalla"""
    # Redibujar la pantalla
    screen.fill(ai_settings.bg_color)
    # Redibujar todas las balas detras de la nave y los aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()

    # Hacer que la pantalla dibujada mas reciente sea visible
    pygame.display.flip()


def update_bullets(bullets):
    """Actualizar posicion de las balas y borrar balas viejas"""
    # Actualizar posicion de las balas
    bullets.update()

    # Borrar balas que desaparecen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))