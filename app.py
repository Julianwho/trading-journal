import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de Streamlit
st.set_page_config(page_title="Trading Journal", layout="wide")

# Cargar datos
@st.cache_data
def load_trade_data():
    try:
        trade_df = pd.read_csv("trade_data.csv")
    except FileNotFoundError:
        trade_df = pd.DataFrame(columns=["Pair", "Open Date", "Close Date", "Order Type", 
                                          "Entry Price", "Exit Price", "Stop Loss", 
                                          "Take Profit", "Position Size", "P&L in Pips", 
                                          "P&L in Money", "Spread", "Commission", "Reason", 
                                          "Notes"])
    return trade_df

def save_trade_data(trade_df):
    trade_df.to_csv("trade_data.csv", index=False)

trade_df = load_trade_data()

# Pestañas
tabs = ["Registro de Operaciones", "Estadísticas y Rendimiento", "Análisis de Psicología y Emociones"]
tab = st.sidebar.selectbox("Selecciona una pestaña", tabs)

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
    commission = st.sidebar.number_input("Comisiones", min_value=0.0)
    reason = st.sidebar.selectbox("Motivo de la Operación", 
                                   options=["Fundamental", "Técnico"])
    notes = st.sidebar.text_area("Notas Personales")

    if st.sidebar.button("Agregar Registro de Operación"):
        # Validar que los campos obligatorios no estén vacíos
        if entry_price <= 0 or exit_price <= 0:
            st.sidebar.error("El precio de entrada y salida deben ser mayores a 0.")
        else:
            # Calcular P&L
            if spread == 0:
                pnl_pips = 0  # Si el spread es cero, establecemos P&L en pips a 0
                pnl_money = 0  # Similar para el P&L en dinero
            else:
                pnl_pips = (exit_price - entry_price) / spread * 10000
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

    if trade_df.empty:
        st.warning("No hay registros de operaciones disponibles.")
    else:
        # Calcular estadísticas
        total_trades = len(trade_df)
        win_trades = trade_df[trade_df["P&L in Money"] > 0]
        loss_trades = trade_df[trade_df["P&L in Money"] <= 0]

        win_rate = len(win_trades) / total_trades * 100 if total_trades > 0 else 0
        total_pnl = trade_df["P&L in Money"].sum()
        
        # Gráficos
        st.subheader("Ganancias y Pérdidas Acumuladas")
        daily_pnl = trade_df.groupby(pd.to_datetime(trade_df["Open Date"])).sum()["P&L in Money"].cumsum()
        st.line_chart(daily_pnl)

        st.subheader("Ratio de Aciertos")
        st.write(f"Ratio de Aciertos: {win_rate:.2f}%")
        st.write(f"P&L Total: ${total_pnl:.2f}")

        # Gráficos adicionales
        st.subheader("Análisis de P&L")
        fig, ax = plt.subplots()
        sns.histplot(trade_df["P&L in Money"], bins=30, kde=True, ax=ax)
        ax.axvline(0, color='red', linestyle='--')
        st.pyplot(fig)

elif tab == "Análisis de Psicología y Emociones":
    st.title("Análisis de Psicología y Emociones")

    st.sidebar.header("Diario Emocional")
    
    emotions = ["Estrés", "Ansiedad", "Confianza", "Felicidad"]
    emotion_values = {emotion: st.sidebar.slider(emotion, 0, 10, 5) for emotion in emotions}

    if st.sidebar.button("Registrar Estado Emocional"):
        st.sidebar.success("Estado emocional registrado!")

    # Gráficos de emociones
    st.subheader("Impacto de las Emociones en el Rendimiento")
    if not trade_df.empty:
        win_emotions = {emotion: emotion_values[emotion] for emotion in emotions if trade_df["P&L in Money"].sum() > 0}
        loss_emotions = {emotion: emotion_values[emotion] for emotion in emotions if trade_df["P&L in Money"].sum() <= 0}
        
        fig, ax = plt.subplots()
        ax.bar(win_emotions.keys(), win_emotions.values(), color='green', alpha=0.5, label='Operaciones Ganadoras')
        ax.bar(loss_emotions.keys(), loss_emotions.values(), color='red', alpha=0.5, label='Operaciones Perdedoras')
        ax.legend()
        ax.set_ylabel('Intensidad')
        st.pyplot(fig)

        # Registro de creencias limitantes
        st.subheader("Registro de Creencias Limitantes")
        limiting_beliefs = st.text_area("Escribe tus creencias limitantes")
        if st.button("Registrar Creencias Limitantes"):
            st.success("Creencias limitantes registradas!")

