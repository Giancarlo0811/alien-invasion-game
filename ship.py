import pygame.image


class Ship():

    def __init__(self, screen):
        """Inicializar nave y establecer su posicion inicial"""
        self.screen = screen

        # Cargar la imagen de la nave
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Iniciar cada nave nueva abajo en el centro
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

    def blitme(self):
        """Dibujar la nave en su posicion actual"""
        self.screen.blit(self.image, self.rect)