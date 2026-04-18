"""
Script para extraer proyecciones de precios de metales (Oro, Plata, Cobre)
de JP Morgan, UBS y Goldman Sachs, y calcular la mediana.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime
import json
import re
import time

class MetalProjectionScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.metals = ['Gold', 'Silver', 'Copper']
        self.banks = ['JP Morgan', 'UBS', 'Goldman Sachs']
        self.projections = []
        
    def search_bank_projections(self, bank, metal):
        """
        Busca proyecciones de un banco específico para un metal
        """
        # URLs base para buscar informes (estas pueden necesitar actualización)
        search_urls = {
            'JP Morgan': f'https://www.jpmorgan.com/insights/research/{metal.lower()}-outlook',
            'UBS': f'https://www.ubs.com/global/en/wealth-management/insights/{metal.lower()}.html',
            'Goldman Sachs': f'https://www.goldmansachs.com/insights/pages/{metal.lower()}-forecast.html'
        }
        
        try:
            # Nota: En la práctica, muchos de estos sitios requieren autenticación
            # o los datos están en PDFs/informes que necesitan descarga
            url = search_urls.get(bank, '')
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Buscar patrones de precios (esto es un ejemplo genérico)
                price_pattern = re.compile(r'\$?\d{1,5}(?:,\d{3})*(?:\.\d{2})?')
                prices = price_pattern.findall(soup.get_text())
                return prices
            
        except Exception as e:
            print(f"Error scraping {bank} - {metal}: {str(e)}")
            return None
    
    def get_kitco_consensus(self, metal):
        """
        Alternativa: Obtener consenso de analistas desde Kitco
        (Kitco agrega proyecciones de múltiples bancos)
        """
        try:
            url = 'https://www.kitco.com/market-analyst-predictions.html'
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            # Buscar tabla de proyecciones
            # Este código es un ejemplo y necesitaría adaptarse a la estructura real
            return None
        except Exception as e:
            print(f"Error getting Kitco data: {str(e)}")
            return None
    
    def search_investing_com(self, metal):
        """
        Buscar proyecciones en Investing.com
        """
        metal_urls = {
            'Gold': 'https://www.investing.com/commodities/gold',
            'Silver': 'https://www.investing.com/commodities/silver',
            'Copper': 'https://www.investing.com/commodities/copper'
        }
        
        try:
            url = metal_urls.get(metal)
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extraer datos de consenso de analistas
            return None
        except Exception as e:
            print(f"Error searching Investing.com: {str(e)}")
            return None
    
    def manual_data_entry(self):
        """
        Método para ingresar datos manualmente si el scraping no funciona
        (los datos se obtienen de informes públicos/noticias)
        """
        print("\n=== INGRESO MANUAL DE PROYECCIONES ===")
        print("Ingresa las proyecciones que encontraste para cada combinación:")
        print("(Presiona Enter sin valor para omitir)\n")
        
        data = []
        
        for metal in self.metals:
            for bank in self.banks:
                print(f"\n{bank} - {metal}")
                
                # Proyección Q1 2026
                q1 = input(f"  Proyección Q1 2026 (USD): ")
                if q1:
                    data.append({
                        'Bank': bank,
                        'Metal': metal,
                        'Period': 'Q1 2026',
                        'Price_USD': float(q1.replace(',', ''))
                    })
                
                # Proyección Q2 2026
                q2 = input(f"  Proyección Q2 2026 (USD): ")
                if q2:
                    data.append({
                        'Bank': bank,
                        'Metal': metal,
                        'Period': 'Q2 2026',
                        'Price_USD': float(q2.replace(',', ''))
                    })
                
                # Proyección año completo 2026
                year = input(f"  Proyección promedio 2026 (USD): ")
                if year:
                    data.append({
                        'Bank': bank,
                        'Metal': metal,
                        'Period': '2026 Avg',
                        'Price_USD': float(year.replace(',', ''))
                    })
        
        return pd.DataFrame(data)
    
    def load_sample_data(self):
        """
        Carga datos de ejemplo basados en proyecciones típicas
        (ESTOS SON DATOS DE EJEMPLO - DEBEN SER REEMPLAZADOS CON DATOS REALES)
        """
        sample_data = [
            # ORO (USD/oz)
            {'Bank': 'JP Morgan', 'Metal': 'Gold', 'Period': 'Q1 2026', 'Price_USD': 2750},
            {'Bank': 'JP Morgan', 'Metal': 'Gold', 'Period': 'Q2 2026', 'Price_USD': 2800},
            {'Bank': 'JP Morgan', 'Metal': 'Gold', 'Period': '2026 Avg', 'Price_USD': 2775},
            
            {'Bank': 'UBS', 'Metal': 'Gold', 'Period': 'Q1 2026', 'Price_USD': 2700},
            {'Bank': 'UBS', 'Metal': 'Gold', 'Period': 'Q2 2026', 'Price_USD': 2725},
            {'Bank': 'UBS', 'Metal': 'Gold', 'Period': '2026 Avg', 'Price_USD': 2710},
            
            {'Bank': 'Goldman Sachs', 'Metal': 'Gold', 'Period': 'Q1 2026', 'Price_USD': 2850},
            {'Bank': 'Goldman Sachs', 'Metal': 'Gold', 'Period': 'Q2 2026', 'Price_USD': 2900},
            {'Bank': 'Goldman Sachs', 'Metal': 'Gold', 'Period': '2026 Avg', 'Price_USD': 2875},
            
            # PLATA (USD/oz)
            {'Bank': 'JP Morgan', 'Metal': 'Silver', 'Period': 'Q1 2026', 'Price_USD': 32.5},
            {'Bank': 'JP Morgan', 'Metal': 'Silver', 'Period': 'Q2 2026', 'Price_USD': 33.0},
            {'Bank': 'JP Morgan', 'Metal': 'Silver', 'Period': '2026 Avg', 'Price_USD': 32.75},
            
            {'Bank': 'UBS', 'Metal': 'Silver', 'Period': 'Q1 2026', 'Price_USD': 31.0},
            {'Bank': 'UBS', 'Metal': 'Silver', 'Period': 'Q2 2026', 'Price_USD': 31.5},
            {'Bank': 'UBS', 'Metal': 'Silver', 'Period': '2026 Avg', 'Price_USD': 31.25},
            
            {'Bank': 'Goldman Sachs', 'Metal': 'Silver', 'Period': 'Q1 2026', 'Price_USD': 34.0},
            {'Bank': 'Goldman Sachs', 'Metal': 'Silver', 'Period': 'Q2 2026', 'Price_USD': 35.0},
            {'Bank': 'Goldman Sachs', 'Metal': 'Silver', 'Period': '2026 Avg', 'Price_USD': 34.5},
            
            # COBRE (USD/lb)
            {'Bank': 'JP Morgan', 'Metal': 'Copper', 'Period': 'Q1 2026', 'Price_USD': 4.75},
            {'Bank': 'JP Morgan', 'Metal': 'Copper', 'Period': 'Q2 2026', 'Price_USD': 4.85},
            {'Bank': 'JP Morgan', 'Metal': 'Copper', 'Period': '2026 Avg', 'Price_USD': 4.80},
            
            {'Bank': 'UBS', 'Metal': 'Copper', 'Period': 'Q1 2026', 'Price_USD': 4.50},
            {'Bank': 'UBS', 'Metal': 'Copper', 'Period': 'Q2 2026', 'Price_USD': 4.60},
            {'Bank': 'UBS', 'Metal': 'Copper', 'Period': '2026 Avg', 'Price_USD': 4.55},
            
            {'Bank': 'Goldman Sachs', 'Metal': 'Copper', 'Period': 'Q1 2026', 'Price_USD': 5.00},
            {'Bank': 'Goldman Sachs', 'Metal': 'Copper', 'Period': 'Q2 2026', 'Price_USD': 5.10},
            {'Bank': 'Goldman Sachs', 'Metal': 'Copper', 'Period': '2026 Avg', 'Price_USD': 5.05},
        ]
        
        return pd.DataFrame(sample_data)
    
    def calculate_medians(self, df):
        """
        Calcula la mediana de las proyecciones por metal y período
        """
        medians = df.groupby(['Metal', 'Period'])['Price_USD'].agg([
            ('Median', 'median'),
            ('Mean', 'mean'),
            ('Min', 'min'),
            ('Max', 'max'),
            ('Count', 'count')
        ]).reset_index()
        
        return medians
    
    def create_summary_report(self, df, medians):
        """
        Crea un reporte resumen con las proyecciones
        """
        print("\n" + "="*80)
        print("RESUMEN DE PROYECCIONES DE PRECIOS DE METALES")
        print("="*80)
        
        for metal in self.metals:
            print(f"\n{metal.upper()}")
            print("-" * 80)
            
            # Datos por banco
            metal_data = df[df['Metal'] == metal]
            print("\nProyecciones por Banco:")
            print(metal_data.to_string(index=False))
            
            # Medianas
            metal_medians = medians[medians['Metal'] == metal]
            print(f"\nEstadísticas Consolidadas ({metal}):")
            print(metal_medians.to_string(index=False))
            print("\n")
    
    def export_to_excel(self, df, medians, filename='metal_projections.xlsx'):
        """
        Exporta los resultados a Excel
        """
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Proyecciones', index=False)
            medians.to_excel(writer, sheet_name='Medianas', index=False)
            
            # Crear hoja de resumen
            summary_data = []
            for metal in self.metals:
                avg_projection = medians[
                    (medians['Metal'] == metal) & 
                    (medians['Period'] == '2026 Avg')
                ]['Median'].values
                
                if len(avg_projection) > 0:
                    summary_data.append({
                        'Metal': metal,
                        'Mediana 2026': avg_projection[0]
                    })
            
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Resumen', index=False)
        
        print(f"\n✓ Datos exportados a: {filename}")


def main():
    scraper = MetalProjectionScraper()
    
    print("="*80)
    print("SCRAPER DE PROYECCIONES DE PRECIOS DE METALES")
    print("JP Morgan | UBS | Goldman Sachs")
    print("="*80)
    
    print("\nOpciones:")
    print("1. Usar datos de ejemplo (para pruebas)")
    print("2. Ingresar datos manualmente")
    print("3. Intentar web scraping automático (experimental)")
    
    choice = input("\nSelecciona una opción (1-3): ")
    
    if choice == '1':
        print("\n⚠ Usando datos de ejemplo. Reemplaza con datos reales.")
        df = scraper.load_sample_data()
    elif choice == '2':
        df = scraper.manual_data_entry()
    else:
        print("\n⚠ El scraping automático requiere configuración adicional.")
        print("Los sitios de los bancos suelen requerir autenticación o los datos")
        print("están en PDFs. Se recomienda ingreso manual o usar datos de ejemplo.\n")
        df = scraper.load_sample_data()
    
    if len(df) > 0:
        # Calcular medianas
        medians = scraper.calculate_medians(df)
        
        # Mostrar reporte
        scraper.create_summary_report(df, medians)
        
        # Exportar a Excel
        scraper.export_to_excel(df, medians)
        
        print("\n✓ Proceso completado!")
    else:
        print("\n⚠ No se ingresaron datos.")


if __name__ == "__main__":
    main()