import streamlit as st
import pydeck as pdk
import pandas as pd
from engine import UrbanDataEngine

st.set_page_config(page_title="Thermos-3D | Consultoría", layout="wide")

engine = UrbanDataEngine()

# --- SIDEBAR ---
st.sidebar.title("Configuración")
city_list = sorted(list(engine.city_coords.keys()))
selected_city = st.sidebar.selectbox("Ciudad Española", city_list)
points = st.sidebar.slider("Densidad de datos", 500, 5000, 2000)

data = engine.generate_thermal_data(selected_city, n_points=points)
m = engine.get_metrics(data)

# --- HEADER ---
st.title(f"🏙️ Análisis de Estrés Térmico: {selected_city}")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Temp. Media", f"{m['avg']:.1f} °C")
c2.metric("Pico Máximo", f"{m['max']:.1f} °C")
c3.metric("Zonas Críticas", m['risk'])
c4.metric("Índice Vegetación", f"{m['veg']:.2f}")

# --- MAPA MEJORADO (HEATMAP) ---
st.subheader("Mapa de Calor de Superficie (LST)")
st.markdown("El mapa muestra la intensidad térmica. Los colores **rojos intensos** indican zonas de asfalto sin refrigeración.")

# Usamos HeatmapLayer: es mucho más visual y profesional para consultoría
view_state = pdk.ViewState(latitude=data['lat'].mean(), longitude=data['lon'].mean(), zoom=12, pitch=0)

layer = pdk.Layer(
    "HeatmapLayer",
    data,
    get_position=['lon', 'lat'],
    get_weight="temperature",
    radius_pixels=60,
    intensity=1,
    threshold=0.05,
    color_range=[
        [255, 255, 178], [254, 217, 118], [254, 178, 76],
        [253, 141, 60], [240, 59, 32], [189, 0, 38]
    ]
)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

# --- NUEVA GRÁFICA DE PARÁMETROS ---
st.divider()
st.subheader("Distribución de Rangos Térmicos")
# Creamos categorías para que el usuario sepa "hasta qué parámetro llega"
bins = [0, 30, 35, 40, 45, 100]
labels = ['Templado (<30)', 'Cálido (30-35)', 'Aviso (35-40)', 'Peligro (40-45)', 'Extremo (>45)']
data['Rango'] = pd.cut(data['temperature'], bins=bins, labels=labels)
dist_data = data['Rango'].value_counts().reindex(labels)

st.bar_chart(dist_data)

# --- FOOTER ---
st.divider()
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0e1117;
        color: #fafafa;
        text-align: center;
        padding: 10px;
        font-family: sans-serif;
    }
    </style>
    <div class="footer">
        <p>Desarrollado por <b>Jose Luis Asenjo</b> | Thermos-3D © 2026</p>
    </div>
    """,
    unsafe_allow_html=True
)
