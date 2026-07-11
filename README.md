# Proposta
Nossa proposta é uma plataforma de descoberta e inventário automatizado de dados pessoais para apoio à conformidade com a LGPD em pequenas e médias empresas.

## Escopo do MVP
- Scanner para arquivos estruturados (CSV/XLSX) locais.
- Identificação automática de dados pessoais (CPF, nome, email, telefone, endereço), usando expressões regulares (REGEX) e processamento de linguagem natural (NLP).
- Classificação de risco.
- Geração de relatório de conformidade em PDF.

## Tecnologias
#### Back end
- Python
  
#### Front end
- Streamlit

#### Processamento de Dados
- Pandas 

#### Processamento de Linguagem Natural (NLP)
- Spacy 

#### Geração de Relatórios
- fpdf2

## Fluxo do usuário 
- Usuário faz upload de arquivo: CSV, XLSX  
- Sistema analisa e exibe os dados detectados  
- Usuário interage com a interface para preencher a Base Legal e Finalidade  
- Usuário clica em um novo botão para gerar o PDF consolidado  

