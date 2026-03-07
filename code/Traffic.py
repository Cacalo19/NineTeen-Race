import pygame

from code.Constante import WINDOW_HEIGHT
from code.Entity import Entity

class Traffic(Entity):
    def __init__(self, name: str, position: tuple, speed: int):
        super().__init__(name, position)
        self.speed = speed
        self.velocidade_original = speed

    def move(self, current_player_speed):
        relative_speed = current_player_speed - self.speed
        self.rect.y += relative_speed

        if self.rect.y > WINDOW_HEIGHT + 100:
            self.kill()
    
    def detectar_e_desviar(self, lista_inimigos):
        distancia_sensor = self.speed * 25
        obstaculo_a_frente = False
    
        for outro in lista_inimigos:
            if outro == self:
                continue
                
            # 1. Checa se o outro carro está na mesma coluna (X) com uma margem
            if abs(self.rect.centerx - outro.rect.centerx) < 50:
                # 2. Checa se o outro carro está à frente e dentro da distância do sensor
                distancia_y = self.rect.y - outro.rect.y
                if 0 < distancia_y < distancia_sensor:
                    obstaculo_a_frente = True
                    # Só entra aqui se realmente houver alguém no caminho
                    if self.speed > outro.speed:
                        passo_lateral = self.speed * 0.7

                        # Logica de checagem Lateral
                        direcao = 0                                               
                        #if self.rect.x <= 210: self.rect.x += passo_lateral
                        #elif self.rect.right >= 660: self.rect.x -= passo_lateral
                        if self.rect.x <= 210: direcao = 1
                        elif self.rect.right >= 660: direcao = -1
                        else:direcao = -1 if self.rect.centerx < outro.rect.centerx else 1
                        
                        bloqueado = False
                        for vizinho in lista_inimigos:
                            if vizinho == self or vizinho == outro: continue
                            distancia_x_vizinho = vizinho.rect.centerx - self.rect.centerx
                            if (direcao == 1 and 40 < distancia_x_vizinho < 120) or (direcao == -1 and -120 < distancia_x_vizinho < -40):
                                if abs(self.rect.y - vizinho.rect.y) < 160:
                                    bloqueado = True
                                    break
                            
                        if not bloqueado:
                            self.rect.x += (direcao * passo_lateral)
                        else:
                            self.speed *= 0.98

                        # else:
                        #     if self.rect.centerx < outro.rect.centerx:
                        #         self.rect.x -= passo_lateral
                        #     else:
                        #         self.rect.x += passo_lateral
                        
                        break # Encontrou um obstáculo, não precisa checar o resto da lista

        # --- LÓGICA DE RECUPERAÇÃO DE VELOCIDADE ---
        # Se não há obstáculos à frente e a velocidade atual é menor que a original
        if not obstaculo_a_frente and self.speed < self.velocidade_original:
            self.speed += 0.1 # Acelera gradualmente
            if self.speed > self.velocidade_original:
                self.speed = self.velocidade_original

    def draw(self, window: pygame.Surface):
        window.blit(self.surf, self.rect)

