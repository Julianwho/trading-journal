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
        return pd.DataFrame(columns=["Status", "Date", "Symbol", "Entry", "Exit", "Qty", "Return $"])

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

status = st.sidebar.selectbox("Status", options=["WIN", "LOSS"])
date = st.sidebar.date_input("Fecha")
symbol = st.sidebar.text_input("Símbolo")
entry = st.sidebar.number_input("Precio de Entrada", min_value=0.0, format="%.2f")
exit_price = st.sidebar.number_input("Precio de Salida", min_value=0.0, format="%.2f")
qty = st.sidebar.number_input("Cantidad", min_value=1)
return_dollars = (exit_price - entry) * qty

if st.sidebar.button("Agregar Operación"):
    # Agregar una nueva fila al DataFrame
    new_row = {
        "Status": status,
        "Date": date.strftime("%b %d, %Y"),
        "Symbol": symbol,
        "Entry": entry,
        "Exit": exit_price,
        "Qty": qty,
        "Return $": return_dollars
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
st.line_chart(df["Return $"])
