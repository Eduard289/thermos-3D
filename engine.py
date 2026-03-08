import pandas as pd
import numpy as np

class UrbanDataEngine:
    """
    Motor de análisis geoespacial para Thermos-3D.
    Simula datos de Temperatura de Superficie (LST) y parámetros de resiliencia urbana.
    """
    
    def __init__(self):
        # Base de datos completa: 52 Capitales de Provincia de España
        self.city_coords = {
            "Álava (Vitoria)": [42.8467, -2.6716], "Albacete": [38.9944, -1.8585], 
            "Alicante": [38.3452, -0.4810], "Almería": [36.8340, -2.4637], 
            "Asturias (Oviedo)": [43.3603, -5.8448], "Ávila": [40.6567, -4.7002], 
            "Badajoz": [38.8794, -6.9706], "Barcelona": [41.3851, 2.1734], 
            "Burgos": [42.3439, -3.6969], "Cáceres": [39.4753, -6.3722], 
            "Cádiz": [36.5271, -6.2886], "Cantabria (Santander)": [43.4623, -3.8099], 
            "Castellón": [39.9864, -0.0513], "Ciudad Real": [38.9848, -3.9274], 
            "Córdoba": [37.8882, -4.7794], "Cuenca": [40.0704, -2.1374], 
            "Girona": [41.9794, 2.8214], "Granada": [37.1773, -3.5986], 
            "Guadalajara": [40.6327, -3.1648], "Guipúzcoa (San Sebastián)": [43.3209, -1.9840], 
            "Huelva": [37.2614, -6.9447], "Huesca": [42.1362, -0.4085], 
            "Islas Baleares (Palma)": [39.5693, 2.6502], "Jaén": [37.7796, -3.7849], 
            "La Coruña": [43.3623, -8.4115], "La Rioja (Logroño)": [42.4627, -2.4450], 
            "Las Palmas de Gran Canaria": [28.1235, -15.4363], "León": [42.5987, -5.5670], 
            "Lleida": [41.6176, 0.6200], "Lugo": [43.0121, -7.5581], 
            "Madrid": [40.4167, -3.7037], "Málaga": [36.7212, -4.4214], 
            "Murcia": [37.9922, -1.1307], "Navarra (Pamplona)": [42.8125, -1.6458], 
            "Ourense": [42.3358, -7.8639], "Palencia": [42.0095, -4.5284], 
            "Pontevedra": [42.4336, -8.6475], "Salamanca": [40.9701, -5.6635], 
            "Santa Cruz de Tenerife": [28.4636, -16.2518], "Segovia": [40.9429, -4.1088], 
            "Sevilla": [37.3891, -5.9845], "Soria": [41.7640, -2.4688], 
            "Tarragona": [41.1189, 1.2445], "Teruel": [40.3457, -1.1065], 
            "Toledo": [39.8628, -4.0273], "Valencia": [39.4699, -0.3763], 
            "Valladolid": [41.6522, -4.7245], "Vizcaya (Bilbao)": [43.2630, -2.9350], 
            "Zamora": [41.5032, -5.7445], "Zaragoza": [41.6488, -0.8891],
            "Ceuta": [35.8894, -5.3198], "Melilla": [35.2923, -2.9381]
        }

    def generate_thermal_data(self, city_name, n_points=2500):
        """
        Genera un dataset sintético basado en la ubicación real de la ciudad.
        """
        if city_name not in self.city_coords:
            return pd.DataFrame()

        center = self.city_coords[city_name]
        
        # Dispersión geográfica (simulando área metropolitana)
        lats = np.random.normal(center[0], 0.028, n_points)
        lons = np.random.normal(center[1], 0.028, n_points)
        
        # Cálculo de temperatura (LST): Más calor en el centro por densidad de asfalto
        dist_from_center = np.sqrt((lats - center[0])**2 + (lons - center[1])**2)
        # Base de 48°C en el centro, bajando según la distancia
        temp = 48 - (dist_from_center * 135) + np.random.normal(0, 1.8, n_points)
        temp = np.clip(temp, 21, 53) # Límites realistas

        # Parámetro Albedo: Capacidad de reflexión (0.1 asfalto oscuro, 0.4 zonas claras/verdes)
        # Inversamente proporcional a la temperatura
        albedo = 0.55 - (temp / 110) + np.random.normal(0, 0.04, n_points)
        albedo = np.clip(albedo, 0.08, 0.45)

        return pd.DataFrame({
            'lat': lats,
            'lon': lons,
            'temperature': temp,
            'albedo': albedo
        })

    def get_metrics(self, df):
        """
        Calcula KPIs estratégicos para el informe de consultoría.
        """
        if df.empty:
            return None

        avg_temp = df['temperature'].mean()
        max_temp = df['temperature'].max()
        
        # Zonas Críticas: Puntos que superan los 42°C de superficie
        risk_zones = len(df[df['temperature'] > 42])
        
        # Albedo Medio de la ciudad
        avg_albedo = df['albedo'].mean()

        # Impacto Energético: Estimación de sobrecoste en refrigeración 
        # (+3.5% de consumo por cada grado por encima de 25°C de media)
        energy_hike = max(0, (avg_temp - 25) * 3.5)

        return {
            "avg": avg_temp,
            "max": max_temp,
            "risk": risk_zones,
            "albedo_med": avg_albedo,
            "energy_hike": energy_hike
        }
