import pandas as pd
import plotly.express as px
import datetime
import os

# Crear un archivo CSV si no existe
if not os.path.isfile('emotional_journal.csv'):
    df = pd.DataFrame(columns=["Fecha", "Emotion Before", "Emotion During", "Emotion After", "Limiting Beliefs"])
    df.to_csv('emotional_journal.csv', index=False)

elif tab == "Análisis de Psicología y Emociones":
    st.title("Análisis de Psicología y Emociones")

    # Sección para registrar emociones
    st.subheader("Diario Emocional")

    # Campo para ingresar la fecha
    date = st.date_input("Fecha de la operación", datetime.date.today())
    
    # Formulario para registrar emociones
    emotion_before = st.selectbox("¿Cómo te sentías antes de la operación?", options=["Estrés", "Ansiedad", "Confianza", "Indecisión", "Tranquilo"])
    emotion_during = st.selectbox("¿Cómo te sentías durante la operación?", options=["Estrés", "Ansiedad", "Confianza", "Indecisión", "Tranquilo"])
    emotion_after = st.selectbox("¿Cómo te sentías después de la operación?", options=["Estrés", "Ansiedad", "Confianza", "Indecisión", "Tranquilo"])

    # Registrar creencias limitantes
    limiting_beliefs = st.text_area("Identifica y analiza tus creencias limitantes")

    # Botón para guardar las emociones
    if st.button("Guardar Emociones"):
        # Agregar registro de emociones a un archivo CSV
        emotion_entry = {
            "Fecha": date,
            "Emotion Before": emotion_before,
            "Emotion During": emotion_during,
            "Emotion After": emotion_after,
            "Limiting Beliefs": limiting_beliefs
        }
        
        # Leer el archivo CSV existente
        df = pd.read_csv('emotional_journal.csv')
        # Agregar la nueva entrada
        df = df.append(emotion_entry, ignore_index=True)
        # Guardar de nuevo en el CSV
        df.to_csv('emotional_journal.csv', index=False)
        
        st.success("Emociones guardadas exitosamente!")

    # Mostrar los registros guardados
    st.subheader("Registros de Emociones")
    if os.path.isfile('emotional_journal.csv'):
        df_records = pd.read_csv('emotional_journal.csv')
        st.dataframe(df_records)

    # Sección para mostrar gráficos de emociones
    st.subheader("Gráficos de Emociones")
    
    # Simular algunos datos para mostrar (esto puede reemplazarse por datos reales)
    if not df_records.empty:
        emotional_df = df_records.copy()
        emotional_df['Resultado'] = ['Ganadora' if i % 2 == 0 else 'Perdedora' for i in range(len(emotional_df))]  # Simulando resultados
        emotional_df["Emoción Antes"] = emotional_df["Emotion Before"].apply(lambda x: ["Estrés", "Ansiedad", "Confianza", "Indecisión", "Tranquilo"].index(x) + 1)
        emotional_df["Emoción Durante"] = emotional_df["Emotion During"].apply(lambda x: ["Estrés", "Ansiedad", "Confianza", "Indecisión", "Tranquilo"].index(x) + 1)
        emotional_df["Emoción Después"] = emotional_df["Emotion After"].apply(lambda x: ["Estrés", "Ansiedad", "Confianza", "Indecisión", "Tranquilo"].index(x) + 1)

        # Gráfico de emociones
        fig_emotions = px.box(emotional_df, x="Resultado", y=["Emoción Antes", "Emoción Durante", "Emoción Después"],
                               labels={"value": "Nivel de Emoción", "variable": "Estado Emocional"},
                               title="Impacto Emocional por Resultado de la Operación",
                               color="Resultado")

        fig_emotions.update_layout(template='plotly_white', hovermode='x unified')

        st.plotly_chart(fig_emotions)

    # Análisis de creencias limitantes
    st.subheader("Análisis de Creencias Limitantes")
    st.write("Aquí puedes reflexionar sobre cómo estas creencias afectan tus decisiones de trading.")
