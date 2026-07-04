import streamlit as st
import pandas as pd

# Importação dos módulos do backend
from motor_busca import analisar_dataframe
from gerador_pdf import gerar_pdf_bytes

st.set_page_config(page_title="Scanner de Privacidade", layout="centered")
st.title("Scanner")
st.subheader("Inventário Automatizado de Dados Pessoais")

st.markdown("### Upload de Arquivo")
arquivo = st.file_uploader("Selecione o arquivo de dados", type=["csv", "xlsx"])

if arquivo is not None:
    try:
        # Leitura do arquivo
        if arquivo.name.endswith('.csv'):
            df = pd.read_csv(arquivo)
        else:
            df = pd.read_excel(arquivo)

        st.success(f"Arquivo '{arquivo.name}' carregado com sucesso!")
        st.info(f"O arquivo possui {df.shape[0]} linhas e {df.shape[1]} colunas.")
        
        # Mantém a visualização rápida e segura dos metadados
        st.markdown("#### Visualização Rápida")
        df_metadados = pd.DataFrame({
            "Nome da Coluna": df.columns,
            "Tipo Original": df.dtypes.astype(str)
        })
        st.dataframe(df_metadados, hide_index=True, use_container_width=True)

        st.markdown("---")

        # Integração Completa dos Módulos
        if st.button("Analisar e Gerar Relatório PDF"):
            with st.spinner("Analisando padrões e calculando riscos..."):
                
                # 1. Aciona o Motor de Busca
                df_resultados = analisar_dataframe(df)
                
                # 2. Exibe o resultado na interface
                st.markdown("### 📊 Resultado da Análise de Risco")
                if not df_resultados.empty:
                    st.dataframe(df_resultados, hide_index=True, use_container_width=True)
                else:
                    st.success("Nenhum dado pessoal sensível foi detectado de forma evidente neste arquivo.")
                
                # 3. Aciona o Gerador de PDF
                total_linhas = df.shape[0]
                pdf_bytes = gerar_pdf_bytes(df_resultados, total_linhas)
                
                # 4. Habilita o botão de Download
                st.markdown("### 📄 Relatório de Adequação")
                st.download_button(
                    label="Baixar Relatório LGPD em PDF",
                    data=bytes(pdf_bytes),
                    file_name=f"Relatorio_LGPD_{arquivo.name}.pdf",
                    mime="application/pdf"
                )

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
