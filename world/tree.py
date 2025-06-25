import pygame
from core.settings import COINS_PER_TREE_CUT

class Tree(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None: # x e y são passados aqui
        super().__init__()
        try:
            self.image = pygame.image.load("assets/images/tree.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (180, 120)) # Altura 120
        except pygame.error:
            print("Erro: Imagem da árvore (tree.png) não encontrada. Usando um retângulo verde como placeholder.")
            self.image = pygame.Surface((180, 120), pygame.SRCALPHA)
            self.image.fill((0, 100, 0)) 
            pygame.draw.rect(self.image, (139, 69, 19), (25, 90, 30, 30)) 

        # O rect é criado aqui com o x e y passados
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health: int = 3 # Quantos "hits" para cortar a árvore
        self.coins_on_cut: int = COINS_PER_TREE_CUT
        self.is_cut: bool = False

    def take_hit(self, damage: int) -> int:
        """
        Recebe dano. Retorna a quantidade de moedas se for cortada.
        Args:
            damage (int): Quantidade de dano recebido.
        Returns:
            int: Quantidade de moedas se a árvore for cortada, 0 caso contrário.
        """
        if self.is_cut:
            return 0
            
        self.health -= damage
        print(f"Árvore atingida! Vida restante: {self.health}")
        if self.health <= 0:
            self.is_cut = True
            print("Árvore cortada!")
            # Tocar som de árvore caindo/cortando
            return self.coins_on_cut
        return 0

    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha a árvore na tela se não estiver cortada.
        Args:
            screen (pygame.Surface): A superfície da tela do Pygame.
        """
        if not self.is_cut:
            screen.blit(self.image, self.rect)