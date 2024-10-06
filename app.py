import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime

# Inicializar la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Crear un DataFrame vacío para almacenar las operaciones
df = pd.DataFrame(columns=['Par', 'Fecha_Apertura', 'Fecha_Cierre', 'Tipo_Orden', 'Precio_Entrada', 'Precio_Salida', 
                           'Stop_Loss', 'Take_Profit', 'Tamaño_Posicion', 'Resultado_Pips', 'Resultado_Dinero', 
                           'Spread', 'Slippage', 'Comisiones', 'Motivo', 'Notas'])

# Diseño del dashboard
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Dashboard de Trading"), className="mb-4")
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Registro de Operaciones"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(dcc.Input(id='par', placeholder='Par de divisas', type='text')),
                        dbc.Col(dcc.DatePickerSingle(id='fecha-apertura', placeholder='Fecha de apertura')),
                        dbc.Col(dcc.DatePickerSingle(id='fecha-cierre', placeholder='Fecha de cierre')),
                    ]),
                    dbc.Row([
                        dbc.Col(dcc.Dropdown(id='tipo-orden', options=[
                            {'label': 'Market', 'value': 'Market'},
                            {'label': 'Limit', 'value': 'Limit'},
                            {'label': 'Stop', 'value': 'Stop'}
                        ], placeholder='Tipo de orden')),
                        dbc.Col(dcc.Input(id='precio-entrada', placeholder='Precio de entrada', type='number')),
                        dbc.Col(dcc.Input(id='precio-salida', placeholder='Precio de salida', type='number')),
                    ]),
                    dbc.Row([
                        dbc.Col(dcc.Input(id='stop-loss', placeholder='Stop Loss', type='number')),
                        dbc.Col(dcc.Input(id='take-profit', placeholder='Take Profit', type='number')),
                        dbc.Col(dcc.Input(id='tamaño-posicion', placeholder='Tamaño de posición', type='number')),
                    ]),
                    dbc.Row([
                        dbc.Col(dcc.Input(id='resultado-pips', placeholder='Resultado en pips', type='number')),
                        dbc.Col(dcc.Input(id='resultado-dinero', placeholder='Resultado en dinero', type='number')),
                        dbc.Col(dcc.Input(id='spread', placeholder='Spread', type='number')),
                    ]),
                    dbc.Row([
                        dbc.Col(dcc.Input(id='slippage', placeholder='Slippage', type='number')),
                        dbc.Col(dcc.Input(id='comisiones', placeholder='Comisiones', type='number')),
                        dbc.Col(dcc.Dropdown(id='motivo', options=[
                            {'label': 'Fundamental', 'value': 'Fundamental'},
                            {'label': 'Técnico', 'value': 'Técnico'}
                        ], placeholder='Motivo')),
                    ]),
                    dbc.Row([
                        dbc.Col(dcc.Textarea(id='notas', placeholder='Notas personales', style={'width': '100%', 'height': 100})),
                    ]),
                    dbc.Button("Registrar Operación", id='submit-button', color="primary", className="mt-3"),
                ])
            ], className="mb-4"),
            
            dbc.Card([
                dbc.CardHeader("Resumen de Operaciones"),
                dbc.CardBody([
                    dcc.Graph(id='resumen-grafico')
                ])
            ])
        ], width=8),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Estadísticas"),
                dbc.CardBody([
                    html.Div(id='estadisticas')
                ])
            ], className="mb-4"),
            
            dbc.Card([
                dbc.CardHeader("Últimas Operaciones"),
                dbc.CardBody([
                    html.Div(id='ultimas-operaciones')
                ])
            ])
        ], width=4)
    ])
], fluid=True)

# Callback para registrar una nueva operación
@app.callback(
    Output('estadisticas', 'children'),
    Output('ultimas-operaciones', 'children'),
    Output('resumen-grafico', 'figure'),
    Input('submit-button', 'n_clicks'),
    [State('par', 'value'),
     State('fecha-apertura', 'date'),
     State('fecha-cierre', 'date'),
     State('tipo-orden', 'value'),
     State('precio-entrada', 'value'),
     State('precio-salida', 'value'),
     State('stop-loss', 'value'),
     State('take-profit', 'value'),
     State('tamaño-posicion', 'value'),
     State('resultado-pips', 'value'),
     State('resultado-dinero', 'value'),
     State('spread', 'value'),
     State('slippage', 'value'),
     State('comisiones', 'value'),
     State('motivo', 'value'),
     State('notas', 'value')]
)
def registrar_operacion(n_clicks, par, fecha_apertura, fecha_cierre, tipo_orden, precio_entrada, precio_salida,
                        stop_loss, take_profit, tamaño_posicion, resultado_pips, resultado_dinero, spread,
                        slippage, comisiones, motivo, notas):
    global df
    if n_clicks is None:
        return dash.no_update, dash.no_update, dash.no_update
    
    nueva_operacion = pd.DataFrame({
        'Par': [par],
        'Fecha_Apertura': [fecha_apertura],
        'Fecha_Cierre': [fecha_cierre],
        'Tipo_Orden': [tipo_orden],
        'Precio_Entrada': [precio_entrada],
        'Precio_Salida': [precio_salida],
        'Stop_Loss': [stop_loss],
        'Take_Profit': [take_profit],
        'Tamaño_Posicion': [tamaño_posicion],
        'Resultado_Pips': [resultado_pips],
        'Resultado_Dinero': [resultado_dinero],
        'Spread': [spread],
        'Slippage': [slippage],
        'Comisiones': [comisiones],
        'Motivo': [motivo],
        'Notas': [notas]
    })
    
    df = pd.concat([df, nueva_operacion], ignore_index=True)
    
    # Actualizar estadísticas
    estadisticas = html.Div([
        html.P(f"Total de operaciones: {len(df)}"),
        html.P(f"Ganancia total: {df['Resultado_Dinero'].sum():.2f}"),
        html.P(f"Operaciones ganadoras: {len(df[df['Resultado_Dinero'] > 0])}")
    ])
    
    # Actualizar últimas operaciones
    ultimas_operaciones = html.Div([
        html.P(f"{row['Par']} - {row['Resultado_Dinero']:.2f}") for _, row in df.tail(5).iterrows()
    ])
    
    # Actualizar gráfico de resumen
    fig = go.Figure(data=[go.Bar(x=df['Par'], y=df['Resultado_Dinero'])])
    fig.update_layout(title='Resultado por Par de Divisas')
    
    return estadisticas, ultimas_operaciones, fig

if __name__ == '__main__':
    app.run_server(debug=True)
