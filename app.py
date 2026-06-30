import streamlit as st
import pandas as pd
import spacy

st.set_page_config(
    page_title="Scanner", 
    layout="centered"
)

# --- INICIALIZAÇÃO DO NLP ---
@st.cache_resource
def carregar_modelo_nlp():
    """
    Carrega o modelo que já foi pré-instalado pelo requirements.txt
    """
    return spacy.load("pt_core_news_sm")

try:
    nlp = carregar_modelo_nlp()
except Exception as e:
    st.error(f"Erro ao carregar o modelo de NLP: {e}")
    st.stop()

from motor_busca import analisar_dataframe
from gerador_pdf import gerar_pdf_bytes

# --- INTERFACE VISUAL ---
st.title("Scanner de Conformidade")
st.subheader("Inventário Automatizado de Dados")

st.markdown("""
Faça o upload de arquivos estruturados (**CSV** ou **XLSX**) para identificar automaticamente a presença 
de dados pessoais (CPF, E-mail, Telefone, Nome Completo) e gerar o relatório de riscos.
""")

# Componente de Upload de Arquivos
arquivo = st.file_uploader("Selecione o arquivo de dados", type=["csv", "xlsx"])

if arquivo is not None:
    try:
        # 1. Ingestão e Processamento 100% em Memória
        if arquivo.name.endswith('.csv'):
            df = pd.read_csv(arquivo)
        else:
            df = pd.read_excel(arquivo)
            
        st.success(f"Arquivo '{arquivo.name}' carregado com sucesso!")
        
        # 2. Execução do Motor de Busca
        st.write("### Analisando dados...")
        resultados = analisar_dataframe(df)
        
        # 3. Exibição do Diagnóstico e Nível de Risco na Tela
        if resultados:
            st.warning(" Foram encontrados dados pessoais no arquivo!")
            dados_tabela = [{"Coluna no Arquivo": col, "Tipo de Dado Detectado": tipo} for col, tipo in resultados.items()]
            st.table(dados_tabela)
            
            qtd_colunas_expostas = len(resultados)
            if qtd_colunas_expostas >= 3:
                st.error("Nível de Risco Geral: ALTO (Múltiplos identificadores expostos)")
            else:
                st.warning(" Nível de Risco Geral: MÉDIO (Dados pessoais identificados)")
        else:
            # Caso não encontre nada, exibe sucesso na tela
            st.success(" Nenhum dado pessoal evidente (CPF, Email, Telefone, Nome Completo) foi detectado nas amostras.")
            
        # 4. Geração e Download do Relatório em PDF
        st.write("---")
        st.write("### Relatório de Adequação")
        st.markdown("Clique no botão abaixo para descarregar o relatório de riscos em formato PDF.")
        
        pdf_data = gerar_pdf_bytes(resultados, len(df))
        
        st.download_button(
            label="📥 Descarregar Relatório PDF",
            data=bytes(pdf_data),
            file_name=f"Relatorio_Adequacao_{arquivo.name}.pdf",
            mime="application/pdf"
        )
            
        # 5. Pré-visualização dos Dados Originais (Apenas as primeiras 5 linhas)
        st.write("---")
        st.write("#### Pré-visualização dos dados enviados:")
        st.dataframe(df.head(5))
        
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
