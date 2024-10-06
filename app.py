if tab == "Registro de Operaciones":
    st.title("Registro de Operaciones")

    # Sección para agregar nuevos registros
    st.sidebar.header("Agregar Registro de Operación")

    pair = st.sidebar.text_input("Par de divisas (o activo)")
    open_date = st.sidebar.date_input("Fecha y Hora de Apertura")
    close_date = st.sidebar.date_input("Fecha y Hora de Cierre")
    order_type = st.sidebar.selectbox("Tipo de Orden", 
                                       options=["Market", "Limit", "Stop"])
    entry_price = st.sidebar.number_input("Precio de Entrada")
    exit_price = st.sidebar.number_input("Precio de Salida")
    stop_loss = st.sidebar.number_input("Stop-Loss")
    take_profit = st.sidebar.number_input("Take-Profit")
    position_size = st.sidebar.number_input("Tamaño de la Posición", min_value=0.0)
    spread = st.sidebar.number_input("Tamaño del Spread", min_value=0.0)
    commission = st.sidebar.number_input("Comisiones", min_value=0.0)
    reason = st.sidebar.selectbox("Motivo de la Operación", 
                                   options=["Fundamental", "Técnico"])
    notes = st.sidebar.text_area("Notas Personales")

    if st.sidebar.button("Agregar Registro de Operación"):
        # Validar que los campos obligatorios no estén vacíos
        if entry_price <= 0 or exit_price <= 0:
            st.sidebar.error("El precio de entrada y salida deben ser mayores a 0.")
        else:
            # Calcular P&L
            if spread == 0:
                pnl_pips = 0  # Si el spread es cero, establecemos P&L en pips a 0
                pnl_money = 0  # Similar para el P&L en dinero
            else:
                pnl_pips = (exit_price - entry_price) / spread * 10000
                pnl_money = pnl_pips * position_size
            
            # Agregar una nueva fila al DataFrame
            new_trade_row = pd.DataFrame([{
                "Pair": pair,
                "Open Date": open_date,
                "Close Date": close_date,
                "Order Type": order_type,
                "Entry Price": entry_price,
                "Exit Price": exit_price,
                "Stop Loss": stop_loss,
                "Take Profit": take_profit,
                "Position Size": position_size,
                "P&L in Pips": pnl_pips,
                "P&L in Money": pnl_money,
                "Spread": spread,
                "Commission": commission,
                "Reason": reason,
                "Notes": notes
            }])
            
            # Usar pd.concat para añadir la nueva fila al DataFrame
            trade_df = pd.concat([trade_df, new_trade_row], ignore_index=True)
            
            # Guardar los datos actualizados en el archivo CSV
            save_trade_data(trade_df)
            
            st.sidebar.success("Registro de operación agregado exitosamente!")

    # Mostrar la tabla de registros de operaciones existentes
    st.subheader("Historial de Operaciones")
    st.dataframe(trade_df)
