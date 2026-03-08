import pandas as pd
import numpy as np

class UrbanDataEngine:
    def __init__(self):
        # Lista ampliada de ciudades españolas (Capitales y grandes ciudades)
        self.city_coords = {
            "Madrid": [40.4167, -3.7037], "Barcelona": [41.3851, 2.1734],
            "Valencia": [39.4699, -0.3763], "Sevilla": [37.3891, -5.9845],
            "Zaragoza": [41.6488, -0.8891], "Málaga": [36.7212, -4.4214],
            "Murcia": [37.9922, -1.1307], "Palma": [39.5693, 2.6502],
            "Bilbao": [43.2630, -2.9350], "Alicante": [38.3452, -0.4810],
            "Córdoba": [37.8882, -4.7794], "Valladolid": [41.6522, -4.7245],
            "Vigo": [42.2406, -8.7207], "Gijón": [43.5322, -5.6611],
            "A Coruña": [43.3623, -8.4115], "Granada": [37.1773, -3.5986],
            "Vitoria": [42.8467, -2.6716], "Santa Cruz de Tenerife": [28.4636, -16.2518],
            "Las Palmas": [28.1235, -15.4363], "Oviedo": [43.3603, -5.8448],
            "Pamplona": [42.8125, -1.6458], "Almería": [36.8340, -2.4637],
            "San Sebastián": [43.3209, -1.9840], "Burgos": [42.3439, -3.6969],
            "Santander": [43.4623, -3.8099], "Castellón": [39.9864, -0.0513],
            "Logroño": [42.4627, -2.4450], "Badajoz": [38.8794, -6.9706],
            "Salamanca": [40.9701, -5.6635], "Huelva": [37.2614, -6.9447],
            "Lleida": [41.6176, 0.6200], "Tarragona": [41.1189, 1.2445],
            "León": [42.5987, -5.5670], "Cádiz": [36.5271, -6.2886],
            "Jaén": [37.7796, -3.7849], "Ourense": [42.3358, -7.8639],
            "Girona": [41.9794, 2.8214], "Lugo": [43.0121, -7.5581],
            "Cáceres": [39.4753, -6.3722], "Guadalajara": [40.6327, -3.1648],
            "Toledo": [39.8628, -4.0273], "Pontevedra": [42.4336, -8.6475],
            "Palencia": [42.0095, -4.5284], "Ciudad Real": [38.9848, -3.9274],
            "Zamora": [41.5032, -5.7445], "Ávila": [40.6567, -4.7002],
            "Cuenca": [40.0704, -2.1374], "Huesca": [42.1362, -0.4085],
            "Segovia": [40.9429, -4.1088], "Soria": [41.7640, -2.4688],
            "Teruel": [40.3457, -1.1065]
        }

    def generate_thermal_data(self, city, n_points=2000):
        if city not in self.city_coords: return pd.DataFrame()
        center = self.city_coords[city]
        
        # Generar puntos más dispersos para que cubran la ciudad
        lats = np.random.normal(center[0], 0.025, n_points)
        lons = np.random.normal(center[1], 0.025, n_points)
        
        # Lógica térmica mejorada
        dist = np.sqrt((lats - center[0])**2 + (lons - center[1])**2)
        temp = 48 - (dist * 120) + np.random.normal(0, 2, n_points)
        temp = np.clip(temp, 22, 52) # Rango realista de verano

        return pd.DataFrame({'lat': lats, 'lon': lons, 'temperature': temp})

    def get_metrics(self, df):
        return {
            "avg": df['temperature'].mean(),
            "max": df['temperature'].max(),
            "risk": len(df[df['temperature'] > 42]),
            "veg": 0.5 - (df['temperature'].mean() / 100)
        }
