import streamlit as st
import pandas as pd
from motor_busca import analisar_dataframe
# IMPORTANTE: Importar o novo gerador de PDF
from gerador_pdf import gerar_pdf_bytes

st.set_page_config(page_title="Scanner LGPD", page_icon="🛡️", layout="centered")

st.title("🛡️ Scanner de Conformidade LGPD")
st.subheader("Inventário Automatizado para PMEs")

st.markdown("Faça o upload de arquivos estruturados (CSV ou XLSX) para identificar automaticamente a presença de dados pessoais.")

arquivo = st.file_uploader("Selecione o arquivo de dados", type=["csv", "xlsx"])

if arquivo is not None:
    try:
        if arquivo.name.endswith('.csv'):
            df = pd.read_csv(arquivo)
        else:
            df = pd.read_excel(arquivo)
            
        st.success(f"Arquivo '{arquivo.name}' carregado com sucesso!")
        
        st.write("### 🔍 Analisando dados...")
        resultados = analisar_dataframe(df)
        
        if resultados:
            st.warning("⚠️ Foram encontrados dados pessoais no arquivo!")
            
            dados_tabela = [{"Coluna no Arquivo": col, "Tipo de Dado Detectado": tipo} for col, tipo in resultados.items()]
            st.table(dados_tabela)
            
            # Cálculo de risco
            qtd_colunas_expostas = len(resultados)
            if qtd_colunas_expostas >= 3:
                st.error("🚨 Nível de Risco Geral: ALTO (Múltiplos identificadores sensíveis expostos)")
            else:
                st.warning("⚠️ Nível de Risco Geral: MÉDIO (Dados pessoais identificados)")
            
            # --- AQUI ENTRA A MÁGICA DO PDF ---
            st.write("---")
            st.write("### 📄 Relatório de Adequação")
            st.markdown("Clique no botão abaixo para descarregar o relatório oficial de riscos da LGPD em formato PDF.")
            
            # Geramos os bytes do PDF em tempo real na memória
            pdf_data = gerar_pdf_bytes(resultados, len(df))
            
            # Botão oficial do Streamlit que permite o download direto do navegador
            st.download_button(
                label="📥 Descarregar Relatório PDF",
                data=bytes(pdf_data),
                file_name=f"Relatorio_Adequacao_LGPD_{arquivo.name}.pdf",
                mime="application/pdf"
            )
            
        else:
            st.success("✅ Nenhum dado pessoal evidente (CPF, Email, Telefone) foi detectado nas amostras.")
            
        st.write("---")
        st.write("#### Pré-visualização dos dados enviados:")
        st.dataframe(df.head(5))
        
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
