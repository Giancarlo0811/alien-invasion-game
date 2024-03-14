class Settings():
    """Clase para guardar todas las configuraciones del juego"""

    def __init__(self):
        """Inicializar las configuraciones"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        self.ship_speed_factor = 1.5
        self.ship_limit = 3
        # Bala settings
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        # Alien settings
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        # fleet_direction de 1 representa derecha, -1 izquierda
        self.fleet_direction = 1