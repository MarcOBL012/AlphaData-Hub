import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

# --- PASO 1: CARGA Y LIMPIEZA DE DATOS ---
def cargar_datos(archivo_csv):
    df = pd.read_csv(archivo_csv)
    df['Fecha_dt'] = pd.to_datetime(df['Fecha_dt'])
    df = df.sort_values('Fecha_dt')
    df.set_index('Fecha_dt', inplace=True)
    
    # Rellenar fines de semana o feriados con el valor del día anterior (Forward Fill)
    # Es crucial en series financieras para mantener la continuidad temporal
    df = df.asfreq('D')
    df = df.ffill()
    
    # Seleccionamos solo Compra y Venta
    dataset = df[['Compra', 'Venta']].values
    return df, dataset

# --- PASO 2: PREPARACIÓN PARA LSTM ---
def crear_dataset_lstm(dataset, look_back=60):
    """
    Crea ventanas de tiempo.
    X: Datos de los últimos 'look_back' días.
    Y: Datos del día siguiente.
    """
    X, Y = [], []
    for i in range(len(dataset) - look_back):
        X.append(dataset[i:(i + look_back), :])
        Y.append(dataset[i + look_back, :])
    return np.array(X), np.array(Y)

# --- CONFIGURACIÓN ---
ARCHIVO = 'TipoCambio_CompraVenta.csv'
LOOK_BACK = 15  # Días que el modelo "mira hacia atrás" (aumentar a 60 si tienes más datos)
EPOCHS = 50
BATCH_SIZE = 16

# Cargar
try:
    df_raw, data_values = cargar_datos(ARCHIVO)
    print("Datos cargados correctamente.")
except FileNotFoundError:
    print(f"Error: No se encuentra {ARCHIVO}. Ejecuta primero tu script de scraping.")
    exit()

# Escalamiento (MinMax es vital para que la LSTM converja)
scaler = MinMaxScaler(feature_range=(0, 1))
data_scaled = scaler.fit_transform(data_values)

# Crear estructuras X e Y
X, Y = crear_dataset_lstm(data_scaled, LOOK_BACK)

# División Train/Test (80% entrenamiento, 20% prueba)
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
Y_train, Y_test = Y[:train_size], Y[train_size:]

print(f"Forma de entrada X_train: {X_train.shape}") # (Muestras, Pasos, Features)

# --- PASO 3: ARQUITECTURA DEL MODELO ---
model = Sequential()

# Capa 1: LSTM
# return_sequences=True si vamos a añadir otra capa LSTM después
model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 2)))
model.add(Dropout(0.2)) # Evitar overfitting

# Capa 2: LSTM
model.add(LSTM(units=50, return_sequences=False))
model.add(Dropout(0.2))

# Capa de Salida: 2 neuronas (una para Compra, una para Venta)
model.add(Dense(units=2)) 

model.compile(optimizer='adam', loss='mean_squared_error')

# --- PASO 4: ENTRENAMIENTO ---
# EarlyStopping detiene el entrenamiento si no mejora para ahorrar tiempo
early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

history = model.fit(
    X_train, Y_train,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    validation_data=(X_test, Y_test),
    callbacks=[early_stop],
    verbose=1
)

# --- PASO 5: VALIDACIÓN Y VISUALIZACIÓN ---
predictions_scaled = model.predict(X_test)

# Invertir la escala para obtener valores reales en Soles
predictions = scaler.inverse_transform(predictions_scaled)
Y_test_real = scaler.inverse_transform(Y_test)

# Graficar Resultados
plt.figure(figsize=(14, 6))

# Subplot Compra
plt.subplot(1, 2, 1)
plt.plot(Y_test_real[:, 0], color='blue', label='Real Compra')
plt.plot(predictions[:, 0], color='red', linestyle='--', label='Predicción Compra')
plt.title('Predicción Tipo de Cambio: COMPRA')
plt.legend()

# Subplot Venta
plt.subplot(1, 2, 2)
plt.plot(Y_test_real[:, 1], color='green', label='Real Venta')
plt.plot(predictions[:, 1], color='orange', linestyle='--', label='Predicción Venta')
plt.title('Predicción Tipo de Cambio: VENTA')
plt.legend()

plt.tight_layout()
plt.show()

# --- PASO 6: PROYECCIÓN FUTURA (Mañana) ---
last_sequence = data_scaled[-LOOK_BACK:] # Últimos días conocidos
last_sequence = last_sequence.reshape(1, LOOK_BACK, 2) # Formato (1, pasos, 2)

next_day_scaled = model.predict(last_sequence)
next_day = scaler.inverse_transform(next_day_scaled)

print("\nResultados del Modelo:")
print(f"Proyección para mañana -> Compra: {next_day[0][0]:.3f} | Venta: {next_day[0][1]:.3f}")



