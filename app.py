import streamlit as st
import pandas as pd
import datetime
import base64
import os

# Funciones para cargar imágenes
def load_image(image_file):
    img = open(image_file, "rb").read()
    return f'<img src="data:image/png;base64,{base64.b64encode(img).decode()}" style="width: 100%;"/>'

# Configuración inicial
st.set_page_config(page_title="Trading Journal", layout="wide")

# Cargar datos desde un archivo CSV
def load_data():
    if os.path.exists("trading_data.csv"):
        return pd.read_csv("trading_data.csv")
    else:
        return pd.DataFrame(columns=[
            "Currency Pair", "Open Date", "Close Date", "Order Type", "Entry Price", 
            "Exit Price", "Stop Loss", "Take Profit", "Position Size", "Pips", 
            "Result", "Spread", "Slippage", "Commission", "Reason", "Notes", 
            "Image", "FOMO", "Impatience", "Revenge Trading"
        ])

# Guardar datos en un archivo CSV
def save_data(df):
    df.to_csv("trading_data.csv", index=False)

# Función principal de la aplicación
def main():
    st.title("Trading Journal")

    # Cargar o inicializar los datos
    df = load_data()

    # Pestañas
    tabs = st.tabs(["Registro de Operaciones", "Estadísticas y Rendimiento", "Análisis de Psicología y Emociones"])

    # Pestaña de Registro de Operaciones
    with tabs[0]:
        st.header("Registro de Operaciones")

        # Entradas de datos
        currency_pair = st.text_input("Par de divisas (o activo)")
        open_date = st.sidebar.date_input("Fecha de Apertura", value=datetime.datetime.now().date())
        close_date = st.sidebar.date_input("Fecha de Cierre", value=datetime.datetime.now().date())
        order_type = st.selectbox("Tipo de Orden", ["Market", "Limit", "Stop"])
        entry_price = st.number_input("Precio de Entrada", format="%.2f")
        exit_price = st.number_input("Precio de Salida", format="%.2f")
        stop_loss = st.number_input("Stop-Loss", format="%.2f")
        take_profit = st.number_input("Take-Profit", format="%.2f")
        position_size = st.number_input("Tamaño de la Posición (lotes)", format="%.2f")
        spread = st.number_input("Spread", format="%.2f")
        slippage = st.number_input("Slippage", format="%.2f")
        commission = st.number_input("Comisiones", format="%.2f")
        reason = st.selectbox("Motivo de la Operación", ["Fundamental", "Técnico"])
        notes = st.text_area("Notas Personales")
        fomo = st.checkbox("FOMO")
        impatience = st.checkbox("Impatiencia")
        revenge_trading = st.checkbox("Trading Revenge")

        # Subida de imagen
        image_file = st.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])

        if st.button("Registrar Operación"):
            if currency_pair:
                pips = (exit_price - entry_price) * 10000  # Suponiendo pips para divisas
                result = exit_price - entry_price - commission - (spread + slippage)
                new_row = {
                    "Currency Pair": currency_pair,
                    "Open Date": open_date,
                    "Close Date": close_date,
                    "Order Type": order_type,
                    "Entry Price": entry_price,
                    "Exit Price": exit_price,
                    "Stop Loss": stop_loss,
                    "Take Profit": take_profit,
                    "Position Size": position_size,
                    "Pips": pips,
                    "Result": result,
                    "Spread": spread,
                    "Slippage": slippage,
                    "Commission": commission,
                    "Reason": reason,
                    "Notes": notes,
                    "Image": image_file.name if image_file else "",
                    "FOMO": fomo,
                    "Impatience": impatience,
                    "Revenge Trading": revenge_trading
                }
                df = df.append(new_row, ignore_index=True)
                save_data(df)
                st.success("Operación registrada exitosamente.")
            else:
                st.error("Por favor, ingresa todos los campos requeridos.")

        # Mostrar el registro de operaciones en formato de tabla
        st.write("### Registro de Operaciones")
        if not df.empty:
            df["Resultado Final"] = df["Result"].apply(lambda x: "Positiva" if x >= 0 else "Negativa")
            color_map = df["Resultado Final"].map({"Positiva": "background-color: lightgreen", "Negativa": "background-color: lightcoral"})
            styled_df = df.style.apply(lambda x: color_map, axis=1)
            st.dataframe(styled_df)

            for _, row in df.iterrows():
                st.write(f"**Par de Divisas:** {row['Currency Pair']}")
                st.write(f"**Fecha de Apertura:** {row['Open Date']}, **Fecha de Cierre:** {row['Close Date']}")
                st.write(f"**Resultado Final:** {row['Result']}")
                if row['Image']:
                    st.markdown(load_image(row['Image']) if row['Image'] else "")
                st.write(f"**Motivo de la Operación:** {row['Reason']}")
                st.write(f"**FOMO:** {'Sí' if row['FOMO'] else 'No'}, **Impatiencia:** {'Sí' if row['Impatience'] else 'No'}, **Trading Revenge:** {'Sí' if row['Revenge Trading'] else 'No'}")
                st.write("---")

    # Pestaña de Estadísticas y Rendimiento
    with tabs[1]:
        st.header("Estadísticas y Rendimiento")
        if not df.empty:
            # Calcular estadísticas
            total_trades = df.shape[0]
            wins = df[df["Result"] >= 0].shape[0]
            losses = total_trades - wins
            win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0

            st.write(f"**Total de Operaciones:** {total_trades}")
            st.write(f"**Operaciones Ganadoras:** {wins}")
            st.write(f"**Operaciones Perdedoras:** {losses}")
            st.write(f"**Ratio de Aciertos:** {win_rate:.2f}%")

            # Gráfico de Ganancias y Pérdidas
            st.subheader("Gráfico de Ganancias y Pérdidas")
            df['Cumulative P&L'] = df['Result'].cumsum()
            st.line_chart(df['Cumulative P&L'])

            # Gráfico de Operaciones por Tipo
            st.subheader("Operaciones por Tipo")
            st.bar_chart(df['Order Type'].value_counts())

    # Pestaña de Análisis de Psicología y Emociones
    with tabs[2]:
        st.header("Análisis de Psicología y Emociones")
        if not df.empty:
            emotions = df[['Open Date', 'FOMO', 'Impatience', 'Revenge Trading']]
            st.write("### Diario Emocional")
            for _, row in emotions.iterrows():
                st.write(f"**Fecha de Apertura:** {row['Open Date']}, **FOMO:** {'Sí' if row['FOMO'] else 'No'}, **Impatiencia:** {'Sí' if row['Impatience'] else 'No'}, **Trading Revenge:** {'Sí' if row['Revenge Trading'] else 'No'}")
        else:
            st.write("No hay operaciones registradas para mostrar.")

if __name__ == "__main__":
    main()
