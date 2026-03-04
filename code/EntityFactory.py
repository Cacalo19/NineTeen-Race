import random
from re import match

from code.Constante import VELOCIDADE_VEICULOS, WINDOW_HEIGHT
from code.Traffic import Traffic
from code.Background import Background
from code.Player import Player


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0, 0)):
        #x_aleatorio = random.randint(170, 670) # Limite da pista eicho x
        faixas_x = [200, 340, 460, 600]
        x_centralizado = random.choice(faixas_x)
        y_topo = -50 # Spawn acima da tela no eicho y
        #posicao_final = (x_aleatorio, y_topo)
        posicao_final = (x_centralizado, y_topo)

        match entity_name:
            case 'Level1':
                return Background('pista1', position)
            case 'Player':
                return Player('player', position)
            
            # Veículos da CPU
            case 'carro-caminhao':
                #return Traffic('carro_caminhao', position(WINDOW_HEIGHT - 1, random.randint(130, 710)), speed=VELOCIDADE_VEICULOS['carro-caminhao'])
                return Traffic('carro_caminhao', posicao_final, speed=VELOCIDADE_VEICULOS['carro-caminhao'])
            case 'carro-lento':
                #return Traffic('carro_lento1', position(WINDOW_HEIGHT - 1, random.randint(130, 710)), speed=VELOCIDADE_VEICULOS['carro-lento'])
                return Traffic('carro_lento1', posicao_final, speed=VELOCIDADE_VEICULOS['carro-lento'])
            case 'carro-padrao':
                #return Traffic('carro_padrao1', position(WINDOW_HEIGHT - 1, random.randint(130, 710)), speed=VELOCIDADE_VEICULOS['carro-padrao'])
                return Traffic('carro_padrao1', posicao_final, speed=VELOCIDADE_VEICULOS['carro-padrao'])
            case 'carro-esportivo':
                #return Traffic('carro_esportivo1', position(WINDOW_HEIGHT - 1, random.randint(130, 710)), speed=VELOCIDADE_VEICULOS['carro-esportivo'])
                return Traffic('carro_esportivo1', posicao_final, speed=VELOCIDADE_VEICULOS['carro-esportivo'])
        return None