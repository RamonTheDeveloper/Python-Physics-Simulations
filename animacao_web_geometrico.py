import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# --- FUNÇÕES PARA GERAR OS SÓLIDOS (Vértices e Faces) ---

def dados_cubo():
    # 8 Vértices (x, y, z)
    x = np.array([-1, -1, 1, 1, -1, -1, 1, 1])
    y = np.array([-1, 1, 1, -1, -1, 1, 1, -1])
    z = np.array([-1, -1, -1, -1, 1, 1, 1, 1])
    # Índices dos triângulos das faces
    i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2]
    j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3]
    k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6]
    return x, y, z, i, j, k

def dados_piramide():
    # 5 Vértices
    x = np.array([-1, 1, 1, -1, 0])
    y = np.array([-1, -1, 1, 1, 0])
    z = np.array([0, 0, 0, 0, 1.5])
    # Faces
    i = [0, 0,  0, 1, 2, 3]
    j = [1, 2,  1, 2, 3, 0]
    k = [2, 3,  4, 4, 4, 4]
    return x, y, z, i, j, k

def dados_prisma():
    # 6 Vértices
    x = np.array([-1, 1, 0,   -1, 1, 0])
    y = np.array([-1, -1, 1,  -1, -1, 1])
    z = np.array([0, 0, 0,    2, 2, 2])
    # Faces
    i = [0, 3,  0, 0, 1, 1, 2, 2]
    j = [1, 4,  1, 4, 2, 5, 0, 3]
    k = [2, 5,  3, 1, 4, 2, 3, 5]
    return x, y, z, i, j, k

# --- FUNÇÃO DE ROTAÇÃO (Matemática Pura) ---
def rotacionar_pontos(x, y, z, angulo_graus, eixo='z'):
    """Aplica uma matriz de rotação aos pontos."""
    theta = np.radians(angulo_graus)
    c, s = np.cos(theta), np.sin(theta)

    if eixo == 'z':
        # Rotação em torno do eixo Z (o mais comum para "girar" o objeto)
        x_rot = x * c - y * s
        y_rot = x * s + y * c
        z_rot = z # Z não muda
    elif eixo == 'y':
        x_rot = x * c + z * s
        y_rot = y
        z_rot = -x * s + z * c
    elif eixo == 'x':
        x_rot = x
        y_rot = y * c - z * s
        z_rot = y * s + z * c
    
    return x_rot, y_rot, z_rot

# --- PREPARAÇÃO DOS DADOS INICIAIS ---
xc, yc, zc, ic, jc, kc = dados_cubo()
xp, yp, zp, ip, jp, kp = dados_piramide()
xpr, ypr, zpr, ipr, jpr, kpr = dados_prisma()

# --- CRIAÇÃO DA FIGURA COM SUBPLOTS ---
fig = make_subplots(
    rows=1, cols=3,
    specs=[[{'type': 'mesh3d'}, {'type': 'mesh3d'}, {'type': 'mesh3d'}]],
    subplot_titles=("Cubo em Rotação", "Pirâmide em Rotação", "Prisma em Rotação")
)

# Adiciona os traços iniciais (Frame 0)
fig.add_trace(go.Mesh3d(x=xc, y=yc, z=zc, i=ic, j=jc, k=kc, color='cyan', opacity=0.8, name='Cubo'), row=1, col=1)
fig.add_trace(go.Mesh3d(x=xp, y=yp, z=zp, i=ip, j=jp, k=kp, color='orange', opacity=0.8, name='Pirâmide'), row=1, col=2)
fig.add_trace(go.Mesh3d(x=xpr, y=ypr, z=zpr, i=ipr, j=jpr, k=kpr, color='mediumpurple', opacity=0.8, name='Prisma'), row=1, col=3)

# --- CRIAÇÃO DOS FRAMES DA ANIMAÇÃO ---
frames = []
num_frames = 120 # 360 graus / 3 graus por frame = 120 frames

for k in range(num_frames):
    angulo = k * 3 # Gira 3 graus por frame
    
    # Calcula a nova posição para cada sólido
    xc_rot, yc_rot, zc_rot = rotacionar_pontos(xc, yc, zc, angulo, 'z')
    xp_rot, yp_rot, zp_rot = rotacionar_pontos(xp, yp, zp, angulo, 'z')
    xpr_rot, ypr_rot, zpr_rot = rotacionar_pontos(xpr, ypr, zpr, angulo, 'z')
    
    # Cria o frame com os novos dados para os 3 traços
    frames.append(go.Frame(data=[
        go.Mesh3d(x=xc_rot, y=yc_rot, z=zc_rot), # Atualiza Cubo (trace 0)
        go.Mesh3d(x=xp_rot, y=yp_rot, z=zp_rot), # Atualiza Pirâmide (trace 1)
        go.Mesh3d(x=xpr_rot, y=ypr_rot, z=zpr_rot) # Atualiza Prisma (trace 2)
    ], name=f'frame{k}'))

fig.frames = frames

# --- LAYOUT ---
fig.update_layout(
    title=dict(text="Animação Geométrica Interativa", x=0.5, font=dict(size=24)),
    template="plotly_dark",
    
    # MODO TELA CHEIA
    autosize=True,  # Ajusta ao tamanho do navegador
    # height=600,   
    
    # Margens mínimas
    margin=dict(l=0, r=0, t=50, b=0),
    
    # Câmera fixa
    scene =dict(aspectmode='cube', xaxis=dict(range=[-2,2]), yaxis=dict(range=[-2,2]), zaxis=dict(range=[-2,2])),
    scene2=dict(aspectmode='cube', xaxis=dict(range=[-2,2]), yaxis=dict(range=[-2,2]), zaxis=dict(range=[-2,2])),
    scene3=dict(aspectmode='cube', xaxis=dict(range=[-2,2]), yaxis=dict(range=[-2,2]), zaxis=dict(range=[-2,2])),
    
    # Controles (Play/Pause)
    updatemenus=[dict(
        type='buttons', showactive=False,
        y=0.1, x=0.5, xanchor='center', # Botões centralizados embaixo
        buttons=[
            dict(label='▶ Play', method='animate', args=[None, dict(frame=dict(duration=50, redraw=True), fromcurrent=True)]),
            dict(label='❚❚ Pause', method='animate', args=[[None], dict(frame=dict(duration=0, redraw=False), mode='immediate')])
        ]
    )],
    sliders=[dict(
        steps=[dict(method='animate', args=[[f'fr{k}'], dict(mode='immediate', frame=dict(duration=50, redraw=True))], label=f'{k*3}°') for k in range(num_frames)],
        currentvalue=dict(prefix='Ângulo: '),
        pad=dict(t=50), 
        y=0
    )]
)

fig.write_html("animacao_fullscreen.html", auto_open=True)