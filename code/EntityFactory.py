import random

from code.Constante import VEICULOS_ASSETS, VELOCIDADE_VEICULOS
from code.Traffic import Traffic
from code.Background import Background
from code.Player import Player


class EntityFactory:

    @staticmethod
    def get_entity(nome_entidade: str, position=(0, 0), entidades_atuais=None):
        if entidades_atuais is None:
            entidades_atuais = []

        faixas_x = [200, 340, 460, 600] # Posição spawn de cada faixa na coordenada X.
        acostamento = [129, 670] # Posição spawn no acostamento na coordenada X.

        # Define o local de spawn no topo da tela
        y_spawn = position[1] if position[1] != 0 else -150
        # se veio posição específica, usa ela
        if position[0] != 0:
            x_selecionado = position[0]
            posicao_final = (x_selecionado, y_spawn)

        else:
            if nome_entidade.startswith('carro'):
                # Define se o carro deve ir para a pista ou para o acostamento.
                if nome_entidade in ['carro-policia', 'carro-preso']:
                    faixas_possiveis = acostamento.copy()
                else:
                    faixas_possiveis = faixas_x.copy()

                random.shuffle(faixas_possiveis) # Sorteia a ordem das faixas.
                x_selecionado = None

                # Lógica para evitar que carros nasçam um em cima do outro.
                for faixa in faixas_possiveis:
                    ocupada = False        
                    for ent in entidades_atuais:
                        if hasattr(ent, 'rect'):
                            if ent.rect.y < 250 and abs(ent.rect.x - faixa) < 40:
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

        # cria a entidade de acordo com o nome recebido
        match nome_entidade:
            case 'Level1':
                return Background('pista1', position)
            case 'Player':
                return Player('player', position)
            
            # Veículos da CPU            
            case 'carro-lento':
                asset = random.choice(VEICULOS_ASSETS['carro-lento'])
                return Traffic(asset, posicao_final, velocidade=VELOCIDADE_VEICULOS['carro-lento'])
            case 'carro-padrao':
                asset = random.choice(VEICULOS_ASSETS['carro-padrao'])
                return Traffic(asset, posicao_final, velocidade=VELOCIDADE_VEICULOS['carro-padrao'])
            case 'carro-esportivo':
                asset = random.choice(VEICULOS_ASSETS['carro-esportivo'])
                return Traffic(asset, posicao_final, velocidade=VELOCIDADE_VEICULOS['carro-esportivo'])
            case 'carro-emergencia':
                asset = random.choice(VEICULOS_ASSETS['carro-emergencia'])
                return Traffic(asset, posicao_final, velocidade =VELOCIDADE_VEICULOS['carro-emergencia'])
            case 'carro-policia':
                asset = random.choice(VEICULOS_ASSETS['carro-policia'])
                return Traffic(asset, posicao_final, velocidade=VELOCIDADE_VEICULOS['carro-parado'])
            case 'carro-preso':
                asset = random.choice(VEICULOS_ASSETS['carro-preso'])
                return Traffic(asset, posicao_final, velocidade=VELOCIDADE_VEICULOS['carro-parado'])
        return None