import pandas as pd

def calcular_metricas_rendimiento(df_operaciones):
    beneficio_total = df_operaciones['Beneficio/Pérdida'].sum()
    tasa_aciertos = (df_operaciones['Beneficio/Pérdida'] > 0).mean()
    ganancia_media = df_operaciones[df_operaciones['Beneficio/Pérdida'] > 0]['Beneficio/Pérdida'].mean()
    perdida_media = df_operaciones[df_operaciones['Beneficio/Pérdida'] < 0]['Beneficio/Pérdida'].mean()
    
    return {
        'Beneficio Total': beneficio_total,
        'Tasa de Aciertos': tasa_aciertos,
        'Ganancia Media': ganancia_media,
        'Pérdida Media': perdida_media,
        'Factor de Beneficio': abs(ganancia_media / perdida_media) if perdida_media != 0 else float('inf')
    }

def calcular_drawdown(curva_capital):
    maximo_acumulado = curva_capital.cummax()
    drawdown = (curva_capital - maximo_acumulado) / maximo_acumulado
    return drawdown.min(), drawdown.idxmin()

def analizar_estado_emocional(df_emocional, df_operaciones):
    df_combinado = pd.merge(df_emocional, df_operaciones, on='Fecha', how='inner')
    if 'Nivel de Estrés' in df_combinado.columns and 'Beneficio/Pérdida' in df_combinado.columns:
        correlacion = df_combinado['Nivel de Estrés'].corr(df_combinado['Beneficio/Pérdida'])
        return correlacion
    else:
        return 0  # Valor por defecto si no hay datos suficientes
