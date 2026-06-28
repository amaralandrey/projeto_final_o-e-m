import streamlit as st
import pandas as pd
# Importamos as funções dos outros arquivos do projeto
from motor_busca import analisar_dataframe
from gerador_pdf import gerar_pdf_bytes

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Scanner LGPD - PMEs", 
    page_icon="🛡️", 
    layout="centered"
)

# Cabeçalho da Interface Visual
st.title("🛡️ Scanner de Conformidade LGPD")
st.subheader("Inventário Automatizado para Pequenas e Médias Empresas")

st.markdown("""
Faça o upload de arquivos estruturados (**CSV** ou **XLSX**) para identificar automaticamente a presença 
de dados pessoais (CPF, E-mail, Telefone) e gerar o relatório de riscos sem salvar nenhuma informação no servidor.
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
        st.write("### 🔍 Analisando dados...")
        resultados = analisar_dataframe(df)
        
        # 3. Exibição do Diagnóstico e Nível de Risco
        if resultados:
            st.warning("⚠️ Foram encontrados dados pessoais no arquivo!")
            
            # Monta uma tabela visual no Streamlit para mostrar o inventário
            dados_tabela = [
                {"Coluna no Arquivo": col, "Tipo de Dado Detectado": tipo} 
                for col, tipo in resultados.items()
            ]
            st.table(dados_tabela)
            
            # Regra de cálculo de risco simples para a banca do MVP
            qtd_colunas_expostas = len(resultados)
            if qtd_colunas_expostas >= 3:
                st.error("🚨 Nível de Risco Geral: ALTO (Múltiplos identificadores expostos)")
            else:
                st.warning("⚠️ Nível de Risco Geral: MÉDIO (Dados pessoais identificados)")
            
            # 4. Geração e Download do Relatório em PDF
            st.write("---")
            st.write("### 📄 Relatório de Adequação")
            st.markdown("Clique no botão abaixo para descarregar o relatório oficial de riscos da LGPD em formato PDF.")
            
            # Gera os bytes do PDF em tempo real na memória (Privacy by Design)
            pdf_data = gerar_pdf_bytes(resultados, len(df))
            
            # Botão nativo do Streamlit para download de ficheiros
            st.download_button(
                label="📥 Descarregar Relatório PDF",
                data=bytes(pdf_data),
                file_name=f"Relatorio_Adequacao_LGPD_{arquivo.name}.pdf",
                mime="application/pdf"
            )
            
        else:
            st.success("✅ Nenhum dado pessoal evidente (CPF, Email, Telefone) foi detectado nas amostras.")
            
        # 5. Pré-visualização dos Dados Originais (Apenas as primeiras 5 linhas)
        st.write("---")
        st.write("#### Pré-visualização dos dados enviados:")
        st.dataframe(df.head(5))
        
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
