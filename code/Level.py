import pygame

from code.Background import Background
from code.EntityFactory import EntityFactory


class Level:
    def __init__(self, window, name):
        self.window = window
        self.name = name

        self.entity_list = []


        self.player = EntityFactory.get_entity('Player', (350, 950))
        self.bg = EntityFactory.get_entity('Level1', (0, 0))

        if self.bg: self.entity_list.append(self.bg)
        if self.player: self.entity_list.append(self.player)

    def run(self, ):
        #pygame.mixer_music.load('./asset/som/musica.mp3')
        #pygame.mixer_music.play(-1)

        clock = pygame.time.Clock()

        while True:
            clock.tick(60)        
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            if self.player:
                self.player.move()

            for ent in self.entity_list:
                if isinstance(ent, Background):

                    ent.move(self.player.current_speed)
                elif ent != self.player:
                    ent.move()

            # Desenho
            self.window.fill((0, 0, 0))

            for ent in self.entity_list:
                if hasattr(ent, 'draw'):
                    ent.draw(self.window)
                else:
                    self.window.blit(ent.surf, ent.rect)

            pygame.display.flip()
