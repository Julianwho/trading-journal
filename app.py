import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

# Archivo CSV para almacenar los datos de operaciones
TRADE_CSV_FILE = "trading_data.csv"
# Archivo CSV para almacenar los datos de emociones
EMOTION_CSV_FILE = "trading_emotions.csv"

# Función para cargar datos de operaciones
def load_trade_data():
    if os.path.exists(TRADE_CSV_FILE):
        return pd.read_csv(TRADE_CSV_FILE)
    else:
        return pd.DataFrame(columns=[
            "Pair", "Open Date", "Close Date", "Order Type", "Entry Price", 
            "Exit Price", "Stop Loss", "Take Profit", "Position Size", 
            "P&L in Pips", "P&L in Money", "Spread", "Slippage", 
            "Commission", "Reason", "Notes"
        ])

# Función para guardar datos de operaciones
def save_trade_data(df):
    df.to_csv(TRADE_CSV_FILE, index=False)

# Cargar los datos de operaciones existentes
trade_df = load_trade_data()

# Función para cargar datos de emociones
def load_emotion_data():
    if os.path.exists(EMOTION_CSV_FILE):
        return pd.read_csv(EMOTION_CSV_FILE)
    else:
        return pd.DataFrame(columns=[
            "Date", "Before Trade Emotion", 
            "During Trade Emotion", "After Trade Emotion", 
            "Limiting Belief", "Impact on Trading", 
            "FOMO", "Trading Revenge", "Impatience"
        ])

# Función para guardar datos de emociones
def save_emotion_data(df):
    df.to_csv(EMOTION_CSV_FILE, index=False)

# Cargar los datos de emociones existentes
emotion_df = load_emotion_data()

# Sidebar para seleccionar pestañas
tab = st.sidebar.selectbox("Selecciona una pestaña", 
                            ("Registro de Operaciones", 
                             "Estadísticas y Rendimiento", 
                             "Análisis de Psicología y Emociones"))

if tab == "Registro de Operaciones":
    st.title("Registro de Operaciones")

    # Sección para agregar nuevos registros
    st.sidebar.header("Agregar Registro de Operación")

    pair = st.sidebar.text_input("Par de divisas (o activo)")
    open_date = st.sidebar.date_input("Fecha y Hora de Apertura")
    close_date = st.sidebar.date_input("Fecha y Hora de Cierre")
    order_type = st.sidebar.selectbox("Tipo de Orden", 
                                       options=["Market", "Limit", "Stop"])
    entry_price = st.sidebar.number_input("Precio de Entrada")
    exit_price = st.sidebar.number_input("Precio de Salida")
    stop_loss = st.sidebar.number_input("Stop-Loss")
    take_profit = st.sidebar.number_input("Take-Profit")
    position_size = st.sidebar.number_input("Tamaño de la Posición", min_value=0.0)
    spread = st.sidebar.number_input("Tamaño del Spread", min_value=0.0)
    slippage = st.sidebar.number_input("Slippage", min_value=0.0)
    commission = st.sidebar.number_input("Comisiones", min_value=0.0)
    reason = st.sidebar.selectbox("Motivo de la Operación", 
                                   options=["Fundamental", "Técnico"])
    notes = st.sidebar.text_area("Notas Personales")

    if st.sidebar.button("Agregar Registro de Operación"):
        # Calcular P&L
        pnl_pips = (exit_price - entry_price) / (spread + slippage) * 10000
        pnl_money = pnl_pips * position_size
        
        # Agregar una nueva fila al DataFrame
        new_trade_row = {
            "Pair": pair,
            "Open Date": open_date,
            "Close Date": close_date,
            "Order Type": order_type,
            "Entry Price": entry_price,
            "Exit Price": exit_price,
            "Stop Loss": stop_loss,
            "Take Profit": take_profit,
            "Position Size": position_size,
            "P&L in Pips": pnl_pips,
            "P&L in Money": pnl_money,
            "Spread": spread,
            "Slippage": slippage,
            "Commission": commission,
            "Reason": reason,
            "Notes": notes
        }
        
        # Añadir la nueva fila al DataFrame
        trade_df = trade_df.append(new_trade_row, ignore_index=True)
        
        # Guardar los datos actualizados en el archivo CSV
        save_trade_data(trade_df)
        
        st.sidebar.success("Registro de operación agregado exitosamente!")

    # Mostrar la tabla de registros de operaciones existentes
    st.subheader("Historial de Operaciones")
    st.dataframe(trade_df)

