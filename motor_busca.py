import re
import pandas as pd
import spacy

nlp = spacy.load("pt_core_news_sm") #[cite: 6]

def analisar_texto_livre(series):
    """
    Usa spaCy para encontrar entidades com lógica percentual para evitar falsos positivos.
    """
    valores_validos = series.dropna().astype(str).str.strip()
    valores_validos = valores_validos[valores_validos != ""]

    if valores_validos.empty:
        return None

    tamanho_amostra = min(50, len(valores_validos))
    amostra = valores_validos.sample(n=tamanho_amostra, random_state=42)

    entidades_encontradas = {"PER": 0, "LOC": 0} #[cite: 6]

    for texto in amostra:
        doc = nlp(texto) #[cite: 6]
        for ent in doc.ents: #[cite: 6]
            if ent.label_ == "PER": entidades_encontradas["PER"] += 1 #[cite: 6]
            if ent.label_ == "LOC": entidades_encontradas["LOC"] += 1 #[cite: 6]
                
    limiar_minimo = tamanho_amostra * 0.40

    if entidades_encontradas["PER"] > entidades_encontradas["LOC"] and entidades_encontradas["PER"] >= limiar_minimo:
        return "Nome"

    if entidades_encontradas["LOC"] > entidades_encontradas["PER"] and entidades_encontradas["LOC"] >= limiar_minimo:
        return "Endereço"

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
    Inspeciona o metadado garantindo correspondência exata de palavras.
    """
    nome_normalizado = str(nome_coluna).lower().strip().replace('_', ' ')

    palavras_chave_nome = ['nome', 'razao social', 'cliente', 'titular', 'favorecido', 'contato'] #[cite: 6]
    palavras_chave_endereco = ['endereco', 'rua', 'logradouro', 'cep', 'bairro', 'cidade', 'estado', 'uf'] #[cite: 6]

    # 3. Usa Regex para garantir que a palavra não é apenas parte de outra palavra (\b)
    if any(re.search(rf'\b{palavra}\b', nome_normalizado) for palavra in palavras_chave_nome):
        return "Nome"

    if any(re.search(rf'\b{palavra}\b', nome_normalizado) for palavra in palavras_chave_endereco):
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

    tamanho_maximo = min(200, len(valores))
    amostra = valores.sample(n=tamanho_maximo, random_state=42)
    
    regex_cpf = r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$'
    regex_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    regex_telefone = r'^\(?[1-9]{2}\)? ?(?:[2-8]|9[1-9])\d{3}-?\d{4}$'

    cpfs_encontrados = sum(1 for v in amostra if re.match(regex_cpf, v))
    emails_encontrados = sum(1 for v in amostra if re.match(regex_email, v))
    telefones_encontrados = sum(1 for v in amostra if re.match(regex_telefone, v))

    if cpfs_encontrados / tamanho_maximo > 0.7:
        return "CPF"
    elif emails_encontrados / tamanho_maximo > 0.7:
        return "E-mail"
    elif telefones_encontrados / tamanho_maximo > 0.7:
        return "Telefone"
        
    return None

def verificar_exclusao_coluna(nome_coluna):
    """
    Bloqueia colunas que claramente se referem a dados corporativos,
    de produtos ou infraestrutura, evitando falsos positivos.
    """
    nome_normalizado = str(nome_coluna).lower().strip().replace('_', ' ')

    palavras_exclusao = [
        'produto', 'deposito', 'depósito', 'filial', 'empresa', 'cnpj',
        'loja', 'departamento', 'estoque', 'equipamento', 'marca',
        'fabricante', 'fornecedor', 'servico', 'serviço', 'cargo',
        'setor', 'maquina', 'veiculo', 'placa', 'patrimonio',
        'categoria', 'tipo', 'classe'
    ]

    if any(re.search(rf'\b{palavra}\b', nome_normalizado) for palavra in palavras_exclusao):
        return True

    return False
    
def analisar_dataframe(df):
    inventario = []

    for coluna in df.columns:
        if verificar_exclusao_coluna(coluna):
            continue

        tipo_dado = None

        tipo_dado = extrair_padroes_coluna(df[coluna])

        if not tipo_dado:
            tipo_dado = verificar_heuristica_coluna(coluna)

        if not tipo_dado:
            tipo_dado = analisar_texto_livre(df[coluna])

        if tipo_dado:
            inventario.append({
                "Coluna": coluna,
                "Tipo de Dado Pessoal": tipo_dado,
                "Nível de Risco": RISCO_MAPEAMENTO.get(tipo_dado, "Indefinido")
            })

    return pd.DataFrame(inventario)
