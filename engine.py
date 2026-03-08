import pandas as pd
import numpy as np

class UrbanDataEngine:
    """
    Simula el procesamiento de datos satelitales y geoespaciales 
    para el análisis de islas de calor.
    """
    
    def __init__(self):
        # Coordenadas base para ciudades de ejemplo
        self.city_coords = {
            "Madrid": [40.4167, -3.7037],
            "Barcelona": [41.3851, 2.1734],
            "Sevilla": [37.3891, -5.9845],
            "Valencia": [39.4699, -0.3763]
        }

    def generate_thermal_data(self, city, n_points=1500):
        """
        Genera un dataset sintético que imita lecturas de satélite (LST).
        """
        if city not in self.city_coords:
            return pd.DataFrame()

        center = self.city_coords[city]
        
        # Generar puntos aleatorios alrededor del centro de la ciudad
        lats = np.random.normal(center[0], 0.015, n_points)
        lons = np.random.normal(center[1], 0.015, n_points)
        
        # Simular temperatura: más alta en el centro (asfalto), más baja en periferia
        dist_from_center = np.sqrt((lats - center[0])**2 + (lons - center[1])**2)
        temp = 45 - (dist_from_center * 150) + np.random.normal(0, 2, n_points)
        
        # Simular NDVI (Índice de vegetación): Inverso a la temperatura
        ndvi = 1 - (temp / 50) + np.random.normal(0, 0.1, n_points)
        ndvi = np.clip(ndvi, 0, 1)

        df = pd.DataFrame({
            'lat': lats,
            'lon': lons,
            'temperature': temp,
            'ndvi': ndvi,
            'is_hotspot': temp > 40
        })
        
        return df

    def get_consultancy_metrics(self, df):
        """
        Calcula KPIs clave para el informe de consultoría.
        """
        metrics = {
            "avg_temp": df['temperature'].mean(),
            "max_temp": df['temperature'].max(),
            "hotspot_count": df['is_hotspot'].sum(),
            "vegetation_index": df['ndvi'].mean()
        }
        return metrics
