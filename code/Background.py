import pygame

from code.Entity import Entity
from code.Constante import WINDOW_HEIGHT

class Background(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

    def move(self, velocidade_atual_player):
        # Move o fundo para baixo de acordo com a velocidade do jogador criando o efeito infinito
        self.rect.y += velocidade_atual_player
        if self.rect.y >= WINDOW_HEIGHT:
            self.rect.y = 0
    
    def draw(self, window: pygame.Surface): 
        # Desenha duas imagens para criar a pista infinita
        window.blit(self.image, self.rect)
        window.blit(self.image, (self.rect.x, self.rect.y - self.rect.height))