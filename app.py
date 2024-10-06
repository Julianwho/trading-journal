import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from PIL import Image
import io

# Inicialización de la sesión de estado
if 'operations' not in st.session_state:
    st.session_state['operations'] = pd.DataFrame(columns=[
        'Fecha', 'Hora de Entrada', 'Hora de Salida', 'Precio de Entrada', 'Precio de Salida', 
        'Stop Loss', 'Take Profit', 'Resultado', 'Imagen'
    ])

if 'psychological_analysis' not in st.session_state:
    st.session_state['psychological_analysis'] = pd.DataFrame(columns=[
        'Fecha', 'Operación ID', 'FOMO', 'Trade Revenge', 'Impaciencia', 
        'Emoción Antes', 'Emoción Durante', 'Emoción Después'
    ])

# Función para agregar una operación
def add_operation(date, entry_time, exit_time, entry_price, exit_price, stop_loss, take_profit, image):
    result = exit_price - entry_price
    new_row = {
        'Fecha': date,
        'Hora de Entrada': entry_time,
        'Hora de Salida': exit_time,
        'Precio de Entrada': entry_price,
        'Precio de Salida': exit_price,
        'Stop Loss': stop_loss,
        'Take Profit': take_profit,
        'Resultado': result,
        'Imagen': image
    }
    st.session_state['operations'] = pd.concat([st.session_state['operations'], pd.DataFrame([new_row])], ignore_index=True)

# Función para agregar análisis psicológico
def add_psychological_analysis(date, operation_id, fomo, revenge, impatience, emotion_before, emotion_during, emotion_after):
    new_row = {
        'Fecha': date,
        'Operación ID': operation_id,
        'FOMO': fomo,
        'Trade Revenge': revenge,
        'Impaciencia': impatience,
        'Emoción Antes': emotion_before,
        'Emoción Durante': emotion_during,
        'Emoción Después': emotion_after
    }
    st.session_state['psychological_analysis'] = pd.concat([st.session_state['psychological_analysis'], pd.DataFrame([new_row])], ignore_index=True)

# Interfaz principal
st.title("Trading Journal Dashboard")

# Pestañas
tab1, tab2, tab3 = st.tabs(["Registro de Operaciones", "Estadísticas y Rendimiento", "Análisis Psicológico"])

with tab1:
    st.header("Registro de Operaciones")
    
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Fecha", datetime.today())
        entry_time = st.time_input("Hora de Entrada")
        exit_time = st.time_input("Hora de Salida")
        entry_price = st.number_input("Precio de Entrada", min_value=0.0, step=0.00001, format="%.5f")
        exit_price = st.number_input("Precio de Salida", min_value=0.0, step=0.00001, format="%.5f")
    
    with col2:
        stop_loss = st.number_input("Donde estaba tu Stop Loss", min_value=0.0, step=0.00001, format="%.5f")
        take_profit = st.number_input("Donde estaba tu Take Profit", min_value=0.0, step=0.00001, format="%.5f")
        image = st.file_uploader("Subir imagen del trade", type=['png', 'jpg', 'jpeg'])
    
    if st.button("Agregar Operación"):
        if image is not None:
            image_bytes = image.getvalue()
        else:
            image_bytes = None
        add_operation(date, entry_time, exit_time, entry_price, exit_price, stop_loss, take_profit, image_bytes)

    # Mostrar operaciones en formato de tabla
    if not st.session_state['operations'].empty:
        st.write("### Registro de Operaciones")
        df = st.session_state['operations'].copy()
        df['Imagen'] = df['Imagen'].apply(lambda x: 'Sí' if x is not None else 'No')
        
        def color_result(val):
            color = 'red' if val < 0 else 'green' if val > 0 else 'white'
            return f'background-color: {color}'
        
        styled_df = df.style.applymap(color_result, subset=['Resultado'])
        st.dataframe(styled_df)

        # Mostrar imágenes
        if st.button("Mostrar/Ocultar Imágenes"):
            for idx, row in df.iterrows():
                if row['Imagen'] == 'Sí':
                    st.image(row['Imagen'], caption=f"Operación {idx}", use_column_width=True)

