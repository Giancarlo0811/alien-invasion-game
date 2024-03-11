import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Clase para las balas disparadas por la nave"""
    def __init__(self, ai_settings, screen, ship):
        """Crear objeto bala en la posicion actual de la nave"""
        super().__init__()
        self.screen = screen

        # Crear bala rect en (0,0) y establecer posicion correcta
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Guardar la posicion de la bala
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Mover la bala hacia arriba"""
        # Actualizar la posicion decimal de la bala
        self.y -= self.speed_factor
        # Actualizar la posicion del rect
        self.rect.y = self.y

    def draw_bullet(self):
        """Dibujar la bala en la pantalla"""
        pygame.draw.rect(self.screen, self.color, self.rect)
