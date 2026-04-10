import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Galton Board Realistica", layout="wide")

st.title("🏗️ Galton Board: La Campana in Movimento")
st.markdown("Se le palline sembrano ferme, clicca 'Lancia'. Ognuna segue un percorso casuale unico.")

# --- CONFIGURAZIONE ---
n_layers = 10
if 'results' not in st.session_state:
    st.session_state.results = []

with st.sidebar:
    n_balls = st.number_input("Quante palline lanciare?", min_value=1, max_value=100, value=10)
    speed = st.slider("Lentezza caduta", 0.01, 0.2, 0.05)
    if st.button("Lancia le palline!"):
        st.session_state.run = True
    else:
        st.session_state.run = False

# --- FUNZIONE PER GENERARE UN PERCORSO FLUIDO ---
def generate_smooth_path(layers):
    x = [0.0]
    y = [layers + 1.0]
    curr_x = 0.0
    for i in range(layers, 0, -1):
        # Decisione: destra o sinistra
        step = np.random.choice([-0.5, 0.5])
        curr_x += step
        # Aggiungiamo punti intermedi per rendere la caduta fluida
        x.extend([x[-1], curr_x]) 
        y.extend([i + 0.5, i])
    x.append(curr_x)
    y.append(0)
    return x, y, curr_x

# --- AREA VISIVA ---
placeholder = st.empty()

# Disegno dei pioli (Pegs)
pegs_x = []
pegs_y = []
for r in range(1, n_layers + 1):
    row = np.arange(-r/2, r/2 + 1, 1)
    pegs_x.extend(row)
    pegs_y.extend([r] * len(row))

if st.session_state.run:
    for b in range(n_balls):
        path_x, path_y, final_x = generate_smooth_path(n_layers)
        st.session_state.results.append(final_x)
        
        # Animazione della singola pallina
        for i in range(len(path_x)):
            fig = go.Figure()
            
            # 1. Pioli
            fig.add_trace(go.Scatter(x=pegs_x, y=pegs_y, mode='markers', 
                                     marker=dict(color='lightgray', size=10), showlegend=False))
            
            # 2. Pallina che cade
            fig.add_trace(go.Scatter(x=[path_x[i]], y=[path_y[i]], mode='markers',
                                     marker=dict(color='red', size=18, symbol='circle'), showlegend=False))
            
            # 3. Istogramma dei risultati precedenti (canali in basso)
            if len(st.session_state.results) > 0:
                fig.add_trace(go.Histogram(x=st.session_state.results[:-1] if i < len(path_x)-1 else st.session_state.results,
                                           nbinsx=n_layers+1, marker_color='blue', opacity=0.3, showlegend=False))

            fig.update_layout(
                xaxis=dict(range=[-n_layers/2 - 1, n_layers/2 + 1], fixedrange=True, showgrid=False, zeroline=False),
                yaxis=dict(range=[-1, n_layers + 2], fixedrange=True, showgrid=False, zeroline=False),
                height=600, template="plotly_white"
            )
            
            placeholder.plotly_chart(fig, use_container_width=True)
            time.sleep(speed)
    
    st.session_state.run = False
