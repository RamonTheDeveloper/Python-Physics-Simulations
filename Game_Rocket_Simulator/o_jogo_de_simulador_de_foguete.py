import pygame
import math
import random

# --- Configurações Iniciais ---
# Resolução padrão da janela
LARGURA_PADRAO, ALTURA_PADRAO = 900, 700
LARGURA, ALTURA = LARGURA_PADRAO, ALTURA_PADRAO
FPS = 60

# Cores (Visual SpaceX)
PRETO_ESPACO = (10, 10, 20)
BRANCO = (230, 230, 230)
PRETO_FOGUETE = (30, 30, 30)
CINZA_METAL = (150, 150, 160)
VERMELHO_FOGO = (255, 80, 20)
AMARELO_FOGO = (255, 220, 50)
VERDE_PAD = (50, 180, 50)
CINZA_LUA = (80, 80, 90)

# Física
GRAVIDADE = 0.05
FORCA_MOTOR = 0.16
CONSUMO_COMBUSTIVEL = 0.5
ROTACAO_VELOCIDADE = 2

pygame.init()
# Inicia como redimensionável
TELA = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
pygame.display.set_caption("SpaceX Lander Simulator")

FONTE = pygame.font.SysFont("Consolas", 18, bold=True)
FONTE_BIG = pygame.font.SysFont("Arial", 40, bold=True)

class Particula:
    def __init__(self, x, y, angulo_foguete, velocidade_extra=0):
        self.x = x
        self.y = y
        self.vida = random.randint(15, 35)
        
        rad = math.radians(angulo_foguete + 180 + random.uniform(-15, 15))
        velocidade = random.uniform(3, 7) + velocidade_extra
        
        self.vx = math.sin(rad) * velocidade
        self.vy = math.cos(rad) * velocidade
        
        if random.random() < 0.3:
             self.cor = (255, 255, 255) 
        else:
             self.cor = random.choice([VERMELHO_FOGO, AMARELO_FOGO])
        
        self.tamanho = random.randint(4, 10)

    def atualizar(self):
        self.x += self.vx
        self.y += self.vy
        self.vida -= 1
        self.tamanho *= 0.92 

    def desenhar(self, tela):
        if self.vida > 0:
            pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), int(self.tamanho))
            pygame.draw.circle(tela, (255,255,200), (int(self.x), int(self.y)), int(self.tamanho/2))

