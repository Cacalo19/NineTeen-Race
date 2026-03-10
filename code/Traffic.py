import pygame

from code.Constante import WINDOW_HEIGHT
from code.Entity import Entity

class Traffic(Entity): # Classe responsável pelos veículos da CPU.
    def __init__(self, name: str, position: tuple, velocidade: int):
        super().__init__(name, position)
        self.velocidade = velocidade # Velocidade própria do veículo.
        self.velocidade_original = velocidade
        self.is_parado = False

    def move(self, velocidade_jogador):
        # Se o carro estiver parado (ex: após uma colisão), ele não processa movimento.
        if self.is_parado:
            return
        
        # Faz o carro da CPU descer ou subir na tela conforme a sua velocidade.
        velocidade_relativa = velocidade_jogador - self.velocidade
        self.rect.y += velocidade_relativa

        # Remove o objeto do jogo se ele sumir muito para baixo da tela
        if self.rect.y > WINDOW_HEIGHT + 100:
            self.kill()
    
    def detectar_e_desviar(self, lista_inimigos):
        if self.is_parado:
            return
        
        # # Sensor de distância: quanto mais rápido o carro, mais longe ele "enxerga".
        distancia_sensor = self.velocidade * 25
        obstaculo_a_frente = False
        
        for outro in lista_inimigos:
            if outro == self:
                continue
                
            # Verifica se o outro carro está na mesma coluna X (faixa).
            if abs(self.rect.centerx - outro.rect.centerx) < 50:
                distancia_y = self.rect.y - outro.rect.y

                # Se o carro à frente estiver dentro do alcance do sensor,
                if 0 < distancia_y < distancia_sensor:
                    obstaculo_a_frente = True
                    if self.velocidade > outro.velocidade:
                        passo_lateral = self.velocidade * 0.7
                        direcao = 0 # 1 para direita, -1 para esquerda  ,                                             

                        # Decide para onde desviar baseando-se nas bordas da pista,
                        if self.rect.x <= 210: direcao = 1
                        elif self.rect.right >= 660: direcao = -1
                        else:direcao = -1 if self.rect.centerx < outro.rect.centerx else 1
                        
                        # Verifica se a faixa ao lado está livre para desviar,
                        bloqueado = False
                        for vizinho in lista_inimigos:
                            if vizinho == self or vizinho == outro: continue
                            distancia_x_vizinho = vizinho.rect.centerx - self.rect.centerx
                            if (direcao == 1 and 40 < distancia_x_vizinho < 120) or (direcao == -1 and -120 < distancia_x_vizinho < -40):
                                if abs(self.rect.y - vizinho.rect.y) < 160:
                                    bloqueado = True # Tem um carro fechando a passagem lateral,
                                    break
                            
                        if not bloqueado:
                            self.rect.x += int(direcao * passo_lateral) # Faz a troca de faixa,
                        else:
                            self.velocidade *= 0.98 # Se estiver cercado, pisa no freio

                        break # Encontrou um obstáculo, não precisa checar o resto da lista

        # Se o caminho estiver livre, o carro volta a ganhar velocidade gradualmente
        if not obstaculo_a_frente and self.velocidade < self.velocidade_original:
            self.velocidade += 0.1 # Acelera gradualmente
            if self.velocidade > self.velocidade_original:
                self.velocidade = self.velocidade_original

    def draw(self, window: pygame.Surface):
        window.blit(self.image, self.rect)

