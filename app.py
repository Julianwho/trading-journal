import streamlit as st
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import base64

# Configuración inicial
if 'trade_df' not in st.session_state:
    st.session_state.trade_df = pd.DataFrame(columns=["Open Date", "Entry Price", "Exit Price", "P&L in Money", "Final Result", "Image", "Motivo de la Operación", "FOMO", "Trading Revenge", "Impatience"])

# Función para cargar imágenes
def load_image(image_file):
    img = base64.b64encode(image_file.read()).decode()
    return f'<img src="data:image/png;base64,{img}" width="300"/>'

# Selección de pestaña
tab = st.sidebar.selectbox("Selecciona una pestaña", ["Registro de Operaciones", "Estadísticas y Rendimiento", "Análisis de Psicología y Emociones"])

# Pestaña Registro de Operaciones
if tab == "Registro de Operaciones":
    st.header("Registro de Operaciones")

    # Entrada de datos de la operación
    try:
        open_date = st.sidebar.date_input("Fecha de Apertura", value=dt.date.today())
        open_time = st.sidebar.time_input("Hora de Apertura", value=dt.datetime.now().time())
        open_datetime = dt.datetime.combine(open_date, open_time)
        
        entry_price = st.sidebar.number_input("Precio de Entrada", format="%.2f")
        exit_price = st.sidebar.number_input("Precio de Salida", format="%.2f")
        final_result = st.sidebar.number_input("Resultado Final de la Operación", format="%.2f", step=0.01)
        motivo_operacion = st.text_area("Motivo de la Operación")
        image_file = st.file_uploader("Sube una imagen", type=["jpg", "png", "jpeg"])

        # Checkboxes para emociones
        fomo = st.checkbox("¿Experimentaste FOMO en esta operación?")
        trading_revenge = st.checkbox("¿Experimentaste Trading Revenge?")
        impatience = st.checkbox("¿Experimentaste Impaciencia?")

        if st.sidebar.button("Agregar Operación"):
            # Cálculo de P&L
            pnl = final_result  # Tomar el resultado final directamente
            new_trade_row = {
                "Open Date": open_datetime,
                "Entry Price": entry_price,
                "Exit Price": exit_price,
                "P&L in Money": pnl,
                "Final Result": final_result,
                "Image": image_file,
                "Motivo de la Operación": motivo_operacion,
                "FOMO": fomo,
                "Trading Revenge": trading_revenge,
                "Impatience": impatience
            }
            st.session_state.trade_df = st.session_state.trade_df.append(new_trade_row, ignore_index=True)

        # Mostrar el registro de operaciones
        st.subheader("Operaciones Registradas")
        if not st.session_state.trade_df.empty:
            for index, row in st.session_state.trade_df.iterrows():
                st.write(f"**Fecha y Hora:** {row['Open Date']}")
                st.write(f"**Precio de Entrada:** {row['Entry Price']}")
                st.write(f"**Precio de Salida:** {row['Exit Price']}")
                st.write(f"**P&L en Dinero:** {row['P&L in Money']}")
                st.write(f"**Resultado Final:** {row['Final Result']}")
                st.markdown(load_image(row['Image']) if row['Image'] is not None else "No hay imagen", unsafe_allow_html=True)
                st.write(f"**Motivo de la Operación:** {row['Motivo de la Operación']}")
                st.write(f"**FOMO:** {'Sí' if row['FOMO'] else 'No'}, **Trading Revenge:** {'Sí' if row['Trading Revenge'] else 'No'}, **Impatience:** {'Sí' if row['Impatience'] else 'No'}")
                st.write("---")

    except Exception as e:
        st.error(f"Ocurrió un error: {e}")

# Pestaña Estadísticas y Rendimiento
elif tab == "Estadísticas y Rendimiento":
    st.header("Estadísticas y Rendimiento")
    if not st.session_state.trade_df.empty:
        try:
            # Convertir las fechas a datetime
            st.session_state.trade_df['Open Date'] = pd.to_datetime(st.session_state.trade_df['Open Date'])

            # Gráficos de P&L
            plt.figure(figsize=(10, 6))
            sns.lineplot(data=st.session_state.trade_df, x="Open Date", y="P&L in Money", marker='o')
            plt.title("Ganancias y Pérdidas Acumuladas")
            plt.xlabel("Fecha")
            plt.ylabel("P&L en Dinero")
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(plt)

            # Otras estadísticas
            win_rate = (st.session_state.trade_df['P&L in Money'] > 0).mean() * 100
            average_pnl = st.session_state.trade_df['P&L in Money'].mean()
            max_win_streak = (st.session_state.trade_df['P&L in Money'] > 0).astype(int).groupby(st.session_state.trade_df['Open Date'].dt.to_period('M')).cumsum().max()
            max_loss_streak = (st.session_state.trade_df['P&L in Money'] < 0).astype(int).groupby(st.session_state.trade_df['Open Date'].dt.to_period('M')).cumsum().max()

            st.write(f"**Ratio de Aciertos:** {win_rate:.2f}%")
            st.write(f"**Promedio de Ganancias/Pérdidas:** {average_pnl:.2f}")
            st.write(f"**Máxima Racha de Operaciones Ganadoras:** {max_win_streak}")
            st.write(f"**Máxima Racha de Operaciones Perdedoras:** {max_loss_streak}")

        except Exception as e:
            st.error(f"Ocurrió un error: {e}")

# Pestaña Análisis de Psicología y Emociones
elif tab == "Análisis de Psicología y Emociones":
    st.header("Análisis de Psicología y Emociones")
    st.write("Aquí podrás analizar tus emociones y registrar tus estados anímicos.")
