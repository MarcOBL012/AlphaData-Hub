import pandas as pd
import pandas_datareader.data as web
from datetime import datetime

def extraer_china_macro():
    # 1. Configuración de Series
    # CHILPR1Y: China Loan Prime Rate (1 Year) - Dato mensual oficial desde 2019
    # CSCICP03CNM665S: OECD Consumer Confidence China (Normalizado, 100=Promedio)
    # QCNR628BIS: Real Residential Property Prices for China (Trimestral -> lo convertiremos)
    
    series_mensuales = {
        'CHILPR1Y': 'China_LPR_1Y',
        'CSCICP03CNM665S': 'China_Consumer_Conf_Index'
    }
    
    series_trimestrales = {
        'QCNR628BIS': 'China_Real_Estate_Prices_Index'
    }

    fecha_inicio = '2010-01-01' # Tomamos desde 2010 para tener buen histórico
    fecha_fin = datetime.now()

    print("Conectando con FRED para datos de China...")
    
    try:
        # --- PASO 1: Extraer Datos Mensuales ---
        df_m = web.DataReader(list(series_mensuales.keys()), 'fred', fecha_inicio, fecha_fin)
        df_m = df_m.rename(columns=series_mensuales)

        # --- PASO 2: Extraer Datos Trimestrales (Real Estate) ---
        df_q = web.DataReader(list(series_trimestrales.keys()), 'fred', fecha_inicio, fecha_fin)
        df_q = df_q.rename(columns=series_trimestrales)

        # --- PASO 3: Procesamiento y Transformación ---
        
        # A) Resamplear Real Estate de Trimestral a Mensual
        # Usamos 'ffill' (forward fill) para propagar el último dato conocido a los meses siguientes
        df_q_monthly = df_q.resample('MS').ffill()
        
        # B) Unir ambos DataFrames por el índice (Fecha)
        df_total = df_m.join(df_q_monthly, how='outer')

        # C) Calcular YoY para Real Estate (Crecimiento Anual)
        # La serie original es un Índice, así que calculamos la variación % de 12 meses
        df_total['China_Real_Estate_YoY'] = df_total['China_Real_Estate_Prices_Index'].pct_change(periods=12) * 100

        # --- PASO 4: Limpieza Final ---
        df_reset = df_total.reset_index()
        df_reset['Año-Mes'] = df_reset['DATE'].dt.strftime('%Y-%m')
        
        # Seleccionar columnas finales
        cols = ['Año-Mes', 'China_LPR_1Y', 'China_Consumer_Conf_Index', 'China_Real_Estate_YoY']
        df_final = df_reset[cols]
        
        # Filtrar datos vacíos recientes o muy antiguos
        df_final = df_final.dropna(subset=['China_Consumer_Conf_Index']) 
        df_final = df_final[df_final['Año-Mes'] >= '2015-01'] # Filtramos desde 2015 para ver mejor el LPR

        # --- PASO 5: Exportar ---
        archivo = 'macro_china_data.csv'
        df_final.to_csv(archivo, index=False, float_format='%.2f')
        
        print(f"¡Éxito! Archivo generado: {archivo}")
        print("\nVista previa de los datos:")
        print(df_final.tail(10))

    except Exception as e:
        print(f"Error extrayendo datos: {e}")
        print("Tip: Verifica tu conexión. Algunos datos de China en FRED pueden tener retraso de 1-2 meses.")

if __name__ == '__main__':
    extraer_china_macro()