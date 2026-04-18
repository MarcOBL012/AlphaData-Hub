import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

# Enlaces de fuentes identificadas
sources = [
    # JPMorgan
    'https://www.jpmorgan.com/insights/global-research/commodities/gold-prices',
    'https://www.jpmorgan.com/insights/podcast-hub/research-recap/silver-market-2026',
    'https://www.jpmorgan.com/insights/markets-and-economy/top-market-takeaways/tmt-the-case-against-gold-and-why-its-wrong',
    # UBS
    'https://www.ubs.com/global/en/wealthmanagement/insights.html',
    'https://www.ubs.com/global/en/wealthmanagement/insights/global-wealth-report.html',
    # Goldman Sachs
    'https://www.goldmansachs.com/insights/goldman-sachs-research/commodity-outlook-2026-ride-the-power-race-and-supply-waves',
    'https://www.goldmansachs.com/insights/outlooks/2026-outlooks',
]

# Palabras clave para buscar precios
keywords = ['gold', 'silver', 'copper', 'oro', 'plata', 'cobre', 'forecast', 'proyeccion', '2026', '2025', '2027']

# Función para extraer texto relevante de una página

def extract_relevant_text(url):
    try:
        resp = requests.get(url, timeout=15)
        soup = BeautifulSoup(resp.text, 'html.parser')
        text = soup.get_text(separator=' ')
        # Buscar frases con precios y metales
        pattern = r'(gold|silver|copper|oro|plata|cobre)[^\d\n]{0,40}([\d,\.]+)[^\n]{0,40}(2026|2025|2027|2024|2023|2022|2021|2020)'
        matches = re.findall(pattern, text, re.IGNORECASE)
        return matches
    except Exception as e:
        print(f"Error en {url}: {e}")
        return []

# Recopilar resultados
resultados = []
for url in sources:
    print(f"Buscando en: {url}")
    matches = extract_relevant_text(url)
    for match in matches:
        resultados.append({'metal': match[0], 'precio': match[1], 'anio': match[2], 'fuente': url})

# Convertir a DataFrame y mostrar
if resultados:
    df = pd.DataFrame(resultados)
    print(df)
    df.to_csv('proyecciones_metales_scraping.csv', index=False)
    print('Archivo CSV generado: proyecciones_metales_scraping.csv')
else:
    print('No se encontraron proyecciones en las fuentes analizadas.')
