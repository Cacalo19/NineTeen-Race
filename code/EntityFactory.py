from re import match

from code.Background import Background
from code.Player import Player


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0, 0)):
        match entity_name:
            case 'Level1':
                return Background('pista1', position)
            case 'Player':
                return Player('player', position)
            case 'Caminhao':
               #return Enemy('Caminhao_inimigo', position, speed = 1)
               pass
        return None