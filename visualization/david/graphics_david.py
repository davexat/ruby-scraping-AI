import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, '../../data/sandoval.csv')
df = pd.read_csv(csv_path)

df['f_title'] = df['Title'].str.lower()
df['f_content'] = df['Content'].str.lower()

# PREGUNTA 1: 
# ¿Qué porcentaje de titulares en la sección de IA mencionan empresas líderes (OpenAI, Google, Meta, Anthropic) para identificar el dominio del mercado?

# Para contestar esta pregunta, se considerará una sola categoría unificada de empresas líderes.
# Es decir, no se considerará si su dominio son modelos, infraestructura, etc.

target_companies = [
    ['OpenAI'],
    ['Google', 'Alphabet'],
    ['Anthropic'],
    ['Meta', 'Facebook', 'Instagram', 'WhatsApp'],
    ['Microsoft', 'MSFT', 'Azure'],
    ['xAI', 'Elon Musk', 'Grok'],
    ['Amazon', 'AWS'],
    ['Oracle'],
    ['NVIDIA', 'Nvidia'],
    ['AMD', 'Advanced Micro Devices'],
    ['Intel', 'Intel Corp'],
    ['TSMC', 'Taiwan Semiconductor'],
    ['Hugging Face'],
    ['Stability AI'],
    ['Mistral AI', 'Mistral'],
    ['Cohere'],
    ['Apple'],
    ['Tesla'],
    ['Perplexity', 'Perplexity AI'],
    ['IBM', 'IBM WatsonX'],
    ['Salesforce', 'Slack', 'Einstein GPT'],
    ['Adobe', 'Adobe Firefly'],
    ['Snowflake'],
    ['Palantir'],
    ['Databricks'],
    ['Baidu', 'Ernie Bot'],
    ['Alibaba', 'Qwen'],
    ['Tencent'],
    ['Samsung'],
    ['ASML'],
    ['Broadcom'],
    ['Qualcomm'],
    ['Groq'],
    ['Scale AI'],
    ['DeepL']
]

companies_count = {companies[0]: 0 for companies in target_companies}

for title in df['f_title']:
    for companies in target_companies:
        if any(company.lower() in title for company in companies):
            companies_count[companies[0]] += 1

total_news = len(df)

percentages = {
    company: round((count/total_news)*100, 2) for company, count in companies_count.items() if count > 0
}

ordered_percentages = sorted(percentages.items(), key=lambda x: x[1], reverse=True)

df_1 = pd.DataFrame(ordered_percentages, columns=['Company', 'Percentage'])

sns.barplot(x='Percentage', y='Company', hue='Company', data=df_1)
plt.title('% de Titulares que mencionan empresas líderes')
plt.xlabel('% de Titulares')
plt.ylabel('Empresa')
plt.savefig(os.path.join(script_dir, 'question1.png'))
plt.show()

# PREGUNTA 2
# ¿Cuál es la frecuencia de términos técnicos específicos (LLM, RAG, Agents, GPU y otros) en el texto completo de las noticias para medir el nivel de tecnificación del lenguaje?

# Para contestar esta pregunta, se buscarán los términos técnicos específicos en el texto completo de las noticias y se contarán las apariciones individuales de cada uno, similar al método utilizado en la pregunta 1.
# Luego, se utilizará un diccionario de nivel cognitivo para clasificar la noticia en función de la complejidad del lenguaje utilizado.

