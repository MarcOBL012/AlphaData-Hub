import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv

def scrape_exchange_rates():
    """
    Scrape USD buy/sell exchange rates from SBS Peru
    from January 1, 2021 to current date
    """
    url = "https://www.sbs.gob.pe/app/pp/SISTIP_PORTAL/Paginas/Publicacion/TipoCambioPromedio.aspx"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table with exchange rates
        table = soup.find('table', {'class': 'table'})
        
        if not table:
            print("No table found. Check page structure.")
            return
        
        rows = table.find_all('tr')[1:]  # Skip header row
        
        exchange_data = []
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:
                try:
                    fecha = cols[0].text.strip()
                    compra = cols[1].text.strip()
                    venta = cols[2].text.strip()
                    
                    exchange_data.append({
                        'fecha': fecha,
                        'compra': compra,
                        'venta': venta
                    })
                except Exception as e:
                    print(f"Error parsing row: {e}")
                    continue
        
        # Save to CSV
        if exchange_data:
            with open('exchange_rates.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['fecha', 'compra', 'venta'])
                writer.writeheader()
                writer.writerows(exchange_data)
            
            print(f"Extracted {len(exchange_data)} records")
            print("Saved to exchange_rates.csv")
        else:
            print("No data found")
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")

if __name__ == "__main__":
    scrape_exchange_rates()