with tab2:
    st.header("Estadísticas y Rendimiento")
    
    if not st.session_state['operations'].empty:
        df = st.session_state['operations']
        
        # Gráfico de resultados acumulados
        df['Resultado Acumulado'] = df['Resultado'].cumsum()
        fig_results = px.line(df, x='Fecha', y='Resultado Acumulado', title='Resultados Acumulados')
        st.plotly_chart(fig_results)
        
        # Estadísticas generales
        total_trades = len(df)
        winning_trades = len(df[df['Resultado'] > 0])
        losing_trades = len(df[df['Resultado'] < 0])
        win_rate = winning_trades / total_trades * 100 if total_trades > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de operaciones", total_trades)
        col2.metric("Operaciones ganadoras", winning_trades)
        col3.metric("Ratio de aciertos", f"{win_rate:.2f}%")
        
        # Distribución de resultados
        fig_dist = px.histogram(df, x='Resultado', title='Distribución de Resultados')
        st.plotly_chart(fig_dist)

with tab3:
    st.header("Análisis Psicológico")
    
    # Formulario para añadir análisis psicológico
    st.subheader("Registrar Análisis Psicológico")
    date = st.date_input("Fecha del análisis", datetime.today())
    operation_id = st.number_input("ID de la Operación", min_value=0, step=1)
    fomo = st.checkbox("¿Tuviste FOMO?")
    revenge = st.checkbox("¿Tuviste Trade Revenge?")
    impatience = st.checkbox("¿Tuviste Impaciencia?")
    emotion_before = st.select_slider("Emoción antes de la operación", options=["Muy Negativa", "Negativa", "Neutral", "Positiva", "Muy Positiva"])
    emotion_during = st.select_slider("Emoción durante la operación", options=["Muy Negativa", "Negativa", "Neutral", "Positiva", "Muy Positiva"])
    emotion_after = st.select_slider("Emoción después de la operación", options=["Muy Negativa", "Negativa", "Neutral", "Positiva", "Muy Positiva"])

    if st.button("Registrar Análisis Psicológico"):
        add_psychological_analysis(date, operation_id, fomo, revenge, impatience, emotion_before, emotion_during, emotion_after)

    # Mostrar análisis psicológico
    if not st.session_state['psychological_analysis'].empty:
        st.write("### Registro de Análisis Psicológico")
        st.dataframe(st.session_state['psychological_analysis'])

        # Gráfico de emociones a lo largo del tiempo
        emotions_df = st.session_state['psychological_analysis'][['Fecha', 'Emoción Antes', 'Emoción Durante', 'Emoción Después']]
        emotions_df = emotions_df.melt('Fecha', var_name='Etapa', value_name='Emoción')
        fig_emotions = px.line(emotions_df, x='Fecha', y='Emoción', color='Etapa', title='Evolución de Emociones')
        st.plotly_chart(fig_emotions)

        # Gráfico de factores psicológicos
        factors_df = st.session_state['psychological_analysis'][['Fecha', 'FOMO', 'Trade Revenge', 'Impaciencia']]
        factors_df = factors_df.melt('Fecha', var_name='Factor', value_name='Presencia')
        fig_factors = px.bar(factors_df, x='Fecha', y='Presencia', color='Factor', title='Factores Psicológicos por Operación')
        st.plotly_chart(fig_factors)

# Botón para descargar los datos
if not st.session_state['operations'].empty:
    operations_csv = st.session_state['operations'].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Descargar Registro de Operaciones como CSV",
        data=operations_csv,
        file_name="trading_operations.csv",
        mime="text/csv",
    )

if not st.session_state['psychological_analysis'].empty:
    psych_csv = st.session_state['psychological_analysis'].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Descargar Análisis Psicológico como CSV",
        data=psych_csv,
        file_name="psychological_analysis.csv",
        mime="text/csv",
    )
