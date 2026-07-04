import re
import pandas as pd

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
    """
    Varre todo o DataFrame cruzando Regex e Heurística.
    Retorna o inventário detalhado com Nível de Risco.
    """
    inventario = []
    
    for coluna in df.columns:
        tipo_dado = None
        
        # 1. Tentativa Primária: Identificação por conteúdo exato (Regex)
        tipo_regex = extrair_padroes_coluna(df[coluna])
        
        if tipo_regex:
            tipo_dado = tipo_regex
        else:
            # 2. Tentativa Secundária: Identificação pelo nome da coluna (Heurística)
            tipo_heuristica = verificar_heuristica_coluna(coluna)
            if tipo_heuristica:
                tipo_dado = tipo_heuristica
        
        # 3. Mapeamento de Risco e Construção do Inventário
        if tipo_dado:
            nivel_risco = RISCO_MAPEAMENTO.get(tipo_dado, "Indefinido")
            inventario.append({
                "Coluna": coluna,
                "Tipo de Dado Pessoal": tipo_dado,
                "Nível de Risco": nivel_risco
            })
            
    return pd.DataFrame(inventario) if inventario else pd.DataFrame()
