import pygame

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

        self.mostrar_texto = True
        self.timer_piscar = pygame.time.get_ticks()
        self.som_contagem = pygame.mixer.Sound('./asset/som/countdown.ogg')
        pygame.mixer_music.load('./asset/som/neon_sign_circuit_bpm145.ogg')

        try:
            self.fonte_contagem = pygame.font.Font('./asset/fonte/PressStart2P-Regular.ttf', 80)
        except:
            self.fonte_contagem = pygame.font.SysFont('Arial', 80, bold=True)

        self.player = EntityFactory.get_entity('Player', (350, 950))
        self.bg = EntityFactory.get_entity('Level1', (0, 0))

        if self.bg: self.entity_list.append(self.bg)
        if self.player: self.entity_list.append(self.player)

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
                    #Som de contagem

                    #if self.contagem_regressiva > 0:
                        #self.som_contagem.play()
                    
                    if self.contagem_regressiva == 0:
                        #self.som_contagem.stop()
                        self.corrida_iniciada = True
                        self.go_timer = agora
                        #pygame.mixer_music.play(-1)
                    
                    if self.corrida_iniciada and not pygame.mixer.music.get_busy():
                        # Se já passou 1 segundo (1000ms) do momento do GO!
                        if agora - self.go_timer >= 1000:
                            pygame.mixer.music.play(-1)

            # Evento fechar a janela
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
            
            # Movimentação
            if self.corrida_iniciada:
                if self.player:
                    self.player.move()

                    for ent in self.entity_list:
                        if isinstance(ent, Background):
                            ent.move(self.player.current_speed)
                        elif ent != self.player:
                            ent.move()

            # Desenho
            self.window.fill((0, 0, 0))

            for ent in self.entity_list:
                if hasattr(ent, 'draw'):
                    ent.draw(self.window)
                else:
                    self.window.blit(ent.surf, ent.rect)

            if agora - self.timer_piscar > 500:
                self.mostrar_texto = not self.mostrar_texto
                self.timer_piscar = agora

            mostrar_go = self.corrida_iniciada and (agora - self.go_timer < 1000)

            if (not self.corrida_iniciada or mostrar_go) and self.mostrar_texto:
                texto_str = str(self.contagem_regressiva) if self.contagem_regressiva > 0 else "GO!"
                # Amarelo para os números, Verde para o GO!
                cor = (COR_AMARELA) if self.contagem_regressiva > 0 else (COR_VERDE)
                
                self.draw_text_with_outline(texto_str, cor, self.window.get_width()/2, self.window.get_height()/2)
            

            pygame.display.flip()
