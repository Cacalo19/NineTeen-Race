import pygame
from code.Entity import Entity

class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.vel_horizontal = 5
        self.is_acelerando = False 
        self.current_speed = 0 # Começa parado
        self.max_speed = 40   # Velocidade maxima
        self.acelerando = 0.1 # Quanho de velocidade
        self.freiando = 0.3

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.is_acelerando = True
            if self.current_speed < self.max_speed:
                self.current_speed += self.acelerando
        else:
            self.is_acelerando = False
            if self.current_speed > 0:
                self.current_speed -= self.freiando
            else:
                self.current_speed = 0

        
        if keys[pygame.K_a]:
            self.rect.x -= self.vel_horizontal
        if keys[pygame.K_d]:
            self.rect.x += self.vel_horizontal

        # Impede o carro de sair pela esquerda
        if self.rect.left < 129:
            self.rect.left = 150
        # Impede o carro de sair pela direita (ajuste 600 para a largura da sua pista)
        if self.rect.right > 710:
            self.rect.right = 685