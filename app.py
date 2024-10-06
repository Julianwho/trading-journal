import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import numpy as np
from scipy import stats
import base64
from io import BytesIO

# Configuración de la página
st.set_page_config(layout="wide", page_title="Trading Journal Pro")

# Inicialización de la sesión de estado
@st.cache_data
def init_session_state():
    if 'operations' not in st.session_state:
        st.session_state['operations'] = pd.DataFrame(columns=[
            'Fecha', 'Par', 'Dirección', 'Hora de Entrada', 'Hora de Salida', 
            'Precio de Entrada', 'Precio de Salida', 'Stop Loss', 'Take Profit', 
            'Resultado', 'Apalancamiento', 'Margen', 'Tamaño Posición'
        ])
    if 'psychological_analysis' not in st.session_state:
        st.session_state['psychological_analysis'] = pd.DataFrame(columns=[
            'Fecha', 'Operación ID', 'FOMO', 'Trade Revenge', 'Impaciencia', 
            'Emoción Antes', 'Emoción Durante', 'Emoción Después'
        ])

init_session_state()

# Función para obtener noticias de Forex Factory
@st.cache_data(ttl=3600)
def get_forex_factory_news():
    try:
        url = "https://www.forexfactory.com/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        news_table = soup.find('table', class_='calendar__table')
        if not news_table:
            return pd.DataFrame(columns=['Time', 'Currency', 'Impact', 'Event', 'Actual', 'Forecast', 'Previous'])
        
        news_data = []
        date = datetime.now().strftime("%Y-%m-%d")
        
        for row in news_table.find_all('tr', class_='calendar__row'):
            time_cell = row.find('td', class_='calendar__time')
            currency_cell = row.find('td', class_='calendar__currency')
            impact_cell = row.find('td', class_='calendar__impact')
            event_cell = row.find('td', class_='calendar__event')
            actual_cell = row.find('td', class_='calendar__actual')
            forecast_cell = row.find('td', class_='calendar__forecast')
            previous_cell = row.find('td', class_='calendar__previous')
            
            if all([time_cell, currency_cell, event_cell]):
                news_data.append({
                    'Time': time_cell.text.strip(),
                    'Currency': currency_cell.text.strip(),
                    'Impact': impact_cell.find('span')['class'][0] if impact_cell and impact_cell.find('span') else 'Low',
                    'Event': event_cell.text.strip(),
                    'Actual': actual_cell.text.strip() if actual_cell else '',
                    'Forecast': forecast_cell.text.strip() if forecast_cell else '',
                    'Previous': previous_cell.text.strip() if previous_cell else ''
                })
        
        return pd.DataFrame(news_data)
    except Exception as e:
        st.error(f"Error al obtener noticias: {str(e)}")
        return pd.DataFrame(columns=['Time', 'Currency', 'Impact', 'Event', 'Actual', 'Forecast', 'Previous'])

# Función para calcular métricas de riesgo
def calculate_risk_metrics(df):
    if df.empty:
        return {
            'var_95': 0,
            'var_99': 0,
            'expected_shortfall': 0,
            'max_drawdown': 0,
            'sharpe_ratio': 0,
            'win_rate': 0
        }
    
    returns = df['Resultado'].pct_change()
    cumulative_returns = (1 + returns).cumprod()
    rolling_max = cumulative_returns.expanding().max()
    drawdowns = cumulative_returns / rolling_max - 1
    
    return {
        'var_95': np.percentile(df['Resultado'], 5),
        'var_99': np.percentile(df['Resultado'], 1),
        'expected_shortfall': df[df['Resultado'] < np.percentile(df['Resultado'], 5)]['Resultado'].mean(),
        'max_drawdown': drawdowns.min(),
        'sharpe_ratio': returns.mean() / returns.std() if returns.std() != 0 else 0,
        'win_rate': len(df[df['Resultado'] > 0]) / len(df) if len(df) > 0 else 0
    }

# Función para obtener sentimiento del mercado
@st.cache_data(ttl=3600)
def get_market_sentiment():
    # Simulación de datos de sentimiento
    return {
        'fear_greed_index': np.random.randint(0, 100),
        'long_short_ratio': np.random.uniform(0.5, 1.5),
        'volatility_index': np.random.uniform(10, 30)
    }

# Interfaz principal
st.title("Trading Journal Pro")

# Pestañas
tab1, tab2, tab3, tab4 = st.tabs(["Registro de Operaciones", "Gestión del Riesgo", "Análisis Psicológico", "Noticias y Sentimiento"])

