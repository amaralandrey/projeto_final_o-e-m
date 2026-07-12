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

        if "df_resultados" not in st.session_state:
            st.session_state.df_resultados = None
        if "analise_concluida" not in st.session_state:
            st.session_state.analise_concluida = False

        if st.button("Analisar Arquivo"):
            with st.spinner("Analisando padrões e calculando riscos..."):
                st.session_state.df_resultados = analisar_dataframe(df)
                st.session_state.analise_concluida = True

        if st.session_state.analise_concluida:
            df_resultados = st.session_state.df_resultados

            st.markdown("### Classificação de Tratamento (ROPA)")

            df_para_relatorio = df_resultados

            if not df_resultados.empty:
                st.info("Preencha a Base Legal e a Finalidade para cada dado pessoal encontrado. Essas informações constarão no relatório final.")

                if "Base Legal" not in df_resultados.columns:
                    df_resultados["Base Legal"] = "Não classificado"
                if "Finalidade" not in df_resultados.columns:
                    df_resultados["Finalidade"] = ""

                df_para_relatorio = st.data_editor(
                    df_resultados,
                    column_config={
                        "Coluna": st.column_config.TextColumn("Coluna do Arquivo", disabled=True),
                        "Tipo de Dado Pessoal": st.column_config.TextColumn("Tipo de Dado", disabled=True),
                        "Nível de Risco": st.column_config.TextColumn("Risco", disabled=True),
                        "Base Legal": st.column_config.SelectboxColumn(
                            "Base Legal",
                            help="Selecione a base legal aplicável (Art. 7º LGPD)",
                            options=[
                                "Não classificado", "Consentimento", "Execução de Contrato",
                                "Obrigação Legal", "Legítimo Interesse", "Proteção da Vida",
                                "Tutela da Saúde", "Proteção ao Crédito", "Exercício Regular de Direitos"
                            ],
                            required=True
                        ),
                        "Finalidade": st.column_config.TextColumn(
                            "Finalidade",
                            help="Descreva brevemente o motivo da coleta (Máx. 35 caracteres recomendados)",
                            default=""
                        )
                    },
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.success("Nenhum dado pessoal sensível foi detectado de forma evidente neste arquivo.")

            total_linhas = df.shape[0]
            pdf_bytes = gerar_pdf_bytes(df_para_relatorio, total_linhas)

            st.markdown("### Relatório de Adequação")
            st.download_button(
                label="Baixar Relatório em PDF (ROPA)",
                data=bytes(pdf_bytes),
                file_name=f"Relatorio_{nome_arquivo.split('.')[0]}.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
