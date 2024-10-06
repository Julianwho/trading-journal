import plotly.express as px

# ... (código anterior)

# Navegación entre pestañas
tab = st.sidebar.selectbox("Selecciona una pestaña", ["Registro de Operaciones", "Estadísticas y Rendimiento"])

if tab == "Registro de Operaciones":
    # Código existente para Registro de Operaciones...
    # (aquí va el código anterior del registro de operaciones)

elif tab == "Estadísticas y Rendimiento":
    # Título de la sección
    st.title("Estadísticas y Rendimiento")

    # Cálculos de estadísticas
    df["Result ($)"] = df["Result ($)"].astype(float)  # Asegúrate de que sea tipo float
    df["Date Close"] = pd.to_datetime(df["Date Close"])  # Convertir a tipo datetime

    # Ganancias y pérdidas acumuladas
    df['Cumulative P&L'] = df['Result ($)'].cumsum()

    # Ratio de aciertos (win rate)
    total_trades = len(df)
    win_trades = len(df[df['Status'] == "WIN"])
    win_rate = (win_trades / total_trades) * 100 if total_trades > 0 else 0

    # Expectativa de operación
    expectation = df['Result ($)'].mean()

    # Promedio de ganancias/pérdidas por operación
    avg_gain = df[df['Status'] == "WIN"]['Result ($)'].mean() if win_trades > 0 else 0
    avg_loss = df[df['Status'] == "LOSS"]['Result ($)'].mean() if total_trades - win_trades > 0 else 0

    # Máxima racha de operaciones ganadoras y perdedoras
    df['Win Streak'] = df['Status'].eq("WIN").astype(int).groupby(df['Status'].ne(df['Status'].shift()).cumsum()).cumsum()
    df['Loss Streak'] = df['Status'].eq("LOSS").astype(int).groupby(df['Status'].ne(df['Status'].shift()).cumsum()).cumsum()

    max_win_streak = df['Win Streak'].max()
    max_loss_streak = df['Loss Streak'].max()

    # Gráficos de estadísticas
    st.subheader("Ganancias y Pérdidas Acumuladas")
    fig = px.line(df, x='Date Close', y='Cumulative P&L', title='P&L Acumulado')
    st.plotly_chart(fig)

    st.subheader("Estadísticas Generales")
    st.metric("Win Rate (%)", win_rate)
    st.metric("Expectativa de Operación ($)", expectation)
    st.metric("Promedio de Ganancias ($)", avg_gain)
    st.metric("Promedio de Pérdidas ($)", avg_loss)
    st.metric("Máxima Racha de Ganancias", max_win_streak)
    st.metric("Máxima Racha de Pérdidas", max_loss_streak)

    # Comparación por tipo de operación
    # Suponiendo que tengas una columna "Tipo de Operación" en tu DataFrame
    if 'Order Type' in df.columns:
        order_type_stats = df.groupby('Order Type')['Result ($)'].sum().reset_index()
        fig2 = px.bar(order_type_stats, x='Order Type', y='Result ($)', title='Ganancias/Pérdidas por Tipo de Operación')
        st.plotly_chart(fig2)

    # Análisis adicional aquí...
