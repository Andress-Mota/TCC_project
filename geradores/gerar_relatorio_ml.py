# -*- coding: utf-8 -*-
"""
RelatÃ³rio tÃ©cnico sobre TÃ©cnicas de Aprendizado de MÃ¡quina em PDF
conforme normas FATEC GuaratinguetÃ¡ 2022.
Mesmo algoritmo (KNN/Cleveland), resultados e literatura do artigo principal.
"""

from fpdf import FPDF
import os

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


class RelatorioFATEC(FPDF):

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
        if lh is None:
            lh = LINE_H if size == SIZE_BODY else LINE_H_SM
        self.set_body(bold=bold, italic=italic, size=size)
        if indent:
            self.set_x(MARGIN_LEFT + INDENT)
            self.multi_cell(CONTENT_W - INDENT, lh, text, align=align)
        else:
            self.set_x(MARGIN_LEFT)
            self.multi_cell(CONTENT_W, lh, text, align=align)

    def section(self, num, title):
        self.ln(3)
        self.set_body(bold=True, size=SIZE_BODY)
        label = (f"{num} {title}").strip()
        self.set_x(MARGIN_LEFT)
        self.multi_cell(CONTENT_W, LINE_H, label, align="L")
        self.ln(1)

    def center_line(self, text, size=SIZE_BODY, bold=False, italic=False):
        lh = LINE_H if size >= SIZE_BODY else LINE_H_SM
        self.set_body(bold=bold, italic=italic, size=size)
        self.set_x(MARGIN_LEFT)
        self.multi_cell(CONTENT_W, lh, text, align="C")

    def quote_block(self, text):
        self.set_body(size=SIZE_SMALL)
        self.set_x(MARGIN_LEFT + 40)
        self.multi_cell(CONTENT_W - 40, LINE_H_SM, text, align="J")
        self.ln(2)

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

    def draw_hline(self):
        self.set_draw_color(0)
        self.set_line_width(0.3)
        self.line(MARGIN_LEFT, self.get_y(), PAGE_W - MARGIN_RIGHT, self.get_y())
        self.ln(1)

    def pros_cons(self, items):
        """Lista de pontos fortes (+) e fracos (-) com prefixo em negrito."""
        for prefix, text in items:
            self.set_x(MARGIN_LEFT + INDENT)
            self.set_body(bold=True, size=SIZE_BODY)
            pw = self.get_string_width(prefix + " ")
            self.set_x(MARGIN_LEFT + INDENT)
            self.set_body(size=SIZE_BODY)
            self.multi_cell(CONTENT_W - INDENT, LINE_H,
                            f"{prefix} {text}", align="J")
        self.ln(1)

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


# ===========================================================================
# ConteÃºdo do relatÃ³rio
# ===========================================================================

