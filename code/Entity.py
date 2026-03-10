from abc import ABC, abstractmethod

import pygame

# Classe base para todas as entidades do jogo (player, carros, fundo, etc.)
class Entity(ABC):
    def __init__(self, name:str, position:tuple):
        self.name = name
        self.image = pygame.image.load('./asset/imagem/' + name + '.png').convert_alpha()
        self.rect = self.image.get_rect(left=position[0], top=position[1])
        self.velocidade = 0

        self.mask = pygame.mask.from_surface(self.image) # Usada para colisões mais precisa.

    @abstractmethod
    def move(self, ):
        pass

    def draw(self, window):
        window.blit(self.image, self.rect)