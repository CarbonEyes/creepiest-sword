# cena_menu.py
import pygame
import sys
from botao import Botao
from cena import Cena
from cena_opcoes import CenaOpcoes 
from cena_jogo import CenaJogo # Importa a nova CenaJogo

class CenaMenu(Cena):
    """
    Representa a cena do menu principal do jogo.
    """
    def __init__(self, jogo):
        self.jogo = jogo
        self.botoes = []  # Inicializa a lista de botões aqui

        # Criar botões
        # ESTES BOTÕES DEVEM SER CRIADOS APENAS AQUI NO __init__
        btn_jogar = Botao(
            x=jogo.largura//2 - 100,
            y=200,
            largura=200,
            altura=50,
            texto="Jogar",
            cor_normal=(100, 255, 100),
            cor_hover=(50, 200, 50),
            acao=self.iniciar_jogo
        )
        
        btn_opcoes = Botao(
            x=jogo.largura//2 - 100,
            y=300,
            largura=200,
            altura=50,
            texto="Opções",
            cor_normal=(100, 100, 255),
            cor_hover=(50, 50, 200),
            acao=self.ir_para_opcoes # Adiciona a ação para ir para a cena de opções
        )
        
        btn_sair = Botao(
            x=jogo.largura//2 - 100,
            y=400,
            largura=200,
            altura=50,
            texto="Sair",
            cor_normal=(255, 100, 100),
            cor_hover=(200, 50, 50),
            acao=self.sair
        )
        
        self.botoes.extend([btn_jogar, btn_opcoes, btn_sair]) 
    
    def iniciar_jogo(self) -> None:
        """
        Função chamada ao clicar no botão "Jogar".
        Muda para a CenaJogo.
        """
        print("Iniciando o jogo...")
        # AQUI VOCÊ SÓ MUDA A CENA, NÃO RECRIA OS BOTÕES
        self.jogo.mudar_cena(CenaJogo(self.jogo)) 
    
    def ir_para_opcoes(self) -> None:
        """
        Função chamada ao clicar no botão "Opções", muda para a cena de opções.
        """
        self.jogo.mudar_cena(CenaOpcoes(self.jogo))
        
    def sair(self) -> None:
        """
        Função chamada ao clicar no botão "Sair", encerra o Pygame e o sistema.
        """
        self.jogo.rodando = False 
    
    def atualizar(self, eventos: list) -> None:
        """
        Atualiza o estado da cena do menu.
        Args:
            eventos (list): Lista de eventos do Pygame.
        """
        for botao in self.botoes:
            botao.atualizar(eventos)
    
    def desenhar(self, tela: pygame.Surface) -> None:
        """
        Desenha a cena do menu na tela.
        Args:
            tela (pygame.Surface): A superfície onde a cena será desenhada.
        """
        tela.fill((240, 240, 240))  # Fundo cinza claro
        
        # Desenha título
        fonte_titulo = pygame.font.SysFont('Arial', 48, bold=True)
        titulo = fonte_titulo.render("CREEPIEST SWORD", True, (0, 0, 0))
        tela.blit(titulo, (self.jogo.largura//2 - titulo.get_width()//2, 80))
        
        # Desenha botões
        for botao in self.botoes:
            botao.desenhar(tela)