import pygame
import sys
from jogo import Jogo
from cena_menu import CenaMenu

def main():
    # Cria a instância do jogo
    jogo = Jogo()
    
    # Define a cena inicial
    jogo.cena_atual = CenaMenu(jogo)
    
    # Inicia o loop principal
    jogo.executar()

if __name__ == "__main__":
    main()