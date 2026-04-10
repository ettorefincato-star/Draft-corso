import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Galton Board Fluida", layout="wide")

st.title("🏗️ Galton Board Professionale")
st.markdown("Le palline cadono attraverso i pioli (punti grigi) per formare la Distribuzione Normale.")

# --- PARAMETRI ---
n_layers = 10
n_balls = st.sidebar.slider("Numero di palline", 10, 100, 30)

# --- GENERAZIONE COORDINATE DI CADUTA ---
frames = []
all_paths_x = [ [0.0] for _ in range(n_balls) ]
all_paths_y = [ [float(n_layers + 1)] for _ in range(n_balls) ]

for b in range(n_balls):
    curr_x = 0.0
    for l in range(n_layers, 0, -1):
        curr_x += np.random.choice([-0.5, 0.5])
        all_paths_x[b].append(curr_x)
        all_paths_y[b].append(float(l))
    # Punto finale nel canale
    all_paths_x[b].append(curr_x)
    all_paths_y[b].append(-0.5)

# --- CREAZIONE DEI FRAME ---
max_steps = n_layers + 2
for s in range(max_steps + 1):
    current_x = [path[min(s, len(path)-1)] for path in all_paths_x]
    current_y = [path[min(s, len(path)-1)] for path in all_paths_y]
    
    frames.append(go.Frame(
        data=[go.Scatter(x=current_x, y=current_y, mode='markers', 
                         marker=dict(color='red', size=12))],
        name=f'frame{s}'
    ))

# --- COSTRUZIONE LAYOUT (Pioli fissi) ---
# Creiamo i pioli come "scatter" nel dato iniziale che non viene rimosso
pegs_x = []
pegs_y = []
for r in range(1, n_layers + 1):
    row = np.arange(-r/2, r/2 + 1, 1)
    pegs_x.extend(row)
    pegs_y.extend([r] * len(row))

fig = go.Figure(
    data=[
        # Traccia 0: Le palline (animate)
        go.Scatter(x=[0]*n_balls, y=[n_layers+1]*n_balls, mode='markers',
                   marker=dict(color='red', size=12), name="Palline"),
        # Traccia 1: I pioli (fissi)
        go.Scatter(x=pegs_x, y=pegs_y, mode='markers', 
                   marker=dict(color='darkgray', size=8), hoverinfo='skip', name="Pioli")
    ],
    layout=go.Layout(
        xaxis=dict(range=[-n_layers/2 - 2, n_layers/2 + 2], showgrid=False, zeroline=False, fixedrange=True),
        yaxis=dict(range=[-1, n_layers + 2], showgrid=False, zeroline=False, fixedrange=True),
        height=700,
        template="plotly_white",
        updatemenus=[{
            "type": "buttons",
            "buttons": [{
                "label": "▶ Lancia Palline",
                "method": "animate",
                "args": [None, {"frame": {"duration": 300, "redraw": True}, "fromcurrent": True}]
            }]
        }]
    ),
    frames=frames
)

# Aggiunta visiva dei canali alla base
for x in np.arange(-n_layers/2, n_layers/2 + 1, 1):
    fig.add_shape(type="line", x0=x, y0=-0.8, x1=x, y1=0.2, line=dict(color="lightgray", width=1))

st.plotly_chart(fig, use_container_width=True)
