import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import yfinance as yf

# Inicialización de la sesión de estado
if 'operations' not in st.session_state:
    st.session_state['operations'] = pd.DataFrame(columns=[
        'Date', 'Symbol', 'Order Type', 'Entry Price', 'Exit Price', 'Stop Loss', 'Take Profit',
        'Position Size', 'Result (pips)', 'Result ($)', 'Spread', 'Slippage', 'Commissions',
        'Reason', 'Notes', 'Emotion Before', 'Emotion During', 'Emotion After'
    ])

# Función para agregar una operación
def add_operation(date, symbol, order_type, entry_price, exit_price, stop_loss, take_profit,
                  position_size, spread, slippage, commissions, reason, notes,
                  emotion_before, emotion_during, emotion_after):
    result_pips = (exit_price - entry_price) * 10000 if 'USD' in symbol else (exit_price - entry_price) * 100
    result_money = (exit_price - entry_price) * position_size - commissions
    
    new_row = {
        'Date': date,
        'Symbol': symbol,
        'Order Type': order_type,
        'Entry Price': entry_price,
        'Exit Price': exit_price,
        'Stop Loss': stop_loss,
        'Take Profit': take_profit,
        'Position Size': position_size,
        'Result (pips)': result_pips,
        'Result ($)': result_money,
        'Spread': spread,
        'Slippage': slippage,
        'Commissions': commissions,
        'Reason': reason,
        'Notes': notes,
        'Emotion Before': emotion_before,
        'Emotion During': emotion_during,
        'Emotion After': emotion_after
    }
    st.session_state['operations'] = pd.concat([st.session_state['operations'], pd.DataFrame([new_row])], ignore_index=True)

# Interfaz principal
st.title("Trading Journal Dashboard")

# Pestañas
tab1, tab2, tab3 = st.tabs(["Registro de Operaciones", "Estadísticas y Rendimiento", "Análisis Psicológico"])

with tab1:
    st.header("Registro de Operaciones")
    
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Fecha", datetime.today())
        symbol = st.text_input("Par de divisas/Activo")
        order_type = st.selectbox("Tipo de orden", ["Market", "Limit", "Stop"])
        entry_price = st.number_input("Precio de Entrada", min_value=0.0, step=0.00001, format="%.5f")
        exit_price = st.number_input("Precio de Salida", min_value=0.0, step=0.00001, format="%.5f")
        stop_loss = st.number_input("Stop Loss", min_value=0.0, step=0.00001, format="%.5f")
        take_profit = st.number_input("Take Profit", min_value=0.0, step=0.00001, format="%.5f")
        position_size = st.number_input("Tamaño de la posición", min_value=0.0, step=0.01)
    
    with col2:
        spread = st.number_input("Spread", min_value=0.0, step=0.00001, format="%.5f")
        slippage = st.number_input("Slippage", min_value=0.0, step=0.00001, format="%.5f")
        commissions = st.number_input("Comisiones", min_value=0.0, step=0.01)
        reason = st.selectbox("Motivo de la operación", ["Técnico", "Fundamental", "Mixto"])
        notes = st.text_area("Notas")
        emotion_before = st.select_slider("Emoción antes de la operación", options=["Muy Negativa", "Negativa", "Neutral", "Positiva", "Muy Positiva"])
        emotion_during = st.select_slider("Emoción durante la operación", options=["Muy Negativa", "Negativa", "Neutral", "Positiva", "Muy Positiva"])
        emotion_after = st.select_slider("Emoción después de la operación", options=["Muy Negativa", "Negativa", "Neutral", "Positiva", "Muy Positiva"])

    if st.button("Agregar Operación"):
        add_operation(date, symbol, order_type, entry_price, exit_price, stop_loss, take_profit,
                      position_size, spread, slippage, commissions, reason, notes,
                      emotion_before, emotion_during, emotion_after)

    # Mostrar operaciones en formato de tabla
    if not st.session_state['operations'].empty:
        st.write("### Registro de Operaciones")
        st.dataframe(st.session_state['operations'].style.highlight_max(axis=0))

with tab2:
    st.header("Estadísticas y Rendimiento")
    
    if not st.session_state['operations'].empty:
        df = st.session_state['operations']
        
        # Gráfico de P&L acumulado
        df['Cumulative P&L'] = df['Result ($)'].cumsum()
        fig_pnl = px.line(df, x='Date', y='Cumulative P&L', title='P&L Acumulado')
        st.plotly_chart(fig_pnl)
        
        # Estadísticas generales
        total_trades = len(df)
        winning_trades = len(df[df['Result ($)'] > 0])
        losing_trades = len(df[df['Result ($)'] < 0])
        win_rate = winning_trades / total_trades * 100 if total_trades > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de operaciones", total_trades)
        col2.metric("Operaciones ganadoras", winning_trades)
        col3.metric("Ratio de aciertos", f"{win_rate:.2f}%")
        
        # Rendimiento por estrategia
        fig_strategy = px.pie(df, names='Reason', values='Result ($)', title='Rendimiento por Estrategia')
        st.plotly_chart(fig_strategy)

with tab3:
    st.header("Análisis Psicológico")
    
    if not st.session_state['operations'].empty:
        df = st.session_state['operations']
        
        # Gráfico de emociones
        emotions_df = df[['Date', 'Emotion Before', 'Emotion During', 'Emotion After']].melt('Date', var_name='Etapa', value_name='Emoción')
        fig_emotions = px.line(emotions_df, x='Date', y='Emoción', color='Etapa', title='Evolución de Emociones')
        st.plotly_chart(fig_emotions)
        
        # Correlación entre emociones y resultados
        emotion_map = {"Muy Negativa": 1, "Negativa": 2, "Neutral": 3, "Positiva": 4, "Muy Positiva": 5}
        df['Emotion Before Numeric'] = df['Emotion Before'].map(emotion_map)
        correlation = df['Emotion Before Numeric'].corr(df['Result ($)'])
        st.write(f"Correlación entre emoción antes de operar y resultado: {correlation:.2f}")

# Botón para descargar los datos
if not st.session_state['operations'].empty:
    csv = st.session_state['operations'].to_csv(index=False)
    st.download_button(
        label="Descargar datos como CSV",
        data=csv,
        file_name="trading_journal.csv",
        mime="text/csv",
    )
