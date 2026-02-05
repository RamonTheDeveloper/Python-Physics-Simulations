import pygame
import math

# --- Configurações ---
LARGURA, ALTURA = 800, 600
GRAVIDADE = 0.5
ATRITO = 0.99
RIGIDEZ = 4        
ESPACAMENTO = 16   
LINHAS = 25
COLUNAS = 40

COR_FUNDO = (20, 20, 25)
COR_TECIDO = (200, 200, 255)
COR_CORTE = (255, 50, 50)

class Ponto:
    def __init__(self, x, y, fixo=False):
        self.x = x
        self.y = y
        self.px = x # Posição anterior (Previous X)
        self.py = y # Posição anterior (Previous Y)
        self.fixo = fixo

    def atualizar(self):
        if self.fixo: return
        
        # Física de Verlet: A velocidade é a diferença entre onde estou e onde estava
        vx = (self.x - self.px) * ATRITO
        vy = (self.y - self.py) * ATRITO

        self.px = self.x
        self.py = self.y

        self.x += vx
        self.y += vy + GRAVIDADE
        
        # Limites da tela (chão e paredes)
        if self.y > ALTURA - 5: 
            self.y = ALTURA - 5
            self.py = self.y # Tira a velocidade ao bater (kinda)
        if self.x < 0: self.x = 0
        if self.x > LARGURA: self.x = LARGURA

class Conexao:
    def __init__(self, p1, p2, distancia):
        self.p1 = p1
        self.p2 = p2
        self.distancia = distancia
        self.ativa = True

    def resolver(self):
        if not self.ativa: return
        
        # Distância atual entre os pontos
        dx = self.p1.x - self.p2.x
        dy = self.p1.y - self.p2.y
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist == 0: return # Evita divisão por zero

        # Diferença do que deveria ser (Lei de Hooke simplificada)
        diferenca = (self.distancia - dist) / dist
        
        # Quanto cada um deve se mover para corrigir (metade pra cada)
        correcao_x = dx * diferenca * 0.5
        correcao_y = dy * diferenca * 0.5

        if not self.p1.fixo:
            self.p1.x += correcao_x
            self.p1.y += correcao_y
        if not self.p2.fixo:
            self.p2.x -= correcao_x
            self.p2.y -= correcao_y

# --- Setup da Simulação ---
pygame.init()
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Simulador de Tecido (Verlet Integration)")

pontos = []
conexoes = []

# Criar a grade de pontos
for y in range(LINHAS):
    for x in range(COLUNAS):
        # Fixar apenas a primeira linha (o varão da cortina)
        fixo = (y == 0) and (x % 3 == 0) # Prende a cada 3 pontos pra ficar soltinho
        p = Ponto(x * ESPACAMENTO + 100, y * ESPACAMENTO + 50, fixo)
        pontos.append(p)

# Criar as conexões (Sticks)
def conectar(i1, i2):
    p1 = pontos[i1]
    p2 = pontos[i2]
    dist = math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
    conexoes.append(Conexao(p1, p2, dist))

for y in range(LINHAS):
    for x in range(COLUNAS):
        i = y * COLUNAS + x
        if x < COLUNAS - 1: conectar(i, i + 1) # Conexão Horizontal
        if y < LINHAS - 1: conectar(i, i + COLUNAS) # Conexão Vertical

relogio = pygame.time.Clock()
executando = True

while executando:
    TELA.fill(COR_FUNDO)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        
        # Reiniciar com 'R'
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
                pass

    # --- FÍSICA ---
    # 1. Atualizar Pontos (Gravidade e Inércia)
    for p in pontos:
        p.atualizar()
        
        # Interação: Mouse Esquerdo empurra/arrasta (Vento local)
        if mouse_click[0]:
            dx = p.x - mouse_x
            dy = p.y - mouse_y
            dist_sq = dx*dx + dy*dy
            if dist_sq < 2500: # Raio de efeito
                # Empurra suavemente
                p.px = p.x - (dx * 0.05) # Gambiarra de Verlet pra dar velocidade
                p.py = p.y - (dy * 0.05) 

    # 2. Resolver Conexões (Tensionar o tecido)
    for _ in range(RIGIDEZ):
        for c in conexoes:
            c.resolver()

    # 3. Rasgar Tecido (Botão Direito)
    if mouse_click[2]: # Botão Direito
        pygame.draw.circle(TELA, COR_CORTE, (mouse_x, mouse_y), 15, 1)
        # Remove conexões que o mouse tocar
        for c in conexoes:
            if c.ativa:
                # Checagem simples: se o centro da linha estiver perto do mouse
                cx = (c.p1.x + c.p2.x) / 2
                cy = (c.p1.y + c.p2.y) / 2
                if (cx - mouse_x)**2 + (cy - mouse_y)**2 < 400:
                    c.ativa = False

    # --- DESENHO ---
    for c in conexoes:
        if c.ativa:
            # Cor baseada na tensão (opcional, está estático pra performance)
            pygame.draw.line(TELA, COR_TECIDO, (c.p1.x, c.p1.y), (c.p2.x, c.p2.y), 1)

    # UI
    font = pygame.font.SysFont('Arial', 14)
    info = font.render("Esq: Empurrar | Dir: Rasgar/Cortar", True, (150, 150, 150))
    TELA.blit(info, (10, 10))

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()