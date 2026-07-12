from fpdf import FPDF
from datetime import datetime
import pandas as pd

class RelatorioLGPD(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.set_text_color(26, 54, 93)
        self.cell(0, 10, "Relatório de Adequação à LGPD (MVP)", ln=True, align="C")
        self.set_font("Arial", "I", 10)
        self.set_text_color(113, 128, 150)
        self.cell(0, 10, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(113, 128, 150)
        self.cell(0, 10, f"Página {self.page_no()}/{{nb}} - Plataforma de Inventário de Dados", align="C")

def gerar_pdf_bytes(df_resultados, total_linhas):
    pdf = RelatorioLGPD()
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(43, 108, 176)
    pdf.cell(0, 10, "1. Resumo do Diagnóstico do Arquivo", ln=True)
    pdf.ln(2)

    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(45, 55, 72)
    pdf.multi_cell(0, 6, f"O scanner analisou com sucesso um total de {total_linhas} linhas.")
    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(43, 108, 176)
    pdf.cell(0, 10, "2. Inventário de Dados Pessoais Detectados (ROPA)", ln=True)
    pdf.ln(2)

    pdf.set_font("Arial", "B", 8)
    pdf.set_fill_color(226, 232, 240)
    pdf.cell(35, 8, "Coluna do Arquivo", border=1, fill=True)
    pdf.cell(30, 8, "Tipo de Dado", border=1, fill=True)
    pdf.cell(20, 8, "Risco", border=1, fill=True)
    pdf.cell(45, 8, "Base Legal", border=1, fill=True)
    pdf.cell(60, 8, "Finalidade", border=1, fill=True, ln=True)

    pdf.set_font("Arial", "", 8)

    if not df_resultados.empty:
        for index, row in df_resultados.iterrows():
            coluna_nome = str(row['Coluna'])[:20]
            tipo_dado = str(row['Tipo de Dado Pessoal'])[:15]
            risco = str(row['Nível de Risco'])
            base_legal = str(row.get('Base Legal', 'Não classificado'))[:25]
            finalidade = str(row.get('Finalidade', ''))[:35]

            pdf.cell(35, 8, coluna_nome, border=1)
            pdf.cell(30, 8, tipo_dado, border=1)

            if risco == "Alto":
                pdf.set_text_color(229, 62, 62)
            elif risco == "Médio":
                pdf.set_text_color(221, 107, 32)
            else:
                pdf.set_text_color(56, 161, 105)

            pdf.cell(20, 8, risco, border=1)

            pdf.set_text_color(45, 55, 72)

            pdf.cell(45, 8, base_legal, border=1)
            pdf.cell(60, 8, finalidade, border=1, ln=True)
    else:
        pdf.cell(190, 8, "Nenhum dado pessoal evidente detectado neste arquivo.", border=1, ln=True)

    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(43, 108, 176)
    pdf.cell(0, 10, "3. Recomendações Iniciais", ln=True)
    pdf.ln(2)

    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(45, 55, 72)
    recomendacoes = (
        "- Minimize a coleta: Avalie se todas as colunas com dados pessoais listadas acima são estritamente necessárias para a operação da empresa.\n"
        "- Controle de Acesso: Restrinja o acesso a este arquivo apenas a colaboradores que realmente necessitam tratá-lo.\n"
        "- Descarte Seguro: Caso o arquivo não possua mais finalidade legal ou comercial válida, elimine-o permanentemente dos seus sistemas corporativos.\n"
        "- Armazenamento Seguro: Se precisar manter o arquivo, prefira armazená-lo em ambientes de nuvem protegidos por criptografia e autenticação em dois fatores (2FA)."
    )
    pdf.multi_cell(0, 6, recomendacoes)

    return pdf.output()
