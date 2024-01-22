import pygame

class Ship:
    """Classe para cuidar da espaçonave"""

    def __init__(self, ci_game):
        """Inicializa a espaçonave e define sua posição inicial"""

        self.screen = ci_game.screen
        self.settings = ci_game.settings
        self.screen_rect = ci_game.screen.get_rect()

        # Sobe a imagem da espaçonave e obtém seu rect
        #Pygame permite tratar cada elemento como retângulos (rects)
        self.image = pygame.image.load('images/ship_a.bmp')
        self.rect = self.image.get_rect()

        # Começa cada espaçonave nova no centro inferior da tela
        self.rect.midbottom = self.screen_rect.midbottom

        # Armazena um float para a posição horizontal exata da espaçonave
        self.x = float(self.rect.x)

        # Flags de movimentos; inicia definido como parado por padrão
        self.moving_right = False
        self.moving_left = False
    

    def update(self):
        """Atualiza a posição com base nas flags de movimento"""

        if self.moving_right and (self.rect.right < self.screen_rect.right):
            self.x += self.settings.ship_speed
        if self.moving_left and (self.rect.left > 0):
            self.x -= self.settings.ship_speed
        
        # Atualiza o objeto rect de self.x
        self.rect.x = self.x


    def blitme(self):
        """Desenha a espaçonave em sua localização atual"""
        
        self.screen.blit(self.image, self.rect)
