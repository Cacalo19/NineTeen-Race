from abc import ABC, abstractmethod

import pygame


class Entity(ABC):
    def __init__(self, name:str, position:tuple):
        self.name = name
        self.surf = pygame.image.load('./asset/imagem/' + name + '.png')
        self.rect = self.surf.get_rect(left=position[0], top=position[1])
        self.speed = 0

        self.mask = pygame.mask.from_surface(self.surf)

    @abstractmethod
    def move(self, ):
        pass

    def draw(self, window):
        window.blit(self.surf, self.rect)