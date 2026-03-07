import random
from re import match

from code.Constante import VEICULOS_ASSETS, VELOCIDADE_VEICULOS, WINDOW_HEIGHT
from code.Traffic import Traffic
from code.Background import Background
from code.Player import Player


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0, 0), current_entities=[]):

        faixas_x = [200, 340, 460, 600]
        y_spawn = position[1] if position[1] != 0 else -150

        acostamento = [129, 670]

        if entity_name.startswith('carro'):
            if entity_name in ['carro-emergencia']:
                faixas_possiveis = acostamento.copy()
            else:
                faixas_possiveis = faixas_x.copy()

            random.shuffle(faixas_possiveis)
            x_selecionado = None

            for faixa in faixas_possiveis:
                ocupada = False
                for ent in current_entities:
                    if hasattr(ent, 'rect'):
 
                        if abs(ent.rect.x - faixa) < 20 and ent.rect.y < 250:
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
                asset = random.choice(VEICULOS_ASSETS['carro-caminhao'])
                return Traffic(asset, posicao_final, speed=VELOCIDADE_VEICULOS['carro-caminhao'])
            case 'carro-lento':
                asset = random.choice(VEICULOS_ASSETS['carro-lento'])
                return Traffic(asset, posicao_final, speed=VELOCIDADE_VEICULOS['carro-lento'])
            case 'carro-padrao':
                asset = random.choice(VEICULOS_ASSETS['carro-padrao'])
                return Traffic(asset, posicao_final, speed=VELOCIDADE_VEICULOS['carro-padrao'])
            case 'carro-esportivo':
                asset = random.choice(VEICULOS_ASSETS['carro-esportivo'])
                return Traffic(asset, posicao_final, speed=VELOCIDADE_VEICULOS['carro-esportivo'])
            case 'carro-emergencia':
                asset = random.choice(VEICULOS_ASSETS['carro-emergencia'])
                return Traffic(asset, posicao_final, speed =VELOCIDADE_VEICULOS['carro-parado'])
            case 'carro-preso':
                asset = random.choice(VEICULOS_ASSETS['carro-preso'])
                return Traffic(asset, posicao_final, speed=VELOCIDADE_VEICULOS['carro-parado'])
        return None