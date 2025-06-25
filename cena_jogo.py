import pygame
from cena import Cena 
from characters.player import Player 
from world.environment import Environment 
from world.coin import Coin 

class CenaJogo(Cena):
    def __init__(self, jogo):
        self.jogo = jogo
        
        player_height = 70
        ground_y_top = jogo.altura - 50 
        player_y = ground_y_top - player_height

        self.player = Player(jogo.largura // 2 - (50//2), player_y) 
        self.environment = Environment()
        self.player_sword_damage: int = 1 
        
        self.monster_attack_cooldown: int = 60 # Cooldown em frames para monstros atacarem o jogador
        self.monster_last_attack_time: int = 0
 

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

            # Colisão de monstros com o jogador (monstros causando dano ao jogador)
        # Verifica colisões apenas a cada 'monster_attack_cooldown' frames para evitar dano instantâneo
        current_time = pygame.time.get_ticks() # Tempo atual em milissegundos

        #Converter cooldown de frames para milissegundos para usar com get_ticks()
        cooldown_ms = self.monster_attack_cooldown * (1000 / 60) # Considerando 60 FPS

        if self.player.health <= 0:
            print("GAME OVER!")
            from cena_menu import CenaMenu # Importação local para evitar dependência circular
            self.jogo.mudar_cena(CenaMenu(self.jogo)) # Volta para o menu 
        
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

        # Lógica de Game Over (se a vida do jogador chegar a 0)
       