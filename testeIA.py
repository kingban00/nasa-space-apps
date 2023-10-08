import netCDF4 as nc
import pandas as pd
from datetime import datetime, timedelta

# Abra o arquivo .nc
arquivo = nc.Dataset('SPURS_WHOI_1_D_M1H.nc')  # Substitua 'seuarquivo.nc' pelo nome do seu arquivo .nc

# Extraia as variáveis de interesse
time = arquivo.variables['TIME'][:]
latitude = arquivo.variables['LATITUDE'][0]  # Como 'LATITUDE' tem shape (1,), pegamos o primeiro elemento
longitude = arquivo.variables['LONGITUDE'][0]  # Como 'LONGITUDE' tem shape (1,), pegamos o primeiro elemento
air_temperature = arquivo.variables['AIRT'][:]
shortwave_radiation = arquivo.variables['SW'][:]

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

print(dados.head())

arquivo.close()