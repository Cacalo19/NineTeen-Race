import pygame

from code.Constante import WINDOW_HEIGHT, WINDOW_WIDTH
from code.Menu import Menu

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    def run(self):

        while True:
            menu = Menu(self.window)
            menu.run()
            pass
