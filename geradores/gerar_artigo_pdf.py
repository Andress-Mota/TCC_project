# -*- coding: utf-8 -*-
"""
Gerador de artigo científico em PDF conforme normas FATEC Guaratinguetá 2022.
Fonte: Arial 11, margens 2.5/2/2/2, espaçamento 1.5, parágrafos 1.25cm.
"""

from fpdf import FPDF
import os

# ---------------------------------------------------------------------------
# Constantes de formatação FATEC 2022
# ---------------------------------------------------------------------------
MARGIN_LEFT   = 20.0   # mm (2 cm)
MARGIN_RIGHT  = 20.0   # mm (2 cm)
MARGIN_TOP    = 25.0   # mm (2.5 cm)
MARGIN_BOTTOM = 20.0   # mm (2 cm)
PAGE_W        = 210.0  # mm A4
PAGE_H        = 297.0  # mm A4
CONTENT_W     = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT  # 170 mm
FONT          = "Arial"
SIZE_BODY     = 11
SIZE_SMALL    = 10
SIZE_TITLE    = 12
LINE_H        = 7.0    # altura de linha ≈ 1.5 × 11 pt
LINE_H_SM     = 6.0    # linha para tamanho 10
LINE_H_TBL    = 5.5    # linha para tabelas (espaçamento simples)
INDENT        = 12.5   # mm (1.25 cm)


ARIAL_FONTS = {
    "":   "C:/Windows/Fonts/arial.ttf",
    "B":  "C:/Windows/Fonts/arialbd.ttf",
    "I":  "C:/Windows/Fonts/ariali.ttf",
    "BI": "C:/Windows/Fonts/arialbi.ttf",
}


