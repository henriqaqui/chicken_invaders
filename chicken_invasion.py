import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from chicken import Chicken

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

        # Cria uma instância para armazenar estatísticas do jogo
        self.stats = GameStats(self)
        
        # Define a cor do background
        self.bg_color = self.settings.bg_color

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.chickens = pygame.sprite.Group()

        self._create_fleet()

        # Inicializa o game em um estado ativo
        self.game_active = True

    
    def run_game(self):
        """Inicia o loop principal do jogo"""
        
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_chickens()

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
        
        self._check_bullet_chicken_collisions()

    
    def _check_bullet_chicken_collisions(self):
        """Responde à colisões"""

        # Remove todos os projéteis e galinhas que tenham colidido
        collision = pygame.sprite.groupcollide(
            self.bullets, self.chickens, True, True
        )

        if not self.chickens:
            # Destrói os projéteis existentes e cria uma nova frota
            self.bullets.empty()
            self._create_fleet()

    
    def _update_chickens(self):
        """Verifica se a frota está na borda e atualiza as posições"""

        self._check_fleet_edges()
        self.chickens.update()

        # Detecta colisões entre galinhas e espaçonaves
        if pygame.sprite.spritecollideany(self.ship, self.chickens):
            self._ship_hit()
        
        # Procura por galinhas se chocando contra a parte inferior da tela
        self._check_chickens_bottom()

    
    def _check_chickens_bottom(self):
        """Verifica se alguma galinha chegou à parte inferior da tela"""

        for chicken in self.chickens.sprites():
            if chicken.rect.bottom >= self.settings.screen_height:
                # Trata isso como se a espaçonave tivesse sido abatida
                self._ship_hit()
                break

    
    def _ship_hit(self):
        """Responde à espaçonave sendo abatida por uma galinha"""

        if self.stats.ships_left > 0:
            # Decrementa ships_left
            self.stats.ships_left -= 1

            # Descarta quaisquer projéteis e galinhas restantes
            self.bullets.empty()
            self.chickens.empty()

            # Cria uma nova frota e centraliza espaçonave
            self._create_fleet()
            self.ship.center_ship()

            # Pausa
            sleep(0.5)
        else:
            self.game_active = False


    def _create_fleet(self):
        """Cria a frota de galinhas"""

        # Cria galinha e continua adicionando até limite de tela
        # O distanciamento entre galinhas é a largura e altura de uma
        chicken = Chicken(self)
        chicken_width, chicken_height = chicken.rect.size

        # Posição da próxima galinha a ser posicionada
        current_x, current_y = chicken_width, chicken_height
        while current_y < (self.settings.screen_height - 6 * chicken_height):
            while current_x < (self.settings.screen_width - 2 * chicken_width):
                self._create_chicken(current_x, current_y)
                current_x += 2 * chicken_width

            # Temina uma fileira, redefine valor de x e incrementa y
            current_x = chicken_width
            current_y += 2 * chicken_height


    def _create_chicken(self, x_position, y_position):
        """Cria uma galinha e a posiciona na frota"""

        new_chicken = Chicken(self)
        new_chicken.x = x_position
        new_chicken.rect.x = x_position
        new_chicken.rect.y = y_position
        self.chickens.add(new_chicken)

    
    def _check_fleet_edges(self):
        """Responde apropriadamente se alguma galinha alcançou a borda"""

        for chicken in self.chickens.sprites():
            if chicken.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """Faz toda a frota descer e mudar de direção"""

        for chicken in self.chickens.sprites():
            chicken.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        

    def _update_screen(self):
        """Atualiza as imagens na tela e muda para a nova tela"""

        self.screen.fill(self.bg_color)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()
        self.chickens.draw(self.screen)

        # Deixa a tela desenhada mais recente visível
        pygame.display.flip()


if __name__ == '__main__':
    # Cria uma instância do jogo e executa o jogo
    ci = ChickenInvasion()
    ci.run_game()
