import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Galton Board Dinamica", layout="wide")

st.title("🏗️ Galton Board: L'Ordine Dinamico")
st.markdown("Guarda come ogni pallina sceglie il suo percorso. Il caos individuale crea l'ordine collettivo.")

# Sidebar per i controlli
with st.sidebar:
    st.header("Configurazione")
    n_balls = st.slider("Numero di palline totali", 10, 500, 100)
    speed = st.slider("Velocità animazione", 0.01, 0.5, 0.1)
    if st.button("Lancia le palline!"):
        st.session_state.run = True
    else:
        if 'run' not in st.session_state:
            st.session_state.run = False

# Inizializzazione contenitore per i risultati
if 'results' not in st.session_state or st.session_state.run:
    st.session_state.results = []
    st.session_state.paths = []

n_layers = 12

# AREA DELLA SIMULAZIONE
placeholder = st.empty()

if st.session_state.run:
    for i in range(n_balls):
        # Generiamo il percorso della singola pallina
        # 0 = sinistra, 1 = destra
        steps = np.random.choice([-0.5, 0.5], size=n_layers)
        path_x = np.cumsum(steps) # Coordinata X che cambia cadendo
        path_y = np.arange(n_layers, 0, -1) # Coordinata Y che scende
        
        # Aggiungiamo il punto di partenza (0, n_layers+1)
        path_x = np.insert(path_x, 0, 0)
        path_y = np.insert(path_y, 0, n_layers + 1)
        
        st.session_state.results.append(path_x[-1])
        
        # Creazione del grafico dinamico con Plotly
        fig = go.Figure()

        # Disegniamo i "pioli" (background fisso)
        for y in range(1, n_layers + 1):
            row_x = np.arange(-y/2, y/2 + 1, 1)
            fig.add_trace(go.Scatter(x=row_x, y=[y]*len(row_x), mode='markers', 
                                     marker=dict(color='gray', size=5), showlegend=False))

        # Disegniamo il percorso della pallina attuale
        fig.add_trace(go.Scatter(x=path_x, y=path_y, mode='lines+markers',
                                 line=dict(color='red', width=2), marker=dict(size=8),
                                 name="Pallina in caduta"))

        # Disegniamo l'istogramma accumulato in basso
        if len(st.session_state.results) > 0:
            fig.add_trace(go.Histogram(x=st.session_state.results, 
                                       nbinsx=n_layers + 1, 
                                       marker_color='#1f77b4',
                                       opacity=0.6,
                                       name="Distribuzione accumulata",
                                       yaxis='y2'))

        # Layout del grafico
        fig.update_layout(
            xaxis=dict(range=[-n_layers/2 - 1, n_layers/2 + 1], showgrid=False, zeroline=False),
            yaxis=dict(range=[0, n_layers + 2], showgrid=False, zeroline=False),
            yaxis2=dict(overlaying='y', side='right', range=[0, n_balls/2], showgrid=False),
            height=600,
            template="plotly_white",
            showlegend=False
        )

        placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(speed)
    
    st.session_state.run = False
    st.success(f"Simulazione completata con {n_balls} palline!")

else:
    st.info("Configura il numero di palline nella barra laterale e clicca su 'Lancia le palline!'")
