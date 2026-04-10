import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Galton Board Reale", layout="wide")

st.title("🏗️ Galton Board: Simulazione Fisica")

# --- PARAMETRI FISSI ---
n_layers = 10
columns = np.arange(-n_layers/2, n_layers/2 + 1, 1)

# --- SIDEBAR CONTROLLI ---
with st.sidebar:
    n_balls = st.slider("Numero di palline", 10, 200, 50)
    speed = st.slider("Velocità caduta", 0.01, 0.5, 0.1)
    run = st.button("Lancia Palline")

# Inizializzazione risultati nel browser
if 'final_counts' not in st.session_state:
    st.session_state.final_counts = {col: 0 for col in columns}

# --- GENERAZIONE PIOLI ---
pegs_x = []
pegs_y = []
for r in range(1, n_layers + 1):
    row = np.arange(-r/2, r/2 + 1, 1)
    pegs_x.extend(row)
    pegs_y.extend([r] * len(row))

# --- AREA DI DISEGNO ---
plot_spot = st.empty()

def draw_board(current_ball_x=None, current_ball_y=None):
    fig = go.Figure()

    # 1. I Pioli (Grigi)
    fig.add_trace(go.Scatter(x=pegs_x, y=pegs_y, mode='markers', 
                             marker=dict(color='lightgray', size=10), showlegend=False))

    # 2. L'Istogramma (Barre Blu in basso)
    fig.add_trace(go.Bar(x=list(st.session_state.final_counts.keys()), 
                         y=list(st.session_state.final_counts.values()),
                         marker_color='rgba(0, 0, 255, 0.5)', name="Accumulo"))

    # 3. La Pallina Attuale (Rossa)
    if current_ball_x is not None:
        fig.add_trace(go.Scatter(x=[current_ball_x], y=[current_ball_y], mode='markers',
                                 marker=dict(color='red', size=15), showlegend=False))

    fig.update_layout(
        xaxis=dict(range=[-n_layers/2 - 1, n_layers/2 + 1], fixedrange=True, showgrid=False, zeroline=False),
        yaxis=dict(range=[-2, n_layers + 2], fixedrange=True, showgrid=False, zeroline=False),
        height=600, template="plotly_white", showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    return fig

# --- LOGICA DI CADUTA ---
if run:
    # Reset conteggi per nuova simulazione
    st.session_state.final_counts = {col: 0 for col in columns}
    
    for b in range(n_balls):
        curr_x = 0.0
        # La pallina scende livello per livello
        for curr_y in range(n_layers + 1, 0, -1):
            # Disegniamo la pallina in questa posizione
            plot_spot.plotly_chart(draw_board(curr_x, curr_y), use_container_width=True)
            time.sleep(speed / 2)
            
            # Se tocca un piolo (y intero tra 1 e n_layers)
            if 1 <= curr_y <= n_layers:
                # Rimbalzo: cambia direzione SOLO qui
                move = np.random.choice([-0.5, 0.5])
                curr_x += move
        
        # Arrivo al suolo (y=0)
        # Troviamo la colonna più vicina (canale)
        final_col = min(columns, key=lambda x:abs(x-curr_x))
        st.session_state.final_counts[final_col] += 1
        
        # Aggiornamento finale per questa pallina
        plot_spot.plotly_chart(draw_board(curr_x, 0), use_container_width=True)
        time.sleep(speed / 4)

else:
    # Stato iniziale
    plot_spot.plotly_chart(draw_board(), use_container_width=True)
