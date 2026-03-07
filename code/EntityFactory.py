import random
from re import match

from code.Constante import VELOCIDADE_VEICULOS, WINDOW_HEIGHT
from code.Traffic import Traffic
from code.Background import Background
from code.Player import Player


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0, 0), current_entities=[]):

        faixas_x = [200, 340, 460, 600]
        y_spawn = position[1] if position[1] != 0 else -150

        if entity_name.startswith('carro'):

            random.shuffle(faixas_x)
            x_selecionado = None

            for faixa in faixas_x:
                ocupada = False
                for ent in current_entities:
                    if hasattr(ent, 'rect'):
                        if ent.rect.x == faixa and ent.rect.y < 250:
                            ocupada = True
                            break
                
                if not ocupada:
                    x_selecionado = faixa
                    break

            if x_selecionado is None:
                return None
                      
            posicao_final = (x_selecionado, y_spawn)
        else:
            posicao_final = position

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