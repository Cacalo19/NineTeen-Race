import pygame

from code.Entity import Entity
from code.Constante import WINDOW_HEIGHT

class Background(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

    def move(self, current_player_speed):
        self.rect.y += current_player_speed

        if self.rect.y >= WINDOW_HEIGHT:
            self.rect.y = 0


    
    def draw(self, window: pygame.Surface):
        window.blit(self.surf, self.rect)
        window.blit(self.surf, (self.rect.x, self.rect.y - self.rect.height))