import streamlit as st
import pandas as pd
import os
from gestor_datos import GestorDatos
from analisis import calcular_metricas_rendimiento, calcular_drawdown, analizar_estado_emocional
from visualizaciones import crear_curva_capital, crear_distribucion_operaciones, crear_grafico_torta_ganadoras_perdedoras, crear_grafico_estado_emocional

st.set_page_config(layout="wide", page_title="Diario de Trading")

# Asegúrate de que esta ruta sea accesible y escribible
ruta_archivo = 'datos/diario_trading.xlsx'

gestor_datos = GestorDatos(ruta_archivo)

st.title("Dashboard de Diario de Trading")

# Barra lateral para entrada de datos
with st.sidebar:
    st.header("Agregar Nueva Operación")
    fecha = st.date_input("Fecha")
    simbolo = st.text_input("Símbolo")
    precio_entrada = st.number_input("Precio de Entrada")
    precio_salida = st.number_input("Precio de Salida")
    tamano_posicion = st.number_input("Tamaño de la Posición")
    
    if st.button("Agregar Operación"):
        datos_operacion = {
            'Fecha': fecha,
            'Símbolo': simbolo,
            'Precio de Entrada': precio_entrada,
            'Precio de Salida': precio_salida,
            'Tamaño de la Posición': tamano_posicion,
            'Beneficio/Pérdida': (precio_salida - precio_entrada) * tamano_posicion
        }
        gestor_datos.escribir_operacion(datos_operacion)
        st.success("Operación agregada con éxito!")

    st.header("Registro de Estado Emocional")
    fecha_emocional = st.date_input("Fecha", key="fecha_emocional")
    nivel_estres = st.slider("Nivel de Estrés", 1, 10)
    nivel_confianza = st.slider("Nivel de Confianza", 1, 10)
    
    if st.button("Registrar Estado Emocional"):
        datos_emocionales = {
            'Fecha': fecha_emocional,
            'Nivel de Estrés': nivel_estres,
            'Nivel de Confianza': nivel_confianza
        }
        gestor_datos.escribir_estado_emocional(datos_emocionales)
        st.success("Estado emocional registrado con éxito!")

# Dashboard principal
df_operaciones = gestor_datos.leer_operaciones()
df_emocional = gestor_datos.leer_estado_emocional()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total de Operaciones", len(df_operaciones))

with col2:
    st.metric("Beneficio/Pérdida Total", f"${df_operaciones['Beneficio/Pérdida'].sum():.2f}")

with col3:
    tasa_aciertos = (df_operaciones['Beneficio/Pérdida'] > 0).mean()
    st.metric("Tasa de Aciertos", f"{tasa_aciertos:.2%}")

st.plotly_chart(crear_curva_capital(df_operaciones), use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(crear_distribucion_operaciones(df_operaciones), use_container_width=True)

with col2:
    st.plotly_chart(crear_grafico_torta_ganadoras_perdedoras(df_operaciones), use_container_width=True)

# Sección de Psicología
st.header("Análisis Psicológico")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(crear_grafico_estado_emocional(df_emocional), use_container_width=True)

with col2:
    correlacion_estres_rendimiento = analizar_estado_emocional(df_emocional, df_operaciones)
    st.metric("Correlación Estrés-Rendimiento", f"{correlacion_estres_rendimiento:.2f}")
    st.write("Una correlación negativa indica que a mayor estrés, menor rendimiento.")

# Añadir más secciones y visualizaciones según sea necesario
