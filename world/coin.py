import pygame
from core.settings import SCREEN_HEIGHT

class Coin(pygame.sprite.Sprite):
    """
    Representa uma moeda que o jogador pode coletar.
    """
    def __init__(self, x: int, y: int, value: int = 1) -> None:
        super().__init__()
        try:
            self.image = pygame.image.load("assets/images/coin.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 40)) # Tamanho da moeda
        except pygame.error:
            print("Erro: Imagem da moeda (coin.png) não encontrada. Usando um círculo amarelo como placeholder.")
            self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 255, 0), (20, 20), 20) # Amarelo
        
        self.rect = self.image.get_rect(topleft=(x, y))
        self.value: int = value
        self.collected: bool = False
    
    def update(self) -> None:
        """
        Atualiza a lógica da moeda (queda).
        """
        if self.collected: # Moedas coletadas não precisam de update
            return

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Colisão com o CHÃO VERDE
        ground_level = SCREEN_HEIGHT - 50 #
        if self.rect.bottom >= ground_level:
            self.rect.bottom = ground_level
            self.velocity_y = 0 # Para que ela pare de cair

    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha a moeda na tela se não foi coletada.
        Args:
            screen (pygame.Surface): A superfície da tela do Pygame.
        """
        if not self.collected:
            screen.blit(self.image, self.rect)