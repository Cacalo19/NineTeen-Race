import pygame
import sys

from code.Score import Score

from code.Level import Level
from code.Constante import COR_BRANCA, WINDOW_HEIGHT, WINDOW_WIDTH
from code.Menu import Menu

class Game:
    def __init__(self):
        pygame.init()
        

        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        ##
        self.fonte_principal = pygame.font.SysFont('Arial', 40, bold=True)
        # Cria a superfície do texto
        self.surf_texto_space = self.fonte_principal.render("PRESSIONE ESPAÇO\n      PARA INICIAR", True, COR_BRANCA)
        # Posiciona o texto (Centralizado horizontalmente, e a 100 pixels do fundo)
        self.rect_texto_space = self.surf_texto_space.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 500))
        # Variáveis para o efeito de piscar
        self.timer_pisca = pygame.time.get_ticks()
        self.mostrar_texto = True
        
        ##

        # Estados do Jogo
        self.estado = 'SPLASH'
        self.tempo_inicial = pygame.time.get_ticks() # Marca o tempo de inicio

        # Carregamento das Imagens
        self.surf_logo = pygame.image.load('asset/imagem/logo_empresa.png').convert_alpha()
        self.rect_logo = self.surf_logo.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        self.surf_titulo = pygame.image.load('asset/imagem/background_titulo.png').convert_alpha()
        self.rect_titulo = self.surf_titulo.get_rect(topleft=(0, 0))

    def run(self):
            running = True

            pygame.mixer_music.load('./asset/som/racing_game_title_bpm140.mp3')
            pygame.mixer_music.play(-1)

            while running:
                # Captura o tempo atual para o controle do Splash
                
                agora = pygame.time.get_ticks()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    
                    if self.estado == "TITLE" and event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            pygame.mixer.music.stop()
                            self.estado = "MENU"

                # 3. LÓGICA DE DESENHO (Usando os nomes certos)
                if self.estado == "SPLASH":
                    self.window.fill((0, 0, 0))
                    # Use os nomes definidos no __init__
                    self.window.blit(self.surf_logo, self.rect_logo)                    
                    if agora - self.tempo_inicial > 5000:
                        self.estado = "TITLE"
                    
                elif self.estado == "TITLE":
                    # 1. Desenha o fundo da tela de título primeiro
                    self.window.blit(self.surf_titulo, self.rect_titulo)

                    # --- NOVO: Lógica para fazer o texto piscar ---
                    if agora - self.timer_pisca > 500: # Muda a cada meio segundo
                        self.mostrar_texto = not self.mostrar_texto
                        self.timer_pisca = agora

                    # 2. Se for o momento de mostrar, desenha o texto por cima do fundo
                    if self.mostrar_texto:
                        self.window.blit(self.surf_texto_space, self.rect_texto_space)
                    
                elif self.estado == "MENU":
                    if not pygame.mixer.music.get_busy():
                        pygame.mixer_music.load('./asset/som/racing_game_menu.mp3')
                        pygame.mixer_music.play(-1)
                    
                    menu = Menu(self.window)
                    escolha = menu.run() 
                    
                    if escolha == "INICIAR":
                        pygame.mixer_music.stop()
                        level = Level(self.window, 'Level1')
                        pontos = level.run()

                        lista_atual = Score.get_high_score()

                        if len(lista_atual) < 10 or (len(lista_atual) > 0 and pontos > lista_atual[-1][1]):
                            nome_jogador =Score.input_nome(self.window)
                            Score.salvar_score(nome_jogador, pontos)
                        else:

                            # --- TELA DE GAME OVER ---
                            self.window.fill((0, 0, 0)) # Fundo preto
                            fonte = pygame.font.SysFont('Arial', 50, bold=True)
                            
                            # Criar os textos
                            texto_game_over = fonte.render("GAME OVER!", True, (255, 0, 0))
                            texto_score = fonte.render(f"Score Final: {pontos}", True, (255, 255, 255))
                            
                            # Centralizar e desenhar na tela
                            rect_go = texto_game_over.get_rect(center=(self.window.get_width()/2, self.window.get_height()/2 - 30))
                            rect_sc = texto_score.get_rect(center=(self.window.get_width()/2, self.window.get_height()/2 + 40))
                            
                            self.window.blit(texto_game_over, rect_go)
                            self.window.blit(texto_score, rect_sc)
                            
                            pygame.display.flip() # Atualiza a tela para mostrar o texto
                            
                            # Esperar 3 segundos (3000 milissegundos)
                            pygame.time.wait(3000)
                        
                        # Salvar e voltar
                        self.estado = 'MENU'

                    elif escolha == 'RECORDES':
                        Score.mostrar_score(self.window)
                        self.estado = 'MENU'

                    elif escolha == "SAIR" or escolha == None:
                        running = False            
    
                pygame.display.flip()
                self.clock.tick(60)             
            
            pygame.quit()
            sys.exit()   