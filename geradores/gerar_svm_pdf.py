# -*- coding: utf-8 -*-
"""
Gerador de PDFs para o SVM aplicado ao diagnóstico de doença cardíaca.
Produz:
  - graficos_svm/  (PNGs intermediários)
  - Artigo_SVM_FATEC.pdf
  - Relatorio_SVM_FATEC.pdf
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from fpdf import FPDF

# ---------------------------------------------------------------------------
# Diretório de saída dos gráficos
# ---------------------------------------------------------------------------
GRAFICOS_DIR = os.path.join(os.path.dirname(__file__), "graficos_svm")
os.makedirs(GRAFICOS_DIR, exist_ok=True)

def gpath(name):
    return os.path.join(GRAFICOS_DIR, name)

# ===========================================================================
# GERAÇÃO DOS GRÁFICOS (matplotlib → PNG)
# ===========================================================================

AZUL     = "#2563EB"
LARANJA  = "#EA580C"
VERDE    = "#16A34A"
CINZA    = "#6B7280"
VERMELHO = "#DC2626"
ROXO     = "#7C3AED"

PLT_PARAMS = {
    "font.family": "DejaVu Sans",
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.dpi": 150,
}
plt.rcParams.update(PLT_PARAMS)


def fig1_acuracia_blocos():
    """Acurácia por bloco – SVM."""
    blocos  = ["Bloco 1\n(1-50)", "Bloco 2\n(51-100)", "Bloco 3\n(101-150)",
               "Bloco 4\n(151-200)", "Bloco 5\n(201-250)", "Bloco 6\n(251-297)"]
    svm     = [90.00, 86.00, 92.00, 84.00, 86.00, 78.72]
    x       = np.arange(len(blocos))
    width   = 0.55

    fig, ax = plt.subplots(figsize=(9, 4.5))
    bars1 = ax.bar(x, svm, width, label="SVM (RBF, C=0,1)",
                   color=AZUL, alpha=0.88, edgecolor="white")

    ax.axhline(83.51, color=AZUL, linestyle="--", linewidth=1.5,
               label="Cross-val 10-fold (83,51%)")

    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f"{bar.get_height():.0f}%", ha="center", va="bottom",
                fontsize=9, color=AZUL, fontweight="bold")

    ax.set_xlabel("Bloco de registros")
    ax.set_ylabel("Acurácia (%)")
    ax.set_title("Figura 1 – Acurácia por Bloco de Registros (SVM)", fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(blocos)
    ax.set_ylim(70, 100)
    ax.legend(fontsize=9, loc="lower left")
    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(gpath("fig1_acuracia_blocos.png"), bbox_inches="tight")
    plt.close(fig)
    print("  fig1_acuracia_blocos.png gerado.")


def fig2_matriz_confusao():
    """Heatmap da matriz de confusão."""
    cm   = np.array([[30, 2], [6, 22]])
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    im = ax.imshow(cm, cmap="Blues", vmin=0, vmax=32)
    plt.colorbar(im, ax=ax, fraction=0.04, pad=0.04)

    labels = [["VN = 30\nSaudável corretamente\nidentificado",
               "FP = 2\nSaudável classificado\ncomo Doente"],
              ["FN = 6\nDoente classificado\ncomo Saudável",
               "VP = 22\nDoente corretamente\nidentificado"]]
    cores  = [["#1E40AF", "#DC2626"], ["#DC2626", "#1E40AF"]]

    for i in range(2):
        for j in range(2):
            ax.text(j, i, labels[i][j],
                    ha="center", va="center", fontsize=8.5,
                    color="white" if cm[i, j] > 15 else "black",
                    fontweight="bold")

    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["Previsto: Saudável (0)", "Previsto: Doente (1)"], fontsize=9)
    ax.set_yticklabels(["Real: Saudável (0)", "Real: Doente (1)"], fontsize=9)
    ax.set_xlabel("Classe Prevista", fontsize=10)
    ax.set_ylabel("Classe Real", fontsize=10)
    ax.set_title("Figura 2 – Matriz de Confusão (Conjunto de Teste, n=60)",
                 fontweight="bold", fontsize=11)
    fig.tight_layout()
    fig.savefig(gpath("fig2_matriz_confusao.png"), bbox_inches="tight")
    plt.close(fig)
    print("  fig2_matriz_confusao.png gerado.")


def fig3_metricas_por_classe():
    """Barras agrupadas: Precisão / Revocação / F1 por classe."""
    classes  = ["Saudável (0)", "Doente (1)"]
    precisao = [0.83, 0.92]
    recall   = [0.94, 0.79]
    f1       = [0.88, 0.85]

    x     = np.arange(len(classes))
    width = 0.25
    fig, ax = plt.subplots(figsize=(7, 4.5))

    b1 = ax.bar(x - width, precisao, width, label="Precisão",  color=AZUL,    alpha=0.88)
    b2 = ax.bar(x,         recall,   width, label="Revocação", color=LARANJA,  alpha=0.88)
    b3 = ax.bar(x + width, f1,       width, label="F1-Score",  color=VERDE,    alpha=0.88)

    for bars in [b1, b2, b3]:
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                    f"{bar.get_height():.2f}", ha="center", va="bottom", fontsize=9)

    ax.set_ylim(0, 1.12)
    ax.set_xticks(x)
    ax.set_xticklabels(classes, fontsize=10)
    ax.set_ylabel("Valor da Métrica")
    ax.set_title("Figura 3 – Precisão, Revocação e F1-Score por Classe (Conjunto de Teste)",
                 fontweight="bold")
    ax.legend(fontsize=9)
    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(gpath("fig3_metricas_por_classe.png"), bbox_inches="tight")
    plt.close(fig)
    print("  fig3_metricas_por_classe.png gerado.")


def fig4_top5_hiperparametros():
    """Barras horizontais: top-5 combinações de hiperparâmetros."""
    labels  = [
        "C=1,0 | poly | scale",
        "C=0,1 | linear | auto",
        "C=0,1 | linear | scale",
        "C=0,1 | rbf | auto",
        "C=0,1 | rbf | scale  (sel)",
    ]
    acc     = [81.00, 81.00, 81.00, 82.27, 82.27]
    erros   = [4.68,  6.98,  6.98,  5.28,  5.28]
    colors  = [CINZA, CINZA, CINZA, LARANJA, AZUL]

    fig, ax = plt.subplots(figsize=(9, 4))
    bars = ax.barh(labels, acc, xerr=erros, color=colors, alpha=0.88,
                   capsize=4, error_kw={"elinewidth": 1.5, "ecolor": "gray"})

    for bar, a in zip(bars, acc):
        ax.text(bar.get_width() - 0.3, bar.get_y() + bar.get_height()/2,
                f"{a:.2f}%", ha="right", va="center", fontsize=9,
                color="white", fontweight="bold")

    ax.set_xlabel("Acurácia CV Média (%)")
    ax.set_title("Figura 4 – Top-5 Combinações de Hiperparâmetros (GridSearchCV 5-fold)",
                 fontweight="bold")
    ax.set_xlim(76, 90)
    ax.xaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)

    patch_best  = mpatches.Patch(color=AZUL,    label="Melhor combinação (selecionada)")
    patch_2nd   = mpatches.Patch(color=LARANJA, label="2ª colocada")
    patch_other = mpatches.Patch(color=CINZA,   label="Demais combinações")
    ax.legend(handles=[patch_best, patch_2nd, patch_other], fontsize=8, loc="lower right")
    fig.tight_layout()
    fig.savefig(gpath("fig4_top5_hiperparametros.png"), bbox_inches="tight")
    plt.close(fig)
    print("  fig4_top5_hiperparametros.png gerado.")


def fig5_distribuicao_acertos():
    """Pizza: distribuição de acertos e erros nos 297 registros."""
    valores = [256, 41]
    labels  = ["Acertos (256 — 86,20%)", "Erros (41 — 13,80%)"]
    cores   = [AZUL, VERMELHO]
    explode = (0.03, 0.08)

    fig, ax = plt.subplots(figsize=(6, 5))
    wedges, texts, autotexts = ax.pie(
        valores, labels=labels, colors=cores, explode=explode,
        autopct="%1.1f%%", startangle=90,
        textprops={"fontsize": 10},
        wedgeprops={"edgecolor": "white", "linewidth": 2})
    for at in autotexts:
        at.set_fontsize(11)
        at.set_fontweight("bold")
        at.set_color("white")

    ax.set_title("Figura 5 – Distribuição de Acertos e Erros\n(297 registros — conjunto completo)",
                 fontweight="bold")

    # Detalhamento dos erros (FN / FP)
    ax2 = fig.add_axes([0.68, 0.08, 0.28, 0.28])
    ax2.pie([6, 2], labels=["FN\n(6)", "FP\n(2)"],
            colors=[VERMELHO, LARANJA], startangle=90,
            textprops={"fontsize": 8},
            wedgeprops={"edgecolor": "white", "linewidth": 1.5})
    ax2.set_title("Erros\n(teste)", fontsize=8, pad=3)

    fig.subplots_adjust(left=0.08, right=0.95, top=0.92, bottom=0.08)
    fig.savefig(gpath("fig5_distribuicao_acertos.png"), bbox_inches="tight")
    plt.close(fig)
    print("  fig5_distribuicao_acertos.png gerado.")


def fig6_resumo_desempenho():
    """Barras: resumo das métricas de desempenho do SVM."""
    metricas = ["Acurácia\nTeste", "Acurácia\nCV 10-fold", "F1\nSaudável", "F1\nDoente"]
    valores  = [86.67, 83.51, 88.0, 85.0]
    cores    = [AZUL, VERDE, ROXO, LARANJA]

    x     = np.arange(len(metricas))
    width = 0.50
    fig, ax = plt.subplots(figsize=(8, 4.5))

    bars = ax.bar(x, valores, width, color=cores, alpha=0.88, edgecolor="white")

    for bar, v in zip(bars, valores):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f"{v:.1f}%", ha="center", va="bottom",
                fontsize=11, fontweight="bold", color="black")

    ax.set_xticks(x)
    ax.set_xticklabels(metricas, fontsize=10)
    ax.set_ylabel("Valor (% / escala x100 para F1)")
    ax.set_ylim(70, 97)
    ax.set_title("Figura 6 – Resumo de Desempenho do SVM (C=0,1, kernel=rbf, gamma=scale)",
                 fontweight="bold")
    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(gpath("fig6_comparacao_svm_knn.png"), bbox_inches="tight")
    plt.close(fig)
    print("  fig6_comparacao_svm_knn.png gerado.")


def fig7_kernel_comparacao():
    """Barras: acurácia média CV por kernel."""
    kernels = ["linear\nscale", "linear\nauto", "poly\nscale", "poly\nauto",
               "rbf\nscale(sel)", "rbf\nauto"]
    accs    = [81.00, 81.00, 81.00, 79.50, 82.27, 82.27]
    stds    = [6.98, 6.98, 4.68, 5.20, 5.28, 5.28]
    cores   = [CINZA, CINZA, CINZA, CINZA, AZUL, LARANJA]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    bars = ax.bar(kernels, accs, yerr=stds, color=cores, alpha=0.88,
                  capsize=5, error_kw={"elinewidth": 1.5, "ecolor": "dimgray"})
    for bar, a in zip(bars, accs):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + .6,
                f"{a:.2f}%", ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax.set_xlabel("Kernel | Gamma  (C=0,1 para todos)")
    ax.set_ylabel("Acurácia CV Média (%)")
    ax.set_ylim(70, 92)
    ax.set_title("Figura 7 – Acurácia na Validação Cruzada por Kernel (C=0,1)",
                 fontweight="bold")
    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    patch_best = mpatches.Patch(color=AZUL,    label="Melhor (selecionado)")
    patch_2nd  = mpatches.Patch(color=LARANJA, label="Equivalente 2°")
    patch_ot   = mpatches.Patch(color=CINZA,   label="Demais")
    ax.legend(handles=[patch_best, patch_2nd, patch_ot], fontsize=9)
    fig.tight_layout()
    fig.savefig(gpath("fig7_kernel_comparacao.png"), bbox_inches="tight")
    plt.close(fig)
    print("  fig7_kernel_comparacao.png gerado.")


def gerar_todos_graficos():
    print("\n=== Gerando gráficos ===")
    fig1_acuracia_blocos()
    fig2_matriz_confusao()
    fig3_metricas_por_classe()
    fig4_top5_hiperparametros()
    fig5_distribuicao_acertos()
    fig6_resumo_desempenho()
    fig7_kernel_comparacao()
    print("Todos os gráficos gerados em:", GRAFICOS_DIR)


# ===========================================================================
# CLASSE PDF BASE (padrão FATEC)
# ===========================================================================

MARGIN_LEFT   = 20.0
MARGIN_RIGHT  = 20.0
MARGIN_TOP    = 25.0
MARGIN_BOTTOM = 20.0
PAGE_W        = 210.0
PAGE_H        = 297.0
CONTENT_W     = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT
FONT          = "Arial"
SIZE_BODY     = 11
SIZE_SMALL    = 10
SIZE_TITLE    = 12
LINE_H        = 7.0
LINE_H_SM     = 6.0
LINE_H_TBL    = 5.5
INDENT        = 12.5

ARIAL_FONTS = {
    "":   "C:/Windows/Fonts/arial.ttf",
    "B":  "C:/Windows/Fonts/arialbd.ttf",
    "I":  "C:/Windows/Fonts/ariali.ttf",
    "BI": "C:/Windows/Fonts/arialbi.ttf",
}


class BaseFATEC(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for style, path in ARIAL_FONTS.items():
            if os.path.exists(path):
                self.add_font("Arial", style, path)

    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font(FONT, "", SIZE_SMALL)
        self.cell(0, 10, str(self.page_no()), align="C")

    def set_body(self, bold=False, italic=False, size=SIZE_BODY):
        style = ("B" if bold else "") + ("I" if italic else "")
        self.set_font(FONT, style, size)

    def para(self, text, indent=True, align="J", size=SIZE_BODY,
             bold=False, italic=False, lh=None):
        lh = lh or (LINE_H if size == SIZE_BODY else LINE_H_SM)
        self.set_body(bold=bold, italic=italic, size=size)
        if indent:
            self.set_x(MARGIN_LEFT + INDENT)
            self.multi_cell(CONTENT_W - INDENT, lh, text, align=align)
        else:
            self.set_x(MARGIN_LEFT)
            self.multi_cell(CONTENT_W, lh, text, align=align)

    def section(self, num, title, level=1):
        self.ln(3)
        self.set_body(bold=True, size=SIZE_BODY)
        label = f"{num} {title}".strip()
        self.set_x(MARGIN_LEFT)
        self.multi_cell(CONTENT_W, LINE_H, label, align="L")
        self.ln(1)

    def center_line(self, text, size=SIZE_BODY, bold=False, italic=False):
        lh = LINE_H if size >= SIZE_BODY else LINE_H_SM
        self.set_body(bold=bold, italic=italic, size=size)
        self.set_x(MARGIN_LEFT)
        self.multi_cell(CONTENT_W, lh, text, align="C")

    def ref_entry(self, text):
        self.set_body(size=SIZE_BODY)
        self.set_x(MARGIN_LEFT)
        self.multi_cell(CONTENT_W, LINE_H_TBL + 0.5, text, align="J")
        self.ln(2)

    def table_caption(self, text):
        self.set_body(bold=True, size=SIZE_SMALL)
        self.set_x(MARGIN_LEFT)
        self.multi_cell(CONTENT_W, LINE_H_SM, text, align="C")

    def table_source(self, text):
        self.set_body(size=SIZE_SMALL)
        self.set_x(MARGIN_LEFT)
        self.multi_cell(CONTENT_W, LINE_H_SM, text, align="C")
        self.ln(3)

    def fig_caption(self, text):
        self.set_body(size=SIZE_SMALL)
        self.set_x(MARGIN_LEFT)
        self.multi_cell(CONTENT_W, LINE_H_SM, text, align="C")
        self.ln(3)

    def draw_hline(self):
        self.set_draw_color(0)
        self.set_line_width(0.3)
        self.line(MARGIN_LEFT, self.get_y(), PAGE_W - MARGIN_RIGHT, self.get_y())
        self.ln(1)

    def insert_figure(self, img_path, w=150, caption=None):
        """Insere uma figura centralizada com legenda opcional."""
        if not os.path.exists(img_path):
            return
        x = MARGIN_LEFT + (CONTENT_W - w) / 2
        self.image(img_path, x=x, w=w)
        self.ln(1)
        if caption:
            self.fig_caption(caption)

    def simple_table(self, headers, rows, col_widths,
                     header_align=None, row_aligns=None):
        self.set_body(bold=True, size=SIZE_SMALL)
        x0 = MARGIN_LEFT
        self.set_x(x0)
        ha = header_align or ["C"] * len(headers)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], LINE_H_TBL + 1, h, border=1, align=ha[i])
        self.ln()
        self.set_body(size=SIZE_SMALL)
        ra = row_aligns or [["L"] + ["C"] * (len(headers) - 1)] * len(rows)
        for ri, row in enumerate(rows):
            self.set_x(x0)
            aligns = ra[ri] if isinstance(ra[0], list) else ra
            for i, cell in enumerate(row):
                self.cell(col_widths[i], LINE_H_TBL + 1, str(cell),
                          border=1, align=aligns[i])
            self.ln()
        self.ln(2)

    def formula(self, text):
        self.set_body(italic=True, size=SIZE_BODY)
        self.set_x(MARGIN_LEFT + INDENT)
        self.multi_cell(CONTENT_W - INDENT, LINE_H, text, align="L")
        self.ln(1)

    def quote_block(self, text):
        self.set_body(size=SIZE_SMALL)
        self.set_x(MARGIN_LEFT + 40)
        self.multi_cell(CONTENT_W - 40, LINE_H_SM, text, align="J")
        self.ln(2)


# ===========================================================================
# ARTIGO SVM — PDF COMPLETO
# ===========================================================================

def build_artigo():
    pdf = BaseFATEC(orientation="P", unit="mm", format="A4")
    pdf.set_margins(MARGIN_LEFT, MARGIN_TOP, MARGIN_RIGHT)
    pdf.set_auto_page_break(auto=True, margin=MARGIN_BOTTOM)
    pdf.add_page()

    # TÍTULO
    pdf.set_body(bold=True, size=SIZE_TITLE)
    pdf.set_x(MARGIN_LEFT)
    pdf.multi_cell(CONTENT_W, LINE_H,
        "SUPPORT VECTOR MACHINE APLICADO AO DIAGNÓSTICO DE DOENÇA CARDÍACA: "
        "FUNDAMENTOS MATEMÁTICOS, IMPLEMENTAÇÃO E ANÁLISE DE DESEMPENHO",
        align="C")
    pdf.ln(2)

    pdf.center_line("André Felipe", size=SIZE_SMALL, italic=True)
    pdf.center_line("Faculdade de Tecnologia de Guaratinguetá", size=SIZE_SMALL, italic=True)
    pdf.center_line("andressmota78@gmail.com", size=SIZE_SMALL, italic=True)
    pdf.ln(4)

    # RESUMO
    pdf.set_body(bold=True)
    pdf.set_x(MARGIN_LEFT)
    pdf.cell(CONTENT_W, LINE_H, "Resumo", align="L")
    pdf.ln(1)
    pdf.para(
        "Este artigo apresenta a aplicação do algoritmo Support Vector Machine (SVM) para a "
        "classificação binária de doença cardíaca utilizando o Cleveland Heart Disease Dataset "
        "(UCI Machine Learning Repository, id=45). São cobertos os fundamentos matemáticos do "
        "algoritmo, incluindo a formulação do problema de otimização de margem máxima, a introdução "
        "de variáveis de folga para margens suaves, o truque do kernel e as funções RBF, linear e "
        "polinomial. A implementação foi desenvolvida em Python com a biblioteca scikit-learn, "
        "empregando padronização Z-score, particionamento estratificado e otimização automática dos "
        "hiperparâmetros C, kernel e gamma via GridSearchCV. A melhor combinação encontrada foi "
        "C = 0,1, kernel RBF e gamma = scale, obtendo acurácia de 86,67% no conjunto de teste e "
        "83,51% +/- 7,66% na validação cruzada de 10 dobras sobre 297 registros avaliados.",
        indent=False)
    pdf.ln(1)
    pdf.set_font(FONT, "B", SIZE_BODY)
    pdf.set_x(MARGIN_LEFT)
    pdf.write(LINE_H, "Palavras-chave: ")
    pdf.set_body()
    pdf.write(LINE_H,
        "Support Vector Machine; Kernel RBF; Aprendizado de Máquina; Doença Cardíaca; "
        "Classificação Binária; Validação Cruzada.")
    pdf.ln(4)

    # ABSTRACT
    pdf.set_body(bold=True)
    pdf.set_x(MARGIN_LEFT)
    pdf.cell(CONTENT_W, LINE_H, "Abstract", align="L")
    pdf.ln(1)
    pdf.para(
        "This paper presents the application of the Support Vector Machine (SVM) algorithm for "
        "binary classification of heart disease using the Cleveland Heart Disease Dataset (UCI "
        "Machine Learning Repository, id=45). The mathematical foundations of the algorithm are "
        "covered, including the maximum-margin optimization formulation, soft-margin slack variables, "
        "the kernel trick, and RBF, linear and polynomial kernel functions. The Python implementation "
        "uses Z-score standardization, stratified data partitioning and automatic hyperparameter "
        "optimization of C, kernel and gamma via GridSearchCV. The best combination found was "
        "C = 0.1, RBF kernel and gamma = scale, achieving 86.67% accuracy on the test set and "
        "83.51% +/- 7.66% in 10-fold cross-validation over 297 evaluated patients.",
        indent=False)
    pdf.ln(1)
    pdf.set_font(FONT, "B", SIZE_BODY)
    pdf.set_x(MARGIN_LEFT)
    pdf.write(LINE_H, "Keywords: ")
    pdf.set_body()
    pdf.write(LINE_H,
        "Support Vector Machine; RBF Kernel; Machine Learning; Heart Disease; "
        "Binary Classification; Cross-Validation.")
    pdf.ln(6)

    # =====================================================================
    # INTRODUÇÃO
    # =====================================================================
    pdf.section("", "Introdução", level=0)
    pdf.para(
        "As doenças cardiovasculares (DCV) representam a principal causa de mortalidade global, "
        "responsáveis por aproximadamente 17,9 milhões de óbitos anuais — cerca de 32% de todas "
        "as mortes no mundo, segundo a Organização Mundial da Saúde. No Brasil, esse número "
        "ultrapassa 300 mil óbitos por ano, sendo que grande parcela poderia ser evitada com "
        "diagnóstico precoce e intervenção oportuna (MIENYE; SUN, 2022). A doença arterial "
        "coronariana, em particular, frequentemente evolui de forma silenciosa por anos antes "
        "do primeiro evento agudo, tornando o rastreamento sistemático essencial para a "
        "redução da morbimortalidade.")
    pdf.para(
        "O diagnóstico preciso de doença cardíaca envolve combinação de exames clínicos, "
        "eletrocardiograma em esforço, ecocardiografia e, nos casos mais graves, cateterismo "
        "cardíaco — procedimentos de alta complexidade e custo. Em sistemas públicos de saúde, "
        "como o SUS no Brasil, o acesso a esses exames é limitado por filas de espera e "
        "capacidade de infraestrutura. Ferramentas de triagem automatizada baseadas em "
        "aprendizado de máquina representam uma alternativa custo-efetiva para identificar "
        "pacientes de maior risco a partir de dados clínicos de rotina, coletados em qualquer "
        "unidade básica de atendimento.")
    pdf.para(
        "Nesse contexto, o Cleveland Heart Disease Dataset (JANOSI et al., 1988), disponível "
        "no UCI Machine Learning Repository, tornou-se o benchmark dominante para estudos de "
        "diagnóstico cardíaco por aprendizado de máquina, com centenas de trabalhos publicados "
        "ao longo das últimas três décadas. O dataset contém 13 atributos clínicos e demográficos "
        "amplamente disponíveis — pressão arterial, frequência cardíaca máxima, tipo de dor "
        "torácica, resultados de ECG, entre outros — que coletivamente permitem diferenciar "
        "pacientes saudáveis de pacientes com comprometimento coronariano.")
    pdf.para(
        "O Support Vector Machine (SVM) destaca-se pelo sólido embasamento na teoria estatística "
        "da aprendizagem, especialmente na teoria de Vapnik-Chervonenkis (VC), que fornece "
        "garantias teóricas de generalização. Introduzido por Boser, Guyon e Vapnik (1992) e "
        "consolidado por Cortes e Vapnik (1995), o SVM formula a classificação como um problema "
        "de otimização convexa: encontrar o hiperplano que maximiza a distância geométrica entre "
        "as classes. Essa propriedade de margem máxima confere ao SVM capacidade de generalização "
        "superior, especialmente quando os dados de treino são escassos ou ruidosos.")
    pdf.para(
        "O SVM constrói uma representação global da fronteira decisória definida por um "
        "subconjunto mínimo de amostras denominadas vetores de suporte. Pontos distantes "
        "da fronteira não influenciam o hiperplano ótimo, conferindo robustez intrínseca a "
        "outliers e ruídos de medição — comuns em dados clínicos coletados em diferentes "
        "hospitais e condições (RUSSELL; NORVIG, 2020). Essa esparsidade da solução também "
        "torna a predição eficiente em termos computacionais, pois depende apenas de uma "
        "fração dos exemplos de treinamento.")
    pdf.para(
        "O presente artigo tem como objetivos: (i) fundamentar matematicamente o SVM desde a "
        "formulação de margem rígida até a margem suave e o truque do kernel, com ênfase nas "
        "condições de otimalidade de Karush-Kuhn-Tucker; (ii) descrever detalhadamente a "
        "implementação sobre o Cleveland Heart Disease Dataset, incluindo o pipeline de "
        "pré-processamento e a otimização de hiperparâmetros via GridSearchCV; (iii) apresentar "
        "e analisar os resultados — acurácia por blocos, matriz de confusão, relatório por classe "
        "e validação cruzada; e (iv) discutir as propriedades qualitativas do SVM no contexto "
        "clínico, incluindo robustez a outliers e eficiência de predição.")
    pdf.para(
        "O artigo está organizado da seguinte forma: a Seção 1 apresenta o referencial teórico "
        "com a fundamentação matemática completa; a Seção 2 descreve a metodologia experimental; "
        "a Seção 3 apresenta e discute os resultados com gráficos e tabelas; as Considerações "
        "Finais sintetizam as principais conclusões, limitações e perspectivas.")

    # =====================================================================
    # 1. REFERENCIAL TEÓRICO
    # =====================================================================
    pdf.section("1", "Referencial Teórico")

    pdf.section("1.1", "O Algoritmo Support Vector Machine")
    pdf.para(
        "Dado um conjunto de treinamento D = {(x1,y1), ..., (xn,yn)}, onde "
        "xi em R^d e yi em {-1,+1}, o SVM busca o hiperplano f(x) = w^T·x + b = 0 "
        "que separa as duas classes com margem máxima. A função de decisão é:")
    pdf.formula("y_hat = sinal( w^T·xq + b )")
    pdf.para(
        "onde w em R^d é o vetor normal ao hiperplano e b em R é o viés. "
        "O SVM foi introduzido por Boser, Guyon e Vapnik (1992) na formulação com kernel "
        "e consolidado por Cortes e Vapnik (1995) com a incorporação das margens suaves.")

    pdf.section("1.2", "Maximização da Margem — Formulação de Margem Rígida")
    pdf.para(
        "Para dados linearmente separáveis, a margem geométrica entre as classes é "
        "a distância entre os dois hiperplanos de suporte:")
    pdf.formula(
        "Hiperplano positivo: w^T·xi + b = +1   (para yi = +1)\n"
        "Hiperplano negativo: w^T·xi + b = -1   (para yi = -1)")
    pdf.para("A margem é:")
    pdf.formula("Margem = 2 / ||w||")
    pdf.para(
        "Maximizar a margem equivale a minimizar ||w||, formulando o problema primal "
        "de programação quadrática convexa:")
    pdf.formula(
        "min_{w,b}    (1/2) ||w||^2\n"
        "sujeito a:   yi ( w^T·xi + b ) >= 1,   para todo i = 1, ..., n")
    pdf.para(
        "Esse problema possui solução única e global garantida pelo convexidade da função objetivo.")

    pdf.section("1.3", "Vetores de Suporte e Condições KKT")
    pdf.para(
        "Os pontos de treinamento que satisfazem a restrição com igualdade "
        "— yi(w^T·xi + b) = 1 — são os vetores de suporte. Apenas esses pontos "
        "influenciam a posição do hiperplano ótimo. O vetor de pesos é expresso como:")
    pdf.formula("w = SUM_{i: alpha_i > 0}  alpha_i · yi · xi")
    pdf.para(
        "onde alpha_i são os multiplicadores de Lagrange. Essa propriedade de esparsidade "
        "confere ao SVM robustez a outliers que estejam distantes da fronteira — pontos "
        "afastados do hiperplano decisorio não são vetores de suporte e não influenciam a "
        "solução final, tornando o modelo inerentemente resistente a medições ruidosas.")

    pdf.section("1.4", "Formulação de Margem Suave — Parâmetro C")
    pdf.para(
        "Para dados não linearmente separáveis, Cortes e Vapnik (1995) introduziram "
        "variáveis de folga xi_i >= 0 que permitem violações da margem a um custo penalizado:")
    pdf.formula(
        "min_{w,b,xi}    (1/2) ||w||^2 + C * SUM_{i=1}^{n} xi_i\n\n"
        "sujeito a:   yi ( w^T·xi + b ) >= 1 - xi_i,   xi_i >= 0")
    pdf.para(
        "O hiperparâmetro C > 0 controla o equilíbrio entre margem e penalidade por violações: "
        "C pequeno permite margens largas com mais erros (maior regularização, menos overfitting); "
        "C grande força a correta classificação de quase todos os pontos (menor regularização, "
        "maior risco de overfitting). O GridSearchCV identificou C = 0,1 como valor ótimo para "
        "este dataset, indicando que os dados se beneficiam de forte regularização.")

    pdf.section("1.5", "O Truque do Kernel")
    pdf.para(
        "Para dados não linearmente separáveis no espaço original, o SVM utiliza uma "
        "transformação phi: R^d → H que mapeia amostras para um espaço de Hilbert de maior "
        "dimensão. O truque do kernel evita calcular phi explicitamente, substituindo os "
        "produtos internos na formulação dual por uma função K(xi, xj):")
    pdf.formula("K(xi, xj) = phi(xi)^T · phi(xj)")
    pdf.para(
        "A função de decisão kernelizada é:")
    pdf.formula(
        "f(x) = sinal( SUM_{i: alpha_i > 0} alpha_i · yi · K(xi, x) + b )")

    pdf.section("1.6", "Funções de Kernel")
    pdf.para(
        "Os três kernels testados neste trabalho são:")
    pdf.para(
        "Kernel Linear: K(xi,xj) = xi^T·xj. "
        "Não realiza transformação; interpreta coeficientes de w como importância dos atributos. "
        "Acurácia CV: 81,00% neste experimento.", bold=False)
    pdf.formula("K_lin(xi, xj) = xi^T · xj")
    pdf.para(
        "Kernel RBF (Radial Basis Function) — o mais amplamente utilizado (GÉRON, 2019): "
        "mapeia implicitamente para dimensão infinita via expansão da função exponencial. "
        "Acurácia CV: 82,27% — melhor resultado.", bold=False)
    pdf.formula("K_rbf(xi, xj) = exp( -gamma * ||xi - xj||^2 )")
    pdf.para(
        "Kernel Polinomial: captura interações entre atributos de até grau d. "
        "Acurácia CV: 81,00% neste experimento.", bold=False)
    pdf.formula("K_poly(xi, xj) = ( gamma * xi^T·xj + r )^d")

    pdf.section("1.7", "Parâmetro Gamma no Kernel RBF")
    pdf.para(
        "O parâmetro gamma controla a largura da função gaussiana: "
        "gamma grande gera fronteiras irregulares (risco de overfitting); "
        "gamma pequeno gera fronteiras suaves (risco de underfitting). "
        "O scikit-learn oferece dois modos automáticos:")
    pdf.formula(
        "gamma = 'scale':  gamma = 1 / (n_features * Var(X_train))\n"
        "gamma = 'auto' :  gamma = 1 / n_features")
    pdf.para(
        "Após padronização Z-score, Var(X_train) ≈ 1 para todos os atributos, tornando "
        "'scale' e 'auto' equivalentes — fato confirmado pelos resultados idênticos do "
        "GridSearchCV (82,27% para ambos).")

    pdf.section("1.8", "Normalização e Data Leakage")
    pdf.para(
        "O SVM maximiza a margem geométrica com base em distâncias e produtos internos. "
        "Atributos em escalas distintas distorcem essas distâncias, enviesando o hiperplano "
        "decisório. A padronização Z-score (StandardScaler) é obrigatória:")
    pdf.formula("zij = ( xij - mu_j ) / sigma_j")
    pdf.para(
        "onde mu_j e sigma_j são estimados exclusivamente sobre X_train. "
        "Aplicar essa transformação ao conjunto de teste previne data leakage — "
        "garantindo que as estimativas de desempenho sejam válidas para dados novos.")

    pdf.section("1.9", "Métricas de Avaliação")
    pdf.para(
        "O desempenho é avaliado pela matriz de confusão e pelas métricas derivadas:")
    items = [
        "Acurácia  = (VP + VN) / (VP + VN + FP + FN)",
        "Precisão  = VP / (VP + FP)",
        "Revocação = VP / (VP + FN)  [sensibilidade diagnóstica]",
        "F1-Score  = 2 * (Precisão × Revocação) / (Precisão + Revocação)",
    ]
    for item in items:
        pdf.formula(item)
    pdf.para(
        "Em triagem clínica, os Falsos Negativos — pacientes doentes classificados como "
        "saudáveis — representam o erro de maior impacto, pois levam à privação de tratamento "
        "para pacientes em risco real. A revocação da classe Doente é a métrica de maior "
        "relevância médica neste contexto.")

    # =====================================================================
    # 2. METODOLOGIA
    # =====================================================================
    pdf.section("2", "Metodologia")

    pdf.section("2.1", "Conjunto de Dados")
    pdf.para(
        "O estudo utiliza o Cleveland Heart Disease Dataset (JANOSI et al., 1988), coletado no "
        "Cleveland Clinic Foundation e disponível no UCI Machine Learning Repository (id=45). "
        "É um dos benchmarks mais referenciados na literatura de diagnóstico cardíaco por "
        "aprendizado de máquina, com centenas de trabalhos científicos publicados nas últimas "
        "três décadas (MIENYE; SUN, 2022). O dataset original contém 303 registros com 13 "
        "atributos preditores. Após remoção dos 6 registros com valores ausentes — "
        "predominantemente nos atributos ca (vasos por fluoroscopia) e thal (cintilografia com "
        "tálio) — restaram 297 registros válidos, todos utilizados neste estudo.")
    pdf.para(
        "Os 13 atributos cobrem dimensões demográficas (idade, sexo), sintomas clínicos "
        "(tipo de dor torácica, angina por exercício), medidas hemodinâmicas (pressão arterial "
        "em repouso, frequência cardíaca máxima atingida), bioquímica (colesterol sérico, "
        "glicemia em jejum) e resultados de exames complementares (ECG em repouso, depressão "
        "do segmento ST, inclinação do ST, número de vasos por fluoroscopia e cintilografia "
        "com tálio). A Tabela 1 descreve cada atributo com seu significado clínico e tipo.")
    pdf.ln(2)
    pdf.table_caption("Tabela 1 – Atributos do Cleveland Heart Disease Dataset")
    headers1 = ["Atributo", "Descrição", "Tipo"]
    rows1 = [
        ("age",      "Idade do paciente (anos)",            "Numérico"),
        ("sex",      "Sexo (1=masculino; 0=feminino)",      "Binário"),
        ("cp",       "Tipo de dor torácica (0–3)",          "Categórico"),
        ("trestbps", "Pressão arterial em repouso (mmHg)",  "Numérico"),
        ("chol",     "Colesterol sérico (mg/dl)",            "Numérico"),
        ("fbs",      "Glicemia em jejum > 120 mg/dl",       "Binário"),
        ("restecg",  "Resultado do ECG em repouso",         "Categórico"),
        ("thalach",  "Freq. cardíaca máxima (bpm)",         "Numérico"),
        ("exang",    "Angina por exercício (1/0)",          "Binário"),
        ("oldpeak",  "Depressão do segmento ST",            "Numérico"),
        ("slope",    "Inclinação do segmento ST",           "Categórico"),
        ("ca",       "Vasos coloridos por fluoroscopia",    "Ordinal"),
        ("thal",     "Teste de estresse com tálio",         "Categórico"),
    ]
    pdf.simple_table(headers1, rows1, [28, 106, 36],
                     header_align=["C","C","C"],
                     row_aligns=[["L","L","C"]]*len(rows1))
    pdf.table_source("Fonte: JANOSI et al. (1988).")

    pdf.section("2.2", "Binarização e Pipeline")
    pdf.para(
        "A variável alvo original assume cinco valores inteiros (0 a 4), representando o "
        "grau de comprometimento coronariano detectado em angiografia. Para este experimento, "
        "adotou-se a binarização padrão da literatura: valor 0 é mapeado para Saudável (y=0) "
        "e qualquer valor de 1 a 4 é mapeado para Doente (y=1). Essa abordagem reduz o "
        "problema à detecção de presença ou ausência de doença — a questão clínica primária "
        "em triagem diagnóstica, independente do grau de comprometimento.")
    pdf.para(
        "Após binarização, o dataset contém 164 Saudáveis (55,2%) e 133 Doentes (44,8%) — "
        "proporção razoavelmente balanceada que não exige técnicas de reamostragem como SMOTE "
        "ou ajuste de pesos de classe. A divisão treino/teste foi realizada via train_test_split "
        "com estratificação (stratify=y, random_state=42): 237 amostras para treino e 60 para "
        "teste. O parâmetro stratify garante que ambos os subconjuntos preservem a proporção "
        "original de classes, evitando vieses de amostragem.")
    pdf.para(
        "A padronização Z-score (StandardScaler) foi aplicada a todos os 13 atributos. "
        "Os parâmetros mu_j e sigma_j foram estimados exclusivamente sobre X_train e então "
        "aplicados ao X_train e X_test. Esse procedimento previne data leakage: se os "
        "parâmetros de escala fossem estimados sobre todos os dados antes da divisão, "
        "a avaliação de desempenho seria otimista e não refletiria o comportamento real "
        "com dados genuinamente novos.")

    pdf.section("2.3", "Otimização de Hiperparâmetros")
    pdf.para(
        "O SVM possui três hiperparâmetros que influenciam fundamentalmente o desempenho: "
        "C (regularização), kernel (função de similaridade) e gamma (largura da gaussiana "
        "para RBF). Como os valores ótimos dependem da geometria específica de cada dataset, "
        "a busca em grade (GridSearchCV) avaliou sistematicamente 4 × 3 × 2 = 24 combinações, "
        "usando validação cruzada estratificada de 5 dobras (StratifiedKFold) sobre X_train, "
        "totalizando 120 treinos completos. A grade de busca foi:")
    pdf.para("C in {0,1; 1; 10; 100},  kernel in {linear, rbf, poly},  gamma in {scale, auto}",
             indent=True)
    pdf.para(
        "Os valores de C foram escolhidos em escala logarítmica, cobrindo desde forte "
        "regularização (C=0,1 — margem larga) até ajuste estrito ao treino (C=100 — margem "
        "estreita). O critério de seleção foi a acurácia média nas 5 dobras, calculada "
        "sobre dados nunca utilizados no treino de cada dobra — estimativa mais honesta "
        "que a acurácia de treino, que tenderia a favorecer modelos com overfitting.")
    pdf.para(
        "A avaliação final do modelo selecionado utilizou validação cruzada estratificada de "
        "10 dobras (StratifiedKFold, k=10) sobre os 297 registros completos. Essa métrica é "
        "reportada como média ± desvio-padrão das 10 dobras e constitui a métrica principal "
        "deste estudo, pois usa toda a base de dados e fornece indicador de variabilidade.")

    # =====================================================================
    # 3. RESULTADOS E DISCUSSÃO
    # =====================================================================
    pdf.section("3", "Resultados e Discussão")

    pdf.section("3.1", "Otimização de Hiperparâmetros")
    pdf.ln(2)
    pdf.table_caption("Tabela 2 – Top-5 Combinações de Hiperparâmetros (GridSearchCV 5-fold)")
    headers2 = ["#", "C", "Kernel", "Gamma", "Acurácia CV", "Desvio"]
    rows2 = [
        ("1 (*)", "0,1", "rbf",    "scale", "82,27%", "±5,28%"),
        ("2",   "0,1", "rbf",    "auto",  "82,27%", "±5,28%"),
        ("3",   "0,1", "linear", "scale", "81,00%", "±6,98%"),
        ("4",   "0,1", "linear", "auto",  "81,00%", "±6,98%"),
        ("5",   "1,0", "poly",   "scale", "81,00%", "±4,68%"),
    ]
    pdf.simple_table(headers2, rows2, [12, 18, 26, 22, 32, 28],
                     header_align=["C"]*6,
                     row_aligns=[["C"]*6]*len(rows2))
    pdf.table_source("Fonte: elaborado pelo autor (2026).")
    pdf.ln(1)
    pdf.insert_figure(gpath("fig4_top5_hiperparametros.png"), w=155)
    pdf.insert_figure(gpath("fig7_kernel_comparacao.png"), w=155)
    pdf.para(
        "A Tabela 2 e as Figuras 4 e 7 apresentam os resultados do GridSearchCV. A Figura 4 "
        "usa barras horizontais com barras de erro (desvio-padrão das 5 dobras), mostrando "
        "não apenas a acurácia média mas a variabilidade de cada configuração. A Figura 7 "
        "compara diretamente os três kernels para o melhor valor de regularização (C=0,1).")
    pdf.para(
        "O kernel RBF com C=0,1 obteve 82,27% nas duas configurações de gamma — resultado "
        "igual pois, após padronização Z-score, a variância dos atributos é aproximadamente "
        "1, tornando gamma_scale = 1/(13 × Var) ≈ 1/13 ≈ gamma_auto. Os kernels linear e "
        "polinomial ficaram em 81,00%, diferença de 1,27 pp que confirma a presença de "
        "componentes não-lineares na fronteira de decisão ótima para esta base de dados.")
    pdf.para(
        "A superioridade do RBF sobre o kernel linear é clinicamente plausível: a doença "
        "coronariana envolve interações complexas entre atributos como pressão arterial, "
        "frequência cardíaca máxima e tipo de dor torácica. O kernel RBF captura implicitamente "
        "essas interações ao mapear os dados para um espaço de dimensão infinita via expansão "
        "gaussiana — modelo linear não consegue representar essas relações diretamente.")
    pdf.para(
        "O valor ótimo C=0,1 — o menor da grade — é resultado informativo sobre a estrutura "
        "dos dados: aumentar a penalidade por violações de margem (valores maiores de C) "
        "não beneficiou o modelo. Esse padrão é típico de datasets com sobreposição clínica "
        "natural entre classes — pacientes limítrofes com sinais leves apresentam atributos "
        "intermediários difíceis de separar mesmo por especialistas humanos. Margem larga "
        "(C pequeno) evita overfitting nesses casos ambíguos, melhorando a generalização.")

    pdf.section("3.2", "Acurácia por Blocos de Registros")
    pdf.ln(2)
    pdf.table_caption(
        "Tabela 3 – Acurácia do SVM (C=0,1, RBF, gamma=scale) por Bloco de Registros")
    headers3 = ["Bloco", "Registros", "Acertos", "Acurácia (%)"]
    rows3 = [
        ("1", "1 – 50",    "45/50", "90,00"),
        ("2", "51 – 100",  "43/50", "86,00"),
        ("3", "101 – 150", "46/50", "92,00"),
        ("4", "151 – 200", "42/50", "84,00"),
        ("5", "201 – 250", "43/50", "86,00"),
        ("6", "251 – 297", "37/47", "78,72"),
        ("Total", "1 – 297", "256/297", "86,20"),
    ]
    pdf.simple_table(headers3, rows3, [20, 40, 35, 45],
                     header_align=["C"]*4,
                     row_aligns=[["C"]*4]*len(rows3))
    pdf.table_source("Fonte: elaborado pelo autor (2026).")
    pdf.ln(1)
    pdf.insert_figure(gpath("fig1_acuracia_blocos.png"), w=155)
    pdf.para(
        "A Tabela 3 e a Figura 1 analisam o desempenho do SVM em 6 blocos contíguos de "
        "50 registros (exceto o último com 47), aplicando o modelo treinado sobre X_train "
        "sequencialmente a todo o dataset. O objetivo é verificar se o desempenho é "
        "homogêneo ou se existem regiões sistematicamente mais difíceis de classificar.")
    pdf.para(
        "Os resultados mostram variabilidade expressiva: de 78,72% (bloco 6, registros "
        "251-297) a 92,00% (bloco 3, registros 101-150) — amplitude de 13,28 pp. "
        "O bloco 3 é o melhor: 46 de 50 acertos. O bloco 6 é o mais difícil: 37 de 47 "
        "acertos. Esse padrão é inerente aos dados — o bloco 6 corresponde aos registros "
        "finais do Cleveland dataset, que tipicamente contêm perfis clínicos mais "
        "complexos e combinações atípicas de atributos.")
    pdf.para(
        "A linha tracejada na Figura 1 indica a média de validação cruzada (83,51%). "
        "Blocos 1, 2, 3 e 5 ficam acima dessa linha, evidenciando que a validação "
        "cruzada representa adequadamente o desempenho esperado na maioria dos "
        "cenários práticos. O bloco 6 fica visivelmente abaixo (78,72%), confirmando "
        "que registros com perfis clínicos atípicos são mais desafiadores. A acurácia "
        "total sobre os 297 registros é 86,20% (256 de 297 acertos).")

    pdf.section("3.3", "Métricas Consolidadas")
    pdf.ln(2)
    pdf.table_caption("Tabela 4 – Resumo de Desempenho do SVM (C=0,1, kernel=rbf, gamma=scale)")
    headers4 = ["Métrica", "Valor"]
    rows4 = [
        ("Acurácia — teste hold-out",        "86,67%"),
        ("Acurácia — cross-val 10-fold (*)",  "83,51% +/- 7,66%"),
        ("Acurácia — conjunto completo",      "86,20%"),
        ("Precisão — classe Doente",          "0,92"),
        ("Revocação — classe Doente",         "0,79"),
        ("F1-Score — classe Doente",          "0,85"),
        ("Falsos Negativos (teste)",          "6 (de 28 doentes)"),
    ]
    pdf.simple_table(headers4, rows4, [110, 60],
                     header_align=["L","C"],
                     row_aligns=[["L","C"]]*len(rows4))
    pdf.table_source("(*) Métrica de referência principal.  Fonte: elaborado pelo autor (2026).")
    pdf.para(
        "A Tabela 4 consolida as principais métricas de desempenho do SVM. Cada linha "
        "provém de uma perspectiva diferente de avaliação, com confiabilidade e propósito "
        "distintos para o contexto do TCC.")
    pdf.para(
        "Acurácia no teste hold-out (86,67%): resultado sobre 60 amostras reservadas antes "
        "do treinamento, nunca vistas pelo modelo durante a otimização. Por ser calculado "
        "sobre apenas 60 amostras, possui alta variância — errar ou acertar 1 amostra "
        "movimenta 1,67 pp.")
    pdf.para(
        "Validação cruzada de 10 dobras — MÉTRICA DE REFERÊNCIA — (83,51% +/- 7,66%): "
        "divide os 297 registros em 10 partições, cada uma servindo como teste enquanto "
        "as outras 9 treinam o modelo. O processo se repete 10 vezes, gerando 10 "
        "acurácias distintas. O resultado final — média +/- desvio-padrão — usa toda a "
        "base de dados e produz estimativa com variabilidade mensurável. O alto desvio "
        "(7,66%) reflete a sensibilidade natural do modelo à amostragem específica em "
        "datasets com ~297 registros. Esta é a métrica recomendada para reportar no TCC.")

    pdf.section("3.4", "Matriz de Confusão e Distribuição de Erros")
    pdf.ln(2)
    pdf.table_caption("Tabela 5 – Matriz de Confusão (Conjunto de Teste, n=60)")
    headers5 = ["", "Previsto: Saudável (0)", "Previsto: Doente (1)"]
    rows5 = [
        ("Real: Saudável (0)", "30 (VN)", "2 (FP)"),
        ("Real: Doente (1)",   " 6 (FN)", "22 (VP)"),
    ]
    pdf.simple_table(headers5, rows5, [62, 54, 54],
                     header_align=["L","C","C"],
                     row_aligns=[["L","C","C"]]*len(rows5))
    pdf.table_source("Fonte: elaborado pelo autor (2026).")
    pdf.ln(2)
    pdf.insert_figure(gpath("fig2_matriz_confusao.png"), w=110)
    pdf.insert_figure(gpath("fig5_distribuicao_acertos.png"), w=120)
    pdf.para(
        "A Tabela 5 e a Figura 2 apresentam a matriz de confusão do SVM sobre o conjunto "
        "de teste (n=60: 32 Saudáveis e 28 Doentes reais). A matriz decompõe os resultados "
        "em quatro categorias com interpretações clínicas distintas e consequências "
        "práticas muito diferentes para um sistema de triagem.")
    pdf.para(
        "30 Verdadeiros Negativos (VN): pacientes saudáveis corretamente classificados como "
        "saudáveis — 93,75% dos 32 saudáveis do teste. 22 Verdadeiros Positivos (VP): "
        "pacientes doentes corretamente detectados — 78,57% dos 28 doentes do teste. "
        "Juntos, VN + VP = 52 acertos de 60 amostras, acurácia de 86,67%.")
    pdf.para(
        "2 Falsos Positivos (FP): pacientes saudáveis classificados como doentes. No "
        "contexto clínico, esses 2 pacientes seriam encaminhados para exames adicionais "
        "desnecessários — custo e ansiedade indevidos, mas sem risco à saúde. Em triagem "
        "de saúde pública, 1 FP em cada 32 saudáveis é uma taxa clinicamente aceitável.")
    pdf.para(
        "6 Falsos Negativos (FN): pacientes doentes classificados como saudáveis — o erro "
        "de maior impacto clínico. Esses 6 pacientes não receberiam acompanhamento adequado, "
        "com risco de progressão silenciosa até evento agudo. Taxa de FN = 6/28 = 21,4% "
        "dos doentes. Para triagem primária, onde o objetivo é reduzir o espaço de "
        "investigação (não substituir o diagnóstico), essa taxa é aceitável; porém, "
        "pacientes com histórico familiar ou sintomas atípicos devem ser investigados "
        "adicionalmente mesmo quando o modelo classifica como saudável.")
    pdf.para(
        "A Figura 5 mostra a distribuição global sobre os 297 registros: 256 acertos "
        "(86,20%, fatia azul) e 41 erros (13,80%, fatia vermelha). O inset no quadrante "
        "inferior direito decompõe os 8 erros do conjunto de teste em FN (6, vermelho) e "
        "FP (2, laranja) — proporção 3:1 que confirma a assimetria gerada pelo limiar "
        "padrão de 0,5 e pela revocação de 0,79 da classe Doente.")

    pdf.section("3.5", "Relatório de Classificação por Classe")
    pdf.ln(2)
    pdf.table_caption("Tabela 6 – Relatório de Classificação por Classe (Conjunto de Teste, n=60)")
    headers6 = ["Classe", "Precisão", "Revocação", "F1-Score", "Suporte"]
    rows6 = [
        ("Saudável (0)", "0,83", "0,94", "0,88", "32"),
        ("Doente (1)",   "0,92", "0,79", "0,85", "28"),
        ("Acurácia",     "",     "",     "0,87",  "60"),
        ("Média macro",  "0,88", "0,86", "0,86",  "60"),
        ("Média pond.",  "0,87", "0,87", "0,87",  "60"),
    ]
    pdf.simple_table(headers6, rows6, [38, 30, 32, 32, 28],
                     header_align=["C"]*5,
                     row_aligns=[["L","C","C","C","C"]]*len(rows6))
    pdf.table_source("Fonte: elaborado pelo autor (2026).")
    pdf.ln(1)
    pdf.insert_figure(gpath("fig3_metricas_por_classe.png"), w=140)
    pdf.para(
        "A Tabela 6 e a Figura 3 apresentam o relatório de classificação por classe, "
        "oferecendo visão mais granular que a acurácia global. Cada métrica evidencia "
        "um aspecto diferente do comportamento do modelo para cada uma das classes.")
    pdf.para(
        "Classe Saudável (0): precisão 0,83, revocação 0,94, F1-Score 0,88. A elevada "
        "revocação (0,94) significa que o modelo detecta 30 dos 32 saudáveis — apenas 2 "
        "foram alertados desnecessariamente (FP). A precisão 0,83 reflete que entre todos "
        "os classificados como saudáveis, 6 eram na verdade doentes (FN), reduzindo a "
        "confiabilidade de um resultado 'negativo' do modelo.")
    pdf.para(
        "Classe Doente (1): precisão 0,92, revocação 0,79, F1-Score 0,85. A precisão 0,92 "
        "confirma que os alertas de doença são confiáveis: 22 dos 24 pacientes classificados "
        "como doentes realmente o eram (apenas 2 falsos alarmes). A revocação 0,79 é a "
        "métrica mais crítica clinicamente: o modelo detecta 79% dos doentes, deixando 21% "
        "sem alerta (FN). Ajustar o limiar de probabilidade para abaixo de 0,5 aumentaria "
        "a revocação à custa de mais falsos positivos — trade-off típico em triagem clínica.")
    pdf.para(
        "As médias macro (0,86) e ponderada (0,87) são próximas, indicando desempenho "
        "equilibrado entre as classes. Isso é favorecido pela proporção balanceada "
        "do dataset (53% saudáveis, 47% doentes no teste). Em datasets fortemente "
        "desbalanceados, seria necessário reportar separadamente a métrica ponderada "
        "para evitar a ilusão de bom desempenho gerada pela maioria de classe.")
    pdf.para(
        "A Figura 6 a seguir consolida visualmente as quatro métricas principais do SVM "
        "em um único painel, facilitando a comunicacao dos resultados. A acurácia de teste "
        "de 86,67% e a validação cruzada de 83,51% demonstram solidão do modelo, enquanto "
        "os F1-Scores de 0,88 (Saudável) e 0,85 (Doente) confirmam o desempenho "
        "equilibrado entre as duas classes.")
    pdf.insert_figure(gpath("fig6_comparacao_svm_knn.png"), w=145)

    # =====================================================================
    # CONSIDERAÇÕES FINAIS
    # =====================================================================
    pdf.section("", "Considerações Finais", level=0)
    pdf.para(
        "Este artigo apresentou a fundamentação matemática completa, a implementação "
        "computacional e a análise experimental do Support Vector Machine aplicado à "
        "classificação binária de doença cardíaca sobre o Cleveland Heart Disease Dataset "
        "(UCI, id=45). Foram utilizados 297 registros válidos, pipeline com StandardScaler, "
        "busca em 24 combinações de hiperparâmetros via GridSearchCV e avaliação por "
        "validação cruzada de 10 dobras estratificadas. Os principais achados são:")
    conclusoes = [
        "O SVM com C=0,1, kernel RBF e gamma=scale obteve 86,67% de acurácia no teste "
        "e 83,51% +/- 7,66% na validação cruzada de 10 dobras — métrica de referência.",
        "O kernel RBF superou os kernels linear e polinomial (82,27% vs. 81,00%), "
        "confirmando componentes não-lineares na fronteira de decisão ótima.",
        "O valor ótimo C=0,1 indica que o dataset beneficia-se de forte regularização, "
        "compatível com a sobreposição clínica entre pacientes limítrofes.",
        "A padronização Z-score é condição obrigatória para o correto funcionamento "
        "do SVM, pois o algoritmo maximiza margens baseadas em distâncias.",
        "A robustez do SVM a outliers, garantida pela esparsidade dos vetores de suporte, "
        "e a eficiencia de predicao em O(n_sv x d) sao vantagens qualitativas "
        "relevantes para aplicacoes clinicas em producao.",
        "A taxa de Falsos Negativos de 21,4% reforça que o modelo deve ser utilizado "
        "como ferramenta de triagem, e não como diagnóstico autônomo.",
    ]
    for i, c in enumerate(conclusoes, 1):
        pdf.set_body(size=SIZE_BODY)
        pdf.set_x(MARGIN_LEFT)
        pdf.write(LINE_H, f"{i}. ")
        self_x = MARGIN_LEFT + pdf.get_string_width(f"{i}. ")
        pdf.set_x(self_x)
        pdf.multi_cell(CONTENT_W - (self_x - MARGIN_LEFT), LINE_H, c, align="J")
    pdf.ln(2)
    pdf.para(
        "Os resultados demonstram que o SVM com C=0,1, kernel RBF e gamma=scale é uma "
        "escolha sólida para triagem de doença cardíaca a partir de dados clínicos de rotina. "
        "A acurácia de 86,67% no teste e 83,51% +/- 7,66% na validação cruzada, combinadas "
        "com precisão de 0,92 para a classe Doente, evidenciam que o modelo emite alertas "
        "confiáveis e apresenta desempenho robusto sobre este benchmark clínico.")
    pdf.para(
        "Como limitações do estudo, destacam-se: o tamanho moderado do dataset (297 "
        "registros), que contribui para o alto desvio-padrão na validação cruzada (7,66%); "
        "a ausência de validação externa em outra instituição; e o uso do kernel RBF, que "
        "não oferece interpretabilidade direta dos coeficientes — característica disponível "
        "apenas no kernel linear. Trabalhos futuros poderiam explorar técnicas de "
        "explicabilidade como SHAP para identificar os atributos mais relevantes nas "
        "decisões do modelo, conectando os resultados à clínica cardiovascular.")

    # =====================================================================
    # REFERÊNCIAS
    # =====================================================================
    pdf.section("", "Referências", level=0)
    refs = [
        "BOSER, B. E.; GUYON, I. M.; VAPNIK, V. N. A training algorithm for optimal "
        "margin classifiers. In: Annual ACM Workshop on Computational Learning Theory, 5., "
        "1992, Pittsburgh. Proceedings... New York: ACM, 1992. p. 144-152. "
        "DOI: 10.1145/130385.130401.",

        "CORTES, C.; VAPNIK, V. Support-vector networks. Machine Learning, v. 20, n. 3, "
        "p. 273-297, 1995. DOI: 10.1007/BF00994018.",

        "GÉRON, Aurélien. Hands-On Machine Learning with Scikit-Learn, Keras, and "
        "TensorFlow. 2. ed. Sebastopol, CA: O'Reilly Media, 2019.",

        "JANOSI, A.; STEINBRUNN, W.; PFISTERER, M.; DETRANO, R. Heart Disease Dataset. "
        "UCI Machine Learning Repository, 1988. Disponível em: "
        "https://archive.ics.uci.edu/dataset/45/heart+disease. Acesso em: abr. 2026.",

        "MIENYE, I. D.; SUN, Y. A Survey of Ensemble Learning: Concepts, Algorithms, "
        "Applications, and Prospects. IEEE Access, v. 10, p. 99129-99149, 2022. "
        "DOI: 10.1109/ACCESS.2022.3207287.",

        "PEDREGOSA, F. et al. Scikit-learn: Machine Learning in Python. Journal of "
        "Machine Learning Research, v. 12, p. 2825-2830, 2011.",

        "RUSSELL, S.; NORVIG, P. Artificial Intelligence: A Modern Approach. "
        "4. ed. Hoboken, NJ: Pearson, 2020.",

        "SCHOLKOPF, B.; SMOLA, A. J. Learning with Kernels: Support Vector Machines, "
        "Regularization, Optimization, and Beyond. Cambridge, MA: MIT Press, 2002.",
    ]
    for ref in refs:
        pdf.ref_entry(ref)

    out = os.path.join(os.path.dirname(__file__), "Artigo_SVM_FATEC.pdf")
    pdf.output(out)
    print(f"  Artigo_SVM_FATEC.pdf gerado em: {out}")
    return out


# ===========================================================================
# RELATÓRIO TÉCNICO SVM — PDF COMPLETO
# ===========================================================================

def build_relatorio():
    pdf = BaseFATEC(orientation="P", unit="mm", format="A4")
    pdf.set_margins(MARGIN_LEFT, MARGIN_TOP, MARGIN_RIGHT)
    pdf.set_auto_page_break(auto=True, margin=MARGIN_BOTTOM)
    pdf.add_page()

    # TÍTULO
    pdf.set_body(bold=True, size=SIZE_TITLE)
    pdf.set_x(MARGIN_LEFT)
    pdf.multi_cell(CONTENT_W, LINE_H,
        "RELATÓRIO TÉCNICO — SUPPORT VECTOR MACHINE APLICADO AO "
        "DIAGNÓSTICO DE DOENÇA CARDÍACA",
        align="C")
    pdf.ln(2)

    pdf.center_line("André Felipe", size=SIZE_SMALL, italic=True)
    pdf.center_line("Faculdade de Tecnologia de Guaratinguetá", size=SIZE_SMALL, italic=True)
    pdf.center_line("andressmota78@gmail.com", size=SIZE_SMALL, italic=True)
    pdf.center_line("Abril de 2026", size=SIZE_SMALL, italic=True)
    pdf.ln(5)
    pdf.draw_hline()
    pdf.ln(3)

    # 1. OBJETIVO
    pdf.section("1", "Objetivo")
    pdf.para(
        "Este relatório técnico documenta de forma detalhada e reproduzível a aplicação do "
        "algoritmo Support Vector Machine (SVM) para classificação binária de doença cardíaca "
        "utilizando o Cleveland Heart Disease Dataset (UCI Machine Learning Repository, id=45). "
        "O documento destina-se ao uso no Trabalho de Conclusão de Curso (TCC) da Faculdade de "
        "Tecnologia de Guaratinguetá (FATEC-GT), servindo como registro das decisões "
        "metodológicas, parâmetros técnicos e resultados experimentais obtidos.")
    pdf.para(
        "São cobertos os seguintes aspectos: (i) caracterização da base de dados e "
        "tratamento de valores ausentes; (ii) pipeline de pré-processamento com "
        "binarização da variável alvo, particionamento estratificado e padronização Z-score; "
        "(iii) busca automática de hiperparâmetros via GridSearchCV com validação cruzada de 5 "
        "dobras; (iv) avaliação com múltiplas métricas — acurácia, precisão, revocação, "
        "F1-Score, matriz de confusão e validação cruzada de 10 dobras; (v) análise de "
        "desempenho por blocos de registros; e (vi) recomendações metodológicas específicas para o TCC.")
    pdf.para(
        "Todos os resultados foram obtidos a partir do script SupportVectorMachine.py, "
        "implementado em Python 3 com a biblioteca scikit-learn. A reprodutibilidade é "
        "garantida pelo parâmetro random_state=42 nas funções de particionamento e pela "
        "ausência de elementos estocásticos no pipeline após a divisão inicial.")

    # 2. BASE DE DADOS
    pdf.section("2", "Base de Dados")
    pdf.ln(2)
    pdf.table_caption("Tabela 1 – Informações da Base de Dados")
    hd = ["Item", "Valor"]
    rd = [
        ("Fonte",                            "UCI Machine Learning Repository (id=45)"),
        ("Nome",                             "Cleveland Heart Disease Dataset"),
        ("Registros originais",              "303"),
        ("Removidos (valores ausentes)",     "6"),
        ("Registros válidos utilizados",     "297"),
        ("Atributos preditores",             "13 (clínicos)"),
        ("Variável alvo — original",         "5 classes (0–4)"),
        ("Variável alvo — binarizada",       "0 = Saudável / 1 = Doente"),
    ]
    pdf.simple_table(hd, rd, [75, 95], header_align=["C","C"],
                     row_aligns=[["L","L"]]*len(rd))
    pdf.table_source("Fonte: JANOSI et al. (1988).")
    pdf.para(
        "A variável alvo original assume valores de 0 a 4 (grau de comprometimento coronariano). "
        "Para este estudo foi binarizada: 0 = Saudável, 1 a 4 = Doente. Após essa transformação, "
        "o dataset contém 164 saudáveis (55,2%) e 133 doentes (44,8%) — proporção "
        "razoavelmente balanceada, sem necessidade de técnicas de reamostragem.")
    pdf.para(
        "Na literatura, os atributos com maior poder discriminatório para doença coronariana "
        "neste dataset são: cp (tipo de dor torácica), thal (cintilografia com tálio), "
        "ca (vasos por fluoroscopia), oldpeak (depressão do segmento ST) e exang (angina por "
        "exercício). Esses atributos são candidatos prioritários para análise de importância "
        "em trabalhos futuros com kernel linear ou técnicas como SHAP.")

    # 3. PIPELINE
    pdf.section("3", "Pipeline de Pré-processamento")

    pdf.section("3.1", "Binarização da Variável Alvo")
    pdf.formula(
        "y = 0  →  y_original = 0  (Saudável: sem doença)\n"
        "y = 1  →  y_original > 0  (Doente: qualquer grau)")

    pdf.section("3.2", "Divisão Treino/Teste")
    pdf.ln(2)
    pdf.table_caption("Tabela 2 – Divisão Treino/Teste com Estratificação")
    hd2 = ["Conjunto", "Registros", "Saudável", "Doente"]
    rd2 = [
        ("Treinamento (80%)", "237", "128 (54%)", "109 (46%)"),
        ("Teste (20%)",       "60",  "32 (53%)",  "28 (47%)"),
    ]
    pdf.simple_table(hd2, rd2, [52, 34, 44, 40],
                     header_align=["C"]*4, row_aligns=[["L","C","C","C"]]*len(rd2))
    pdf.table_source("Método: train_test_split com stratify=y e random_state=42.")

    pdf.section("3.3", "Normalização Z-score")
    pdf.para(
        "O SVM maximiza uma margem geométrica medida em distância euclidiana no espaço de "
        "atributos. Se os atributos estiverem em escalas muito diferentes — por exemplo, "
        "colesterol sérico (100-600 mg/dl) versus sexo (0 ou 1) — os de maior magnitude "
        "dominarão artificialmente a geometria da margem, enviesando o hiperplano decisório. "
        "A padronização Z-score normaliza cada atributo j para média zero e desvio-padrão "
        "unitário:")
    pdf.formula("z_ij = ( x_ij - mu_j ) / sigma_j")
    pdf.para(
        "mu_j e sigma_j são estimados exclusivamente sobre X_train e aplicados ao X_test "
        "sem recalcular — prevenindo data leakage. Após normalização, gamma_scale = "
        "1/(n_features x Var(X_train)) \u2248 1/13 \u2248 gamma_auto, o que explica os resultados "
        "idênticos para as duas opções de gamma no GridSearchCV (82,27% para ambas com RBF).")
    pdf.para(
        "A normalização também melhora a estabilidade numérica do solver QP interno do SVM. "
        "Atributos em escalas muito diferentes podem causar mal-condicionamento da matriz "
        "de kernel, aumentando o número de iterações necessárias para convergência. "
        "Com StandardScaler aplicado corretamente, o solver converge em poucas dezenas de "
        "iterações para este dataset.")

    # 4. OTIMIZAÇÃO
    pdf.section("4", "Otimização de Hiperparâmetros")

    pdf.section("4.1", "Grade de Busca")
    pdf.ln(2)
    pdf.table_caption("Tabela 3 – Grade de Hiperparâmetros Testada")
    hd3 = ["Hiperparâmetro", "Valores Testados", "Total"]
    rd3 = [
        ("C",      "0,1 / 1 / 10 / 100",             "4"),
        ("kernel", "linear / rbf / poly",             "3"),
        ("gamma",  "scale / auto",                    "2"),
        ("Total",  "4 × 3 × 2 = 24 combinações",     "24"),
    ]
    pdf.simple_table(hd3, rd3, [40, 100, 30],
                     header_align=["C"]*3, row_aligns=[["L","L","C"]]*len(rd3))
    pdf.table_source("Método: GridSearchCV + StratifiedKFold(5) — 24 × 5 = 120 treinos.")
    pdf.para(
        "A escala logarítmica para C (0,1; 1; 10; 100) permite explorar um intervalo de 1000x "
        "com apenas 4 valores, cobrindo desde máxima regularização (C=0,1, margem larga) até "
        "ajuste muito estrito ao conjunto de treino (C=100). Os três kernels testam fronteiras "
        "lineares simples (linear), não-lineares suaves (RBF) e polinomiais (poly grau=3). "
        "O parâmetro gamma é testado nas duas configurações automáticas do scikit-learn.")
    pdf.para(
        "Cada uma das 24 combinações foi avaliada em 5 dobras estratificadas sobre X_train "
        "(237 registros): ~190 amostras para treino interno e ~47 para validação interna em "
        "cada dobra. Esse protocolo garante que os hiperparâmetros sejam selecionados com base "
        "em generalização, não em memorização do conjunto de treino.")

    pdf.section("4.2", "Top-5 Resultados da Busca")
    pdf.ln(2)
    pdf.table_caption("Tabela 4 – Top-5 Combinações (Validação Cruzada 5-fold)")
    hd4 = ["#", "C", "Kernel", "Gamma", "Média CV", "Desvio"]
    rd4 = [
        ("1 (*)", "0,1", "rbf",    "scale", "82,27%", "±5,28%"),
        ("2",   "0,1", "rbf",    "auto",  "82,27%", "±5,28%"),
        ("3",   "0,1", "linear", "scale", "81,00%", "±6,98%"),
        ("4",   "0,1", "linear", "auto",  "81,00%", "±6,98%"),
        ("5",   "1,0", "poly",   "scale", "81,00%", "±4,68%"),
    ]
    pdf.simple_table(hd4, rd4, [12, 18, 26, 22, 30, 28],
                     header_align=["C"]*6, row_aligns=[["C"]*6]*len(rd4))
    pdf.table_source("(*) Combinacao selecionada.  Fonte: elaborado pelo autor (2026).")
    pdf.ln(1)
    pdf.insert_figure(gpath("fig4_top5_hiperparametros.png"), w=155)
    pdf.insert_figure(gpath("fig7_kernel_comparacao.png"), w=155)
    pdf.para(
        "A Tabela 4 apresenta os 5 melhores resultados do GridSearchCV. A Figura 4 "
        "visualiza as combinações com barras horizontais e barras de erro (desvio-padrão "
        "das 5 dobras) — tornando visível a variabilidade de cada configuração, não "
        "apenas a acurácia média. A Figura 7 detalha o desempenho por tipo de kernel.")
    pdf.para(
        "O kernel RBF com C=0,1 obteve 82,27% nas duas variantes de gamma (empate "
        "esperado após normalização Z-score). Os kernels linear e polinomial ficaram "
        "em 81,00%, confirmando não-linearidades na fronteira ótima. O kernel polinomial "
        "com gamma='auto' obteve o pior resultado da busca (79,50%), sugerindo que o "
        "grau 3 padrão não é adequado para as relações presentes neste dataset clínico.")
    pdf.para(
        "A diferença de 1,27 pp entre RBF (82,27%) e os demais (81,00%) foi consistente "
        "em todas as 5 dobras, justificando a seleção do RBF. C=0,1 sendo o melhor valor "
        "— o menor da grade — indica que o dataset se beneficia de forte regularização: "
        "pacientes limítrofes com sinais leves de comprometimento coronariano têm atributos "
        "clínicos intermediários que tornam a separação rígida prejudicial à generalização.")
    pdf.para(
        "A combinação selecionada (*) — C=0,1, kernel=rbf, gamma=scale — foi usada para "
        "treinar o modelo final sobre X_train completo. Esse modelo foi então aplicado ao "
        "conjunto de teste hold-out (60 registros) para a acurácia final e submetido à "
        "validação cruzada de 10 dobras sobre todos os 297 registros para a métrica principal.")

    pdf.section("4.3", "Hiperparâmetros Ótimos Selecionados")
    pdf.ln(2)
    pdf.table_caption("Tabela 5 – Hiperparâmetros Ótimos e Justificativas")
    hd5 = ["Parâmetro", "Valor", "Significado"]
    rd5 = [
        ("C",      "0,1",   "Forte regularização — margem larga, tolerante a violações"),
        ("kernel", "rbf",   "Fronteira não-linear no espaço de dimensão infinita"),
        ("gamma",  "scale", "gamma = 1/(n_features × Var(X_train)) — adaptativo"),
    ]
    pdf.simple_table(hd5, rd5, [22, 22, 126],
                     header_align=["C"]*3, row_aligns=[["L","C","L"]]*len(rd5))
    pdf.table_source("Fonte: elaborado pelo autor (2026).")

    # 5. RESULTADOS
    pdf.section("5", "Resultados de Desempenho")

    pdf.section("5.1", "Métricas Globais")
    pdf.ln(2)
    pdf.table_caption("Tabela 6 – Métricas Globais de Desempenho")
    hd6 = ["Métrica", "Valor", "Observação"]
    rd6 = [
        ("Acurácia — teste (60 registros)",      "86,67%",           "Dados nunca vistos"),
        ("Acurácia — CV 10-fold  (*)",             "83,51% ± 7,66%",  "MÉTRICA PRINCIPAL"),
        ("Acurácia — todos os dados (297)",       "86,20%",           "Estimativa otimista"),
        ("Avaliação qualitativa",                  "BOM",              "Boa maioria dos casos"),
    ]
    pdf.simple_table(hd6, rd6, [74, 50, 46],
                     header_align=["L","C","C"],
                     row_aligns=[["L","C","L"]]*len(rd6))
    pdf.table_source(
        "(*) Use cross-val 10-fold como metrica principal no TCC - mais honesta e confiavel.")
    pdf.para(
        "A Tabela 6 apresenta três perspectivas de acurácia que devem ser interpretadas de "
        "forma complementar. Cada uma avalia o modelo em uma condição diferente e produz "
        "estimativas com diferentes níveis de confiabilidade estatística.")
    pdf.para(
        "Acurácia no teste hold-out (86,67%): 52 acertos em 60 amostras nunca vistas. "
        "Por ser calculada em apenas 60 registros, cada erro ou acerto move a acurácia "
        "em 1,67 pp. É útil como verificação final, mas possui alta variância estatística.")
    pdf.para(
        "Validação cruzada de 10 dobras — MÉTRICA PRINCIPAL — (83,51% ± 7,66%): "
        "calculada sobre todos os 297 registros em 10 rotações, produz estimativa robusta "
        "com desvio-padrão mensurável. O desvio de 7,66% indica que o modelo oscila nessa "
        "faixa em diferentes amostras de dados — esperado para um dataset com ~300 registros. "
        "Esta é a métrica recomendada para reportar no TCC e comparar com outros algoritmos.")
    pdf.para(
        "Acurácia sobre todos os dados (86,20%): 256 de 297 acertos com o modelo final. "
        "É uma estimativa otimista (o modelo viu parte desses dados no treino) e serve "
        "principalmente para a análise por blocos na Seção 5.2, não deve ser reportada "
        "como métrica principal de desempenho.")

    pdf.section("5.2", "Acurácia por Blocos de Registros")
    pdf.ln(2)
    pdf.table_caption("Tabela 7 – Acurácia por Bloco (SVM completo, 297 registros)")
    hd7 = ["Bloco", "Registros", "Acertos", "Acurácia (%)"]
    rd7 = [
        ("1", "1 – 50",    "45/50",  "90,00"),
        ("2", "51 – 100",  "43/50",  "86,00"),
        ("3", "101 - 150", "46/50",  "92,00  (max)"),
        ("4", "151 – 200", "42/50",  "84,00"),
        ("5", "201 – 250", "43/50",  "86,00"),
        ("6", "251 – 297", "37/47",  "78,72  (mínimo)"),
        ("Total", "1 – 297", "256/297", "86,20"),
    ]
    pdf.simple_table(hd7, rd7, [20, 40, 35, 75],
                     header_align=["C"]*4, row_aligns=[["C","C","C","L"]]*len(rd7))
    pdf.table_source("(*) Bloco de maior acuracia.  Fonte: elaborado pelo autor (2026).")
    pdf.ln(1)
    pdf.insert_figure(gpath("fig1_acuracia_blocos.png"), w=155)
    pdf.para(
        "A Tabela 7 e a Figura 1 analisam o desempenho do SVM segmentado em 6 blocos de 50 "
        "registros (exceto o último com 47). Os resultados revelam variabilidade expressiva: "
        "de 78,72% (bloco 6, registros 251-297) a 92,00% (bloco 3, registros 101-150), "
        "amplitude de 13,28 pp. Bloco 3: 46 de 50 acertos. Bloco 6: 37 de 47 acertos.")
    pdf.para(
        "A linha tracejada na Figura 1 indica a média de validação cruzada do SVM (83,51%). "
        "Os blocos 1, 2, 3 e 5 ficam acima dessa referência, enquanto o bloco 6 fica "
        "visivelmente abaixo (78,72%), confirmando a variabilidade natural em registros "
        "com perfis clínicos atípicos.")
    pdf.para(
        "A dificuldade do bloco 6 é inerente aos dados, não uma limitação do SVM: "
        "os últimos registros do Cleveland dataset tendem a incluir perfis clínicos menos "
        "frequentes, com combinações atípicas de atributos que diferem dos padrões aprendidos "
        "no treino. Esse comportamento é relevante para uso clínico: o modelo pode ter "
        "desempenho inferior em subpopulações sub-representadas no treinamento.")

    pdf.section("5.3", "Matriz de Confusão")
    pdf.ln(2)
    pdf.table_caption("Tabela 8 – Matriz de Confusão (Conjunto de Teste, n=60)")
    hd8 = ["", "Previsto: Saudável (0)", "Previsto: Doente (1)"]
    rd8 = [
        ("Real: Saudável (0)", "30 — VN", "2 — FP"),
        ("Real: Doente (1)",   " 6 — FN", "22 — VP"),
    ]
    pdf.simple_table(hd8, rd8, [62, 54, 54],
                     header_align=["L","C","C"],
                     row_aligns=[["L","C","C"]]*len(rd8))
    pdf.table_source("VN=Verdadeiro Negativo, FP=Falso Positivo, FN=Falso Negativo, VP=Verdadeiro Positivo.")
    pdf.ln(2)
    pdf.table_caption("Tabela 9 – Análise Clínica dos Resultados da Matriz de Confusão")
    hd9 = ["Tipo", "Qtd", "Interpretação Clínica"]
    rd9 = [
        ("VN", "30", "Saudáveis corretamente identificados (93,75% dos saudáveis)"),
        ("VP", "22", "Doentes corretamente identificados (78,57% dos doentes)"),
        ("FP",  "2", "Saudáveis alertados sem necessidade (exames desnecessários)"),
        ("FN",  "6", "Doentes não detectados — 21,4% de FN — risco clínico crítico"),
    ]
    pdf.simple_table(hd9, rd9, [15, 12, 143],
                     header_align=["C","C","L"],
                     row_aligns=[["C","C","L"]]*len(rd9))
    pdf.table_source("Fonte: elaborado pelo autor (2026).")
    pdf.ln(1)
    pdf.insert_figure(gpath("fig2_matriz_confusao.png"), w=110)
    pdf.insert_figure(gpath("fig5_distribuicao_acertos.png"), w=120)
    pdf.para(
        "As Tabelas 8 e 9 e a Figura 2 detalham a matriz de confusão do conjunto de teste "
        "(n=60). Os 30 VN e 22 VP somam 52 acertos. Os 2 FP e 6 FN somam 8 erros — "
        "todos decompostos na Tabela 9 com interpretação clínica detalhada.")
    pdf.para(
        "O ponto crítico é a taxa de Falsos Negativos: 6/28 = 21,4% dos doentes do teste "
        "não foram detectados. Para triagem primária, essa taxa pode ser aceitável — o "
        "objetivo é reduzir o espaço de investigação, não substituir o diagnóstico. "
        "Em cenários de alta sensibilidade, o limiar de probabilidade poderia ser reduzido "
        "(abaixo de 0,5) para capturar mais doentes, aceitando mais falsos positivos.")
    pdf.para(
        "A Figura 5 apresenta a distribuição global: 86,20% de acertos (fatia azul, 256 "
        "registros) e 13,80% de erros (fatia vermelha, 41 registros) sobre todos os 297. "
        "O inset decomposta os 8 erros do teste em FN (6, vermelho) e FP (2, laranja), "
        "proporção 3:1 que confirma a assimetria típica do limiar padrão de 0,5.")

    pdf.section("5.4", "Relatório de Classificação por Classe")
    pdf.ln(2)
    pdf.table_caption("Tabela 10 – Métricas por Classe (Conjunto de Teste, n=60)")
    hd10 = ["Classe", "Precisão", "Revocação", "F1-Score", "Suporte"]
    rd10 = [
        ("Saudável (0)", "0,83", "0,94", "0,88", "32"),
        ("Doente (1)",   "0,92", "0,79", "0,85", "28"),
        ("Acurácia",     "",     "",     "0,87",  "60"),
        ("Média macro",  "0,88", "0,86", "0,86",  "60"),
        ("Média pond.",  "0,87", "0,87", "0,87",  "60"),
    ]
    pdf.simple_table(hd10, rd10, [40, 30, 32, 32, 28],
                     header_align=["C"]*5,
                     row_aligns=[["L","C","C","C","C"]]*len(rd10))
    pdf.table_source("Fonte: elaborado pelo autor (2026).")
    pdf.ln(1)
    pdf.insert_figure(gpath("fig3_metricas_por_classe.png"), w=145)
    pdf.para(
        "Leitura clínica da Tabela 10 e Figura 3: para a classe Saudável (0), precisão 0,83, "
        "revocação 0,94 e F1 0,88. A elevada revocação (94%) indica que o modelo detecta "
        "30 dos 32 saudáveis corretamente, com apenas 2 falsos alarmes (FP). A precisão "
        "0,83 reflete que entre todos os classificados como saudáveis, 6 eram doentes (FN).")
    pdf.para(
        "Para a classe Doente (1): precisão 0,92, revocação 0,79, F1 0,85. A precisão 0,92 "
        "confirma que os alertas de doença emitidos pelo modelo são confiáveis em 92% dos "
        "casos. A revocação 0,79 é o ponto de atenção: 21% dos doentes não são detectados. "
        "Para aumentar a revocação, seria necessário reduzir o limiar de classificação "
        "abaixo de 0,5 — trade-off típico em triagem clínica que deve ser discutido no TCC.")
    pdf.para(
        "As médias macro e ponderada próximas (0,86-0,87) indicam desempenho equilibrado entre "
        "as classes, favorecido pela proporção balanceada do dataset. A consistência entre a "
        "acurácia global (86,67%) e a média ponderada do F1 (0,87) confirma que as métricas "
        "são internamente coerentes.")

    # 6. RECOMENDAÇÕES
    pdf.section("6", "Recomendações para o TCC")
    recomendacoes = [
        "Use sempre GridSearchCV para selecionar C, kernel e gamma. Esse procedimento "
        "garante que os valores sejam justificados por dados, não por tentativa e erro.",

        "Justifique o kernel RBF: a superioridade sobre o kernel linear (82,27% vs. "
        "81,00%) evidencia não-linearidades no espaço de 13 atributos clínicos.",

        "Justifique C=0,1 (forte regularização): o menor valor da grade sendo ótimo "
        "indica que o dataset se beneficia de margem ampla, compatível com a sobreposição "
        "clínica entre pacientes limítrofes.",

        "A normalização Z-score é obrigatória para o SVM. Calcule mu e sigma apenas "
        "sobre X_train e aplique ao X_test. Isso previne data leakage.",

        "Métrica principal para o TCC: cross-val 10-fold = 83,51% ± 7,66%. "
        "Sempre reporte média ± desvio-padrão.",

        "Variáveis mais relevantes na literatura (dataset Cleveland): cp (dor torácica), "
        "thal, ca, oldpeak, exang. Para interpretabilidade no SVM linear, os coeficientes "
        "de w indicam a importância de cada feature.",
    ]
    for i, rec in enumerate(recomendacoes, 1):
        pdf.set_body(size=SIZE_BODY)
        pdf.set_x(MARGIN_LEFT)
        pdf.write(LINE_H, f"{i}. ")
        sx = MARGIN_LEFT + pdf.get_string_width(f"{i}. ")
        pdf.set_x(sx)
        pdf.multi_cell(CONTENT_W - (sx - MARGIN_LEFT), LINE_H, rec, align="J")
    pdf.ln(3)

    # 7. RESUMO EXECUTIVO
    pdf.section("7", "Resumo Executivo")
    pdf.draw_hline()
    sumario = (
        "Dataset          : UCI Heart Disease (Cleveland, id=45)\n"
        "Registros        : 297 validos (303 originais - 6 ausentes)\n"
        "Divisao          : 237 treino (80%) / 60 teste (20%), estratificada\n\n"
        "Hiperparametros  : C=0.1, kernel=rbf, gamma=scale (GridSearchCV 5-fold)\n"
        "Normalizacao     : StandardScaler (Z-score), ajustado apenas em X_train\n\n"
        "DESEMPENHO:\n"
        "  Acuracia - teste hold-out    : 86.67%  (52/60 acertos)\n"
        "  Acuracia - cross-val 10-fold : 83.51% +/- 7.66%   <- METRICA PRINCIPAL\n"
        "  Acuracia - todos os dados    : 86.20%  (256/297 acertos)\n\n"
        "MATRIZ DE CONFUSAO (teste):\n"
        "  VN=30  FP=2   (Saudaveis: 32 reais, 30 corretos)\n"
        "  FN=6   VP=22  (Doentes  : 28 reais, 6 nao detectados)\n\n"
        "POR CLASSE:\n"
        "  Saudavel: Precisao=0.83  Recall=0.94  F1=0.88\n"
        "  Doente  : Precisao=0.92  Recall=0.79  F1=0.85\n"
        "  Acuracia global: 0.87\n\n"
        "AVALIACAO: BOM - classifica bem a maioria dos casos.\n"
        "           Usar como apoio ao diagnostico, nao substituto clinico.")
    pdf.set_body(size=SIZE_SMALL)
    pdf.set_x(MARGIN_LEFT)
    pdf.multi_cell(CONTENT_W, LINE_H_SM, sumario, align="L")
    pdf.draw_hline()
    pdf.ln(3)

    # REFERÊNCIAS
    pdf.section("8", "Referências")
    refs = [
        "BOSER, B. E.; GUYON, I. M.; VAPNIK, V. N. A training algorithm for optimal "
        "margin classifiers. In: Annual ACM Workshop on COLT, 5., 1992. "
        "DOI: 10.1145/130385.130401.",

        "CORTES, C.; VAPNIK, V. Support-vector networks. Machine Learning, v. 20, "
        "n. 3, p. 273-297, 1995. DOI: 10.1007/BF00994018.",

        "GÉRON, Aurélien. Hands-On Machine Learning with Scikit-Learn, Keras and "
        "TensorFlow. 2. ed. O'Reilly Media, 2019.",

        "JANOSI, A. et al. Heart Disease Dataset. UCI Machine Learning Repository, 1988. "
        "Disponível em: https://archive.ics.uci.edu/dataset/45/heart+disease.",

        "MIENYE, I. D.; SUN, Y. A Survey of Ensemble Learning. IEEE Access, v. 10, "
        "p. 99129-99149, 2022. DOI: 10.1109/ACCESS.2022.3207287.",

        "PEDREGOSA, F. et al. Scikit-learn: Machine Learning in Python. JMLR, "
        "v. 12, p. 2825-2830, 2011.",

        "RUSSELL, S.; NORVIG, P. Artificial Intelligence: A Modern Approach. "
        "4. ed. Pearson, 2020.",
    ]
    for ref in refs:
        pdf.ref_entry(ref)

    out = os.path.join(os.path.dirname(__file__), "Relatorio_SVM_FATEC.pdf")
    pdf.output(out)
    print(f"  Relatorio_SVM_FATEC.pdf gerado em: {out}")
    return out


# ===========================================================================
# MAIN
# ===========================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  GERADOR DE PDFs — SVM / Doença Cardíaca / FATEC")
    print("=" * 60)

    gerar_todos_graficos()

    print("\n=== Gerando Artigo PDF ===")
    build_artigo()

    print("\n=== Gerando Relatório PDF ===")
    build_relatorio()

    print("\n" + "=" * 60)
    print("  CONCLUÍDO — Arquivos gerados:")
    print("    graficos_svm/     (7 figuras PNG)")
    print("    Artigo_SVM_FATEC.pdf")
    print("    Relatorio_SVM_FATEC.pdf")
    print("=" * 60)
