import streamlit as st
import pydeck as pdk
from engine import UrbanDataEngine

# 1. Configuración de la interfaz
st.set_page_config(
    page_title="Urban Resilience Lab | Consultancy Tool",
    page_icon="🏙️",
    layout="wide"
)

# Inicializar el motor de datos
@st.cache_resource
def load_engine():
    return UrbanDataEngine()

engine = load_engine()

# 2. Sidebar - Control de parámetros
st.sidebar.image("https://img.icons8.com/fluency/96/city.png", width=80)
st.sidebar.title("Configuración de Análisis")

selected_city = st.sidebar.selectbox(
    "Seleccione la ciudad para análisis:",
    ["Madrid", "Barcelona", "Sevilla", "Valencia"]
)

temp_threshold = st.sidebar.slider(
    "Umbral de Alerta Térmica (°C)",
    min_value=30,
    max_value=50,
    value=40
)

# 3. Procesamiento de Datos
data = engine.generate_thermal_data(selected_city)
metrics = engine.get_consultancy_metrics(data)

# 4. Cabecera del Dashboard
st.title(f"📊 Informe de Resiliencia: {selected_city}")
st.markdown(f"""
Este panel analiza la **Isla de Calor Urbana (UHI)** en {selected_city}. 
Utiliza datos sintéticos calibrados para demostrar capacidades de análisis geoespacial.
""")

# 5. Visualización de KPIs (Métricas clave)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Temp. Media", f"{metrics['avg_temp']:.1f} °C")
c2.metric("Pico Máximo", f"{metrics['max_temp']:.1f} °C", delta="Crítico", delta_color="inverse")
c3.metric("Zonas de Riesgo", metrics['hotspot_count'], help="Áreas por encima del umbral")
c4.metric("Índice de Vegetación", f"{metrics['vegetation_index']:.2f}", delta="-4%", delta_color="inverse")

# 6. Mapa 3D de Calor (Pydeck)
st.subheader("Visualización Espacial de Riesgo Térmico")

# Definir la capa del mapa
layer = pdk.Layer(
    "HexagonLayer",
    data,
    get_position=['lon', 'lat'],
    radius=120,
    elevation_scale=40,
    elevation_range=[0, 1000],
    pickable=True,
    extruded=True,
    # Color dinámico basado en temperatura (de verde a rojo)
    get_fill_color="[255, (1 - (temperature - 25) / 25) * 255, 0, 160]",
)

# Estado inicial de la cámara
view_state = pdk.ViewState(
    latitude=data['lat'].mean(),
    longitude=data['lon'].mean(),
    zoom=12,
    pitch=45,
)

# Renderizar el mapa
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/dark-v10',
    initial_view_state=view_state,
    layers=[layer],
    tooltip={"text": "Temperatura estimada: {elevationValue}°C"}
))

# 7. Insights de Consultoría
st.divider()
with st.expander("📝 Ver Recomendaciones Estratégicas", expanded=True):
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("### 🟢 Soluciones Basadas en la Naturaleza")
        st.write("""
        - **Micro-parques:** Implementación de zonas verdes en los hotspots detectados.
        - **Techos Verdes:** Incentivos fiscales para edificios comerciales con cobertura vegetal.
        """)
        
    with col_right:
        st.markdown("### 🏗️ Infraestructura y Urbanismo")
        st.write("""
        - **Albedo Urbano:** Uso de materiales reflectantes en pavimentos.
        - **Corredores de Viento:** Restricción de altura en áreas de flujo de aire crítico.
        """)
