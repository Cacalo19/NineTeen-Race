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
    
    def detectar_e_desviar(self, lista_inimigos):
        distancia_sensor = self.speed * 25
    
        for outro in lista_inimigos:
            if outro == self:
                continue
                
            # Em vez de criar um Rect novo, fazemos uma conta matemática simples:
            # 1. Checa se o outro carro está na mesma coluna (X) com uma margem
            if abs(self.rect.centerx - outro.rect.centerx) < 50:
                # 2. Checa se o outro carro está à frente e dentro da distância do sensor
                distancia_y = self.rect.y - outro.rect.y
                if 0 < distancia_y < distancia_sensor:
                    # Só entra aqui se realmente houver alguém no caminho
                    if self.speed > outro.speed:
                        passo_lateral = self.speed * 0.7
                        
                        if self.rect.x <= 210: self.rect.x += passo_lateral
                        elif self.rect.right >= 660: self.rect.x -= passo_lateral
                        else:
                            if self.rect.centerx < outro.rect.centerx:
                                self.rect.x -= passo_lateral
                            else:
                                self.rect.x += passo_lateral
                        
                        break # Encontrou um obstáculo, não precisa checar o resto da lista

    def draw(self, window: pygame.Surface):
        window.blit(self.surf, self.rect)

