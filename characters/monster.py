# characters/monster.py
import pygame
from core.settings import COINS_PER_MONSTER_KILL

class Monster(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, speed: int = 2, health: int = 20, damage: int = 5) -> None:
        super().__init__()
        try:
            self.image = pygame.image.load("assets/images/monster.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 60)) # Altura 60
        except pygame.error:
            print("Erro: Imagem do monstro (monster.png) não encontrada. Usando um retângulo vermelho como placeholder.")
            self.image = pygame.Surface((60, 60), pygame.SRCALPHA)
            self.image.fill((255, 0, 0)) 
        
        # O rect é criado aqui com o x e y passados
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed: int = speed
        self.health: int = health
        self.damage: int = damage # Dano que o monstro causa ao jogador
        self.coins_on_defeat: int = COINS_PER_MONSTER_KILL
        self.is_alive: bool = True

        # Para movimento simples de ir e vir
        self.direction: int = 1 # 1 para direita, -1 para esquerda
        self.walk_limit_left: int = x - 100 # Monstro anda 100px para a esquerda
        self.walk_limit_right: int = x + 100 # Monstro anda 100px para a direita


    def take_damage(self, damage: int) -> int:
        """
        Recebe dano. Retorna a quantidade de moedas se for derrotado.
        Args:
            damage (int): Quantidade de dano recebido.
        Returns:
            int: Quantidade de moedas se o monstro for derrotado, 0 caso contrário.
        """
        if not self.is_alive:
            return 0

        self.health -= damage
        print(f"Monstro atingido! Vida restante: {self.health}")
        if self.health <= 0:
            self.is_alive = False
            print("Monstro derrotado!")
            # Tocar som de monstro morrendo
            return self.coins_on_defeat
        return 0

    def update(self) -> None:
        """
        Atualiza a lógica do monstro (movimento).
        """
        if not self.is_alive:
            return

        # Movimento simples de patrulha
        self.rect.x += self.speed * self.direction
        
        if self.rect.x <= self.walk_limit_left:
            self.direction = 1 # Vai para a direita
            # Opcional: virar a imagem do monstro
        elif self.rect.x >= self.walk_limit_right:
            self.direction = -1 # Vai para a esquerda
            # Opcional: virar a imagem do monstro


    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha o monstro na tela se estiver vivo.
        Args:
            screen (pygame.Surface): A superfície da tela do Pygame.
        """
        if self.is_alive:
            # Se o monstro estiver virado para a esquerda, espelha a imagem
            if self.direction == -1:
                flipped_image = pygame.transform.flip(self.image, True, False)
                screen.blit(flipped_image, self.rect)
            else:
                screen.blit(self.image, self.rect)