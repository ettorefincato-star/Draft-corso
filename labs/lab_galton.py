import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Galton Board Fluida", layout="wide")

st.title("🏗️ Galton Board Professionale")
st.markdown("Una simulazione fluida dell'ordine statistico.")

# --- PARAMETRI ---
n_layers = 12
n_balls = st.sidebar.slider("Numero di palline", 5, 50, 20)

# --- GENERAZIONE DEI PIOLI (Sempre uguali) ---
pegs_x = []
pegs_y = []
for r in range(1, n_layers + 1):
    row = np.arange(-r/2, r/2 + 1, 1)
    pegs_x.extend(row)
    pegs_y.extend([r] * len(row))

# --- GENERAZIONE COORDINATE DI CADUTA ---
# Creiamo i frame dell'animazione per tutte le palline contemporaneamente
frames = []
steps = 25  # fluidità della caduta

# Inizializziamo le posizioni X e Y per ogni pallina
ball_positions_x = np.zeros(n_balls)
ball_positions_y = np.full(n_balls, n_layers + 1.0)
final_results = []

# Calcoliamo i percorsi in anticipo
all_paths_x = [ [0.0] for _ in range(n_balls) ]
all_paths_y = [ [float(n_layers + 1)] for _ in range(n_balls) ]

for b in range(n_balls):
    curr_x = 0.0
    for l in range(n_layers, 0, -1):
        curr_x += np.random.choice([-0.5, 0.5])
        all_paths_x[b].append(curr_x)
        all_paths_y[b].append(float(l))
    final_results.append(curr_x)

# --- CREAZIONE DEI FRAME ---
# Ogni frame mostra la posizione di tutte le palline in quel momento
max_steps = n_layers + 1
for s in range(max_steps + 1):
    current_x = [path[min(s, len(path)-1)] for path in all_paths_x]
    current_y = [path[min(s, len(path)-1)] for path in all_paths_y]
    
    frames.append(go.Frame(
        data=[go.Scatter(x=current_x, y=current_y, mode='markers', 
                         marker=dict(color='red', size=12))]
    ))

# --- GRAFICO INIZIALE ---
fig = go.Figure(
    data=[
        # Pioli (Sempre visibili)
        go.Scatter(x=pegs_x, y=pegs_y, mode='markers', 
                   marker=dict(color='lightgray', size=8), hoverinfo='skip'),
        # Palline (Punto di partenza)
        go.Scatter(x=[0]*n_balls, y=[n_layers+1]*n_balls, mode='markers',
                   marker=dict(color='red', size=12))
    ],
    layout=go.Layout(
        xaxis=dict(range=[-n_layers/2 - 2, n_layers/2 + 2], showgrid=False, zeroline=False, fixedrange=True),
        yaxis=dict(range=[-1, n_layers + 2], showgrid=False, zeroline=False, fixedrange=True),
        height=700,
        updatemenus=[{
            "type": "buttons",
            "buttons": [{
                "label": "Lancia Palline",
                "method": "animate",
                "args": [None, {"frame": {"duration": 200, "redraw": False}, "fromcurrent": True}]
            }]
        }]
    ),
    frames=frames
)

# Aggiungiamo i rettangoli per i canali in basso (estetica)
for x in np.arange(-n_layers/2, n_layers/2 + 1, 1):
    fig.add_shape(type="rect", x0=x-0.4, y0=-0.5, x1=x+0.4, y1=0, line=dict(color="RoyalBlue"))

st.plotly_chart(fig, use_container_width=True)

st.info("Clicca sul tasto 'Lancia Palline' dentro il grafico per avviare l'animazione senza ricaricare la pagina.")
