import pygame

from code.Constante import COR_BRANCA, MENU_OPCOES, WINDOW_WIDTH


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/imagem/Menu.png').convert_alpha()
        self.rect = self.surf.get_rect()

    def run(self):
        #pygame.mixer.music.load('./asset/som/racing_game_menu.mp3')
        #pygame.mixer.music.play(-1)

        while True:          


            self.window.blit(self.surf, self.rect)

            #self.menu_text('START', 50, COR_BRANCA, WINDOW_WIDTH // 2, 930)
            #self.menu_text('SCORE', 50, (COR_BRANCA), WINDOW_WIDTH // 2, 1050)
            #self.menu_text('EXIT', 50, (COR_BRANCA), WINDOW_WIDTH // 2, 1170)

            for i in range(len(MENU_OPCOES)):
                self.menu_text(MENU_OPCOES[i], 50, COR_BRANCA, WINDOW_WIDTH // 2, 930 + 120 * i)
            
            pygame.display.flip()

            # Check todos os os eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    def menu_text(self, text, font_size, color, x, y):

        try:
            font = pygame.font.Font('./asset/fonte/PressStart2P-Regular.ttf', font_size)
        except:
            font = pygame.font.SysFont('Comic Sans MS', font_size, bold=True)
            print('Fonte personalizada não encontrada. Usando fonte padrão.')

        outline_color = (0, 0, 0)  # Cor preta para a borda

        offsets = [(-2, -2), (2, -2), (-2, 2), (2, 2)]  # Deslocamentos para criar a borda

        for ox, oy in offsets:
            outline_surf = font.render(text, True, outline_color) # Cor preta
            outline_rect = outline_surf.get_rect(center=(x + ox, y + oy))
            self.window.blit(outline_surf, outline_rect)


        # Efeito de sombra (opcional)
        #shadow_color = (20, 20, 20)  # Cor escura para a sombra
        #shadow_surface = font.render(text, True, shadow_color) # Cor escura
        #shadow_rect = shadow_surface.get_rect(center=(x + 6, y + 6))
        #self.window.blit(shadow_surface, shadow_rect)

        # Texto principal
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.window.blit(text_surface, text_rect)
