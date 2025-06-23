import pygame

class Botao:
    def __init__(self, x, y, largura, altura, texto, cor_normal, cor_hover, acao=None):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor_normal = cor_normal
        self.cor_hover = cor_hover
        self.acao = acao # Certifique-se de que a ação é armazenada
        self.cor_atual = cor_normal # Inicializa a cor atual
        pygame.font.init() # Inicializa o módulo de fontes do Pygame, se ainda não estiver inicializado globalmente
        self.fonte = pygame.font.SysFont('Arial', 30) # Inicializa a fonte aqui
        
    def atualizar(self, eventos):
        mouse_pos = pygame.mouse.get_pos()
        self.clicado = False
        
        # Verifica hover
        if self.rect.collidepoint(mouse_pos):
            self.cor_atual = self.cor_hover
            # Verifica clique
            for evento in eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    self.clicado = True
                    if self.acao:
                        self.acao()
        else:
            self.cor_atual = self.cor_normal
            
    def desenhar(self, tela):
        # Desenha o retângulo do botão
        pygame.draw.rect(tela, self.cor_atual, self.rect)
        pygame.draw.rect(tela, (0, 0, 0), self.rect, 2)  # Borda
        
        # Desenha o texto
        texto_surf = self.fonte.render(self.texto, True, (0, 0, 0))
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        tela.blit(texto_surf, texto_rect)