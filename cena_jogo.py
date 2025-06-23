import pygame
from cena import Cena 
from characters.player import Player 
from world.environment import Environment 
from world.coin import Coin 

class CenaJogo(Cena):
    def __init__(self, jogo):
        self.jogo = jogo

        # A altura do jogador é 70 (se usando placeholder ou escala)
        player_height = 70 
        # O Y do topleft do jogador deve ser ground_y_top - player_height
        ground_y_top = jogo.altura - 50 #
        player_y = ground_y_top - player_height

        self.player = Player(jogo.largura // 2 - (50//2), player_y) #
        # O cálculo acima já define o topleft Y corretamente. Não precisa mais do self.player.rect.bottom = jogo.altura - 50
        # A linha self.player.rect.bottom = jogo.altura - 50 no __init__ de CenaJogo é redundante
        # se o y for calculado como acima. Mantenha apenas uma das abordagens.
        # Se você usar o y = ground_y_top - player_height, a linha self.player.rect.bottom = jogo.altura - 50
        # não é mais necessária, pois o player já estará posicionado corretamente.

        # Ajusta a posição X para o centro da largura da tela.
        # O X passado para Player deve ser o topleft, então subtrai metade da largura do player (50//2).
        self.player.rect.x = jogo.largura // 2 - (self.player.rect.width // 2)

        self.environment = Environment()
        self.player_sword_damage: int = 1 

    def atualizar(self, eventos: list) -> None:
        """
        Atualiza a lógica da cena do jogo.
        Args:
            eventos (list): Lista de eventos do Pygame.
        """
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE: # Exemplo: voltar ao menu
                    from cena_menu import CenaMenu
                    self.jogo.mudar_cena(CenaMenu(self.jogo))
                elif evento.key == pygame.K_c: # Botão 'C' para simular coletar moeda (TESTE)
                    self.player.collect_coin(1)
                elif evento.key == pygame.K_x: # Botão 'X' para simular coletar muitas moedas (TESTE)
                    self.player.collect_coin(10) # Para testar crescimento rápido da espada

            # Passa todos os eventos para o jogador para que ele lide com seus inputs
            self.player.handle_input(evento)

        self.player.update() # Atualiza a lógica do jogador
        self.environment.update() # Atualiza a lógica do ambiente (movimento de monstros, etc.)

        # --- Lógica de Colisões e Interações ---
        # Colisão da espada do jogador com elementos do ambiente
        if self.player.sword.is_attacking: # Apenas verifica colisão se a espada estiver atacando
            # Colisão com árvores
            hit_trees = pygame.sprite.spritecollide(self.player.sword, self.environment.trees, False)
            for tree in hit_trees:
                # Cada acerto da espada causa dano à árvore
                coins_gained = tree.take_hit(self.player_sword_damage) # O dano pode vir da espada.power
                if coins_gained > 0:
                    self.player.collect_coin(coins_gained)

            # Colisão com monstros
            hit_monsters = pygame.sprite.spritecollide(self.player.sword, self.environment.monsters, False)
            for monster in hit_monsters:
                coins_gained = monster.take_damage(self.player_sword_damage)
                if coins_gained > 0:
                    self.player.collect_coin(coins_gained)

        # Colisão do jogador com moedas
        collected_coins = pygame.sprite.spritecollide(self.player, self.environment.coins, True) # 'True' remove a moeda ao colidir
        for coin in collected_coins:
            self.player.collect_coin(coin.value)
            # Tocar som de moeda coletada aqui (com volume de efeitos)
            # self.jogo.tocar_som("coin_collect.wav", self.jogo.volume_efeitos) # Exemplo

        # TODO: Colisão de monstros com o jogador (monstros causando dano ao jogador)
        # Isso envolveria um método player.take_damage(monster.damage)
        # e talvez uma condição para o monstro atacar (ex: estar perto do jogador)


    def desenhar(self, tela: pygame.Surface) -> None:
        """
        Desenha os elementos da cena do jogo na tela.
        Args:
            tela (pygame.Surface): A superfície onde a cena será desenhada.
        """
        tela.fill((135, 206, 235)) # Céu azul claro
        pygame.draw.rect(tela, (34, 139, 34), (0, self.jogo.altura - 50, self.jogo.largura, 50)) # Chão verde

        self.environment.draw(tela) # Desenha os elementos do ambiente
        self.player.draw(tela) # Desenha o jogador e sua espada

        # Exibir moedas (HUD temporário)
        font = pygame.font.SysFont('Arial', 30)
        coin_text = font.render(f"Moedas: {self.player.coins}", True, (0, 0, 0))
        tela.blit(coin_text, (10, 10))

        # Exibir tamanho da espada (HUD temporário)
        sword_height = self.player.sword.image.get_height()
        sword_size_text = font.render(f"Espada: {sword_height}px", True, (0, 0, 0))
        tela.blit(sword_size_text, (10, 50))

        # Exibir vida do jogador (HUD temporário)
        health_text = font.render(f"Vida: {self.player.health}", True, (0, 0, 0))
        tela.blit(health_text, (10, 90))