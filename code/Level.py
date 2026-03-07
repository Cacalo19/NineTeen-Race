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
        self.spawn_delay = 1000       

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

    def draw_hud(self):
        fonte_hud = pygame.font.SysFont('Arial', 30, bold=True)
        texto_surf = fonte_hud.render(f"PONTOS: {self.score}", True, (255, 255, 255))
        self.window.blit(texto_surf, (20, 20)) # Desenha no canto superior esquerdo


        if hasattr(self, 'recorde_atual'):
            lista_scores = Score.get_high_score()
            melhor_valor = lista_scores[0][1] if lista_scores else 0

            rec_surf = fonte_hud.render(f"RECORDE: {melhor_valor}", True, (255, 215, 0))
            self.window.blit(rec_surf, (20, 60))

    def run(self, ):
        clock = pygame.time.Clock()
        self.som_contagem.play()

        while True:
            clock.tick(60)
            agora = pygame.time.get_ticks()

            # --- LÓGICA DE CONTAGEM REGRESSIVA ---
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

            # Eventos
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

            # --- LÓGICA DO JOGO (MOVIMENTO E COLISÃO) ---
            if not self.pausado:               
                if self.corrida_iniciada and self.player:
                    self.player.move()

                    # 1. Filtra a lista de tráfego apenas UMA VEZ para a IA usar
                    lista_trafego = [e for e in self.entity_list if isinstance(e, Traffic)]
                    
                    # 2. LOOP ÚNICO: Processa Movimento, IA, Pontuação e Remoção
                    nova_lista = []
                    for ent in self.entity_list:
                        if isinstance(ent, (Background, Traffic)):
                            # Move fundo e inimigos com base na velocidade do player
                            ent.move(self.player.current_speed)
                            
                            if isinstance(ent, Traffic):
                                # Inteligência de desvio (executa apenas 30x por segundo para economizar CPU)
                                if agora % 2 == 0:
                                    ent.detectar_e_desviar(lista_trafego)
                                
                                # Pontuação: Se o carro saiu por baixo da tela
                                if ent.rect.y >= 1200:
                                    self.score += 10
                                    continue # Pula o append: remove o carro da lista
                        else:
                            # Movimenta entidades que não dependem do player (como o próprio player se houver lógica interna)
                            if ent != self.player: 
                                ent.move()

                        nova_lista.append(ent)
                    
                    self.entity_list = nova_lista

                    # --- LÓGICA DE DIFICULDADE (AJUSTE DINÂMICO) ---
                    if self.score > 200:
                        self.spawn_delay = 500  # 2 carros por segundo (mais difícil)
                    elif self.score > 100:
                        self.spawn_delay = 750  # ~1.3 carros por segundo
                    else:
                        self.spawn_delay = 1000 # 1 carro por segundo (inicial)

                    # 3. SPAWN DE VEÍCULOS
                    if self.corrida_iniciada:
                        if agora - self.timer_spawn > self.spawn_delay:
                            chance = random.randint(1, 10)
                            if chance <= 3: # 10% de chance de ser um obstáculo parado
                                
                                tipo_sorteado = random.choice(['carro-emergencia'])
                            else:                        
                                tipo_sorteado = random.choice(['carro-caminhao', 'carro-lento', 'carro-padrao', 'carro-esportivo'])
                                
                            novo_inimigo = EntityFactory.get_entity(tipo_sorteado, (0, -200), self.entity_list)
                            
                            if novo_inimigo:
                                self.entity_list.append(novo_inimigo)
                            self.timer_spawn = agora

                    # 4. CHECAR COLISÃO
                    if self.player.detectar_colisoes(self.entity_list):
                        print(f"GAME OVER! Score Final: {self.score}")
                        pygame.mixer.music.stop()
                        return self.score                  
                
            # --- DESENHO (RENDERIZAÇÃO) ---
            self.window.fill((0, 0, 0))

            # Desenha todas as entidades da lista
            for ent in self.entity_list:
                if hasattr(ent, 'draw'):
                    ent.draw(self.window)
                else:
                    self.window.blit(ent.surf, ent.rect)

            self.draw_hud()

            # Efeito visual de texto piscante
            if agora - self.timer_piscar > 500:
                self.mostrar_texto = not self.mostrar_texto
                self.timer_piscar = agora

            # Desenha Contagem Regressiva ou "GO!"
            mostrar_go = self.corrida_iniciada and (agora - self.go_timer < 1000)

            if (not self.corrida_iniciada or mostrar_go) and self.mostrar_texto:
                texto_str = str(self.contagem_regressiva) if self.contagem_regressiva > 0 else "GO!"
                # Amarelo para os números, Verde para o GO!
                cor = (COR_AMARELA) if self.contagem_regressiva > 0 else (COR_VERDE)
                
                self.draw_text_with_outline(texto_str, cor, self.window.get_width()/2, self.window.get_height()/2)
            
           # --- Tela de Pause ---
            if self.pausado:
                # Opcional: Escurece a tela ao pausar
                overlay = pygame.Surface(self.window.get_size(), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                self.window.blit(overlay, (0, 0))
                
                self.draw_text_with_outline("PAUSADO", (255, 255, 255), self.window.get_width()/2, self.window.get_height()/2)

            pygame.display.flip()