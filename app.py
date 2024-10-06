import dash
from dash import dcc, html, dash_table
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Necesitarás instalar:
# pip install dash pandas plotly numpy

# Generar datos de ejemplo
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

app = dash.Dash(__name__)

# Estilo
colors = {
    'background': '#1e222d',
    'text': '#7fafdf',
    'grid': '#2c3040'
}

# Diseño del dashboard
app.layout = html.Div([
    html.Div([
        html.H1('Trading Dashboard', style={'color': colors['text']}),
        
        # Sección 1: Resumen General
        html.Div([
            html.H2('Resumen General', style={'color': colors['text']}),
            html.Div([
                html.Div([
                    html.H3('Balance Total', style={'color': colors['text']}),
                    html.H4(id='balance-total', style={'color': '#4CAF50'})
                ], className='metric-box'),
                html.Div([
                    html.H3('Equity', style={'color': colors['text']}),
                    html.H4(id='equity-total', style={'color': '#2196F3'})
                ], className='metric-box'),
                html.Div([
                    html.H3('P/L Acumulado', style={'color': colors['text']}),
                    html.H4(id='pl-total', style={'color': '#FFC107'})
                ], className='metric-box'),
            ], style={'display': 'flex', 'justify-content': 'space-between'}),
            
            dcc.Graph(id='balance-equity-chart')
        ]),
        
        # Sección 2: Estadísticas de Trading
        html.Div([
            html.H2('Estadísticas de Trading', style={'color': colors['text']}),
            html.Div([
                html.Div([
                    html.H3('Win Rate', style={'color': colors['text']}),
                    html.H4(id='win-rate', style={'color': '#4CAF50'})
                ], className='metric-box'),
                html.Div([
                    html.H3('Mejor Trade', style={'color': colors['text']}),
                    html.H4(id='best-trade', style={'color': '#2196F3'})
                ], className='metric-box'),
                html.Div([
                    html.H3('Peor Trade', style={'color': colors['text']}),
                    html.H4(id='worst-trade', style={'color': '#F44336'})
                ], className='metric-box'),
            ], style={'display': 'flex', 'justify-content': 'space-between'}),
            
            dcc.Graph(id='win-loss-distribution')
        ]),
        
        # Sección 3: Análisis por Par de Divisas
        html.Div([
            html.H2('Análisis por Par', style={'color': colors['text']}),
            dcc.Graph(id='pair-performance')
        ]),
        
        # Sección 4: Tabla de Trades
        html.Div([
            html.H2('Registro de Operaciones', style={'color': colors['text']}),
            dash_table.DataTable(
                id='trades-table',
                style_header={
                    'backgroundColor': colors['grid'],
                    'color': colors['text']
                },
                style_cell={
                    'backgroundColor': colors['background'],
                    'color': colors['text']
                }
            )
        ])
    ], style={'backgroundColor': colors['background'], 'padding': '20px'})
])

# Callbacks
@app.callback(
    [Output('balance-total', 'children'),
     Output('equity-total', 'children'),
     Output('pl-total', 'children'),
     Output('win-rate', 'children'),
     Output('best-trade', 'children'),
     Output('worst-trade', 'children'),
     Output('balance-equity-chart', 'figure'),
     Output('win-loss-distribution', 'figure'),
     Output('pair-performance', 'figure'),
     Output('trades-table', 'data')],
    [Input('dummy-input', 'children')]
)
def update_dashboard(_):
    trades_df = generate_sample_data()
    
    # Cálculos para métricas
    balance_total = f"${trades_df['balance'].iloc[-1]:,.2f}"
    equity_total = f"${trades_df['equity'].iloc[-1]:,.2f}"
    pl_total = f"${trades_df['profit_loss'].sum():,.2f}"
    win_rate = f"{(trades_df['profit_loss'] > 0).mean() * 100:.1f}%"
    best_trade = f"${trades_df['profit_loss'].max():,.2f}"
    worst_trade = f"${trades_df['profit_loss'].min():,.2f}"
    
    # Gráfico de Balance y Equity
    balance_equity_fig = go.Figure()
    balance_equity_fig.add_trace(go.Scatter(x=trades_df['date'], y=trades_df['balance'],
                                           name='Balance', line=dict(color='#4CAF50')))
    balance_equity_fig.add_trace(go.Scatter(x=trades_df['date'], y=trades_df['equity'],
                                           name='Equity', line=dict(color='#2196F3')))
    balance_equity_fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['text']),
        xaxis=dict(gridcolor=colors['grid']),
        yaxis=dict(gridcolor=colors['grid'])
    )
    
    # Distribución de Ganancias/Pérdidas
    win_loss_fig = px.histogram(trades_df, x='profit_loss', nbins=20,
                               color_discrete_sequence=['#4CAF50'])
    win_loss_fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['text']),
        xaxis=dict(gridcolor=colors['grid']),
        yaxis=dict(gridcolor=colors['grid'])
    )
    
    # Rendimiento por Par
    pair_performance_fig = px.box(trades_df, x='pair', y='profit_loss',
                                 color='pair', color_discrete_sequence=['#4CAF50', '#2196F3', '#FFC107'])
    pair_performance_fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['text']),
        xaxis=dict(gridcolor=colors['grid']),
        yaxis=dict(gridcolor=colors['grid'])
    )
    
    # Tabla de trades
    table_data = trades_df.tail(10).to_dict('records')
    
    return (balance_total, equity_total, pl_total, win_rate, best_trade, worst_trade,
            balance_equity_fig, win_loss_fig, pair_performance_fig, table_data)

if __name__ == '__main__':
    app.run_server(debug=True)
