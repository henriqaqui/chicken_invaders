class Settings:
    """Classe para armazenar as configurações do Jogo Checken Invasion"""
    
    def __init__(self):
        """Inicializa as configurações do jogo"""
        
        # Configurações da tela
        self.screen_width = 1024
        self.screen_height = 576
        self.bg_color = (8, 18, 33)

        # Configurações da aeronave
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Configurações do projétil
        self.bullet_speed = 2.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (230, 108, 58)
        self.bullets_allowed = 3

        # Configurações da galinha
        self.chicken_speed = 1.0
        self.fleet_drop_speed = 50
        # fleet_direction de 1 representa a direita; -1, esquerda
        self.fleet_direction = 1