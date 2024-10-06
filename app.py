import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Necesitarás instalar:
# pip install streamlit pandas plotly numpy

# Configuración de la página
st.set_page_config(page_title="Trading Dashboard", layout="wide")

# Función para generar datos de ejemplo
def generate_sample_data():
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
    balance = np.cumsum(np.random.normal(0.1, 1, len(dates))) + 10000
    equity = balance + np.random.normal(0, 100, len(dates))
    
    trades = pd.DataFrame({
        'date': dates,
        'balance': balance,
        'equity': equity,
        'profit_loss': np.random.normal(0, 100, len(dates)),
        'pair': np.random.choice(['EUR/USD', 'GBP/USD', 'USD/JPY'], len(dates)),
        'direction': np.random.choice(['Long', 'Short'], len(dates)),
    })
    return trades

# Generar datos
trades_df = generate_sample_data()

# Título principal
st.title('Trading Dashboard')

# Sección 1: Resumen General
st.header('Resumen General')
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Balance Total", f"${trades_df['balance'].iloc[-1]:,.2f}")
with col2:
    st.metric("Equity", f"${trades_df['equity'].iloc[-1]:,.2f}")
with col3:
    st.metric("P/L Acumulado", f"${trades_df['profit_loss'].sum():,.2f}")
with col4:
    st.metric("Win Rate", f"{(trades_df['profit_loss'] > 0).mean() * 100:.1f}%")

# Gráfico de Balance y Equity
fig_balance = go.Figure()
fig_balance.add_trace(go.Scatter(x=trades_df['date'], y=trades_df['balance'],
                                name='Balance'))
fig_balance.add_trace(go.Scatter(x=trades_df['date'], y=trades_df['equity'],
                                name='Equity'))
fig_balance.update_layout(title='Evolución de Balance y Equity')
st.plotly_chart(fig_balance, use_container_width=True)

# Sección 2: Estadísticas de Trading
st.header('Estadísticas de Trading')

col1, col2 = st.columns(2)

with col1:
    # Distribución de Ganancias/Pérdidas
    fig_dist = px.histogram(trades_df, x='profit_loss', 
                           title='Distribución de Ganancias/Pérdidas')
    st.plotly_chart(fig_dist, use_container_width=True)

with col2:
    # Rendimiento por Par
    fig_pair = px.box(trades_df, x='pair', y='profit_loss',
                      title='Rendimiento por Par de Divisas')
    st.plotly_chart(fig_pair, use_container_width=True)

# Sección 3: Métricas Adicionales
st.header('Métricas Adicionales')
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Mejor Trade", f"${trades_df['profit_loss'].max():,.2f}")
with col2:
    st.metric("Peor Trade", f"${trades_df['profit_loss'].min():,.2f}")
with col3:
    st.metric("Número Total de Trades", len(trades_df))

# Sección 4: Registro de Operaciones
st.header('Registro de Operaciones')
st.dataframe(trades_df.tail(10)[['date', 'pair', 'direction', 'profit_loss']])

# Sección 5: Filtros
st.sidebar.header('Filtros')
date_range = st.sidebar.date_input(
    "Rango de fechas",
    [trades_df['date'].min(), trades_df['date'].max()]
)
selected_pairs = st.sidebar.multiselect(
    'Pares de divisas',
    options=trades_df['pair'].unique(),
    default=trades_df['pair'].unique()
)

if __name__ == '__main__':
    st.sidebar.info('Este es un dashboard de ejemplo. Los datos son generados aleatoriamente.')
