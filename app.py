import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Archivo CSV para almacenar los datos
CSV_FILE = "trading_journal.csv"

# Configurar la página de Streamlit
st.set_page_config(page_title="Trading Journal", layout="wide")

# Función para cargar datos
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=[
            "Status", "Date Open", "Date Close", "Symbol", 
            "Order Type", "Entry Price", "Exit Price", 
            "Position Size", "Result (Pips)", "Result ($)", 
            "Spread", "Slippage", "Commissions", 
            "Reason", "Notes"
        ])

# Función para guardar datos
def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# Cargar los datos existentes
df = load_data()

# Título del Journal
st.title("Trading Journal")

# Navegación entre pestañas
tab = st.sidebar.selectbox("Selecciona una pestaña", ["Registro de Operaciones", "Estadísticas y Rendimiento"])

if tab == "Registro de Operaciones":
    # Sección para agregar nuevas operaciones
    st.sidebar.header("Agregar Nueva Operación")

    # Campos para el formulario de registro
    status = st.sidebar.selectbox("Status", options=["WIN", "LOSS"])
    date_open = st.sidebar.date_input("Fecha de Apertura")
    date_close = st.sidebar.date_input("Fecha de Cierre")
    symbol = st.sidebar.text_input("Par de Divisas / Activo")
    order_type = st.sidebar.selectbox("Tipo de Orden", options=["Market", "Limit", "Stop"])
    entry_price = st.sidebar.number_input("Precio de Entrada", min_value=0.0, format="%.2f")
    exit_price = st.sidebar.number_input("Precio de Salida", min_value=0.0, format="%.2f")
    position_size = st.sidebar.number_input("Tamaño de la Posición", min_value=1)
    spread = st.sidebar.number_input("Tamaño del Spread", min_value=0.0, format="%.2f")
    slippage = st.sidebar.number_input("Slippage", min_value=0.0, format="%.2f")
    commissions = st.sidebar.number_input("Comisiones", min_value=0.0, format="%.2f")
    reason = st.sidebar.selectbox("Motivo de la Operación", options=["Fundamental", "Técnico"])
    notes = st.sidebar.text_area("Notas Personales")

    # Calcular el resultado en pips y en dólares
    result_pips = (exit_price - entry_price) * 10000  # Suponiendo que son pares de divisas
    result_dollars = (exit_price - entry_price) * position_size

    if st.sidebar.button("Agregar Operación"):
        # Agregar una nueva fila al DataFrame
        new_row = {
            "Status": status,
            "Date Open": date_open.strftime("%b %d, %Y"),
            "Date Close": date_close.strftime("%b %d, %Y"),
            "Symbol": symbol,
            "Order Type": order_type,
            "Entry Price": entry_price,
            "Exit Price": exit_price,
            "Position Size": position_size,
            "Result (Pips)": result_pips,
            "Result ($)": result_dollars,
            "Spread": spread,
            "Slippage": slippage,
            "Commissions": commissions,
            "Reason": reason,
            "Notes": notes
        }
        
        # Añadir la nueva fila al DataFrame
        df = df.append(new_row, ignore_index=True)
        
        # Guardar los datos actualizados en el archivo CSV
        save_data(df)
        
        st.sidebar.success("Operación agregada exitosamente!")

    # Mostrar la tabla existente
    st.subheader("Historial de Operaciones")
    st.dataframe(df)

    # Estadísticas generales
    st.subheader("Estadísticas Generales")
    col1, col2, col3 = st.columns(3)

    with col1:
        total_trades = len(df)
        st.metric("Total Trades", total_trades)

    with col2:
        win_trades = len(df[df['Status'] == "WIN"])
        st.metric("Winning Trades", win_trades)

    with col3:
        loss_trades = len(df[df['Status'] == "LOSS"])
        st.metric("Losing Trades", loss_trades)

    # Mostrar gráfico interactivo de retornos
    st.subheader("Gráfico de Retornos")
    st.line_chart(df["Result ($)"])

elif tab == "Estadísticas y Rendimiento":
    # Título de la sección
    st.title("Estadísticas y Rendimiento")

    # Cálculos de estadísticas
    df["Result ($)"] = df["Result ($)"].astype(float)  # Asegúrate de que sea tipo float
    df["Date Close"] = pd.to_datetime(df["Date Close"])  # Convertir a tipo datetime

    # Ganancias y pérdidas acumuladas
    df['Cumulative P&L'] = df['Result ($)'].cumsum()

    # Ratio de aciertos (win rate)
    total_trades = len(df)
    win_trades = len(df[df['Status'] == "WIN"])
    win_rate = (win_trades / total_trades) * 100 if total_trades > 0 else 0

    # Expectativa de operación
    expectation = df['Result ($)'].mean()

    # Promedio de ganancias/pérdidas por operación
    avg_gain = df[df['Status'] == "WIN"]['Result ($)'].mean() if win_trades > 0 else 0
    avg_loss = df[df['Status'] == "LOSS"]['Result ($)'].mean() if total_trades - win_trades > 0 else 0

    # Máxima racha de operaciones ganadoras y perdedoras
    df['Win Streak'] = df['Status'].eq("WIN").astype(int).groupby(df['Status'].ne(df['Status'].shift()).cumsum()).cumsum()
    df['Loss Streak'] = df['Status'].eq("LOSS").astype(int).groupby(df['Status'].ne(df['Status'].shift()).cumsum()).cumsum()

    max_win_streak = df['Win Streak'].max()
    max_loss_streak = df['Loss Streak'].max()

    # Gráficos de estadísticas
    st.subheader("Ganancias y Pérdidas Acumuladas")
    fig = px.line(df, x='Date Close', y='Cumulative P&L', title='P&L Acumulado')
    st.plotly_chart(fig)

    st.subheader("Estadísticas Generales")
    st.metric("Win Rate (%)", win_rate)
    st.metric("Expectativa de Operación ($)", expectation)
    st.metric("Promedio de Ganancias ($)", avg_gain)
    st.metric("Promedio de Pérdidas ($)", avg_loss)
    st.metric("Máxima Racha de Ganancias", max_win_streak)
    st.metric("Máxima Racha de Pérdidas", max_loss_streak)

    # Comparación por tipo de operación
    # Suponiendo que tengas una columna "Tipo de Operación" en tu DataFrame
    if 'Order Type' in df.columns:
        order_type_stats = df.groupby('Order Type')['Result ($)'].sum().reset_index()
        fig2 = px.bar(order_type_stats, x='Order Type', y='Result ($)', title='Ganancias/Pérdidas por Tipo de Operación')
        st.plotly_chart(fig2)

    # Análisis adicional aquí...