def build_relatorio():
    pdf = RelatorioFATEC(orientation="P", unit="mm", format="A4")
    pdf.set_margins(MARGIN_LEFT, MARGIN_TOP, MARGIN_RIGHT)
    pdf.set_auto_page_break(auto=True, margin=MARGIN_BOTTOM)
    pdf.add_page()

    # -----------------------------------------------------------------------
    # TÃTULO
    # -----------------------------------------------------------------------
    pdf.set_body(bold=True, size=SIZE_TITLE)
    pdf.set_x(MARGIN_LEFT)
    pdf.multi_cell(CONTENT_W, LINE_H,
        "K-NEAREST NEIGHBORS APLICADO AO DIAGNÃ“STICO DE DOENÃ‡A CARDÃACA: "
        "FUNDAMENTOS MATEMÃTICOS, IMPLEMENTAÃ‡ÃƒO E ANÃLISE DE DESEMPENHO",
        align="C")
    pdf.ln(2)

    pdf.center_line("AndrÃ© Felipe", size=SIZE_SMALL, italic=True)
    pdf.center_line("Faculdade de Tecnologia de GuaratinguetÃ¡", size=SIZE_SMALL, italic=True)
    pdf.center_line("andressmota78@gmail.com", size=SIZE_SMALL, italic=True)
    pdf.ln(4)

    # -----------------------------------------------------------------------
    # RESUMO
    # -----------------------------------------------------------------------
    pdf.set_body(bold=True)
    pdf.set_x(MARGIN_LEFT)
    pdf.cell(CONTENT_W, LINE_H, "Resumo", align="L")
    pdf.ln(1)
    pdf.para(
        "Este relatÃ³rio apresenta a aplicaÃ§Ã£o do algoritmo K-Nearest Neighbors (KNN) para a "
        "classificaÃ§Ã£o binÃ¡ria de doenÃ§a cardÃ­aca utilizando o Cleveland Heart Disease Dataset "
        "(UCI Machine Learning Repository). SÃ£o cobertos os fundamentos matemÃ¡ticos do "
        "algoritmo, incluindo mÃ©tricas de distÃ¢ncia, regra de votaÃ§Ã£o majoritÃ¡ria e seleÃ§Ã£o do "
        "hiperparÃ¢metro K por validaÃ§Ã£o cruzada estratificada. A implementaÃ§Ã£o foi desenvolvida "
        "em Python com scikit-learn, empregando padronizaÃ§Ã£o Z-score, particionamento "
        "estratificado e otimizaÃ§Ã£o automÃ¡tica de K via GridSearchCV. O melhor valor encontrado "
        "foi K = 29, obtendo acurÃ¡cia de 86,67% no conjunto de teste e 82,86% +/- 6,99% na "
        "validaÃ§Ã£o cruzada de 10 dobras sobre 297 registros avaliados.",
        indent=False)
    pdf.ln(1)
    pdf.set_font(FONT, "B", SIZE_BODY)
    pdf.set_x(MARGIN_LEFT)
    pdf.write(LINE_H, "Palavras-chave: ")
    pdf.set_body()
    pdf.write(LINE_H,
        "K-Nearest Neighbors; Aprendizado de MÃ¡quina; DoenÃ§a CardÃ­aca; "
        "ClassificaÃ§Ã£o BinÃ¡ria; ValidaÃ§Ã£o Cruzada.")
    pdf.ln(6)

    # =======================================================================
    # INTRODUÃ‡ÃƒO
    # =======================================================================
    pdf.section("", "IntroduÃ§Ã£o")
    pdf.para(
        "As doenÃ§as cardiovasculares representam a principal causa de mortalidade global segundo "
        "a OrganizaÃ§Ã£o Mundial da SaÃºde. O diagnÃ³stico precoce Ã© essencial para reduzir Ã³bitos "
        "e custos hospitalares, mas exames como eletrocardiogramas avanÃ§ados e "
        "cineangiocoronariografias possuem alto custo e disponibilidade limitada, especialmente "
        "em paÃ­ses em desenvolvimento (MIENYE; SUN, 2022).")
    pdf.para(
        "O aprendizado de mÃ¡quina (AM) tem se consolidado como ferramenta de suporte Ã  decisÃ£o "
        "clÃ­nica, sendo aplicado ao diagnÃ³stico de diabetes, hipertensÃ£o, cÃ¢ncer e doenÃ§as "
        "renais. GÃ©ron (2019, p. 4) destaca que algoritmos de classificaÃ§Ã£o podem identificar "
        "padrÃµes em dados clÃ­nicos com acurÃ¡cia comparÃ¡vel Ã  de especialistas, democratizando "
        "o acesso Ã  triagem mÃ©dica.")
    pdf.para(
        "Dentre os algoritmos de classificaÃ§Ã£o supervisionada, o K-Nearest Neighbors (KNN) se "
        "destaca pela simplicidade conceitual, transparÃªncia matemÃ¡tica e facilidade de "
        "implementaÃ§Ã£o. Por nÃ£o construir um modelo explÃ­cito durante o treinamento, Ã© "
        "classificado como algoritmo de aprendizado lazy (preguiÃ§oso) e baseado em instÃ¢ncias "
        "(GÃ‰RON, 2019). Essa caracterÃ­stica o torna especialmente adequado para aplicaÃ§Ãµes "
        "clÃ­nicas onde a interpretabilidade Ã© relevante.")
    pdf.para(
        "Este relatÃ³rio tem como objetivos: (i) fundamentar matematicamente o algoritmo KNN; "
        "(ii) descrever a metodologia de implementaÃ§Ã£o sobre o Cleveland Heart Disease Dataset; "
        "(iii) apresentar e analisar os resultados experimentais; e (iv) discutir o comportamento "
        "do modelo, suas potencialidades e suas limitaÃ§Ãµes no contexto do diagnÃ³stico cardÃ­aco.")

    # =======================================================================

    # =======================================================================
    # 1. REFERENCIAL TEÓRICO
    # =======================================================================
    pdf.section("1", "Referencial Teórico")

    pdf.section("1.1", "O Algoritmo K-Nearest Neighbors")
    pdf.para(
        "O algoritmo KNN foi proposto por Fix e Hodges (1951) e formalizado por Cover e Hart "
        "(1967). Sua premissa central e que amostras semelhantes tendem a pertencer a mesma "
        "classe: um ponto de consulta e classificado pela maioria de seus K vizinhos mais "
        "proximos no espaco de caracteristicas.")
    pdf.para(
        "Formalmente, dado um conjunto de treinamento D = {(x1,y1),...,(xn,yn)}, onde xi "
        "representa o vetor de atributos do i-esimo registro e yi o respectivo rotulo de "
        "classe, a predicao para uma nova amostra xq e definida por:")
    pdf.set_body(italic=True)
    pdf.set_x(MARGIN_LEFT + INDENT)
    pdf.multi_cell(CONTENT_W - INDENT, LINE_H,
        "y_hat = argmax_c  SUM_{i em N_K(xq)}  1[yi = c]", align="L")
    pdf.ln(1)
    pdf.para(
        "onde N_K(xq) representa o conjunto dos K indices cujos vetores de atributos estao "
        "mais proximos de xq segundo uma metrica de distancia, e 1[.] e a funcao indicadora. "
        "Na classificacao binaria adotada (c em {0,1}), a regra de decisao se reduz a:")
    pdf.set_body(italic=True)
    pdf.set_x(MARGIN_LEFT + INDENT)
    pdf.multi_cell(CONTENT_W - INDENT, LINE_H,
        "y_hat = 1  se  SUM_{i em N_K(xq)} yi > K/2;   y_hat = 0  caso contrario", align="L")
    pdf.ln(1)
    pdf.para(
        "O modelo nao ajusta nenhum parametro durante o treinamento: toda a computacao ocorre "
        "no momento da previsao, justificando sua classificacao como algoritmo lazy. O custo "
        "de predicao cresce linearmente com o tamanho do conjunto de treinamento.")

    pdf.section("1.2", "Metricas de Distancia")
    pdf.para(
        "A qualidade das vizinhancas depende diretamente da metrica de distancia utilizada. "
        "A familia de metricas de Minkowski oferece uma generalizacao unificada das distancias "
        "mais empregadas em aprendizado de maquina:")
    pdf.set_body(italic=True)
    pdf.set_x(MARGIN_LEFT + INDENT)
    pdf.multi_cell(CONTENT_W - INDENT, LINE_H,
        "d_p(x,z) = ( SUM_{j=1}^{d} |xj - zj|^p )^(1/p)", align="L")
    pdf.ln(1)
    pdf.para(
        "Os tres casos especiais mais relevantes sao:")
    for lbl, formula, desc in [
        ("Euclidiana (p=2):",
         "d_E(x,z) = SQRT( SUM_{j=1}^{d} (xj-zj)^2 )",
         "metrica padrao do KNeighborsClassifier do scikit-learn; equivale a linha reta "
         "entre dois pontos no espaco d-dimensional. Adotada neste trabalho."),
        ("Manhattan (p=1):",
         "d_M(x,z) = SUM_{j=1}^{d} |xj - zj|",
         "soma diferencas absolutas atributo a atributo; menos sensivel a valores extremos."),
        ("Chebyshev (p->inf):",
         "d_inf(x,z) = max_j |xj - zj|",
         "considera apenas o atributo com maior diferenca absoluta entre os pontos."),
    ]:
        pdf.set_body(bold=True, size=SIZE_BODY)
        pdf.set_x(MARGIN_LEFT + INDENT)
        pdf.multi_cell(CONTENT_W - INDENT, LINE_H, lbl, align="L")
        pdf.set_body(italic=True)
        pdf.set_x(MARGIN_LEFT + INDENT * 2)
        pdf.multi_cell(CONTENT_W - INDENT * 2, LINE_H, formula, align="L")
        pdf.set_body(size=SIZE_BODY)
        pdf.set_x(MARGIN_LEFT + INDENT)
        pdf.multi_cell(CONTENT_W - INDENT, LINE_H, desc, align="J")
        pdf.ln(1)

    pdf.section("1.3", "Necessidade de Normalizacao dos Atributos")
    pdf.para(
        "Por basear toda a decisao em distancias, o KNN e altamente sensivel a escala dos "
        "atributos. Sem normalizacao, um atributo com amplitude numerica elevada — como "
        "pressao arterial (80-200 mmHg) — dominaria o calculo em relacao a atributos binarios "
        "(0 ou 1), distorcendo as vizinhancas. Geron (2019) ressalta que a normalizacao e "
        "etapa obrigatoria para algoritmos baseados em distancia.")
    pdf.para(
        "A Padronizacao Z-score (StandardScaler) transforma cada atributo j de modo que a "
        "distribuicao resultante tenha media zero e desvio padrao unitario:")
    pdf.set_body(italic=True)
    pdf.set_x(MARGIN_LEFT + INDENT)
    pdf.multi_cell(CONTENT_W - INDENT, LINE_H,
        "zij = (xij - x_bar_j) / sigma_j", align="L")
    pdf.ln(1)
    pdf.para(
        "Os parametros x_bar_j e sigma_j sao calculados exclusivamente sobre o conjunto de "
        "treinamento. Ao aplica-los ao conjunto de teste, garante-se que nenhuma informacao "
        "do teste contamine o pre-processamento — pratica essencial conhecida como prevencao "
        "de data leakage.")

    pdf.section("1.4", "Hiperparametro K e o Trade-off Vies-Variancia")
    pdf.para(
        "O valor de K controla o tamanho da vizinhanca considerada para cada predicao. "
        "Sua escolha envolve o trade-off vies-variancia:")
    pdf.pros_cons([
        ("K pequeno:",
         "cada predicao depende de pouquissimas amostras — alta variancia, overfitting. "
         "O modelo memoriza os dados de treinamento e generaliza mal."),
        ("K grande:",
         "a vizinhanca abrange grande parte do dataset — alto vies, underfitting. "
         "O modelo perde capacidade de discriminacao local."),
    ])
    pdf.para(
        "O erro esperado de generalizacao pode ser decomposto formalmente como:")
    pdf.set_body(italic=True)
    pdf.set_x(MARGIN_LEFT + INDENT)
    pdf.multi_cell(CONTENT_W - INDENT, LINE_H,
        "Erro(xq) = Vies^2 + Variancia + epsilon   (ruido irredutivel)", align="L")
    pdf.ln(1)
    pdf.para(
        "O objetivo e encontrar o K que minimiza a soma dos dois primeiros termos sobre dados "
        "nao vistos. Para isso, emprega-se a busca em grade com validacao cruzada estratificada "
        "(GridSearchCV + StratifiedKFold):")
    pdf.set_body(italic=True)
    pdf.set_x(MARGIN_LEFT + INDENT)
    pdf.multi_cell(CONTENT_W - INDENT, LINE_H,
        "K* = argmax_{k em {1,...,Kmax}}  (1/v) * SUM_{i=1}^{v} Acc(k, dobra_i)", align="L")
    pdf.ln(1)

    pdf.section("1.5", "Validacao Cruzada Estratificada")
    pdf.para(
        "A validacao cruzada k-fold estratificada (StratifiedKFold) particiona o conjunto D "
        "em v dobras mutuamente exclusivas, mantendo em cada dobra a mesma proporcao de classes "
        "do conjunto original. Para cada dobra i, um modelo treinado em D \\ Di e avaliado "
        "sobre Di:")
    pdf.set_body(italic=True)
    pdf.set_x(MARGIN_LEFT + INDENT)
    pdf.multi_cell(CONTENT_W - INDENT, LINE_H,
        "Acc_CV = (1/v) * SUM_{i=1}^{v} Acc( M_{D\\Di}, Di )", align="L")
    pdf.ln(1)
    pdf.para(
        "Segundo Geron (2019), a validacao cruzada e preferivel a simples divisao treino/teste "
        "porque: (i) aproveita todos os dados disponíveis para treinamento e avaliacao; "
        "(ii) reduz a variancia da estimativa de desempenho; e (iii) e menos dependente de "
        "uma unica particao aleatoria. Esta e a metrica de referencia principal deste trabalho.")

    pdf.section("1.6", "Metricas de Avaliacao de Classificadores Binarios")
    pdf.para(
        "Para classificacao binaria, as predicoes se enquadram em quatro categorias, "
        "organizadas na matriz de confusao:")
    pdf.ln(2)
    pdf.table_caption("Tabela 1 - Estrutura da Matriz de Confusao")
    conf_headers = ["", "Previsto: Saudavel (0)", "Previsto: Doente (1)"]
    conf_rows = [
        ("Real: Saudavel (0)", "VN - Verdadeiro Negativo", "FP - Falso Positivo"),
        ("Real: Doente (1)",   "FN - Falso Negativo",      "VP - Verdadeiro Positivo"),
    ]
    pdf.simple_table(conf_headers, conf_rows, [50, 65, 55],
                     header_align=["C", "C", "C"],
                     row_aligns=[["L", "C", "C"]] * 2)
    pdf.table_source("Fonte: elaborada pelo autor (2026).")
    pdf.para(
        "As metricas derivadas da matriz de confusao sao:")
    for nome, formula in [
        ("Acuracia:",
         "Acc = (VP + VN) / (VP + VN + FP + FN)"),
        ("Precisao:",
         "Prec = VP / (VP + FP)"),
        ("Revocacao (Sensibilidade):",
         "Rec = VP / (VP + FN)"),
        ("F1-Score:",
         "F1 = 2 * (Prec * Rec) / (Prec + Rec)"),
    ]:
        pdf.set_body(bold=True, size=SIZE_BODY)
        pdf.set_x(MARGIN_LEFT + INDENT)
        pdf.multi_cell(CONTENT_W - INDENT, LINE_H, nome, align="L")
        pdf.set_body(italic=True)
        pdf.set_x(MARGIN_LEFT + INDENT * 2)
        pdf.multi_cell(CONTENT_W - INDENT * 2, LINE_H, formula, align="L")
        pdf.ln(1)
    pdf.para(
        "Em triagem clinica, a Revocacao da classe Doente e a metrica de maior relevancia "
        "medica: os Falsos Negativos — pacientes doentes classificados como saudaveis — "
        "representam o erro com maior potencial de dano clinico.")

    # =======================================================================
    # 2. METODOLOGIA
    # =======================================================================
    pdf.section("2", "Metodologia")

    pdf.section("2.1", "Conjunto de Dados")
    pdf.para(
        "O estudo utiliza o Cleveland Heart Disease Dataset, disponibilizado pelo UCI Machine "
        "Learning Repository sob o identificador id=45 (JANOSI et al., 1988). O dataset "
        "original contem 303 registros e 14 atributos — 13 preditores clinicos e 1 variavel "
        "alvo com 5 classes. Apos remocao de registros com valores ausentes, restaram 297 "
        "registros validos. A Tabela 2 descreve os 13 atributos preditores utilizados.")
    pdf.ln(2)
    pdf.table_caption("Tabela 2 - Atributos do Cleveland Heart Disease Dataset")
    headers_attr = ["Atributo", "Descricao", "Tipo"]
    rows_attr = [
        ("age",      "Idade do paciente (anos)",                          "Numerico"),
        ("sex",      "Sexo (1=masculino; 0=feminino)",                    "Binario"),
        ("cp",       "Tipo de dor toracica (0-3)",                        "Categorico"),
        ("trestbps", "Pressao arterial em repouso (mmHg)",                "Numerico"),
        ("chol",     "Colesterol serico (mg/dl)",                         "Numerico"),
        ("fbs",      "Glicemia em jejum > 120 mg/dl (1/0)",               "Binario"),
        ("restecg",  "Resultado do ECG em repouso (0-2)",                 "Categorico"),
        ("thalach",  "Frequencia cardiaca maxima atingida (bpm)",         "Numerico"),
        ("exang",    "Angina induzida por exercicio (1=sim; 0=nao)",      "Binario"),
        ("oldpeak",  "Depressao do segmento ST pelo exercicio",           "Numerico"),
        ("slope",    "Inclinacao do segmento ST de pico (0-2)",           "Categorico"),
        ("ca",       "Numero de vasos coloridos por fluoroscopia (0-3)",  "Ordinal"),
        ("thal",     "Resultado do teste de estresse com talio (0-3)",    "Categorico"),
    ]
    pdf.simple_table(headers_attr, rows_attr, [22, 112, 36],
                     header_align=["C", "C", "C"],
                     row_aligns=[["C", "L", "C"]] * len(rows_attr))
    pdf.table_source("Fonte: JANOSI et al. (1988).")

    pdf.section("2.2", "Binarizacao da Variavel Alvo")
    pdf.para(
        "O dataset original apresenta 5 niveis de diagnostico, introduzindo ambiguidade entre "
        "graus intermediarios. Para focar na questao diagnostica central — o paciente possui "
        "ou nao evidencia de doenca cardiaca — adotou-se a binarizacao da variavel alvo "
        "(MIENYE; SUN, 2022):")
    pdf.set_body(italic=True)
    pdf.set_x(MARGIN_LEFT + INDENT)
    pdf.multi_cell(CONTENT_W - INDENT, LINE_H,
        "y_bin = 0  se y_orig = 0  (Saudavel);   y_bin = 1  se y_orig > 0  (Doente)",
        align="L")
    pdf.ln(1)
    pdf.para(
        "Essa reducao de 5 para 2 classes simplifica a interpretacao clinica e elimina "
        "ambiguidades entre classes intermediarias.")

    pdf.section("2.3", "Pipeline de Pre-processamento")
    pdf.para(
        "O pipeline de pre-processamento compreende tres etapas sequenciais obrigatorias:")
    for etapa, desc in [
        ("Etapa 1 - Remocao de valores ausentes:",
         "registros com NaN em qualquer atributo foram descartados. Dos 303 registros "
         "originais, 6 foram removidos, resultando em 297 registros validos."),
        ("Etapa 2 - Padronizacao Z-score:",
         "os 13 atributos foram padronizados com StandardScaler. Media e desvio padrao "
         "calculados exclusivamente sobre X_train para evitar data leakage."),
        ("Etapa 3 - Particionamento estratificado:",
         "80% treinamento (237 registros) e 20% teste (60 registros), com stratify=y "
         "e random_state=42, preservando a proporcao de classes em ambas as particoes."),
    ]:
        pdf.set_body(bold=True, size=SIZE_BODY)
        pdf.set_x(MARGIN_LEFT + INDENT)
        pdf.multi_cell(CONTENT_W - INDENT, LINE_H, etapa, align="L")
        pdf.set_body(size=SIZE_BODY)
        pdf.set_x(MARGIN_LEFT + INDENT)
        pdf.multi_cell(CONTENT_W - INDENT, LINE_H, desc, align="J")
        pdf.ln(1)

    pdf.section("2.4", "Otimizacao do Hiperparametro K")
    pdf.para(
        "A selecao do melhor K foi realizada por GridSearchCV sobre K em {1,...,30}, usando "
        "StratifiedKFold(5) aplicado exclusivamente sobre X_train, com scoring=accuracy:")
    pdf.set_body(italic=True)
    pdf.set_x(MARGIN_LEFT + INDENT)
    pdf.multi_cell(CONTENT_W - INDENT, LINE_H,
        "K* = argmax_{k em {1,...,30}}  (1/5) * SUM_{i=1}^{5} Acc(k, dobra_i)   =>  K* = 29",
        align="L")
    pdf.ln(1)

    pdf.section("2.5", "Protocolo de Avaliacao Final")
    pdf.para(
        "Com K* = 29, o modelo final foi treinado com todo X_train e avaliado em tres "
        "instancias complementares:")
    for num, item in enumerate([
        "Conjunto de teste hold-out (60 registros, 20%): avalia desempenho em dados "
        "completamente nao vistos durante nenhuma etapa do treinamento ou selecao de K.",
        "Validacao cruzada 10-fold sobre os 297 registros completos: metrica de "
        "referencia mais robusta, obtida com StratifiedKFold(10) e cross_val_score.",
        "Predicao sobre o conjunto completo (297 registros): analise granular dos "
        "acertos e erros em blocos consecutivos de 50 registros.",
    ], start=1):
        pdf.set_body(size=SIZE_BODY)
        pdf.set_x(MARGIN_LEFT + INDENT)
        pdf.multi_cell(CONTENT_W - INDENT, LINE_H, f"{num}. {item}", align="J")
        pdf.ln(1)

    # =======================================================================
    # 3. RESULTADOS E DISCUSSÃO
    # =======================================================================
    pdf.section("3", "Resultados e Discussao")

    pdf.section("3.1", "Otimizacao do Hiperparametro K")
    pdf.para(
        "A Tabela 3 apresenta os 5 melhores valores de K identificados pelo GridSearchCV "
        "na validacao cruzada de 5 dobras sobre o conjunto de treinamento:")
    pdf.ln(2)
    pdf.table_caption("Tabela 3 - Top-5 valores de K (5-fold CV, conjunto de treino)")
    headers_k = ["K", "Acuracia CV Media"]
    rows_k = [
        ("29", "83,97%"),
        ("27", "83,55%"),
        ("17", "83,55%"),
        ("30", "83,55%"),
        ("26", "83,55%"),
    ]
    pdf.simple_table(headers_k, rows_k, [30, 140],
                     header_align=["C", "C"],
                     row_aligns=[["C", "C"]] * len(rows_k))
    pdf.table_source("Fonte: elaborada pelo autor (2026).")
    pdf.para(
        "O agrupamento dos melhores resultados na faixa K em [17,30] indica que o dataset "
        "apresenta padroes relativamente suaves que beneficiam vizinhancas maiores. Valores de "
        "K inferiores a 10 apresentaram maior variabilidade entre dobras, evidenciando "
        "sensibilidade a ruidos locais. A margem pequena entre K=29 (83,97%) e seus vizinhos "
        "proximos (83,55%) indica que a superficie de desempenho e relativamente plana na "
        "regiao [17,30], conferindo robustez a escolha.")

    pdf.section("3.2", "Acuracia por Blocos de Registros")
    pdf.para(
        "A Tabela 4 apresenta a distribuicao de acuracia por blocos consecutivos de 50 "
        "registros sobre os 297 pacientes:")
    pdf.ln(2)
    pdf.table_caption("Tabela 4 - Acuracia do KNN (K=29) por bloco de registros")
    headers_blk = ["Bloco", "Registros", "Acertos", "Acuracia"]
    rows_blk = [
        ("1", "1 - 50",    "45/50", "90,00%"),
        ("2", "51 - 100",  "42/50", "84,00%"),
        ("3", "101 - 150", "45/50", "90,00%"),
        ("4", "151 - 200", "40/50", "80,00%"),
        ("5", "201 - 250", "43/50", "86,00%"),
        ("6", "251 - 297", "37/47", "78,72%"),
        ("Total", "1 - 297", "252/297", "84,85%"),
    ]
    pdf.simple_table(headers_blk, rows_blk, [20, 40, 40, 70],
                     header_align=["C", "C", "C", "C"],
                     row_aligns=[["C", "C", "C", "C"]] * len(rows_blk))
    pdf.table_source("Fonte: elaborada pelo autor (2026).")
    pdf.para(
        "A variacao entre blocos (78,72% a 90,00%) reflete a heterogeneidade das amostras. "
        "O bloco 6 apresentou o menor desempenho (78,72%), possivelmente por conter maior "
        "proporcao de casos ambiguos. Os blocos 1 e 3 atingiram 90,00%, sugerindo regioes do "
        "espaco de caracteristicas com fronteiras de decisao mais nitidas.")

    pdf.section("3.3", "Metricas Consolidadas do Modelo")
    pdf.para(
        "A Tabela 5 apresenta o resumo completo do desempenho do classificador KNN com K=29:")
    pdf.ln(2)
    pdf.table_caption("Tabela 5 - Resumo de desempenho do classificador KNN (K=29)")
    headers_res = ["Metrica", "Valor"]
    rows_res = [
        ("Acuracia — conjunto de teste (hold-out 20%, 60 registros)", "86,67%"),
        ("Acuracia — validacao cruzada 10-fold (metrica principal, n=297)", "82,86% +/- 6,99%"),
        ("Acuracia — conjunto completo (297 registros)",                "84,85%"),
        ("F1-Score ponderado (conjunto de teste)",                      "0,87"),
        ("K (numero de vizinhos)",                                      "29"),
        ("Tamanho do conjunto de treinamento",                          "237 registros"),
        ("Tamanho do conjunto de teste",                                "60 registros"),
        ("Total de registros avaliados",                                "297 registros"),
    ]
    pdf.simple_table(headers_res, rows_res, [120, 50],
                     header_align=["C", "C"],
                     row_aligns=[["L", "C"]] * len(rows_res))
    pdf.table_source("Fonte: elaborada pelo autor (2026).")
    pdf.para(
        "A validacao cruzada 10-fold (82,86% +/- 6,99%) e a metrica de referencia recomendada "
        "para o TCC, pois estima a capacidade de generalizacao de forma imparcial: em cada uma "
        "das 10 iteracoes, o modelo e avaliado sobre uma dobra que nao participou do seu "
        "treinamento (GERON, 2019). O intervalo aproximado de desempenho situa-se entre "
        "75,87% e 89,85%. A avaliacao qualitativa do modelo e classificada como BOA.")

    pdf.section("3.4", "Matriz de Confusao")
    pdf.para(
        "A Tabela 6 apresenta a matriz de confusao sobre os 60 registros do conjunto de "
        "teste, detalhando cada tipo de predicao:")
    pdf.ln(2)
    pdf.table_caption("Tabela 6 - Matriz de confusao (conjunto de teste, n=60)")
    conf2_headers = ["", "Previsto: Saudavel (0)", "Previsto: Doente (1)"]
    conf2_rows = [
        ("Real: Saudavel (0)", "30  (VN)", "2  (FP)"),
        ("Real: Doente (1)",   "6  (FN)",  "22 (VP)"),
    ]
    pdf.simple_table(conf2_headers, conf2_rows, [50, 65, 55],
                     header_align=["C", "C", "C"],
                     row_aligns=[["L", "C", "C"]] * 2)
    pdf.table_source("Fonte: elaborada pelo autor (2026).")
    pdf.para(
        "Os 6 Falsos Negativos sao o erro mais critico: pacientes doentes que receberiam "
        "diagnostico negativo. Com 28 pacientes doentes no teste, isso equivale a uma taxa "
        "de falsos negativos de 21,4% — aceitavel para um modelo de triagem automatizada, "
        "mas insuficiente para uso clinico autonomo sem supervisao medica.")

    pdf.section("3.5", "Relatorio de Classificacao por Classe")
    pdf.para(
        "A Tabela 7 detalha as metricas por classe, revelando o comportamento assimetrico "
        "do modelo:")
    pdf.ln(2)
    pdf.table_caption("Tabela 7 - Relatorio de classificacao por classe (conjunto de teste, n=60)")
    headers_cls = ["Classe", "Precisao", "Revocacao", "F1-Score", "Suporte"]
    rows_cls = [
        ("Saudavel (0)", "0,83", "0,94", "0,88", "32"),
        ("Doente (1)",   "0,92", "0,79", "0,85", "28"),
        ("Acuracia",     "",     "",     "0,87",  "60"),
        ("Media macro",  "0,88", "0,86", "0,86",  "60"),
        ("Media ponder.", "0,87", "0,87", "0,87", "60"),
    ]
    pdf.simple_table(headers_cls, rows_cls, [34, 30, 30, 30, 30],
                     header_align=["C", "C", "C", "C", "C"],
                     row_aligns=[["L", "C", "C", "C", "C"]] * len(rows_cls))
    pdf.table_source("Fonte: elaborada pelo autor (2026).")
    pdf.para(
        "Precisao da classe Doente = 0,92: quando o modelo preve Doente, esta correto em "
        "92% dos casos. Revocacao da classe Doente = 0,79: detecta 79% dos pacientes "
        "efetivamente doentes. F1-Score equilibrado (0,85 e 0,88): sem desvio marcante para "
        "nenhuma das classes. F1-Score macro medio = 0,86: confirma desempenho consistente "
        "e equilibrado.")

    pdf.section("3.6", "Analise dos Erros de Classificacao")
    pdf.para(
        "Os 45 erros identificados nos 297 registros (15,15% do total) se dividem em dois "
        "tipos com causas e implicacoes distintas:")
    for tipo, descricao in [
        ("Falsos Negativos — doente classificado como saudavel:",
         "ocorrem quando um paciente doente possui combinacao de atributos que se assemelha, "
         "no espaco padronizado de 13 dimensoes, ao perfil de pacientes saudaveis na "
         "vizinhanca de K=29. Exemplos observados: registros 17, 23, 34, 45, 52, 53, 58, "
         "67, 70, 75, 81, 130, 144 e 145."),
        ("Falsos Positivos — saudavel classificado como doente:",
         "ocorrem quando um paciente saudavel apresenta perfil clinico proximo ao de "
         "pacientes doentes no espaco padronizado. Exemplos: registros 33, 52, 124, 141, "
         "167, 171, 179, 183 e 187."),
    ]:
        pdf.set_body(bold=True, size=SIZE_BODY)
        pdf.set_x(MARGIN_LEFT + INDENT)
        pdf.multi_cell(CONTENT_W - INDENT, LINE_H, tipo, align="L")
        pdf.set_body(size=SIZE_BODY)
        pdf.set_x(MARGIN_LEFT + INDENT)
        pdf.multi_cell(CONTENT_W - INDENT, LINE_H, descricao, align="J")
        pdf.ln(1)
    pdf.para(
        "Esses erros sao explicados pela natureza do KNN: o algoritmo opera usando apenas "
        "informacao local (K=29 vizinhos), sem construir representacao global da distribuicao "
        "das classes. Regioes do espaco de caracteristicas onde as duas classes se sobrepoem "
        "representam casos inerentemente dificeis para o classificador.")

    # =======================================================================
    # CONSIDERAÇÕES FINAIS
    # =======================================================================
    pdf.section("", "Consideracoes Finais")
    pdf.para(
        "Este relatório apresentou a fundamentacao matematica, a implementacao computacional "
        "e a analise experimental do algoritmo K-Nearest Neighbors para classificacao binaria "
        "de doenca cardiaca sobre o Cleveland Heart Disease Dataset.")
    pdf.para(
        "Os principais resultados e conclusoes sao:")
    for num, texto in [
        ("1.", "O KNN com K=29 obteve 86,67% de acuracia no conjunto de teste e "
               "82,86% +/- 6,99% na validacao cruzada de 10 dobras — metrica de referencia "
               "recomendada por ser a estimativa de generalizacao mais honesta disponivel."),
        ("2.", "A binarizacao da variavel alvo (5 classes -> 2 classes: Saudavel/Doente) "
               "foi decisao metodologica fundamental: eliminou ambiguidades entre graus "
               "intermediarios e alinhou o problema a pergunta diagnostica clinicamente "
               "relevante."),
        ("3.", "A padronizacao Z-score e condicao obrigatoria para o correto funcionamento "
               "do KNN sobre dados clinicos com atributos de escalas heterogeneas. Sua "
               "aplicacao estrita com parametros calculados apenas sobre X_train e essencial "
               "para evitar data leakage."),
        ("4.", "O valor otimo K=29 situa-se na regiao de vizinhanca larga, equilibrando "
               "adequadamente vies e variancia para as caracteristicas deste dataset. A busca "
               "automatizada por GridSearchCV e preferivel a escolha manual."),
        ("5.", "A matriz de confusao revela alta precisao para a classe Doente (0,92) e "
               "alta revocacao para a classe Saudavel (0,94). Os 6 Falsos Negativos (21,4%) "
               "representam a principal limitacao clinica, reforçando que o KNN deve ser "
               "utilizado como ferramenta de apoio a decisao medica, nao como sistema "
               "diagnostico autonomo."),
        ("6.", "Como trabalho futuro, recomenda-se: investigar metricas de distancia "
               "alternativas (Manhattan, Minkowski com p != 2); avaliar KNN ponderado com "
               "peso inversamente proporcional a distancia; aplicar SMOTE para melhorar "
               "a revocacao da classe Doente; e explorar selecao de atributos para "
               "identificar o subconjunto mais informativo dentre os 13 preditores."),
    ]:
        pdf.set_body(size=SIZE_BODY)
        pdf.set_x(MARGIN_LEFT + INDENT)
        pdf.multi_cell(CONTENT_W - INDENT, LINE_H, f"{num} {texto}", align="J")
        pdf.ln(1)

    # =======================================================================
    # REFERÊNCIAS
    # =======================================================================
    pdf.section("", "Referencias")

    refs = [
        "COVER, T. M.; HART, P. E. Nearest neighbor pattern classification. "
        "IEEE Transactions on Information Theory, v. 13, n. 1, p. 21-27, 1967. "
        "DOI: 10.1109/TIT.1967.1053964.",

        "FIX, E.; HODGES, J. L. Discriminatory Analysis: Nonparametric Discrimination, "
        "Consistency Properties. USAF School of Aviation Medicine, Randolph Field, Texas. "
        "Technical Report n. 4, 1951.",

        "GERON, Aurelien. Hands-On Machine Learning with Scikit-Learn, Keras, and "
        "TensorFlow: Concepts, Tools, and Techniques to Build Intelligent Systems. "
        "2. ed. Sebastopol, CA: O'Reilly Media, 2019.",

        "JANOSI, A.; STEINBRUNN, W.; PFISTERER, M.; DETRANO, R. Heart Disease Dataset. "
        "UCI Machine Learning Repository, 1988. Disponivel em: "
        "https://archive.ics.uci.edu/dataset/45/heart+disease. Acesso em: mar. 2026.",

        "MIENYE, I. D.; SUN, Y. A Survey of Ensemble Learning: Concepts, Algorithms, "
        "Applications, and Prospects. IEEE Access, v. 10, p. 99129-99149, 2022. "
        "DOI: 10.1109/ACCESS.2022.3207287.",

        "PEDREGOSA, F. et al. Scikit-learn: Machine Learning in Python. "
        "Journal of Machine Learning Research, v. 12, p. 2825-2830, 2011. "
        "Disponivel em: https://jmlr.org/papers/v12/pedregosa11a.html. Acesso em: mar. 2026.",

        "RUSSELL, S.; NORVIG, P. Artificial Intelligence: A Modern Approach. "
        "4. ed. Hoboken, NJ: Pearson, 2020.",
    ]
    for ref in refs:
        pdf.ref_entry(ref)

    return pdf


if __name__ == "__main__":
    pdf = build_relatorio()
    out_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "Relatorio_KNN_FATEC.pdf"
    )
    pdf.output(out_path)
    print(f"PDF gerado com sucesso: {out_path}")
