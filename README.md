# Scraping and Data Analytics - AI 👻

[![Ruby](https://img.shields.io/badge/Ruby-CC342D?style=for-the-badge&logo=ruby&logoColor=white)](https://www.ruby-lang.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=python&logoColor=white)](https://matplotlib.org/)

Un proyecto de **análisis de datos sencillo** que responde a preguntas concretas mediante **gráficos automáticos** generados a partir de noticias sobre **Inteligencia Artificial** extraídas de fuentes líderes en tecnología.

## 📋 Descripción

Este proyecto combina **web scraping** con **análisis de datos** para obtener insights sobre el panorama actual de la IA. Extrae noticias de fuentes de tecnología reconocidas y genera visualizaciones que responden preguntas específicas sobre:

- 🏢 **Empresas líderes** mencionadas en los titulares
- 📊 **Nivel de especialización** de los artículos (divulgativos, conceptuales o técnicos)
- 🔬 **Categorías de IA** más populares (LLMs, Computer Vision, Robotics, etc.)

## 🛠️ Tecnologías Utilizadas

### Web Scraping (Ruby)
- **Nokogiri** - Parser HTML/XML
- **Open-URI** - Cliente HTTP
- **CSV** - Manejo de archivos CSV

### Análisis de Datos (Python)
- **Pandas** - Manipulación de datos
- **Matplotlib** - Visualizaciones
- **Seaborn** - Gráficos estadísticos avanzados
- **NumPy** - Computación numérica

## 📂 Estructura del Proyecto

```
progamming-languages/
│
├── 📄 scr_sandoval.rb      # Scraper para TechCrunch
├── 📄 scr_pazmino.rb       # Scraper para Ars Technica
├── 📄 scr_romero.rb        # Scraper para Hacker News
│
├── 📁 data/                # Datos extraídos (CSV)
│   ├── sandoval.csv
│   ├── pazmino.csv
│   └── romero.csv
│
├── 📁 visualization/       # Scripts de análisis y visualización
│   ├── bruno/
│   │   └── graphics_bruno.py
│   ├── david/
│   │   └── graphics_david.py
│   └── jaren/
│       └── graphics_jaren.py    
│
├── 📄 Gemfile              # Dependencias Ruby
├── 📄 requirements.txt     # Dependencias Python
└── 📄 README.md
```

## 🚀 Instalación y Uso

### 1️⃣ Configuración del entorno Ruby

```bash
# Instalar dependencias
bundle install
```

### 2️⃣ Configuración del entorno Python

```bash
# Crear entorno virtual (opcional pero recomendado)
python -m venv env

# Activar el entorno virtual
# En Windows:
.\env\Scripts\activate
# En macOS/Linux:
source env/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3️⃣ Ejecutar los scrapers

Cada scraper extrae datos de una fuente diferente:

```bash
# TechCrunch - Noticias de IA
ruby scr_sandoval.rb

# Ars Technica - Artículos técnicos
ruby scr_pazmino.rb

# Hacker News - Tendencias tech
ruby scr_romero.rb
```

Los datos se guardarán automáticamente en la carpeta `/data/`.

### 4️⃣ Generar visualizaciones

```bash
cd visualization/david
python graphics_david.py
```

Los gráficos se generarán como imágenes PNG en el directorio correspondiente.

## 📊 Preguntas que Responde el Análisis

### 🔍 Pregunta 1: ¿Qué empresas líderes se mencionan más?
Identifica las empresas tecnológicas más mencionadas en los titulares (OpenAI, Google, Meta, Microsoft, etc.) y calcula el porcentaje de aparición.

![Gráfico tipo barras horizontales mostrando % de titulares por empresa]

### 📚 Pregunta 2: ¿Cuál es el nivel de especialización de las noticias?
Clasifica las noticias en tres niveles según la complejidad de los términos técnicos utilizados:
- **Divulgativos**: Lenguaje general, accesible
- **Conceptuales**: Términos intermedios (AGI, Foundation Models)
- **Técnicos**: Jerga especializada (LoRA, RLHF, Vector DB)

![Gráfico de barras mostrando distribución por nivel de especialización]

### 🤖 Pregunta 3: ¿Qué categorías de IA son más populares?
Analiza los temas principales en el contenido completo de las noticias:
- Generative AI & LLMs
- Computer Vision
- AI Ethics & Governance
- Robotics & Automation
- Autonomous Vehicles
- Business & Enterprise AI

![Gráfico de barras mostrando frecuencia de categorías de IA]

## 🎯 Metodología

1. **Extracción**: Los scripts Ruby utilizan Nokogiri para parsear HTML y extraer:
   - Títulos de artículos
   - URLs
   - Contenido completo

2. **Almacenamiento**: Los datos se guardan en formato CSV con encoding UTF-8

3. **Análisis**: Python procesa los CSVs mediante:
   - Búsqueda de patrones con expresiones regulares
   - Conteo de frecuencias
   - Clasificación por niveles cognitivos

4. **Visualización**: Se generan gráficos con Matplotlib/Seaborn usando:
   - Paleta de colores personalizada
   - Tema `whitegrid` de Seaborn
   - Dimensiones óptimas para legibilidad

## 🔧 Características Técnicas

- ✅ **Headers personalizados** para evitar bloqueos por User-Agent
- ✅ **Delays entre requests** para respetar políticas de scraping
- ✅ **Manejo de errores** HTTP (404, 403, timeouts)
- ✅ **Clasificación multinivel** basada en diccionarios de términos
- ✅ **Búsqueda case-insensitive** para máxima precisión
- ✅ **Rutas dinámicas** con `os.path` para portabilidad

## 📈 Resultados Ejemplo

El análisis procesa **cientos de artículos** y genera métricas como:

```
Total de noticias analizadas: 247
Empresas líderes identificadas: 12
Ratio técnico/divulgativo: 2.34
Categoría dominante: Generative AI & LLMs (67%)
```

## 🤝 Contribuciones

Este proyecto fue desarrollado como parte de un análisis académico sobre tendencias en Inteligencia Artificial. Las contribuciones son bienvenidas mediante:

1. Fork del repositorio
2. Creación de una rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Apertura de un Pull Request

## 📝 Notas

- Los scrapers están diseñados para **uso educativo** y respetan las políticas de robots.txt
- Se recomienda usar delays apropiados entre requests
- Los datos extraídos son para **análisis estadístico**, no redistribución

## 📜 Licencia

Este proyecto está bajo una licencia educativa. El uso comercial no está permitido sin autorización.

---

**Desarrollado con ❤️ para el análisis de tendencias en IA** 🚀👻
