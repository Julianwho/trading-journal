import streamlit as st
import pandas as pd
import datetime

# Inicializar el DataFrame para almacenar las operaciones
if 'operations' not in st.session_state:
    st.session_state['operations'] = pd.DataFrame(columns=[
        'Precio de Entrada',
        'Precio de Salida',
        'Dónde estaba tu Stop Loss',
        'Dónde estaba tu Take Profit',
        'Resultado de la operación'
    ])

def add_operation(entry_price, exit_price, stop_loss, take_profit, result):
    new_row = pd.Series({
        'Precio de Entrada': entry_price,
        'Precio de Salida': exit_price,
        'Dónde estaba tu Stop Loss': stop_loss,
        'Dónde estaba tu Take Profit': take_profit,
        'Resultado de la operación': result
    })
    st.session_state['operations'] = st.session_state['operations'].append(new_row, ignore_index=True)

def display_operations():
    # Aplicar el color basado en el resultado
    def highlight_result(row):
        if row['Resultado de la operación'] < 0:
            return ['background-color: lightcoral'] * len(row)
        elif row['Resultado de la operación'] > 0:
            return ['background-color: lightgreen'] * len(row)
        return [''] * len(row)

    # Mostrar la tabla
    styled_df = st.session_state['operations'].style.apply(highlight_result, axis=1)
    st.write(styled_df)

def main():
    st.title("Registro de Operaciones")

    # Entradas de usuario
    entry_price = st.number_input("Precio de Entrada", step=0.01)
    exit_price = st.number_input("Precio de Salida", step=0.01)
    stop_loss = st.number_input("Dónde estaba tu Stop Loss", step=0.01)
    take_profit = st.number_input("Dónde estaba tu Take Profit", step=0.01)
    result = st.number_input("Resultado de la operación", step=1.0)

    if st.button("Agregar Operación"):
        add_operation(entry_price, exit_price, stop_loss, take_profit, result)
        st.success("Operación añadida exitosamente!")

    # Mostrar operaciones
    display_operations()

if __name__ == "__main__":
    main()