class Foguete:
    def __init__(self):
        self.largura = 18 
        self.altura = 85
        self.resetar()
        
        self.imagem_base = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        self._criar_design_foguete()

    def _criar_design_foguete(self):
        pygame.draw.rect(self.imagem_base, BRANCO, (0, 15, self.largura, self.altura - 20))
        pygame.draw.polygon(self.imagem_base, BRANCO, [(0, 15), (self.largura, 15), (self.largura/2, 0)])
        pygame.draw.rect(self.imagem_base, PRETO_FOGUETE, (0, 15, self.largura, 10))
        pygame.draw.line(self.imagem_base, CINZA_METAL, (2, self.altura-10), (2, self.altura-40), 3)
        pygame.draw.line(self.imagem_base, CINZA_METAL, (self.largura-2, self.altura-10), (self.largura-2, self.altura-40), 3)
        pygame.draw.rect(self.imagem_base, (40,40,40), (self.largura//4, self.altura-5, self.largura//2, 5))

    def resetar(self):
        # Centraliza baseado na largura atual da tela
        self.x = LARGURA // 2
        self.y = 100
        self.vx = 0
        self.vy = 0
        self.angulo = 0
        self.combustivel = 1200 
        self.ligado = False
        self.pousado = False
        self.explodiu = False
        self.particulas = []

    def aplicar_fisica(self):
        if self.pousado or self.explodiu: return

        self.vy += GRAVIDADE

        if self.ligado and self.combustivel > 0:
            self.combustivel -= CONSUMO_COMBUSTIVEL
            
            rad = math.radians(self.angulo)
            self.vx += math.sin(rad) * FORCA_MOTOR
            self.vy += -math.cos(rad) * FORCA_MOTOR
            
            base_x = self.x - math.sin(rad) * (self.altura/2)
            base_y = self.y + math.cos(rad) * (self.altura/2)
            
            for _ in range(5):
                self.particulas.append(Particula(base_x, base_y, self.angulo))

        self.x += self.vx
        self.y += self.vy
        
        for p in self.particulas:
            p.atualizar()
        self.particulas = [p for p in self.particulas if p.vida > 0]

    def checar_colisao(self, pad_x, pad_largura):
        if self.pousado or self.explodiu: return

        # O chão é sempre 50px do fundo da tela atual
        chao_y = ALTURA - 50
        rad = math.radians(self.angulo)
        base_y_rotacionada = self.y + math.cos(rad) * (self.altura/2)
        
        if base_y_rotacionada >= chao_y:
            velocidade_total = math.sqrt(self.vx**2 + self.vy**2)
            dentro_do_pad = pad_x < self.x < pad_x + pad_largura
            angulo_ok = -8 < self.angulo < 8 
            
            if velocidade_total < 5.0 and dentro_do_pad and angulo_ok:
                self.pousado = True
                self.vy = 0
                self.vx = 0
                self.y = chao_y - math.cos(rad)*(self.altura/2) 
            else:
                self.explodiu = True

        # Limites laterais e superior (se sair muito, explode)
        if self.x < -50 or self.x > LARGURA + 50 or self.y < -500 or self.y > ALTURA + 100:
            self.explodiu = True

    def desenhar(self, tela):
        for p in self.particulas:
            p.desenhar(tela)
            
        if self.explodiu:
            for i in range(5):
                raio = random.randint(20, 80)
                cor = random.choice([VERMELHO_FOGO, AMARELO_FOGO])
                offset_x = random.randint(-30, 30)
                offset_y = random.randint(-30, 30)
                pygame.draw.circle(tela, cor, (int(self.x+offset_x), int(self.y+offset_y)), raio)
            return

        imagem_final = self.imagem_base
        if self.pousado:
             imagem_final = self.imagem_base.copy()
             pygame.draw.line(imagem_final, CINZA_METAL, (2, self.altura-10), (-10, self.altura+5), 4)
             pygame.draw.line(imagem_final, CINZA_METAL, (self.largura-2, self.altura-10), (self.largura+10, self.altura+5), 4)

        imagem_rotacionada = pygame.transform.rotate(imagem_final, -self.angulo)
        rect_rotacionado = imagem_rotacionada.get_rect(center=(self.x, self.y))
        tela.blit(imagem_rotacionada, rect_rotacionado)

# --- SISTEMA DE TELA CHEIA E REDIMENSIONAMENTO ---

clock = pygame.time.Clock()
foguete = Foguete()
fullscreen = False
estrelas = []

def gerar_estrelas():
    """ Recria as estrelas para preencher a tela inteira """
    global estrelas
    estrelas = []
    # Quantidade baseada no tamanho da tela
    qtd = int((LARGURA * ALTURA) / 8000) 
    for _ in range(qtd):
        estrelas.append((random.randint(0, LARGURA), random.randint(0, ALTURA-50)))

gerar_estrelas()

executando = True
while executando:
    
    # 1. Eventos e Troca de Tela
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            executando = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                foguete.resetar()
            
            # LÓGICA DE TELA CHEIA (Tecla F)
            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    # Pega a resolução do monitor
                    info = pygame.display.Info()
                    LARGURA, ALTURA = info.current_w, info.current_h
                    TELA = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)
                else:
                    # Volta para janela padrão
                    LARGURA, ALTURA = LARGURA_PADRAO, ALTURA_PADRAO
                    TELA = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
                
                gerar_estrelas() # Redistribui estrelas
        
        # Se o usuário arrastar a borda da janela
        if event.type == pygame.VIDEORESIZE:
            if not fullscreen:
                LARGURA, ALTURA = event.w, event.h
                TELA = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
                gerar_estrelas()

    # 2. Atualizar Posição dos Elementos Dinâmicos
    # A plataforma deve sempre estar no meio e no fundo
    PAD_LARGURA = 140
    PAD_X = LARGURA // 2 - PAD_LARGURA // 2
    PAD_Y = ALTURA - 50

    # 3. Inputs
    teclas = pygame.key.get_pressed()
    if not foguete.pousado and not foguete.explodiu:
        if teclas[pygame.K_UP] or teclas[pygame.K_SPACE] or teclas[pygame.K_w]:
            foguete.ligado = True
        else:
            foguete.ligado = False
        
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]: foguete.angulo += ROTACAO_VELOCIDADE
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]: foguete.angulo -= ROTACAO_VELOCIDADE

    foguete.aplicar_fisica()
    foguete.checar_colisao(PAD_X, PAD_LARGURA)

    # 4. Desenho
    TELA.fill(PRETO_ESPACO)
    
    # Estrelas (COM EFEITO PISCA-PISCA)
    for ex, ey in estrelas:
        # Se a estrela estiver dentro da tela
        if ex < LARGURA and ey < ALTURA - 50:
            
            # TRUQUE RETRÔ: 
            # 1. Pequena chance (5%) da estrela não ser desenhada neste frame (ela "pula" um frame)
            # 2. Ou desenha com um brilho aleatório (cinza escuro a branco)
            
            if random.random() > 0.05: # 95% de chance de aparecer
                # Gera uma cor cinza aleatória entre 50 (escuro) e 255 (branco)
                brilho = random.randint(50, 255)
                pygame.draw.circle(TELA, (brilho, brilho, brilho), (ex, ey), 1)

    # Chão
    pygame.draw.rect(TELA, CINZA_LUA, (0, ALTURA - 50, LARGURA, 50))
    
    # Plataforma
    pygame.draw.rect(TELA, (30,30,30), (PAD_X-5, PAD_Y, PAD_LARGURA+10, 15))
    pygame.draw.rect(TELA, VERDE_PAD, (PAD_X, PAD_Y+2, PAD_LARGURA, 10))
    texto_pad = FONTE.render("SPACEX LANDING ZONE", True, (200, 255, 200))
    # Centraliza texto no pad
    TELA.blit(texto_pad, (PAD_X + (PAD_LARGURA - texto_pad.get_width())//2, PAD_Y + 20))

    foguete.desenhar(TELA)

    # 5. HUD (Painel Flutuante)
    vel_total = math.sqrt(foguete.vx**2 + foguete.vy**2) * 10
    altura_rel = (PAD_Y - foguete.y) / 10
    
    cor_vel = BRANCO
    if vel_total > 35: cor_vel = VERMELHO_FOGO
    elif vel_total < 5 and altura_rel < 5: cor_vel = VERDE_PAD

    cor_comb = BRANCO
    if foguete.combustivel < 250: cor_comb = VERMELHO_FOGO
    
    # Desenha o painel
    pygame.draw.rect(TELA, (20,20,30), (10, 10, 230, 95), border_radius=10)
    pygame.draw.rect(TELA, BRANCO, (10, 10, 230, 95), 2, border_radius=10)

    TELA.blit(FONTE.render(f"ALTITUDE  : {altura_rel:.1f} m", True, BRANCO), (20, 20))
    TELA.blit(FONTE.render(f"VELOCIDADE: {vel_total:.1f} km/h", True, cor_vel), (20, 40))
    
    # Barra de Combustível
    bar_width = int((foguete.combustivel / 1200) * 100)
    pygame.draw.rect(TELA, (50,50,50), (120, 65, 100, 15))
    pygame.draw.rect(TELA, cor_comb, (120, 65, bar_width, 15))
    TELA.blit(FONTE.render(f"FUEL:", True, cor_comb), (20, 63))
    TELA.blit(FONTE.render(f"ÂNGULO    : {foguete.angulo:.1f}°", True, BRANCO), (20, 80))

    # Mensagens de Centro de Tela
    if foguete.pousado:
        msg = FONTE_BIG.render("O FALCON POUSOU!", True, VERDE_PAD)
        # Centralização dinâmica
        TELA.blit(msg, (LARGURA//2 - msg.get_width()//2, ALTURA//2))
        msg2 = FONTE.render("Pressione 'R' para reiniciar", True, BRANCO)
        TELA.blit(msg2, (LARGURA//2 - msg2.get_width()//2, ALTURA//2 + 50))
        
    if foguete.explodiu:
        msg = FONTE_BIG.render("MISSÃO FALHOU", True, VERMELHO_FOGO)
        TELA.blit(msg, (LARGURA//2 - msg.get_width()//2, ALTURA//2))
        msg2 = FONTE.render("Pressione 'R' para tentar de novo", True, BRANCO)
        TELA.blit(msg2, (LARGURA//2 - msg2.get_width()//2, ALTURA//2 + 50))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()