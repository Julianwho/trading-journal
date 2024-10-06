import streamlit as st
import sqlite3
import datetime
import pandas as pd

# Conectar a la base de datos SQLite
conn = sqlite3.connect("trading_journal.db")
cursor = conn.cursor()

# Crear tablas si no existen
cursor.execute('''
CREATE TABLE IF NOT EXISTS operaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    open_time TEXT,
    simbolo TEXT,
    operacion TEXT,
    cantidad REAL,
    precio REAL,
    stop_loss REAL,
    take_profit REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS diario_emocional (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    estado_animo TEXT,
    emociones TEXT,
    creencias_limitantes TEXT
)
''')

# Título de la aplicación
st.title("Diario de Trading")

# Pestañas
tabs = st.tabs(["Registro de Operaciones", "Análisis de Psicología y Emociones"])

# Pestaña de Registro de Operaciones
with tabs[0]:
    st.header("Registro de Operaciones")
    
    # Formulario para ingresar operaciones
    with st.form(key='operaciones_form'):
        open_time = st.datetime_input("Fecha y hora de apertura", datetime.datetime.now())
        simbolo = st.text_input("Símbolo")
        operacion = st.selectbox("Tipo de operación", ["Compra", "Venta"])
        cantidad = st.number_input("Cantidad", min_value=0.0, format="%.2f")
        precio = st.number_input("Precio", min_value=0.0, format="%.2f")
        stop_loss = st.number_input("Stop Loss", min_value=0.0, format="%.2f")
        take_profit = st.number_input("Take Profit", min_value=0.0, format="%.2f")

        # Botón de envío
        submit_button = st.form_submit_button("Guardar operación")

    # Lógica para guardar la operación en la base de datos
    if submit_button:
        cursor.execute('''
        INSERT INTO operaciones (open_time, simbolo, operacion, cantidad, precio, stop_loss, take_profit)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (open_time, simbolo, operacion, cantidad, precio, stop_loss, take_profit))
        conn.commit()
        st.success("Operación guardada exitosamente.")

    # Mostrar operaciones guardadas
    st.subheader("Operaciones guardadas")
    data = cursor.execute("SELECT * FROM operaciones").fetchall()
    if data:
        for row in data:
            st.write(f"ID: {row[0]}, Fecha: {row[1]}, Símbolo: {row[2]}, Operación: {row[3]}, "
                     f"Cantidad: {row[4]}, Precio: {row[5]}, Stop Loss: {row[6]}, Take Profit: {row[7]}")
    else:
        st.write("No hay operaciones guardadas.")

# Pestaña de Análisis de Psicología y Emociones
with tabs[1]:
    st.header("Análisis de Psicología y Emociones")

    # Formulario para el diario emocional
    with st.form(key='diario_emocional_form'):
        fecha = st.date_input("Fecha de la emoción", datetime.datetime.now())
        estado_animo = st.text_input("Estado de ánimo")
        emociones = st.text_area("Emociones experimentadas")
        creencias_limitantes = st.text_area("Creencias limitantes")

        # Botón de envío
        submit_diario = st.form_submit_button("Guardar entrada del diario emocional")

    # Lógica para guardar el diario emocional en la base de datos
    if submit_diario:
        cursor.execute('''
        INSERT INTO diario_emocional (fecha, estado_animo, emociones, creencias_limitantes)
        VALUES (?, ?, ?, ?)
        ''', (fecha, estado_animo, emociones, creencias_limitantes))
        conn.commit()
        st.success("Entrada del diario emocional guardada exitosamente.")

    # Mostrar entradas del diario emocional
    st.subheader("Entradas del diario emocional guardadas")
    emocional_data = cursor.execute("SELECT * FROM diario_emocional").fetchall()
    if emocional_data:
        for row in emocional_data:
            st.write(f"ID: {row[0]}, Fecha: {row[1]}, Estado de ánimo: {row[2]}, "
                     f"Emociones: {row[3]}, Creencias limitantes: {row[4]}")
    else:
        st.write("No hay entradas del diario emocional guardadas.")

# Cerrar la conexión a la base de datos
conn.close()
