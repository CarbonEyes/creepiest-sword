import pygame
from core.settings import SWORD_GROWTH_PER_COIN, COINS_FOR_SWORD_LEVEL_UP # Importar de settings

class Sword(pygame.sprite.Sprite):
    """
    Representa a espada do jogador, que pode crescer.
    """
    def __init__(self, start_x: int, start_y: int) -> None:
        """
        Inicializa a espada.
        Args:
            start_x (int): Posição inicial X (relativa ao jogador).
            start_y (int): Posição inicial Y (relativa ao jogador).
        """
        super().__init__()

        # Imagem base da espada
        try:
            self.original_image = pygame.image.load("assets/images/sword.png").convert_alpha()
            self.original_image = pygame.transform.scale(self.original_image, (30, 100)) # Tamanho inicial
        except pygame.error:
            print("Erro: Imagem da espada (sword.png) não encontrada. Usando um retângulo como placeholder.")
            self.original_image = pygame.Surface((30, 100), pygame.SRCALPHA)
            self.original_image.fill((150, 150, 150)) # Cinza (lâmina)
            pygame.draw.rect(self.original_image, (100, 50, 0), (10, 80, 10, 20)) # Cabo marrom

        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=(start_x, start_y))

        self.base_width: int = self.image.get_width()
        self.base_height: int = self.image.get_height()
        self.current_growth_level: int = 0
        self.total_coins_collected: int = 0 # Para controle do crescimento

        self.is_attacking: bool = False
        self.attack_duration: int = 10 # Duração do ataque em frames
        self.attack_frame: int = 0
        self.facing_right: bool = True # Direção da espada

    def try_grow_by_coins(self, total_coins: int) -> None:
        """
        Tenta aumentar o tamanho da espada com base nas moedas coletadas.
        Args:
            total_coins (int): O total de moedas coletadas pelo jogador.
        """
        # A espada cresce a cada COINS_FOR_SWORD_LEVEL_UP moedas
        new_growth_level = total_coins // COINS_FOR_SWORD_LEVEL_UP
        
        if new_growth_level > self.current_growth_level:
            self.current_growth_level = new_growth_level
            # Aumenta a altura da espada (tamanho principal)
            new_height = self.base_height + (self.current_growth_level * SWORD_GROWTH_PER_COIN * 10) # Multiplica por 10 para um crescimento mais visível
            
            # Redimensiona a imagem da espada
            self.image = pygame.transform.scale(self.original_image, (self.base_width, int(new_height)))
            self.rect = self.image.get_rect(center=self.rect.center) # Recalcula o rect para manter o centro
            print(f"Espada cresceu! Nível: {self.current_growth_level}, Altura: {new_height:.2f}px")

    def attack(self) -> None:
        """
        Inicia o estado de ataque da espada.
        """
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_frame = 0
            print("Espada atacando!")
            # Tocar som de ataque aqui (usando o volume de efeitos do jogo)

    def update(self, player_attach_point: tuple[int, int], facing_right: bool) -> None:
        """
        Atualiza a posição e estado da espada.
        Args:
            player_attach_point (tuple[int, int]): O ponto do jogador onde a espada deve se anexar.
            facing_right (bool): True se o jogador está virado para a direita.
        """
        self.facing_right = facing_right

        # Posiciona a espada em relação ao jogador
        # A espada precisa se ajustar para ficar à direita ou esquerda do jogador e virar
        if self.facing_right:
            self.rect.midleft = player_attach_point # Fica à direita do jogador
            self.image = self.original_image # Garante que a imagem não esteja espelhada
            # Ajustar a imagem para o tamanho atual de crescimento
            new_height = self.base_height + (self.current_growth_level * SWORD_GROWTH_PER_COIN * 10)
            self.image = pygame.transform.scale(self.original_image, (self.base_width, int(new_height)))
            self.rect = self.image.get_rect(midleft=player_attach_point)
        else:
            self.rect.midright = player_attach_point # Fica à esquerda do jogador
            self.image = pygame.transform.flip(self.original_image, True, False) # Espelha
            # Ajustar a imagem para o tamanho atual de crescimento
            new_height = self.base_height + (self.current_growth_level * SWORD_GROWTH_PER_COIN * 10)
            self.image = pygame.transform.scale(self.image, (self.base_width, int(new_height)))
            self.rect = self.image.get_rect(midright=player_attach_point)


        # Lógica de ataque
        if self.is_attacking:
            self.attack_frame += 1
            if self.attack_frame >= self.attack_duration:
                self.is_attacking = False
                self.attack_frame = 0
            # Você pode adicionar animação de ataque aqui (ex: girar a espada, mover para frente)
            # Por enquanto, apenas muda o estado.

    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha a espada na tela.
        Args:
            screen (pygame.Surface): A superfície da tela do Pygame.
        """
        screen.blit(self.image, self.rect)