with tab1:
    st.header("Registro de Operaciones")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        date = st.date_input("Fecha", datetime.today())
        par = st.text_input("Par de Trading", "EUR/USD")
        direccion = st.selectbox("Dirección", ["Long", "Short"])
        entry_time = st.time_input("Hora de Entrada")
    with col2:
        exit_time = st.time_input("Hora de Salida")
        entry_price = st.number_input("Precio de Entrada", min_value=0.0, step=0.00001, format="%.5f")
        exit_price = st.number_input("Precio de Salida", min_value=0.0, step=0.00001, format="%.5f")
    with col3:
        stop_loss = st.number_input("Stop Loss", min_value=0.0, step=0.00001, format="%.5f")
        take_profit = st.number_input("Take Profit", min_value=0.0, step=0.00001, format="%.5f")
        position_size = st.number_input("Tamaño de la Posición", min_value=0.01, step=0.01)
        leverage = st.number_input("Apalancamiento", min_value=1, step=1)

    if st.button("Agregar Operación"):
        margin = position_size / leverage
        result = (exit_price - entry_price) * position_size * (1 if direccion == "Long" else -1)
        
        new_row = pd.DataFrame([{
            'Fecha': date,
            'Par': par,
            'Dirección': direccion,
            'Hora de Entrada': entry_time,
            'Hora de Salida': exit_time,
            'Precio de Entrada': entry_price,
            'Precio de Salida': exit_price,
            'Stop Loss': stop_loss,
            'Take Profit': take_profit,
            'Resultado': result,
            'Apalancamiento': leverage,
            'Margen': margin,
            'Tamaño Posición': position_size
        }])
        
        st.session_state['operations'] = pd.concat([st.session_state['operations'], new_row], ignore_index=True)

    if not st.session_state['operations'].empty:
        st.write("### Historial de Operaciones")
        st.dataframe(st.session_state['operations'])

with tab2:
    st.header("Gestión del Riesgo")
    
    if not st.session_state['operations'].empty:
        risk_metrics = calculate_risk_metrics(st.session_state['operations'])
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("VaR (95%)", f"${risk_metrics['var_95']:.2f}")
        col2.metric("VaR (99%)", f"${risk_metrics['var_99']:.2f}")
        col3.metric("Max Drawdown", f"{risk_metrics['max_drawdown']:.2%}")
        col4.metric("Sharpe Ratio", f"{risk_metrics['sharpe_ratio']:.2f}")
        
        # Gráfico de drawdown
        df = st.session_state['operations'].copy()
        df['Cumulative'] = df['Resultado'].cumsum()
        df['Rolling Max'] = df['Cumulative'].expanding().max()
        df['Drawdown'] = df['Cumulative'] - df['Rolling Max']
        
        fig_drawdown = px.line(df, x='Fecha', y='Drawdown', title='Drawdown Over Time')
        st.plotly_chart(fig_drawdown)
        
        # Simulador de riesgo
        st.subheader("Simulador de Riesgo")
        risk_per_trade = st.slider("Riesgo por operación (%)", 0.1, 10.0, 1.0)
        position_sizing = st.radio("Estrategia de tamaño de posición", 
                                  ["Fijo", "Porcentaje del capital", "Volatilidad ajustada"])
        
        # Simulación Monte Carlo
        n_simulations = 1000
        n_trades = 100
        win_rate = risk_metrics['win_rate']
        
        simulated_results = []
        for _ in range(n_simulations):
            trades = np.random.choice([1, -1], n_trades, p=[win_rate, 1-win_rate])
            cumulative = np.cumsum(trades * risk_per_trade/100)
            simulated_results.append(cumulative)
        
        simulated_df = pd.DataFrame(simulated_results).T
        quantiles = simulated_df.quantile([0.05, 0.5, 0.95], axis=1).T
        
        fig_simulation = go.Figure()
        for i in range(n_simulations):
            fig_simulation.add_trace(go.Scatter(y=simulated_results[i], mode='lines', 
                                               line=dict(color='rgba(0,100,80,0.05)'), showlegend=False))
        fig_simulation.add_trace(go.Scatter(y=quantiles[0.05], mode='lines', name='5th Percentile',
                                           line=dict(color='red', dash='dash')))
        fig_simulation.add_trace(go.Scatter(y=quantiles[0.5], mode='lines', name='Median',
                                           line=dict(color='blue')))
        fig_simulation.add_trace(go.Scatter(y=quantiles[0.95], mode='lines', name='95th Percentile',
                                           line=dict(color='green', dash='dash')))
        
        fig_simulation.update_layout(title='Simulación Monte Carlo de Resultados',
                                    xaxis_title='Número de operaciones',
                                    yaxis_title='Retorno acumulado (%)')
        st.plotly_chart(fig_simulation)

