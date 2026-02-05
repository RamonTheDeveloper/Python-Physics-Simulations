import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# --- FUNÇÕES GERADORAS DE FORMAS ---

def get_cubo():
    v = np.array([
        [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
        [-1, -1, 1],  [1, -1, 1],  [1, 1, 1],  [-1, 1, 1]
    ])
    a = [
        (0,1), (1,2), (2,3), (3,0), # Base
        (4,5), (5,6), (6,7), (7,4), # Topo
        (0,4), (1,5), (2,6), (3,7)  # Laterais
    ]
    return v, a, 80 # Retorna vértices, arestas e tamanho da bolinha

def get_piramide():
    v = np.array([
        [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1], # Base
        [0, 0, 1] # Ponta (Ápice)
    ])
    a = [
        (0,1), (1,2), (2,3), (3,0), # Quadrado da base
        (0,4), (1,4), (2,4), (3,4)  # Laterais subindo
    ]
    return v, a, 80

def get_octaedro(): # O "Diamante"
    v = np.array([
        [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], # Meio
        [0, 0, 1], [0, 0, -1] # Pontas Cima/Baixo
    ])
    a = [
        (0,2), (2,1), (1,3), (3,0), # Cintura
        (0,4), (2,4), (1,4), (3,4), # Cima
        (0,5), (2,5), (1,5), (3,5)  # Baixo
    ]
    return v, a, 80

def get_esfera(raio=1.5, divisoes=12):
    lista_v = []
    lista_a = []
    # Matemática: Coordenadas Esféricas
    for i in range(divisoes + 1):
        lat = np.pi * i / divisoes
        for j in range(divisoes):
            lon = 2 * np.pi * j / divisoes
            x = raio * np.sin(lat) * np.cos(lon)
            y = raio * np.sin(lat) * np.sin(lon)
            z = raio * np.cos(lat)
            lista_v.append([x, y, z])
            
    num_pts = len(lista_v)
    for i in range(num_pts):
        if (i + 1) % divisoes != 0: lista_a.append((i, i + 1))
        else: lista_a.append((i, i - divisoes + 1))
        if i + divisoes < num_pts: lista_a.append((i, i + divisoes))
            
    return np.array(lista_v), lista_a, 20 # Bolinha menor pra não poluir

def get_toro(R=1.5, r=0.5, divisoes=15): # O "Donut"
    lista_v = []
    lista_a = []
    for i in range(divisoes):
        theta = 2 * np.pi * i / divisoes
        for j in range(divisoes):
            phi = 2 * np.pi * j / divisoes
            # Matemática do Toro
            x = (R + r * np.cos(theta)) * np.cos(phi)
            y = (R + r * np.cos(theta)) * np.sin(phi)
            z = r * np.sin(theta)
            lista_v.append([x, y, z])
    
    num_pts = len(lista_v)
    for i in range(num_pts):
        lista_a.append((i, (i + 1) % num_pts)) # Ligações simples
        lista_a.append((i, (i + divisoes) % num_pts))

    return np.array(lista_v), lista_a, 15

# --- MENU DE SELEÇÃO ---
print("="*30)
print("VISUALIZADOR 3D MATEMÁTICO")
print("="*30)
print("1. Cubo")
print("2. Pirâmide")
print("3. Octaedro (Diamante)")
print("4. Esfera")
print("5. Toro (Donut)")
print("="*30)

opcao = input("Escolha o número da forma: ")

# Define a forma baseada na escolha
if opcao == '1': vertices, arestas, tam_ponto = get_cubo()
elif opcao == '2': vertices, arestas, tam_ponto = get_piramide()
elif opcao == '3': vertices, arestas, tam_ponto = get_octaedro()
elif opcao == '4': vertices, arestas, tam_ponto = get_esfera()
elif opcao == '5': vertices, arestas, tam_ponto = get_toro()
else: 
    print("Opção inválida! Carregando Cubo padrão.")
    vertices, arestas, tam_ponto = get_cubo()

# --- LÓGICA DE ROTAÇÃO E ANIMAÇÃO ---

def rotacionar(pontos, angulo):
    c, s = np.cos(angulo), np.sin(angulo)
    Rx = np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    Ry = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    Rz = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    
    # Ordem: Z -> Y -> X
    R = Rz @ Ry @ Rx 
    return pontos @ R.T

fig = plt.figure(figsize=(9,9), facecolor='black')
ax = fig.add_subplot(111, projection='3d', facecolor='black')
ax.set_box_aspect([1,1,1])

def init():
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.axis('off')
    return []

def update(frame):
    ax.cla()
    ax.set_xlim(-2, 2); ax.set_ylim(-2, 2); ax.set_zlim(-2, 2)
    ax.axis('off')
    
    # Rotação suave
    ang = frame * 0.02
    verts_rot = rotacionar(vertices, ang)
    
    # Desenha as linhas (Arestas)
    for i, j in arestas:
        # Garante que os índices existem (segurança para formas complexas)
        if i < len(verts_rot) and j < len(verts_rot):
            cor = plt.cm.hsv((frame % 200)/200)  # Efeito Arco-íris
            ax.plot(verts_rot[[i,j], 0], verts_rot[[i,j], 1], verts_rot[[i,j], 2],
                    color=cor, lw=2, alpha=0.8)
    
    # Desenha os pontos (Vértices)
    ax.scatter(verts_rot[:,0], verts_rot[:,1], verts_rot[:,2],
               color='white', s=tam_ponto, edgecolor='lime', zorder=10)
    
    return []

ani = FuncAnimation(fig, update, frames=360, init_func=init, interval=30, blit=False)
plt.show()