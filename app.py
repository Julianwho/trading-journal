import streamlit as st
import pandas as pd

# Inicialización de la sesión de estado
if 'operations' not in st.session_state:
    st.session_state['operations'] = pd.DataFrame(columns=['Entry Price', 'Exit Price', 'Stop Loss', 'Take Profit', 'Result'])

# Función para agregar una operación
def add_operation(entry_price, exit_price, stop_loss, take_profit):
    result = exit_price - entry_price  # Calcular el resultado de la operación
    new_row = {'Entry Price': entry_price, 'Exit Price': exit_price, 'Stop Loss': stop_loss, 'Take Profit': take_profit, 'Result': result}
    st.session_state['operations'] = pd.concat([st.session_state['operations'], pd.DataFrame([new_row])], ignore_index=True)

# Configuración de la interfaz
st.title("Registro de Operaciones")

# Inputs para el registro de la operación
entry_price = st.number_input("Precio de Entrada", min_value=0.0, step=0.01)
exit_price = st.number_input("Precio de Salida", min_value=0.0, step=0.01)
stop_loss = st.number_input("Donde estaba tu Stop Loss", min_value=0.0, step=0.01)
take_profit = st.number_input("Donde estaba tu Take Profit", min_value=0.0, step=0.01)

if st.button("Agregar Operación"):
    add_operation(entry_price, exit_price, stop_loss, take_profit)

# Mostrar operaciones en formato de tabla
if not st.session_state['operations'].empty:
    df = st.session_state['operations']

    # Mostrar el DataFrame para verificar las columnas
    st.write("### DataFrame de Operaciones")
    st.dataframe(df)

    # Aplicar color a la columna de resultados
    def highlight_result(s):
        return ['background-color: #ffcccc' if val < 0 else 'background-color: #ccffcc' for val in s]

    try:
        styled_df = df.style.apply(highlight_result, subset=['Result'])
        st.write("### Registro de Operaciones")
        st.dataframe(styled_df)
    except KeyError as e:
        st.error(f"Error al aplicar el estilo al DataFrame: {e}")

