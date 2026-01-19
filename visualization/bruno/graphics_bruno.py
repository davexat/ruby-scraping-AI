import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
archivo = os.path.join(script_dir, '../../data/romero.csv')

print(f"Cargando datos desde: {archivo}")

try:
    df = pd.read_csv(archivo)
except FileNotFoundError:
    print("Error: Archivo no encontrado.")
    exit()

def limpiar_numero(valor):
    if pd.isna(valor): return 0
    texto = str(valor)
    numeros = re.findall(r'\d+', texto)
    if numeros:
        return int(numeros[0])
    return 0

df['Puntos'] = df['Puntos'].apply(limpiar_numero)
df['Comentarios'] = df['Comentarios'].apply(limpiar_numero)

sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# ==============================================================================
# GRÁFICO 1: PIE CHART
# Pregunta: ¿Cuánto domina la IA la conversación?
# ==============================================================================
plt.figure(figsize=(8, 8))
conteo = df['Relevancia'].value_counts()
colores = {'ALTA (IA)': '#ff6b6b', 'General Tech': '#4ecdc4'}

plt.pie(conteo, labels=conteo.index, autopct='%1.1f%%', 
        startangle=140, colors=[colores.get(x, '#999999') for x in conteo.index], textprops={'fontsize': 14, 'weight': 'bold'})

plt.title('Distribución de Noticias: IA vs Tecnología General', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'question1.png'))

# ==============================================================================
# GRÁFICO 2: BARRAS DE IMPACTO PROMEDIO
# Pregunta: ¿La IA genera más engagement (puntos/comentarios) promedio?
# ==============================================================================
plt.figure(figsize=(10, 6))

promedios = df.groupby('Relevancia')[['Puntos', 'Comentarios']].mean().reset_index()

df_melted = promedios.melt(id_vars='Relevancia', var_name='Métrica', value_name='Promedio')

ax = sns.barplot(data=df_melted, x='Relevancia', y='Promedio', hue='Métrica', 
            palette='magma')

plt.title('Comparativa de Impacto Promedio: Aprobación vs. Debate', fontsize=16, fontweight='bold')
plt.ylabel('Cantidad Promedio', fontsize=12)
plt.xlabel('')

ax.legend().remove()

# Agregar valores en las barras
for container in ax.containers:
    tmp_hue = df_melted.loc[df_melted['Métrica']==container.get_label()]
    ax.bar_label(container, labels=tmp_hue['Promedio'])

plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'question2.png'))

# ==============================================================================
# GRÁFICO 3: TOP FUENTES DE IA
# Pregunta: ¿De dónde salen las noticias de IA?
# ==============================================================================
plt.figure(figsize=(10, 6))

df_ia = df[df['Relevancia'] == 'ALTA (IA)'].copy()

top_fuentes = df_ia['Sitio'].value_counts().head(7)

sns.barplot(x=top_fuentes.values, y=top_fuentes.index, hue=top_fuentes.index, palette='magma')

plt.title('Top 7 Fuentes de Noticias sobre IA', fontsize=16, fontweight='bold')
plt.xlabel('Cantidad de Noticias', fontsize=12)
plt.ylabel('Sitio Web', fontsize=12)

plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'question3.png'))