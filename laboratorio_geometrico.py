import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# --- MATEMÁTICA E AS FUNÇÕES UNIVERSAIS ---

def gerar_cilindro_ou_prisma(lados=30, raio=1, altura=2):

    # Ângulos para criar o círculo da base
    theta = np.linspace(0, 2*np.pi, lados, endpoint=False)
    x_base = raio * np.cos(theta)
    y_base = raio * np.sin(theta)
    
    # Listas de vértices
    x, y, z = [], [], []
    
    # Topo e Base
    # Base (z=0)
    x.extend(x_base); y.extend(y_base); z.extend([0]*lados)
    # Topo (z=altura)
    x.extend(x_base); y.extend(y_base); z.extend([altura]*lados)
    # Centro baixo e Centro alto (para fechar as tampas)
    x.extend([0, 0]); y.extend([0, 0]); z.extend([0, altura])
    
    idx_centro_baixo = 2 * lados
    idx_centro_alto = 2 * lados + 1
    
    # Triângulos (Faces)
    i, j, k = [], [], []
    
    for idx in range(lados):
        prox = (idx + 1) % lados
        
        # 1. Paredes Laterais (formadas por 2 triângulos cada)
        # Pontos da base: idx, prox
        # Pontos do topo: idx+lados, prox+lados
        
        # Triângulo 1
        i.append(idx); j.append(prox); k.append(idx + lados)
        # Triângulo 2
        i.append(prox); j.append(prox + lados); k.append(idx + lados)
        
        # 2. Tampa de Baixo (conecta com centro baixo)
        i.append(idx); j.append(prox); k.append(idx_centro_baixo)
        
        # 3. Tampa de Cima (conecta com centro alto - ordem inversa para normal correta)
        i.append(idx + lados); j.append(idx_centro_alto); k.append(prox + lados)

    return x, y, z, i, j, k

def gerar_cone_ou_piramide(lados=30, raio=1, altura=2):

    theta = np.linspace(0, 2*np.pi, lados, endpoint=False)
    x_base = raio * np.cos(theta)
    y_base = raio * np.sin(theta)
    
    x = list(x_base) + [0] # Base + Ponta (Ápice)
    y = list(y_base) + [0]
    z = [0] * lados + [altura]
    
    idx_ponta = lados
    
    # Centro da base para fechar embaixo
    x.append(0); y.append(0); z.append(0)
    idx_centro_base = lados + 1
    
    i, j, k = [], [], []
    
    for idx in range(lados):
        prox = (idx + 1) % lados
        
        # Paredes (Triângulos que sobem até a ponta)
        i.append(idx); j.append(prox); k.append(idx_ponta)
        
        # Tampa de Baixo
        i.append(idx); j.append(idx_centro_base); k.append(prox)
        
    return x, y, z, i, j, k

def gerar_icosaedro():

    phi = (1 + np.sqrt(5)) / 2
    
    # 12 Vértices do Icosaedro (Retângulos Áureos entrelaçados)
    verts = [
        (-1, phi, 0), (1, phi, 0), (-1, -phi, 0), (1, -phi, 0),
        (0, -1, phi), (0, 1, phi), (0, -1, -phi), (0, 1, -phi),
        (phi, 0, -1), (phi, 0, 1), (-phi, 0, -1), (-phi, 0, 1)
    ]
    
    # Separando em X, Y, Z
    x = [v[0] for v in verts]
    y = [v[1] for v in verts]
    z = [v[2] for v in verts]
    
    # As 20 Faces (Triângulos) - Índices manuais baseados na geometria
    indices = [
        0,11,5, 0,5,1, 0,1,7, 0,7,10, 0,10,11,
        1,5,9, 5,11,4, 11,10,2, 10,7,6, 7,1,8,
        3,9,4, 3,4,2, 3,2,6, 3,6,8, 3,8,9,
        4,9,5, 2,4,11, 6,2,10, 8,6,7, 9,8,1
    ]
    
    # Plotly espera listas separadas para i, j, k
    i = indices[0::3]
    j = indices[1::3]
    k = indices[2::3]
    
    return x, y, z, i, j, k

# --- CONFIGURAÇÃO DA CENA ---

fig = make_subplots(
    rows=2, cols=2,
    specs=[[{'type': 'mesh3d'}, {'type': 'mesh3d'}],
           [{'type': 'mesh3d'}, {'type': 'mesh3d'}]],
    subplot_titles=("Cone (Alta Resolução)", "Cilindro (Alta Resolução)", 
                    "Icosaedro (D20 - Sólido de Platão)", "Prisma Hexagonal (Cilindro Low Poly)")
)

# --- ADICIONANDO OS OBJETOS ---

# A. CONE
xc, yc, zc, ic, jc, kc = gerar_cone_ou_piramide(lados=50, raio=1, altura=2)
fig.add_trace(go.Mesh3d(
    x=xc, y=yc, z=zc, i=ic, j=jc, k=kc,
    intensity=zc, colorscale='Viridis', name='Cone'
), row=1, col=1)

# B. CILINDRO
xcl, ycl, zcl, icl, jcl, kcl = gerar_cilindro_ou_prisma(lados=50, raio=1, altura=2)
fig.add_trace(go.Mesh3d(
    x=xcl, y=ycl, z=zcl, i=icl, j=jcl, k=kcl,
    intensity=zcl, colorscale='Plasma', name='Cilindro'
), row=1, col=2)

# C. ICOSAEDRO (D20)
xi, yi, zi, ii, ji, ki = gerar_icosaedro()
fig.add_trace(go.Mesh3d(
    x=xi, y=yi, z=zi, i=ii, j=ji, k=ki,
    color='#00ffcc', flatshading=True, name='Icosaedro'
), row=2, col=1)

# D. PRISMA HEXAGONAL (Reutilizando a função do cilindro com menos lados)
xp, yp, zp, ip, jp, kp = gerar_cilindro_ou_prisma(lados=6, raio=1, altura=2)
fig.add_trace(go.Mesh3d(
    x=xp, y=yp, z=zp, i=ip, j=jp, k=kp,
    intensity=zp, colorscale='Inferno', flatshading=True, name='Hexágono'
), row=2, col=2)


# --- ESTÉTICA FINAL ---
fig.update_layout(
    title=dict(
        text="Laboratório Geométrico Avançado",
        x=0.5, # Centraliza o título horizontalmente
        xanchor='center',
        font=dict(size=24)
    ),
    template="plotly_dark", 
    

    autosize=True,   # Permite que o gráfico se ajuste ao tamanho da janela
    # height=800,    
    # width=1000,    
    
    # Margens zeradas para aproveitar cada pixel da tela
    margin=dict(l=10, r=10, t=60, b=10),
    
    # Configurações de câmera para centralizar melhor os objetos
    scene=dict(aspectmode='data'),
    scene2=dict(aspectmode='data'),
    scene3=dict(aspectmode='data'),
    scene4=dict(aspectmode='data')
)

# Gera o arquivo HTML (Melhor forma de ver em tela cheia)
fig.write_html("geometria_fullscreen.html", auto_open=True)