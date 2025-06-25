# world/environment.py
import pygame
import random
from world.tree import Tree
from world.coin import Coin
from characters.monster import Monster
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Environment:
    """
    Gerencia os elementos do cenário, como árvores, moedas e inimigos.
    """
    def __init__(self) -> None:
        self.trees: pygame.sprite.Group = pygame.sprite.Group() 
        self.coins: pygame.sprite.Group = pygame.sprite.Group() 
        self.monsters: pygame.sprite.Group = pygame.sprite.Group() 

        self._generate_initial_elements()

    def _generate_initial_elements(self) -> None:
        ground_y_top = SCREEN_HEIGHT - 50 # A linha Y onde o chão começa

        # Árvores
        for i in range(3):
            x = random.randint(100, SCREEN_WIDTH - 200)
            # O Y que passamos é o topleft. Para que o bottom fique em ground_y_top,
            # o topleft deve ser ground_y_top - altura_do_sprite
            # Para uma Tree, a altura é 120 (baseado em tree.py ou na imagem real)
            y = ground_y_top - 120 # O rect.top será este valor, e o bottom será y + 120
            self.trees.add(Tree(x, y))

        # Monstros
        for i in range(2):
            x = random.randint(150, SCREEN_WIDTH - 150)
            # Para um Monster, a altura é 60 (baseado em monster.py ou na imagem real)
            y = ground_y_top - 60 # O rect.top será este valor, e o bottom será y + 60
            self.monsters.add(Monster(x, y))

    def update(self) -> None:
        """
        Atualiza a lógica de todos os elementos do ambiente.
        """
        self.monsters.update() 
        self.coins.update() # NOVO: Atualiza a física das moedas

        # Remover árvores cortadas e gerar moedas no local da árvore
        for tree in self.trees.copy(): 
            if tree.is_cut:
                # Gerar algumas moedas um pouco acima de onde a árvore estava, para que caiam
                for _ in range(tree.coins_on_cut):
                    coin_x = tree.rect.x + random.randint(0, tree.rect.width - 30)
                    coin_y = tree.rect.y + (tree.rect.height // 4) # Mais acima na árvore
                    self.coins.add(Coin(coin_x, coin_y))
                self.trees.remove(tree) 

        # Remover monstros derrotados e gerar moedas
        for monster in self.monsters.copy():
            if not monster.is_alive:
                for _ in range(monster.coins_on_defeat):
                    coin_x = monster.rect.x + random.randint(0, monster.rect.width - 30)
                    coin_y = monster.rect.y + (monster.rect.height // 4) # Mais acima no monstro
                    self.coins.add(Coin(coin_x, coin_y))
                self.monsters.remove(monster) 


    def check_collisions(self, player_rect: pygame.Rect, player_sword_rect: pygame.Rect, player_damage: int) -> None:
        """
        Verifica colisões entre o jogador, sua espada e os elementos do ambiente.
        Args:
            player_rect (pygame.Rect): O retângulo de colisão do jogador.
            player_sword_rect (pygame.Rect): O retângulo de colisão da espada do jogador.
            player_damage (int): O dano que o jogador (ou sua espada) causa.
        """
        # Colisão da espada com árvores
        if self.player_sword_active: # Apenas se a espada estiver em modo de ataque
            hit_trees = pygame.sprite.spritecollide(self.player_sword, self.trees, False) # False = não remove a árvore
            for tree in hit_trees:
                coins_gained = tree.take_hit(player_damage)
                if coins_gained > 0:
                    # Chamar o método collect_coin do jogador diretamente para ele gerenciar
                    # Isso será feito na CenaJogo, que tem acesso ao player
                    pass # A lógica de coletar moeda pelo player será feita em CenaJogo

            # Colisão da espada com monstros
            hit_monsters = pygame.sprite.spritecollide(self.player_sword, self.monsters, False)
            for monster in hit_monsters:
                coins_gained = monster.take_damage(player_damage)
                if coins_gained > 0:
                    pass # A lógica de coletar moeda pelo player será feita em CenaJogo

        # Colisão do jogador com moedas
        collected_coins = pygame.sprite.spritecollide(self.player, self.coins, True) # True = remove a moeda
        for coin in collected_coins:
            # Chamar o método collect_coin do jogador
            pass # Isso será feito na CenaJogo

        # Colisão de monstros com o jogador (inimigo causa dano ao jogador)
        # Mais tarde, você implementará a lógica de dano ao jogador aqui
        # hit_player_by_monster = pygame.sprite.spritecollide(player, self.monsters, False)
        # for monster in hit_player_by_monster:
        #     player.take_damage(monster.damage)


    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha todos os elementos do ambiente na tela.
        Args:
            screen (pygame.Surface): A superfície da tela do Pygame.
        """
        self.trees.draw(screen)
        self.monsters.draw(screen)
        self.coins.draw(screen)