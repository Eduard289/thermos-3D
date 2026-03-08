import pandas as pd
import numpy as np

class UrbanDataEngine:
    def __init__(self):
        # (Mantener la lista de ciudades anterior aquí...)
        self.city_coords = {
            "Madrid": [40.4167, -3.7037], "Barcelona": [41.3851, 2.1734],
            "Valencia": [39.4699, -0.3763], "Sevilla": [37.3891, -5.9845],
            "Zaragoza": [41.6488, -0.8891], "Málaga": [36.7212, -4.4214],
            "Murcia": [37.9922, -1.1307], "Palma": [39.5693, 2.6502],
            "Bilbao": [43.2630, -2.9350], "Alicante": [38.3452, -0.4810],
            # ... resto de ciudades
        }

    def generate_thermal_data(self, city, n_points=2000):
        if city not in self.city_coords: return pd.DataFrame()
        center = self.city_coords[city]
        
        lats = np.random.normal(center[0], 0.025, n_points)
        lons = np.random.normal(center[1], 0.025, n_points)
        
        dist = np.sqrt((lats - center[0])**2 + (lons - center[1])**2)
        temp = 48 - (dist * 120) + np.random.normal(0, 2, n_points)
        temp = np.clip(temp, 22, 52)

        # NUEVO: Albedo (Reflectividad). El asfalto caliente tiene poco albedo (0.1 - 0.2)
        albedo = 0.5 - (temp / 120) + np.random.normal(0, 0.05, n_points)
        albedo = np.clip(albedo, 0.1, 0.4)

        return pd.DataFrame({
            'lat': lats, 
            'lon': lons, 
            'temperature': temp,
            'albedo': albedo
        })

    def get_metrics(self, df):
        avg_temp = df['temperature'].mean()
        # Estimación de sobrecoste en AC: +3% de consumo por cada grado sobre 25°C
        energy_impact = max(0, (avg_temp - 25) * 3.5)
        
        return {
            "avg": avg_temp,
            "max": df['temperature'].max(),
            "albedo_med": df['albedo'].mean(),
            "energy_hike": energy_impact
        }
