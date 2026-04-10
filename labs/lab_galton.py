import streamlit as st
import numpy as np
import time

st.set_page_config(page_title="Galton Board Fluida", layout="centered")

st.title("🏗️ Galton Board Ultra-Fluida")
st.markdown("Questa versione elimina il lampeggio usando rendering testuale dinamico.")

# --- CONFIGURAZIONE ---
n_layers = 10
columns = list(range(n_layers + 1))

if 'counts' not in st.session_state:
    st.session_state.counts = [0] * (n_layers + 1)

with st.sidebar:
    n_balls = st.slider("Palline", 1, 100, 20)
    speed = st.slider("Velocità", 0.01, 0.5, 0.1)
    run = st.button("Lancia!")

# AREA DI DISEGNO PRINCIPALE
board_spot = st.empty()
hist_spot = st.empty()

def render_board(ball_pos=None, layer=None):
    board_html = "<div style='font-family: monospace; text-align: center; line-height: 1.2; font-size: 20px;'>"
    
    for l in range(n_layers + 1):
        # Disegniamo i pioli
        row_content = ""
        # Spazi iniziali per centrare la piramide
        row_content += "&nbsp;" * (n_layers - l)
        
        for i in range(l + 1):
            if ball_pos == i and layer == l:
                row_content += "🔴" # La pallina
            else:
                row_content += "⚪" # Il piolo
            row_content += "&nbsp;"
        
        board_html += row_content + "<br>"
    
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
