## Proposta
Nossa proposta é uma plataforma de descoberta e inventário automatizado de dados pessoais para apoio à conformidade com a LGPD em pequenas e médias empresas.

### Escopo MVP
- Scanner para arquivos estruturados locais.
- Upload de CSV/XLSX.
- Identificação automática de dados pessoais (CPF, nome, email, telefone, endereço).
- Classificação de risco.
- Geração de relatório de adequação a LGPD em PDF.

**Fluxo do usuário**  
Usuário faz upload de arquivo: CSV, XLSX  
Sistema analisa colunas  
Sistema calcula risco  
Exemplo:  
| Base contém:  |  
|---------|
|- 1.200 CPFs|
|- 1.200 emails|
|- 1.200 telefones|
|Risco: Médio|

Sistema gera relatório
Exemplo:

Relatório de Inventário de Dados Pessoais

Arquivos analisados:
- clientes.csv

Dados encontrados:
- CPF
- Nome
- Email

Recomendação:
- Criptografar armazenamento
- Restringir acesso
- Definir política de retenção

## Evolução do projeto (próximos passos).
Mapear explicitamente alguns artigos da lei, por exemplo:  
- Inventário de dados pessoais
- Minimização de dados
- Controle de retenção
- Segurança da informação
