import pandas as pd
import numpy as np
import requests
from datetime import datetime

bonos_data = [
    {"ticker": "PERUGB 8.2 08/12/2026", "cupon": 0.0820, "vencimiento": "2026-08-12", "ytm_img": 3.87},
    {"ticker": "PERUGB 6.35 08/12/2028", "cupon": 0.0635, "vencimiento": "2028-08-12", "ytm_img": 3.97},
    {"ticker": "PERUGB 6 02/12/2029", "cupon": 0.0600, "vencimiento": "2029-02-12", "ytm_img": 4.05},
    {"ticker": "PERUGB 5.94 02/12/2029", "cupon": 0.0594, "vencimiento": "2029-02-12", "ytm_img": 4.04},
    {"ticker": "PERUGB 2.8893 02/12/2030", "cupon": 0.028893, "vencimiento": "2030-02-12", "ytm_img": 2.03},
    {"ticker": "PERUGB 6.95 08/12/2031", "cupon": 0.0695, "vencimiento": "2031-08-12", "ytm_img": 4.37},
    {"ticker": "PERUGB 6.15 08/12/2032", "cupon": 0.0615, "vencimiento": "2032-08-12", "ytm_img": 4.58},
    {"ticker": "PERUGB 7.3 08/12/2033", "cupon": 0.0730, "vencimiento": "2033-08-12", "ytm_img": 4.96},
    {"ticker": "PERUGB 5.4 08/12/2034", "cupon": 0.0540, "vencimiento": "2034-08-12", "ytm_img": 5.38},
    {"ticker": "PERUGB 6.85 08/12/2035", "cupon": 0.0685, "vencimiento": "2035-08-12", "ytm_img": 5.77},
    {"ticker": "PERUGB 7.39 01/31/2035", "cupon": 0.0739, "vencimiento": "2035-01-31", "ytm_img": 2.89},
    {"ticker": "PERUGB 6.9 08/12/2037", "cupon": 0.0690, "vencimiento": "2037-08-12", "ytm_img": 6.24},
    {"ticker": "PERUGB 7.6 08/12/2039", "cupon": 0.0760, "vencimiento": "2039-08-12", "ytm_img": 6.47},
    {"ticker": "PERUGB 5.35 08/12/2040", "cupon": 0.0535, "vencimiento": "2040-08-12", "ytm_img": 6.47},
    {"ticker": "PERUGB 6.85 02/12/2042", "cupon": 0.0685, "vencimiento": "2042-02-12", "ytm_img": 6.16},
    {"ticker": "PERUGB 3.1412 02/12/2040", "cupon": 0.031412, "vencimiento": "2040-02-12", "ytm_img": 3.93},
    {"ticker": "PERUGB 6.7142 02/12/2055", "cupon": 0.067142, "vencimiento": "2055-02-12", "ytm_img": 6.12},
    {"ticker": "PERUGB 3.83 08/12/2046", "cupon": 0.0383, "vencimiento": "2046-08-12", "ytm_img": 3.19},
    {"ticker": "PERUGB 3.2669 02/12/2054", "cupon": 0.032669, "vencimiento": "2054-02-12", "ytm_img": 3.66},
]

def get_latest_ytm_bcrp(series_code):
    url = f"https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{series_code}/json"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return float(data['periods'][-1]['values'][0]) / 100
    except:
        return None

def calcular_duracion_modificada(ytm, cupon, años_a_vencimiento, frecuencia=2):
    if ytm is None or ytm == 0 or años_a_vencimiento <= 0: 
        return 0
    
    cash_flows = []
    times = []
    num_periodos = max(1, int(años_a_vencimiento * frecuencia))
    
    for i in range(1, num_periodos + 1):
        t = i / frecuencia
        cf = (cupon / frecuencia) * 100
        if i == num_periodos:
            cf += 100
        tasa_periodo = ytm / frecuencia
        descuento = (1 + tasa_periodo) ** i
        pv = cf / descuento
        cash_flows.append(pv)
        times.append(t)
    
    price = sum(cash_flows)
    if price == 0:
        return 0
    
    macaulay_duration = sum([cf_p * t for cf_p, t in zip(cash_flows, times)]) / price
    tasa_periodo = ytm / frecuencia
    mod_duration = macaulay_duration / (1 + tasa_periodo)
    return round(mod_duration, 4)


resultados = []

fecha_referencia = datetime(2024, 1, 1) 

for b in bonos_data:
    venc = datetime.strptime(b['vencimiento'], "%Y-%m-%d")
    años = (venc - fecha_referencia).days / 365.25
    
    
    ytm_actual = b['ytm_img'] / 100 
    
    mod_dur = calcular_duracion_modificada(ytm_actual, b['cupon'], años, frecuencia=2)
    
    ratio = (ytm_actual * 100) / mod_dur if mod_dur > 0 else 0
    
    resultados.append({
        "Tickers": b['ticker'],
        "Modified Duration (yrs)": mod_dur,
        "YTM (%)": round(ytm_actual * 100, 2),
        "YTM/Modified Duration": round(ratio, 2)
    })

df = pd.DataFrame(resultados)
print("REPORTE COMPLETO DE BONOS SOBERANOS PERÚ (TODOS LOS AÑOS)")
print("-" * 90)
print(df.to_string(index=False))

# Guardar a CSV
nombre_archivo = 'bonos_soberanos_peru.csv'
df.to_csv(nombre_archivo, index=False)
print(f"\nArchivo guardado exitosamente: {nombre_archivo}")