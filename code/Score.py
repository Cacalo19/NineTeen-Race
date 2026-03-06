import sys

import pygame

from code.Constante import FONTE_PERSONALIZADA, COR_PRETA, COR_AZUL

FILE_NAME = 'highscore.text'

class Score:
    def __init__(self, window, ):
        self.window = window
        self.font = pygame.font.Font(FONTE_PERSONALIZADA, 40)

    @staticmethod
    def get_high_score():
        arquivo = 'highscore.text'
        scores = []

        try:
            with open(arquivo, 'r') as f:
                for linha in f:
                    linha = linha.strip()
                    if ':' in linha:
                        nome, pontos = linha.split(':')
                        scores.append((nome, int(pontos)))
                    elif linha:
                        scores.append(('---', int(linha)))

            scores.sort(key=lambda x: x[1], reverse=True)
            return scores[:10]

        except (FileNotFoundError, ValueError):
            return []

    @staticmethod
    def salvar_score(nome, pontuacao_final):
        arquivo = 'highscore.text'

        scores = Score.get_high_score()

        scores.append((nome, pontuacao_final))

        scores.sort(key=lambda x: x[1], reverse=True)
        scores = scores[:10]

        try:
            with open(arquivo, 'w') as f:
                for n, p in scores:
                    f.write(f"{n}:{p}\n")
            print(f"Lista de recordes atualizada com {nome}!")
        except Exception as e:
            print(f"Erro ao salvar arquivo: {e}")
    
    @staticmethod
    def mostrar_score(window):
        # Carrega o fundo (reutilizando o do menu para o teste)
        try:
            surf = pygame.image.load('./asset/imagem/score.png').convert_alpha()

        except:
            surf = pygame.Surface(window.get_size())
            surf.fill((50, 50, 50)) # Cinza escuro caso a imagem falhe

        try:
            fonte_base = pygame.font.Font(FONTE_PERSONALIZADA, 30)
            fonte_recorde = pygame.font.Font(FONTE_PERSONALIZADA, 20)

        except:
            fonte_base = pygame.font.SysFont('Ariel', 40, bold=True)
            fonte_recorde = pygame.font.SysFont('Ariel', 50, bold=True)

        # Fonte para o aviso
        fonte_titulo = fonte_base.render("TOP 10 RECORDES", True, (COR_PRETA))
        rect_titulo = fonte_titulo.get_rect(midtop=(window.get_width()//2, 520))

        texto_voltar = fonte_base.render("Aperte ESPACO para voltar", True, (255, 255, 255))
        rect_texto_voltar = texto_voltar.get_rect(midbottom=(window.get_width() // 2, window.get_height() - 50))
        
        lista_scores = Score.get_high_score()

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
            window.blit(fonte_titulo, rect_titulo)

            y_pos = 580 # Altura inicial do primeiro recorde
            for i, recorde in enumerate(lista_scores):
                nome, pontos = recorde

                texto_linha = f"{i+1:>2}.{nome:<10} - {pontos:>5} pts"
                cor_item = (COR_AZUL) if i == 0 else COR_PRETA

                img_linha = fonte_recorde.render(texto_linha, True, cor_item)
                rect_linha = img_linha.get_rect(midtop=(window.get_width() // 2, y_pos))
                window.blit(img_linha, rect_linha)

                y_pos += 25
            window.blit(texto_voltar, rect_texto_voltar)
            
            pygame.display.flip()

    def input_nome(window):
        nome = ''
        fonte = pygame.font.Font(None, 80)
        digitando = True

        contador_cursor = 0

        while digitando:
            window.fill((0, 0 ,0))
            contador_cursor += 1
            cursor = '_' if (contador_cursor // 30) % 2 == 0 else ''

            in_mensagem = fonte.render('  Novo Recorde!\nDigite seu nome:', True, (255, 255, 255))
            in_nome = fonte.render(nome + cursor, True, (255, 215, 0))

            window.blit(in_mensagem, (window.get_width()//2 - in_mensagem.get_width()//2, 200))
            window.blit(in_nome, (window.get_width()//2 - in_nome.get_width()//2, 400))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(nome) > 0:
                            digitando = False

                    elif event.key == pygame.K_BACKSPACE:
                        nome = nome[:-1]

                    else:
                        if len(nome) < 6 and event.unicode.isalnum():
                            nome += event.unicode.upper()

            pygame.display.flip()
            pygame.time.Clock().tick(60)

        return nome if nome != '' else 'PLAYER'        