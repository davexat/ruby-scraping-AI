import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuración visual
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# 1. Cargar el CSV
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, '../../data/sandoval.csv')
df = pd.read_csv(csv_path)

# Limpieza: Convertir todo a string y minúsculas para facilitar la búsqueda
df['Titulo_Lower'] = df['Title'].astype(str).str.lower()
df['Contenido_Lower'] = df['Content'].astype(str).str.lower()

# Pregunta 1
# Definimos las empresas a rastrear
empresas_target = ['openai', 'google', 'meta', 'anthropic', 'microsoft', 'perplexity', 'xai']

# Diccionario para guardar el conteo
conteo_empresas = {empresa: 0 for empresa in empresas_target}
total_noticias = len(df)

# Contamos apariciones
for titulo in df['Titulo_Lower']:
    for empresa in empresas_target:
        if empresa in titulo:
            conteo_empresas[empresa] += 1

# Convertimos a porcentajes
data_empresas = pd.DataFrame(list(conteo_empresas.items()), columns=['Empresa', 'Conteo'])
data_empresas['Porcentaje'] = (data_empresas['Conteo'] / total_noticias) * 100
data_empresas = data_empresas.sort_values('Porcentaje', ascending=False)

# --- GRÁFICO DE BARRAS (Share of Voice) ---
plt.figure(figsize=(10, 6))
ax = sns.barplot(data=data_empresas, x='Porcentaje', y='Empresa', palette='Blues_d')

plt.title('Dominio del Mercado: % de Titulares que Mencionan a Cada Empresa', fontsize=14)
plt.xlabel('Porcentaje de Aparición (%)', fontsize=12)
plt.ylabel('Empresa', fontsize=12)

# Añadir el valor exacto al final de la barra
for p in ax.patches:
    width = p.get_width()
    plt.text(width + 0.5, p.get_y() + p.get_height()/2, f'{width:.1f}%', va='center')

plt.xlim(0, max(data_empresas['Porcentaje']) + 5) # Dar espacio para el texto
plt.show()

# Pregunta 2
# Términos técnicos a buscar (en minúsculas para coincidir)
terminos_tecnicos = {
    'llm': 'LLM', 
    'rag': 'RAG', 
    'agents': 'Agents/Agentes', 
    'gpu': 'GPU/Chips', 
    'transformer': 'Transformer',
    'parameters': 'Parámetros',
    'training': 'Training'
}

conteo_tech = {label: 0 for label in terminos_tecnicos.values()}

# Buscamos en los títulos
for titulo in df['Titulo_Lower']:
    for term, label in terminos_tecnicos.items():
        # Usamos 'search' con bordes de palabra para evitar falsos positivos 
        # (ej: que no cuente "program" como "rag")
        if f" {term} " in f" {titulo} " or f"{term}," in titulo: 
            conteo_tech[label] += 1

# DataFrame
df_tech = pd.DataFrame(list(conteo_tech.items()), columns=['Término', 'Frecuencia'])
df_tech = df_tech.sort_values('Frecuencia', ascending=False)

# --- GRÁFICO DE BARRAS VERTICAL ---
plt.figure(figsize=(10, 6))
sns.barplot(data=df_tech, x='Término', y='Frecuencia', palette='viridis')

plt.title('Nivel de Especialización: Frecuencia de Términos Técnicos en Titulares', fontsize=14)
plt.ylabel('Número de Noticias', fontsize=12)
plt.xlabel('Término Técnico', fontsize=12)
plt.show()

# Pregunta 3
# Definir palabras clave por categoría
keywords = {
    'Generativa (Texto/Img)': ['generative', 'chatgpt', 'image', 'video', 'midjourney', 'dall-e', 'prompt'],
    'Robótica/Hardware': ['robot', 'humanoid', 'hardware', 'chip', 'nvidia', 'gpu', 'device'],
    'Ética/Legal': ['lawsuit', 'copyright', 'bias', 'safety', 'regulation', 'risk', 'security', 'deepfake'],
    'Negocios/Inversión': ['funding', 'startup', 'valuation', 'acquisition', 'ipo', 'round']
}

# Función para clasificar una noticia
def clasificar_noticia(texto):
    for categoria, palabras in keywords.items():
        for palabra in palabras:
            if palabra in texto:
                return categoria
    return 'Otros/General'

# Combinamos Título y Contenido para mejor contexto
df['Texto_Completo'] = df['Titulo_Lower'] + " " + df['Contenido_Lower']
df['Categoria'] = df['Texto_Completo'].apply(clasificar_noticia)

# Contar categorías
conteo_categorias = df['Categoria'].value_counts()

# --- GRÁFICO DE PASTEL (PIE CHART) ---
plt.figure(figsize=(8, 8))
plt.pie(conteo_categorias, labels=conteo_categorias.index, autopct='%1.1f%%', 
        startangle=140, colors=sns.color_palette('pastel'), explode=[0.05]*len(conteo_categorias))

plt.title('Distribución de Temas: ¿De qué se habla en IA?', fontsize=16)
plt.show()