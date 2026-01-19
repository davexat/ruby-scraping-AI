import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from collections import Counter
import re
import os

# Descargar recursos necesarios de NLTK (solo la primera vez)
nltk.download('stopwords')
nltk.download('punkt')

# 1. Cargar el CSV
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, '../../data/pazmino.csv')
df = pd.read_csv(csv_path)

# Limpieza básica: Eliminar filas vacías si falló el scraping
df.dropna(subset=['Titulo', 'Contenido Completo'], inplace=True)

# Configuración de estilo para los gráficos
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# 2. Análisis de Sentimientos

# Pregunta 1
# Función para obtener polaridad
def analizar_sentimiento(texto):
    if pd.isna(texto): return 0
    return TextBlob(str(texto)).sentiment.polarity

# Aplicar análisis
df['Sentimiento_Titulo'] = df['Titulo'].apply(analizar_sentimiento)
df['Sentimiento_Contenido'] = df['Contenido Completo'].apply(analizar_sentimiento)

# Crear el Gráfico
sns.scatterplot(data=df, x='Sentimiento_Contenido', y='Sentimiento_Titulo', 
                color='crimson', alpha=0.6, s=100)

# Añadir líneas de referencia
plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
plt.axvline(0, color='gray', linestyle='--', linewidth=0.8)

# Línea de identidad (x=y) para ver la concordancia perfecta
plt.plot([-1, 1], [-1, 1], color='blue', linestyle='--', label='Concordancia Perfecta')

plt.title('Discrepancia Emocional: Título vs. Contenido', fontsize=16, fontweight='bold')
plt.xlabel('Sentimiento del Contenido (Cuerpo de la noticia)', fontsize=12)
plt.ylabel('Sentimiento del Título (El Hook)', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig(os.path.join(script_dir, 'question1.png'))
plt.clf()

# Pregunta 2
from nltk.util import ngrams
from nltk.tokenize import word_tokenize

# Descargar recurso necesario de NLTK (solo la primera vez si no se descargó con 'punkt')
nltk.download('punkt_tab')

# Unir todo el texto en una sola cadena gigante
texto_completo = " ".join(df['Contenido Completo'].astype(str).tolist()).lower()

# Limpieza de texto (quitar signos de puntuación básicos)
texto_completo = re.sub(r'[^\w\s]', '', texto_completo)

# Tokenización y Stopwords
tokens = word_tokenize(texto_completo)
stop_words = set(stopwords.words('english'))
# Agregamos palabras comunes que no aportan valor en este contexto
stop_words.update(['said', 'also', 'would', 'one', 'new', 'like', 'time', 'get', 'use'])

tokens_limpios = [word for word in tokens if word not in stop_words and len(word) > 2]

# Generar Bigramas (Pares de palabras)
bigrams = ngrams(tokens_limpios, 2)
bigram_counts = Counter(bigrams)

# Obtener los 15 más comunes
common_bigrams = bigram_counts.most_common(15)
etiquetas = [" ".join(bg[0]) for bg in common_bigrams]
valores = [bg[1] for bg in common_bigrams]

# Crear Gráfico de Barras Horizontal
sns.barplot(x=valores, y=etiquetas, palette='viridis')

plt.subplots_adjust(left=0.17)
plt.title('Tendencias de Adopción: Conceptos más Frecuentes (Bigramas)', fontsize=16, fontweight='bold')
plt.xlabel('Frecuencia de Aparición', fontsize=12)
plt.ylabel('Concepto / Término', fontsize=12)
plt.savefig(os.path.join(script_dir, 'question2.png'))
plt.clf()

# Pregunta 3
# Lista de actores a rastrear
actores = {
    'OpenAI': 0,
    'Google': 0,
    'Microsoft': 0,
    'Apple': 0,
    'Meta': 0,
    'Nvidia': 0,
    'Anthropic': 0,
    'Grok': 0,
    'Amazon': 0
}

# Contamos las menciones en todo el texto
# Iteramos sobre cada noticia
for noticia in df['Contenido Completo'].astype(str):
    noticia_lower = noticia.lower()
    for actor in actores:
        # Sumamos cuántas veces aparece el nombre del actor en esta noticia
        actores[actor] += noticia_lower.count(actor.lower())

# Convertir a DataFrame para graficar
df_actores = pd.DataFrame(list(actores.items()), columns=['Actor', 'Menciones'])
df_actores = df_actores.sort_values(by='Menciones', ascending=False)

# Crear Gráfico de Barras
grafico = sns.barplot(data=df_actores, x='Actor', y='Menciones', palette='magma')

plt.title('Dominio Mediático: Empresas y Actores más Mencionados', fontsize=16, fontweight='bold')
plt.xlabel('Actor / Empresa', fontsize=12)
plt.ylabel('Total de Menciones', fontsize=12)

# Añadir el número exacto encima de cada barra
for p in grafico.patches:
    grafico.annotate(f'{int(p.get_height())}', 
                     (p.get_x() + p.get_width() / 2., p.get_height()), 
                     ha = 'center', va = 'center', 
                     xytext = (0, 9), 
                     textcoords = 'offset points')

plt.savefig(os.path.join(script_dir, 'question3.png'))
plt.clf()