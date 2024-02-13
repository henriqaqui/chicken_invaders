class GameStats:
    """Rastreia as estatísticas de Chicken Invasion"""

    def __init__(self, ci_game):
        """Inicializa as estatísticas"""
        self.settings = ci_game.settings
        self. reset_stats()

    
    def reset_stats(self):
        """Inicializa as estatísticas que podem mudar durante o jogo"""
        self.ships_left = self.settings.ship_limit
        