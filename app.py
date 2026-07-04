import streamlit as st
import pandas as pd

st.set_page_config(page_title="Scanner de Privacidade", layout="centered")
st.title("Scanner")
st.subheader("Inventário Automatizado de Dados Pessoais")

st.markdown("### Upload de Arquivo")
arquivo = st.file_uploader("Selecione o arquivo de dados", type=["csv", "xlsx"])

if arquivo is not None:
    try:
        if arquivo.name.endswith('.csv'):
            df = pd.read_csv(arquivo)
        else:
            df = pd.read_excel(arquivo)

        st.success(f"Arquivo '{arquivo.name}' carregado com sucesso!")
        st.info(f"O arquivo possui {df.shape[0]} linhas e {df.shape[1]} colunas.")

        if st.button("Analisar e Gerar Relatório PDF"):
            st.warning("O motor de busca e o gerador de PDF serão integrados nas próximas etapas.")

        st.markdown("#### Visualização Rápida")
        df_metadados = pd.DataFrame({
            "Nome da Coluna": df.columns,
            "Tipo Original": df.dtypes.astype(str)
        })
        st.dataframe(df_metadados, hide_index=True, use_container_width=True)

        st.markdown("---")
        
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
