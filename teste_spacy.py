import streamlit as st
import spacy
import pandas as pd

st.set_page_config(page_title="Hello World SpaCy", layout="centered")
st.title("Hello World: SpaCy + Streamlit")

@st.cache_resource
def carregar_modelo():
    return spacy.load("pt_core_news_sm")

st.markdown("Iniciando o carregamento do modelo de Linguagem Natural...")

try:
    with st.spinner("Carregando pt_core_news_sm (isso pode levar alguns segundos)..."):
        nlp = carregar_modelo()
    st.success("Modelo carregado com sucesso na memória!")

    st.markdown("---")
    st.subheader("Teste de Extração de Dados Pessoais")

    texto_livre = st.text_area(
        "Digite um texto livre para o motor ler:",
        "O cliente João Carlos da Silva solicitou que a entrega fosse feita na Avenida Paulista, número 1500, São Paulo. Ele relatou ter hipertensão."
    )

    if st.button("Analisar Texto"):
        doc = nlp(texto_livre)

        entidades = []
        for entidade in doc.ents:
            entidades.append({
                "Texto Encontrado": entidade.text,
                "Rótulo (Label)": entidade.label_,
                "Explicação": spacy.explain(entidade.label_)
            })

        if entidades:
            df_entidades = pd.DataFrame(entidades)
            st.dataframe(df_entidades, hide_index=True, use_container_width=True)

            st.info("""
            **Dica de Leitura dos Rótulos:**
            * **PER**: Pessoa (Name/Person)
            * **LOC**: Localização (Endereço/Location)
            * **ORG**: Organização (Empresa)
            * **MISC**: Diversos (Miscellaneous)
            """)
        else:
            st.warning("Nenhuma entidade reconhecida neste texto.")

except Exception as e:
    st.error(f"Erro ao carregar o modelo ou processar o texto. Detalhes: {e}")
