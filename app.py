import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import sqlite3

# Conectar a la base de datos (o crearla)
conn = sqlite3.connect('trading_journal.db')
c = conn.cursor()

# Crear tablas si no existen
c.execute('''CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY,
    currency_pair TEXT,
    open_time TEXT,
    close_time TEXT,
    order_type TEXT,
    entry_price REAL,
    exit_price REAL,
    stop_loss REAL,
    take_profit REAL,
    position_size REAL,
    result_money REAL,
    result_pips REAL,
    spread REAL,
    slippage REAL,
    commission REAL,
    trade_reason TEXT,
    personal_notes TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS emotions (
    id INTEGER PRIMARY KEY,
    emotion_date TEXT,
    emotion_before TEXT,
    emotion_during TEXT,
    emotion_after TEXT,
    fomo INTEGER,
    impatience INTEGER,
    trading_revenge INTEGER,
    emotional_notes TEXT
)''')

# Configurar el título de la aplicación
st.title("Trading Journal")

# Seleccionar la pestaña
tabs = ["Registro de Operaciones", "Estadísticas y Rendimiento", "Análisis de Psicología y Emociones"]
tab = st.sidebar.selectbox("Selecciona una pestaña", tabs)

# Pestaña de Registro de Operaciones
if tab == "Registro de Operaciones":
    st.subheader("Registro de Operaciones Completo")

    # Formulario para registrar una operación
    with st.form("trade_form"):
        currency_pair = st.text_input("Par de divisas (o activo)")
        open_time = st.datetime_input("Fecha y hora de apertura", datetime.datetime.now())
        close_time = st.datetime_input("Fecha y hora de cierre", datetime.datetime.now())
        order_type = st.selectbox("Tipo de orden", ["Market", "Limit", "Stop"])
        entry_price = st.number_input("Precio de entrada", format="%.2f")
        exit_price = st.number_input("Precio de salida", format="%.2f")
        stop_loss = st.number_input("Stop-Loss", format="%.2f")
        take_profit = st.number_input("Take-Profit", format="%.2f")
        position_size = st.number_input("Tamaño de la posición (lotes o unidades)", format="%.2f")
        spread = st.number_input("Tamaño del spread", format="%.2f")
        slippage = st.number_input("Slippage", format="%.2f")
        commission = st.number_input("Comisiones y costos asociados", format="%.2f")
        trade_reason = st.selectbox("Motivo de la operación", ["Fundamental", "Técnico"])
        personal_notes = st.text_area("Notas personales")

        # Añadir el botón de envío
        submit_button = st.form_submit_button("Registrar Operación")

    # Procesar el registro después del envío
    if submit_button:
        # Calcular el resultado
        result_money = (exit_price - entry_price) * position_size - commission
        result_pips = (exit_price - entry_price) * 10000  # Asumiendo que es un par de divisas

        # Insertar en la base de datos
        c.execute('''INSERT INTO trades (currency_pair, open_time, close_time, order_type, entry_price, exit_price,
            stop_loss, take_profit, position_size, result_money, result_pips, spread, slippage, commission, trade_reason,
            personal_notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            (currency_pair, open_time, close_time, order_type, entry_price, exit_price, stop_loss,
            take_profit, position_size, result_money, result_pips, spread, slippage, commission, trade_reason,
            personal_notes))
        
        conn.commit()  # Guardar los cambios en la base de datos
        st.success("Operación registrada correctamente!")

# Pestaña de Estadísticas y Rendimiento
elif tab == "Estadísticas y Rendimiento":
    st.subheader("Estadísticas y Rendimiento")

    # Leer el archivo de la base de datos de operaciones
    trade_df = pd.read_sql_query("SELECT * FROM trades", conn)

    if not trade_df.empty:
        # Asegurarse de que las columnas sean del tipo correcto
        trade_df['result_money'] = trade_df['result_money'].astype(float)

        # Calcular estadísticas
        total_pnL = trade_df['result_money'].sum()
        win_rate = len(trade_df[trade_df['result_money'] > 0]) / len(trade_df) * 100
        average_profit = trade_df['result_money'].mean()
        average_loss = trade_df[trade_df['result_money'] < 0]['result_money'].mean()
        max_consecutive_wins = (trade_df['result_money'] > 0).astype(int).groupby(trade_df['result_money'].lt(0).cumsum()).sum().max()
        max_consecutive_losses = (trade_df['result_money'] < 0).astype(int).groupby(trade_df['result_money'].gt(0).cumsum()).sum().max()

        st.write(f"**Ganancias y Pérdidas Totales:** {total_pnL:.2f} €")
        st.write(f"**Tasa de Aciertos:** {win_rate:.2f}%")
        st.write(f"**Promedio de Ganancias:** {average_profit:.2f} €")
        st.write(f"**Promedio de Pérdidas:** {average_loss:.2f} €")
        st.write(f"**Máxima Racha Ganadora:** {max_consecutive_wins}")
        st.write(f"**Máxima Racha Perdedora:** {max_consecutive_losses}")

        # Gráfico de Ganancias y Pérdidas
        fig_pnl = px.histogram(trade_df, x='result_money',
                                title='Distribución de Ganancias y Pérdidas',
                                labels={'result_money': 'Resultado (en €)'},
                                template='plotly_white')
        st.plotly_chart(fig_pnl)

        # Gráfico de Ratio de Aciertos
        st.subheader("Gráfico de Ratio de Aciertos")
        fig_win_rate = px.pie(names=['Ganadoras', 'Perdedoras'],
                               values=[len(trade_df[trade_df['result_money'] > 0]),
                                       len(trade_df[trade_df['result_money'] <= 0])],
                               title='Ratio de Aciertos')
        st.plotly_chart(fig_win_rate)

    else:
        st.warning("No hay operaciones registradas. Registra al menos una operación para ver estadísticas.")

# Pestaña de Análisis de Psicología y Emociones
elif tab == "Análisis de Psicología y Emociones":
    st.subheader("Análisis de Psicología y Emociones")

    # Formulario para registrar emociones
    with st.form("emotion_form"):
        emotion_date = st.date_input("Fecha de la operación", datetime.datetime.now())
        emotion_before = st.selectbox("Emoción antes de la operación", ["Estrés", "Ansiedad", "Confianza", "Neutral"])
        emotion_during = st.selectbox("Emoción durante la operación", ["Estrés", "Ansiedad", "Confianza", "Neutral"])
        emotion_after = st.selectbox("Emoción después de la operación", ["Estrés", "Ansiedad", "Confianza", "Neutral"])
        fomo = st.checkbox("FOMO")
        impatience = st.checkbox("Impatience")
        trading_revenge = st.checkbox("Trading Revenge")
        emotional_notes = st.text_area("Notas sobre tus emociones")

        # Añadir el botón de envío
        submit_emotion = st.form_submit_button("Registrar Emoción")

    # Procesar el registro de emociones después del envío
    if submit_emotion:
        # Insertar en la base de datos
        c.execute('''INSERT INTO emotions (emotion_date, emotion_before, emotion_during, emotion_after,
            fomo, impatience, trading_revenge, emotional_notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
            (emotion_date, emotion_before, emotion_during, emotion_after, 
            int(fomo), int(impatience), int(trading_revenge), emotional_notes))
        
        conn.commit()  # Guardar los cambios en la base de datos
        st.success("Emoción registrada correctamente!")

    # Gráfico de emociones
    emotional_df = pd.read_sql_query("SELECT * FROM emotions", conn)

    if not emotional_df.empty:
        emotional_df['fomo'] = emotional_df['fomo'].map({1: 'Sí', 0: 'No'})
        emotional_df['impatience'] = emotional_df['impatience'].map({1: 'Sí', 0: 'No'})
        emotional_df['trading_revenge'] = emotional_df['trading_revenge'].map({1: 'Sí', 0: 'No'})
        
        fig_emotions = px.histogram(emotional_df, x='emotion_after', color='fomo',
                                     title='Impacto de las Emociones en el Rendimiento',
                                     labels={'emotion_after': 'Emoción Después', 'fomo': 'FOMO'},
                                     template='plotly_white')
        st.plotly_chart(fig_emotions)

    else:
        st.warning("No hay registros emocionales. Registra al menos una emoción para ver gráficos.")

# Cerrar la conexión a la base de datos
conn.close()
