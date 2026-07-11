import os
import streamlit as st
import pandas as pd
from motor_busca import analisar_dataframe
from gerador_pdf import gerar_pdf_bytes

st.set_page_config(page_title="Scanner de Privacidade", layout="centered")
st.title("Scanner")
st.subheader("Inventário Automatizado de Dados Pessoais")

st.sidebar.title("Configurações")
modo_entrada = st.sidebar.radio(
    "Escolha o modo de operação:",
    ("Upload Padrão", "Modo de Demonstração")
)

df = None
nome_arquivo = ""

if modo_entrada == "Upload Padrão":
    st.markdown("### Upload de Arquivo")
    arquivo = st.file_uploader("Selecione o arquivo de dados", type=["csv", "xlsx"])

    if arquivo is not None:
        try:
            if arquivo.name.endswith('.csv'):
                df = pd.read_csv(arquivo)
            else:
                df = pd.read_excel(arquivo)
            nome_arquivo = arquivo.name
        except Exception as e:
            st.error(f"Erro ao ler o arquivo enviado: {e}")

else:
    st.markdown("### Modo de Demo")

    pasta_demo = "data_demo"

    if os.path.exists(pasta_demo) and os.path.isdir(pasta_demo):
        arquivos_demo = [f for f in os.listdir(pasta_demo) if f.endswith(('.csv', '.xlsx'))]

        if arquivos_demo:
            arquivo_selecionado = st.sidebar.selectbox(
                "Selecione a base de demonstração:",
                arquivos_demo
            )
            caminho_demo = os.path.join(pasta_demo, arquivo_selecionado)

            try:
                if arquivo_selecionado.endswith('.csv'):
                    df = pd.read_csv(caminho_demo)
                else:
                    df = pd.read_excel(caminho_demo)
                nome_arquivo = arquivo_selecionado
            except Exception as e:
                st.error(f"Erro ao ler o arquivo de demonstração: {e}")
        else:
            st.warning(f"A pasta '{pasta_demo}' existe, mas está vazia. Adicione arquivos .csv ou .xlsx.")
    else:
        st.warning(f"Pasta '{pasta_demo}' não encontrada no repositório. Crie a pasta na raiz do projeto e adicione os arquivos de teste.")

if df is not None:
    try:
        st.success(f"Arquivo '{nome_arquivo}' carregado com sucesso!")
        st.info(f"O arquivo possui {df.shape[0]} linhas e {df.shape[1]} colunas.")

        if st.button("Analisar e Gerar Relatório PDF"):
            with st.spinner("Analisando padrões e calculando riscos..."):

                df_resultados = analisar_dataframe(df)

                st.markdown("### Resultado da Análise de Risco")
                if not df_resultados.empty:
                    st.dataframe(df_resultados, hide_index=True, use_container_width=True)
                else:
                    st.success("Nenhum dado pessoal sensível foi detectado de forma evidente neste arquivo.")

                total_linhas = df.shape[0]
                pdf_bytes = gerar_pdf_bytes(df_resultados, total_linhas)

                st.markdown("### Relatório de Adequação")
                st.download_button(
                    label="Baixar Relatório em PDF",
                    data=bytes(pdf_bytes),
                    file_name=f"Relatorio_{nome_arquivo.split('.')[0]}.pdf",
                    mime="application/pdf"
                )

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