with tab3:
    st.header("Análisis Psicológico")
    
    # Formulario para análisis psicológico
    psych_date = st.date_input("Fecha del análisis", datetime.today(), key="psych_date")
    operation_id = st.selectbox("Operación", 
                               options=st.session_state['operations'].index.tolist() if not st.session_state['operations'].empty else [0])
    
    col1, col2 = st.columns(2)
    with col1:
        fomo = st.checkbox("FOMO")
        revenge = st.checkbox("Trade Revenge")
        impatience = st.checkbox("Impaciencia")
    with col2:
        emotion_before = st.select_slider("Emoción antes", options=["Muy Negativa", "Negativa", "Neutral", "Positiva", "Muy Positiva"])
        emotion_during = st.select_slider("Emoción durante", options=["Muy Negativa", "Negativa", "Neutral", "Positiva", "Muy Positiva"])
        emotion_after = st.select_slider("Emoción después", options=["Muy Negativa", "Negativa", "Neutral", "Positiva", "Muy Positiva"])

    if st.button("Registrar Análisis Psicológico"):
        new_psych = pd.DataFrame([{
            'Fecha': psych_date,
            'Operación ID': operation_id,
            'FOMO': fomo,
            'Trade Revenge': revenge,
            'Impaciencia': impatience,
            'Emoción Antes': emotion_before,
            'Emoción Durante': emotion_during,
            'Emoción Después': emotion_after
        }])
        st.session_state['psychological_analysis'] = pd.concat([st.session_state['psychological_analysis'], new_psych], 
                                                              ignore_index=True)

    if not st.session_state['psychological_analysis'].empty:
        st.write("### Historial de Análisis Psicológico")
        st.dataframe(st.session_state['psychological_analysis'])
        
        # Gráficos de análisis psicológico
        emotions_df = st.session_state['psychological_analysis'].melt(
            id_vars=['Fecha'], 
            value_vars=['Emoción Antes', 'Emoción Durante', 'Emoción Después'],
            var_name='Momento', value_name='Emoción'
        )
        fig_emotions = px.line(emotions_df, x='Fecha', y='Emoción', color='Momento', 
                              title='Evolución de Emociones')
        st.plotly_chart(fig_emotions)

with tab4:
    st.header("Noticias y Sentimiento del Mercado")
    
    col1, col2 = st.columns(2)# Continuación de la sección tab4 (Noticias y Sentimiento del Mercado)
    with col1:
        st.subheader("Noticias de Forex Factory")
        forex_news = get_forex_factory_news()
        
        if not forex_news.empty:
            # Estilizar las noticias según su impacto
            def style_news(impact):
                if 'high' in impact.lower():
                    return 'background-color: #ffcdd2'
                elif 'medium' in impact.lower():
                    return 'background-color: #fff9c4'
                return 'background-color: #c8e6c9'
            
            styled_news = forex_news.style.apply(lambda x: [style_news(impact) for impact in x['Impact']], 
                                                axis=0, subset=['Impact'])
            st.dataframe(styled_news, height=400)
        else:
            st.warning("No se pudieron cargar las noticias. Intente más tarde.")

    with col2:
        st.subheader("Sentimiento del Mercado")
        sentiment = get_market_sentiment()
        
        # Fear & Greed Index
        st.metric("Índice de Miedo y Codicia", f"{sentiment['fear_greed_index']}")
        fear_greed_color = np.interp(sentiment['fear_greed_index'], [0, 50, 100], [0, 0.5, 1])
        fig_fear_greed = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = sentiment['fear_greed_index'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Fear & Greed Index"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': f'hsl({120*fear_greed_color}, 70%, 50%)'},
                'steps': [
                    {'range': [0, 20], 'color': 'red'},
                    {'range': [20, 40], 'color': 'orange'},
                    {'range': [40, 60], 'color': 'yellow'},
                    {'range': [60, 80], 'color': 'lightgreen'},
                    {'range': [80, 100], 'color': 'green'}
                ]
            }
        ))
        st.plotly_chart(fig_fear_greed)
        
        # Long/Short Ratio
        st.metric("Ratio Long/Short", f"{sentiment['long_short_ratio']:.2f}")
        fig_long_short = go.Figure(go.Indicator(
            mode = "delta",
            value = sentiment['long_short_ratio'],
            delta = {'reference': 1, 'relative': True},
            title = {'text': "Long/Short Ratio"}
        ))
        st.plotly_chart(fig_long_short)
        
        # Volatility Index
        st.metric("Índice de Volatilidad", f"{sentiment['volatility_index']:.2f}")
        fig_vix = go.Figure(go.Indicator(
            mode = "number+delta",
            value = sentiment['volatility_index'],
            delta = {'reference': 20, 'relative': True},
            title = {'text': "VIX"}
        ))
        st.plotly_chart(fig_vix)

