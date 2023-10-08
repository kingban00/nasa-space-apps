import netCDF4 as nc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime, timedelta

# Carregar o nc_file NetCDF4
nc_file = 'SPURS_WHOI_1_D_M1H.nc'
dataset = nc.Dataset(nc_file)

# Extraia as variáveis de interesse
time = dataset.variables['TIME'][:]
latitude = dataset.variables['LATITUDE'][0]  # Como 'LATITUDE' tem shape (1,), pegamos o primeiro elemento
longitude = dataset.variables['LONGITUDE'][0]  # Como 'LONGITUDE' tem shape (1,), pegamos o primeiro elemento
air_temperature = dataset.variables['AIRT'][:]
shortwave_radiation = dataset.variables['SW'][:]

# Converta o tempo para objetos de data e hora
base_time = datetime(1950, 1, 1)
datas = [base_time + timedelta(days=float(t)) for t in time]

# Certifique-se de que todas as variáveis tenham o mesmo comprimento
min_length = min(len(time), len(air_temperature), len(shortwave_radiation))
time = time[:min_length]
air_temperature = air_temperature[:min_length]
shortwave_radiation = shortwave_radiation[:min_length]
datas = datas[:min_length]

# Crie um DataFrame do Pandas com os dados
dados = pd.DataFrame({
    'Data': datas,
    'Latitude': [latitude] * min_length,
    'Longitude': [longitude] * min_length,
    'Temperatura do Ar (°C)': air_temperature,
    'Radiação de Ondas Curtas (W/m^2)': shortwave_radiation
})

# Separar as variáveis independentes (X) e a variável alvo (y)
X = dados[['Latitude', 'Longitude']]  # Corrija o nome das colunas aqui
y = dados['Temperatura do Ar (°C)']  # Variável alvo (temperatura do ar)

# Dividir os dados em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Criar e treinar um modelo de regressão linear
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# Realizar previsões no conjunto de teste
y_pred = modelo.predict(X_test)

# Avaliar o desempenho do modelo
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Visualização das previsões em relação aos valores reais
plt.scatter(y_test, y_pred)
plt.xlabel("Valores Reais")
plt.ylabel("Previsões")
plt.title("Valores Reais vs. Previsões")
plt.show()

print(f"Erro Quadrático Médio (MSE): {mse}")
print(f"R-quadrado (R²): {r2}")