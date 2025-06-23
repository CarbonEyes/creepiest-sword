from abc import ABC, abstractmethod

class Cena(ABC):
    @abstractmethod
    def atualizar(self, eventos):
        pass
    
    @abstractmethod
    def desenhar(self, tela):
        pass