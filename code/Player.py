import pygame
from code.Entity import Entity
from code.Background import Background
from code.Traffic import Traffic

class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.vel_horizontal = 5
        self.is_acelerando = False 
        self.current_speed = 0 # Começa parado
        self.max_speed = 45   # Velocidade maxima
        self.acelerando = 0.25 # Quanho de velocidade
        self.freiando = 0.4

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

    def detectar_colisoes(self, entity_list):
        for ent in entity_list:
            # 1. Ignorar se for o próprio jogador
            if ent == self:
                continue
            
            # 2. Ignorar se for o Fundo (Background)
            # Verifique se a classe se chama 'Background' no seu código
            if isinstance(ent, Background):
                continue
            # 3. SÓ CHECA COLISÃO SE FOR UM CARRO DA CPU (Traffic)
            if isinstance(ent, Traffic):
                # O collide_mask só retorna algo se os pixels REAIS se tocarem
                if pygame.sprite.collide_mask(self, ent):
                    print(f"COLISÃO REAL COM: {ent.name}") # Debug para o terminal
                    return True
        return False