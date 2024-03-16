class Settings():
    """Clase para guardar todas las configuraciones del juego"""

    def __init__(self):
        """Inicializar las configuraciones estaticas"""
        # Configuracion Pantalla
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        # Configuracion Nave
        self.ship_limit = 3

        # Configuracion Bala
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Configuracion Aliens
        self.fleet_drop_speed = 8

        # Velocidad juego
        self.speedup_scale = 1.1

        # Velocidad puntaje
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Inicializar configuraciones dinamicas"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # fleet_direction de 1 representa derecha; -1 representa izquierda
        self.fleet_direction = 1

        # puntaje
        self.alien_points = 50

    def increase_speed(self):
        """Aumentar configuraciones de velocidad"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
