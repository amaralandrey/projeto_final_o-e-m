import re
import pandas as pd
import spacy

# Carrega o modelo de processamento de linguagem
nlp = spacy.load("pt_core_news_sm")

def analisar_texto_livre(series):
    """
    Usa spaCy para encontrar entidades em texto não estruturado.
    Analisa uma amostra para otimizar performance.
    """
    amostra = series.dropna().astype(str).sample(n=min(50, len(series)), random_state=42)

    entidades_encontradas = {"PER": 0, "LOC": 0} # PER = Pessoas, LOC = Localizações

    for texto in amostra:
        doc = nlp(texto)
        for ent in doc.ents:
            if ent.label_ == "PER": entidades_encontradas["PER"] += 1
            if ent.label_ == "LOC": entidades_encontradas["LOC"] += 1

    # Se uma proporção significativa da amostra contiver entidades
    if entidades_encontradas["PER"] > 5: return "Nome"
    if entidades_encontradas["LOC"] > 5: return "Endereço"

    return None

RISCO_MAPEAMENTO = {
    "CPF": "Médio",
    "E-mail": "Médio",
    "Telefone": "Médio",
    "Nome": "Baixo",
    "Endereço": "Alto"
}

def verificar_heuristica_coluna(nome_coluna):
    """
    Inspeciona o metadado (nome da coluna) para identificar 
    dados que não possuem padrões matemáticos rigorosos.
    """
    # Normaliza o texto removendo acentos e deixando em minúsculo
    nome_normalizado = str(nome_coluna).lower().strip()
    
    palavras_chave_nome = ['nome', 'razao social', 'cliente', 'titular', 'favorecido', 'contato']
    palavras_chave_endereco = ['endereco', 'rua', 'logradouro', 'cep', 'bairro', 'cidade', 'estado', 'uf']
    
    # Busca por correspondência de palavras-chave
    if any(palavra in nome_normalizado for palavra in palavras_chave_nome):
        return "Nome"
    
    if any(palavra in nome_normalizado for palavra in palavras_chave_endereco):
        return "Endereço"
        
    return None

def extrair_padroes_coluna(series):
    """
    Analisa os valores de uma coluna por amostragem aleatória 
    para identificar padrões de Regex (CPF, Email ou Telefone).
    """
    valores = series.dropna().astype(str).str.strip()
    
    if valores.empty:
        return None

    # Amostragem Aleatória: Coleta até 200 linhas para garantir robustez
    tamanho_maximo = min(200, len(valores))
    amostra = valores.sample(n=tamanho_maximo, random_state=42)
    
    regex_cpf = r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$'
    regex_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    regex_telefone = r'^\(?[1-9]{2}\)? ?(?:[2-8]|9[1-9])\d{3}-?\d{4}$'

    cpfs_encontrados = sum(1 for v in amostra if re.match(regex_cpf, v))
    emails_encontrados = sum(1 for v in amostra if re.match(regex_email, v))
    telefones_encontrados = sum(1 for v in amostra if re.match(regex_telefone, v))

    # Mantém o limiar de 70% de correspondência sobre a amostra aleatória
    if cpfs_encontrados / tamanho_maximo > 0.7:
        return "CPF"
    elif emails_encontrados / tamanho_maximo > 0.7:
        return "E-mail"
    elif telefones_encontrados / tamanho_maximo > 0.7:
        return "Telefone"
        
    return None

def analisar_dataframe(df):
    inventario = []

    for coluna in df.columns:
        tipo_dado = None

        # 1. Regex (Dados Estruturados)
        tipo_dado = extrair_padroes_coluna(df[coluna])

        # 2. Heurística (Títulos das colunas)
        if not tipo_dado:
            tipo_dado = verificar_heuristica_coluna(coluna)

        # 3. NLP/spaCy (Dados Não Estruturados - O Pulo do Gato)
        if not tipo_dado:
            tipo_dado = analisar_texto_livre(df[coluna])

        if tipo_dado:
            inventario.append({
                "Coluna": coluna,
                "Tipo de Dado Pessoal": tipo_dado,
                "Nível de Risco": RISCO_MAPEAMENTO.get(tipo_dado, "Indefinido")
            })

    return pd.DataFrame(inventario)