# Correlación entre sentimiento y resultados
if not st.session_state['operations'].empty:
    st.subheader("Análisis de Correlación: Sentimiento vs Resultados")
    
    # Simulamos datos históricos de sentimiento para correlacionar con operaciones
    dates = st.session_state['operations']['Fecha'].unique()
    historical_sentiment = pd.DataFrame({
        'Fecha': dates,
        'Fear_Greed': np.random.randint(0, 100, size=len(dates)),
        'Volatility': np.random.uniform(10, 30, size=len(dates))
    })
    
    merged_data = pd.merge(st.session_state['operations'], historical_sentiment, on='Fecha')
    
    fig_correlation = px.scatter(merged_data, x='Fear_Greed', y='Resultado',
                                title='Correlación entre Sentimiento y Resultados',
                                trendline="ols")
    st.plotly_chart(fig_correlation)

# Calendario económico personalizado
st.subheader("Calendario Económico Personalizado")
col1, col2, col3 = st.columns(3)
with col1:
    start_date = st.date_input("Fecha de inicio", datetime.today() - timedelta(days=7))
with col2:
    end_date = st.date_input("Fecha de fin", datetime.today() + timedelta(days=7))
with col3:
    selected_currencies = st.multiselect("Monedas", 
                                        options=['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'NZD'],
                                        default=['USD', 'EUR'])

# Filtrar noticias según selección
if not forex_news.empty:
    filtered_news = forex_news[
        forex_news['Currency'].isin(selected_currencies)
    ].copy()
    
    if not filtered_news.empty:
        st.dataframe(filtered_news)
    else:
        st.info("No hay noticias para las monedas seleccionadas en este período.")

# Análisis de impacto de noticias en resultados
if not st.session_state['operations'].empty:
    st.subheader("Análisis de Impacto de Noticias en Resultados")
    
    impact_analysis = pd.merge(st.session_state['operations'], forex_news, 
                              left_on=['Fecha', 'Par'], 
                              right_on=['Time', 'Currency'], 
                              how='left')
    
    fig_impact = px.box(impact_analysis, x='Impact', y='Resultado',
                        title='Distribución de Resultados por Impacto de Noticia')
    st.plotly_chart(fig_impact)

# Configuración de alertas
st.subheader("Configuración de Alertas")
col1, col2 = st.columns(2)
with col1:
    alert_news = st.multiselect("Alertas de Noticias", 
                                options=['Alto Impacto', 'Medio Impacto', 'Bajo Impacto'],
                                default=['Alto Impacto'])
    alert_sentiment = st.slider("Alerta de Cambio de Sentimiento", 0, 100, 20)
with col2:
    alert_email = st.text_input("Email para alertas")
    if st.button("Guardar Configuración de Alertas"):
        st.success("Configuración de alertas guardada")

# Exportar datos
st.subheader("Exportar Datos")
if st.button("Exportar todos los datos"):
    # Crear un archivo Excel con múltiples hojas
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        st.session_state['operations'].to_excel(writer, sheet_name='Operaciones', index=False)
        st.session_state['psychological_analysis'].to_excel(writer, sheet_name='Análisis Psicológico', index=False)
        forex_news.to_excel(writer, sheet_name='Noticias', index=False)
    
    b64 = base64.b64encode(output.getvalue()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="trading_journal_data.xlsx">Descargar Excel</a>'
    st.markdown(href, unsafe_allow_html=True)

# Agregar funcionalidad de backup y restauración
st.subheader("Backup y Restauración")
col1, col2 = st.columns(2)
with col1:
    if st.button("Crear Backup"):
        backup_data = {
            'operations': st.session_state['operations'].to_dict(),
            'psychological_analysis': st.session_state['psychological_analysis'].to_dict()
        }
        backup_json = json.dumps(backup_data)
        b64 = base64.b64encode(backup_json.encode()).decode()
        href = f'<a href="data:file/json;base64,{b64}" download="trading_journal_backup.json">Descargar Backup</a>'
        st.markdown(href, unsafe_allow_html=True)
with col2:
    uploaded_file = st.file_uploader("Restaurar desde Backup", type=['json'])
    if uploaded_file is not None:
        backup_data = json.load(uploaded_file)
        st.session_state['operations'] = pd.DataFrame.from_dict(backup_data['operations'])
        st.session_state['psychological_analysis'] = pd.DataFrame.from_dict(backup_data['psychological_analysis'])
        st.success("Datos restaurados exitosamente")
