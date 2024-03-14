import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Clase para representar un alien"""
    def __init__(self, ai_settings, screen):
        """Inicializar alien y establecer su posicion inicial"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Cargar la imagen y establecer su rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Iniciar cada alien nuevo en la esquina superior izquierda
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # Guardar la posicion exacta
        self.x = float(self.rect.x)

    def blitme(self):
        """Dibujar el alien en su posicion actual"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Devolver true si el alien esta en el borde"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True


    def update(self):
        """Mover alien a la derecha o izquierda"""
        self.x += (self.ai_settings.alien_speed_factor *
                    self.ai_settings.fleet_direction)
        self.rect.x = self.x