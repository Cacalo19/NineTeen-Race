import random 

import pygame

from code.Score import Score
from code.Traffic import Traffic
from code.Background import Background
from code.EntityFactory import EntityFactory
from code.Constante import COR_AMARELA, COR_VERDE, COR_PRETA, OFFSETS_BORDA


class Level:
    def __init__(self, window, name):
        self.window = window
        self.name = name

        self.entity_list = []
        
        self.contagem_regressiva = 3
        self.go_timer = 0
        self.timer_iniciar = pygame.time.get_ticks()
        self.corrida_iniciada = False
        self.pausado = False

        self.mostrar_texto = True
        self.timer_piscar = pygame.time.get_ticks()
        self.som_contagem = pygame.mixer.Sound('./asset/som/countdown.ogg')
        pygame.mixer_music.load('./asset/som/neon_sign_circuit_bpm145.ogg')

        self.pontuacao = 0
        self.score = 0
        self.recorde_atual = Score.get_high_score()

        try:
            self.fonte_contagem = pygame.font.Font('./asset/fonte/PressStart2P-Regular.ttf', 80)
        except:
            self.fonte_contagem = pygame.font.SysFont('Arial', 80, bold=True)

        self.player = EntityFactory.get_entity('Player', (320, 950))
        self.bg = EntityFactory.get_entity('Level1', (0, 0))

        if self.bg: self.entity_list.append(self.bg)
        if self.player: self.entity_list.append(self.player)

        self.timer_spawn = 0
        self.spawn_delay = 1500
        

    def draw_text_with_outline(self, text, color, x, y):
        outline_color = (COR_PRETA)
        offsets = (OFFSETS_BORDA )
        
        for ox, oy in offsets:
            outline_surf = self.fonte_contagem.render(text, True, outline_color)
            outline_rect = outline_surf.get_rect(center=(x + ox, y + oy))
            self.window.blit(outline_surf, outline_rect)

        # Texto principal
        text_surf = self.fonte_contagem.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))
        self.window.blit(text_surf, text_rect)

        # fonte_hud = pygame.font.SysFont('Arial', 30, bold=True)
        # texto_surf = fonte_hud.render(f"PONTOS: {self.pontuacao}", True, (255, 255, 255))
        # self.window.blit(texto_surf, (20, 20)) # Desenha no canto superior esquerdo
    def draw_hud(self):
        fonte_hud = pygame.font.SysFont('Arial', 30, bold=True)
        texto_surf = fonte_hud.render(f"PONTOS: {self.score}", True, (255, 255, 255))
        self.window.blit(texto_surf, (20, 20)) # Desenha no canto superior esquerdo
        if hasattr(self, 'recorde_atual'):
            rec_surf = fonte_hud.render(f"RECORDE: {self.recorde_atual}", True, (255, 215, 0))
            self.window.blit(rec_surf, (20, 60))
    def run(self, ):
        clock = pygame.time.Clock()
        self.som_contagem.play()

        while True:
            clock.tick(60)
            agora = pygame.time.get_ticks()

            if not self.corrida_iniciada:
                if agora - self.timer_iniciar >= 1000:
                    self.contagem_regressiva -= 1
                    self.timer_iniciar = agora

                    if self.contagem_regressiva == 0:
                        self.corrida_iniciada = True
                        self.go_timer = agora

            # Iniciar Musica após o Go!       
            if self.corrida_iniciada and not pygame.mixer.music.get_busy() and not self.pausado:
                if agora - self.go_timer >= 1000:
                    pygame.mixer.music.play(-1)

            # Eventos Parte 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pausado = not self.pausado
                        if self.pausado:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()

            # Evento Parte 2 Logica de movimento
            if not self.pausado:               
                if self.corrida_iniciada and self.player:
                    self.player.move()

                # Movimentação das CPUs e Fundo
                for ent in self.entity_list: # Move o NPC
                    # Se for o Fundo ou um Carro da CPU, eles dependem da velocidade do Player
                    if isinstance(ent, Background) or isinstance(ent, Traffic):
                        ent.move(self.player.current_speed)

                # Spaw de veículos
                if self.corrida_iniciada:
                    agora = pygame.time.get_ticks()
                    tempo_decorrida = agora - self.go_timer # Tempo desde o  GO
                    if tempo_decorrida > 3000:
                        if agora - self.timer_spawn > self.spawn_delay:
                            tipo_sorteado = random.choice(['carro-caminhao', 'carro-lento', 'carro-padrao', 'carro-esportivo'])
                            novo_inimigo = EntityFactory.get_entity(tipo_sorteado)
                            if novo_inimigo:
                                self.entity_list.append(novo_inimigo)                            
                            self.timer_spawn = agora

                # Você precisa chamar o move() deles passando a velocidade do player
                for ent in self.entity_list:
                    if isinstance(ent, Traffic):
                        ent.move(self.player.current_speed)
                    elif isinstance(ent, Background):
                        ent.move(self.player.current_speed)

                #for ent in self.entity_list:
                    #if isinstance(ent, Traffic) and ent.rect.y >= 1200:
                        #self.score += 10
                for ent in self.entity_list:
                    # Verifica se é um carro da CPU (Traffic) e se ele passou do limite
                    if isinstance(ent, Traffic) and ent.rect.y >= 1200:
                        self.score += 100  # Aumenta para 100 pontos como você pediu
                        #ent.kill()        # Remove o carro da lista na HORA para não contar ponto de novo
                        print(f"Score atual: {self.score}")

                # Limpeza da lista
                self.entity_list = [ent for ent in self.entity_list if not isinstance(ent, Traffic) or ent.rect.y < 1200]
            
            # Desenho
            self.window.fill((0, 0, 0))

            for ent in self.entity_list:
                if hasattr(ent, 'draw'):
                    ent.draw(self.window)
                else:
                    self.window.blit(ent.surf, ent.rect)

            self.draw_hud()
            # Lógica do texto piscante
            if agora - self.timer_piscar > 500:
                self.mostrar_texto = not self.mostrar_texto
                self.timer_piscar = agora

            mostrar_go = self.corrida_iniciada and (agora - self.go_timer < 1000)

            if (not self.corrida_iniciada or mostrar_go) and self.mostrar_texto:
                texto_str = str(self.contagem_regressiva) if self.contagem_regressiva > 0 else "GO!"
                # Amarelo para os números, Verde para o GO!
                cor = (COR_AMARELA) if self.contagem_regressiva > 0 else (COR_VERDE)
                
                self.draw_text_with_outline(texto_str, cor, self.window.get_width()/2, self.window.get_height()/2)
            
           # --- MENSAGEM DE PAUSE (Desenha por cima de tudo) ---
            if self.pausado:
                # Opcional: Escurece a tela ao pausar
                overlay = pygame.Surface(self.window.get_size(), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                self.window.blit(overlay, (0, 0))
                
                self.draw_text_with_outline("PAUSADO", (255, 255, 255), self.window.get_width()/2, self.window.get_height()/2)

            pygame.display.flip()

        #return self.score
