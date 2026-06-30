import re
import pandas as pd
import spacy
import streamlit as st

# Faz o cache do modelo para carregar rápido no Streamlit Cloud
@st.cache_resource
def carregar_modelo_nlp():
    return spacy.load("pt_core_news_sm")

nlp = carregar_modelo_nlp()

def extrair_padroes_coluna(series):
    valores = series.dropna().astype(str).str.strip()
    
    if valores.empty:
        return None

    # Regex para os outros padrões
    regex_cpf = r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$'
    regex_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    regex_telefone = r'^\(?[1-9]{2}\)? ?(?:[2-8]|9[1-9])\d{3}-?\d{4}$'

    amostra = valores.head(50)
    total_itens = len(amostra)
    
    cpfs_encontrados = sum(1 for v in amostra if re.match(regex_cpf, v))
    emails_encontrados = sum(1 for v in amostra if re.match(regex_email, v))
    telefones_encontrados = sum(1 for v in amostra if re.match(regex_telefone, v))
    
    # Validação com NLP (spaCy) para Nomes Próprios
    nomes_encontrados = 0
    for v in amostra:
        # Ignora textos muito longos ou muito curtos para poupar processamento
        if 5 < len(v) < 60: 
            doc = nlp(v)
            # Verifica se o modelo identificou uma Entidade de Pessoa (PER)
            if any(ent.label_ == "PER" for ent in doc.ents):
                nomes_encontrados += 1

    # Lógica de classificação (70% de acerto)
    if cpfs_encontrados / total_itens > 0.7:
        return "CPF"
    elif emails_encontrados / total_itens > 0.7:
        return "E-mail"
    elif telefones_encontrados / total_itens > 0.7:
        return "Telefone"
    elif nomes_encontrados / total_itens > 0.7:
        return "Nome Completo"
        
    return None

def analisar_dataframe(df):
    """
    Varre todo o DataFrame coluna por coluna e retorna um inventário
    de onde foram encontrados dados pessoais.
    """
    inventario = {}
    
    for coluna in df.columns:
        tipo_dado = extrair_padroes_coluna(df[coluna])
        if tipo_dado:
            inventario[coluna] = tipo_dado
            
    return inventario