target_terms = {
    "LLM": [
        "llm",
        "large language model",
        "slm",
        "small language model"
    ],
    "RAG": [
        "rag",
        "retrieval-augmented generation",
        "graphrag"
    ],
    "AI Agent": [
        "ai agent",
        "autonomous agent",
        "agentic workflow",
        "agentic ai",
        "multi-agent system"
    ],
    "Hardware Acceleration": [
        "gpu",
        "tpu",
        "npu",
        "lpu",
        "tensor processing unit",
        "neural processing unit",
        "h100",
        "a100",
        "blackwell",
        "gb200",
        "cuda",
        "tensor core"
    ],
    "Compute": [
        "compute cluster",
        "high performance computing",
        "hpc",
        "flops",
        "petaflops",
        "exaflops"
    ],
    "Transformer Architecture": [
        "transformer architecture",
        "transformer model",
        "attention mechanism",
        "self-attention",
        "multi-head attention",
        "flashattention"
    ],
    "MoE": [
        "moe",
        "mixture of expert",
        "sparse moe",
        "active parameter"
    ],
    "Reinforcement Learning": [
        "rlhf",
        "reinforcement learning from human feedback",
        "rlaif",
        "reward model",
        "ppo",
        "dpo"
    ],
    "Fine-Tuning": [
        "sft",
        "supervised fine-tuning",
        "peft",
        "parameter-efficient fine-tuning",
        "instruction tuning",
        "full fine-tuning"
    ],
    "LoRA": [
        "lora",
        "low-rank adaptation",
        "qlora",
        "dora"
    ],
    "Quantization": [
        "quantization",
        "quantized",
        "weight quantization",
        "fp8",
        "fp16",
        "int8",
        "4-bit"
    ],
    "Prompt Engineering Techniques": [
        "cot",
        "chain of thought",
        "chain-of-thought",
        "in-context learning",
        "few-shot learning",
        "zero-shot learning"
    ],
    "Generative Methods": [
        "diffusion model",
        "latent diffusion",
        "ldm",
        "autoregressive",
        "gan",
        "generative adversarial network"
    ],
    "Model Behavior Issues": [
        "ai hallucination",
        "model hallucination",
        "catastrophic forgetting",
        "model collapse",
        "mode collapse"
    ],
    "Alignment": [
        "ai alignment",
        "superalignment",
        "constitutional ai",
        "automated interpretability",
        "mechanistic interpretability"
    ],
    "Multimodality": [
        "multimodal",
        "multimodality",
        "lmm",
        "large multimodal model",
        "vlm",
        "vision language model"
    ],
    "Vector Technology": [
        "vector database",
        "vector db",
        "vector search",
        "dense retrieval",
        "semantic search"
    ],
    "Inference": [
        "inference time",
        "inference cost",
        "inference speed",
        "model inference",
        "real-time inference"
    ],
    "Performance Metrics": [
        "tokens per second",
        "tps",
        "time to first token",
        "ttft",
        "latency",
        "throughput"
    ],
    "Training Process": [
        "pre-training",
        "pretraining",
        "backpropagation",
        "gradient descent",
        "checkpointing",
        "loss function"
    ],
    "Foundation Models": [
        "foundation model",
        "frontier model",
        "open weight",
        "state-of-the-art model",
        "sota model"
    ],
    "Model Components": [
        "embedding",
        "hyperparameter",
        "model weight",
        "parameter count",
        "context window",
        "context length",
        "kv cache",
        "logits"
    ],
    "AGI Concepts": [
        "artificial general intelligence",
        "agi",
        "artificial superintelligence",
        "asi",
        "technological singularity"
    ]
}

terms_count = {term: 0 for term in target_terms.keys()}

cognitive_levels = {
    1: [
        "AGI Concepts",
        "Alignment",
        "Model Behavior Issues",
        "Foundation Models",
        "Generative Methods",
        "Multimodality",
        "AI Agent"
    ],
    2: [
        "LLM",
        "RAG",
        "Transformer Architecture",
        "MoE",
        "Reinforcement Learning",
        "Prompt Engineering Techniques",
        "Vector Technology",
        "Model Components"
    ],
    3: [
        "Fine-Tuning",
        "LoRA",
        "Quantization",
        "Inference",
        "Training Process",
        "Performance Metrics",
        "Hardware Acceleration",
        "Compute"
    ]
}

for text in df['f_content']:
    for term, labels in target_terms.items():
        if any(label in text for label in labels):
            terms_count[term] += 1

technification_level = {level: 0 for level in cognitive_levels.keys()}

for term, count in terms_count.items():
    for level, terms in cognitive_levels.items():
        if term in terms:
            technification_level[level] += count

technification_ratio = technification_level[3] / (technification_level[1] + technification_level[2])

df_2 = pd.DataFrame(list(technification_level.items()), columns = ['Level', 'Count'])

ax = sns.barplot(data=df_2, x='Level', y='Count', hue='Level')

plt.title('Frecuencia de Términos Técnicos en Titulares', fontsize=14)
plt.ylabel('Número de Noticias', fontsize=12)
plt.xlabel('Nivel de Especialización', fontsize=12)
plt.xticks([0, 1, 2], ["Divulgativos", "Conceptuales", "Técnicos"])
ax.legend().remove()
plt.savefig(os.path.join(script_dir, 'question2.png'))
plt.show()

