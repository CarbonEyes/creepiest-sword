# world/projectile.py
import pygame
import math
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, SFX_VOLUME # Importa SCREEN_WIDTH e SCREEN_HEIGHT para limites de tela, e SFX_VOLUME para sons [cite: 9a, 10d]

class Projectile(pygame.sprite.Sprite):
    """
    Representa um projétil genérico (como uma bola de fogo).
    Gerencia seu movimento, dano e colisão.
    """
    def __init__(self, x: int, y: int, target_pos: tuple[int, int], speed: int = 5, damage: int = 10) -> None:
        """
        Inicializa um projétil.
        Args:
            x (int): Posição inicial X do projétil.
            y (int): Posição inicial Y do projétil.
            target_pos (tuple[int, int]): Posição (x, y) do alvo para onde o projétil se moverá.
            speed (int): Velocidade do projétil.
            damage (int): Dano que o projétil causa ao colidir.
        """
        super().__init__() # Inicializa a classe base pygame.sprite.Sprite

        # Carregar imagem do projétil ou usar placeholder
        try:
            self.image = pygame.image.load("assets/images/fireball.png").convert_alpha() # Carrega a imagem da bola de fogo [cite: 9a]
            self.image = pygame.transform.scale(self.image, (30, 30)) # Redimensiona a imagem para 30x30 pixels [cite: 9a]
        except pygame.error:
            print("Erro: Imagem da bola de fogo (fireball.png) não encontrada. Usando um círculo laranja como placeholder.")
            self.image = pygame.Surface((30, 30), pygame.SRCALPHA) # Cria uma Surface transparente [cite: 9a]
            pygame.draw.circle(self.image, (255, 120, 0), (15, 15), 15) # Desenha um círculo laranja como placeholder [cite: 9a]
        
        # O rect é a área de colisão e posição do sprite
        self.rect = self.image.get_rect(center=(x, y)) # Define o rect centralizado na posição inicial [cite: 9a]
        
        self.speed: int = speed
        self.damage: int = damage
        self.is_active: bool = True # Flag para controlar se o projétil ainda deve ser processado/desenhado

        # Calcular direção para o alvo usando vetores
        dx = target_pos[0] - x
        dy = target_pos[1] - y
        distance = math.hypot(dx, dy) # Calcula a distância euclidiana (magnitude do vetor)
        
        # Normaliza o vetor de direção para ter comprimento 1
        if distance == 0: # Evita divisão por zero se o alvo for exatamente a origem do projétil
            self.direction_x = 0
            self.direction_y = 0
        else:
            self.direction_x = dx / distance
            self.direction_y = dy / distance

        # Opcional: Rotação da imagem para apontar para o alvo
        # Isso faz a bola de fogo "olhar" para onde está indo [cite: 9a]
        angle = math.degrees(math.atan2(-dy, dx)) # atan2(y, x) retorna o ângulo em radianos; -dy porque o eixo Y do Pygame é invertido [cite: 9a]
        self.image = pygame.transform.rotate(self.image, angle) # Rota a imagem da Surface [cite: 9a]
        self.rect = self.image.get_rect(center=(x,y)) # Recalcula o rect após a rotação para manter o centro [cite: 9a]


    def update(self) -> None:
        """
        Atualiza a posição do projétil a cada frame.
        """
        if not self.is_active: # Se não estiver ativo, não atualiza [cite: 9a]
            return

        # Move o projétil na direção calculada com base na velocidade [cite: 9a]
        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed

        # Remover projéteis que saem da tela para evitar sobrecarga de memória [cite: 9a]
        screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT) # Cria um retângulo que representa a tela inteira [cite: 9a]
        if not screen_rect.colliderect(self.rect): # Verifica se o projétil colide com a área da tela [cite: 9a]
            self.is_active = False # Marca o projétil como inativo (será removido pelo grupo de sprites na CenaJogo) [cite: 9a]
            print("Projétil fora da tela.") # Mensagem de depuração [cite: 9a]


    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha o projétil na tela se estiver ativo.
        Args:
            screen (pygame.Surface): A superfície da tela do Pygame onde o projétil será desenhado.
        """
        if self.is_active: # Só desenha se estiver ativo [cite: 9a]
            screen.blit(self.image, self.rect) # Desenha a imagem na posição do rect do projétil [cite: 9a]
