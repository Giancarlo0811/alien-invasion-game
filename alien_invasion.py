import sys
import pygame

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

    # Crear nave
    ship = Ship(ai_settings, screen)

    # Iniciar loop principal del juego
    while True:
        gf.check_events(ship)
        ship.update()

        gf.update_screen(ai_settings, screen, ship)


run_game()