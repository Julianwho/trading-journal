import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from PIL import Image
import io
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Función para obtener noticias de Forex Factory
def get_forex_factory_news():
    url = "https://www.forexfactory.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_table = soup.find('table', class_='calendar__table')
    news_data = []

    if news_table:
        rows = news_table.find_all('tr', class_='calendar__row')
        for row in rows:
            time = row.find('td', class_='calendar__time')
            currency = row.find('td', class_='calendar__currency')
            event = row.find('td', class_='calendar__event')
            impact = row.find('td', class_='calendar__impact')
            
            if time and currency and event:
                news_data.append({
                    'Time': time.text.strip(),
                    'Currency': currency.text.strip(),
                    'Event': event.text.strip(),
                    'Impact': impact.find('span')['class'][0] if impact else 'N/A'
                })
    
    return pd.DataFrame(news_data)

# Inicialización de la sesión de estado
if 'operations' not in st.session_state:
    st.session_state['operations'] = pd.DataFrame(columns=[
        'Fecha', 'Hora de Entrada', 'Hora de Salida', 'Precio de Entrada', 'Precio de Salida', 
        'Stop Loss', 'Take Profit', 'Resultado', 'Apalancamiento', 'Margen', 'Imagen'
    ])

if 'psychological_analysis' not in st.session_state:
    st.session_state['psychological_analysis'] = pd.DataFrame(columns=[
        'Fecha', 'Operación ID', 'FOMO', 'Trade Revenge', 'Impaciencia', 
        'Emoción Antes', 'Emoción Durante', 'Emoción Después'
    ])

if 'news_impact' not in st.session_state:
    st.session_state['news_impact'] = pd.DataFrame(columns=[
        'Fecha', 'Noticia', 'Impacto', 'Descripción'
    ])

# Función para agregar una operación
def add_operation(date, entry_time, exit_time, entry_price, exit_price, stop_loss, take_profit, result, leverage, margin, image):
    new_row = {
        'Fecha': date,
        'Hora de Entrada': entry_time,
        'Hora de Salida': exit_time,
        'Precio de Entrada': entry_price,
        'Precio de Salida': exit_price,
        'Stop Loss': stop_loss,
        'Take Profit': take_profit,
        'Resultado': result,
        'Apalancamiento': leverage,
        'Margen': margin,
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

# Función para agregar impacto de noticias
def add_news_impact(date, news, impact, description):
    new_row = {
        'Fecha': date,
        'Noticia': news,
        'Impacto': impact,
        'Descripción': description
    }
    st.session_state['news_impact'] = pd.concat([st.session_state['news_impact'], pd.DataFrame([new_row])], ignore_index=True)

# Interfaz principal
st.title("Trading Journal Dashboard")

# Pestañas
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Registro de Operaciones", "Estadísticas y Rendimiento", "Gestión del Riesgo", "Análisis Psicológico", "Noticias y Sentimiento"])

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
        result = st.number_input("Resultado de la operación", step=0.01, format="%.2f")
        leverage = st.number_input("Apalancamiento utilizado", min_value=1.0, step=0.1)
        margin = st.number_input("Margen utilizado", min_value=0.0, step=0.01)
        image = st.file_uploader("Subir imagen del trade", type=['png', 'jpg', 'jpeg'])
    
    if st.button("Agregar Operación"):
        if image is not None:
            image_bytes = image.getvalue()
        else:
            image_bytes = None
        add_operation(date, entry_time, exit_time, entry_price, exit_price, stop_loss, take_profit, result, leverage, margin, image_bytes)

    # Mostrar operaciones en formato de tabla
    if not st.session_state['operations'].empty:
        st.write("### Registro de Operaciones")
        df = st.session_state['operations'].copy()
        df['Imagen'] = df['Imagen'].apply(lambda x: 'Sí' if x is not None else 'No')
        
        def color_result(val):
            if val < 0:
                return 'background-color: rgba(255, 0, 0, 0.1)'
            elif val > 0:
                return 'background-color: rgba(0, 255, 0, 0.1)'
            else:
                return ''
        
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
    st.header("Gestión del Riesgo")
    
    if not st.session_state['operations'].empty:
        df = st.session_state['operations']
        
        # Cálculo del VaR (simplificado)
        returns = df['Resultado'].pct_change()
        var_95 = returns.quantile(0.05)
        st.metric("Value at Risk (95%)", f"{var_95:.2%}")
        
        # Cálculo del Drawdown
        df['Cumulative'] = df['Resultado'].cumsum()
        df['Drawdown'] = df['Cumulative'] - df['Cumulative'].cummax()
        max_drawdown = df['Drawdown'].min()
        st.metric("Máximo Drawdown", f"{max_drawdown:.2f}")
        
        # Gráfico de apalancamiento
        fig_leverage = px.line(df, x='Fecha', y='Apalancamiento', title='Apalancamiento Utilizado')
        st.plotly_chart(fig_leverage)
        
        # Gráfico de margen
        fig_margin = px.line(df, x='Fecha', y='Margen', title='Margen Utilizado')
        st.plotly_chart(fig_margin)
        
        # Calendario de rendimiento
        fig, ax = plt.subplots(figsize=(12, 6))
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        df.set_index('Fecha', inplace=True)
        cmap = plt.cm.RdYlGn
        df['Resultado'].plot(kind='bar', ax=ax, color=cmap(df['Resultado']/df['Resultado'].abs().max()))
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MONDAY))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.title('Rendimiento Diario')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

