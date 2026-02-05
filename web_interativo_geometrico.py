import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- FUNÇÕES PARA CRIAR OS SÓLIDOS (DATA) ---

def dados_cubo():
    # 8 Vértices (x, y, z)
    x = [-1, -1, 1, 1, -1, -1, 1, 1]
    y = [-1, 1, 1, -1, -1, 1, 1, -1]
    z = [-1, -1, -1, -1, 1, 1, 1, 1]
    
    # Índices (i, j, k) que formam os triângulos das faces
    # Cada face quadrada precisa de 2 triângulos
    i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2]
    j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3]
    k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6]
    
    return x, y, z, i, j, k

def dados_piramide():
    # Base Quadrada (4 pontos) + Ponta (1 ponto)
    # 0: (-1,-1,0), 1: (1,-1,0), 2: (1,1,0), 3: (-1,1,0), 4: (0,0,1.5)
    x = [-1, 1, 1, -1, 0]
    y = [-1, -1, 1, 1, 0]
    z = [0, 0, 0, 0, 1.5]
    
    # Faces: Base (2 triângulos) + 4 Laterais
    i = [0, 0,  0, 1, 2, 3]
    j = [1, 2,  1, 2, 3, 0]
    k = [2, 3,  4, 4, 4, 4]
    
    return x, y, z, i, j, k

def dados_prisma():
    # Triângulo Base (3 pontos) + Triângulo Topo (3 pontos)
    # Altura Z vai de 0 a 2
    x = [-1, 1, 0,   -1, 1, 0]
    y = [-1, -1, 1,  -1, -1, 1]
    z = [0, 0, 0,    2, 2, 2]
    
    # Faces: Base, Topo, e 3 Laterais Retangulares (2 triângulos cada)
    i = [0, 3,  0, 0, 1, 1, 2, 2]
    j = [1, 4,  1, 4, 2, 5, 0, 3]
    k = [2, 5,  3, 1, 4, 2, 3, 5]
    
    return x, y, z, i, j, k

# --- CONFIGURAÇÃO DA FIGURA ---

fig = make_subplots(
    rows=1, cols=3,
    specs=[[{'type': 'mesh3d'}, {'type': 'mesh3d'}, {'type': 'mesh3d'}]],
    subplot_titles=("Cubo", "Pirâmide Quadrada", "Prisma Triangular")
)

# 1. Cubo
xc, yc, zc, ic, jc, kc = dados_cubo()
fig.add_trace(
    go.Mesh3d(
        x=xc, y=yc, z=zc, i=ic, j=jc, k=kc,
        color='cyan', opacity=0.8, name='Cubo', flatshading=True
    ), row=1, col=1
)

# 2. Pirâmide
xp, yp, zp, ip, jp, kp = dados_piramide()
fig.add_trace(
    go.Mesh3d(
        x=xp, y=yp, z=zp, i=ip, j=jp, k=kp,
        color='orange', opacity=0.8, name='Pirâmide', flatshading=True
    ), row=1, col=2
)

# 3. Prisma
xpr, ypr, zpr, ipr, jpr, kpr = dados_prisma()
fig.add_trace(
    go.Mesh3d(
        x=xpr, y=ypr, z=zpr, i=ipr, j=jpr, k=kpr,
        color='mediumpurple', opacity=0.8, name='Prisma', flatshading=True
    ), row=1, col=3
)

# --- LAYOUT FINAL ---
fig.update_layout(
    title="Sólidos Geométricos Interativos (Plotly)",
    width=1200, height=600,
    scene =dict(aspectmode='data'),
    scene2=dict(aspectmode='data'),
    scene3=dict(aspectmode='data'),
    margin=dict(l=20, r=20, t=60, b=20)
)

fig.show()

# Para salvar:
# fig.write_html("geometria_solida.html")