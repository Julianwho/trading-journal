import pandas as pd
import os

class GestorDatos:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.inicializar_archivo()
        
    def inicializar_archivo(self):
        if not os.path.exists(self.ruta_archivo):
            # Crear el directorio si no existe
            os.makedirs(os.path.dirname(self.ruta_archivo), exist_ok=True)
            
            # Crear un DataFrame vacío con las columnas necesarias
            df_operaciones = pd.DataFrame(columns=['Fecha', 'Símbolo', 'Precio de Entrada', 'Precio de Salida', 'Tamaño de la Posición', 'Beneficio/Pérdida'])
            df_emocional = pd.DataFrame(columns=['Fecha', 'Nivel de Estrés', 'Nivel de Confianza'])
            
            # Guardar los DataFrames vacíos en el archivo Excel
            with pd.ExcelWriter(self.ruta_archivo) as writer:
                df_operaciones.to_excel(writer, sheet_name='Operaciones', index=False)
                df_emocional.to_excel(writer, sheet_name='EstadoEmocional', index=False)
    
    def leer_operaciones(self):
        try:
            return pd.read_excel(self.ruta_archivo, sheet_name='Operaciones')
        except FileNotFoundError:
            print(f"Archivo no encontrado: {self.ruta_archivo}")
            return pd.DataFrame(columns=['Fecha', 'Símbolo', 'Precio de Entrada', 'Precio de Salida', 'Tamaño de la Posición', 'Beneficio/Pérdida'])
    
    def escribir_operacion(self, datos_operacion):
        df = self.leer_operaciones()
        df = df.append(datos_operacion, ignore_index=True)
        self.guardar_dataframe(df, 'Operaciones')
    
    def leer_estado_emocional(self):
        try:
            return pd.read_excel(self.ruta_archivo, sheet_name='EstadoEmocional')
        except FileNotFoundError:
            print(f"Archivo no encontrado: {self.ruta_archivo}")
            return pd.DataFrame(columns=['Fecha', 'Nivel de Estrés', 'Nivel de Confianza'])
    
    def escribir_estado_emocional(self, datos_emocionales):
        df = self.leer_estado_emocional()
        df = df.append(datos_emocionales, ignore_index=True)
        self.guardar_dataframe(df, 'EstadoEmocional')
    
    def guardar_dataframe(self, df, nombre_hoja):
        with pd.ExcelWriter(self.ruta_archivo, mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=nombre_hoja, index=False)
