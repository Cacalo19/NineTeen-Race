import pygame

from code.Constante import COR_AZUL, COR_BRANCA, MENU_OPCOES, WINDOW_WIDTH


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/imagem/menu.png').convert_alpha()
        self.rect = self.surf.get_rect()

    def run(self):
        menu_opcoes = 0
        #pygame.mixer.music.load('./asset/som/racing_game_menu.mp3')
        #pygame.mixer.music.play(-1)

        while True:          


            self.window.blit(self.surf, self.rect)

            for i in range(len(MENU_OPCOES)):
                if i == menu_opcoes:
                    self.menu_text(MENU_OPCOES[i], 45, COR_AZUL, WINDOW_WIDTH // 2, 925 + 120 * i)
                else:
                    self.menu_text(MENU_OPCOES[i], 45, COR_BRANCA, WINDOW_WIDTH // 2, 925 + 120 * i)
                        
            pygame.display.flip()

            # Check todos os os eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # Navegação do menu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if menu_opcoes < len(MENU_OPCOES) - 1:
                            menu_opcoes += 1
                        else:
                            menu_opcoes = 0
                    
                    if event.key == pygame.K_UP:
                        if menu_opcoes > 0:
                            menu_opcoes -= 1
                        else:
                            menu_opcoes = len(MENU_OPCOES) - 1
                    
                    if event.key == pygame.K_RETURN:
                        return MENU_OPCOES[menu_opcoes]

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


        # Texto principal
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.window.blit(text_surface, text_rect)
