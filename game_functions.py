import sys
import pygame
from time import sleep

from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Eventos al presionar teclado"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


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


def update_screen(ai_settings, screen, ship, aliens, bullets):
    """Actualizar imagenes en la pantalla y cambiar a nueva pantalla"""
    # Redibujar la pantalla
    screen.fill(ai_settings.bg_color)
    # Redibujar todas las balas detras de la nave y los aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Hacer que la pantalla dibujada mas reciente sea visible
    pygame.display.flip()


def update_bullets(ai_settings, screen, ship, bullets, aliens):
    """Actualizar posicion de las balas y borrar balas viejas"""
    # Actualizar posicion de las balas
    bullets.update()

    # Borrar balas que desaparecen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))

    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    """Responder a bala-alien colision"""
    # Eliminar bala y alien que colisionan
    colissions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        # Destruir balas existentes y crear nueva flota
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)

def get_number_aliens_x(ai_settings, alien_width):
    """Determinar numero de aliens que caben en una fila"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determinar el numero de filas de aliens"""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # Crear alien y ponerlo en la fila
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Crear flota de aliens"""
    # Crear alien y encontrar el numero de aliens en una fila
    # Espacio entre aliens = ancho de un alien
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                  alien.rect.height)

    # Crear flota de aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)


def check_fleet_edges(ai_settings, aliens):
    """Responder apropiadamente si los aliens llegan al borde"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Bajar la flota entera y cambiar direccion"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Verificar si un alien llega al final"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # La nave fue golpeada
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """Verificar si flota esta en el borde
        y actualizar posicion de todos los aliens"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # alien-nave colisiones
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    # Verificar aliens que llegaron al final
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """responder a una nave golpeada por un alien"""
    if stats.ships_left > 0:
        # Decrementar ships_left
        stats.ships_left -= 1

        # Vaciar lista de aliens y balas
        aliens.empty()
        bullets.empty()

        # Crear nueva flota de aliens y centrar nave
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pausa
        sleep(0.5)

    else:
        stats.game_active = False
