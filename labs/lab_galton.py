import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Galton Board Simulator", layout="centered")

st.title("🏗️ Simulatore Galton Board")
st.markdown("Ogni pallina cade e decide 10 volte se andare a destra (+1) o sinistra (-1).")

# Controlli per lo studente
n_balls = st.select_slider(
    "Quante palline vuoi lanciare?",
    options=[10, 100, 500, 1000, 5000, 10000],
    value=500
)

n_layers = 10 # Numero di file di pioli

# Simulazione del cammino casuale
# Generiamo una matrice di decisioni (0 o 1)
data = np.random.randint(0, 2, size=(n_balls, n_layers))
# Sommiamo le decisioni per vedere dove finisce ogni pallina
final_positions = np.sum(data, axis=1)

# Calcolo della curva teorica (Normale) per confronto
x_theory = np.linspace(0, n_layers, 100)
mu = n_layers / 2
sigma = np.sqrt(n_layers * 0.25)
y_theory = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_theory - mu) / sigma)**2)

# Grafico
fig, ax = plt.subplots(figsize=(10, 6))

# Istogramma delle palline cadute
counts, bins, _ = ax.hist(final_positions, bins=np.arange(n_layers + 2) - 0.5, 
                          density=True, color='#1f77b4', alpha=0.7, rwidth=0.8, label="Palline cadute")

# Sovrapponiamo la campana teorica
ax.plot(x_theory, y_theory, color='#ff7f0e', lw=3, label="Distribuzione Normale (Teoria)")

ax.set_title(f"Distribuzione finale dopo {n_balls} lanci")
ax.set_xlabel("Posizione finale (Canali)")
ax.set_ylabel("Frequenza")
ax.legend()
ax.grid(axis='y', alpha=0.3)

st.pyplot(fig)

# Messaggio educativo
st.info(f"Nota come con {n_balls} palline, la forma dei blocchi blu si avvicini sempre di più alla linea arancione. Questo è il passaggio dal caos individuale all'ordine statistico.")
