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


def check_events(ai_settings, screen, ship, bullets, play_button, stats,
                 aliens, sb):
    # eventos del teclado y mouse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen,
                              stats, play_button, ship, aliens, bullets,
                              mouse_x, mouse_y, sb)


def check_play_button(ai_settings, screen, stats, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y, sb):
    """Iniciar juego nuevo cuando se presiona el boton"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # resetear velocidad del juego
        ai_settings.initialize_dynamic_settings()

        # esconder cursor
        pygame.mouse.set_visible(False)

        # resetear estadisticas
        stats.reset_stats()
        stats.game_active = True

        # resetear imagenes de puntajes
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Vaciar lista de aliens y balas
        aliens.empty()
        bullets.empty()

        # Crear nueva flota de aliens
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, ship, aliens, bullets, play_button,
                  stats, sb):
    """Actualizar imagenes en la pantalla y cambiar a nueva pantalla"""
    # Redibujar la pantalla
    screen.fill(ai_settings.bg_color)
    # Redibujar todas las balas detras de la nave y los aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Dibujar informacion de puntaje
    sb.show_score()

    # Dibujar boton si el juego esta inactivo
    if not stats.game_active:
        play_button.draw_button()

    # Hacer que la pantalla dibujada mas reciente sea visible
    pygame.display.flip()


def update_bullets(ai_settings, screen, ship, bullets, aliens,
                   stats, sb):
    """Actualizar posicion de las balas y borrar balas viejas"""
    # Actualizar posicion de las balas
    bullets.update()

    # Borrar balas que desaparecen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))

    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets,
                                  stats, sb)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets,
                                  stats, sb):
    """Responder a bala-alien colision"""
    # Eliminar bala y alien que colisionan
    colissions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if colissions:
        for aliens in colissions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_scores(stats, sb)

    if len(aliens) == 0:
        # Si la flota completa es destruida, iniciar nuevo nivel
        bullets.empty()
        ai_settings.increase_speed()

        # aumentar nivel
        stats.level += 1
        sb.prep_level()

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


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """Verificar si un alien llega al final"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # La nave fue golpeada
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
            break


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """Verificar si flota esta en el borde
        y actualizar posicion de todos los aliens"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # alien-nave colisiones
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)

    # Verificar aliens que llegaron al final
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """responder a una nave golpeada por un alien"""
    if stats.ships_left > 0:
        # Decrementar ships_left
        stats.ships_left -= 1

        # Actualizar puntaje
        sb.prep_ships()

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
        pygame.mouse.set_visible(True)


def check_high_scores(stats, sb):
    """Verificar si hay puntaje mas alto"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()