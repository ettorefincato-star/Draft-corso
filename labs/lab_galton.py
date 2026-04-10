import streamlit as st
import numpy as np
import time

st.set_page_config(page_title="Galton Board", layout="centered")

st.title("🏗️ Galton Board Ultra-Fluida")
st.markdown("La pallina, in ogni slot, ha il 50% di andare a destra e il 50% di andare a sinistra")

# --- CONFIGURAZIONE ---
n_layers = 10
columns = list(range(n_layers + 1))

if 'counts' not in st.session_state:
    st.session_state.counts = [0] * (n_layers + 1)

with st.sidebar:
    n_balls = st.slider("Palline", 1, 300, 20)
    speed = st.slider("Velocità", 0.01, 0.5, 0.1)
    run = st.button("Lancia!")

# AREA DI DISEGNO PRINCIPALE
board_spot = st.empty()
hist_spot = st.empty()

def render_board(ball_pos=None, layer=None):
    # CSS per centrare perfettamente ogni riga e definire la dimensione dei cerchi
    board_html = """
    <style>
        .galton-container {
            font-family: 'Courier New', Courier, monospace;
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
        }
        .galton-row {
            display: flex;
            justify-content: center;
            height: 30px;
            margin-bottom: 5px;
        }
        .cell {
            width: 35px;
            text-align: center;
            font-size: 25px;
        }
    </style>
    <div class='galton-container'>
    """
    
    for l in range(n_layers + 1):
        board_html += "<div class='galton-row'>"
        for i in range(l + 1):
            if ball_pos == i and layer == l:
                content = "🔴" # La pallina
            else:
                content = "⚪" # Il piolo
            board_html += f"<div class='cell'>{content}</div>"
        board_html += "</div>"
    
    board_html += "</div>"
    return board_html

def render_hist():
    # Crea un istogramma semplice con barre colorate
    max_c = max(st.session_state.counts) if max(st.session_state.counts) > 0 else 1
    hist_html = "<div style='display: flex; align-items: flex-end; justify-content: center; height: 150px; padding-top: 20px;'>"
    for c in st.session_state.counts:
        height = (c / max_c) * 100
        hist_html += f"<div style='background-color: #1f77b4; width: 20px; height: {height}px; margin: 2px; border-radius: 2px;'></div>"
    hist_html += "</div>"
    return hist_html

# --- LOGICA ---
if run:
    st.session_state.counts = [0] * (n_layers + 1)
    for b in range(n_balls):
        curr_pos = 0 # Inizia in cima (posizione 0)
        for l in range(n_layers + 1):
            # Mostra la pallina
            board_spot.markdown(render_board(curr_pos, l), unsafe_allow_html=True)
            time.sleep(speed)
            
            # Decisione per il livello successivo
            if l < n_layers:
                curr_pos += np.random.choice([0, 1])
        
        # Aggiorna conteggio finale
        st.session_state.counts[curr_pos] += 1
        hist_spot.markdown(render_hist(), unsafe_allow_html=True)

else:
    board_spot.markdown(render_board(), unsafe_allow_html=True)
    hist_spot.markdown(render_hist(), unsafe_allow_html=True)
