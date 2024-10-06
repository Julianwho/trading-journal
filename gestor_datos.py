import pandas as pd
import os

class GestorDatos:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.inicializar_archivo()
        
    def inicializar_archivo(self):
        if not os.path.exists(self.ruta_archivo):
            os.makedirs(os.path.dirname(self.ruta_archivo), exist_ok=True)
            df_operaciones = pd.DataFrame(columns=['Fecha', 'Símbolo', 'Precio de Entrada', 'Precio de Salida', 'Tamaño de la Posición', 'Beneficio/Pérdida'])
            df_emocional = pd.DataFrame(columns=['Fecha', 'Nivel de Estrés', 'Nivel de Confianza'])
            with pd.ExcelWriter(self.ruta_archivo) as writer:
                df_operaciones.to_excel(writer, sheet_name='Operaciones', index=False)
                df_emocional.to_excel(writer, sheet_name='EstadoEmocional', index=False)
    
    def leer_operaciones(self):
        try:
            df = pd.read_excel(self.ruta_archivo, sheet_name='Operaciones')
            df['Fecha'] = pd.to_datetime(df['Fecha'])
            df['Retorno'] = df['Beneficio/Pérdida'] / (df['Precio de Entrada'] * df['Tamaño de la Posición'])
            return df
        except FileNotFoundError:
            print(f"Archivo no encontrado: {self.ruta_archivo}")
            return pd.DataFrame(columns=['Fecha', 'Símbolo', 'Precio de Entrada', 'Precio de Salida', 'Tamaño de la Posición', 'Beneficio/Pérdida'])
    
    def escribir_operacion(self, datos_operacion):
        df = self.leer_operaciones()
        df = pd.concat([df, pd.DataFrame([datos_operacion])], ignore_index=True)
        self.guardar_dataframe(df, 'Operaciones')
    
    def leer_estado_emocional(self):
        try:
            df = pd.read_excel(self.ruta_archivo, sheet_name='EstadoEmocional')
            df['Fecha'] = pd.to_datetime(df['Fecha'])
            return df
        except FileNotFoundError:
            print(f"Archivo no encontrado: {self.ruta_archivo}")
            return pd.DataFrame(columns=['Fecha', 'Nivel de Estrés', 'Nivel de Confianza'])
    
    def escribir_estado_emocional(self, datos_emocionales):
        df = self.leer_estado_emocional()
        df = pd.concat([df, pd.DataFrame([datos_emocionales])], ignore_index=True)
        self.guardar_dataframe(df, 'EstadoEmocional')
    
    def guardar_dataframe(self, df, nombre_hoja):
        with pd.ExcelWriter(self.ruta_archivo, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=nombre_hoja, index=False)