elif tab == "Estadísticas y Rendimiento":
    st.title("Estadísticas y Rendimiento")

    if not trade_df.empty:
        # Calcular estadísticas
        total_pnl = trade_df["P&L in Money"].sum()
        win_rate = (trade_df[trade_df["P&L in Money"] > 0].shape[0] / trade_df.shape[0]) * 100
        average_pnl = trade_df["P&L in Money"].mean()
        
        # Gráficos de estadísticas
        st.subheader("Ganancias y Pérdidas Acumuladas")
        pnl_acumulado = trade_df.groupby("Open Date")["P&L in Money"].sum().cumsum()
        st.line_chart(pnl_acumulado)

        # Mostrar estadísticas
        st.write(f"Total P&L: ${total_pnl:.2f}")
        st.write(f"Ratio de Aciertos: {win_rate:.2f}%")
        st.write(f"Promedio de P&L por Operación: ${average_pnl:.2f}")

        # Gráfico de P&L por Tipo de Operación
        pnl_by_type = trade_df.groupby("Order Type")["P&L in Money"].sum().reset_index()
        fig = px.bar(pnl_by_type, x='Order Type', y='P&L in Money', 
                     title='P&L por Tipo de Operación', 
                     color='P&L in Money', color_continuous_scale='Viridis')
        st.plotly_chart(fig)

else:
    st.title("Análisis de Psicología y Emociones")

    # Sección para agregar nuevos registros emocionales
    st.sidebar.header("Agregar Registro Emocional")

    # Campos para el formulario de registro emocional
    date = st.sidebar.date_input("Fecha")
    before_trade_emotion = st.sidebar.selectbox("Emoción Antes de la Operación", 
                                                  options=["Estrés", "Ansiedad", "Confianza", "Incertidumbre"])
    during_trade_emotion = st.sidebar.selectbox("Emoción Durante la Operación", 
                                                  options=["Estrés", "Ansiedad", "Confianza", "Incertidumbre"])
    after_trade_emotion = st.sidebar.selectbox("Emoción Después de la Operación", 
                                                  options=["Estrés", "Ansiedad", "Confianza", "Incertidumbre"])
    limiting_belief = st.sidebar.text_input("Creencia Limitante")
    impact_on_trading = st.sidebar.text_area("Impacto en el Trading")

    # Casillas de verificación para emociones específicas
    fomo = st.sidebar.checkbox("¿Sentiste FOMO (miedo a perderte una oportunidad)?")
    trading_revenge = st.sidebar.checkbox("¿Tuviste impulsos de Trading Revenge (trading por venganza)?")
    impatience = st.sidebar.checkbox("¿Te sentiste impaciente durante la operación?")

    if st.sidebar.button("Agregar Registro Emocional"):
        # Agregar una nueva fila al DataFrame
        new_emotion_row = {
            "Date": date.strftime("%b %d, %Y"),
            "Before Trade Emotion": before_trade_emotion,
            "During Trade Emotion": during_trade_emotion,
            "After Trade Emotion": after_trade_emotion,
            "Limiting Belief": limiting_belief,
            "Impact on Trading": impact_on_trading,
            "FOMO": fomo,
            "Trading Revenge": trading_revenge,
            "Impatience": impatience
        }
        
        # Añadir la nueva fila al DataFrame
        emotion_df = emotion_df.append(new_emotion_row, ignore_index=True)
        
        # Guardar los datos actualizados en el archivo CSV
        save_emotion_data(emotion_df)
        
        st.sidebar.success("Registro emocional agregado exitosamente!")

    # Mostrar la tabla de registros emocionales existentes
    st.subheader("Historial de Registros Emocionales")
    st.dataframe(emotion_df)

    # Gráficos de emociones
    st.subheader("Gráficos de Emociones")

    if not emotion_df.empty:
        # Contar las emociones
        emotion_counts = emotion_df.groupby("After Trade Emotion").size().reset_index(name='Counts')
        
        # Gráfico de barras de emociones después de la operación
        fig = px.bar(emotion_counts, x='After Trade Emotion', y='Counts', 
                     title='Emociones Después de la Operación', 
                     color='Counts', color_continuous_scale='Viridis')

        fig.update_layout(template='plotly_white', xaxis_title='Emoción', yaxis_title='Cantidad de Registros')
        st.plotly_chart(fig)
