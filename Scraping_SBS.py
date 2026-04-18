import time
import pandas as pd
import random
from datetime import datetime, timedelta
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def obtener_tipo_cambio(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    print(f"Iniciando Scraping SBS del {start_date} al {end_date}...")
    
    driver = uc.Chrome(options=options)
    
    url = "https://www.sbs.gob.pe/app/pp/SISTIP_PORTAL/Paginas/Publicacion/TipoCambioPromedio.aspx"
    driver.get(url)
    
    data = []
    current_date = start_date
    
    wait = WebDriverWait(driver, 20)

    try:
        while current_date <= end_date:
            fecha_str = current_date.strftime("%d/%m/%Y")
            
            try:
                tiempo_espera = random.uniform(3.0, 6.0)
                print(f"Esperando {tiempo_espera:.2f}s...")
                time.sleep(tiempo_espera)

                try:
                    tabla_vieja = driver.find_element(By.ID, "ctl00_cphContent_rgTipoCambio_ctl00")
                except:
                    tabla_vieja = None 

                date_input = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_cphContent_rdpDate_dateInput")))
                date_input.click()
                date_input.clear()
                
                for char in fecha_str:
                    date_input.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.2))
                
                consultar_btn = driver.find_element(By.ID, "ctl00_cphContent_btnConsultar")
                consultar_btn.click()
                
                if tabla_vieja:
                    try:
                        wait.until(EC.staleness_of(tabla_vieja))
                    except:
                        pass 
                
                wait.until(EC.presence_of_element_located((By.ID, "ctl00_cphContent_rgTipoCambio_ctl00")))

                rows = driver.find_elements(By.XPATH, "//table[@id='ctl00_cphContent_rgTipoCambio_ctl00']//tr")
                compra_val = None
                venta_val = None
                
                for row in rows:
                    if "Dólar de N.A." in row.text:
                        cols = row.find_elements(By.TAG_NAME, "td")
                        if len(cols) >= 3:
                            compra_val = cols[1].text.strip()
                            venta_val = cols[2].text.strip()
                            break
                
                if compra_val and venta_val:
                    data.append({
                        "Fecha_txt": fecha_str, 
                        "Compra": float(compra_val),
                        "Venta": float(venta_val)
                    })
                    print(f"{fecha_str}: C: {compra_val} | V: {venta_val}")
                else:
                    print(f"{fecha_str}: Sin cotización")
                    data.append({
                        "Fecha_txt": fecha_str, 
                        "Compra": None, 
                        "Venta": None
                    })

            except Exception as e:
                print(f"Error en {fecha_str}: {e}")
                time.sleep(5)
                driver.get(url)

            current_date += timedelta(days=1)
            
    finally:
        driver.quit()

    df = pd.DataFrame(data)
    if not df.empty:
        df['Fecha_dt'] = pd.to_datetime(df['Fecha_txt'], format='%d/%m/%Y')
        df = df.sort_values('Fecha_dt')
    
    return df




def main():
    today = datetime.now().strftime('%Y-%m-%d')
    df_sbs = obtener_tipo_cambio('2021-01-01', today)
    
    if not df_sbs.empty:
        df_sbs_clean = df_sbs[['Fecha_dt', 'Compra', 'Venta']]
        nombre_archivo = 'TipoCambio_CompraVenta_2021_Hoy.csv'
        df_sbs_clean.to_csv(nombre_archivo, index=False)
        print(f"Archivo guardado exitosamente: {nombre_archivo}")
    else:
        print("No se obtuvieron datos.")

if __name__ == "__main__":
    main()