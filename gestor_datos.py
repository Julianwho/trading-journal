import pandas as pd

class GestorDatos:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        
    def leer_operaciones(self):
        return pd.read_excel(self.ruta_archivo, sheet_name='Operaciones')
    
    def escribir_operacion(self, datos_operacion):
        df = self.leer_operaciones()
        df = df.append(datos_operacion, ignore_index=True)
        with pd.ExcelWriter(self.ruta_archivo, mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name='Operaciones', index=False)
    
    def leer_estado_emocional(self):
        return pd.read_excel(self.ruta_archivo, sheet_name='EstadoEmocional')
    
    def escribir_estado_emocional(self, datos_emocionales):
        df = self.leer_estado_emocional()
        df = df.append(datos_emocionales, ignore_index=True)
        with pd.ExcelWriter(self.ruta_archivo, mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name='EstadoEmocional', index=False)
