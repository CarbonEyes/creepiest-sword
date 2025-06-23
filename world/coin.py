import pygame

class Coin(pygame.sprite.Sprite):
    """
    Representa uma moeda que o jogador pode coletar.
    """
    def __init__(self, x: int, y: int, value: int = 1) -> None:
        super().__init__()
        try:
            self.image = pygame.image.load("assets/images/coin.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 30)) # Tamanho da moeda
        except pygame.error:
            print("Erro: Imagem da moeda (coin.png) não encontrada. Usando um círculo amarelo como placeholder.")
            self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 255, 0), (15, 15), 15) # Amarelo
        
        self.rect = self.image.get_rect(topleft=(x, y))
        self.value: int = value
        self.collected: bool = False

    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha a moeda na tela se não foi coletada.
        Args:
            screen (pygame.Surface): A superfície da tela do Pygame.
        """
        if not self.collected:
            screen.blit(self.image, self.rect)