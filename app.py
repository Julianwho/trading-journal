import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import os

# Configuración inicial
st.title("Trading Journal")
tab = st.sidebar.selectbox("Selecciona una pestaña", 
                            ["Registro de Operaciones", 
                             "Estadísticas y Rendimiento", 
                             "Análisis de Psicología y Emociones"])

# Crear un archivo CSV si no existe para el diario emocional
if not os.path.isfile('emotional_journal.csv'):
    df = pd.DataFrame(columns=["Fecha", "Emotion Before", "Emotion During", "Emotion After", "Limiting Beliefs"])
    df.to_csv('emotional_journal.csv', index=False)

# Crear un archivo CSV si no existe para las operaciones
if not os.path.isfile('trade_journal.csv'):
    trade_df = pd.DataFrame(columns=["Par de divisas", "Fecha de Apertura", "Fecha de Cierre", "Tipo de Orden", 
                                      "Precio de Entrada", "Precio de Salida", "Stop-Loss", "Take-Profit", 
                                      "Tamaño de la Posición", "Resultado en Pips", "Resultado en Dinero", 
                                      "Spread", "Slippage", "Comisiones", "Motivo de la Operación", "Notas"])
    trade_df.to_csv('trade_journal.csv', index=False)

# Pestaña de Registro de Operaciones
if tab == "Registro de Operaciones":
    st.subheader("Registro de Operaciones Completo")

    # Formulario para registrar operaciones
    with st.form("trade_form"):
        currency_pair = st.text_input("Par de divisas (o activo)")
        open_datetime = st.date_input("Fecha de Apertura", datetime.date.today())
        close_datetime = st.date_input("Fecha de Cierre", datetime.date.today())
        order_type = st.selectbox("Tipo de Orden", options=["Market", "Limit", "Stop"])
        entry_price = st.number_input("Precio de Entrada", min_value=0.0, format="%.2f")
        exit_price = st.number_input("Precio de Salida", min_value=0.0, format="%.2f")
        stop_loss = st.number_input("Stop-Loss", min_value=0.0, format="%.2f")
        take_profit = st.number_input("Take-Profit", min_value=0.0, format="%.2f")
        position_size = st.number_input("Tamaño de la Posición (en lotes)", min_value=0.0, format="%.2f")
        spread = st.number_input("Tamaño del Spread", min_value=0.0, format="%.2f")
        slippage = st.number_input("Slippage", min_value=0.0, format="%.2f")
        commissions = st.number_input("Comisiones", min_value=0.0, format="%.2f")
        trade_reason = st.selectbox("Motivo de la Operación", options=["Fundamental", "Técnico"])
        notes = st.text_area("Notas Personales")

        submit_button = st.form_submit_button("Registrar Operación")

    if submit_button:
        # Calcular resultados
        result_pips = (exit_price - entry_price) / (0.0001 if order_type in ["Market", "Limit"] else 0.01)
        result_money = result_pips * position_size - commissions
        
        # Guardar en el archivo CSV
        trade_entry = {
            "Par de divisas": currency_pair,
            "Fecha de Apertura": open_datetime,
            "Fecha de Cierre": close_datetime,
            "Tipo de Orden": order_type,
            "Precio de Entrada": entry_price,
            "Precio de Salida": exit_price,
            "Stop-Loss": stop_loss,
            "Take-Profit": take_profit,
            "Tamaño de la Posición": position_size,
            "Resultado en Pips": result_pips,
            "Resultado en Dinero": result_money,
            "Spread": spread,
            "Slippage": slippage,
            "Comisiones": commissions,
            "Motivo de la Operación": trade_reason,
            "Notas": notes
        }

        # Leer el archivo CSV existente
        trade_df = pd.read_csv('trade_journal.csv')
        # Agregar la nueva entrada
        trade_df = trade_df.append(trade_entry, ignore_index=True)
        # Guardar de nuevo en el CSV
        trade_df.to_csv('trade_journal.csv', index=False)

        st.success("Operación registrada exitosamente!")

# Pestaña de Estadísticas y Rendimiento
elif tab == "Estadísticas y Rendimiento":
    st.subheader("Estadísticas y Rendimiento")

    # Leer el archivo CSV de operaciones
    trade_df = pd.read_csv('trade_journal.csv')

    if not trade_df.empty:
        # Calcular estadísticas
        trade_df['Resultado en Dinero'] = trade_df['Resultado en Dinero'].astype(float)
        total_pnL = trade_df['Resultado en Dinero'].sum()
        win_rate = len(trade_df[trade_df['Resultado en Dinero'] > 0]) / len(trade_df) * 100
        average_profit = trade_df['Resultado en Dinero'].mean()
        average_loss = trade_df[trade_df['Resultado en Dinero'] < 0]['Resultado en Dinero'].mean()
        
        st.write(f"Ganancias y Pérdidas Totales: {total_pnL:.2f} €")
        st.write(f"Tasa de Aciertos: {win_rate:.2f}%")
        st.write(f"Promedio de Ganancias: {average_profit:.2f} €")
        st.write(f"Promedio de Pérdidas: {average_loss:.2f} €")

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

