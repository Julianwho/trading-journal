import streamlit as st
import pandas as pd
import datetime as dt
import base64
import matplotlib.pyplot as plt
import seaborn as sns

# Inicializa el DataFrame para almacenar las operaciones
if 'trade_df' not in st.session_state:
    st.session_state.trade_df = pd.DataFrame(columns=["Fecha y Hora de Apertura", "Precio de Entrada", "Precio de Salida", "Resultado Final", "FOMO", "Trading Revenge", "Impaciencia", "Imagen"])

# Configura la interfaz de Streamlit
st.title("Diario de Trading")
tab = st.sidebar.radio("Selecciona una pestaña", ["Registro de Operaciones", "Análisis de Psicología y Emociones", "Estadísticas y Rendimiento"])

# Pestaña: Registro de Operaciones
if tab == "Registro de Operaciones":
    st.header("Registro de Operaciones")
    
    open_datetime = st.sidebar.date_input("Fecha de Apertura", value=dt.datetime.now().date())
    open_time = st.sidebar.time_input("Hora de Apertura", value=dt.datetime.now().time())
    entry_price = st.sidebar.number_input("Precio de Entrada", format="%.2f")
    exit_price = st.sidebar.number_input("Precio de Salida", format="%.2f")
    final_result = st.sidebar.number_input("Resultado Final de la Operación", format="%.2f")
    
    # Captura las emociones
    fomo = st.sidebar.checkbox("¿Sentiste FOMO?", value=False)
    revenge = st.sidebar.checkbox("¿Hiciste Trading Revenge?", value=False)
    impatience = st.sidebar.checkbox("¿Sentiste Impaciencia?", value=False)

    # Subir imagen
    uploaded_file = st.sidebar.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])
    
    if st.sidebar.button("Registrar Operación"):
        if uploaded_file is not None:
            # Lee la imagen
            img_bytes = uploaded_file.read()
            img_base64 = base64.b64encode(img_bytes).decode()
            img_url = f"data:image/jpeg;base64,{img_base64}"
        else:
            img_url = ""

        # Agrega la operación al DataFrame
        new_entry = {
            "Fecha y Hora de Apertura": dt.datetime.combine(open_datetime, open_time),
            "Precio de Entrada": entry_price,
            "Precio de Salida": exit_price,
            "Resultado Final": final_result,
            "FOMO": fomo,
            "Trading Revenge": revenge,
            "Impaciencia": impatience,
            "Imagen": img_url
        }
        st.session_state.trade_df = st.session_state.trade_df.append(new_entry, ignore_index=True)

    # Muestra el registro de operaciones en formato de tabla
    if not st.session_state.trade_df.empty:
        # Colorear filas según el resultado final
        def color_negative_red(val):
            if val < 0:
                return 'background-color: lightcoral'
            elif val > 0:
                return 'background-color: lightgreen'
            else:
                return ''

        styled_df = st.session_state.trade_df.style.applymap(color_negative_red, subset=['Resultado Final'])
        st.dataframe(styled_df)

# Pestaña: Análisis de Psicología y Emociones
elif tab == "Análisis de Psicología y Emociones":
    st.header("Análisis de Psicología y Emociones")

    # Mostrar todas las emociones registradas
    if not st.session_state.trade_df.empty:
        st.subheader("Registro de Emociones")
        emotions_df = st.session_state.trade_df[["Fecha y Hora de Apertura", "FOMO", "Trading Revenge", "Impaciencia"]]
        st.dataframe(emotions_df)

# Pestaña: Estadísticas y Rendimiento
elif tab == "Estadísticas y Rendimiento":
    st.header("Estadísticas y Rendimiento")

    if not st.session_state.trade_df.empty:
        st.subheader("Gráficos de Rendimiento")
        
        # Calcula P&L total
        st.session_state.trade_df["P&L en Dinero"] = st.session_state.trade_df["Resultado Final"]
        st.session_state.trade_df["Fecha y Hora de Apertura"] = pd.to_datetime(st.session_state.trade_df["Fecha y Hora de Apertura"])

        # Gráfico de línea de P&L
        plt.figure(figsize=(10, 5))
        sns.lineplot(data=st.session_state.trade_df, x="Fecha y Hora de Apertura", y="P&L en Dinero", marker='o')
        plt.title("Evolución de P&L")
        plt.xlabel("Fecha y Hora de Apertura")
        plt.ylabel("P&L en Dinero")
        st.pyplot(plt)

        # Mostrar estadísticas generales
        total_trades = len(st.session_state.trade_df)
        total_profit = st.session_state.trade_df["Resultado Final"].sum()
        st.write(f"Número total de operaciones: {total_trades}")
        st.write(f"Ganancia total: {total_profit:.2f}")
