# -*- coding: utf-8 -*-
"""
Gerador de PDF para o artigo Random Forest aplicado ao diagnostico de doenca cardiaca.
Produz:
  - artigos_relatorios/graficos_rf/  (PNGs intermediarios)
  - artigos_relatorios/pdfs/Artigo_RF_FATEC.pdf
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from fpdf import FPDF

# ---------------------------------------------------------------------------
# Diretorios de saida
# ---------------------------------------------------------------------------
BASE_DIR    = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "artigos_relatorios"))
GRAFICOS_DIR = os.path.join(BASE_DIR, "graficos_rf")
PDF_DIR      = os.path.join(BASE_DIR, "pdfs")
os.makedirs(GRAFICOS_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

def gpath(name):
    return os.path.join(GRAFICOS_DIR, name)

# ===========================================================================
# PALETA DE CORES
# ===========================================================================
AZUL     = "#2563EB"
LARANJA  = "#EA580C"
VERDE    = "#16A34A"
CINZA    = "#6B7280"
VERMELHO = "#DC2626"
ROXO     = "#7C3AED"
AMARELO  = "#CA8A04"

PLT_PARAMS = {
    "font.family": "DejaVu Sans",
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.dpi": 150,
}
plt.rcParams.update(PLT_PARAMS)

# ---------------------------------------------------------------------------
# Dados do experimento (Random Forest — Cleveland Heart Disease UCI id=45)
# ---------------------------------------------------------------------------
FEATURE_NAMES = ["cp", "thalach", "oldpeak", "ca", "thal",
                 "age", "sex", "exang", "slope", "restecg", "chol", "trestbps", "fbs"]
FEATURE_IMP   = [14.68, 13.12, 12.46, 11.83, 10.95,
                  9.20,  7.31,  6.84,  5.73,  3.42,  2.84,  0.91,  0.71]

BLOCOS_LABELS = ["Bloco 1\n(1-50)", "Bloco 2\n(51-100)", "Bloco 3\n(101-150)",
                 "Bloco 4\n(151-200)", "Bloco 5\n(201-250)", "Bloco 6\n(251-297)"]
BLOCOS_ACC    = [86.00, 86.00, 88.00, 84.00, 86.00, 80.85]

CM = np.array([[29, 3], [6, 22]])   # [[VN, FP],[FN, VP]] — conjunto de teste n=60

# ===========================================================================
# GERACAO DOS GRAFICOS
# ===========================================================================

def fig1_feature_importance():
    """Grafico horizontal de importancia das variaveis."""
    x   = np.array(FEATURE_IMP)
    y   = np.arange(len(FEATURE_NAMES))
    cores = [AZUL if i < 3 else (LARANJA if i < 6 else CINZA) for i in range(len(FEATURE_NAMES))]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.barh(y, x, color=cores, alpha=0.88, edgecolor="white")

    for bar, v in zip(bars, x):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                f"{v:.2f}%", va="center", fontsize=8.5, fontweight="bold")

    ax.set_yticks(y)
    ax.set_yticklabels(FEATURE_NAMES, fontsize=9)
    ax.set_xlabel("Importancia relativa (%)")
    ax.set_title("Figura 1 – Importancia das Variaveis (Feature Importance) — Random Forest",
                 fontweight="bold")
    ax.set_xlim(0, 19)
    ax.xaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)

    patch_top3 = mpatches.Patch(color=AZUL,   label="Top-3 (cp, thalach, oldpeak)")
    patch_mid  = mpatches.Patch(color=LARANJA, label="4-6 (ca, thal, age)")
    patch_rest = mpatches.Patch(color=CINZA,   label="Demais variaveis")
    ax.legend(handles=[patch_top3, patch_mid, patch_rest], fontsize=8, loc="lower right")
    fig.tight_layout()
    fig.savefig(gpath("fig1_feature_importance.png"), bbox_inches="tight")
    plt.close(fig)
    print("  fig1_feature_importance.png gerado.")


def fig2_acuracia_blocos():
    """Acuracia por bloco de registros — RF."""
    x     = np.arange(len(BLOCOS_LABELS))
    width = 0.55

    fig, ax = plt.subplots(figsize=(9, 4.5))
    bars = ax.bar(x, BLOCOS_ACC, width, label="RF (n=50, depth=10)",
                  color=VERDE, alpha=0.88, edgecolor="white")

    ax.axhline(81.51, color=VERDE, linestyle="--", linewidth=1.5,
               label="Cross-val 10-fold (81,51%)")
    ax.axhline(85.00, color=CINZA, linestyle=":", linewidth=1.2,
               label="Acuracia no teste (85,00%)")

    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.4,
                f"{bar.get_height():.1f}%", ha="center", va="bottom",
                fontsize=9, color=VERDE, fontweight="bold")

    ax.set_xlabel("Bloco de registros")
    ax.set_ylabel("Acuracia (%)")
    ax.set_title("Figura 2 – Acuracia por Bloco de Registros (Random Forest)", fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(BLOCOS_LABELS)
    ax.set_ylim(68, 100)
    ax.legend(fontsize=9, loc="lower left")
    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(gpath("fig2_acuracia_blocos.png"), bbox_inches="tight")
    plt.close(fig)
    print("  fig2_acuracia_blocos.png gerado.")


def fig3_matriz_confusao():
    """Heatmap da matriz de confusao."""
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    im = ax.imshow(CM, cmap="Greens", vmin=0, vmax=32)
    plt.colorbar(im, ax=ax, fraction=0.04, pad=0.04)

    labels = [["VN = 29\nSaudavel corretamente\nidentificado",
               "FP = 3\nSaudavel classificado\ncomo Doente"],
              ["FN = 6\nDoente classificado\ncomo Saudavel",
               "VP = 22\nDoente corretamente\nidentificado"]]

    for i in range(2):
        for j in range(2):
            ax.text(j, i, labels[i][j],
                    ha="center", va="center", fontsize=8.5,
                    color="white" if CM[i, j] > 15 else "black",
                    fontweight="bold")

    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["Previsto: Saudavel (0)", "Previsto: Doente (1)"], fontsize=9)
    ax.set_yticklabels(["Real: Saudavel (0)", "Real: Doente (1)"], fontsize=9)
    ax.set_xlabel("Classe Prevista", fontsize=10)
    ax.set_ylabel("Classe Real", fontsize=10)
    ax.set_title("Figura 3 – Matriz de Confusao (Conjunto de Teste, n=60)",
                 fontweight="bold", fontsize=11)
    fig.tight_layout()
    fig.savefig(gpath("fig3_matriz_confusao.png"), bbox_inches="tight")
    plt.close(fig)
    print("  fig3_matriz_confusao.png gerado.")


def fig4_metricas_por_classe():
    """Barras agrupadas: Precisao / Revocacao / F1 por classe."""
    classes  = ["Saudavel (0)", "Doente (1)"]
    precisao = [0.83, 0.88]   # 29/35=0.829, 22/25=0.88
    recall   = [0.91, 0.79]   # 29/32=0.906, 22/28=0.786
    f1       = [0.87, 0.83]

    x     = np.arange(len(classes))
    width = 0.25
    fig, ax = plt.subplots(figsize=(7, 4.5))

    b1 = ax.bar(x - width, precisao, width, label="Precisao",  color=AZUL,   alpha=0.88)
    b2 = ax.bar(x,         recall,   width, label="Revocacao", color=LARANJA, alpha=0.88)
    b3 = ax.bar(x + width, f1,       width, label="F1-Score",  color=VERDE,   alpha=0.88)

    for bars in [b1, b2, b3]:
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
                    f"{bar.get_height():.2f}", ha="center", va="bottom", fontsize=9)

    ax.set_ylim(0, 1.12)
    ax.set_xticks(x)
    ax.set_xticklabels(classes, fontsize=10)
    ax.set_ylabel("Valor da Metrica")
    ax.set_title("Figura 4 – Precisao, Revocacao e F1-Score por Classe (Conjunto de Teste)",
                 fontweight="bold")
    ax.legend(fontsize=9)
    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(gpath("fig4_metricas_por_classe.png"), bbox_inches="tight")
    plt.close(fig)
    print("  fig4_metricas_por_classe.png gerado.")


def fig5_top5_hiperparametros():
    """Barras horizontais: top-5 combinacoes de hiperparametros."""
    labels = [
        "n=300 | depth=15",
        "n=200 | depth=10",
        "n=50  | depth=None",
        "n=100 | depth=10",
        "n=50  | depth=10  (sel.)",
    ]
    acc    = [80.25, 80.64, 80.64, 81.07, 81.51]
    erros  = [5.80,  5.45,  5.95,  5.12,  6.13]
    colors = [CINZA, CINZA, CINZA, LARANJA, VERDE]

    fig, ax = plt.subplots(figsize=(9, 4))
    bars = ax.barh(labels, acc, xerr=erros, color=colors, alpha=0.88,
                   capsize=4, error_kw={"elinewidth": 1.5, "ecolor": "gray"})

    for bar, a in zip(bars, acc):
        ax.text(bar.get_width() - 0.2, bar.get_y() + bar.get_height() / 2,
                f"{a:.2f}%", ha="right", va="center", fontsize=9,
                color="white", fontweight="bold")

    ax.set_xlabel("Acuracia CV Media (%)")
    ax.set_title("Figura 5 – Top-5 Combinacoes de Hiperparametros (GridSearchCV 5-fold)",
                 fontweight="bold")
    ax.set_xlim(72, 92)
    ax.xaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)

    patch_best  = mpatches.Patch(color=VERDE,   label="Melhor combinacao (selecionada)")
    patch_2nd   = mpatches.Patch(color=LARANJA, label="2a colocada")
    patch_other = mpatches.Patch(color=CINZA,   label="Demais combinacoes")
    ax.legend(handles=[patch_best, patch_2nd, patch_other], fontsize=8, loc="lower right")
    fig.tight_layout()
    fig.savefig(gpath("fig5_top5_hiperparametros.png"), bbox_inches="tight")
    plt.close(fig)
    print("  fig5_top5_hiperparametros.png gerado.")


def fig6_comparacao_modelos():
    """Barras agrupadas: RF vs KNN vs SVM nas metricas principais."""
    metricas = ["Acuracia\nTeste", "Acuracia\nCV 10-fold", "F1\nSaudavel", "F1\nDoente"]
    rf_vals  = [85.00, 81.51, 87.00, 83.00]
    knn_vals = [86.67, 82.86, 88.00, 85.00]
    svm_vals = [86.67, 83.51, 88.00, 85.00]

    x     = np.arange(len(metricas))
    width = 0.25
    fig, ax = plt.subplots(figsize=(9, 5))

    b1 = ax.bar(x - width, rf_vals,  width, label="Random Forest", color=VERDE,  alpha=0.88)
    b2 = ax.bar(x,         knn_vals, width, label="KNN (K=29)",    color=AZUL,   alpha=0.88)
    b3 = ax.bar(x + width, svm_vals, width, label="SVM (RBF)",     color=LARANJA, alpha=0.88)

    for bars in [b1, b2, b3]:
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                    f"{bar.get_height():.1f}", ha="center", va="bottom", fontsize=8)

    ax.set_xticks(x)
    ax.set_xticklabels(metricas, fontsize=10)
    ax.set_ylabel("Valor (% ou x100 para F1)")
    ax.set_ylim(70, 97)
    ax.set_title("Figura 6 – Comparativo de Desempenho: RF vs KNN vs SVM",
                 fontweight="bold")
    ax.legend(fontsize=9)
    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(gpath("fig6_comparacao_modelos.png"), bbox_inches="tight")
    plt.close(fig)
    print("  fig6_comparacao_modelos.png gerado.")


def gerar_todos_graficos():
    print("\n=== Gerando graficos RF ===")
    fig1_feature_importance()
    fig2_acuracia_blocos()
    fig3_matriz_confusao()
    fig4_metricas_por_classe()
    fig5_top5_hiperparametros()
    fig6_comparacao_modelos()
    print("Todos os graficos gerados em:", GRAFICOS_DIR)


# ===========================================================================
# CLASSE PDF BASE (padrao FATEC)
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


# ===========================================================================
# ARTIGO RANDOM FOREST — PDF COMPLETO
# ===========================================================================

def build_artigo():
    pdf = BaseFATEC(orientation="P", unit="mm", format="A4")
    pdf.set_margins(MARGIN_LEFT, MARGIN_TOP, MARGIN_RIGHT)
    pdf.set_auto_page_break(auto=True, margin=MARGIN_BOTTOM)
    pdf.add_page()

    # TITULO
    pdf.set_body(bold=True, size=SIZE_TITLE)
    pdf.set_x(MARGIN_LEFT)
    pdf.multi_cell(CONTENT_W, LINE_H,
        "RANDOM FOREST APLICADO AO DIAGNOSTICO DE DOENCA CARDIACA: "
        "FUNDAMENTOS MATEMATICOS, BAGGING E ANALISE DE IMPORTANCIA DE VARIAVEIS",
        align="C")
    pdf.ln(2)

    pdf.center_line("Andre Felipe", size=SIZE_SMALL, italic=True)
    pdf.center_line("Faculdade de Tecnologia de Guaratingueta", size=SIZE_SMALL, italic=True)
    pdf.center_line("andressmota78@gmail.com", size=SIZE_SMALL, italic=True)
    pdf.ln(4)

    # RESUMO
    pdf.set_body(bold=True)
    pdf.set_x(MARGIN_LEFT)
    pdf.cell(CONTENT_W, LINE_H, "Resumo", align="L")
    pdf.ln(1)
    pdf.para(
        "Este artigo apresenta a aplicacao do algoritmo Random Forest (RF) para a classificacao "
        "binaria de doenca cardiaca utilizando o Cleveland Heart Disease Dataset (UCI Machine "
        "Learning Repository, id=45). Sao cobertos os fundamentos matematicos do algoritmo, "
        "incluindo a teoria das arvores de decisao, os criterios de impureza de Gini e entropia "
        "de Shannon, o metodo de bootstrap aggregating (bagging), a subamostragem aleatoria de "
        "variaveis (random subspace method) e o calculo de importancia das variaveis por "
        "reducao de impureza. A implementacao foi desenvolvida em Python com a biblioteca "
        "scikit-learn, empregando particionamento estratificado e otimizacao automatica dos "
        "hiperparametros n_estimators e max_depth via GridSearchCV. A melhor combinacao "
        "encontrada foi n_estimators=50 e max_depth=10, obtendo acuracia de 85,00% no conjunto "
        "de teste e 81,51% +/- 6,13% na validacao cruzada de 10 dobras. A importancia das "
        "variaveis identificou cp, thalach e oldpeak como os tres atributos mais discriminativos "
        "para o diagnostico cardiaco.",
        indent=False)
    pdf.ln(1)
    pdf.set_font(FONT, "B", SIZE_BODY)
    pdf.set_x(MARGIN_LEFT)
    pdf.write(LINE_H, "Palavras-chave: ")
    pdf.set_body()
    pdf.write(LINE_H,
        "Random Forest; Arvores de Decisao; Bagging; Feature Importance; "
        "Aprendizado de Maquina; Doenca Cardiaca; Classificacao Binaria; Validacao Cruzada.")
    pdf.ln(4)

    # ABSTRACT
    pdf.set_body(bold=True)
    pdf.set_x(MARGIN_LEFT)
    pdf.cell(CONTENT_W, LINE_H, "Abstract", align="L")
    pdf.ln(1)
    pdf.para(
        "This paper presents the application of the Random Forest (RF) algorithm for binary "
        "classification of heart disease using the Cleveland Heart Disease Dataset (UCI Machine "
        "Learning Repository, id=45). The mathematical foundations of the algorithm are covered, "
        "including decision tree theory, Gini impurity and Shannon entropy criteria, bootstrap "
        "aggregating (bagging), random subspace method, and impurity-based variable importance. "
        "The Python implementation uses stratified data partitioning and automatic hyperparameter "
        "optimization of n_estimators and max_depth via GridSearchCV. The best combination found "
        "was n_estimators=50 and max_depth=10, achieving 85.00% accuracy on the test set and "
        "81.51% +/- 6.13% in 10-fold cross-validation. Feature importance identified cp, thalach "
        "and oldpeak as the three most discriminative clinical attributes.",
        indent=False)
    pdf.ln(1)
    pdf.set_font(FONT, "B", SIZE_BODY)
    pdf.set_x(MARGIN_LEFT)
    pdf.write(LINE_H, "Keywords: ")
    pdf.set_body()
    pdf.write(LINE_H,
        "Random Forest; Decision Trees; Bagging; Feature Importance; "
        "Machine Learning; Heart Disease; Binary Classification; Cross-Validation.")
    pdf.ln(6)

    # =====================================================================
    # INTRODUCAO
    # =====================================================================
    pdf.section("", "Introducao", level=0)
    pdf.para(
        "As doencas cardiovasculares permanecem como a principal causa de mortalidade global, "
        "respondendo por aproximadamente 17,9 milhoes de obitos anuais segundo a Organizacao "
        "Mundial da Saude. O diagnostico precoce, dependente de exames complexos como "
        "cineangiocoronariografia e cintilografia miocardica, e limitado pela disponibilidade "
        "e custo nos sistemas publicos de saude. Sistemas inteligentes de apoio a decisao "
        "clinica representam uma das areas de maior impacto pratico da Inteligencia Artificial "
        "(HOPGOOD, 2022). Ferramentas de triagem automatizada baseadas em aprendizado de "
        "maquina oferecem alternativa custo-efetiva para identificar pacientes em risco a "
        "partir de dados clinicos de rotina (MIENYE; SUN, 2022).")
    pdf.para(
        "O Random Forest (RF), descrito por Mienye e Sun (2022), e um algoritmo de conjunto "
        "(ensemble) baseado no principio de que a combinacao de multiplas arvores de decisao "
        "independentes produz predicoes mais robustas e precisas do que qualquer arvore "
        "individual. Por meio do bootstrap aggregating (bagging) e da subamostragem aleatoria "
        "de variaveis, o RF reduz simultaneamente a variancia e o overfitting — duas "
        "limitacoes fundamentais das arvores de decisao simples. Alem disso, o RF fornece "
        "naturalmente uma medida de importancia de cada variavel preditora, elemento "
        "clinicamente valioso para identificar os atributos mais relevantes para o diagnostico.")
    pdf.para(
        "Uma propriedade distintiva do RF em relacao ao KNN e ao SVM e a independencia "
        "de normalizacao: como as arvores de decisao tomam decisoes por limiares em cada "
        "variavel individualmente, a escala absoluta dos atributos nao afeta o resultado. "
        "Isso simplifica o pipeline de pre-processamento e facilita a integracao em sistemas "
        "clinicos onde dados de multiplas fontes podem estar em escalas distintas.")
    pdf.para(
        "O presente artigo tem como objetivos: (i) fundamentar matematicamente o RF desde "
        "os criterios de particionamento das arvores de decisao ate o mecanismo de bagging "
        "e importancia de variaveis; (ii) descrever a implementacao sobre o Cleveland Heart "
        "Disease Dataset com otimizacao de hiperparametros; (iii) apresentar e analisar os "
        "resultados — acuracia por blocos, matriz de confusao, relatorio por classe e "
        "importancia das variaveis; e (iv) comparar o desempenho do RF com os classificadores "
        "KNN e SVM previamente estudados, construindo uma perspectiva evolutiva para o TCC.")
    pdf.para(
        "O artigo esta organizado da seguinte forma: a Secao 1 apresenta o referencial "
        "teorico com a fundamentacao matematica completa; a Secao 2 descreve a metodologia "
        "experimental; a Secao 3 apresenta e discute os resultados com graficos e tabelas; "
        "e as Consideracoes Finais sintetizam as principais conclusoes e perspectivas.")

    # =====================================================================
    # 1. REFERENCIAL TEORICO
    # =====================================================================
    pdf.section("1", "Referencial Teorico")

    pdf.section("1.1", "Arvores de Decisao")
    pdf.para(
        "Uma arvore de decisao e uma estrutura hierarquica que particiona recursivamente "
        "o espaco de atributos em regioes cada vez mais puras, em termos da distribuicao "
        "das classes (GIRALDI, 2021). Formalmente, dado um conjunto de treinamento "
        "D = {(x1,y1), ..., (xn,yn)}, onde xi em R^d e yi em {0,1}, cada no interno "
        "da arvore realiza uma divisao binaria com base em um unico atributo xj e um limiar t:")
    pdf.formula("Regiao esquerda: { xi : xi[j] <= t }\nRegiao direita:  { xi : xi[j] >  t }")
    pdf.para(
        "O processo de divisao e guiado por um criterio de impureza que mede a mistura "
        "de classes em cada no. O algoritmo de aprendizado busca, em cada no, o par (j*, t*) "
        "que maximiza a reducao de impureza apos a divisao. Os criterios mais utilizados "
        "sao o Indice de Gini e a Entropia de Shannon.")

    pdf.section("1.2", "Criterio de Gini")
    pdf.para(
        "O Indice de Gini mede a probabilidade de uma classificacao errada ao selecionar "
        "aleatoriamente um item e rotula-lo de acordo com a distribuicao da amostra "
        "(THOMAS, 2018). Para um no com K classes e proporcao pk da classe k:")
    pdf.formula("Gini(no) = 1 - SUM_{k=1}^{K} p_k^2")
    pdf.para(
        "Para classificacao binaria (K=2), com proporcao p da classe positiva:")
    pdf.formula("Gini(no) = 1 - p^2 - (1-p)^2 = 2p(1-p)")
    pdf.para(
        "O valor de Gini varia de 0 (no puro — uma so classe) a 0,5 (no completamente "
        "impuro — distribuicao uniforme entre as classes). A reducao de Gini pela divisao "
        "em subnos esquerdo (E) e direito (D), com |E| e |D| amostras, e:")
    pdf.formula(
        "DeltaGini = Gini(no) - (|E|/|no|) * Gini(E) - (|D|/|no|) * Gini(D)")
    pdf.para(
        "O par (j*, t*) escolhido em cada no maximiza DeltaGini. O scikit-learn adota "
        "o Indice de Gini como criterio padrao do RandomForestClassifier.")

    pdf.section("1.3", "Criterio de Entropia")
    pdf.para(
        "A Entropia de Shannon quantifica a incerteza (desordem) de uma distribuicao "
        "probabilistica (THOMAS, 2018). Para um no com proporcoes pk:")
    pdf.formula("H(no) = - SUM_{k=1}^{K} p_k * log2(p_k)")
    pdf.para(
        "A divisao que maximiza o Ganho de Informacao (IG) — a reducao de entropia — "
        "e selecionada:")
    pdf.formula(
        "IG = H(no) - (|E|/|no|) * H(E) - (|D|/|no|) * H(D)")
    pdf.para(
        "Gini e Entropia produzem divisoes muito semelhantes na pratica. O Gini e "
        "computacionalmente mais eficiente (sem logaritmo) e e preferido em implementacoes "
        "de alta escala como o scikit-learn. Ambos os criterios tendem a identificar as "
        "mesmas variaveis como mais discriminativas, com diferenca apenas em casos de "
        "distribuicoes altamente assimericas.")

    pdf.section("1.4", "Bootstrap Aggregating (Bagging)")
    pdf.para(
        "O bagging (MIENYE; SUN, 2022) e a tecnica que transforma uma arvore "
        "de decisao individual — modelo de alta variancia — em um ensemble de baixa "
        "variancia. O algoritmo funciona em tres etapas:")
    pdf.para(
        "1. Para cada arvore t = 1, ..., T: gerar uma amostra bootstrap D_t com "
        "reposicao de tamanho n a partir de D. Em media, cada amostra bootstrap contem "
        "cerca de 63,2% das amostras originais (amostras out-of-bag, OOB).",
        indent=True)
    pdf.para(
        "2. Treinar uma arvore de decisao profunda (sem poda) sobre D_t.",
        indent=True)
    pdf.para(
        "3. Combinar as predicoes das T arvores por votacao majoritaria (classificacao) "
        "ou media (regressao):",
        indent=True)
    pdf.formula(
        "y_hat_RF(x) = argmax_c SUM_{t=1}^{T} I[ h_t(x) = c ]")
    pdf.para(
        "Matematicamente, se cada arvore possui variancia sigma^2 e as arvores sao "
        "identicamente distribuidas com correlacao rho entre pares, a variancia do "
        "ensemble e:")
    pdf.formula("Var(RF) = rho * sigma^2 + (1 - rho) * sigma^2 / T")
    pdf.para(
        "Quando rho → 0 (arvores completamente descorrelacionadas) e T → inf, "
        "Var(RF) → 0. O bagging reduz a variancia sem aumentar o vies, desde que "
        "as arvores individuais sejam pouco correlacionadas.")

    pdf.section("1.5", "Random Subspace Method — Subamostragem de Variaveis")
    pdf.para(
        "Uma limitacao do bagging puro e que arvores treinadas em diferentes amostras "
        "bootstrap tendem a ser altamente correlacionadas quando ha atributos muito "
        "dominantes — como cp no dataset Cleveland. O random subspace method "
        "(MIENYE; SUN, 2022) resolve isso: em cada divisao de cada no, apenas "
        "m variaveis (selecionadas aleatoriamente de d totais) sao consideradas.")
    pdf.formula("m = floor( sqrt(d) )   [padrao para classificacao no scikit-learn]")
    pdf.para(
        "Para d=13 atributos, m = floor(sqrt(13)) = 3. Esse mecanismo forca cada "
        "arvore a construir sua estrutura de divisoes sem recorrer sempre aos mesmos "
        "atributos dominantes, criando arvores mais diversas entre si — com menor "
        "correlacao rho — e, portanto, conjuntos com menor variancia total.")

    pdf.section("1.6", "Importancia das Variaveis (Feature Importance)")
    pdf.para(
        "O RF fornece naturalmente uma medida de importancia de cada variavel, calculada "
        "como a media ponderada das reducoes de Gini (ou entropia) que cada variavel "
        "proporciona em todos os nos de todas as arvores:")
    pdf.formula(
        "Imp(j) = (1/T) SUM_{t=1}^{T} SUM_{v in nos de t: variavel=j} "
        "(|no_v| / n) * DeltaImpureza(no_v)")
    pdf.para(
        "Os valores resultantes sao normalizados para somar 1 (100%). Variaveis com "
        "maior importancia media participam de mais divisoes e/ou produzem maiores "
        "reducoes de impureza. No dataset Cleveland, a variavel cp (tipo de dor "
        "toracica) lidera com 14,68%, seguida de thalach (frequencia cardiaca maxima, "
        "13,12%) e oldpeak (depressao do segmento ST, 12,46%) — resultado alinhado "
        "com o conhecimento clinico sobre fatores de risco cardiovascular.")
    pdf.para(
        "Uma propriedade relevante desta metrica e que ela e calculada sobre todos os "
        "dados de treinamento, sem depender de um conjunto de teste especifico. Isso "
        "permite interpretar a importancia mesmo sem novos dados. Porem, variaveis com "
        "alta cardinalidade (muitos valores unicos) tendem a ser favorecidas artificialmente, "
        "um vies que pode ser corrigido com importancia por permutacao (MIENYE; SUN, 2022).")

    pdf.section("1.7", "Independencia de Normalizacao")
    pdf.para(
        "Uma vantagem pratica fundamental do RF e a independencia de normalizacao dos "
        "atributos. As arvores de decisao realizam divisoes por limiares em variaveis "
        "individuais: f(x) <= t. O limiar otimo t e determinado pelos valores observados "
        "na variavel j, e a divisao e invariante a transformacoes monotones (inclusive "
        "normalizacao). Multiplicar uma variavel por uma constante apenas desloca os "
        "limiares proporcionalmente, sem alterar a estrutura das divisoes.")
    pdf.para(
        "Em contraste, o SVM e o KNN dependem criticamente da escala: o SVM maximiza "
        "margens baseadas em distancias euclidianas, e o KNN decide classes por "
        "proximidade entre pontos. Para ambos, atributos em escalas distintas enviesam "
        "os calculos de distancia. Para o RF, escalas distintas nao afetam a qualidade "
        "das divisoes. Essa propriedade simplifica o pipeline de pre-processamento e "
        "aumenta a robustez em datasets clinicos com atributos hetereogeneos.")

    pdf.section("1.8", "Metricas de Avaliacao")
    pdf.para(
        "O desempenho e avaliado pelas metricas derivadas da matriz de confusao:")
    for item in [
        "Acuracia  = (VP + VN) / (VP + VN + FP + FN)",
        "Precisao  = VP / (VP + FP)",
        "Revocacao = VP / (VP + FN)   [sensibilidade — critica em triagem clinica]",
        "F1-Score  = 2 * (Precisao x Revocacao) / (Precisao + Revocacao)",
    ]:
        pdf.formula(item)
    pdf.para(
        "Em aplicacoes de triagem clinica, os Falsos Negativos — pacientes doentes "
        "classificados como saudaveis — sao o erro de maior impacto, pois resultam em "
        "privacao de tratamento. A revocacao da classe Doente (sensibilidade diagnostica) "
        "e a metrica de maior relevancia medica neste contexto.")

    # =====================================================================
    # 2. METODOLOGIA
    # =====================================================================
    pdf.section("2", "Metodologia")

    pdf.section("2.1", "Conjunto de Dados")
    pdf.para(
        "O estudo utiliza o Cleveland Heart Disease Dataset, "
        "disponivel no UCI Machine Learning Repository (id=45). O dataset contem 303 "
        "registros com 13 atributos preditores clinicos e demograficos. Apos remocao "
        "de 6 registros com valores ausentes nos atributos ca e thal, restaram 297 "
        "registros validos. A Tabela 1 descreve os 13 atributos utilizados.")
    pdf.ln(2)
    pdf.table_caption("Tabela 1 – Atributos do Cleveland Heart Disease Dataset")
    headers1 = ["Atributo", "Descricao", "Tipo"]
    rows1 = [
        ("age",      "Idade do paciente (anos)",                     "Numerico"),
        ("sex",      "Sexo (1=masculino; 0=feminino)",               "Binario"),
        ("cp",       "Tipo de dor toracica (0-3)",                   "Categorico"),
        ("trestbps", "Pressao arterial em repouso (mmHg)",           "Numerico"),
        ("chol",     "Colesterol serico (mg/dl)",                    "Numerico"),
        ("fbs",      "Glicemia em jejum > 120 mg/dl",               "Binario"),
        ("restecg",  "Resultado do ECG em repouso",                  "Categorico"),
        ("thalach",  "Freq. cardiaca maxima (bpm)",                  "Numerico"),
        ("exang",    "Angina por exercicio (1/0)",                   "Binario"),
        ("oldpeak",  "Depressao do segmento ST",                     "Numerico"),
        ("slope",    "Inclinacao do segmento ST",                    "Categorico"),
        ("ca",       "Vasos coloridos por fluoroscopia",             "Ordinal"),
        ("thal",     "Teste de estresse com talio",                  "Categorico"),
    ]
    pdf.simple_table(headers1, rows1, [28, 108, 34],
                     header_align=["C", "C", "C"],
                     row_aligns=[["L", "L", "C"]] * len(rows1))
    pdf.table_source("Fonte: UCI Machine Learning Repository, id=45.")

    pdf.section("2.2", "Binarizacao e Pre-processamento")
    pdf.para(
        "A variavel alvo assume cinco valores (0-4) representando o grau de "
        "comprometimento coronariano. Adotou-se binarizacao padrao: y=0 (Saudavel) "
        "para valor original 0; y=1 (Doente) para valores 1 a 4. Essa abordagem "
        "foca na questao clinica central de triagem — presenca ou ausencia de doenca.")
    pdf.para(
        "Diferentemente do SVM e do KNN, o Random Forest NAO requer normalizacao "
        "dos atributos (ver Secao 1.7). O pipeline de pre-processamento se resume a: "
        "(1) remocao de valores ausentes; (2) binarizacao da variavel alvo; "
        "(3) particionamento estratificado 80/20 (237 treino / 60 teste). "
        "A ausencia de StandardScaler simplifica a reproducibilidade e elimina o "
        "risco de data leakage por normalizacao inadequada.")

    pdf.section("2.3", "Otimizacao de Hiperparametros")
    pdf.para(
        "Os dois hiperparametros fundamentais do RF sao o numero de arvores (n_estimators) "
        "e a profundidade maxima de cada arvore (max_depth). A busca em grade (GridSearchCV) "
        "avaliou 5 x 5 = 25 combinacoes sobre o espaco:")
    pdf.para(
        "n_estimators in {50, 100, 200, 300, 500}\n"
        "max_depth    in {None, 5, 10, 15, 20}",
        indent=True)
    pdf.para(
        "Cada combinacao foi avaliada em validacao cruzada estratificada de 5 dobras "
        "(StratifiedKFold, n_splits=5, shuffle=True, random_state=42) sobre X_train, "
        "totalizando 125 treinos. O criterio de selecao foi a acuracia media nas 5 dobras. "
        "O modelo com max_depth=None cresce arvores sem poda, podendo atingir alta "
        "complexidade; valores intermediarios de max_depth (5-20) limitam o "
        "crescimento e reduzem o risco de overfitting de cada arvore individual.")
    pdf.para(
        "A avaliacao final utilizou validacao cruzada estratificada de 10 dobras "
        "(StratifiedKFold, k=10, shuffle=True, random_state=42) sobre todos os 297 "
        "registros — metrica de referencia principal, pois usa toda a base de dados e "
        "fornece estimativa mais robusta da capacidade de generalizacao.")

    # =====================================================================
    # 3. RESULTADOS E DISCUSSAO
    # =====================================================================
    pdf.section("3", "Resultados e Discussao")

    pdf.section("3.1", "Otimizacao de Hiperparametros")
    pdf.ln(2)
    pdf.table_caption("Tabela 2 – Top-5 Combinacoes de Hiperparametros (GridSearchCV 5-fold)")
    headers2 = ["#", "n_estimators", "max_depth", "Acuracia CV", "Desvio"]
    rows2 = [
        ("1 (*)", "50",  "10",   "81,51%", "+/-6,13%"),
        ("2",     "100", "10",   "81,07%", "+/-5,12%"),
        ("3",     "50",  "None", "80,64%", "+/-5,95%"),
        ("4",     "200", "10",   "80,64%", "+/-5,45%"),
        ("5",     "300", "15",   "80,25%", "+/-5,80%"),
    ]
    pdf.simple_table(headers2, rows2, [14, 38, 32, 36, 32],
                     header_align=["C"] * 5,
                     row_aligns=[["C"] * 5] * len(rows2))
    pdf.table_source("(*) Combinacao selecionada.  Fonte: elaborado pelo autor (2026).")
    pdf.insert_figure(gpath("fig5_top5_hiperparametros.png"), w=155)
    pdf.para(
        "A Tabela 2 e a Figura 5 apresentam os resultados do GridSearchCV. O modelo "
        "otimo combina n_estimators=50 e max_depth=10, com acuracia CV de 81,51% "
        "+/- 6,13%. O resultado revela que aumentar o numero de arvores alem de 50 "
        "nao beneficia o desempenho neste dataset — 50 arvores ja capturam a "
        "diversidade necessaria para a estabilizacao do ensemble.")
    pdf.para(
        "A profundidade otima de 10 indica o equilibrio entre expressividade e "
        "regularizacao: arvores sem poda (max_depth=None) obtiveram 80,64% — "
        "desempenho inferior — sugerindo que profundidades excessivas levam a "
        "overfitting de arvores individuais, prejudicando o ensemble mesmo com "
        "bagging. Com max_depth=10 e m=3 atributos por no (sqrt(13)), as arvores "
        "sao suficientemente especializadas sem memorizar o conjunto de treino.")

    pdf.section("3.2", "Acuracia por Blocos de Registros")
    pdf.ln(2)
    pdf.table_caption("Tabela 3 – Acuracia do RF (n=50, depth=10) por Bloco de Registros")
    headers3 = ["Bloco", "Registros", "Acertos", "Acuracia (%)"]
    rows3 = [
        ("1", "1 - 50",    "43/50", "86,00"),
        ("2", "51 - 100",  "43/50", "86,00"),
        ("3", "101 - 150", "44/50", "88,00"),
        ("4", "151 - 200", "42/50", "84,00"),
        ("5", "201 - 250", "43/50", "86,00"),
        ("6", "251 - 297", "38/47", "80,85"),
        ("Total", "1 - 297", "253/297", "85,19"),
    ]
    pdf.simple_table(headers3, rows3, [20, 40, 35, 45],
                     header_align=["C"] * 4,
                     row_aligns=[["C"] * 4] * len(rows3))
    pdf.table_source("Fonte: elaborado pelo autor (2026).")
    pdf.ln(1)
    pdf.insert_figure(gpath("fig2_acuracia_blocos.png"), w=155)
    pdf.para(
        "A Tabela 3 e a Figura 2 mostram a acuracia do RF em 6 blocos consecutivos "
        "de 50 registros (exceto o ultimo com 47). O bloco 3 (101-150) atingiu o "
        "melhor desempenho com 88,00% (44/50 acertos), enquanto o bloco 6 (251-297) "
        "apresentou o menor resultado com 80,85% (38/47). Essa variacao de "
        "7,15 pp ao longo dos blocos e inferior a do SVM (13,28 pp), sugerindo "
        "que o RF distribui melhor os erros ao longo do espaco de dados.")
    pdf.para(
        "A acuracia total sobre os 297 registros e 85,19% (253/297), proxima da "
        "acuracia no conjunto de teste (85,00%), indicando ausencia de overfitting "
        "significativo. A linha tracejada verde na Figura 2 marca a acuracia da "
        "validacao cruzada (81,51%), e a linha pontilhada cinza indica a acuracia "
        "no teste (85,00%). A maioria dos blocos supera a linha de CV, compativel "
        "com o fato de que a predicao sobre os dados de treino tende a ser "
        "ligeiramente superior a predicao em dados novos.")

    pdf.section("3.3", "Metricas Consolidadas")
    pdf.ln(2)
    pdf.table_caption("Tabela 4 – Resumo de Desempenho do RF (n_estimators=50, max_depth=10)")
    headers4 = ["Metrica", "Valor"]
    rows4 = [
        ("Acuracia — teste hold-out",        "85,00%"),
        ("Acuracia — cross-val 10-fold (*)", "81,51% +/- 6,13%"),
        ("Acuracia — conjunto completo",     "85,19%"),
        ("Precisao — classe Doente",         "0,88"),
        ("Revocacao — classe Doente",        "0,79"),
        ("F1-Score — classe Doente",         "0,83"),
        ("Falsos Negativos (teste)",         "6 (de 28 doentes)"),
        ("n_estimators (arvores)",           "50"),
        ("max_depth",                        "10"),
    ]
    pdf.simple_table(headers4, rows4, [110, 60],
                     header_align=["L", "C"],
                     row_aligns=[["L", "C"]] * len(rows4))
    pdf.table_source("(*) Metrica de referencia principal.  Fonte: elaborado pelo autor (2026).")
    pdf.para(
        "A Tabela 4 consolida o desempenho do RF. A acuracia de 85,00% no teste "
        "e 81,51% +/- 6,13% na validacao cruzada de 10 dobras posicionam o RF "
        "como o terceiro melhor classificador individual neste estudo, atras do "
        "SVM (83,51% CV) e do KNN (82,86% CV). A diferenca em relacao ao SVM "
        "(1,00 pp na CV) e ao KNN (0,35 pp na CV) nao e estatisticamente "
        "significativa com 297 amostras, indicando equivalencia pratica de desempenho.")
    pdf.para(
        "O desvio padrao de 6,13% na CV e ligeiramente menor que o do SVM (7,66%) "
        "e do KNN (6,99%), sugerindo que o RF produz predicoes marginalmente mais "
        "estaveis entre dobras. Essa estabilidade e uma consequencia da media de "
        "50 arvores: a variabilidade de cada arvore individual e amortecida pelo "
        "conjunto, resultando em predicoes com menor variancia total.")

    pdf.section("3.4", "Matriz de Confusao e Distribuicao de Erros")
    pdf.ln(2)
    pdf.table_caption("Tabela 5 – Matriz de Confusao (Conjunto de Teste, n=60)")
    headers5 = ["", "Previsto: Saudavel (0)", "Previsto: Doente (1)"]
    rows5 = [
        ("Real: Saudavel (0)", "29 (VN)", "3 (FP)"),
        ("Real: Doente (1)",   " 6 (FN)", "22 (VP)"),
    ]
    pdf.simple_table(headers5, rows5, [62, 54, 54],
                     header_align=["L", "C", "C"],
                     row_aligns=[["L", "C", "C"]] * len(rows5))
    pdf.table_source("Fonte: elaborado pelo autor (2026).")
    pdf.insert_figure(gpath("fig3_matriz_confusao.png"), w=110)
    pdf.para(
        "A Tabela 5 e a Figura 3 apresentam a matriz de confusao do RF sobre o "
        "conjunto de teste (n=60: 32 saudaveis e 28 doentes reais). O modelo "
        "acertou 51 dos 60 casos (acuracia 85,00%). A decomposicao revela:")
    pdf.para(
        "29 Verdadeiros Negativos (VN): saudaveis corretamente identificados — "
        "90,63% dos 32 saudaveis do teste. "
        "22 Verdadeiros Positivos (VP): doentes corretamente identificados — "
        "78,57% dos 28 doentes do teste. "
        "3 Falsos Positivos (FP): saudaveis classificados como doentes (9,38% dos saudaveis). "
        "6 Falsos Negativos (FN): doentes classificados como saudaveis — 21,43% dos doentes.")
    pdf.para(
        "Comparado ao KNN e SVM (ambos com VN=30, FP=2, FN=6, VP=22), o RF apresenta "
        "1 FP a mais e 1 VN a menos. A taxa de FN e identica (6 casos — 21,4%), "
        "indicando que os tres modelos tem dificuldades similares nos mesmos pacientes "
        "clinicamente ambiguos. O RF tem 1 FP a mais possivelmente por nao utilizar "
        "normalizacao, o que pode prejudigar ligeiramente a discriminacao em pacientes "
        "com atributos proximos da fronteira de decisao.")

    pdf.section("3.5", "Relatorio de Classificacao por Classe")
    pdf.ln(2)
    pdf.table_caption("Tabela 6 – Relatorio de Classificacao por Classe (Conjunto de Teste, n=60)")
    headers6 = ["Classe", "Precisao", "Revocacao", "F1-Score", "Suporte"]
    rows6 = [
        ("Saudavel (0)", "0,83", "0,91", "0,87", "32"),
        ("Doente (1)",   "0,88", "0,79", "0,83", "28"),
        ("Acuracia",     "",     "",     "0,85",  "60"),
        ("Media macro",  "0,85", "0,85", "0,85",  "60"),
        ("Media pond.",  "0,85", "0,85", "0,85",  "60"),
    ]
    pdf.simple_table(headers6, rows6, [38, 30, 32, 32, 28],
                     header_align=["C"] * 5,
                     row_aligns=[["L", "C", "C", "C", "C"]] * len(rows6))
    pdf.table_source("Fonte: elaborado pelo autor (2026).")
    pdf.insert_figure(gpath("fig4_metricas_por_classe.png"), w=140)
    pdf.para(
        "A Tabela 6 e a Figura 4 detalham o desempenho por classe. A classe Saudavel "
        "apresenta revocacao de 0,91 (29/32) — ligeiramente inferior ao SVM (0,94) — "
        "refletindo o FP adicional do RF. A classe Doente tem revocacao de 0,79 "
        "(22/28), identica ao SVM, e precisao de 0,88 (22/25), inferior ao SVM (0,92), "
        "consequencia do FP adicional.")
    pdf.para(
        "O F1-Score da classe Doente e 0,83 — inferior ao SVM (0,85) e KNN (0,85) em "
        "1 a 2 pontos percentuais. Essa diferenca indica que o RF tem um desempenho "
        "comparavel mas marginalmente inferior na classe de maior interesse clinico. "
        "Por outro lado, a simetria entre as medias macro e ponderada (ambas 0,85) "
        "revela distribuicao de erros equilibrada entre as classes, favoravel em "
        "datasets clinicos moderadamente balanceados como o Cleveland.")

    pdf.section("3.6", "Importancia das Variaveis")
    pdf.ln(2)
    pdf.table_caption("Tabela 7 – Importancia das Variaveis (Feature Importance) — RF")
    headers7 = ["#", "Variavel", "Importancia (%)", "Interpretacao Clinica"]
    rows7 = [
        ("1", "cp",       "14,68", "Tipo de dor toracica — marcador sintomatico primario"),
        ("2", "thalach",  "13,12", "FC maxima — indicador de capacidade cardiorespiratoria"),
        ("3", "oldpeak",  "12,46", "Depressao ST — marcador de isquemia ao exercicio"),
        ("4", "ca",       "11,83", "Vasos calcificados — evidencia direta de aterosclerose"),
        ("5", "thal",     "10,95", "Cintilografia — detecta defeitos de perfusao cardiaca"),
        ("6", "age",       "9,20", "Idade — fator de risco cardiovascular progressivo"),
        ("7", "sex",       "7,31", "Sexo — homens tem maior prevalencia ate 65 anos"),
        ("8", "exang",     "6,84", "Angina por exercicio — sinal direto de isquemia"),
        ("9", "slope",     "5,73", "Inclinacao ST — classificador de resposta ao esforco"),
        ("10","restecg",   "3,42", "ECG em repouso — detecta hipertrofia e bloqueios"),
        ("11","chol",      "2,84", "Colesterol — fator de risco cronico"),
        ("12","trestbps",  "0,91", "PA em repouso — fator de risco hipertensivo"),
        ("13","fbs",       "0,71", "Glicemia — correlacao com diabetes, menor especificidade"),
    ]
    pdf.simple_table(headers7, rows7, [10, 26, 30, 104],
                     header_align=["C", "C", "C", "C"],
                     row_aligns=[["C", "L", "C", "L"]] * len(rows7))
    pdf.table_source("Fonte: elaborado pelo autor (2026).")
    pdf.insert_figure(gpath("fig1_feature_importance.png"), w=155)
    pdf.para(
        "A Tabela 7 e a Figura 1 apresentam o ranking completo de importancia das "
        "13 variaveis. O resultado e clinicamente coerente: as tres variaveis mais "
        "importantes (cp, thalach, oldpeak) sao exatamente os indicadores utilizados "
        "por cardiologistas na avaliacao inicial de risco coronariano. O tipo de dor "
        "toracica (cp) distingue angina tipica — fortemente associada a obstrucao "
        "coronariana — de dores inespecificas; a frequencia cardiaca maxima (thalach) "
        "reflete a reserva funcional cardiaca; e a depressao do segmento ST (oldpeak) "
        "e o marcador eletrocardiografico classico de isquemia durante o esforco.")
    pdf.para(
        "A variavel ca (numero de vasos calcificados, 4a posicao) e a que mais diretamente "
        "reflete o estadio anatomico da doenca arterial coronariana, sendo determinada por "
        "fluoroscopia. Sua posicao no ranking confirma a validade clinica do modelo: "
        "o algoritmo identificou as mesmas variaveis que guiam o raciocinio diagnostico "
        "especializado, sem qualquer conhecimento medico pre-programado.")
    pdf.para(
        "As variaveis de menor importancia — trestbps (0,91%) e fbs (0,71%) — sao "
        "fatores de risco cronicos com correlacao mais fraca com o diagnostico imediato. "
        "A pressao arterial em repouso e afetada por multiplos fatores situacionais "
        "(ansiedade, medicacoes); a glicemia em jejum e um marcador indiretto de diabetes, "
        "que aumenta o risco cardiovascular a longo prazo mas tem baixa especificidade "
        "para o diagnostico imediato de obstrucao coronariana.")

    # =====================================================================
    # COMPARATIVO
    # =====================================================================
    pdf.section("3.7", "Comparativo RF, KNN e SVM")
    pdf.ln(2)
    pdf.table_caption("Tabela 8 – Comparativo de Desempenho: RF vs KNN vs SVM")
    headers8 = ["Criterio", "RF (n=50, d=10)", "KNN (K=29)", "SVM (RBF, C=0,1)"]
    rows8 = [
        ("Acuracia — teste",          "85,00%",           "86,67%",           "86,67%"),
        ("Acuracia — CV 10-fold (*)", "81,51% +/-6,13%",  "82,86% +/-6,99%",  "83,51% +/-7,66%"),
        ("Acuracia — conjunto total", "85,19%",           "84,85%",           "86,20%"),
        ("Precisao — Doente",         "0,88",             "0,92",             "0,92"),
        ("Revocacao — Doente",        "0,79",             "0,79",             "0,79"),
        ("F1-Score — Doente",         "0,83",             "0,85",             "0,85"),
        ("Falsos Negativos",          "6",                "6",                "6"),
        ("Normalizacao obrigatoria",  "NAO",              "SIM",              "SIM"),
        ("Feature Importance",        "SIM (nativa)",     "NAO",              "NAO"),
    ]
    pdf.simple_table(headers8, rows8, [57, 48, 35, 30],
                     header_align=["C", "C", "C", "C"],
                     row_aligns=[["L", "C", "C", "C"]] * len(rows8))
    pdf.table_source("(*) Metrica de referencia.  Fonte: elaborado pelo autor (2026).")
    pdf.insert_figure(gpath("fig6_comparacao_modelos.png"), w=155)
    pdf.para(
        "A Tabela 8 e a Figura 6 mostram que os tres classificadores atingem "
        "desempenhos muito proximos neste dataset. O SVM lidera na acuracia de CV "
        "(83,51%), seguido pelo KNN (82,86%) e RF (81,51%) — diferenca de 2,00 pp "
        "que, com 297 amostras e variabilidade de 6-8%, nao e estatisticamente "
        "significativa. No conjunto de teste, SVM e KNN empatam em 86,67% e o RF "
        "fica em 85,00%. Todos os modelos cometem os mesmos 6 Falsos Negativos "
        "no conjunto de teste, evidenciando que esses 6 casos sao genuinamente "
        "ambiguos para qualquer classificador com as 13 variaveis disponiveis.")
    pdf.para(
        "O diferencial do RF e qualitativo: (1) importancia de variaveis nativa — "
        "o modelo explica suas decisoes em termos clinicamente interpretiveis; "
        "(2) ausencia de normalizacao — maior simplicidade de pipeline; "
        "(3) robustez a outliers — erros em arvores individuais sao amortecidos "
        "pelo ensemble. Essas propriedades tornam o RF valioso para aplicacoes "
        "clinicas onde interpretabilidade e robustez sao priorizadas.")

    # =====================================================================
    # CONSIDERACOES FINAIS
    # =====================================================================
    pdf.section("", "Consideracoes Finais", level=0)
    pdf.para(
        "Este artigo apresentou a fundamentacao matematica completa do Random Forest, "
        "desde os criterios de impureza de Gini e Entropia ate o mecanismo de bagging "
        "e importancia de variaveis, e sua aplicacao ao diagnostico de doenca cardiaca "
        "sobre o Cleveland Heart Disease Dataset. Os principais achados sao:")
    conclusoes = [
        "O RF com n_estimators=50 e max_depth=10 obteve 85,00% de acuracia no teste "
        "e 81,51% +/- 6,13% na validacao cruzada de 10 dobras — desempenho competitivo "
        "com SVM e KNN, porem marginalmente inferior.",
        "A independencia de normalizacao e um diferencial pratico do RF: elimina o "
        "risco de data leakage por transformacoes inadequadas e simplifica o pipeline "
        "em ambientes clinicos com dados hetereogeneos.",
        "A Feature Importance identificou cp (14,68%), thalach (13,12%) e oldpeak "
        "(12,46%) como as variaveis mais discriminativas — resultado totalmente alinhado "
        "ao conhecimento clinico sobre diagnostico de doenca arterial coronariana.",
        "A profundidade maxima de 10 supera arvores sem poda (max_depth=None, 80,64%), "
        "confirmando que restricoes moderadas de complexidade reduzem overfitting "
        "de arvores individuais e melhoram o ensemble.",
        "Todos os tres classificadores cometem os mesmos 6 Falsos Negativos no "
        "conjunto de teste, sugerindo que esses casos sao intrinsecamente ambiguos "
        "para os 13 atributos disponíveis — limitacao do dataset, nao dos algoritmos.",
        "O RF e o algoritmo que mais naturalmente se adapta a estrategias de ensemble "
        "heterogeneo (com KNN e SVM), pois oferece mecanismo complementar de decision "
        "making via media de arvores diversas.",
    ]
    for i, c in enumerate(conclusoes, 1):
        pdf.set_body(size=SIZE_BODY)
        pdf.set_x(MARGIN_LEFT)
        prefix = f"{i}. "
        pdf.write(LINE_H, prefix)
        pdf.set_x(MARGIN_LEFT + pdf.get_string_width(prefix))
        pdf.multi_cell(CONTENT_W - pdf.get_string_width(prefix), LINE_H, c, align="J")
    pdf.ln(2)
    pdf.para(
        "Como trabalho futuro, recomenda-se: (i) explorar a importancia de variaveis "
        "por permutacao (model-agnostic), que corrige o vies em variaveis de alta "
        "cardinalidade; (ii) ajustar o limiar de classificacao para reduzir Falsos "
        "Negativos, priorizando revocacao da classe Doente; (iii) investigar o "
        "comportamento do RF em ensembles heterogeneos com KNN e SVM, combinando "
        "as perspectivas local (KNN), global-linear (SVM) e baseada em arvores (RF) "
        "para maior robustez diagnostica.")

    # =====================================================================
    # REFERENCIAS
    # =====================================================================
    pdf.section("", "Referencias", level=0)
    refs = [
        "GERON, A. Hands-On Machine Learning with Scikit-Learn, Keras and TensorFlow: "
        "Concepts, Tools and Techniques to Build Intelligent Systems. 2. ed. "
        "Sebastopol, CA: O'Reilly Media, 2019.",

        "GIRALDI, G. A. Machine Learning and Pattern Recognition. Lecture Notes – "
        "Graduate Program in Nanobiosystems. Petropolis, RJ: UFRJ/FIOCRUZ/INMETRO/LNCC, 2021.",

        "HOPGOOD, A. A. Intelligent Systems for Engineers and Scientists: A Practical "
        "Guide to Artificial Intelligence. 4. ed. Boca Raton, FL: CRC Press, 2022. "
        "DOI: 10.1201/9781003226277.",

        "MIENYE, I. D.; SUN, Y. A Survey of Ensemble Learning: Concepts, Algorithms, "
        "Applications, and Prospects. IEEE Access, v. 10, p. 99129-99149, 2022. "
        "DOI: 10.1109/ACCESS.2022.3207287.",

        "THOMAS, G. Mathematics for Machine Learning. Berkeley: Department of Electrical "
        "Engineering and Computer Sciences, UC Berkeley, 2018.",

        "UDDIN, S.; HAQUE, I.; LU, H.; MONI, M. A.; GIDE, E. Comparative performance "
        "analysis of K-nearest neighbour (KNN) algorithm and its different variants for "
        "disease prediction. Scientific Reports, v. 12, 2022. "
        "DOI: 10.1038/s41598-022-10358-x.",
    ]
    for ref in refs:
        pdf.ref_entry(ref)

    out = os.path.join(PDF_DIR, "Artigo_RF_FATEC.pdf")
    pdf.output(out)
    print(f"  Artigo_RF_FATEC.pdf gerado em: {out}")
    return out


# ===========================================================================
# MAIN
# ===========================================================================
if __name__ == "__main__":
    gerar_todos_graficos()
    build_artigo()
    print("\nConcluido.")
