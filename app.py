import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración inicial
st.set_page_config(page_title="Trading Journal", layout="wide")

# Función para cargar los datos
@st.cache_data
def load_trade_data():
    try:
        return pd.read_csv("trades.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Pair", "Open Date", "Close Date", "Order Type", 
                                      "Entry Price", "Exit Price", "Stop Loss", 
                                      "Take Profit", "Position Size", "P&L in Pips", 
                                      "P&L in Money", "Spread", "Commission", 
                                      "Reason", "Notes", "Image"])

# Función para guardar los datos
def save_trade_data(df):
    df.to_csv("trades.csv", index=False)

# Cargar los datos de operaciones
if 'trade_df' not in st.session_state:
    st.session_state.trade_df = load_trade_data()

# Sidebar para navegación
st.sidebar.title("Navegación")
tab = st.sidebar.radio("Selecciona una pestaña", 
                        ["Registro de Operaciones", "Estadísticas y Rendimiento", 
                         "Análisis de Psicología y Emociones"])

# Pestaña: Registro de Operaciones
if tab == "Registro de Operaciones":
    st.title("Registro de Operaciones")

    # Sección para agregar nuevos registros
    st.sidebar.header("Agregar Registro de Operación")

    pair = st.sidebar.text_input("Par de divisas (o activo)")
    open_datetime = st.sidebar.datetime_input("Fecha y Hora de Apertura")
    close_datetime = st.sidebar.datetime_input("Fecha y Hora de Cierre")
    order_type = st.sidebar.selectbox("Tipo de Orden", 
                                       options=["Market", "Limit", "Stop"])
    entry_price = st.sidebar.number_input("Precio de Entrada")
    exit_price = st.sidebar.number_input("Precio de Salida")
    stop_loss = st.sidebar.number_input("Stop-Loss")
    take_profit = st.sidebar.number_input("Take-Profit")
    position_size = st.sidebar.number_input("Tamaño de la Posición", min_value=0.0)
    spread = st.sidebar.number_input("Tamaño del Spread", min_value=0.0)
    commission = st.sidebar.number_input("Comisiones", min_value=0.0)
    reason = st.sidebar.text_area("Motivo de la Operación")
    image = st.sidebar.file_uploader("Subir Imagen", type=["jpg", "png", "jpeg"])
    notes = st.sidebar.text_area("Notas Personales")

    if st.sidebar.button("Agregar Registro de Operación"):
        # Validar que los campos obligatorios no estén vacíos
        if entry_price <= 0 or exit_price <= 0:
            st.sidebar.error("El precio de entrada y salida deben ser mayores a 0.")
        else:
            # Calcular P&L
            pnl_pips = (exit_price - entry_price) / spread * 10000 if spread != 0 else 0
            pnl_money = pnl_pips * position_size
            
            # Agregar una nueva fila al DataFrame
            new_trade_row = pd.DataFrame([{
                "Pair": pair,
                "Open Date": open_datetime,
                "Close Date": close_datetime,
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
                "Notes": notes,
                "Image": image.name if image is not None else None  # Guardar nombre de la imagen
            }])
            
            # Usar pd.concat para añadir la nueva fila al DataFrame
            st.session_state.trade_df = pd.concat([st.session_state.trade_df, new_trade_row], ignore_index=True)
            
            # Guardar los datos actualizados en el archivo CSV
            save_trade_data(st.session_state.trade_df)
            
            st.sidebar.success("Registro de operación agregado exitosamente!")

    # Mostrar la tabla de registros de operaciones existentes
    st.subheader("Historial de Operaciones")
    st.dataframe(st.session_state.trade_df)

# Pestaña: Estadísticas y Rendimiento
elif tab == "Estadísticas y Rendimiento":
    st.title("Estadísticas y Rendimiento")

    if st.session_state.trade_df.empty:
        st.warning("No hay operaciones registradas para mostrar estadísticas.")
    else:
        # Calcular estadísticas
        total_trades = len(st.session_state.trade_df)
        win_trades = st.session_state.trade_df[st.session_state.trade_df["P&L in Money"] > 0]
        loss_trades = st.session_state.trade_df[st.session_state.trade_df["P&L in Money"] <= 0]
        win_rate = len(win_trades) / total_trades * 100 if total_trades > 0 else 0
        avg_win = win_trades["P&L in Money"].mean() if not win_trades.empty else 0
        avg_loss = loss_trades["P&L in Money"].mean() if not loss_trades.empty else 0

        # Gráficos
        st.subheader("Estadísticas Generales")
        st.write(f"Total de operaciones: {total_trades}")
        st.write(f"Tasa de Ganancia: {win_rate:.2f}%")
        st.write(f"Promedio de Ganancias: ${avg_win:.2f}")
        st.write(f"Promedio de Pérdidas: ${avg_loss:.2f}")

        # Gráfico de P&L
        plt.figure(figsize=(10, 5))
        sns.lineplot(data=st.session_state.trade_df, x="Open Date", y="P&L in Money", marker='o')
        plt.title("Ganancias y Pérdidas a lo Largo del Tiempo")
        plt.xlabel("Fecha de Apertura")
        plt.ylabel("P&L en Dinero")
        plt.xticks(rotation=45)
        st.pyplot(plt)

# Pestaña: Análisis de Psicología y Emociones
elif tab == "Análisis de Psicología y Emociones":
    st.title("Análisis de Psicología y Emociones")
    
    # Aquí puedes agregar el contenido que desees para esta sección.
    st.write("Pronto se implementarán herramientas para el análisis de emociones y psicología.")
