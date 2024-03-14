import sys
import pygame
from pygame.sprite import Group

import game_functions
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats

def run_game():
    #  inicializar juego, configuraciones y crear screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")

    # Crear instancia para guardar estadisticas
    stats = GameStats(ai_settings)

    # Crear nave, grupo de balas y grupo de aliens
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # crear flota de aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Iniciar loop principal del juego
    while True:
        gf.check_events(ai_settings, screen, ship, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, bullets, aliens)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, ship, aliens, bullets)



run_game()