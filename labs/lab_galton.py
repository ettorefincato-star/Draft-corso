import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import time

st.set_page_config(page_title="Galton Board Fisica", layout="wide")

st.title("🏗️ Galton Board: Simulazione Fisica")
st.markdown("Osserva le palline cadere e rimbalzare sui pioli. Guarda come si accumulano naturalmente formando una campana.")

# Sidebar per i controlli
with st.sidebar:
    st.header("Configurazione")
    n_balls_per_sim = st.slider("Palline per simulazione", 10, 100, 50)
    n_layers = st.slider("Numero di livelli di pioli", 5, 15, 10)
    speed = st.slider("Velocità di caduta", 0.01, 0.2, 0.05)
    
    if st.button("Lancia le palline!"):
        st.session_state.run_physics = True
    else:
        if 'run_physics' not in st.session_state:
            st.session_state.run_physics = False

# AREA DELLA SIMULAZIONE FISICA
placeholder = st.empty()

# Generazione della griglia dei pioli (statica)
pegs = []
for y in range(1, n_layers + 1):
    row_x = np.arange(-y/2, y/2 + 1, 1)
    for x in row_x:
        pegs.append({'x': x, 'y': y, 'type': 'peg'})
df_pegs = pd.DataFrame(pegs)

if st.session_state.run_physics:
    # Inizializzazione delle palline
    balls = []
    for _ in range(n_balls_per_sim):
        balls.append({'x': 0, 'y': n_layers + 1, 'type': 'ball', 'vx': 0, 'vy': -1, 'stuck_prob': 0.1})
    df_balls = pd.DataFrame(balls)

    # Ciclo di animazione (passi fisici)
    for step in range((n_layers + 2) * 5): # Numero sufficiente di passi per far cadere tutte le palline
        # Aggiornamento fisico delle palline
        for i, ball in df_balls.iterrows():
            if ball['y'] > 0: # Se non è ancora nel canale finale
                # Caduta
                ball['x'] += ball['vx'] * speed
                ball['y'] += ball['vy'] * speed
                
                # Collisione con i pioli (approssimazione)
                peg_collision = df_pegs[(np.abs(df_pegs['x'] - ball['x']) < 0.3) & (np.abs(df_pegs['y'] - ball['y']) < 0.3)]
                if not peg_collision.empty:
                    # Rimbalzo casuale a destra o sinistra
                    direction = np.random.choice([-1, 1])
                    ball['vx'] = direction * 0.5
                    ball['vy'] = -0.5
                else:
                    # Accelerazione di gravità (semplificata)
                    ball['vy'] = -1
                    ball['vx'] *= 0.9 # Attrito dell'aria

            else: # Arrivo nel canale finale
                ball['y'] = 0
                ball['vx'] = 0
                ball['vy'] = 0

        # Creazione del grafico di base con Altair
        base = alt.Chart(pd.concat([df_pegs, df_balls])).encode(
            x=alt.X('x', scale=alt.Scale(domain=[-n_layers/2 - 1, n_layers/2 + 1]), axis=None),
            y=alt.Y('y', scale=alt.Scale(domain=[0, n_layers + 2]), axis=None)
        )

        # Visualizzazione dei pioli (grigi)
        chart_pegs = base.transform_filter(
            alt.datum.type == 'peg'
        ).mark_point(filled=True, color='gray', size=20)

        # Visualizzazione delle palline (rosse)
        chart_balls = base.transform_filter(
            alt.datum.type == 'ball'
        ).mark_point(filled=True, color='red', size=40)

        # Combinazione e rendering
        final_chart = alt.layer(chart_pegs, chart_balls).properties(
            width=800,
            height=600
        ).configure_view(strokeWidth=0)

        placeholder.altair_chart(final_chart, use_container_width=True)
        time.sleep(speed)
    
    st.session_state.run_physics = False
    st.success(f"Simulazione completata!")

else:
    # Mostra solo i pioli e le palline ferme in alto
    chart_pegs = alt.Chart(df_pegs).mark_point(filled=True, color='gray', size=20).encode(
        x=alt.X('x', scale=alt.Scale(domain=[-n_layers/2 - 1, n_layers/2 + 1]), axis=None),
        y=alt.Y('y', scale=alt.Scale(domain=[0, n_layers + 2]), axis=None)
    )
    
    # Palline ferme in alto
    df_initial_balls = pd.DataFrame([{'x': 0, 'y': n_layers + 1, 'type': 'ball'}])
    chart_balls = alt.Chart(df_initial_balls).mark_point(filled=True, color='red', size=40).encode(
        x='x', y='y'
    )
    
    final_chart = alt.layer(chart_pegs, chart_balls).properties(
        width=800,
        height=600
    ).configure_view(strokeWidth=0)
    
    placeholder.altair_chart(final_chart, use_container_width=True)
    st.info("Configura il numero di palline nella barra laterale e clicca su 'Lancia le palline!'")
