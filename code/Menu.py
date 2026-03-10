import pygame

from code.Constante import COR_AZUL, COR_BRANCA, COR_PRETA, FONTE_PERSONALIZADA, MENU_OPCOES, WINDOW_WIDTH, DESLOCAMENTO_BORDA

clock = pygame.time.Clock()
class Menu: # Classe responsável por controlar o menu principal do jogo.
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/imagem/menu.png').convert_alpha()
        self.rect = self.surf.get_rect()

        font_size = 45  # tamanho padrão
        try: # Tenta carregar uma fonte externa; se falhar, usa a do sistema (Comic Sans).
            self.font = pygame.font.Font(FONTE_PERSONALIZADA , font_size)
        except:
            self.font = pygame.font.Font('Comic Sans MS', font_size, bold=True)
            print('Fonte personalizada não encontrada. Usando fonte padrão.')

    def run(self):
        menu_opcoes = 0 # Índice da opção selecionada no momento.
        clock = pygame.time.Clock()
        while True:
            self.window.blit(self.surf, self.rect)

            # Desenha as opções do menu; destaca a selecionada com uma cor diferente.
            for i in range(len(MENU_OPCOES)):
                if i == menu_opcoes:
                    self.menu_text(MENU_OPCOES[i], 45, COR_AZUL, WINDOW_WIDTH // 2, 925 + 120 * i)
                else:
                    self.menu_text(MENU_OPCOES[i], 45, COR_BRANCA, WINDOW_WIDTH // 2, 925 + 120 * i)
                        
            pygame.display.flip()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # Lógica de navegação no menu.
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN: # Move para baixo ou volta para o topo se chegar ao fim.
                        if menu_opcoes < len(MENU_OPCOES) - 1:
                            menu_opcoes += 1
                        else:
                            menu_opcoes = 0
                    
                    if event.key == pygame.K_UP: # Move para cima ou vai para o fim se estiver no top.
                        if menu_opcoes > 0:
                            menu_opcoes -= 1
                        else:
                            menu_opcoes = len(MENU_OPCOES) - 1
                    
                    if event.key == pygame.K_RETURN:
                        return MENU_OPCOES[menu_opcoes]        

    def menu_text(self, text, font_size, color, x, y):
        # Desenha o texto com um efeito de borda (outline).
        font = self.font 
        cor_borda = (COR_PRETA)  
        deslocamentos = (DESLOCAMENTO_BORDA)  

        for ox, oy in deslocamentos:
            surf_borda = font.render(text, True, cor_borda) 
            rect_borda = surf_borda.get_rect(center=(x + ox, y + oy))
            self.window.blit(surf_borda, rect_borda)

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.window.blit(text_surface, text_rect)
