import pygame
import math
import random

# --- Configurações ---
LARGURA, ALTURA = 800, 600
GRAVIDADE = 0.25
RAIO_PARTICULA = 6
NUM_PARTICULAS = 450

COR_FUNDO = (10, 10, 20)
COR_AGUA = (50, 150, 255)
COR_BRILHO = (200, 230, 255)

# Física simplificada de fluidos
AMORTECIMENTO = 0.7  # Perda de energia ao bater na parede
PRESSAO_FORCA = 2.5  # O quanto as partículas se empurram
RAIO_INTERACAO = 25  # Distância que uma partícula "sente" a outra

class Particula:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.cor = COR_AGUA

    def aplicar_fisica(self, particulas):
        # 1. Gravidade
        self.vy += GRAVIDADE
        
        # 2. Movimento
        self.x += self.vx
        self.y += self.vy
        
        # 3. Colisão com Paredes (Caixa de Vidro)
        margem = RAIO_PARTICULA
        
        # Chão
        if self.y > ALTURA - margem:
            self.y = ALTURA - margem
            self.vy *= -AMORTECIMENTO
            self.vx *= 0.95 # Atrito no chão
            
        # Teto
        if self.y < margem:
            self.y = margem
            self.vy *= -AMORTECIMENTO
            
        # Paredes laterais
        if self.x > LARGURA - margem:
            self.x = LARGURA - margem
            self.vx *= -AMORTECIMENTO
        elif self.x < margem:
            self.x = margem
            self.vx *= -AMORTECIMENTO

        # 4. Interação Mouse (Repulsão/Agitação)
        mx, my = pygame.mouse.get_pos()
        botoes = pygame.mouse.get_pressed()
        
        if botoes[0]: # Botão Esquerdo Pressionado
            dx = self.x - mx
            dy = self.y - my
            dist = math.sqrt(dx*dx + dy*dy)
            
            # Se o mouse estiver perto, empurra a água (efeito de mão na piscina)
            if dist < 80 and dist > 0:
                forca = (80 - dist) / 80
                self.vx += (dx / dist) * forca * 2.0
                self.vy += (dy / dist) * forca * 2.0

def resolver_colisoes_fluido(particulas):
    """
    O segredo da água: Partículas não podem ocupar o mesmo espaço.
    Se estiverem muito perto, elas se empurram (Pressão).
    """
      
    for i in range(len(particulas)):
        p1 = particulas[i]
        
        for j in range(i + 1, len(particulas)):
            p2 = particulas[j]
            
            dx = p1.x - p2.x
            dy = p1.y - p2.y
            dist_sq = dx*dx + dy*dy
            
            # Se estiverem dentro do raio de interação (quase tocando)
            raio_minimo = RAIO_INTERACAO
            if dist_sq < raio_minimo * raio_minimo and dist_sq > 0:
                dist = math.sqrt(dist_sq)
                
                # Força de repulsão baseada na sobreposição
                # Quanto mais perto, mais forte o empurrão
                sobreposicao = (raio_minimo - dist) / 2.0
                forca = sobreposicao * 0.1 # Fator de suavidade
                
                move_x = (dx / dist) * forca
                move_y = (dy / dist) * forca
                
                # Afasta as duas
                p1.x += move_x
                p1.y += move_y
                p1.vx += move_x * PRESSAO_FORCA
                p1.vy += move_y * PRESSAO_FORCA
                
                p2.x -= move_x
                p2.y -= move_y
                p2.vx -= move_x * PRESSAO_FORCA
                p2.vy -= move_y * PRESSAO_FORCA

# --- Setup ---
pygame.init()
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Simulador de Fluidos")

particulas = []
for _ in range(NUM_PARTICULAS):
    # Começam no meio da tela caindo
    p = Particula(random.randint(300, 500), random.randint(100, 300))
    particulas.append(p)

relogio = pygame.time.Clock()
executando = True

font = pygame.font.SysFont('Arial', 14)

while executando:
    TELA.fill(COR_FUNDO)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
                particulas = []
                for _ in range(NUM_PARTICULAS):
                    p = Particula(random.randint(300, 500), random.randint(50, 200))
                    particulas.append(p)

    # --- Lógica Física ---
    
    # 1. Movimento individual
    for p in particulas:
        p.aplicar_fisica(particulas)
    
    # 2. Resolver pressão entre elas (O que faz parecer água)
    resolver_colisoes_fluido(particulas)
    
    # --- Desenho ---
    
    for p in particulas:
        # Bolinha principal
        pygame.draw.circle(TELA, COR_AGUA, (int(p.x), int(p.y)), RAIO_PARTICULA)
        # Brilho (Reflexo)
        pygame.draw.circle(TELA, COR_BRILHO, (int(p.x - 2), int(p.y - 2)), 2)

    # Texto
    info = font.render(f"Partículas: {NUM_PARTICULAS} | Mouse: Agitar Água | 'R': Resetar", True, (150, 150, 150))
    TELA.blit(info, (10, 10))

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()