# Pestaña de Análisis de Psicología y Emociones
elif tab == "Análisis de Psicología y Emociones":
    st.subheader("Análisis de Psicología y Emociones")

    # Sección para seleccionar la operación
    st.subheader("Selecciona una Operación para Analizar")
    trade_df = pd.read_csv('trade_journal.csv')

    if not trade_df.empty:
        selected_trade = st.selectbox("Selecciona la operación", trade_df.index, 
                                       format_func=lambda x: f"{trade_df['Par de divisas'][x]} - {trade_df['Resultado en Dinero'][x]:.2f} €")
        selected_trade_details = trade_df.iloc[selected_trade]
        st.write("Detalles de la Operación Seleccionada:")
        st.json(selected_trade_details.to_dict())

    # Sección para registrar emociones
    st.subheader("Diario Emocional")

    # Campo para ingresar la fecha
    date = st.date_input("Fecha de la operación", datetime.date.today())
    
    # Formulario para registrar emociones
    emotion_before = st.selectbox("¿Cómo te sentías antes de la operación?", 
                                   options=["Estrés", "Ansiedad", "Confianza", "Indecisión", "Tranquilo", 
                                            "FOMO", "Impaciencia", "Trading Revenge"])
    emotion_during = st.selectbox("¿Cómo te sentías durante la operación?", 
                                   options=["Estrés", "Ansiedad", "Confianza", "Indecisión", "Tranquilo", 
                                            "FOMO", "Impaciencia", "Trading Revenge"])
    emotion_after = st.selectbox("¿Cómo te sentías después de la operación?", 
                                  options=["Estrés", "Ansiedad", "Confianza", "Indecisión", "Tranquilo", 
                                           "FOMO", "Impaciencia", "Trading Revenge"])

    # Registrar creencias limitantes
    limiting_beliefs = st.text_area("Identifica y analiza tus creencias limitantes")

    # Botón para guardar las emociones
    if st.button("Guardar Emociones"):
        # Agregar registro de emociones a un archivo CSV
        emotion_entry = {
            "Fecha": date,
            "Emotion Before": emotion_before,
            "Emotion During": emotion_during,
            "Emotion After": emotion_after,
            "Limiting Beliefs": limiting_beliefs
        }
        
        # Leer el archivo CSV existente
        df = pd.read_csv('emotional_journal.csv')
        # Agregar la nueva entrada
        df = df.append(emotion_entry, ignore_index=True)
        # Guardar de nuevo en el CSV
         df.to_csv('emotional_journal.csv', index=False)

        st.success("Emociones guardadas exitosamente!")

    # Gráfico de emociones
    if not trade_df.empty:
        emotional_df = pd.read_csv('emotional_journal.csv')
        
        if not emotional_df.empty:
            emotional_df['Resultado'] = emotional_df['Fecha'].map(dict(zip(trade_df['Fecha de Cierre'], trade_df['Resultado en Dinero'])))
            emotional_df["Emoción Antes"] = emotional_df["Emotion Before"].apply(lambda x: ["Estrés", "Ansiedad", "Confianza", "Indecisión", "Tranquilo", "FOMO", "Impaciencia", "Trading Revenge"].index(x) + 1)
            emotional_df["Emoción Durante"] = emotional_df["Emotion During"].apply(lambda x: ["Estrés", "Ansiedad", "Confianza", "Indecisión", "Tranquilo", "FOMO", "Impaciencia", "Trading Revenge"].index(x) + 1)
            emotional_df["Emoción Después"] = emotional_df["Emotion After"].apply(lambda x: ["Estrés", "Ansiedad", "Confianza", "Indecisión", "Tranquilo", "FOMO", "Impaciencia", "Trading Revenge"].index(x) + 1)

            # Gráfico de emociones
            fig_emotions = px.box(emotional_df, x="Resultado", y=["Emoción Antes", "Emoción Durante", "Emoción Después"],
                                   labels={"value": "Nivel de Emoción", "variable": "Estado Emocional"},
                                   title="Impacto Emocional por Resultado de la Operación",
                                   color="Resultado")

            fig_emotions.update_layout(template='plotly_white', hovermode='x unified')

            st.plotly_chart(fig_emotions)

    # Análisis de creencias limitantes
    st.subheader("Análisis de Creencias Limitantes")
    st.write("Aquí puedes reflexionar sobre cómo estas creencias afectan tus decisiones de trading.")
