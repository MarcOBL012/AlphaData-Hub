# AlphaData-Hub
Automated Financial Extraction and Modeling Engine

# 📈 AlphaData Hub: Market Intelligence at a Click

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=for-the-badge&logo=pandas)
![TensorFlow](https://img.shields.io/badge/TensorFlow-LSTM_Forecasting-FF6F00?style=for-the-badge&logo=tensorflow)
![Selenium](https://img.shields.io/badge/Selenium-Web_Scraping-43B02A?style=for-the-badge&logo=selenium)

**AplhaData Hub** is an automated, institutional-grade system designed to centralize, process, and project macroeconomic and financial data. Inspired by platforms like the Bloomberg Terminal, this system extracts information from various official sources and international consulting firms, consolidating descriptive statistics and predictive models with a **single click**.

## 🚀 Key Features

* **Multi-Source Extraction:** Automated scraping and API consumption from key sources like SBS, BCRP, FRED (Federal Reserve), and top investment banks (JPMorgan, UBS, Goldman Sachs).
* **Macro Processing:** Year-over-Year (YoY) analysis of key indicators such as the FED Rate, Core CPI, Unemployment, and real estate variables (e.g., the Chinese market).
* **Fixed Income Market:** Automated calculation of Yield to Maturity (YTM), modified duration, and ratios for Peruvian sovereign bonds using real-time data.
* **Commodity Projections:** Consolidation and median calculation of future estimates for metals (Gold, Silver, Copper) issued by major investment firms.
* **Deep Learning Forecasting:** Integration of recurrent neural networks (LSTM) for time-series prediction, such as estimating future exchange rates (Buy/Sell).

## 🗂️ Module Architecture

The system is divided into specialized modules that can be executed independently or consolidated:

1.  **`Scraping_SBS.py` / `extraer.py`**: A robust engine using Selenium to bypass blocks, tasked with extracting the complete historical exchange rate from the SBS portal.
2.  **`lstm.py`**: A Machine Learning module that ingests SBS data, scales values (MinMaxScaler), and trains an LSTM model to forecast the next day's exchange rate.
3.  **`Hz1.py` / `CHINA.py`**: Connectors to the FRED API to extract, resample (quarterly to monthly), and calculate YoY variations of macro indicators for the US and China.
4.  **`RCR.py`**: Fixed income analyzer. It cross-references coupon and maturity data with the BCRP yield curve to calculate the modified duration of Sovereign Bonds.
5.  **`QUET1.py` / `scraping_metales.py`**: Commodity projection collector, cleaning text via Regex from web reports and structuring the market consensus medians.

## 🛠️ Technologies Used

* **Language:** Python
* **Data Extraction:** `BeautifulSoup4`, `Selenium`, `undetected_chromedriver`, `pandas_datareader`, `requests`.
* **Analysis & Processing:** `Pandas`, `NumPy`.
* **Machine Learning:** `TensorFlow` / `Keras` (LSTM, Dropout, Dense), `Scikit-learn`.
* **Visualization:** `Matplotlib`.

## ⚙️ Installation and Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/MarcOBL012/AlphaData-Hub.git
   cd AlphaData-Hub
    ```

2. Install the required dependencies:

 ```Bash
pip install -r requirements.txt

 ```
