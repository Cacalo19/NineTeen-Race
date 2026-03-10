import random 

import pygame

from code.Score import Score
from code.Traffic import Traffic
from code.Background import Background
from code.EntityFactory import EntityFactory
from code.Constante import COR_AMARELA, COR_VERDE, COR_PRETA, FONTE_PERSONALIZADA, DESLOCAMENTO_BORDA, WINDOW_WIDTH

class Level: # Classe responsável por carregar o jogador, o cenário e gerenciar a lógica da corrida, como o HUD e a contagem regressiva.
    def __init__(self, window, name):
        self.window = window
        self.name = name

        # Entidades - Cria a lista de objetos do jogo e spawna o Player e o Fundo.
        self.lista_entidades = []
        self.player = EntityFactory.get_entity('Player', ((WINDOW_WIDTH // 2) - 100, 950)) # Teste        
        self.fundo = EntityFactory.get_entity('Level1', (0, 0))

        # Adiciona o fundo e o jogador na lista de processamento
        if self.fundo: 
            self.lista_entidades.append(self.fundo)
        if self.player: 
            self.lista_entidades.append(self.player)
        
        # Estado do Jogo - Variáveis para controlar o início da corrida (3, 2, 1... GO!)
        self.contagem_regressiva = 3
        self.go_timer = 0
        self.timer_iniciar = pygame.time.get_ticks()
        self.corrida_iniciada = False
        self.pausado = False

        # Controle visual para textos que piscam na tela
        self.mostrar_texto = True
        self.timer_piscar = pygame.time.get_ticks()

        # Gerenciamento de pontuação e recordes
        self.recordes = 0
        self.pontuacao = 0
        self.recorde_atual = Score.get_high_score()

        self.fonte_hud = pygame.font.SysFont('Arial', 30, bold=True) # Teste

        # Configuração das fontes
        try:
            self.fonte_contagem = pygame.font.Font(FONTE_PERSONALIZADA , 80)
        except:
            self.fonte_contagem = pygame.font.SysFont('Arial', 80, bold=True)

        # Audio - Gerenciamento do tempo de surgimento (spawn) de novos carros
        self.som_contagem = pygame.mixer.Sound('./asset/som/countdown.ogg')
        pygame.mixer_music.load('./asset/som/neon_sign_circuit_bpm145.ogg')

        self.som_explosao = pygame.mixer.Sound('./asset/som/mechanical_explosion.wav')
        self.som_explosao.set_volume(0.8)
        
        # Gerenciamento do tempo de surgimento (spawn) de novos carros
        self.timer_spawn = pygame.time.get_ticks() # Teste
        self.spawn_delay = 1000      

        # Carrega e escala as imagens para a animação de explosão
        self.frame_explosao = []
        for i in range(1, 7):
            explosao_gif = pygame.image.load(f'./asset/imagem/explosion{i}.png').convert_alpha()
            explosao_gif = pygame.transform.scale(explosao_gif, (150, 150))
            self.frame_explosao.append(explosao_gif)  
        
    def draw_text_with_outline(self, text, color, x, y):
        # Desenha a borda do texto primeiro (cor preta).
        cor_borda = (COR_PRETA)
        deslocamentos = (DESLOCAMENTO_BORDA)

        # Desenha o texto várias vezes com pequenos desvios para criar o contorno.
        for ox, oy in deslocamentos:
            surf_borda = self.fonte_contagem.render(text, True, cor_borda)
            rect_borda = surf_borda.get_rect(center=(x + ox, y + oy))
            self.window.blit(surf_borda, rect_borda)

        # Desenha o texto colorido por cima da borda
        text_surf = self.fonte_contagem.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))
        self.window.blit(text_surf, text_rect)

    def draw_hud(self):
        # Renderiza e desenha a pontuação atual no canto superior esquerdo.
        texto_surf = self.fonte_hud.render(f"PONTOS: {self.recordes}", True, (255,255,255))
        self.window.blit(texto_surf, (20, 20)) 

        # Pega o valor do primeiro colocado na lista de recordes (se existir).
        melhor_valor = self.recorde_atual[0][1] if self.recorde_atual else 0

        # Renderiza e desenha o recorde global logo abaixo da pontuação atual.
        rec_surf = self.fonte_hud.render(f"RECORDE: {melhor_valor}", True, (255,215,0))
        self.window.blit(rec_surf, (20, 60))

    def draw(self):
        # Desenha o fundo e os carros da CPU primeiro (camadas de baixo).
        for ent in self.lista_entidades:
            # Se for o player, pulamos para desenhar por último (camada de cima).
            if ent == self.player:
                continue

            # Tenta pegar .surf (usado no Background) ou .image (usado no Traffic/Player).
            img = getattr(ent, 'surf', getattr(ent, 'image', None))
            
            if img:
                self.window.blit(img, ent.rect)

        # Desenha o Player por último para ele nunca ficar "atrás" de outro carro
        if self.player:
            # Se houver uma batida, a imagem aqui será trocada pelos frames da explosão
            self.window.blit(self.player.image, self.player.rect)

        # Desenha o HUD (texto de pontos/recorde) no topo de absolutamente tudo
        self.draw_hud()

    def run(self, ):
        clock = pygame.time.Clock()
        self.som_contagem.play()

        while True:
            clock.tick(60) # Mantém o jogo rodando a 60 quadros por segundo.
            agora = pygame.time.get_ticks()

            # Lógica para tocar a música tema apenas 1 segundo após o "GO!".
            if self.corrida_iniciada and not pygame.mixer.music.get_busy() and not self.pausado:
                if agora - self.go_timer >= 1000:
                    pygame.mixer.music.play(-1)

            # Captura de Eventos (Teclado e Fechamento de Janela).
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    # Sistema de Pausa usando a tecla ESC.
                    if event.key == pygame.K_ESCAPE:
                        self.pausado = not self.pausado # Inverte o estado de pausa.
                        if self.pausado:
                            pygame.mixer.music.pause() # Pausa a música de fundo.
                            pygame.mixer.pause() # Pausa todos os canais de som (motor, etc).
                        else:
                            pygame.mixer.music.unpause()
                            pygame.mixer.unpause()
                            # Reseta o timer para evitar que a contagem regr. pule números ao despausar.
                            self.timer_iniciar = pygame.time.get_ticks()

            # --- LÓGICA DO JOGO (MOVIMENTO E COLISÃO) ---
            if not self.pausado:

                # Gerencia o "3, 2, 1" antes de liberar o movimento do carro.
                if not self.corrida_iniciada:
                    if agora - self.timer_iniciar >= 1000:
                        self.contagem_regressiva -= 1
                        self.timer_iniciar = agora

                        if self.contagem_regressiva == 0:
                            self.corrida_iniciada = True
                            self.go_timer = agora

                # Se a corrida começou, permite que o jogador controle o carro   .        
                if self.corrida_iniciada and self.player:
                    self.player.move()

                    # Cria uma lista apenas com os carros da CPU para a IA processar.
                    lista_trafego = [e for e in self.lista_entidades if isinstance(e, Traffic)]
                    
                    # Processa movimento, IA, pontuação e limpeza de memória em um único loop.
                    nova_lista = []
                    for ent in self.lista_entidades:
                        if isinstance(ent, (Background, Traffic)):
                            # Move fundo e inimigos com base na velocidade do player.
                            ent.move(self.player.velocidade_atual)
                            
                            if isinstance(ent, Traffic):
                                # Faz a IA desviar de outros carros.
                                if agora % 2 == 0:
                                    ent.detectar_e_desviar(lista_trafego)
                                
                                # SISTEMA DE PONTOS: Ganha 10 pontos ao ultrapassar um carro (quando ele sai da tela).
                                if ent.rect.y >= 1200:
                                    self.recordes += 10
                                    continue # Remove o carro da lista para economizar memória.
                        else:
                            # Move outras entidades que não dependem da velocidade da pista.
                            if ent != self.player: 
                                ent.move()

                        nova_lista.append(ent)
                    # Atualiza a lista oficial apenas com as entidades que ainda estão ativas.
                    self.lista_entidades = nova_lista

                    # --- LÓGICA DE DIFICULDADE (AJUSTE DINÂMICO) ---
                    if self.recordes > 1500:
                        self.spawn_delay = 200 # Nível hard: um carro novo quase a cada 0.2 segundos
                    elif self.recordes > 1000:
                        self.spawn_delay = 300
                    elif self.recordes > 600:
                        self.spawn_delay = 450
                    elif self.recordes > 300:
                        self.spawn_delay = 600
                    elif self.recordes > 100:
                        self.spawn_delay = 800
                    else:
                        self.spawn_delay = 1000 # Nível inicial: um carro novo a cada 1 segundo

                    # --- LÓGICA SPAWN DE VEÍCULOS ---.
                    if self.corrida_iniciada:
                        # Verifica se já passou o tempo necessário (delay) para criar um novo carro.
                        if agora - self.timer_spawn > self.spawn_delay:

                            # Filtra a lista para saber quantos carros já existem na pista.
                            carros = [e for e in self.lista_entidades if isinstance(e, Traffic)]

                            # Limita a quantidade de carros para não travar o jogo ou ficar impossível.
                            if len(carros) < 15:
                                # Sorteio para decidir o tipo de carro (30% de chance de ser polícia).
                                chance = random.randint(1, 10)
                                if chance <= 3:
                                    tipo_sorteado = 'carro-policia'
                                else:
                                    tipo_sorteado = random.choice(['carro-emergencia', 'carro-lento', 'carro-padrao', 'carro-esportivo'])
                                
                                novo_inimigo = None

                                # Tenta posicionar o carro até 3 vezes (evita que um nasça em cima do outro).
                                for _ in range(3):
                                    novo_inimigo = EntityFactory.get_entity(tipo_sorteado,(0, -200))
                                    if novo_inimigo:
                                        break

                                if novo_inimigo:
                                    self.lista_entidades.append(novo_inimigo)

                                    # Lógica se for polícia, cria um "carro-preso" logo à frente dela.
                                    if tipo_sorteado == 'carro-policia':
                                        x = novo_inimigo.rect.x
                                        y = novo_inimigo.rect.y - 120

                                        carro_preso = EntityFactory.get_entity('carro-preso',(x, y),self.lista_entidades)

                                        if carro_preso:
                                            self.lista_entidades.append(carro_preso)

                                    # Chance de 35% de criar um segundo carro ao mesmo tempo (engarrafamento).
                                    if random.random() < 0.35:
                                        segundo = EntityFactory.get_entity(
                                            random.choice(['carro-lento','carro-padrao']),(0, -300),self.lista_entidades)
                                        if segundo:
                                            self.lista_entidades.append(segundo)

                            # Reseta o cronômetro de spawn
                            self.timer_spawn = agora
  
                    # --- CHECAR COLISÃO ---
                    if self.player.detectar_colisoes(self.lista_entidades):
                        # --- SEQUÊNCIA DE ANIMAÇÃO DA EXPLOSÃO ---
                        self.corrida_iniciada = False  # Para o movimento do cenário.
                        self.player.canal_motor.stop() 
                        
                        # Toca o som da explosão e salva a posição exata da batida.
                        self.som_explosao.play() 
                        posicao_da_batida = self.player.rect.center

                        # --- SEQUÊNCIA DE ANIMAÇÃO DA EXPLOSÃO ---
                        for frame in self.frame_explosao:
                            # Troca a imagem do player pelo frame da lista
                            self.player.image = frame
                            
                            # Garante que a explosão fique centralizada onde o carro bateu.
                            self.player.rect = self.player.image.get_rect(center=posicao_da_batida)
                            
                            # 3. Desenha a cena e atualiza a tela
                            self.draw() 
                            pygame.display.flip()
                            pygame.time.delay(100)

                        # Pausa para o jogador vê a explosão antes de a tela fechar
                        pygame.time.delay(2000)
                        print(f"GAME OVER! Score Final: {self.recordes}")
                        # Encerra a música e retorna a pontuação para o sistema de Recordes
                        pygame.mixer.music.stop()
                        return self.recordes                  
                
            # --- DESENHO (RENDERIZAÇÃO) ---
            self.window.fill((0, 0, 0))

            # Desenha todas as entidades da lista
            for ent in self.lista_entidades:
                if hasattr(ent, 'draw'):
                    ent.draw(self.window)
                else:
                    self.window.blit(ent.image, ent.rect)

            self.draw_hud()

            # Efeito visual de texto piscante
            if agora - self.timer_piscar > 500:
                self.mostrar_texto = not self.mostrar_texto
                self.timer_piscar = agora

            # Desenha Contagem Regressiva e "GO!"
            mostrar_go = self.corrida_iniciada and (agora - self.go_timer < 1000)

            if (not self.corrida_iniciada or mostrar_go) and self.mostrar_texto:
                texto_str = str(self.contagem_regressiva) if self.contagem_regressiva > 0 else "GO!"
                # Amarelo para os números, Verde para o GO!
                cor = (COR_AMARELA) if self.contagem_regressiva > 0 else (COR_VERDE)
                
                self.draw_text_with_outline(texto_str, cor, self.window.get_width()/2, self.window.get_height()/2)
            
            # --- TELA DE PAUSE ---
            if self.pausado:

                overlay = pygame.Surface(self.window.get_size(), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                self.window.blit(overlay, (0, 0))
                
                self.draw_text_with_outline("PAUSADO", (255, 255, 255), self.window.get_width()/2, self.window.get_height()/2)

            pygame.display.flip()