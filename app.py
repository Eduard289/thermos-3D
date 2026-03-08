import streamlit as st
import pydeck as pdk
import pandas as pd
from engine import UrbanDataEngine

st.set_page_config(page_title="Thermos-3D | Jose Luis Asenjo", layout="wide")

engine = UrbanDataEngine()

# --- SIDEBAR ---
st.sidebar.title("Configuración")
city_list = sorted(list(engine.city_coords.keys()))
selected_city = st.sidebar.selectbox("Ciudad Española", city_list)
points = st.sidebar.slider("Densidad de datos", 500, 5000, 2500)

data = engine.generate_thermal_data(selected_city, n_points=points)
m = engine.get_metrics(data)

# --- HEADER ---
st.title(f"🏙️ Thermos-3D: Resiliencia en {selected_city}")
st.markdown("### Dashboard de Consultoría Estratégica")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Temperatura Media", f"{m['avg']:.1f} °C")
c2.metric("Pico de Superficie", f"{m['max']:.1f} °C", delta="Crítico", delta_color="inverse")
c3.metric("Albedo Medio", f"{m['albedo_med']:.2f}", help="Reflectividad de la superficie. Menos de 0.20 indica absorción crítica de calor.")
c4.metric("Impacto Energético", f"+{m['energy_hike']:.1f}%", help="Aumento estimado en demanda de climatización.")

# --- MAPA ---
st.subheader("Análisis Geoespacial de Calor (LST)")
view_state = pdk.ViewState(latitude=data['lat'].mean(), longitude=data['lon'].mean(), zoom=12, pitch=0)
layer = pdk.Layer(
    "HeatmapLayer", data, get_position=['lon', 'lat'], get_weight="temperature",
    radius_pixels=50, intensity=0.9, threshold=0.1,
    color_range=[[255,255,178], [254,178,76], [240,59,32], [189,0,38]]
)
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

# --- BLOQUE TÉCNICO DE CONSULTORÍA ---
st.divider()
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("📚 Glosario de Parámetros")
    st.markdown("""
    * **LST (Land Surface Temperature):** Temperatura real de los materiales (asfalto, tejados). Suele ser 10-15°C superior a la temperatura del aire.
    * **Albedo Urbano:** Mide cuánto calor refleja el suelo. Un albedo bajo (asfalto negro) convierte la ciudad en un horno.
    * **Estrés Térmico:** Intersección entre calor extremo y falta de zonas verdes (NDVI).
    """)

with col_b:
    st.subheader("⚠️ Consecuencias de la No-Monitorización")
    st.warning("""
    1. **Salud Pública:** Aumento drástico de ingresos hospitalarios por golpes de calor en 'zonas rojas'.
    2. **Costes Operativos:** Incremento masivo del gasto en aire acondicionado en edificios públicos y privados.
    3. **Degradación de Infraestructura:** El calor extremo acelera el agrietamiento del pavimento y fatiga de materiales.
    4. **Efecto Huida:** Desvalorización inmobiliaria de barrios con bajo índice de resiliencia térmica.
    """)

# --- GRÁFICA DE PARÁMETROS ---
st.subheader("Distribución de Riesgo Térmico")
bins = [0, 35, 40, 45, 100]
labels = ['Seguro (<35)', 'Aviso (35-40)', 'Peligro (40-45)', 'Extremo (>45)']
data['Rango'] = pd.cut(data['temperature'], bins=bins, labels=labels)
st.bar_chart(data['Rango'].value_counts().reindex(labels))

# --- FOOTER (NUEVO DISEÑO: Letra negra sobre fondo blanco) ---
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: black;
        text-align: center;
        padding: 5px;
        font-size: 14px;
        border-top: 1px solid #e6e6e6;
        font-weight: 500;
    }
    </style>
    <div class="footer">
        Desarrollado por Jose Luis Asenjo | Thermos-3D © 2026
    </div>
    """,
    unsafe_allow_html=True
)
