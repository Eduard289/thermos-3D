#  Thermos-3D: Plataforma de Inteligencia Térmica Urbana

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Pydeck](https://img.shields.io/badge/Pydeck-0.8.0-orange.svg)](https://deckgl.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Thermos-3D** es un *dashboard* analítico y geoespacial diseñado para la monitorización de Islas de Calor Urbano (UHI - *Urban Heat Islands*). La herramienta permite a consultores ambientales, urbanistas y administraciones públicas visualizar la distribución térmica, evaluar el riesgo en la salud pública y estimar el impacto energético derivado del calentamiento de las infraestructuras.

##  Tabla de Contenidos
1. [Visión General y Caso de Uso](#-visión-general-y-caso-de-uso)
2. [Arquitectura del Motor de Datos](#-arquitectura-del-motor-de-datos)
3. [Métricas Estratégicas Extraídas](#-métricas-estratégicas-extraídas)
4. [Stack Tecnológico](#-stack-tecnológico)
5. [Instalación y Despliegue](#-instalación-y-despliegue)
6. [Autoría y Licencia](#-autoría-y-licencia)

---

##  Visión General y Caso de Uso

El estrés térmico en entornos urbanos acelera la degradación de materiales, aumenta drásticamente el consumo en sistemas de climatización (HVAC) y supone un riesgo crítico para la salud pública. 

Thermos-3D aborda este problema proporcionando un análisis geoespacial interactivo basado en una simulación calibrada de **Land Surface Temperature (LST)** sobre **52 capitales de provincia de España**. Utilizando renderizado de alto rendimiento de capas base oscuras (CartoDB Dark), la plataforma resalta los "hotspots" críticos donde la infraestructura absorbe y retiene la radiación solar.

---

##  Arquitectura del Motor de Datos

Para este entorno de simulación, la clase central `UrbanDataEngine` genera un conjunto de datos estocásticos espaciales. En lugar de una distribución puramente aleatoria, los puntos de datos se agrupan utilizando distribuciones normales multivariadas, modelando matemáticamente la densidad urbana.

### Modelado Térmico (LST)
La temperatura de superficie se calcula de forma inversamente proporcional a la distancia del centro urbano, aplicando un ruido gaussiano para simular la heterogeneidad de los materiales:

$LST = 48 - (d \cdot 135) + \mathcal{N}(0, 1.8)$

Donde $d$ es la distancia euclidiana desde el epicentro de la ciudad:
$d = \sqrt{(lat - lat_{centro})^2 + (lon - lon_{centro})^2}$

### Cálculo del Albedo
El albedo ($\alpha$) urbano se modela correlacionado negativamente con la temperatura, simulando cómo los pavimentos oscuros (bajo albedo) retienen más calor:

$\alpha = 0.55 - (\frac{LST}{110}) + \mathcal{N}(0, 0.04)$

---

##  Métricas Estratégicas Extraídas

El pipeline de análisis procesa el DataFrame geoespacial en tiempo real para extraer los siguientes KPIs de consultoría:

* **Pico Máximo Detectado:** Límite superior de temperatura superficial registrada en asfalto/cubiertas.
* **Albedo Medio Urbano:** Métrica de reflectividad global. Valores inferiores a **0.20** disparan alertas de absorción térmica extrema.
* **Impacto Energético Estimado:** Un modelo simplificado que proyecta un **+3.5% de sobrecoste en climatización** por cada grado que la temperatura media de la superficie supera los 25°C.
* **Zonas de Riesgo Clínico:** Conteo de sectores censales/puntos de muestreo que superan el umbral crítico de los 40-42°C.

---

##  Stack Tecnológico

El proyecto está diseñado bajo una arquitectura limpia separando la lógica de generación (`engine.py`) de la interfaz de usuario (`app.py`).

* **Backend & Data Processing:** Python 3, `pandas`, `numpy` (operaciones vectorizadas para máxima eficiencia).
* **Visualización Geoespacial:** `pydeck` (Deck.GL wrapper para Python), especializado en el renderizado WebGL de grandes datasets directamente en el navegador.
* **Frontend / UI:** `streamlit` para la reactividad de los componentes de control y despliegue rápido.

---
