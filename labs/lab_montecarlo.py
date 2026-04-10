import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Titolo dell'applicazione
st.title("Simulazione Monte Carlo: Stimare $\pi$")

# Introduzione ben formattata
st.write("### L'intuizione geometrica")
st.markdown("""
Immaginiamo un cerchio inscritto in un quadrato. Se lanciamo dei punti casuali nel quadrato, 
la probabilità che cadano nel cerchio dipende dal rapporto tra le aree.
""")

# Formule in evidenza
st.latex(r"Area_{cerchio} = \pi r^2")
st.latex(r"Area_{quadrato} = (2r)^2 = 4r^2")
st.latex(r"\frac{Area_{cerchio}}{Area_{quadrato}} = \frac{\pi}{4}")
st.markdown("Quindi, contando i punti, possiamo ricavare $\pi$:")
st.latex(r"\pi \approx 4 \times \frac{N_{dentro}}{N_{totali}}")

# Parametri della simulazione
st.sidebar.header("Parametri")
numero_punti = st.sidebar.slider("Numero di punti da generare:", min_value=10, max_value=10000, value=1000, step=10)

# Funzione per eseguire la simulazione e calcolare la convergenza
@st.cache_data
def esegui_simulazione_pi(n_punti):
    x = np.random.uniform(0, 1, n_punti)
    y = np.random.uniform(0, 1, n_punti)
    
    centro_x, centro_y = 0.5, 0.5
    raggio = 0.5
    distanza_quadrata = (x - centro_x)**2 + (y - centro_y)**2
    dentro_cerchio = distanza_quadrata <= raggio**2
    
    # Calcolo della stima progressiva per il grafico dell'errore
    # cumsum somma i successi uno dopo l'altro: [T, F, T] -> [1, 1, 2]
    successi_progressivi = np.cumsum(dentro_cerchio)
    tentativi_progressivi = np.arange(1, n_punti + 1)
    stime_progressive = 4 * (successi_progressivi / tentativi_progressivi)
    
    return x, y, dentro_cerchio, stime_progressive

# Esegui la simulazione
x, y, dentro_cerchio, stime_progressive = esegui_simulazione_pi(numero_punti)

# --- VISUALIZZAZIONE GEOMETRICA ---
st.subheader("Visualizzazione Geometrica")
fig1, ax1 = plt.subplots(figsize=(8, 8))
cerchio = plt.Circle((0.5, 0.5), 0.5, color='blue', fill=False, linewidth=2)
ax1.add_artist(cerchio)
ax1.scatter(x[dentro_cerchio], y[dentro_cerchio], color='blue', s=2, alpha=0.6, label='Dentro')
ax1.scatter(x[~dentro_cerchio], y[~dentro_cerchio], color='red', s=2, alpha=0.6, label='Fuori')
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.set_aspect('equal')
ax1.legend(loc='upper right')
st.pyplot(fig1)

# --- METRICHE FINALI ---
st.subheader("Risultato Finale")
punti_dentro = np.sum(dentro_cerchio)
pi_stima = stime_progressive[-1]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Punti Totali", numero_punti)
col2.metric("Punti nel Cerchio", punti_dentro)
col3.metric("Stima di π", f"{pi_stima:.5f}")
col4.metric("Valore reale π", 3.14159)

# --- GRAFICO DELL'ERRORE (CONVERGENZA) ---
st.subheader("Analisi dell'Errore e Convergenza")
st.markdown("Il grafico sotto mostra come l'errore oscilla violentemente all'inizio per poi stabilizzarsi verso lo zero man mano che aumentano i dati (**Legge dei Grandi Numeri**).")

# Calcolo dell'errore residuo (Stima - Reale)
errore_residuo = stime_progressive - np.pi

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.plot(errore_residuo, color='purple', linewidth=1, label='Errore (Stima - π)')
ax2.axhline(y=0, color='black', linestyle='--') # Linea dello zero (errore nullo)
ax2.set_xlabel("Numero di punti lanciati")
ax2.set_ylabel("Errore")
ax2.set_title("Andamento dell'Errore Residuo")
ax2.grid(True, alpha=0.3)
ax2.legend()

st.pyplot(fig2)

# Info aggiuntiva sull'errore finale
errore_percentuale = abs(pi_stima - np.pi) / np.pi * 100
st.write(f"**Errore percentuale finale:** {errore_percentuale:.2f}%")
