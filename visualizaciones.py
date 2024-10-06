import plotly.graph_objects as go
import plotly.express as px

def crear_curva_capital(df_operaciones):
    retornos_acumulados = (1 + df_operaciones['Retorno']).cumprod()
    fig = go.Figure(data=go.Scatter(x=df_operaciones['Fecha'], y=retornos_acumulados, mode='lines'))
    fig.update_layout(title='Curva de Capital', xaxis_title='Fecha', yaxis_title='Capital')
    return fig

def crear_distribucion_operaciones(df_operaciones):
    fig = px.histogram(df_operaciones, x='Beneficio/Pérdida', nbins=50, title='Distribución de Operaciones')
    return fig

def crear_grafico_torta_ganadoras_perdedoras(df_operaciones):
    ganadoras = (df_operaciones['Beneficio/Pérdida'] > 0).sum()
    perdedoras = (df_operaciones['Beneficio/Pérdida'] < 0).sum()
    fig = px.pie(values=[ganadoras, perdedoras], names=['Ganadoras', 'Perdedoras'], title='Proporción Ganadoras/Perdedoras')
    return fig

def crear_grafico_estado_emocional(df_emocional):
    fig = px.line(df_emocional, x='Fecha', y=['Nivel de Estrés', 'Nivel de Confianza'], title='Estado Emocional a lo Largo del Tiempo')
    return fig
