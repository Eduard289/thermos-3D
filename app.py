import streamlit as st
import pydeck as pdk
import pandas as pd
from engine import UrbanDataEngine

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Thermos-3D | Jose Luis Asenjo",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar motor de datos
@st.cache_resource
def load_engine():
    return UrbanDataEngine()

engine = load_engine()

# 2. SIDEBAR - CONTROLES
st.sidebar.image("https://img.icons8.com/fluency/96/city.png", width=80)
st.sidebar.title("Configuración de Análisis")
st.sidebar.markdown("Ajuste los parámetros para la simulación térmica urbana.")

city_list = sorted(list(engine.city_coords.keys()))
selected_city = st.sidebar.selectbox("Seleccione una Ciudad Española", city_list)

points = st.sidebar.select_slider(
    "Densidad de Muestreo Satelital",
    options=[500, 1000, 2500, 5000],
    value=2500
)

st.sidebar.divider()
st.sidebar.info("Este dashboard utiliza datos sintéticos calibrados para demostrar capacidades de consultoría en resiliencia urbana.")

# 3. PROCESAMIENTO DE DATOS
data = engine.generate_thermal_data(selected_city, n_points=points)
m = engine.get_metrics(data)

# 4. HEADER Y KPIs
st.title(f"🏙️ Thermos-3D: Resiliencia Térmica en {selected_city}")
st.markdown("### Dashboard de Consultoría de Impacto Ambiental")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Temp. Media Superficie", f"{m['avg']:.1f} °C")
col2.metric("Pico Máximo Detectado", f"{m['max']:.1f} °C", delta="Zona Crítica", delta_color="inverse")
col3.metric("Albedo Medio Urbano", f"{m['albedo_med']:.2f}", help="Reflectividad: Valores < 0.20 indican alta absorción de calor.")
col4.metric("Impacto Energético", f"+{m['energy_hike']:.1f}%", help="Aumento estimado en la demanda de climatización respecto a zona rural.")

# 5. VISUALIZACIÓN GEOESPACIAL (MAPA DE CALOR)
st.subheader("Análisis Espacial de Islas de Calor (UHI)")
st.markdown("La intensidad del color representa la acumulación térmica en infraestructuras y superficies pavimentadas.")

view_state = pdk.ViewState(
    latitude=data['lat'].mean(),
    longitude=data['lon'].mean(),
    zoom=12,
    pitch=0
)

layer = pdk.Layer(
    "HeatmapLayer",
    data,
    get_position=['lon', 'lat'],
    get_weight="temperature",
    radius_pixels=50,
    intensity=0.9,
    threshold=0.1,
    color_range=[
        [255, 255, 178], # Amarillo claro
        [254, 178, 76],  # Naranja
        [240, 59, 32],   # Rojo
        [189, 0, 38]     # Granate (Calor extremo)
    ]
)

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v10',
    initial_view_state=view_state,
    layers=[layer]
))

# 6. BLOQUE TÉCNICO Y EXPLICATIVO
st.divider()
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📚 Glosario de Parámetros Analizados")
    st.markdown("""
    * **LST (Land Surface Temperature):** Temperatura real de los materiales (asfalto, tejados). Es la variable clave para identificar la retención térmica de una ciudad.
    * **Albedo Urbano:** Mide la fracción de radiación solar que una superficie refleja. Materiales oscuros tienen albedo bajo y contribuyen activamente al calentamiento.
    * **Estrés Térmico:** Factor derivado de la persistencia de temperaturas altas en zonas con escasa ventilación o vegetación.
    """)

with col_right:
    st.subheader("⚠️ Riesgos de la Falta de Monitorización")
    st.warning("""
    1. **Salud Pública:** Incremento en la mortalidad y morbilidad por eventos de calor extremo no mitigados.
    2. **Ineficiencia Energética:** Sobrecostes masivos en refrigeración debido al efecto de 'noche tropical' en edificios.
    3. **Deterioro de Materiales:** Envejecimiento prematuro de pavimentos y redes eléctricas por fatiga térmica.
    4. **Inseguridad Hídrica:** Aumento de la evaporación en depósitos urbanos y mayor demanda de riego.
    """)

# 7. GRÁFICA DE DISTRIBUCIÓN
st.subheader("Distribución de Riesgo por Rangos Térmicos")
bins = [0, 35, 40, 45, 100]
labels = ['Seguro (<35°C)', 'Aviso (35-40°C)', 'Peligro (40-45°C)', 'Extremo (>45°C)']
data['Rango'] = pd.cut(data['temperature'], bins=bins, labels=labels)
st.bar_chart(data['Rango'].value_counts().reindex(labels))

# 8. FOOTER (Fondo blanco, letra negra)
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
        padding: 8px;
        font-size: 14px;
        border-top: 1px solid #dcdcdc;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        z-index: 1000;
    }
    /* Espaciado para que el footer no tape el contenido */
    .main .block-container {
        padding-bottom: 50px;
    }
    </style>
    <div class="footer">
        Desarrollado por <b>Jose Luis Asenjo</b> | Thermos-3D © 2026
    </div>
    """,
    unsafe_allow_html=True
)
