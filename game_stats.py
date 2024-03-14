class GameStats():
    """Manejar estadisticas del juego"""

    def __init__(self, ai_settings):
        """Inicializar estadisticas"""
        self.ai_settings = ai_settings
        self.reset_stats()

        # Iniciar juego en estado activo
        self.game_active = True

    def reset_stats(self):
        """Inicializar estadisticas que cambian durante el juego"""
        self.ships_left = self.ai_settings.ship_limit
