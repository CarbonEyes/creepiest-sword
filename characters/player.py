import pygame
from characters.sword import Sword
from core.settings import PLAYER_SPEED, PLAYER_HEALTH, SCREEN_WIDTH, SCREEN_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None: # x e y são passados aqui
        super().__init__()
        try:
            self.image = pygame.image.load("assets/images/player.png").convert_alpha()
            new_width = int(self.image.get_width() * 0.2)
            new_height = int(self.image.get_height() * 0.2)
            self.image = pygame.transform.scale(self.image, (new_width, new_height))
        except pygame.error:
            print("Erro: Imagem do jogador (player.png) não encontrada. Usando um retângulo como placeholder.")
            self.image = pygame.Surface((80, 200), pygame.SRCALPHA) # Altura 70
            self.image.fill((0, 150, 255))
        
        # O rect é criado aqui com o x e y passados
        self.rect = self.image.get_rect(topleft=(x, y))

        # Atributos do Jogador
        self.speed: int = PLAYER_SPEED
        self.health: int = PLAYER_HEALTH
        self.coins: int = 0
        self.sword: Sword = Sword(self.rect.midright[0], self.rect.midright[1]) # A espada começa à direita do jogador

        # Atributos de Física Simples (Pulo/Gravidade) 
        self.velocity_y: float = 0.0
        self.is_jumping: bool = False
        self.gravity: float = 0.8 # Valor da gravidade
        self.jump_power: float = -15.0 # Força do pulo (negativo para subir)

        # Estado de movimento
        self.moving_left: bool = False
        self.moving_right: bool = False
        self.facing_right: bool = True # Para saber para onde o jogador está virado

    def handle_input(self, event: pygame.event.Event) -> None:
        """
        Processa eventos de teclado para movimento do jogador.
        Args:
            event (pygame.event.Event): O evento do Pygame.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.moving_left = True
                self.facing_right = False
            elif event.key == pygame.K_RIGHT:
                self.moving_right = True
                self.facing_right = True
            elif event.key == pygame.K_SPACE and not self.is_jumping: # Pulo 
                self.velocity_y = self.jump_power
                self.is_jumping = True
            elif event.key == pygame.K_z: # Exemplo de ataque com a espada
                self.sword.attack()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.moving_left = False
            elif event.key == pygame.K_RIGHT:
                self.moving_right = False

    def update(self) -> None:
        """
        Atualiza a lógica do jogador (movimento, física, espada).
        """
        # Movimento Horizontal
        if self.moving_left:
            self.rect.x -= self.speed
        if self.moving_right:
            self.rect.x += self.speed
        
        # Manter jogador dentro da tela
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))

        # Física de Gravidade e Pulo 
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Simples colisão com o "chão" (limite inferior da tela)
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0
            self.is_jumping = False

        # Atualiza a espada, fazendo-a seguir o jogador
        self.sword.update(self.rect.midright if self.facing_right else self.rect.midleft, self.facing_right)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha o jogador na tela.
        Args:
            screen (pygame.Surface): A superfície da tela do Pygame.
        """
        # Desenha o jogador
        # Se o jogador estiver virado para a esquerda, espelha a imagem
        if not self.facing_right:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, self.rect)
        else:
            screen.blit(self.image, self.rect)
        
        # Desenha a espada
        self.sword.draw(screen)

    def collect_coin(self, amount: int = 1) -> None:
        """
        Aumenta o número de moedas do jogador e tenta aumentar o tamanho da espada.
        Args:
            amount (int): A quantidade de moedas coletadas.
        """
        self.coins += amount
        print(f"Moedas: {self.coins}")
        # Lógica de crescimento da espada por moedas (será implementada na Sword)
        self.sword.try_grow_by_coins(self.coins)
        # Resetar moedas para a próxima progressão ou manter total
        # self.coins = 0 # Se a espada crescer por X moedas e resetar a contagem