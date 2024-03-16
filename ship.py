import pygame.image
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """Inicializar nave y establecer su posicion inicial"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Cargar la imagen de la nave
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Iniciar cada nave nueva abajo en el centro
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Guardar valor para la nave en el centro
        self.center = float(self.rect.centerx)

        # Estado del movimiento
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Actualizar movimiento de la nave"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        self.rect.centerx = self.center

    def blitme(self):
        """Dibujar la nave en su posicion actual"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Centrar nave en la pantalla"""
        self.center = self.screen_rect.centerx