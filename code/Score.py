import sys

import pygame

from code.Constante import FONTE_PERSONALIZADA, COR_PRETA

FILE_NAME = 'highscore.text'

class Score:
    def __init__(self, window, ):
        self.window = window

    @staticmethod
    def get_high_score():
        arquivo = 'highscore.text'
        try:
            with open(arquivo, 'r') as f:
                conteudo = f.read().strip()
                return int(conteudo) if conteudo else 0
        except (FileNotFoundError, ValueError):
            return 0

    @staticmethod
    def salvar_score(pontuacao_final):
        arquivo = 'highscore.text'
        recorde = 0

        # Se os pontos forem maior que 0, salva o arquivo
        if pontuacao_final > recorde:
            with open(arquivo, 'w') as f:
                f.write(str(pontuacao_final))
            print(f"Novo recorde salvo: {pontuacao_final}!")
    

    @staticmethod
    def mostrar_score(window):
        # Carrega o fundo (reutilizando o do menu para o teste)
        try:
            surf = pygame.image.load('./asset/imagem/score.png').convert_alpha()

        except:
            surf = pygame.Surface(window.get_size())
            surf.fill((50, 50, 50)) # Cinza escuro caso a imagem falhe

        try:
            fonte_recordes = pygame.font.Font(FONTE_PERSONALIZADA, 50, bold=True)
            fonte_voltar = pygame.font.Font(FONTE_PERSONALIZADA, 50, bold=True)
        except:
            fonte_recordes = pygame.font.SysFont('Arial', 50, bold=True)
            fonte_voltar = pygame.font.SysFont('Arial', 50, bold=True)


        # Fonte para o aviso
        fonte_recordes = fonte_recordes.render("RECORDES", True, (COR_PRETA))
        rect_recordes = fonte_recordes.get_rect(midtop=(window.get_width()//2, 520))


        texto_voltar = fonte_voltar.render("Aperte ESPACO para voltar", True, (255, 255, 255))
        rect_texto_voltar = texto_voltar.get_rect(midbottom=(window.get_width() // 2, window.get_height() - 50))
        

        visualizando = True
        while visualizando:
            # 1. Trata eventos para conseguir sair dessa tela
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        visualizando = False # Sai do loop e volta para o game.py

            # 2. Desenha
            window.blit(surf, (0, 0))
            window.blit(fonte_recordes, rect_recordes)
            window.blit(texto_voltar, rect_texto_voltar)
            
            pygame.display.flip()