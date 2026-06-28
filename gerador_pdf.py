from fpdf import FPDF
from datetime import datetime

class RelatorioLGPD(FPDF):
    def header(self):
        # Título do Relatório
        self.set_font("Arial", "B", 16)
        self.set_text_color(26, 54, 93) # Corrigido: set_text_color
        self.cell(0, 10, "Relatório de Adequação à LGPD (MVP)", ln=True, align="C")
        self.set_font("Arial", "I", 10)
        self.set_text_color(113, 128, 150) # Corrigido: set_text_color
        self.cell(0, 10, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", ln=True, align="C")
        self.ln(10)
        
    def footer(self):
        # Rodapé com numeração de páginas
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(113, 128, 150) # Corrigido: set_text_color
        self.cell(0, 10, f"Página {self.page_no()}/{{nb}} - Plataforma de Inventário de Dados PME", align="C")

def gerar_pdf_bytes(resultados, total_linhas):
    pdf = RelatorioLGPD()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Seção 1: Resumo do Diagnóstico
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(43, 108, 176) # Corrigido: set_text_color
    pdf.cell(0, 10, "1. Resumo do Diagnóstico do Arquivo", ln=True)
    pdf.ln(2)
    
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(45, 55, 72) # Corrigido: set_text_color
    pdf.multi_cell(0, 6, f"O scanner analisou com sucesso um total de {total_linhas} linhas. Com base nas regras automatizadas de identificação de padrões, foi gerado o inventário de dados pessoais descritos a seguir.")
    pdf.ln(5)
    
    # Seção 2: Inventário Encontrado
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(43, 108, 176) # Corrigido: set_text_color
    pdf.cell(0, 10, "2. Inventário de Dados Pessoais Detectados", ln=True)
    pdf.ln(2)
    
    # Cabeçalho da Tabela no PDF
    pdf.set_font("Arial", "B", 10)
    pdf.set_fill_color(226, 232, 240) # Corrigido: set_fill_color
    pdf.cell(90, 8, "Coluna do Arquivo original", border=1, fill=True)
    pdf.cell(100, 8, "Classificação do Dado Encontrado", border=1, fill=True, ln=True)
    
    # Linhas da Tabela
    pdf.set_font("Arial", "", 10)
    if resultados:
        for coluna, tipo in resultados.items():
            pdf.cell(90, 8, str(coluna), border=1)
            pdf.cell(100, 8, f"Contém: {tipo} (Dado Pessoal - Art. 5, I da LGPD)", border=1, ln=True)
    else:
        pdf.cell(190, 8, "Nenhum dado pessoal evidente detectado neste arquivo.", border=1, ln=True)
    pdf.ln(5)
    
    # Seção 3: Recomendações de Segurança
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(43, 108, 176) # Corrigido: set_text_color
    pdf.cell(0, 10, "3. Recomendações Iniciais para a PME", ln=True)
    pdf.ln(2)
    
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(45, 55, 72) # Corrigido: set_text_color
    recomendacoes = (
        "- Minimize a coleta: Avalie se todas as colunas com dados pessoais listadas acima são estritamente necessárias para a operação da empresa.\n"
        "- Controle de Acesso: Restrinja o acesso a este arquivo apenas a colaboradores que realmente necessitam tratá-lo.\n"
        "- Descarte Seguro: Caso o arquivo não possua mais finalidade legal ou comercial válida, elimine-o permanentemente dos seus sistemas corporativos.\n"
        "- Armazenamento Seguro: Se precisar manter o arquivo, prefira armazená-lo em ambientes de nuvem protegidos por criptografia e autenticação em dois fatores (2FA)."
    )
    pdf.multi_cell(0, 6, recomendacoes)
    
    # Retorna o PDF gerado diretamente como bytes na memória
    return pdf.output()
