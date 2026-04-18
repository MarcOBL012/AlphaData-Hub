import requests
from bs4 import BeautifulSoup

def obtener_tipo_cambio_actual():
    url = "https://www.sbs.gob.pe/app/pp/SISTIP_PORTAL/Paginas/Publicacion/TipoCambioPromedio.aspx"
    
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encontrar la tabla de tipos de cambio
    table = soup.find('table', {'id': 'ctl00_cphContent_rgTipoCambio_ctl00'})
    
    if not table:
        print("No se encontró la tabla de tipos de cambio.")
        return None, None
    
    rows = table.find_all('tr')
    
    for row in rows:
        cols = row.find_all('td')
        if cols and "Dólar de N.A." in cols[0].text:
            compra = cols[1].text.strip()
            venta = cols[2].text.strip()
            return compra, venta
    
    print("No se encontró la fila del dólar.")
    return None, None

if __name__ == "__main__":
    compra, venta = obtener_tipo_cambio_actual()
    if compra and venta:
        print(f"Tipo de cambio actual del dólar a sol:")
        print(f"Compra: {compra} PEN")
        print(f"Venta: {venta} PEN")
    else:
        print("No se pudo obtener el tipo de cambio.")
