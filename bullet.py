import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Gerencia os projéteis disparados da espaçonave"""

    def __init__(self, ci_game):
        """Cria um objeto na posição atual da espaçonave"""
        
        super().__init__()
        self.screen = ci_game.screen
        self.settings = ci_game.settings
        self.color = self.settings.bullet_color

        #Cria um bullet rect em (0,0) e, em seguida, define a posição correta
        self.rect = pygame.Rect(0,0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = ci_game.ship.rect.midtop

        # Armazena a posição do projétil como um float
        self.y = float(self.rect.y)


    def update(self):
        """Desloca o projétil vertivalmente pela tela"""
        
        # Atualiza a posição exata do projétil
        self.y -= self.settings.bullet_speed

        # Atualiza a posição do react
        self.rect.y = self.y


    def draw_bullet(self):
        """Desenha o projétil na tela"""
        
        pygame.draw.rect(self.screen, self.color, self.rect)
