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

        # Configuração do texto "PRESSIONE ESPAÇO" e efeito de piscar
        self.fonte_principal = pygame.font.SysFont('Arial', 40, bold=True)
        self.surf_texto_space = self.fonte_principal.render('PRESSIONE ESPAÇO\n      PARA INICIAR', True, COR_BRANCA)
        self.rect_texto_space = self.surf_texto_space.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 500))

        self.timer_pisca = pygame.time.get_ticks()
        self.mostrar_texto = True

        # O estado inicial define qual tela será exibida
        self.estado = 'LOGO_EMPRESA'
        self.tempo_inicial = pygame.time.get_ticks() # Marca o tempo de inicio

        # Carrega os elementos visuais das telas iniciais
        self.surf_logo = pygame.image.load('asset/imagem/logo_empresa.png').convert_alpha()
        self.rect_logo = self.surf_logo.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        self.surf_titulo = pygame.image.load('asset/imagem/background_titulo.png').convert_alpha()
        self.rect_titulo = self.surf_titulo.get_rect(topleft=(0, 0))
        self.menu = Menu(self.window)
    def run(self):
            jogo_rodando = True

            pygame.mixer.music.load('./asset/som/racing_game_title_bpm140.mp3')
            pygame.mixer.music.play(-1)

            while jogo_rodando:                
                agora = pygame.time.get_ticks()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        jogo_rodando = False
                    
                    # Se estiver na tela de título, a tecla ESPAÇO leva ao MENU
                    if self.estado == 'TELA_INICIAL' and event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            pygame.mixer.music.stop()
                            self.estado = "MENU"

                self.window.fill((0, 0, 0))
                
                # Desenha a tela baseada no valor de estado
                if self.estado == 'LOGO_EMPRESA':                    
                    # Use os nomes definidos no __init__
                    self.window.blit(self.surf_logo, self.rect_logo)                    
                    if agora - self.tempo_inicial > 5000:
                        self.estado = 'TELA_INICIAL'
                    
                elif self.estado == 'TELA_INICIAL':
                    # 1. Desenha o fundo da tela de título primeiro
                    self.window.blit(self.surf_titulo, self.rect_titulo)

                    # Lógica para alternar a visibilidade do texto (efeito piscar)
                    if agora - self.timer_pisca > 700: 
                        self.mostrar_texto = not self.mostrar_texto
                        self.timer_pisca = agora

                    if self.mostrar_texto:
                        self.window.blit(self.surf_texto_space, self.rect_texto_space)
                    
                elif self.estado == 'MENU':
                    if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.load('./asset/som/racing_game_menu.mp3')
                        pygame.mixer.music.play(-1)
                    
                    escolha = self.menu.run() 
                    
                    if escolha == 'INICIAR':
                        pygame.mixer.music.stop()
                        level = Level(self.window, 'Level1')
                        pontos = level.run()

                        # Verifica se o jogador entrou no Top 10 de recordes.
                        lista_atual = Score.get_high_score()
                        if len(lista_atual) < 10 or (len(lista_atual) > 0 and pontos > lista_atual[-1][1]):
                            nome_jogador =Score.input_nome(self.window)
                            Score.salvar_score(nome_jogador, pontos)
                        else:
                            # Se não bateu recorde, exibe apenas a tela de Game Over.
                            self.window.fill((0, 0, 0))
                            fonte = pygame.font.SysFont('Arial', 50, bold=True)
                            texto_game_over = fonte.render('GAME OVER!', True, (255, 0, 0))
                            texto_score = fonte.render(f'Score Final: {pontos}', True, (255, 255, 255))
                            rect_game_over = texto_game_over.get_rect(center=(self.window.get_width()/2, self.window.get_height()/2 - 30))
                            rect_score = texto_score.get_rect(center=(self.window.get_width()/2, self.window.get_height()/2 + 40))
                            
                            self.window.blit(texto_game_over, rect_game_over)
                            self.window.blit(texto_score, rect_score)
                            
                            pygame.display.flip()
                            pygame.time.wait(3000) # Esperar 3 segundos.
                        
                        self.estado = 'MENU'

                    elif escolha == 'RECORDES':
                        Score.mostrar_score(self.window)
                        self.estado = 'MENU'

                    elif escolha == 'SAIR' or escolha == None:
                        jogo_rodando = False            
    
                pygame.display.flip() # Atualiza a tela a cada quadro.
                self.clock.tick(60) # Mantém o jogo a 60 FPS.     
            
            pygame.quit()
            sys.exit()   