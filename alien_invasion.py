import sys
import pygame
from pygame.sprite import Group

import game_functions
from settings import Settings
from ship import Ship
import game_functions as gf

def run_game():
    #  inicializar juego, configuraciones y crear screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")

    # Crear nave, grupo de balas y grupo de aliens
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # crear flota de aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Iniciar loop principal del juego
    while True:
        gf.check_events(ai_settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(bullets)
        gf.update_aliens(ai_settings, aliens)
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)



run_game()