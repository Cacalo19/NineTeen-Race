import sys

import pygame

from code.Constante import FONTE_PERSONALIZADA, COR_PRETA, COR_AZUL

FILE_NAME = 'highscore.txt'

class Score:
    def __init__(self, window, ):
        self.window = window
        self.font = pygame.font.Font(FONTE_PERSONALIZADA, 40)

    @staticmethod
    def get_high_score(): # Lê o arquivo de texto e retorna uma lista com os 10 melhores recordes.
        arquivo = 'highscore.txt'
        recordes = []

        try:
            with open(arquivo, 'r') as f:
                for linha in f:
                    linha = linha.strip()
                    if ':' in linha:
                        nome, pontos = linha.split(':')
                        recordes.append((nome, int(pontos)))
                    elif linha:
                        recordes.append(('---', int(linha)))

            # Ordena a lista do maior para o menor score
            recordes.sort(key=lambda x: x[1], reverse=True)
            return recordes[:10]

        except (FileNotFoundError, ValueError):
            return [] # Retorna lista vazia se o arquivo não existir ou estiver corrompido.

    @staticmethod
    def salvar_score(nome, pontuacao_final): # Adiciona um novo score, ordena e salva apenas os 10 melhores no arquivo.
        arquivo = 'highscore.txt'
        recordes = Score.get_high_score()
        recordes.append((nome, pontuacao_final))

        # Mantém apenas o Top 10
        recordes.sort(key=lambda x: x[1], reverse=True)
        recordes = recordes[:10]

        try:
            with open(arquivo, 'w') as f:
                for n, p in recordes:
                    f.write(f"{n}:{p}\n")
            print(f"Lista de recordes atualizada com {nome}!")
        except Exception as e:
            print(f"Erro ao salvar arquivo: {e}")
    
    @staticmethod
    def mostrar_score(window): # Cria a tela visual para exibir o ranking dos jogadores.
        # Carrega o fundo (reutilizando o do menu para o teste)
        try:
            surf = pygame.image.load('./asset/imagem/score.png').convert_alpha()

        except:
            surf = pygame.Surface(window.get_size())
            surf.fill((50, 50, 50))

        try:
            fonte_base = pygame.font.Font(FONTE_PERSONALIZADA, 30)
            fonte_recorde = pygame.font.Font(FONTE_PERSONALIZADA, 20)

        except:
            fonte_base = pygame.font.SysFont('Arial', 40, bold=True)
            fonte_recorde = pygame.font.SysFont('Arial', 50, bold=True)

        fonte_titulo = fonte_base.render("TOP 10 RECORDES", True, (COR_PRETA))
        rect_titulo = fonte_titulo.get_rect(midtop=(window.get_width()//2, 520))

        texto_voltar = fonte_base.render("Aperte ESPACO para voltar", True, (255, 255, 255))
        rect_texto_voltar = texto_voltar.get_rect(midbottom=(window.get_width() // 2, window.get_height() - 50))
        
        # Lógica de carregamento de imagem e fontes.
        lista_recordes = Score.get_high_score()
        visualizando = True
        while visualizando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        visualizando = False # Sai do loop e volta para o game.py

            
            window.blit(surf, (0, 0))
            window.blit(fonte_titulo, rect_titulo)

            posicao_y = 580 # Altura inicial do primeiro recorde
            for i, recorde in enumerate(lista_recordes):
                nome, pontos = recorde

                texto_linha = f"{i+1:>2}.{nome:<10} - {pontos:>5} pts"
                cor_item = (COR_AZUL) if i == 0 else COR_PRETA

                img_linha = fonte_recorde.render(texto_linha, True, cor_item)
                rect_linha = img_linha.get_rect(midtop=(window.get_width() // 2, posicao_y))
                window.blit(img_linha, rect_linha)

                posicao_y += 25
            window.blit(texto_voltar, rect_texto_voltar)
            
            pygame.display.flip()

    def input_nome(window): # Cria uma tela interativa para o jogador digitar o nome ao bater um recorde.
        nome = ''
        fonte = pygame.font.Font(None, 80)
        digitando = True
        contador_cursor = 0 # Usado para o efeito de piscar o '_' .

        while digitando:
            window.fill((0, 0 ,0))
            # Efeito visual do cursor piscando (simula um terminal)
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
                        # Limita o nome a 6 caracteres alfanuméricos
                        if len(nome) < 6 and event.unicode.isalnum():
                            nome += event.unicode.upper()

            # (Desenho dos textos na tela)
            pygame.display.flip()
            pygame.time.Clock().tick(60)

        return nome if nome != '' else 'PLAYER'        