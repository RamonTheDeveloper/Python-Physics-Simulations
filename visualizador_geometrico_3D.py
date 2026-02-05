import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# --- FUNÇÕES GERADORAS DE FORMAS GEOMÉTRICAS ---

def get_cubo():
    # 8 Vértices do cubo
    v = np.array([
        [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
        [-1, -1, 1],  [1, -1, 1],  [1, 1, 1],  [-1, 1, 1]
    ])
    # 12 Arestas conectando os índices
    a = [
        (0,1), (1,2), (2,3), (3,0), # Base
        (4,5), (5,6), (6,7), (7,4), # Topo
        (0,4), (1,5), (2,6), (3,7)  # Colunas laterais
    ]
    return v, a, 80 # Retorna vértices, arestas e tamanho do ponto

def get_piramide_quadrada():
    # 5 Vértices: base quadrada e um topo
    v = np.array([
        [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1], # Base z=-1
        [0, 0, 1] # Ponta (Ápice) z=1
    ])
    # 8 Arestas
    a = [
        (0,1), (1,2), (2,3), (3,0), # Quadrado da base
        (0,4), (1,4), (2,4), (3,4)  # Laterais subindo ao topo
    ]
    return v, a, 80

def get_octaedro(): # O "Diamante"
    # 6 Vértices (Sólido de Platão)
    v = np.array([
        [1, 0, 0], [-1, 0, 0], # Eixo X
        [0, 1, 0], [0, -1, 0], # Eixo Y
        [0, 0, 1], [0, 0, -1]  # Eixo Z (Pontas Cima/Baixo)
    ])
    # 12 Arestas
    a = [
        (0,2), (2,1), (1,3), (3,0), # "Cintura" quadrada do meio
        (0,4), (2,4), (1,4), (3,4), # Conexões para cima
        (0,5), (2,5), (1,5), (3,5)  # Conexões para baixo
    ]
    return v, a, 80

# --- NOVAS FORMAS ---

def get_tetraedro():
    # O sólido mais simples (4 faces triangulares)
    # Coordenadas para um tetraedro regular centrado
    v = np.array([
        [1, 1, 1],
        [1, -1, -1],
        [-1, 1, -1],
        [-1, -1, 1]
    ])
    # 6 Arestas (liga todo mundo com todo mundo)
    a = [
        (0,1), (0,2), (0,3),
        (1,2), (1,3),
        (2,3)
    ]
    return v, a, 100 # Pontos um pouco maiores

def get_prisma_triangular():
    # Base triangular em z=-1 e topo triangular em z=1
    # Usando trig para fazer um triângulo equilátero
    h = np.sqrt(3)/2 # Altura do triângulo
    v = np.array([
        # Triângulo Base (z=-1)
        [-1, -h/3, -1], [1, -h/3, -1], [0, 2*h/3, -1],
        # Triângulo Topo (z=1)
        [-1, -h/3, 1],  [1, -h/3, 1],  [0, 2*h/3, 1]
    ])
    # 9 Arestas
    a = [
        (0,1), (1,2), (2,0), # Base
        (3,4), (4,5), (5,3), # Topo
        (0,3), (1,4), (2,5)  # Colunas verticais
    ]
    return v, a, 80

# --- MENU DE SELEÇÃO ---
print("="*30)
print("VISUALIZADOR GEOMÉTRICO 3D")
print("="*30)
print("Sólidos Básicos:")
print("1. Cubo (Hexaedro)")
print("2. Pirâmide de Base Quadrada")
print("3. Prisma Triangular")
print("-" * 20)
print("Sólidos de Platão (Regulares):")
print("4. Tetraedro (4 faces)")
print("5. Octaedro (8 faces)")
print("="*30)

opcao = input("Escolha o número da forma: ")

# Define a forma baseada na escolha
if opcao == '1': vertices, arestas, tam_ponto = get_cubo()
elif opcao == '2': vertices, arestas, tam_ponto = get_piramide_quadrada()
elif opcao == '3': vertices, arestas, tam_ponto = get_prisma_triangular()
elif opcao == '4': vertices, arestas, tam_ponto = get_tetraedro()
elif opcao == '5': vertices, arestas, tam_ponto = get_octaedro()
else: 
    print("Opção inválida! Carregando Cubo padrão.")
    vertices, arestas, tam_ponto = get_cubo()

# --- LÓGICA DE ROTAÇÃO E ANIMAÇÃO (MATEMÁTICA PURA) ---

def rotacionar(pontos, angulo):
    c, s = np.cos(angulo), np.sin(angulo)
    # Matrizes de rotação em torno dos eixos X, Y, Z
    Rx = np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    Ry = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    Rz = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    
    # Multiplica as matrizes para uma rotação complexa (Z -> Y -> X)
    R = Rz @ Ry @ Rx 
    # Aplica a rotação aos pontos (multiplicação de matrizes)
    return pontos @ R.T

fig = plt.figure(figsize=(8,8), facecolor='black')
ax = fig.add_subplot(111, projection='3d', facecolor='black')
ax.set_box_aspect([1,1,1]) # Garante que não fique esticado

def init():
    # Configura limites para a câmera não ficar "pulando"
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.axis('off') # Esconde os eixos numéricos
    return []

def update(frame):
    ax.cla() # Limpa a tela anterior
    init() # Re-aplica os limites e esconde eixos
    
    # Calcula o ângulo atual baseado no frame da animação
    ang = frame * 0.02 
    
    # A rotação das vértices
    verts_rot = rotacionar(vertices, ang)
    
    # 1. Desenha as LINHAS (Arestas) conectando os pontos rotacionados
    for i, j in arestas:
        # Cor muda com o tempo usando mapa de cores HSV (arco-íris)
        cor = plt.cm.hsv((frame % 240)/240)
        # Plota a linha entre o ponto i e o ponto j
        ax.plot(verts_rot[[i,j], 0], verts_rot[[i,j], 1], verts_rot[[i,j], 2],
                color=cor, lw=3, alpha=0.9)
    
    # 2. Desenha os PONTOS (Vértices) nas novas posições
    ax.scatter(verts_rot[:,0], verts_rot[:,1], verts_rot[:,2],
               color='white', s=tam_ponto, edgecolor='cyan', linewidth=1.5, zorder=10)
    
    return []

# Cria a animação
ani = FuncAnimation(fig, update, frames=360, init_func=init, interval=30, blit=False)
plt.show()