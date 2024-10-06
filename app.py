import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# Configurar el título de la aplicación
st.title("Trading Journal")

# Seleccionar la pestaña
tabs = ["Registro de Operaciones", "Estadísticas y Rendimiento", "Análisis de Psicología y Emociones"]
tab = st.sidebar.selectbox("Selecciona una pestaña", tabs)

# Ruta del archivo CSV
file_path = 'trade_journal.csv'

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

        submitted = st.form_submit_button("Registrar Operación")

        if submitted:
            # Calcular el resultado
            result_money = (exit_price - entry_price) * position_size - commission
            result_pips = (exit_price - entry_price) * 10000  # Asumiendo que es un par de divisas

            # Crear un DataFrame para guardar la operación
            trade_data = {
                "Par de divisas": currency_pair,
                "Fecha Apertura": open_time,
                "Fecha Cierre": close_time,
                "Tipo de Orden": order_type,
                "Precio de Entrada": entry_price,
                "Precio de Salida": exit_price,
                "Stop-Loss": stop_loss,
                "Take-Profit": take_profit,
                "Tamaño de la Posición": position_size,
                "Resultado en Dinero": result_money,
                "Resultado en Pips": result_pips,
                "Spread": spread,
                "Slippage": slippage,
                "Comisiones": commission,
                "Motivo": trade_reason,
                "Notas": personal_notes,
            }

            # Guardar en CSV
            if not pd.DataFrame(trade_data).empty:
                df = pd.DataFrame([trade_data])
                df.to_csv(file_path, mode='a', header=not pd.io.common.file_exists(file_path), index=False)

            st.success("Operación registrada correctamente!")

# Pestaña de Estadísticas y Rendimiento
elif tab == "Estadísticas y Rendimiento":
    st.subheader("Estadísticas y Rendimiento")

    # Leer el archivo CSV de operaciones
    trade_df = pd.read_csv(file_path)

    if not trade_df.empty:
        # Asegurarse de que las columnas sean del tipo correcto
        trade_df['Resultado en Dinero'] = trade_df['Resultado en Dinero'].astype(float)

        # Calcular estadísticas
        total_pnL = trade_df['Resultado en Dinero'].sum()
        win_rate = len(trade_df[trade_df['Resultado en Dinero'] > 0]) / len(trade_df) * 100
        average_profit = trade_df['Resultado en Dinero'].mean()
        average_loss = trade_df[trade_df['Resultado en Dinero'] < 0]['Resultado en Dinero'].mean()
        max_consecutive_wins = (trade_df['Resultado en Dinero'] > 0).astype(int).groupby(trade_df['Resultado en Dinero'].lt(0).cumsum()).sum().max()
        max_consecutive_losses = (trade_df['Resultado en Dinero'] < 0).astype(int).groupby(trade_df['Resultado en Dinero'].gt(0).cumsum()).sum().max()

        st.write(f"**Ganancias y Pérdidas Totales:** {total_pnL:.2f} €")
        st.write(f"**Tasa de Aciertos:** {win_rate:.2f}%")
        st.write(f"**Promedio de Ganancias:** {average_profit:.2f} €")
        st.write(f"**Promedio de Pérdidas:** {average_loss:.2f} €")
        st.write(f"**Máxima Racha Ganadora:** {max_consecutive_wins}")
        st.write(f"**Máxima Racha Perdedora:** {max_consecutive_losses}")

        # Gráfico de Ganancias y Pérdidas
        fig_pnl = px.histogram(trade_df, x='Resultado en Dinero',
                                title='Distribución de Ganancias y Pérdidas',
                                labels={'Resultado en Dinero': 'Resultado (en €)'},
                                template='plotly_white')
        st.plotly_chart(fig_pnl)

        # Gráfico de Ratio de Aciertos
        st.subheader("Gráfico de Ratio de Aciertos")
        fig_win_rate = px.pie(names=['Ganadoras', 'Perdedoras'],
                               values=[len(trade_df[trade_df['Resultado en Dinero'] > 0]),
                                       len(trade_df[trade_df['Resultado en Dinero'] <= 0])],
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

        submitted_emotion = st.form_submit_button("Registrar Emoción")

        if submitted_emotion:
            # Guardar las emociones en un DataFrame
            emotion_data = {
                "Fecha": emotion_date,
                "Emotion Before": emotion_before,
                "Emotion During": emotion_during,
                "Emotion After": emotion_after,
                "FOMO": fomo,
                "Impatience": impatience,
                "Trading Revenge": trading_revenge,
                "Emotional Notes": emotional_notes,
            }

            # Guardar en CSV
            emotion_df = pd.DataFrame([emotion_data])
            emotion_df.to_csv('emotional_journal.csv', mode='a', header=not pd.io.common.file_exists('emotional_journal.csv'), index=False)

            st.success("Emoción registrada correctamente!")

    # Gráfico de emociones
    emotional_df = pd.read_csv('emotional_journal.csv') if pd.io.common.file_exists('emotional_journal.csv') else pd.DataFrame()

    if not emotional_df.empty:
        emotional_df['FOMO'] = emotional_df['FOMO'].map({True: 'Sí', False: 'No'})
        emotional_df['Impatience'] = emotional_df['Impatience'].map({True: 'Sí', False: 'No'})
        emotional_df['Trading Revenge'] = emotional_df['Trading Revenge'].map({True: 'Sí', False: 'No'})

        # Gráfico de emociones
        fig_emotions = px.box(emotional_df, x="Emotion After",
                               title="Impacto Emocional por Resultado de la Operación",
                               labels={"Emotion After": "Estado Emocional"},
                               color="FOMO")

        fig_emotions.update_layout(template='plotly_white', hovermode='x unified')
        st.plotly_chart(fig_emotions)

    # Análisis de creencias limitantes
    st.subheader("Análisis de Creencias Limitantes")
    st.write("Aquí puedes reflexionar sobre cómo estas creencias afectan tus decisiones de trading.")