with tab4:
    st.header("Análisis Psicológico")
    
    # Formulario para añadir análisis psicológico
    st.subheader("Registrar Análisis Psicológico")
    date = st.date_input("Fecha del análisis", datetime.today(), key="psych_date")
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

with tab5:
    st.header("Noticias y Sentimiento del Mercado")
    
    # Obtener noticias de Forex Factory
    forex_news = get_forex_factory_news()
    st.subheader("Noticias de Forex Factory")
    st.dataframe(forex_news)
    
    # Formulario para registrar impacto de noticias
    st.subheader("Registrar Impacto de Noticias")
    news_date = st.date_input("Fecha de la noticia", datetime.today(), key="news_date")
    news_event = st.text_input("Evento o Noticia")
    news_impact = st.selectbox("Impacto en tus operaciones", ["Positivo", "Negativo", "Neutral"])
    news_description = st.text_area("Descripción del impacto")

    if st.button("Registrar Impacto de Noticia"):
        add_news_impact(news_date, news_event, news_impact, news_description)

    # Mostrar registro de impacto de noticias
    if not st.session_state['news_impact'].empty:
        st.write("### Registro de Impacto de Noticias")
        st.dataframe(st.session_state['news_impact'])

        # Gráfico de impacto de noticias
        fig_news_impact = px.bar(st.session_state['news_impact'], x='Fecha', y='Impacto', color='Impacto',
                                 title='Impacto de Noticias en las Operaciones')
        st.plotly_chart(fig_news_impact)

    # Indicador de sentimiento del mercado (simplificado)
    st.subheader("Indicador de Sentimiento del Mercado")
    sentiment = st.slider("Índice de Miedo/Codicia", 0, 100, 50)
    st.progress(sentiment)
    if sentiment < 20:
        st.write("Miedo Extremo")
    elif sentiment < 40:
        st.write("Miedo")
    elif sentiment < 60:
        st.write("Neutral")
    elif sentiment < 80:
        st.write("Codicia")
    else:
        st.write("Codicia Extrema")

# Botones para descargar los datos
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

if not st.session_state['news_impact'].empty:
    news_csv = st.session_state['news_impact'].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Descargar Registro de Impacto de Noticias como CSV",
        data=news_csv,
        file_name="news_impact.csv",
        mime="text/csv",
    )