class ArtigoFATEC(FPDF):
    """PDF personalizado com cabeçalho e rodapé conforme normas FATEC."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for style, path in ARIAL_FONTS.items():
            if os.path.exists(path):
                self.add_font("Arial", style, path)

    def header(self):
        # Cabeçalho em 1 cm — apenas linha reservada (vazio conforme modelo)
        pass

    def footer(self):
        # Rodapé: número de página centralizado, Arial 10
        self.set_y(-15)
        self.set_font(FONT, "", SIZE_SMALL)
        self.cell(0, 10, str(self.page_no()), align="C")

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------
    def set_body(self, bold=False, italic=False, size=SIZE_BODY):
        style = ("B" if bold else "") + ("I" if italic else "")
        self.set_font(FONT, style, size)

    def para(self, text, indent=True, align="J", size=SIZE_BODY,
             bold=False, italic=False, lh=None):
        """Parágrafo com ou sem indentação."""
        if lh is None:
            lh = LINE_H if size == SIZE_BODY else LINE_H_SM
        self.set_body(bold=bold, italic=italic, size=size)
        if indent:
            self.set_x(MARGIN_LEFT + INDENT)
            self.multi_cell(CONTENT_W - INDENT, lh, text, align=align)
        else:
            self.set_x(MARGIN_LEFT)
            self.multi_cell(CONTENT_W, lh, text, align=align)

    def section(self, num, title, level=1):
        """Título de seção ou subseção, negrito, alinhado à esquerda."""
        self.ln(3)
        self.set_body(bold=True, size=SIZE_BODY)
        label = f"{num} {title}"
        self.set_x(MARGIN_LEFT)
        self.multi_cell(CONTENT_W, LINE_H, label, align="L")
        self.ln(1)

    def center_line(self, text, size=SIZE_BODY, bold=False, italic=False,
                    lh=None):
        """Linha de texto centralizada."""
        lh = lh or (LINE_H if size >= SIZE_BODY else LINE_H_SM)
        self.set_body(bold=bold, italic=italic, size=size)
        self.set_x(MARGIN_LEFT)
        self.multi_cell(CONTENT_W, lh, text, align="C")

    def ref_entry(self, text):
        """Entrada de referência: sem recuo, espaçamento simples."""
        self.set_body(size=SIZE_BODY)
        self.set_x(MARGIN_LEFT)
        self.multi_cell(CONTENT_W, LINE_H_TBL + 0.5, text, align="J")
        self.ln(2)

    def table_caption(self, text):
        """Legenda de tabela/figura: tamanho 10, centralizado."""
        self.set_body(bold=True, size=SIZE_SMALL)
        self.set_x(MARGIN_LEFT)
        self.multi_cell(CONTENT_W, LINE_H_SM, text, align="C")

    def table_source(self, text):
        """Fonte de tabela: tamanho 10."""
        self.set_body(size=SIZE_SMALL)
        self.set_x(MARGIN_LEFT)
        self.multi_cell(CONTENT_W, LINE_H_SM, text, align="C")
        self.ln(3)

    def draw_hline(self):
        self.set_draw_color(0)
        self.set_line_width(0.3)
        self.line(MARGIN_LEFT, self.get_y(), PAGE_W - MARGIN_RIGHT, self.get_y())
        self.ln(1)

    def quote_block(self, text):
        """Citação longa: recuo 4 cm, tamanho 10, justificado."""
        self.set_body(size=SIZE_SMALL)
        self.set_x(MARGIN_LEFT + 40)
        self.multi_cell(CONTENT_W - 40, LINE_H_SM, text, align="J")
        self.ln(2)

    # -----------------------------------------------------------------------
    # Tabelas inline
    # -----------------------------------------------------------------------
    def simple_table(self, headers, rows, col_widths, header_align=None,
                     row_aligns=None):
        """Tabela genérica com células bordadas."""
        self.set_body(bold=True, size=SIZE_SMALL)
        x0 = MARGIN_LEFT
        self.set_x(x0)
        ha = header_align or ["C"] * len(headers)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], LINE_H_TBL + 1, h,
                      border=1, align=ha[i])
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

    def confusion_matrix(self):
        """Formata a matriz de confusão 2×2."""
        cw = [55, 42, 42]
        self.set_body(bold=True, size=SIZE_SMALL)
        self.set_x(MARGIN_LEFT)
        self.cell(cw[0], LINE_H_TBL + 1, "", border=1)
        self.cell(cw[1], LINE_H_TBL + 1, "Previsto: Saudável", border=1, align="C")
        self.cell(cw[2], LINE_H_TBL + 1, "Previsto: Doente", border=1, align="C")
        self.ln()
        self.set_body(size=SIZE_SMALL)
        rows = [
            ("Real: Saudável", "30 (VN)", "2 (FP)"),
            ("Real: Doente",   " 6 (FN)", "22 (VP)"),
        ]
        row_bold = [False, False]
        for row in rows:
            self.set_x(MARGIN_LEFT)
            self.set_body(bold=True, size=SIZE_SMALL)
            self.cell(cw[0], LINE_H_TBL + 1, row[0], border=1)
            self.set_body(size=SIZE_SMALL)
            self.cell(cw[1], LINE_H_TBL + 1, row[1], border=1, align="C")
            self.cell(cw[2], LINE_H_TBL + 1, row[2], border=1, align="C")
            self.ln()
        self.ln(2)


# ===========================================================================
# Conteúdo do artigo
# ===========================================================================

def build_pdf():
    pdf = ArtigoFATEC(orientation="P", unit="mm", format="A4")
    pdf.set_margins(MARGIN_LEFT, MARGIN_TOP, MARGIN_RIGHT)
    pdf.set_auto_page_break(auto=True, margin=MARGIN_BOTTOM)
    pdf.add_page()

    # -----------------------------------------------------------------------
    # TÍTULO
    # -----------------------------------------------------------------------
    pdf.set_body(bold=True, size=SIZE_TITLE)
    pdf.set_x(MARGIN_LEFT)
    pdf.multi_cell(CONTENT_W, LINE_H,
        "K-NEAREST NEIGHBORS APLICADO AO DIAGNÓSTICO DE DOENÇA CARDÍACA: "
        "FUNDAMENTOS MATEMÁTICOS, IMPLEMENTAÇÃO E ANÁLISE DE DESEMPENHO",
        align="C")
    pdf.ln(2)

    # -----------------------------------------------------------------------
    # AUTORIA
    # -----------------------------------------------------------------------
    pdf.center_line("André Felipe", size=SIZE_SMALL, italic=True)
    pdf.center_line("Faculdade de Tecnologia de Guaratinguetá", size=SIZE_SMALL, italic=True)
    pdf.center_line("andressmota78@gmail.com", size=SIZE_SMALL, italic=True)
    pdf.ln(4)

    # -----------------------------------------------------------------------
    # RESUMO
    # -----------------------------------------------------------------------
    pdf.set_body(bold=True, size=SIZE_BODY)
    pdf.set_x(MARGIN_LEFT)
    pdf.cell(CONTENT_W, LINE_H, "Resumo", align="L")
    pdf.ln(1)
    pdf.para(
        "Este artigo apresenta a aplicação do algoritmo K-Nearest Neighbors (KNN) para a "
        "classificação binária de doença cardíaca utilizando o Cleveland Heart Disease Dataset "
        "(UCI Machine Learning Repository). São abordados os fundamentos matemáticos do algoritmo, "
        "incluindo métricas de distância, regra de votação majoritária e seleção do hiperparâmetro K "
        "por meio de validação cruzada estratificada. A implementação foi desenvolvida em Python com "
        "a biblioteca scikit-learn, empregando padronização Z-score, particionamento estratificado e "
        "otimização automática de K via GridSearchCV. O melhor valor encontrado foi K = 29, obtendo "
        "acurácia de 86,67% no conjunto de teste e 82,86% ± 6,99% na validação cruzada de 10 dobras. "
        "Os 297 pacientes avaliados foram analisados por matriz de confusão, relatório de classificação "
        "e distribuição de acertos em blocos de 50 registros. O trabalho posiciona o KNN frente à "
        "literatura de aprendizado em conjunto, evidenciando seu papel como algoritmo de referência e "
        "suas limitações comparativas frente a métodos como Random Forest e XGBoost.",
        indent=False)
    pdf.ln(1)
    pdf.set_body(bold=True, size=SIZE_BODY)
    pdf.set_x(MARGIN_LEFT)
    pdf.set_font(FONT, "B", SIZE_BODY)
    pdf.write(LINE_H, "Palavras-chave: ")
    pdf.set_body(size=SIZE_BODY)
    pdf.write(LINE_H,
        "K-Nearest Neighbors; Aprendizado de Máquina; Doença Cardíaca; "
        "Classificação Binária; Validação Cruzada.")
    pdf.ln(4)

    # -----------------------------------------------------------------------
    # ABSTRACT
    # -----------------------------------------------------------------------
    pdf.set_body(bold=True, size=SIZE_BODY)
    pdf.set_x(MARGIN_LEFT)
    pdf.cell(CONTENT_W, LINE_H, "Abstract", align="L")
    pdf.ln(1)
    pdf.para(
        "This paper presents the application of the K-Nearest Neighbors (KNN) algorithm for binary "
        "classification of heart disease using the Cleveland Heart Disease Dataset (UCI Machine "
        "Learning Repository). The mathematical foundations of the algorithm are covered, including "
        "distance metrics, majority voting decision rules and selection of the hyperparameter K "
        "through stratified cross-validation. The Python implementation uses Z-score standardization, "
        "stratified data partitioning and automatic K optimization via GridSearchCV. The best value "
        "found was K = 29, achieving 86.67% accuracy on the test set and 82.86% +/- 6.99% in 10-fold "
        "cross-validation over 297 evaluated patients. The work positions KNN against the ensemble "
        "learning literature, highlighting its role as a baseline algorithm and its comparative "
        "limitations against methods such as Random Forest and XGBoost.",
        indent=False)
    pdf.ln(1)
    pdf.set_font(FONT, "B", SIZE_BODY)
    pdf.set_x(MARGIN_LEFT)
    pdf.write(LINE_H, "Keywords: ")
    pdf.set_body(size=SIZE_BODY)
    pdf.write(LINE_H,
        "K-Nearest Neighbors; Machine Learning; Heart Disease; Binary Classification; "
        "Cross-Validation.")
    pdf.ln(6)

    # =======================================================================
    # INTRODUÇÃO
    # =======================================================================
    pdf.section("", "Introdução", level=0)

    pdf.para(
        "As doenças cardiovasculares representam a principal causa de mortalidade global segundo a "
        "Organização Mundial da Saúde. O diagnóstico precoce é essencial para reduzir óbitos e custos "
        "hospitalares, mas exames como eletrocardiogramas avançados e cineangiocoronariografias possuem "
        "alto custo e disponibilidade limitada, especialmente em países em desenvolvimento "
        "(MIENYE; SUN, 2022).")
    pdf.para(
        "O aprendizado de máquina (AM) tem se consolidado como ferramenta de suporte à decisão clínica, "
        "sendo aplicado ao diagnóstico de diabetes, hipertensão, câncer e doenças renais. Géron (2019) "
        "destaca que algoritmos de classificação podem identificar padrões em dados clínicos com "
        "acurácia comparável à de especialistas, democratizando o acesso à triagem médica.")
    pdf.para(
        "Dentre os algoritmos de classificação, o K-Nearest Neighbors (KNN) se destaca pela "
        "simplicidade conceitual, transparência e facilidade de implementação. Por não construir um "
        "modelo explícito durante o treinamento — postergando toda a computação para o momento da "
        "predição —, é classificado como algoritmo de aprendizado lazy (preguiçoso) e baseado em "
        "instâncias (GÉRON, 2019). Essa característica o torna especialmente adequado para aplicações "
        "clínicas onde a interpretabilidade é relevante.")
    pdf.para(
        "O presente artigo tem como objetivos: (i) fundamentar matematicamente o algoritmo KNN; "
        "(ii) descrever a metodologia de implementação sobre o Cleveland Heart Disease Dataset; "
        "(iii) apresentar e analisar os resultados experimentais; e (iv) posicionar o KNN em relação "
        "à literatura de aprendizado em conjunto, identificando seus limites e as direções para "
        "trabalhos futuros.")

    # =======================================================================
    # 1. REFERENCIAL TEÓRICO
    # =======================================================================
    pdf.section("1", "Referencial Teórico")

    pdf.section("1.1", "O Algoritmo K-Nearest Neighbors")
    pdf.para(
        "O algoritmo KNN foi proposto por Fix e Hodges em 1951 e formalizado por Cover e Hart em 1967. "
        "Sua premissa é intuitiva: um ponto de consulta pertence à mesma classe que a maioria de seus K "
        "vizinhos mais próximos no espaço de características.")
    pdf.para(
        "Dado um conjunto de treinamento D = {(x1,y1), ..., (xn,yn)}, onde "
        "xi em R^d é o vetor de atributos e yi é o rótulo de classe, a predição "
        "para uma nova amostra xq é definida por:")
    # Fórmula - votação majoritária
    pdf.set_body(italic=True, size=SIZE_BODY)
    pdf.set_x(MARGIN_LEFT + INDENT)
    pdf.multi_cell(CONTENT_W - INDENT, LINE_H,
        "y_hat = argmax_c  SUM_{i em N_K(xq)}  1[yi = c]",
        align="L")
    pdf.ln(1)
    pdf.para(
        "onde N_K(xq) denota o conjunto dos K índices mais próximos de xq segundo uma "
        "métrica de distância, e 1[·] é a função indicadora. Na classificação binária adotada "
        "(c em {0,1}), a regra se reduz a:")
    pdf.set_body(italic=True, size=SIZE_BODY)
    pdf.set_x(MARGIN_LEFT + INDENT)
    pdf.multi_cell(CONTENT_W - INDENT, LINE_H,
        "y_hat = 1,  se  SUM_{i em N_K(xq)} yi > K/2\n"
        "y_hat = 0,  caso contrário",
        align="L")
    pdf.ln(1)
    pdf.para(
        "O modelo não constrói nenhuma função paramétrica durante o treinamento; toda a computação é "
        "realizada no momento da previsão, justificando sua classificação como algoritmo lazy. "
        "Géron (2019, p. 10) lista o KNN entre os algoritmos de aprendizado supervisionado mais importantes, "
        "ao lado de Regressão Logística, SVM, Árvores de Decisão e Redes Neurais.")

    pdf.section("1.2", "Métricas de Distância")
    pdf.para(
        "A noção de proximidade entre amostras é central ao KNN. A família de métricas de Minkowski "
        "generaliza as distâncias mais utilizadas:")
    pdf.set_body(italic=True, size=SIZE_BODY)
    pdf.set_x(MARGIN_LEFT + INDENT)
    pdf.multi_cell(CONTENT_W - INDENT, LINE_H,
        "d_p(x, z) = ( SUM_{j=1}^{d}  |xj - zj|^p )^(1/p)",
        align="L")
    pdf.ln(1)
    pdf.para(
        "Os casos especiais mais relevantes são:")
    pdf.set_body(bold=True, size=SIZE_BODY)
    pdf.set_x(MARGIN_LEFT)
    pdf.write(LINE_H, "Distância Euclidiana")
    pdf.set_body(size=SIZE_BODY)
    pdf.write(LINE_H,
        " (p = 2) — métrica padrão do scikit-learn, adequada para dados numéricos contínuos após "
        "normalização:")
    pdf.ln(LINE_H)
    pdf.set_body(italic=True, size=SIZE_BODY)
    pdf.set_x(MARGIN_LEFT + INDENT)
    pdf.multi_cell(CONTENT_W - INDENT, LINE_H,
        "d_E(x, z) = SQRT( SUM_{j=1}^{d} (xj - zj)^2 )",
        align="L")
    pdf.ln(1)
    pdf.set_body(bold=True, size=SIZE_BODY)
    pdf.set_x(MARGIN_LEFT)
    pdf.write(LINE_H, "Distância de Manhattan")
    pdf.set_body(size=SIZE_BODY)
    pdf.write(LINE_H,
        " (p = 1) — menos sensível a valores extremos, por somar diferenças absolutas:")
    pdf.ln(LINE_H)
    pdf.set_body(italic=True, size=SIZE_BODY)
    pdf.set_x(MARGIN_LEFT + INDENT)
    pdf.multi_cell(CONTENT_W - INDENT, LINE_H,
        "d_M(x, z) = SUM_{j=1}^{d} |xj - zj|",
        align="L")
    pdf.ln(1)
    pdf.set_body(bold=True, size=SIZE_BODY)
    pdf.set_x(MARGIN_LEFT)
    pdf.write(LINE_H, "Distância de Chebyshev")
    pdf.set_body(size=SIZE_BODY)
    pdf.write(LINE_H,
        " (p \u2192 \u221e) — considera apenas o atributo com maior diferença entre os pontos:")
    pdf.ln(LINE_H)
    pdf.set_body(italic=True, size=SIZE_BODY)
    pdf.set_x(MARGIN_LEFT + INDENT)
    pdf.multi_cell(CONTENT_W - INDENT, LINE_H,
        "d_inf(x, z) = max_j |xj - zj|",
        align="L")
    pdf.ln(1)
    pdf.para(
        "As métricas de distância fundamentais para o KNN — Euclidiana, p-norm e Chebyshev — "
        "são formalizadas por Giraldi (2021, p. 88) nas expressões (7.19)–(7.21) da seção 7.8 "
        '(Measures of Similarity and Dissimilarity). '
        "A implementação deste trabalho utiliza a distância Euclidiana, padrão do "
        "KNeighborsClassifier do scikit-learn (PEDREGOSA et al., 2011).")

    pdf.section("1.3", "Necessidade de Normalização")
    pdf.para(
        "Por ser fundamentado em distâncias, o KNN é altamente sensível à escala dos atributos. "
        "Um atributo com amplitude numérica elevada — como pressão arterial (80–200 mmHg) — dominaria "
        "o cálculo da distância em relação a atributos com menor variação — como sexo biológico (0 ou 1) "
        "— distorcendo as vizinhanças e prejudicando a classificação. Géron (2019) enfatiza que "
        "atributos com escalas muito diferentes são um problema para algoritmos sensíveis à distância; "
        "Giraldi (2021, p. 90) formaliza o processo de normalização na seção 7.9 como solução para "
        "garantir que todos os atributos operem no mesmo espaço métrico.")
    pdf.para(
        "A Padronização Z-score (StandardScaler) transforma cada atributo j de acordo com:")
    pdf.set_body(italic=True, size=SIZE_BODY)
    pdf.set_x(MARGIN_LEFT + INDENT)
    pdf.multi_cell(CONTENT_W - INDENT, LINE_H,
        "zij = (xij - x_mean_j) / sigma_j",
        align="L")
    pdf.ln(1)
    pdf.para(
        "onde x_mean_j é a média e sigma_j é o desvio padrão calculados exclusivamente "
        "sobre o conjunto de treinamento, garantindo que informações do conjunto de teste não "
        "contaminem o pré-processamento — prática conhecida como prevenção de data leakage. Após "
        "a transformação, todos os atributos possuem média zero e desvio padrão unitário.")

    pdf.section("1.4", "Seleção do Hiperparâmetro K e o Trade-off Viés-Variância")
    pdf.para(
        "O valor de K é o principal hiperparâmetro do KNN e governa o equilíbrio entre viés e variância:")
    pdf.para("K pequeno: o modelo é muito sensível a variações locais, resultando em alta variância "
             "e risco de overfitting.", indent=True)
    pdf.para("K grande: o modelo suaviza excessivamente as fronteiras de decisão, aumentando o viés "
             "e levando ao underfitting.", indent=True)
    pdf.para(
        "O erro esperado de generalização pode ser decomposto como:")
    pdf.set_body(italic=True, size=SIZE_BODY)
    pdf.set_x(MARGIN_LEFT + INDENT)
    pdf.multi_cell(CONTENT_W - INDENT, LINE_H,
        "Erro(xq) = Vies^2 + Variancia + epsilon (ruido irredutivel)",
        align="L")
    pdf.ln(1)
    pdf.para(
        "O método padrão para seleção de K é a busca em grade com validação cruzada estratificada "
        "(GridSearchCV + StratifiedKFold). Para cada candidato k em {1, ..., K_max}:")
    pdf.set_body(italic=True, size=SIZE_BODY)
    pdf.set_x(MARGIN_LEFT + INDENT)
    pdf.multi_cell(CONTENT_W - INDENT, LINE_H,
        "K* = argmax_k  (1/v) SUM_{i=1}^{v} Acc(k, dobra_i)",
        align="L")
    pdf.ln(1)

    pdf.section("1.5", "Validação Cruzada Estratificada")
    pdf.para(
        "A validação cruzada k-fold estratificada (StratifiedKFold) garante que a proporção de "
        "classes em cada dobra reflita a distribuição global do conjunto. Para um conjunto D "
        "particionado em v dobras (GÉRON, 2019, p. 59):")
    pdf.set_body(italic=True, size=SIZE_BODY)
    pdf.set_x(MARGIN_LEFT + INDENT)
    pdf.multi_cell(CONTENT_W - INDENT, LINE_H,
        "Acc_CV = (1/v) SUM_{i=1}^{v} Acc( M_{D \\ Di}, Di )",
        align="L")
    pdf.ln(1)
    pdf.para(
        "onde M_{D/Di} é o modelo treinado em todas as dobras exceto a dobra i, e avaliado "
        "sobre Di. Segundo Géron (2019), a validação cruzada é a métrica mais confiável para "
        "estimar a capacidade de generalização. Esta é a métrica de referência principal deste artigo.")

    pdf.section("1.6", "Métricas de Avaliação de Classificadores")
    pdf.para(
        "O desempenho do classificador é analisado com base na matriz de confusão. As métricas "
        "derivadas são definidas como:")
    items = [
        "Acurácia = (VP + VN) / (VP + VN + FP + FN)",
        "Precisão = VP / (VP + FP)",
        "Revocação (Recall) = VP / (VP + FN)",
        "F1-Score = 2 · (Precisão × Revocação) / (Precisão + Revocação)",
    ]
    for item in items:
        pdf.set_body(italic=True, size=SIZE_BODY)
        pdf.set_x(MARGIN_LEFT + INDENT)
        pdf.multi_cell(CONTENT_W - INDENT, LINE_H, item, align="L")
    pdf.ln(1)
    pdf.para(
        "Em triagem clínica, os Falsos Negativos — pacientes doentes classificados como saudáveis "
        "— são o erro de maior impacto, pois podem resultar em ausência de tratamento para pacientes "
        "em risco.")

    pdf.section("1.7", "O KNN no Contexto do Aprendizado em Conjunto")
    pdf.para(
        "Mienye e Sun (2022) classificam o KNN como um algoritmo estável: pequenas perturbações nos "
        "dados de treinamento produzem variações mínimas no modelo. Essa estabilidade implica que "
        "técnicas de bagging têm eficácia reduzida com o KNN como aprendiz de base.")
    pdf.quote_block(
        '"k-nearest Neighbor (KNN) and naïve Bayes are examples of stable algorithms, and bagging '
        "does not perform well with these algorithms as base learners\" (MIENYE; SUN, 2022, p. 99136).")
    pdf.para(
        "Contudo, o KNN é frequentemente empregado em sistemas de conjunto heterogêneos, contribuindo "
        "com seu padrão de erros distinto para aumentar a diversidade do ensemble. Velusamy e Ramasamy "
        "(2021, apud MIENYE; SUN, 2022) propuseram um classificador heterogêneo combinando SVM, KNN e "
        "Random Forest para detecção de doença cardíaca, alcançando 100% de acurácia com votação "
        "ponderada. Nanglia et al. (2022, apud MIENYE; SUN, 2022) igualmente utilizaram o KNN em uma "
        "pilha de múltiplos classificadores para detecção de câncer de mama, obtendo 78% de acurácia.")

    # =======================================================================
    # 2. METODOLOGIA
    # =======================================================================
    pdf.section("2", "Metodologia")

    pdf.section("2.1", "Conjunto de Dados")
    pdf.para(
        "O estudo utiliza o Cleveland Heart Disease Dataset, disponibilizado pelo UCI Machine "
        "Learning Repository sob o identificador id=45 (JANOSI et al., 1988). O dataset original "
        "contém 303 registros e 14 atributos — 13 preditores clínicos e 1 variável alvo com 5 classes "
        "(0 = sem doença; 1 a 4 = graus crescentes). Após remoção de registros com valores ausentes, "
        "restaram 297 registros válidos. A Tabela 1 descreve os atributos utilizados.")
    pdf.ln(2)

    # Tabela 1
    pdf.table_caption("Tabela 1 – Atributos do Cleveland Heart Disease Dataset")
    headers1 = ["Atributo", "Descrição", "Tipo"]
    rows1 = [
        ("age",      "Idade do paciente (anos)",                       "Numérico"),
        ("sex",      "Sexo (1 = masculino; 0 = feminino)",             "Binário"),
        ("cp",       "Tipo de dor torácica (0–3)",                     "Categórico"),
        ("trestbps", "Pressão arterial em repouso (mmHg)",             "Numérico"),
        ("chol",     "Colesterol sérico (mg/dl)",                      "Numérico"),
        ("fbs",      "Glicemia em jejum > 120 mg/dl (1/0)",            "Binário"),
        ("restecg",  "Resultado do ECG em repouso (0–2)",              "Categórico"),
        ("thalach",  "Frequência cardíaca máxima (bpm)",               "Numérico"),
        ("exang",    "Angina induzida por exercício (1/0)",            "Binário"),
        ("oldpeak",  "Depressão do segmento ST",                       "Numérico"),
        ("slope",    "Inclinação do segmento ST de pico",              "Categórico"),
        ("ca",       "Número de vasos coloridos (0–3)",                "Ordinal"),
        ("thal",     "Resultado do teste de estresse com tálio",       "Categórico"),
    ]
    widths1 = [28, 108, 34]
    aligns1 = [["L", "L", "C"]] * len(rows1)
    pdf.simple_table(headers1, rows1, widths1, header_align=["C","C","C"],
                     row_aligns=aligns1)
    pdf.table_source("Fonte: JANOSI et al. (1988).")

    pdf.section("2.2", "Binarização da Variável Alvo")
    pdf.para(
        "O dataset original apresenta 5 classes, introduzindo ambiguidade entre graus intermediários "
        "de doença. Adotou-se a binarização da variável alvo, estratégia amplamente utilizada na "
        "literatura para este dataset (MIENYE; SUN, 2022):")
    pdf.set_body(italic=True, size=SIZE_BODY)
    pdf.set_x(MARGIN_LEFT + INDENT)
    pdf.multi_cell(CONTENT_W - INDENT, LINE_H,
        "y_binário = 0  se y_original = 0  (Saudável)\n"
        "y_binário = 1  se y_original > 0  (Doente)",
        align="L")
    pdf.ln(1)
    pdf.para(
        "Essa redução de 5 para 2 classes simplifica a interpretação clínica e melhora o desempenho "
        "do modelo, eliminando ambiguidades entre classes intermediárias.")

    pdf.section("2.3", "Pipeline de Pré-processamento")
    pdf.para(
        "O pipeline compreende três etapas sequenciais:")
    pdf.set_body(bold=True, size=SIZE_BODY)
    pdf.set_x(MARGIN_LEFT)
    pdf.write(LINE_H, "Etapa 1 — Remoção de valores ausentes: ")
    pdf.set_body(size=SIZE_BODY)
    pdf.write(LINE_H,
        "registros com NaN em qualquer atributo foram descartados. Dos 303 registros originais, "
        "6 foram removidos, resultando em 297 registros válidos.")
    pdf.ln(LINE_H)
    pdf.set_body(bold=True, size=SIZE_BODY)
    pdf.set_x(MARGIN_LEFT)
    pdf.write(LINE_H, "Etapa 2 — Padronização Z-score: ")
    pdf.set_body(size=SIZE_BODY)
    pdf.write(LINE_H,
        "todos os 13 atributos foram padronizados com StandardScaler, calculando média e desvio "
        "padrão exclusivamente sobre X_train para evitar data leakage.")
    pdf.ln(LINE_H)
    pdf.set_body(bold=True, size=SIZE_BODY)
    pdf.set_x(MARGIN_LEFT)
    pdf.write(LINE_H, "Etapa 3 — Particionamento estratificado: ")
    pdf.set_body(size=SIZE_BODY)
    pdf.write(LINE_H,
        "os dados foram divididos em 80% treinamento (237 registros) e 20% teste (60 registros) "
        "com estratificação pela variável alvo (stratify=y, random_state=42).")
    pdf.ln(LINE_H + 2)

    pdf.section("2.4", "Otimização do Hiperparâmetro K")
    pdf.para(
        "A busca pelo melhor K foi conduzida com GridSearchCV sobre o intervalo "
        "K em {1, 2, ..., 30}, empregando validação cruzada estratificada de 5 dobras "
        "(StratifiedKFold) sobre X_train, com critério scoring='accuracy':")
    pdf.set_body(italic=True, size=SIZE_BODY)
    pdf.set_x(MARGIN_LEFT + INDENT)
    pdf.multi_cell(CONTENT_W - INDENT, LINE_H,
        "K* = argmax_{k em {1,...,30}}  (1/5) SUM_{i=1}^{5} Acc(k, dobra_i)",
        align="L")
    pdf.ln(1)

    pdf.section("2.5", "Protocolo de Avaliação Final")
    pdf.para(
        "Após definido K* = 29, o modelo foi retreinado com todos os dados de treinamento e avaliado "
        "em três instâncias:")
    evals = [
        "Conjunto de teste (hold-out de 20%, 60 registros): avaliação em dados não vistos durante "
        "o treinamento.",
        "Validação cruzada 10-fold sobre os 297 registros: métrica de referência mais robusta.",
        "Conjunto completo (297 registros): análise granular em blocos consecutivos de 50 registros.",
    ]
    for i, e in enumerate(evals, 1):
        pdf.set_body(size=SIZE_BODY)
        pdf.set_x(MARGIN_LEFT + INDENT)
        pdf.multi_cell(CONTENT_W - INDENT, LINE_H, f"{i}. {e}", align="J")
    pdf.ln(1)

    # Algoritmo 1 (pseudocódigo em caixa)
    pdf.set_body(bold=True, size=SIZE_SMALL)
    pdf.set_x(MARGIN_LEFT)
    pdf.cell(CONTENT_W, LINE_H_SM, "Algoritmo 1 – KNN para Classificação de Doença Cardíaca",
             border="TB", align="C")
    pdf.ln(LINE_H_SM)
    algo_lines = [
        "Entrada : Dataset UCI Heart Disease (id=45), K_RANGE = {1,...,30}",
        "Saída   : Modelo KNN otimizado e relatório de classificação",
        "",
        "1. CARREGAR dados via ucimlrepo.fetch_ucirepo(id=45)",
        "2. SELECIONAR os 13 atributos clínicos da Tabela 1",
        "3. REMOVER registros com valores ausentes  ->  297 registros",
        "4. BINARIZAR alvo: y = 1 se y_orig > 0; y = 0 caso contrário",
        "5. PADRONIZAR: X_scaled = StandardScaler().fit(X_train).transform(X)",
        "6. PARTICIONAR: train/test (80%/20%), stratify=y, random_state=42",
        "7. OTIMIZAR K via GridSearchCV + StratifiedKFold(5):",
        "       K* = argmax Acc(k) para k em {1,...,30}  ->  K* = 29",
        "8. TREINAR: KNeighborsClassifier(n_neighbors=29).fit(X_train, y_train)",
        "9. AVALIAR em teste, validação cruzada 10-fold e conjunto completo",
        "10. GERAR confusion_matrix e classification_report",
    ]
    pdf.set_body(size=SIZE_SMALL)
    for line in algo_lines:
        pdf.set_x(MARGIN_LEFT + 5)
        pdf.cell(CONTENT_W - 5, LINE_H_TBL + 0.5, line)
        pdf.ln(LINE_H_TBL + 0.5)
    pdf.set_body(size=SIZE_SMALL)
    pdf.set_x(MARGIN_LEFT)
    pdf.cell(CONTENT_W, 1, "", border="B")
    pdf.ln(4)

    # =======================================================================
    # 3. RESULTADOS E DISCUSSÃO
    # =======================================================================
    pdf.section("3", "Resultados e Discussão")

    pdf.section("3.1", "Otimização do Hiperparâmetro K")
    pdf.para(
        "A Tabela 2 apresenta os 5 melhores valores de K identificados na busca em grade:")
    pdf.ln(2)

    pdf.table_caption("Tabela 2 – Top-5 valores de K na validação cruzada (5-fold, conjunto de treino)")
    headers2 = ["K", "Acurácia CV Média"]
    rows2 = [
        ("29 (melhor)", "83,97%"),
        ("27",          "83,55%"),
        ("17",          "83,55%"),
        ("30",          "83,55%"),
        ("26",          "83,55%"),
    ]
    widths2 = [50, 120]
    pdf.simple_table(headers2, rows2, widths2, header_align=["C","C"],
                     row_aligns=[["C","C"]]*len(rows2))
    pdf.table_source("Fonte: elaborada pelo autor (2026).")

    pdf.para(
        "O agrupamento dos melhores resultados na faixa K em [17, 30] indica que o dataset "
        "apresenta padrões relativamente suaves que beneficiam vizinhanças maiores. K menores "
        "(K < 10) apresentaram maior variabilidade entre dobras, evidenciando sensibilidade a ruídos "
        "locais (overfitting). O fato de K = 30 ter desempenho marginalmente inferior a K = 29 sugere "
        "que o modelo começa a perder resolução local nessa fronteira, consistente com o trade-off "
        "viés-variância descrito por Géron (2019).")

    pdf.section("3.2", "Acurácia por Blocos de Registros")
    pdf.para(
        "A Tabela 3 apresenta a distribuição de acurácia por blocos consecutivos sobre os "
        "297 pacientes:")
    pdf.ln(2)

    pdf.table_caption(
        "Tabela 3 – Acurácia do KNN (K=29) por bloco de registros")
    headers3 = ["Bloco", "Registros", "Acertos", "Acurácia (%)"]
    rows3 = [
        ("1", "1 – 50",   "45/50",  "90,00"),
        ("2", "51 – 100", "42/50",  "84,00"),
        ("3", "101 – 150","45/50",  "90,00"),
        ("4", "151 – 200","40/50",  "80,00"),
        ("5", "201 – 250","43/50",  "86,00"),
        ("6", "251 – 297","37/47",  "78,72"),
        ("Total", "1 – 297", "252/297", "84,85"),
    ]
    widths3 = [22, 40, 35, 73]
    pdf.simple_table(headers3, rows3, widths3,
                     header_align=["C","C","C","C"],
                     row_aligns=[["C","C","C","C"]]*len(rows3))
    pdf.table_source("Fonte: elaborada pelo autor (2026).")

    pdf.para(
        "A variação entre blocos (78,72% a 90,00%) reflete a heterogeneidade das amostras. O "
        "bloco 6 apresentou o menor desempenho (78,72%), possivelmente por conter maior proporção "
        "de casos ambíguos — pacientes cujo perfil de atributos se sobrepõe às duas classes na "
        "vizinhança de K = 29. Os blocos 1 e 3 atingiram 90,00%, sugerindo regiões do espaço de "
        "características com fronteiras de decisão mais bem definidas.")

    pdf.section("3.3", "Métricas Consolidadas do Modelo")
    pdf.para(
        "A Tabela 4 resume o desempenho global do classificador:")
    pdf.ln(2)

    pdf.table_caption("Tabela 4 – Resumo de desempenho do classificador KNN (K=29)")
    headers4 = ["Métrica", "Valor"]
    rows4 = [
        ("Acurácia — conjunto de teste (hold-out 20%)", "86,67%"),
        ("Acurácia — validação cruzada 10-fold (métrica principal)", "82,86% ± 6,99%"),
        ("Acurácia — conjunto completo (297 registros)", "84,85%"),
        ("K (vizinhos)", "29"),
        ("Total de registros avaliados", "297"),
    ]
    widths4 = [120, 50]
    pdf.simple_table(headers4, rows4, widths4,
                     header_align=["C","C"],
                     row_aligns=[["L","C"]]*len(rows4))
    pdf.table_source("Fonte: elaborada pelo autor (2026).")

    pdf.para(
        "A validação cruzada 10-fold (82,86% ± 6,99%) é a métrica de referência mais confiável, "
        "pois estima a capacidade de generalização por meio de 10 partições independentes. O desvio "
        "padrão de ±6,99% é esperado para um dataset de tamanho moderado (297 registros), conforme "
        "aponta Géron (2019). A avaliação qualitativa do modelo é classificada como BOA: acurácias de "
        "cross-validation entre 75% e 85% indicam que o modelo classifica bem a maioria dos casos, "
        "com margem para melhoria por algoritmos mais sofisticados.")

    pdf.section("3.4", "Matriz de Confusão")
    pdf.para(
        "A Tabela 5 apresenta a matriz de confusão sobre os 60 registros do conjunto de teste:")
    pdf.ln(2)

    pdf.table_caption("Tabela 5 – Matriz de confusão (conjunto de teste, n=60)")
    pdf.confusion_matrix()
    pdf.table_source("Fonte: elaborada pelo autor (2026).")

    pdf.para(
        "Os 6 Falsos Negativos representam o erro mais crítico em termos clínicos: pacientes com "
        "doença cardíaca que receberiam diagnóstico negativo pelo modelo. Com 28 pacientes doentes "
        "no conjunto de teste, isso equivale a uma taxa de falsos negativos de 21,4% — aceitável "
        "para um modelo de referência, porém insuficiente para uso clínico autônomo sem supervisão "
        "médica.")

    pdf.section("3.5", "Relatório de Classificação por Classe")
    pdf.para(
        "A Tabela 6 apresenta o relatório completo de classificação:")
    pdf.ln(2)

    pdf.table_caption("Tabela 6 – Relatório de classificação (conjunto de teste, n=60)")
    headers6 = ["Classe", "Precisão", "Revocação", "F1-Score", "Suporte"]
    rows6 = [
        ("Saudável (0)", "0,83", "0,94", "0,88", "32"),
        ("Doente (1)",   "0,92", "0,79", "0,85", "28"),
        ("Acurácia geral", "",    "",     "0,87", "60"),
        ("Média macro",   "0,88", "0,86", "0,86", "60"),
        ("Média ponderada","0,87","0,87", "0,87", "60"),
    ]
    widths6 = [46, 26, 28, 26, 24]
    pdf.simple_table(headers6, rows6, widths6,
                     header_align=["C","C","C","C","C"],
                     row_aligns=[["L","C","C","C","C"]]*len(rows6))
    pdf.table_source("Fonte: elaborada pelo autor (2026).")

    pdf.para(
        "A análise por classe revela: (i) precisão da classe Doente = 0,92 — quando o modelo prevê "
        "\"Doente\", está correto em 92% dos casos; (ii) revocação da classe Doente = 0,79 — o modelo "
        "detecta 79% dos pacientes efetivamente doentes; (iii) F1-Score equilibrado (0,85 e 0,88) — "
        "sem desvio marcante para nenhuma das classes; (iv) F1-Score macro médio = 0,86 — confirma "
        "desempenho equilibrado entre as duas classes.")

    pdf.section("3.6", "Análise Qualitativa dos Erros")
    pdf.para(
        "Os 45 erros observados nos 297 registros (15,15% do total) se dividem em dois padrões:")
    pdf.set_body(bold=True, size=SIZE_BODY)
    pdf.set_x(MARGIN_LEFT)
    pdf.write(LINE_H, "Falsos Negativos (doente classificado como saudável): ")
    pdf.set_body(size=SIZE_BODY)
    pdf.write(LINE_H,
        "ocorrem quando um paciente doente possui perfil clínico semelhante ao de pacientes "
        "saudáveis na vizinhança de K = 29. Exemplos: registros 17, 23, 34, 45, 52, 53 e 58.")
    pdf.ln(LINE_H)
    pdf.set_body(bold=True, size=SIZE_BODY)
    pdf.set_x(MARGIN_LEFT)
    pdf.write(LINE_H, "Falsos Positivos (saudável classificado como doente): ")
    pdf.set_body(size=SIZE_BODY)
    pdf.write(LINE_H,
        "ocorrem quando um paciente saudável apresenta características próximas às de pacientes "
        "doentes no espaço padronizado. Exemplos: registros 33 e 81.")
    pdf.ln(LINE_H + 2)
    pdf.para(
        "Esse padrão é inerente ao KNN, que toma decisões estritamente locais sem capturar relações "
        "globais entre atributos, especialmente interações não lineares entre variáveis como cp "
        "(tipo de dor torácica), thal (resultado do tálio), ca (vasos coloridos) e oldpeak "
        "(depressão do ST) — as mais preditivas do Cleveland dataset segundo a literatura "
        "(MIENYE; SUN, 2022).")

    pdf.section("3.7", "Comparação com a Literatura")
    pdf.para(
        "A Tabela 7 compara os resultados obtidos com trabalhos aplicados ao mesmo dataset:")
    pdf.ln(2)

    pdf.table_caption(
        "Tabela 7 – Comparação com a literatura (Cleveland Heart Disease Dataset)")
    headers7 = ["Referência", "Algoritmo", "Acurácia"]
    rows7 = [
        ("Este trabalho", "KNN (K=29, binário)", "86,67% (teste) / 82,86% (CV-10)"),
        ("GAO et al. (2021)", "Random Forest + PCA/LDA", "98,6%"),
        ("MIENYE et al. (2020)", "WAE + CART (ensemble)", "93,0%"),
        ("VELUSAMY; RAMASAMY (2021)", "Ensemble SVM + KNN + RF (WAV)", "100%"),
        ("MIENYE; SUN (2022)", "XGBoost + SMOTE-ENN + RFE", "95,6%"),
    ]
    widths7 = [50, 64, 56]
    pdf.simple_table(headers7, rows7, widths7,
                     header_align=["C","C","C"],
                     row_aligns=[["L","L","C"]]*len(rows7))
    pdf.table_source("Fonte: MIENYE; SUN (2022).")

    pdf.para(
        "O KNN com K = 29 obtém desempenho competitivo como algoritmo de referência (baseline), "
        "sendo superado pelos métodos ensemble e pelos algoritmos baseados em árvores de decisão. "
        "Essa diferença ilustra a afirmação de Mienye e Sun (2022), segundo a qual ")
    pdf.quote_block(
        '"ensemble classifiers are more robust and perform better than the individual ensemble '
        "learners\" (MIENYE; SUN, 2022, p. 99129).")
    pdf.para(
        "Vale destacar que o resultado de 100% de Velusamy e Ramasamy (2021) foi obtido com um "
        "ensemble que inclui o próprio KNN como componente, reforçando que o KNN, embora limitado "
        "individualmente, agrega valor quando combinado com outros classificadores em arquiteturas "
        "heterogêneas.")

    # =======================================================================
    # CONSIDERAÇÕES FINAIS
    # =======================================================================
    pdf.section("", "Considerações Finais", level=0)
    pdf.para(
        "Este trabalho apresentou a aplicação do algoritmo K-Nearest Neighbors para classificação "
        "binária de doença cardíaca sobre o Cleveland Heart Disease Dataset, com ênfase nos "
        "fundamentos matemáticos, nas decisões metodológicas de implementação e na análise rigorosa "
        "dos resultados experimentais.")
    pdf.para("Os principais achados são:")

    conclusoes = [
        ("1.", "O KNN com K = 29 obteve acurácia de 86,67% no conjunto de teste e 82,86% ± 6,99% "
         "na validação cruzada de 10 dobras, desempenho classificado como BOM e competitivo para "
         "um algoritmo não paramétrico de baixa complexidade computacional."),
        ("2.", "A binarização da variável alvo (5 classes → 2 classes) foi decisiva: eliminou "
         "ambiguidades entre graus intermediários da doença e tornou o problema clinicamente "
         "mais interpretável."),
        ("3.", "A padronização Z-score é condição necessária para o KNN operar corretamente sobre "
         "dados heterogêneos com escalas distintas, conforme ressaltado por Géron (2019)."),
        ("4.", "A validação cruzada 10-fold (82,86%) é a métrica de referência mais honesta para "
         "o TCC, por avaliar o modelo em dados não utilizados no treinamento por meio de 10 "
         "partições independentes."),
        ("5.", "As limitações do KNN ficam evidentes nos 45 erros observados: o algoritmo não "
         "captura relações globais entre atributos nem interações não lineares, sendo superado "
         "por métodos ensemble como XGBoost e Random Forest que, segundo Mienye e Sun (2022), "
         "regularmente atingem 93% a 98% de acurácia no mesmo dataset."),
    ]
    for num, texto in conclusoes:
        pdf.set_body(size=SIZE_BODY)
        pdf.set_x(MARGIN_LEFT + INDENT)
        pdf.multi_cell(CONTENT_W - INDENT, LINE_H, f"{num} {texto}", align="J")
        pdf.ln(1)

    pdf.para(
        "Como trabalho futuro, recomenda-se: (i) aplicar seleção de atributos por Recursive "
        "Feature Elimination (RFE) para identificar as variáveis mais informativas (cp, thal, ca, "
        "oldpeak, exang); (ii) comparar formalmente o KNN com Random Forest e XGBoost sobre o mesmo "
        "protocolo experimental; (iii) investigar métricas de distância alternativas (Manhattan, "
        "Minkowski com p ≠ 2); e (iv) avaliar o impacto de técnicas de balanceamento de classes "
        "como SMOTE sobre a revocação da classe Doente.")

    # =======================================================================
    # REFERÊNCIAS
    # =======================================================================
    pdf.section("", "Referências", level=0)

    refs = [
        "COVER, T. M.; HART, P. E. Nearest neighbor pattern classification. IEEE Transactions on "
        "Information Theory, v. 13, n. 1, p. 21–27, 1967. DOI: 10.1109/TIT.1967.1053964.",

        "FIX, E.; HODGES, J. L. Discriminatory Analysis: Nonparametric Discrimination, Consistency "
        "Properties. USAF School of Aviation Medicine, Randolph Field, Texas. Technical Report n. 4, "
        "1951.",

        "GÉRON, Aurélien. Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow: "
        "Concepts, Tools, and Techniques to Build Intelligent Systems. 2. ed. Sebastopol, CA: "
        "O'Reilly Media, 2019.",

        "GIRALDI, Gilson Antonio. Machine Learning and Pattern Recognition. Notas de Aula do "
        "Programa de Pós-Graduação. Petrópolis, RJ: UFRJ, 2021.",

        "JANOSI, A.; STEINBRUNN, W.; PFISTERER, M.; DETRANO, R. Heart Disease Dataset. UCI Machine "
        "Learning Repository, 1988. Disponível em: https://archive.ics.uci.edu/dataset/45/"
        "heart+disease. Acesso em: mar. 2026.",

        "MIENYE, I. D.; SUN, Y. A Survey of Ensemble Learning: Concepts, Algorithms, Applications, "
        "and Prospects. IEEE Access, v. 10, p. 99129–99149, 2022. "
        "DOI: 10.1109/ACCESS.2022.3207287.",

        "PEDREGOSA, F. et al. Scikit-learn: Machine Learning in Python. Journal of Machine Learning "
        "Research, v. 12, p. 2825–2830, 2011. Disponível em: "
        "https://jmlr.org/papers/v12/pedregosa11a.html. Acesso em: mar. 2026.",
    ]
    for ref in refs:
        pdf.ref_entry(ref)

    return pdf


if __name__ == "__main__":
    pdf = build_pdf()
    out_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "Artigo_KNN_Doenca_Cardiaca_FATEC.pdf"
    )
    pdf.output(out_path)
    print(f"PDF gerado com sucesso: {out_path}")
