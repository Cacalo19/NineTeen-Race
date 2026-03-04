import pygame

from code.Constante import WINDOW_HEIGHT
from code.Entity import Entity

class Traffic(Entity):
    def __init__(self, name: str, position: tuple, speed: int):
        super().__init__(name, position)
        self.speed = speed

    def move(self, current_player_speed):
        relative_speed = current_player_speed - self.speed
        self.rect.y += relative_speed

        if self.rect.y > WINDOW_HEIGHT + 100:
            self.kill()

    def draw(self, window: pygame.Surface):
        window.blit(self.surf, self.rect)

