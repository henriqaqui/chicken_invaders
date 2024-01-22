import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet

class ChickenInvasion:
    """Classe geral para gerenciar ativos e comportamento do jogo"""

    def __init__(self):
        """Inicializa e cria recursos do jogo"""

        pygame.init()

        # Clock ajuda a controlar a taxa de frame com o método tick()
        self.clock = pygame.time.Clock()

        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
            )
        pygame.display.set_caption("Chicken Invasion")
        
        # Define a cor do background
        self.bg_color = self.settings.bg_color

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

    
    def run_game(self):
        """Inicia o loop principal do jogo"""
        
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
            self.clock.tick(60)
            

    def _check_events(self):
        """Responde às teclas precionadas e a eventos do mouse"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
                    

    def _check_keydown_events(self, event):
        """Responde a teclas precionadas"""

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        
        elif event.key == pygame.K_q:
            sys.exit()
        
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    

    def _check_keyup_events(self, event):
        """Responde a teclas soltas"""

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    
    def _fire_bullet(self):
        """Cria um novo projétil e o adiciona ao grupo projéteis"""

        # if verifica limite de bullets permitidos
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        """Atualiza a posição dos projéteis e descarta os antigos"""

        # Atualiza as posições dos projéteis
        self.bullets.update()

        # Descarta os projéteis que desaparecem da tela
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)


    def _update_screen(self):
        """Atualiza as imagens na tela e muda para a nova tela"""
        self.screen.fill(self.bg_color)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()

        # Deixa a tela desenhada mais recente visível
        pygame.display.flip()


if __name__ == '__main__':
    # Cria uma instância do jogo e executa o jogo
    ci = ChickenInvasion()
    ci.run_game()
