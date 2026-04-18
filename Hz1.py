import pandas as pd
import pandas_datareader.data as web
from datetime import datetime

def extraer_macro_data_yoy():
    # 1. Definir los códigos
    # Nota: Seguiremos bajando 'CPILFESL' (el índice), pero lo transformaremos.
    indicadores = {
        'FEDFUNDS': 'Tasa_FED',
        'CPILFESL': 'CPI_Core_Index', # Descargamos el índice base
        'UNRATE': 'Tasa_Desempleo'
    }

    # Ajustamos la fecha de inicio un año antes para no perder datos al calcular el YoY del año 2000
    fecha_inicio = '1990-01-01'
    fecha_fin = datetime.now()

    print("Extrayendo datos y calculando YoY...")
    
    try:
        df = web.DataReader(list(indicadores.keys()), 'fred', fecha_inicio, fecha_fin)
        df = df.rename(columns=indicadores)
        
        # 2. CÁLCULO DEL YoY (Year-over-Year)
        # La fórmula es: (Indice_actual / Indice_hace_12_meses) - 1
        # Pandas lo hace directo con pct_change(periods=12)
        df['CPI_Core_YoY'] = df['CPI_Core_Index'].pct_change(periods=12) * 100
        
        # 3. Limpieza
        # Reseteamos índice para fecha
        df_reset = df.reset_index()
        df_reset['Año-Mes'] = df_reset['DATE'].dt.strftime('%Y-%m')
        
        # Seleccionamos solo lo que pediste (excluyendo el índice bruto)
        columnas_finales = ['Año-Mes', 'Tasa_FED', 'CPI_Core_YoY', 'Tasa_Desempleo']
        df_final = df_reset[columnas_finales]
        
        # Eliminamos las filas donde el cálculo YoY sea NaN (los primeros 12 meses)
        df_final = df_final.dropna()
        
        # Filtrar para que empiece desde el año 2000 (o tu fecha deseada)
        df_final = df_final[df_final['Año-Mes'] >= '1990-01']

        # 4. Exportar
        nombre_archivo = 'macro_usa_core_yoy.csv'
        
        # float_format='%.2f' ayuda a que el CSV tenga solo 2 decimales y sea más legible
        df_final.to_csv(nombre_archivo, index=False, float_format='%.2f')
        
        print(f"¡Listo! Archivo generado: {nombre_archivo}")
        print("\nÚltimos 5 registros:")
        print(df_final.tail())

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    extraer_macro_data_yoy()