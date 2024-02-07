import pygame
from pygame.sprite import Sprite

class Chicken(Sprite):
    """Classe para representar uma única galinha na frota"""

    def __init__(self, ci_game):
        """Inicializa a galinha e define sua posição inicial"""
        super().__init__()
        self.screen = ci_game.screen
        self.settings = ci_game.settings

        # Carrega a imagem da galinha e define seu atributo rect
        self.image = pygame.image.load('images/chicken_alien.bmp')
        self.rect = self.image.get_rect()

        # Inicia cada galinha nova perto do canto superio esquerdo da tela
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Armazena a posição horizontal exata da galinha
        self.x = float(self.rect.x)
    

    def update(self):
        """Move a galinha para a direita ou para a esquerda"""
        self.x += self.settings.chicken_speed * self.settings.fleet_direction
        self.rect.x = self.x


    def check_edges(self):
        """Retorna True se a galinha estiver na borda da tela"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
    