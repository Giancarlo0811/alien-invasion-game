class GameStats():
    """Manejar estadisticas del juego"""

    def __init__(self, ai_settings):
        """Inicializar estadisticas"""
        self.ai_settings = ai_settings
        self.reset_stats()

        # Iniciar juego en estado inactivo
        self.game_active = False

        # Puntaje mas alto no debe reiniciarse
        self.high_score = 0

    def reset_stats(self):
        """Inicializar estadisticas que cambian durante el juego"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