# PREGUNTA 3
# ¿Qué subcategorías de IA (Generativa, Robótica, Ética) predominan en los registros almacenados?

# Para contestar esta pregunta, se buscarán los términos técnicos específicos en el texto completo de las noticias y se contarán las apariciones individuales de cada uno, similar al método utilizado en la pregunta 1.

target_categories = {
    "Generative AI & LLMs": [
        "generative AI", "Generative Artificial Intelligence", "GenAI", 
        "large language model", "LLM", "LLMs", "chatbot", "chatbots", 
        "text generation", "image generation", "video generation", 
        "ChatGPT", "Claude", "Gemini", "Llama", "foundation model", 
        "transformers", "prompt engineering", "GPT"
    ],
    "Computer Vision": [
        "computer vision", "machine vision", "image recognition", 
        "facial recognition", "face recognition", "object detection", 
        "image classification", "video analysis", "visual perception", 
        "OCR", "optical character recognition"
    ],
    "Machine Learning & Data Science": [
        "machine learning", "deep learning", "neural network", "neural networks", 
        "predictive modeling", "predictive analytics", "algorithm", "algorithms", 
        "training data", "data labeling", "reinforcement learning", 
        "supervised learning", "unsupervised learning", "pattern recognition"
    ],
    "Robotics & Automation": [
        "robotics", "robot", "robots", "autonomous robot", "humanoid", 
        "humanoid robot", "drone", "drones", "automation", "robotic process automation", 
        "RPA", "industrial robot", "cobot", "collaborative robot"
    ],
    "Autonomous Vehicles": [
        "autonomous vehicle", "self-driving car", "driverless car", 
        "autonomous driving", "robotaxi", "automated driving system", 
        "ADAS", "lidar", "autonomous truck", "Waymo", "Tesla FSD", "Cruise"
    ],
    "Ethics, Safety & Regulation": [
        "AI ethics", "ethical AI", "AI safety", "AI alignment", 
        "AI regulation", "AI governance", "AI policy", "bias", "fairness", 
        "hallucination", "deepfake", "deepfakes", "misinformation", 
        "copyright", "intellectual property", "EU AI Act", "responsible AI", 
        "job displacement", "existential risk"
    ],
    "Hardware & Infrastructure": [
        "GPU", "GPUs", "AI chip", "AI chips", "accelerator", 
        "TPU", "NPU", "data center", "supercomputer", "computing power", 
        "compute", "NVIDIA", "AMD", "Intel", "semiconductor"
    ],
    "Healthcare & Biotech": [
        "AI in healthcare", "medical AI", "drug discovery", "precision medicine", 
        "medical imaging", "diagnosis", "genomics", "protein folding", 
        "AlphaFold", "clinical trial"
    ],
    "Enterprise & Business Applications": [
        "AI adoption", "enterprise AI", "business intelligence", 
        "customer service AI", "virtual assistant", "productivity tool", 
        "fintech", "algorithmic trading", "fraud detection", "marketing automation"
    ]
}

categories_count = {category: 0 for category in target_categories.keys()}

for text in df['f_content']:
    for category, labels in target_categories.items():
        if any(label.lower() in text for label in labels):
            categories_count[category] += 1

percentages_2 = {
    category: round((count/total_news)*100, 2) for category, count in categories_count.items() if count > 0
}

ordered_percentages_2 = sorted(percentages_2.items(), key=lambda x: x[1], reverse=True)

df_3 = pd.DataFrame(ordered_percentages_2, columns=['Category', 'Percentage'])

sns.barplot(x='Percentage', y='Category', hue='Category', data=df_3)
plt.subplots_adjust(left=0.22)
plt.title('Categorías de Noticias')
plt.xlabel('% de Noticias')
plt.ylabel('Categoría')
plt.yticks(['Generative AI & LLMs', 'Computer Vision', 'Machine Learning & Data Science', 'Robotics & Automation', 'Autonomous Vehicles', 'Ethics, Safety & Regulation', 'Hardware & Infrastructure', 'Healthcare & Biotech', 'Enterprise & Business Applications'], ['IA Generativa', 'Visión por Computadora', 'ML & Datos', 'Robótica', 'Vehículos Autónomos', 'Ética y Regulación', 'Hardware', 'Salud & Biotecnología', 'IA Empresarial'])
plt.savefig(os.path.join(script_dir, 'question3.png'))
plt.show()