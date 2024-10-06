import streamlit as st
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

# Configurar la página
st.set_page_config(page_title="Trading Journal", layout="wide")

# Cargar datos
try:
    trade_df = pd.read_csv("trades.csv")
    # Convertir las fechas a formato datetime
    trade_df['Fecha y Hora de Apertura'] = pd.to_datetime(trade_df['Fecha y Hora de Apertura'])
    trade_df['Fecha y Hora de Cierre'] = pd.to_datetime(trade_df['Fecha y Hora de Cierre'])
except FileNotFoundError:
    trade_df = pd.DataFrame(columns=["Par de Divisas", "Fecha y Hora de Apertura", "Fecha y Hora de Cierre",
                                      "Tipo de Orden", "Precio de Entrada", "Precio de Salida", "Stop-Loss",
                                      "Take-Profit", "Tamaño de la Posición", "Resultado en Pips", 
                                      "Resultado en Dinero", "Comisiones", "Motivo", "Notas", "Imagen"])

# Pestañas
tabs = ["Registro de Operaciones", "Estadísticas y Rendimiento", "Análisis de Psicología y Emociones"]
tab = st.sidebar.selectbox("Selecciona una pestaña", tabs)

if tab == "Registro de Operaciones":
    st.header("Registro de Operaciones")

    # Inputs para registrar operaciones
    pair = st.sidebar.selectbox("Par de Divisas", ["EUR/USD", "GBP/USD", "USD/JPY"])
    open_datetime = st.sidebar.datetime_input("Fecha y Hora de Apertura", value=datetime.datetime.now())
    close_datetime = st.sidebar.datetime_input("Fecha y Hora de Cierre", value=datetime.datetime.now())
    order_type = st.sidebar.selectbox("Tipo de Orden", ["Market", "Limit", "Stop"])
    entry_price = st.sidebar.number_input("Precio de Entrada", min_value=0.0)
    exit_price = st.sidebar.number_input("Precio de Salida", min_value=0.0)
    stop_loss = st.sidebar.number_input("Stop-Loss", min_value=0.0)
    take_profit = st.sidebar.number_input("Take-Profit", min_value=0.0)
    position_size = st.sidebar.number_input("Tamaño de la Posición", min_value=0.0)
    commissions = st.sidebar.number_input("Comisiones", min_value=0.0)
    final_result = st.sidebar.number_input("Resultado de la Operación Final", min_value=-np.inf, max_value=np.inf)

    # Espacio para subir imágenes
    image = st.sidebar.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])

    if st.sidebar.button("Registrar Operación"):
        pnl_pips = (exit_price - entry_price) * 10000  # Supongamos que son pips
        pnl_money = final_result  # Usamos el resultado de la operación final
        new_trade_row = {
            "Par de Divisas": pair,
            "Fecha y Hora de Apertura": open_datetime,
            "Fecha y Hora de Cierre": close_datetime,
            "Tipo de Orden": order_type,
            "Precio de Entrada": entry_price,
            "Precio de Salida": exit_price,
            "Stop-Loss": stop_loss,
            "Take-Profit": take_profit,
            "Tamaño de la Posición": position_size,
            "Resultado en Pips": pnl_pips,
            "Resultado en Dinero": pnl_money,
            "Comisiones": commissions,
            "Motivo": "Ingresado manualmente",
            "Notas": "Ingresado manualmente",
            "Imagen": image
        }
        trade_df = trade_df.append(new_trade_row, ignore_index=True)

        # Guardar el DataFrame actualizado
        trade_df.to_csv("trades.csv", index=False)

    # Mostrar el registro de operaciones
    for index, row in trade_df.iterrows():
        st.subheader(f"Operación {index + 1}")
        st.write(f"Par de Divisas: {row['Par de Divisas']}")
        st.write(f"Fecha y Hora de Apertura: {row['Fecha y Hora de Apertura']}")
        st.write(f"Fecha y Hora de Cierre: {row['Fecha y Hora de Cierre']}")
        st.write(f"Tipo de Orden: {row['Tipo de Orden']}")
        st.write(f"Precio de Entrada: {row['Precio de Entrada']}")
        st.write(f"Precio de Salida: {row['Precio de Salida']}")
        st.write(f"Stop-Loss: {row['Stop-Loss']}")
        st.write(f"Take-Profit: {row['Take-Profit']}")
        st.write(f"Tamaño de la Posición: {row['Tamaño de la Posición']}")
        st.write(f"Resultado en Pips: {row['Resultado en Pips']}")
        st.write(f"Resultado en Dinero: {row['Resultado en Dinero']}")
        st.write(f"Comisiones: {row['Comisiones']}")
        st.write(f"Motivo: {row['Motivo']}")
        st.write(f"Notas: {row['Notas']}")

        # Mostrar imagen si existe
        if row['Imagen'] is not None:
            st.image(row['Imagen'], caption="Imagen de la operación", use_column_width=True)

if tab == "Estadísticas y Rendimiento":
    st.header("Estadísticas y Rendimiento")
    if not trade_df.empty:
        # Asegurarse de que las fechas son del tipo datetime
        trade_df['Fecha y Hora de Apertura'] = pd.to_datetime(trade_df['Fecha y Hora de Apertura'])
        
        # Calcular estadísticas
        total_trades = trade_df.shape[0]
        winning_trades = trade_df[trade_df["Resultado en Dinero"] > 0].shape[0]
        losing_trades = trade_df[trade_df["Resultado en Dinero"] < 0].shape[0]
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        total_pnl = trade_df["Resultado en Dinero"].sum()

        st.subheader("Resumen de Estadísticas")
        st.write(f"Total de Operaciones: {total_trades}")
        st.write(f"Operaciones Ganadoras: {winning_trades}")
        st.write(f"Operaciones Perdedoras: {losing_trades}")
        st.write(f"Tasa de Éxito (Win Rate): {win_rate:.2f}%")
        st.write(f"P&L Total: {total_pnl:.2f}")

        # Gráfico de resultados
        plt.figure(figsize=(10, 5))
        plt.plot(trade_df["Fecha y Hora de Apertura"], trade_df["Resultado en Dinero"].cumsum(), marker='o')
        plt.title("P&L Acumulado")
        plt.xlabel("Fecha y Hora de Apertura")
        plt.ylabel("P&L Acumulado")
        st.pyplot(plt)

if tab == "Análisis de Psicología y Emociones":
    st.header("Análisis de Psicología y Emociones")
    # Aquí se implementará el análisis de psicología y emociones
    st.write("Esta sección estará disponible en futuras actualizaciones.")
