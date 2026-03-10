import pygame
from code.Entity import Entity
from code.Background import Background
from code.Traffic import Traffic

class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.vel_horizontal = 5
        self.is_aceleracao = False 
        self.velocidade_atual = 0 # Começa parado.
        self.velocidade_maxima = 40   # Velocidade maxima.
        self.aceleracao = 0.1 # Quanho de velocidade.
        self.freiando = 0.3 # Frenagem.

        # Configuração do som do motor em loop.
        self.som_motor = pygame.mixer.Sound('./asset/som/engine-loop-1.wav')
        self.canal_motor = pygame.mixer.Channel(0)
        self.volume_motor = 0.1
        self.canal_motor.play(self.som_motor, loops=-1)        
        self.canal_motor.set_volume(self.volume_motor)

    def move(self):
        keys = pygame.key.get_pressed()

        # Lógica de Aceleração e Som
        if keys[pygame.K_w]:
            self.is_aceleracao= True
            if self.velocidade_atual < self.velocidade_maxima:
                self.velocidade_atual += self.aceleracao
            if self.volume_motor < 1:  # 0.8 é o volume máximo (ajuste como preferir).
                self.volume_motor += 0.1

        else: # Desaceleração gradual quando solta a tecla.
            self.is_aceleracao = False
            if self.velocidade_atual > 0:
                self.velocidade_atual -= self.freiando
            else:
                self.velocidade_atual = 0

            if self.volume_motor > 0.1:  # 0.1 é o som do motor ligado, mas parado.
                self.volume_motor -= 0.1
        self.canal_motor.set_volume(self.volume_motor)
        
        # Movimentação Lateral
        if keys[pygame.K_a]:
            self.rect.x -= self.vel_horizontal
        if keys[pygame.K_d]:
            self.rect.x += self.vel_horizontal

        # Limites da pista, Impede o carro de sair pela esquerda.
        if self.rect.left < 129:
            self.rect.left = 150
        # Limites da pista, Impede o carro de sair pela direita.
        if self.rect.right > 710:
            self.rect.right = 685

    def detectar_colisoes(self, entity_list):
        for ent in entity_list:
            # Ignora o próprio player e o fundo para não causar'falsa colisão'.
            if ent == self:
                continue
            
            # Checa colisão apenas com carros do tráfego (CPU).
            if isinstance(ent, Background):
                continue
            # 3. SÓ CHECA COLISÃO SE FOR UM CARRO DA CPU (Traffic).
            if isinstance(ent, Traffic):
                # O collide_mask só retorna algo se os pixels REAIS se tocarem (ignora transparências).
                if pygame.sprite.collide_mask(self, ent):
                    print(f"COLISÃO REAL COM: {ent.name}") # Debug para o terminal.
                    return True
        return False