import streamlit as st
import pandas as pd
import os

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

# Mostrar la tabla existente
st.subheader("Historial de Operaciones")
st.dataframe(df)

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
