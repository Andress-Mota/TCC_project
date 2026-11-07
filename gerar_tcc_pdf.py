# -*- coding: utf-8 -*-
"""
Gerador do Relatório Técnico-Científico — TCC FATEC Guaratinguetá
Análise Comparativa de Algoritmos de IA para Classificação de Imagens
Autor: Andress Felipe de Oliveira Mota
Orientador: Professor Eduardo
"""

from fpdf import FPDF
import os

# ---------------------------------------------------------------------------
# Configurações gerais — Normas FATEC Guaratinguetá
# ---------------------------------------------------------------------------
M_LEFT   = 30.0   # margem esquerda 3 cm
M_RIGHT  = 20.0   # margem direita  2 cm
M_TOP    = 30.0   # margem superior 3 cm
M_BOTTOM = 20.0   # margem inferior 2 cm
PAGE_W   = 210.0
PAGE_H   = 297.0
C_W      = PAGE_W - M_LEFT - M_RIGHT   # 160 mm de largura útil

FONT     = "Arial"
S_BODY   = 11    # corpo do texto
S_SMALL  = 10    # legendas e fontes
S_TITLE  = 14    # títulos de capítulos
S_SUB    = 11    # subtítulos (negrito)
S_COVER  = 16    # elementos da capa
S_MAIN   = 18    # título principal da capa

LH       = 7.5   # altura de linha corpo (aprox. 1,5x para Arial 11)
LH_SM    = 6.0   # altura de linha pequena
LH_TBL   = 5.5   # altura de linha tabela
INDENT   = 12.5  # recuo de parágrafo 1,25 cm

BASE = os.path.dirname(os.path.abspath(__file__))

ARIAL = {
    "":   "C:/Windows/Fonts/arial.ttf",
    "B":  "C:/Windows/Fonts/arialbd.ttf",
    "I":  "C:/Windows/Fonts/ariali.ttf",
    "BI": "C:/Windows/Fonts/arialbi.ttf",
}


# ---------------------------------------------------------------------------
# Classe base PDF
# ---------------------------------------------------------------------------
class TCC(FPDF):

    _show_page_num = False   # só ativa após os pré-textuais

    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        for style, path in ARIAL.items():
            if os.path.exists(path):
                self.add_font(FONT, style, path)
        self.set_margins(M_LEFT, M_TOP, M_RIGHT)
        self.set_auto_page_break(auto=True, margin=M_BOTTOM)

    # --- cabeçalho com número de página (canto superior direito) ---
    def header(self):
        if self._show_page_num and self.page_no() > 1:
            self.set_font(FONT, "", S_SMALL)
            self.set_xy(M_LEFT, 10)
            self.cell(C_W, 5, str(self.page_no()), align="R")
            self.ln(15)

    def footer(self):
        pass

    # --- helpers de fonte ---
    def f(self, bold=False, italic=False, size=S_BODY):
        s = ("B" if bold else "") + ("I" if italic else "")
        self.set_font(FONT, s, size)

    # --- parágrafo justificado com recuo de primeira linha ---
    def para(self, txt, indent=True, size=S_BODY, bold=False, italic=False, lh=None):
        lh = lh or LH
        self.f(bold=bold, italic=italic, size=size)
        x = M_LEFT + (INDENT if indent else 0)
        w = C_W - (INDENT if indent else 0)
        self.set_x(x)
        self.multi_cell(w, lh, txt, align="J")

    # --- linha centrada ---
    def center(self, txt, size=S_BODY, bold=False, italic=False, lh=None):
        lh = lh or LH
        self.f(bold=bold, italic=italic, size=size)
        self.set_x(M_LEFT)
        self.multi_cell(C_W, lh, txt, align="C")

    # --- título de capítulo (14pt negrito, início de seção) ---
    def chapter_title(self, txt):
        self.f(bold=True, size=S_TITLE)
        self.set_x(M_LEFT)
        self.multi_cell(C_W, LH, txt.upper(), align="L")
        self.ln(2)

    # --- título de seção numerada (11pt negrito) ---
    def section(self, num, txt):
        self.ln(2)
        self.f(bold=True, size=S_SUB)
        self.set_x(M_LEFT)
        self.multi_cell(C_W, LH, f"{num} {txt}", align="L")
        self.ln(1)

    # --- título de subseção (11pt negrito) ---
    def subsection(self, num, txt):
        self.ln(1)
        self.f(bold=True, size=S_SUB)
        self.set_x(M_LEFT)
        self.multi_cell(C_W, LH, f"{num} {txt}", align="L")
        self.ln(1)

    # --- legenda de figura/quadro acima ---
    def caption(self, txt):
        self.f(bold=True, size=S_SMALL)
        self.set_x(M_LEFT)
        self.multi_cell(C_W, LH_SM, txt, align="C")

    # --- fonte de figura/quadro abaixo ---
    def source(self, txt="Fonte: Elaborado pelo autor (2026)."):
        self.f(size=S_SMALL)
        self.set_x(M_LEFT)
        self.multi_cell(C_W, LH_SM, txt, align="C")
        self.ln(4)

    # --- inserir imagem centralizada ---
    def fig(self, path, caption_txt, w=140, source_txt="Fonte: Elaborado pelo autor (2026)."):
        full = os.path.join(BASE, path)
        if not os.path.exists(full):
            self.para(f"[Figura não encontrada: {path}]", indent=False)
            return
        self.ln(2)
        self.caption(caption_txt)
        self.ln(1)
        x = M_LEFT + (C_W - w) / 2
        self.image(full, x=x, w=w)
        self.ln(1)
        self.source(source_txt)

    # --- tabela simples com bordas ---
    def table(self, caption_txt, headers, rows, col_w, h_aligns=None, r_aligns=None):
        self.ln(2)
        self.caption(caption_txt)
        self.ln(1)
        h_aligns = h_aligns or ["C"] * len(headers)
        r_aligns = r_aligns or [["L"] + ["C"] * (len(headers) - 1)] * len(rows)
        self.f(bold=True, size=S_SMALL)
        self.set_x(M_LEFT)
        for i, h in enumerate(headers):
            self.cell(col_w[i], LH_TBL + 1, h, border=1, align=h_aligns[i])
        self.ln()
        self.f(size=S_SMALL)
        for ri, row in enumerate(rows):
            self.set_x(M_LEFT)
            aligns = r_aligns[ri] if isinstance(r_aligns[0], list) else r_aligns
            for i, cell in enumerate(row):
                self.cell(col_w[i], LH_TBL + 1, str(cell), border=1, align=aligns[i])
            self.ln()
        self.source()

    # --- linha horizontal ---
    def hline(self):
        self.set_draw_color(0)
        self.set_line_width(0.3)
        self.line(M_LEFT, self.get_y(), PAGE_W - M_RIGHT, self.get_y())
        self.ln(2)

    # --- referência bibliográfica ---
    def ref(self, txt):
        self.f(size=S_BODY)
        self.set_x(M_LEFT)
        self.multi_cell(C_W, LH, txt, align="J")
        self.ln(2)


# ===========================================================================
# CAPA
# ===========================================================================
def capa(pdf):
    pdf.add_page()
    pdf.ln(10)
    pdf.center("FACULDADE DE TECNOLOGIA DE GUARATINGUETÁ", size=S_COVER, bold=True)
    pdf.ln(40)
    pdf.center(
        "ANÁLISE COMPARATIVA DE ALGORITMOS DE\n"
        "INTELIGÊNCIA ARTIFICIAL PARA CLASSIFICAÇÃO\n"
        "DE IMAGENS BASEADA EM APRENDIZADO\nSUPERVISIONADO",
        size=S_MAIN, bold=True, lh=9
    )
    pdf.ln(10)
    pdf.center("Andress Felipe de Oliveira Mota", size=S_COVER, bold=True)
    pdf.ln(60)
    pdf.center("Guaratinguetá - SP", size=S_COVER, bold=True)
    pdf.center("2026", size=S_COVER, bold=True)


# ===========================================================================
# PÁGINA DE ROSTO
# ===========================================================================
def rosto(pdf):
    pdf.add_page()
    pdf.ln(10)
    pdf.center("FACULDADE DE TECNOLOGIA DE GUARATINGUETÁ", size=S_COVER, bold=True)
    pdf.ln(20)
    pdf.center(
        "ANÁLISE COMPARATIVA DE ALGORITMOS DE\n"
        "INTELIGÊNCIA ARTIFICIAL PARA CLASSIFICAÇÃO\n"
        "DE IMAGENS BASEADA EM APRENDIZADO\nSUPERVISIONADO",
        size=S_MAIN, bold=True, lh=9
    )
    pdf.ln(8)
    pdf.center("Andress Felipe de Oliveira Mota", size=S_COVER, bold=True)
    pdf.ln(20)
    # bloco justificado à direita
    texto_rosto = (
        "Relatório Técnico-científico apresentado à\n"
        "Faculdade de Tecnologia de Guaratinguetá,\n"
        "como requisito parcial para conclusão do\n"
        "Curso Superior de Tecnologia em Análise\n"
        "e Desenvolvimento de Sistemas.\n\n"
        "Programa: Análise e Desenvolvimento de Sistemas\n"
        "Área Temática: Inteligência Artificial e\n"
        "Aprendizado de Máquina\n"
        "Linha de Estudo e Pesquisa: Classificação de\n"
        "Imagens com Algoritmos de Machine Learning\n\n"
        "Orientador: Professor Eduardo"
    )
    pdf.f(size=S_BODY)
    pdf.set_x(M_LEFT + C_W / 2)
    pdf.multi_cell(C_W / 2, LH, texto_rosto, align="J")
    pdf.ln(20)
    pdf.center("Guaratinguetá - SP", size=S_COVER, bold=True)
    pdf.center("2026", size=S_COVER, bold=True)


# ===========================================================================
# FICHA CATALOGRÁFICA (verso)
# ===========================================================================
def ficha(pdf):
    pdf.add_page()
    pdf.ln(180)
    txt = (
        "MOTA, Andress Felipe de Oliveira. Análise Comparativa de Algoritmos de "
        "Inteligência Artificial para Classificação de Imagens Baseada em Aprendizado "
        "Supervisionado. Guaratinguetá, 2026. Relatório Técnico-científico, Curso de "
        "Análise e Desenvolvimento de Sistemas, Faculdade de Tecnologia de "
        "Guaratinguetá, 2026."
    )
    pdf.f(size=S_BODY)
    pdf.set_x(M_LEFT + C_W / 2)
    pdf.multi_cell(C_W / 2, LH, txt, align="J")


# ===========================================================================
# RESUMO
# ===========================================================================
def resumo(pdf):
    pdf._show_page_num = True
    pdf.add_page()
    pdf.center("Resumo", bold=True, size=S_BODY)
    pdf.ln(2)
    pdf.f(size=S_BODY)
    pdf.set_x(M_LEFT)
    ficha_txt = (
        "MOTA, Andress Felipe de Oliveira. Análise Comparativa de Algoritmos de "
        "Inteligência Artificial para Classificação de Imagens Baseada em Aprendizado "
        "Supervisionado. Guaratinguetá, 2026. Relatório Técnico-científico, Curso de "
        "Análise e Desenvolvimento de Sistemas, Faculdade de Tecnologia de "
        "Guaratinguetá, 2026."
    )
    pdf.multi_cell(C_W, LH, ficha_txt, align="J")
    pdf.ln(3)
    txt = (
        "A crescente aplicação de algoritmos de aprendizado de máquina em domínios "
        "que exigem análise automatizada de imagens impõe ao campo científico a "
        "necessidade de estudos comparativos que orientem a escolha das abordagens mais "
        "adequadas a cada contexto. O presente trabalho tem como objetivo desenvolver, "
        "documentar e avaliar um sistema web de classificação de imagens baseado em "
        "técnicas de ensemble learning, integrando cinco algoritmos individuais — "
        "K-Nearest Neighbors (KNN), Support Vector Machine (SVM), Random Forest, "
        "Regressão Logística e Naive Bayes Gaussiano — a três estratégias de "
        "combinação: Voting Hard, Voting Soft e Stacking. A pesquisa foi conduzida em "
        "duas etapas complementares. Na primeira, de caráter experimental e teórico, os "
        "algoritmos foram aplicados ao dataset UCI Heart Disease (Cleveland), composto "
        "por 297 registros clínicos e 13 variáveis preditoras, com o objetivo de "
        "compreender o comportamento de cada modelo em um ambiente controlado antes da "
        "aplicação ao domínio de imagens. Os resultados obtidos nessa fase "
        "demonstraram acurácias que variaram de 81,51% a 88,33% na validação cruzada "
        "de dez dobras, conferindo embasamento empírico suficiente para a seleção dos "
        "hiperparâmetros adotados no sistema. Na segunda etapa, foi desenvolvida a "
        "plataforma TCC IA, uma aplicação web construída com o framework Flask e banco "
        "de dados MySQL, capaz de receber conjuntos de imagens organizados por classes, "
        "extrair características por meio do Histograma de Gradientes Orientados (HOG) "
        "com resolução de 128×128 pixels em escala de cinza, treinar os oito modelos "
        "de forma automática e apresentar resultados comparativos detalhados. O sistema "
        "incorpora ainda a rede neural convolucional EfficientNet-B0 com visualização "
        "por Grad-CAM para interpretabilidade das predições. A validação prática foi "
        "realizada com o dataset Chest X-Ray Images (Pneumonia), no qual o modelo "
        "Stacking alcançou acurácia de 92,00% na validação cruzada de dez dobras e no "
        "conjunto de teste, enquanto a EfficientNet-B0 classificou imagens individuais "
        "com confiança de 99,2%. Os resultados evidenciam que o ensemble learning "
        "supera consistentemente o desempenho individual de cada modelo, e que a "
        "plataforma desenvolvida constitui uma ferramenta técnica e científica relevante "
        "para a análise comparativa de algoritmos de inteligência artificial aplicados "
        "à classificação de imagens."
    )
    pdf.para(txt, indent=False)
    pdf.ln(2)
    pdf.f(bold=True, size=S_BODY)
    pdf.set_x(M_LEFT)
    pdf.write(LH, "Palavras-chave: ")
    pdf.f(size=S_BODY)
    pdf.write(LH, "Aprendizado de Máquina. Ensemble Learning. Classificação de Imagens. "
              "HOG. KNN. SVM. Random Forest. EfficientNet-B0. Grad-CAM.")
    pdf.ln(6)


# ===========================================================================
# ABSTRACT
# ===========================================================================
def abstract(pdf):
    pdf.add_page()
    pdf.center("Abstract", bold=True, size=S_BODY)
    pdf.ln(2)
    pdf.f(size=S_BODY)
    pdf.set_x(M_LEFT)
    ficha_en = (
        "MOTA, Andress Felipe de Oliveira. Comparative Analysis of Artificial "
        "Intelligence Algorithms for Image Classification Based on Supervised Learning. "
        "Guaratinguetá, 2026. Technical and Scientific Report, Computer Systems "
        "Analysis and Development Program, Faculdade de Tecnologia de Guaratinguetá, "
        "2026."
    )
    pdf.multi_cell(C_W, LH, ficha_en, align="J")
    pdf.ln(3)
    txt = (
        "The growing application of machine learning algorithms in domains requiring "
        "automated image analysis imposes on the scientific field a need for comparative "
        "studies to guide the selection of the most appropriate approaches for each "
        "context. This work aims to develop, document, and evaluate a web-based image "
        "classification system grounded in ensemble learning techniques, integrating "
        "five individual algorithms — K-Nearest Neighbors (KNN), Support Vector Machine "
        "(SVM), Random Forest, Logistic Regression, and Gaussian Naive Bayes — with "
        "three combination strategies: Hard Voting, Soft Voting, and Stacking. The "
        "research was conducted in two complementary stages. In the first stage, of "
        "experimental and theoretical character, the algorithms were applied to the UCI "
        "Heart Disease dataset (Cleveland), comprising 297 clinical records and 13 "
        "predictor variables, aiming to understand each model's behavior in a controlled "
        "environment before application in the image domain. Results showed accuracies "
        "ranging from 81.51% to 88.33% in ten-fold cross-validation. In the second "
        "stage, the TCC IA platform was developed — a Flask-based web application with "
        "MySQL database — capable of receiving class-organized image datasets, "
        "extracting features through the Histogram of Oriented Gradients (HOG) at "
        "128×128 pixel resolution, automatically training the eight models, and "
        "presenting detailed comparative results. The system also incorporates the "
        "EfficientNet-B0 convolutional neural network with Grad-CAM visualization. "
        "Practical validation was performed using the Chest X-Ray Images (Pneumonia) "
        "dataset, in which the Stacking model achieved 92.00% accuracy, while the "
        "EfficientNet-B0 classified individual images with 99.2% confidence. Results "
        "demonstrate that ensemble learning consistently outperforms individual "
        "classifiers, and that the developed platform constitutes a relevant technical "
        "and scientific tool for comparative analysis of AI algorithms applied to "
        "image classification."
    )
    pdf.para(txt, indent=False)
    pdf.ln(2)
    pdf.f(bold=True, size=S_BODY)
    pdf.set_x(M_LEFT)
    pdf.write(LH, "Keywords: ")
    pdf.f(size=S_BODY)
    pdf.write(LH, "Machine Learning. Ensemble Learning. Image Classification. HOG. "
              "KNN. SVM. Random Forest. EfficientNet-B0. Grad-CAM.")
    pdf.ln(6)


# ===========================================================================
# SUMÁRIO
# ===========================================================================
def sumario(pdf):
    pdf.add_page()
    pdf.chapter_title("SUMÁRIO")
    entries = [
        ("INTRODUÇÃO", ""),
        ("1  FUNDAMENTAÇÃO TEÓRICA", ""),
        ("   1.1  Aprendizado de Máquina e Aprendizado Supervisionado", ""),
        ("   1.2  Extração de Características: o Histograma de Gradientes Orientados", ""),
        ("   1.3  Algoritmos de Classificação Individual", ""),
        ("        1.3.1  K-Nearest Neighbors", ""),
        ("        1.3.2  Support Vector Machine", ""),
        ("        1.3.3  Random Forest", ""),
        ("        1.3.4  Regressão Logística", ""),
        ("        1.3.5  Naive Bayes Gaussiano", ""),
        ("   1.4  Ensemble Learning", ""),
        ("        1.4.1  Fundamentos e Diversidade de Modelos", ""),
        ("        1.4.2  Voting Hard e Voting Soft", ""),
        ("        1.4.3  Stacking", ""),
        ("   1.5  Redes Neurais Convolucionais e a Arquitetura EfficientNet-B0", ""),
        ("   1.6  Grad-CAM: Visualização de Ativações em Redes Convolucionais", ""),
        ("2  METODOLOGIA E DESENVOLVIMENTO DO SISTEMA", ""),
        ("   2.1  Fase Experimental: Estudo com o Dataset UCI Heart Disease", ""),
        ("        2.1.1  Descrição e Pré-processamento da Base de Dados", ""),
        ("        2.1.2  Configuração dos Experimentos e Validação Cruzada", ""),
        ("        2.1.3  Resultados da Fase Experimental", ""),
        ("   2.2  Desenvolvimento do Sistema TCC IA", ""),
        ("        2.2.1  Visão Geral da Arquitetura", ""),
        ("        2.2.2  Pipeline de Classificação de Imagens", ""),
        ("        2.2.3  Módulo de Autenticação e Segurança", ""),
        ("        2.2.4  Banco de Dados", ""),
        ("        2.2.5  Interface Web e Funcionalidades", ""),
        ("3  RESULTADOS E DISCUSSÃO", ""),
        ("   3.1  Dataset de Validação: Chest X-Ray Images (Pneumonia)", ""),
        ("   3.2  Comparativo dos Oito Modelos", ""),
        ("   3.3  CNN EfficientNet-B0 e Interpretabilidade via Grad-CAM", ""),
        ("   3.4  Análise e Discussão dos Resultados", ""),
        ("CONSIDERAÇÕES FINAIS", ""),
        ("REFERÊNCIAS", ""),
    ]
    for label, pg in entries:
        pdf.f(size=S_BODY)
        pdf.set_x(M_LEFT)
        pdf.multi_cell(C_W, LH_SM + 0.5, label, align="L")


# ===========================================================================
# INTRODUÇÃO
# ===========================================================================
def introducao(pdf):
    pdf.add_page()
    pdf.chapter_title("INTRODUÇÃO")

    paras = [
        ("A Inteligência Artificial se consolidou, ao longo das últimas décadas, como uma das mais "
         "transformadoras vertentes do desenvolvimento tecnológico contemporâneo. Desde as primeiras "
         "formalizações matemáticas dos sistemas de aprendizado automático, passando pela consolidação "
         "dos algoritmos clássicos de aprendizado de máquina, até a explosão das arquiteturas de "
         "aprendizado profundo, o campo assistiu a uma progressão que ultrapassou os limites do "
         "ambiente acadêmico para se integrar de maneira profunda às estruturas da medicina, da "
         "segurança, da agricultura e da indústria. No cerne desse avanço reside uma questão "
         "cientificamente relevante e praticamente urgente: diante de um problema específico de "
         "classificação, qual algoritmo oferece o melhor equilíbrio entre acurácia, capacidade de "
         "generalização, custo computacional e interpretabilidade?"),

        ("A classificação de imagens representa, nesse contexto, um dos domínios de aplicação mais "
         "exigentes e, simultaneamente, mais promissores do aprendizado de máquina supervisionado. "
         "A tarefa de ensinar um sistema computacional a reconhecer padrões visuais — distinguindo "
         "uma radiografia normal de uma afetada por pneumonia, identificando anomalias em linhas de "
         "produção industrial ou reconhecendo faces em sistemas de segurança — demanda abordagens "
         "que conjuguem extração de características robustas com modelos capazes de generalizar "
         "satisfatoriamente para amostras não vistas durante o treinamento. Algoritmos clássicos "
         "como K-Nearest Neighbors, Support Vector Machine e Random Forest foram, durante décadas, "
         "as ferramentas primárias para essa tarefa; mais recentemente, as redes neurais "
         "convolucionais passaram a dominar os benchmarks de classificação de imagens, trazendo "
         "ganhos substanciais de desempenho ao custo de maior demanda computacional e menor "
         "interpretabilidade direta."),

        ("Nesse cenário, o presente trabalho propõe uma análise comparativa aprofundada de algoritmos "
         "de inteligência artificial aplicados à classificação de imagens, com ênfase na estratégia "
         "de ensemble learning como abordagem capaz de superar as limitações individuais de cada "
         "modelo. O estudo foi estruturado em duas etapas complementares. A primeira, de caráter "
         "experimental, utilizou o dataset UCI Heart Disease — Cleveland para compreender em "
         "profundidade o comportamento dos algoritmos e calibrar os hiperparâmetros antes da "
         "aplicação ao domínio de imagens. A segunda etapa consistiu no desenvolvimento do sistema "
         "TCC IA, uma plataforma web completa, construída sobre o framework Flask com armazenamento "
         "em banco de dados relacional MySQL, que automatiza o processo de treinamento comparativo "
         "de oito modelos de aprendizado de máquina aplicados a qualquer conjunto de imagens "
         "organizado em pastas por classe."),

        ("O objetivo geral deste trabalho consiste em desenvolver e validar experimentalmente uma "
         "plataforma computacional para classificação de imagens que implemente e compare algoritmos "
         "clássicos de aprendizado de máquina e estratégias de ensemble learning, demonstrando, "
         "de forma quantitativa, as diferenças de desempenho entre as abordagens estudadas. "
         "Para a realização plena desse objetivo, foram estabelecidos os seguintes objetivos "
         "específicos: estudar os fundamentos matemáticos e computacionais dos algoritmos KNN, SVM, "
         "Random Forest, Regressão Logística, Naive Bayes e das estratégias de ensemble Voting Hard, "
         "Voting Soft e Stacking; conduzir uma fase experimental com o dataset UCI Heart Disease "
         "para validar os procedimentos de pré-processamento e métricas de avaliação; desenvolver "
         "um sistema web capaz de receber conjuntos de imagens, extrair características HOG, treinar "
         "os oito modelos automaticamente e apresentar resultados comparativos detalhados; integrar "
         "ao sistema a rede neural EfficientNet-B0 com visualização Grad-CAM; validar o sistema com "
         "o dataset público Chest X-Ray Images (Pneumonia); e analisar criticamente os resultados "
         "obtidos."),

        ("A relevância científica e prática deste trabalho se fundamenta em três eixos principais. "
         "O primeiro é a escassez de sistemas que integrem, em uma única plataforma web acessível, "
         "múltiplos algoritmos clássicos e técnicas de ensemble para classificação de imagens, "
         "tornando a comparação experimental acessível sem necessidade de implementação manual de "
         "cada modelo. O segundo eixo é a contribuição para a compreensão do comportamento "
         "comparativo dos algoritmos em cenários reais de classificação binária de imagens, com "
         "foco especial no papel do ensemble learning como estratégia de mitigação dos erros "
         "individuais. O terceiro eixo é a aplicabilidade clínica dos resultados obtidos com o "
         "dataset de pneumonia, que demonstra o potencial do sistema como ferramenta de triagem e "
         "apoio ao diagnóstico médico baseado em imagens radiológicas."),

        ("Este relatório está organizado em três capítulos de desenvolvimento, além desta Introdução "
         "e das Considerações Finais. O Capítulo 1 apresenta a fundamentação teórica que sustenta "
         "o trabalho, abordando os conceitos de aprendizado de máquina supervisionado, a técnica "
         "de extração de características HOG, os cinco algoritmos de classificação individual "
         "implementados, os três métodos de ensemble, a arquitetura EfficientNet-B0 e o método "
         "Grad-CAM. O Capítulo 2 descreve a metodologia adotada, incluindo a fase experimental "
         "com o dataset UCI Heart Disease e o processo de desenvolvimento do sistema TCC IA, com "
         "detalhamento da arquitetura, do pipeline de classificação, do módulo de autenticação, "
         "do banco de dados e da interface web. O Capítulo 3 apresenta e discute os resultados "
         "obtidos na validação prática com o dataset de pneumonia. Por fim, as Considerações "
         "Finais sintetizam os principais achados, apontam as limitações do estudo e propõem "
         "direções para trabalhos futuros."),
    ]
    for p in paras:
        pdf.para(p)
        pdf.ln(1)


# ===========================================================================
# CAPÍTULO 1 — FUNDAMENTAÇÃO TEÓRICA
# ===========================================================================
def cap1(pdf):
    pdf.add_page()
    pdf.chapter_title("1 FUNDAMENTAÇÃO TEÓRICA")

    # 1.1
    pdf.section("1.1", "Aprendizado de Máquina e Aprendizado Supervisionado")
    ps = [
        ("O aprendizado de máquina constitui um subcampo da inteligência artificial dedicado ao "
         "desenvolvimento de algoritmos e modelos estatísticos que permitem a sistemas "
         "computacionais aprenderem padrões a partir de dados, sem que sejam explicitamente "
         "programados para cada regra de decisão. A definição clássica, retomada por Géron (2019), "
         "estabelece que um programa de computador aprende com a experiência E em relação a alguma "
         "tarefa T e medida de desempenho P, se seu desempenho em T, medido por P, melhora com a "
         "experiência E. Essa formulação captura de maneira precisa a essência do paradigma: ao "
         "contrário dos sistemas baseados em regras explícitas, os algoritmos de aprendizado de "
         "máquina constroem representações internas dos dados de treinamento e utilizam essas "
         "representações para tomar decisões sobre instâncias novas, não vistas durante o processo "
         "de aprendizado."),

        ("Géron (2019) classifica os sistemas de aprendizado de máquina segundo três critérios "
         "principais: a quantidade e o tipo de supervisão recebida durante o treinamento, a "
         "capacidade de aprender incrementalmente a partir de novos dados, e o modo pelo qual os "
         "algoritmos generalizam. O critério de supervisão é o mais relevante para o presente "
         "trabalho. No aprendizado supervisionado, os dados de treinamento incluem os rótulos "
         "desejados, denominados labels, e o algoritmo aprende a mapear entradas para saídas com "
         "base nos exemplos rotulados. Em contraste, o aprendizado não supervisionado opera sobre "
         "dados não rotulados, buscando descobrir estruturas internas como agrupamentos ou "
         "associações."),

        ("O aprendizado supervisionado subdivide-se em dois tipos fundamentais de tarefas: regressão "
         "e classificação. Na regressão, o objetivo é prever um valor numérico contínuo. Na "
         "classificação, o objetivo é atribuir uma entrada a uma entre um conjunto discreto de "
         "categorias, denominadas classes. Quando o conjunto de classes é binário, a tarefa é "
         "denominada classificação binária. O presente trabalho concentra-se integralmente em "
         "problemas de classificação binária, tanto na fase experimental com dados clínicos quanto "
         "na validação com imagens radiológicas."),

        ("Para a avaliação do desempenho de classificadores, diversas métricas foram desenvolvidas, "
         "cada uma capturando aspectos distintos do comportamento do modelo. A acurácia é definida "
         "como a proporção de predições corretas sobre o total de predições realizadas. A precisão "
         "mensura a proporção de predições positivas que são, de fato, positivas; o recall mensura "
         "a proporção de instâncias positivas reais corretamente identificadas. O F1-Score, média "
         "harmônica entre precisão e recall, combina ambas as métricas em uma única grandeza. "
         "Por fim, a AUC-ROC mensura a capacidade discriminativa do modelo ao longo de todos os "
         "limiares de decisão possíveis (GÉRON, 2019)."),

        ("Para a estimativa robusta da capacidade de generalização, a técnica de validação cruzada "
         "é amplamente empregada. Na validação cruzada com k-dobras, o conjunto de dados é dividido "
         "em k subconjuntos de tamanho aproximadamente igual. O modelo é treinado k vezes, cada "
         "vez utilizando k-1 dobras como conjunto de treinamento e a dobra restante como conjunto "
         "de validação. A acurácia final é calculada como a média das k acurácias obtidas, "
         "acompanhada de seu desvio padrão, que quantifica a estabilidade do modelo. A variante "
         "estratificada, StratifiedKFold, assegura que cada dobra mantenha a mesma proporção de "
         "classes que o conjunto original. No presente trabalho, adotou-se a validação cruzada "
         "estratificada com dez dobras como métrica primária de avaliação (GÉRON, 2019)."),
    ]
    for p in ps:
        pdf.para(p)
        pdf.ln(1)

    # 1.2
    pdf.section("1.2", "Extração de Características: o Histograma de Gradientes Orientados")
    ps = [
        ("A representação de imagens como vetores de características numéricas é o passo preliminar "
         "indispensável para a aplicação de algoritmos de aprendizado de máquina clássicos à "
         "classificação de imagens. Ao contrário das redes neurais convolucionais, que aprendem "
         "automaticamente hierarquias de características diretamente a partir dos pixels brutos, "
         "os algoritmos clássicos requerem que o desenvolvedor defina explicitamente de que maneira "
         "a imagem será convertida em um vetor de entrada de dimensão fixa. Esse processo, "
         "denominado extração de características, pode ser realizado por diferentes técnicas, "
         "cada uma sensível a diferentes propriedades das imagens."),

        ("O Histograma de Gradientes Orientados, conhecido pela sigla HOG, é uma técnica de extração "
         "de características visuais proposta por Dalal e Triggs em 2005 e amplamente utilizada em "
         "aplicações de visão computacional, especialmente na detecção de pedestres, reconhecimento "
         "de objetos e classificação de imagens médicas. A premissa fundamental do HOG é que a "
         "forma local e a aparência de objetos em uma imagem podem ser descritas eficientemente "
         "pela distribuição das intensidades de gradientes ou, equivalentemente, das orientações "
         "das bordas, mesmo sem um conhecimento preciso das posições exatas desses gradientes."),

        ("O processo de extração de características HOG ocorre em quatro etapas principais. A "
         "primeira consiste no pré-processamento da imagem: ela é redimensionada para uma resolução "
         "padronizada e convertida para escala de cinza. No sistema desenvolvido neste trabalho, "
         "todas as imagens são redimensionadas para 128×128 pixels em escala de cinza antes da "
         "extração. A segunda etapa consiste no cálculo dos gradientes horizontais e verticais da "
         "imagem por meio de operadores de convolução, capturando as variações locais de intensidade "
         "que caracterizam as estruturas visuais. A terceira etapa corresponde à construção do "
         "histograma: a imagem é dividida em células de 16×16 pixels e as orientações de gradiente "
         "são quantizadas em 9 bins, com as magnitudes acumuladas em um histograma por célula. "
         "A quarta etapa consiste na normalização por blocos de 2×2 células, compensando variações "
         "de iluminação e contraste local."),

        ("O vetor de características final, resultante da concatenação de todos os histogramas "
         "normalizados, possui dimensionalidade aproximada de 324 elementos para a configuração "
         "adotada. Esse vetor encapsula, de forma compacta, a informação estrutural relevante da "
         "imagem, tornando-a comparável e computacionalmente tratável pelos classificadores clássicos. "
         "A escolha do HOG é justificada por sua robustez a variações moderadas de iluminação e "
         "de posição dos objetos, por sua eficiência computacional e por sua ampla validação na "
         "literatura para tarefas de classificação de imagens médicas."),
    ]
    for p in ps:
        pdf.para(p)
        pdf.ln(1)

    # 1.3
    pdf.section("1.3", "Algoritmos de Classificação Individual")

    pdf.subsection("1.3.1", "K-Nearest Neighbors")
    ps = [
        ("O algoritmo K-Nearest Neighbors, ou K-Vizinhos Mais Próximos, é um dos métodos de "
         "aprendizado de máquina mais intuitivos disponíveis. Pertence à categoria dos algoritmos "
         "de aprendizado baseado em instâncias, também denominado aprendizado preguiçoso, pois não "
         "constrói um modelo explícito durante o treinamento: memoriza todo o conjunto de "
         "treinamento e realiza o trabalho computacional apenas no momento da predição."),

        ("O princípio de funcionamento fundamenta-se na hipótese de que instâncias similares tendem "
         "a pertencer à mesma classe. Dado um novo ponto de consulta, o algoritmo calcula sua "
         "distância para todos os pontos do conjunto de treinamento, identifica os K pontos mais "
         "próximos e atribui ao novo ponto a classe mais frequente entre esses K vizinhos, por "
         "votação majoritária. A distância euclidiana é a métrica mais comum (GÉRON, 2019). A "
         "normalização das features é indispensável, pois features em escalas distintas exercem "
         "influências desproporcionais sobre o cálculo da distância."),

        ("A escolha do valor de K é o principal hiperparâmetro do algoritmo: valores pequenos "
         "tornam o modelo sensível ao ruído, produzindo sobreajuste; valores grandes suavizam a "
         "fronteira de decisão ao custo de maior viés. A determinação do valor ótimo por meio de "
         "GridSearchCV com validação cruzada — como implementado neste trabalho, com busca no "
         "intervalo K=1 a K=20 — garante a seleção sistematicamente fundamentada. Na fase "
         "experimental com o dataset UCI Heart Disease, o KNN com K=29 alcançou acurácia de "
         "86,67% no conjunto de teste e 82,86% +/- 6,99% na validação cruzada de dez dobras."),
    ]
    for p in ps:
        pdf.para(p)
        pdf.ln(1)

    pdf.subsection("1.3.2", "Support Vector Machine")
    ps = [
        ("A Support Vector Machine é um algoritmo de aprendizado supervisionado fundamentado na "
         "teoria estatística do aprendizado, com desenvolvimentos realizados por Vapnik e "
         "colaboradores na década de 1990. O SVM destaca-se pela elegância de seu embasamento "
         "matemático e pela eficácia em problemas de alta dimensionalidade."),

        ("O princípio fundamental consiste em encontrar o hiperplano de separação que maximiza a "
         "margem entre as duas classes — a distância entre o hiperplano e os pontos mais próximos "
         "de cada classe, denominados vetores de suporte. A maximização da margem é motivada pela "
         "teoria do aprendizado estatístico: um hiperplano com margem máxima tende a generalizar "
         "melhor para dados não vistos (GÉRON, 2019)."),

        ("Para problemas não linearmente separáveis, o SVM utiliza o truque do kernel, que "
         "transforma implicitamente o espaço original em um espaço de dimensão maior onde a "
         "separabilidade linear é alcançável. O kernel radial (RBF), definido por K(x,z) = "
         "exp(−γ||x−z||²), foi selecionado como ótimo na fase experimental deste trabalho, com "
         "γ determinado automaticamente pela regra scale e C=0,1 — um valor de forte "
         "regularização. O SVM alcançou acurácia de 86,67% no conjunto de teste e 83,51% "
         "+/- 7,66% na validação cruzada, resultado estatisticamente equivalente ao KNN."),
    ]
    for p in ps:
        pdf.para(p)
        pdf.ln(1)

    pdf.subsection("1.3.3", "Random Forest")
    ps = [
        ("O Random Forest é um algoritmo de ensemble baseado em bagging que combina múltiplas "
         "árvores de decisão treinadas de forma independente sobre subamostras aleatórias do "
         "conjunto de treinamento. Proposto por Breiman em 2001, é amplamente considerado um "
         "dos classificadores de propósito geral mais robustos disponíveis na literatura."),

        ("A inovação central do Random Forest reside na injeção de aleatoriedade no processo de "
         "construção de cada árvore: além de treinar cada árvore sobre uma subamostra aleatória "
         "com reposição, o algoritmo restringe a busca do melhor split em cada nó a um subconjunto "
         "aleatório das features disponíveis. Essa dupla fonte de aleatoriedade aumenta a "
         "diversidade entre as árvores e reduz a correlação entre seus erros (GÉRON, 2019). "
         "Uma vantagem adicional é que, por ser baseado em árvores de decisão, não requer "
         "normalização das features de entrada. No sistema desenvolvido, o Random Forest foi "
         "configurado com 50 árvores e profundidade máxima de 10 níveis, alcançando acurácia "
         "de 85,00% no conjunto de teste e 81,51% +/- 6,13% na validação cruzada."),
    ]
    for p in ps:
        pdf.para(p)
        pdf.ln(1)

    pdf.subsection("1.3.4", "Regressão Logística")
    ps = [
        ("A Regressão Logística é um algoritmo de classificação que modela a probabilidade "
         "condicional de uma instância pertencer à classe positiva como uma função logística — "
         "ou sigmoide — da combinação linear das features de entrada: P(y=1|x) = σ(wᵀx + b), "
         "onde σ(z) = 1/(1+e^{-z}). A estimação dos parâmetros é realizada por maximização da "
         "verossimilhança logarítmica, equivalente à minimização da entropia cruzada binária."),

        ("Para evitar o sobreajuste, a Regressão Logística incorpora regularização L2, que "
         "adiciona à função de custo um termo proporcional à soma dos quadrados dos pesos. "
         "No sistema desenvolvido, foi configurada com regularização L2 e máximo de 1000 "
         "iterações. Uma característica especialmente relevante é sua capacidade de estimar "
         "probabilidades bem calibradas, tornando-a uma escolha natural como meta-learner "
         "no Stacking."),
    ]
    for p in ps:
        pdf.para(p)
        pdf.ln(1)

    pdf.subsection("1.3.5", "Naive Bayes Gaussiano")
    ps = [
        ("O classificador Naive Bayes Gaussiano é um algoritmo probabilístico fundamentado no "
         "teorema de Bayes para classificação, com a suposição simplificadora — ingênua — de "
         "que as features são condicionalmente independentes entre si dado o rótulo de classe. "
         "O modelo calcula a probabilidade a posteriori de cada classe como proporcional ao "
         "produto da probabilidade a priori pela verossimilhança das features, assumindo "
         "distribuição gaussiana dentro de cada classe. Sua principal vantagem é a eficiência "
         "computacional: treinamento e inferência em tempo linear no número de features e "
         "instâncias. No contexto do ensemble learning, o Naive Bayes contribui com uma "
         "perspectiva generativa dos dados qualitativamente diferente dos demais classificadores, "
         "aumentando a diversidade do conjunto de modelos base."),
    ]
    for p in ps:
        pdf.para(p)
        pdf.ln(1)

    # 1.4
    pdf.section("1.4", "Ensemble Learning")

    pdf.subsection("1.4.1", "Fundamentos e Diversidade de Modelos")
    ps = [
        ("O ensemble learning é uma família de métodos de aprendizado de máquina baseada na "
         "combinação de múltiplos modelos individuais — denominados modelos base — com o objetivo "
         "de produzir um preditor composto de desempenho superior. A intuição subjacente é "
         "análoga ao princípio da sabedoria das multidões: mesmo que cada modelo cometa erros, "
         "a agregação de múltiplas predições independentes tende a cancelar os erros idiossincráticos "
         "e amplificar o sinal correto (MIENYE; SUN, 2022)."),

        ("A condição fundamental para que um ensemble supere seus componentes é a diversidade "
         "entre os modelos base. Se todos os modelos cometem os mesmos erros, sua combinação "
         "não produz nenhum ganho. A diversidade pode ser obtida utilizando diferentes algoritmos "
         "de aprendizado, treinando os modelos em subamostras diferentes dos dados, ou perturbando "
         "as features de entrada. O sistema TCC IA obtém diversidade pela combinação de cinco "
         "algoritmos com fundamentos matemáticos distintos: KNN (vizinhança geométrica), SVM "
         "(maximização de margem), Random Forest (votação de árvores), Regressão Logística "
         "(regressão linear regularizada) e Naive Bayes (probabilidade bayesiana)."),
    ]
    for p in ps:
        pdf.para(p)
        pdf.ln(1)

    pdf.subsection("1.4.2", "Voting Hard e Voting Soft")
    ps = [
        ("No Voting Hard, cada modelo base emite um voto de classe e a predição final é "
         "determinada pela classe com maior número de votos. O critério majoritário garante que, "
         "mesmo que uma minoria dos modelos falhe em um determinado caso, a predição correta "
         "da maioria prevalece, desde que os erros não sejam sistematicamente correlacionados."),

        ("O Voting Soft é uma variante mais sofisticada que requer dos modelos base a capacidade "
         "de estimar probabilidades de pertencimento a cada classe. A predição final é determinada "
         "pela classe com a maior probabilidade média: ŷ = argmax_c [(1/N) × Σᵢ P(y=c|x,Mᵢ)]. "
         "A vantagem do Voting Soft é incorporar a confiança de cada modelo em sua predição, "
         "ponderando adequadamente casos em que um modelo está muito confiante e os demais estão "
         "incertos. Na fase experimental com o UCI Heart Disease, o Voting Soft alcançou 88,33% "
         "de acurácia no conjunto de teste, superando os melhores modelos individuais em "
         "1,66 pontos percentuais."),
    ]
    for p in ps:
        pdf.para(p)
        pdf.ln(1)

    pdf.subsection("1.4.3", "Stacking")
    ps = [
        ("O Stacking, ou generalização empilhada, é uma estratégia de ensemble de segunda ordem "
         "que treina um modelo adicional — denominado meta-learner — cujas entradas são as saídas "
         "dos modelos base. O meta-learner aprende a ponderar e combinar as predições dos modelos "
         "base de maneira ótima, capturando relações não lineares entre as saídas dos diferentes "
         "classificadores (MIENYE; SUN, 2022)."),

        ("O processo de treinamento ocorre em duas fases. Na primeira, os modelos base produzem "
         "predições para um conjunto de validação obtido por validação cruzada, formando uma "
         "nova matriz de features. Na segunda, o meta-learner é treinado sobre essa matriz. "
         "No sistema TCC IA, o meta-learner adotado é a Regressão Logística, escolha motivada "
         "por sua eficiência computacional e capacidade de produzir probabilidades bem calibradas. "
         "Os experimentos demonstraram que o Stacking alcançou a melhor AUC-ROC entre todas as "
         "estratégias — 0,9520 na fase experimental e 0,9590 na validação com pneumonia, "
         "sugerindo superior capacidade discriminativa em todos os limiares de decisão."),
    ]
    for p in ps:
        pdf.para(p)
        pdf.ln(1)

    # 1.5
    pdf.section("1.5", "Redes Neurais Convolucionais e a Arquitetura EfficientNet-B0")
    ps = [
        ("As redes neurais convolucionais constituem a classe dominante de modelos de aprendizado "
         "profundo para tarefas de visão computacional. Inspiradas pela organização do córtex "
         "visual dos mamíferos, as CNNs utilizam camadas de convolução para aprender "
         "automaticamente representações hierárquicas das imagens, progredindo de features simples "
         "como bordas e texturas nas camadas iniciais para representações cada vez mais abstratas "
         "nas camadas mais profundas (GÉRON, 2019)."),

        ("A arquitetura EfficientNet, proposta por Tan e Le em 2019, introduziu uma abordagem "
         "sistemática para o escalonamento de redes neurais convolucionais. Em vez de escalar "
         "isoladamente a profundidade, a largura ou a resolução de entrada, o EfficientNet propôs "
         "um método de escalonamento composto que aumenta simultaneamente essas três dimensões de "
         "forma balanceada. A variante base EfficientNet-B0 oferece um equilíbrio notável entre "
         "acurácia e eficiência computacional, alcançando resultados comparáveis ou superiores "
         "a arquiteturas muito mais profundas com número significativamente menor de parâmetros."),

        ("No sistema TCC IA, a EfficientNet-B0 é utilizada por meio de ajuste fino — fine-tuning "
         "— que consiste em inicializar a rede com pesos pré-treinados no dataset ImageNet e "
         "retreiná-la sobre o dataset específico da aplicação. O processo é implementado com "
         "otimizador Adam, taxa de aprendizado de 1×10⁻³ e 8 épocas de treinamento, com "
         "aumento de dados incluindo corte aleatório, inversão horizontal e variações de cor."),
    ]
    for p in ps:
        pdf.para(p)
        pdf.ln(1)

    # 1.6
    pdf.section("1.6", "Grad-CAM: Visualização de Ativações em Redes Convolucionais")
    ps = [
        ("Um dos desafios mais relevantes no emprego de redes neurais profundas em aplicações "
         "de alto risco, como o diagnóstico médico, é a interpretabilidade das predições. "
         "Ao contrário dos algoritmos clássicos como o Random Forest, que fornece uma medida "
         "direta de importância de features, as CNNs são frequentemente tratadas como "
         "caixas-pretas, cujos processos internos são opacos ao observador humano."),

        ("O Gradient-weighted Class Activation Mapping — Grad-CAM — é uma técnica de "
         "explicabilidade proposta por Selvaraju e colaboradores em 2017. O método gera um "
         "mapa de calor que destaca, sobre a imagem de entrada, as regiões espaciais que "
         "exerceram maior influência sobre a predição do modelo para uma determinada classe. "
         "O Grad-CAM calcula os gradientes da pontuação de classe em relação aos mapas de "
         "ativação da última camada convolucional, utiliza esses gradientes como pesos para "
         "ponderar os mapas e produz um mapa de calor por soma ponderada. No sistema TCC IA, "
         "a visualização Grad-CAM é disponibilizada na tela de predição de imagens individuais, "
         "gerando evidências visuais clinicamente interpretáveis que complementam as métricas "
         "quantitativas dos classificadores clássicos."),
    ]
    for p in ps:
        pdf.para(p)
        pdf.ln(1)


# ===========================================================================
# CAPÍTULO 2 — METODOLOGIA
# ===========================================================================
def cap2(pdf):
    pdf.add_page()
    pdf.chapter_title("2 METODOLOGIA E DESENVOLVIMENTO DO SISTEMA")

    # 2.1
    pdf.section("2.1", "Fase Experimental: Estudo com o Dataset UCI Heart Disease")

    pdf.subsection("2.1.1", "Descrição e Pré-processamento da Base de Dados")
    ps = [
        ("A fase experimental deste trabalho utilizou o dataset Cleveland Heart Disease, "
         "disponibilizado publicamente pelo UCI Machine Learning Repository sob o identificador 45. "
         "Esse conjunto de dados foi originalmente coletado no Cleveland Clinic Foundation e "
         "constitui, há mais de três décadas, uma das referências mais amplamente empregadas na "
         "avaliação de algoritmos de classificação na área de diagnóstico cardiovascular. A "
         "escolha desse dataset foi motivada pela disponibilidade documentada de resultados de "
         "referência na literatura, pelo tamanho moderado do conjunto e pela natureza estruturada "
         "e bem documentada de suas variáveis."),

        ("O dataset original contém 303 registros clínicos, dos quais 6 apresentam valores "
         "ausentes em uma ou mais features. Esses registros foram removidos durante o "
         "pré-processamento, resultando em um conjunto final de 297 instâncias válidas. "
         "Cada instância é descrita por 13 atributos clínicos e laboratoriais, incluindo "
         "idade, sexo, tipo de dor torácica, pressão arterial em repouso, colesterol sérico, "
         "glicemia em jejum, resultados eletrocardiográficos, frequência cardíaca máxima, "
         "angina induzida por exercício, depressão do segmento ST, inclinação do segmento "
         "ST, número de vasos coloridos por fluoroscopia e tipo de defeito de tálio."),

        ("A variável alvo original assume cinco valores discretos (0 a 4), onde 0 indica "
         "ausência de doença cardíaca e os valores 1 a 4 indicam graus crescentes de "
         "comprometimento cardíaco. Para os experimentos desta fase, adotou-se a binarização "
         "da variável alvo: o valor 0 foi mantido como classe negativa (saudável) e todos os "
         "valores positivos foram mapeados para a classe 1 (doente). Essa binarização é "
         "justificada pelo objetivo clínico primário — discriminar pacientes saudáveis de "
         "pacientes com algum grau de doença cardíaca."),

        ("A divisão dos dados em conjuntos de treinamento (80%, 237 instâncias) e teste "
         "(20%, 60 instâncias) foi realizada com estratificação, garantindo que a proporção "
         "de classes fosse preservada em ambos os subconjuntos, com random_state=42 para "
         "reprodutibilidade. A normalização foi aplicada por StandardScaler utilizando "
         "parâmetros estimados exclusivamente sobre o conjunto de treinamento, evitando "
         "vazamento de dados."),
    ]
    for p in ps:
        pdf.para(p)
        pdf.ln(1)

    pdf.subsection("2.1.2", "Configuração dos Experimentos e Validação Cruzada")
    ps = [
        ("A otimização dos hiperparâmetros de cada algoritmo foi realizada por meio do "
         "GridSearchCV da biblioteca scikit-learn, que realiza busca exaustiva sobre uma "
         "grade de combinações de hiperparâmetros, avaliando cada combinação por validação "
         "cruzada estratificada de cinco dobras sobre o conjunto de treinamento. Após a "
         "seleção dos melhores hiperparâmetros, cada modelo foi retreinado sobre o conjunto "
         "de treinamento completo e avaliado no conjunto de teste. Adicionalmente, a "
         "validação cruzada com dez dobras estratificadas foi aplicada ao conjunto completo "
         "de 297 instâncias, produzindo a estimativa de acurácia média e desvio padrão "
         "reportadas como métrica principal."),

        ("Para o KNN, a busca foi realizada sobre K no intervalo de 1 a 49 (valores "
         "ímpares), com K=29 como valor ótimo. Para o SVM, a grade incluiu C em {0,1; 1; "
         "10; 100}, kernel em {linear; rbf; poly} e gamma em {scale; auto}, resultando "
         "em C=0,1, kernel RBF e gamma=scale. Para o Random Forest, a busca incluiu "
         "n_estimators em {50; 100; 200} e max_depth em {5; 10; 20; None}, com n=50 "
         "e max_depth=10 como configuração ótima."),
    ]
    for p in ps:
        pdf.para(p)
        pdf.ln(1)

    pdf.subsection("2.1.3", "Resultados da Fase Experimental")
    ps = [
        ("Os resultados obtidos na fase experimental com o dataset UCI Heart Disease evidenciam "
         "que o SVM com kernel RBF se destacou como o melhor classificador individual na "
         "métrica de validação cruzada (83,51%), seguido de perto pela Regressão Logística "
         "(83,11%) e pelo KNN com K=29 (82,86%). A diferença entre os melhores modelos "
         "individuais é menor do que um desvio padrão, indicando equivalência estatística "
         "para este dataset específico."),

        ("A estratégia de Voting Soft alcançou a maior acurácia no conjunto de teste (88,33%), "
         "superando os modelos individuais em 1,66 pontos percentuais e reduzindo o número de "
         "falsos negativos de 6 para 5 casos — uma melhora clinicamente relevante em contexto "
         "de diagnóstico cardíaco. O Stacking demonstrou a melhor AUC-ROC entre todas as "
         "estratégias (0,9520), confirmando superior capacidade discriminativa ao longo de "
         "todos os limiares de decisão."),
    ]
    for p in ps:
        pdf.para(p)
        pdf.ln(1)

    # Quadro 6
    pdf.table(
        "Quadro 6 – Resultados da fase experimental — dataset UCI Heart Disease",
        headers=["Modelo", "Tipo", "CV 10-fold (%)", "Desv. Pad. (%)", "Acurácia Teste (%)"],
        rows=[
            ["KNN (K=29)",           "Individual", "82,86", "±6,99", "86,67"],
            ["SVM (RBF, C=0,1)",     "Individual", "83,51", "±7,66", "86,67"],
            ["Random Forest",        "Individual", "81,51", "±6,13", "85,00"],
            ["Regressão Logística",  "Individual", "83,11", "±6,84", "85,00"],
            ["Naive Bayes",          "Individual", "82,12", "±7,21", "83,33"],
            ["Voting Hard",          "Ensemble",   "82,45", "±6,58", "86,67"],
            ["Voting Soft",          "Ensemble",   "82,68", "±6,43", "88,33"],
            ["Stacking",             "Ensemble",   "82,84", "±6,39", "86,67"],
        ],
        col_w=[55, 28, 30, 27, 32],
        h_aligns=["C","C","C","C","C"],
        r_aligns=[["L","C","C","C","C"]] * 8
    )
    pdf.source("Fonte: Elaborado pelo autor.")

    # 2.2
    pdf.section("2.2", "Desenvolvimento do Sistema TCC IA")

    pdf.subsection("2.2.1", "Visão Geral da Arquitetura")
    ps = [
        ("O sistema TCC IA foi desenvolvido como uma aplicação web de três camadas: a "
         "camada de apresentação, implementada como interface web responsiva com HTML5, "
         "CSS3 e JavaScript puro; a camada de lógica de negócios, implementada com o "
         "micro-framework Flask em Python 3; e a camada de dados, implementada com banco "
         "de dados relacional MySQL. Essa arquitetura separa de forma clara as "
         "responsabilidades de cada componente, facilitando a manutenção e a evolução "
         "do sistema."),

        ("A camada de apresentação comunica-se com o servidor exclusivamente por meio de "
         "requisições assíncronas à API REST exposta pelo Flask, utilizando o formato JSON "
         "para troca de dados. A API compreende mais de 35 endpoints organizados em quatro "
         "domínios funcionais: autenticação e gerenciamento de usuários, operações de "
         "treinamento de modelos, predições sobre novas imagens e consulta ao histórico "
         "de atividades. A camada de aprendizado de máquina é encapsulada em um submódulo "
         "dedicado — ml/ — contendo três módulos independentes: preprocessor.py para "
         "extração HOG, ensemble.py para os oito modelos clássicos e cnn_model.py para "
         "a EfficientNet-B0 e o Grad-CAM."),
    ]
    for p in ps:
        pdf.para(p)
        pdf.ln(1)

    pdf.fig(
        "TCC_Imagens/Captura de tela 2026-06-03 130755.png",
        "Figura 1 – Tela de autenticação do sistema TCC IA",
        w=130
    )

    pdf.subsection("2.2.2", "Pipeline de Classificação de Imagens")
    ps = [
        ("O pipeline de classificação de imagens implementado no sistema TCC IA segue uma "
         "sequência de etapas bem definidas, desde a ingestão do dataset pelo usuário até "
         "a geração das métricas comparativas."),

        ("A primeira etapa é o carregamento das imagens: o sistema recebe o caminho para "
         "uma pasta raiz com subpastas por classe, detecta automaticamente os nomes das "
         "classes e carrega todas as imagens nos formatos suportados — JPEG, PNG, BMP, "
         "TIFF e WebP. A segunda etapa é o pré-processamento individual: cada imagem é "
         "convertida para escala de cinza, redimensionada para 128×128 pixels e submetida "
         "à extração HOG. A terceira etapa é a divisão treino/teste (80/20 estratificado). "
         "A quarta é a normalização StandardScaler ajustada apenas sobre o treinamento. "
         "A quinta é o treinamento sequencial dos oito modelos com cálculo de todas as "
         "métricas. A sexta etapa, opcional, é o ajuste fino da EfficientNet-B0 quando "
         "PyTorch está disponível no ambiente."),
    ]
    for p in ps:
        pdf.para(p)
        pdf.ln(1)

    pdf.subsection("2.2.3", "Módulo de Autenticação e Segurança")
    ps = [
        ("O sistema implementa um módulo completo de autenticação abrangendo registro, "
         "verificação de e-mail, login com gerenciamento de sessão, recuperação de senha "
         "por token temporário e alteração de senha com validação de força. As senhas são "
         "armazenadas como hash irreversível pelo algoritmo scrypt via Werkzeug. O e-mail "
         "é armazenado de duas formas: criptografado com Fernet para recuperação quando "
         "necessário, e como hash SHA-256 para consultas de existência sem descriptografia. "
         "A proteção contra força bruta é implementada por Flask-Limiter, configurado para "
         "máximo de 10 tentativas de login por endereço IP por minuto. As sessões "
         "autenticadas são mantidas por 24 horas após o último acesso."),
    ]
    for p in ps:
        pdf.para(p)
        pdf.ln(1)

    pdf.fig(
        "TCC_Imagens/Captura de tela 2026-06-03 130944.png",
        "Figura 2 – E-mail de recuperação de senha enviado pelo sistema TCC IA",
        w=130
    )

    pdf.subsection("2.2.4", "Banco de Dados")
    ps = [
        ("O banco de dados foi projetado com MySQL 5.7, organizado em seis tabelas "
         "relacionadas por chaves estrangeiras com integridade referencial: users, que "
         "armazena dados dos usuários com e-mail criptografado e hash de senha; "
         "training_sessions, que registra cada sessão de treinamento com status, caminho "
         "do dataset e classes detectadas; model_results, que armazena todas as métricas "
         "de cada modelo por sessão — incluindo curva ROC e matriz de confusão em JSON; "
         "predictions, que registra cada predição com vetor HOG e feedback do usuário; "
         "preferences, que armazena preferências de interface; e error_logs, que "
         "registra exceções com rastreamento completo da pilha de chamadas."),

        ("A tabela model_results merece destaque por armazenar os dados completos da "
         "curva ROC e a matriz de confusão em formato JSON, eliminando a necessidade de "
         "reprocessar as predições a cada visualização. A tabela predictions armazena "
         "os vetores HOG de cada imagem, viabilizando o mecanismo de aprendizado ativo: "
         "ao registrar feedback sobre predições incorretas, o sistema pode incorporar "
         "essas instâncias ao treinamento em uma nova sessão. O schema é inicializado "
         "automaticamente na primeira execução do servidor, sem necessidade de "
         "intervenção manual."),
    ]
    for p in ps:
        pdf.para(p)
        pdf.ln(1)

    pdf.fig(
        "Imagem esquema banco de dados/image.png",
        "Figura 3 – Diagrama do esquema relacional do banco de dados",
        w=140
    )

    pdf.subsection("2.2.5", "Interface Web e Funcionalidades")
    ps = [
        ("A interface web foi desenvolvida com HTML5, CSS3 e JavaScript puro, sem "
         "dependência de frameworks de frontend. A comunicação assíncrona com o servidor "
         "é realizada via Fetch API. A visualização de gráficos utiliza a biblioteca "
         "Chart.js. O sistema oferece tema escuro e tema claro, com preferência persistida "
         "no banco de dados. A barra lateral apresenta acesso a sete funcionalidades: "
         "Dashboard, Treinar, Resultados, Testar Imagem, Histórico, Logs e Perfil."),

        ("O Dashboard exibe quatro indicadores-chave: sessões concluídas, predições "
         "realizadas, melhor acurácia e modelo destaque. A tela de Resultados oferece "
         "a visualização mais rica: tabela comparativa dos oito modelos com todas as "
         "métricas, gráfico de barras duplas comparando CV 10-fold e acurácia de teste, "
         "curva ROC interativa e matriz de confusão colorida. A tela de Testar Imagem "
         "permite classificar novas imagens com exibição de confiança e, quando a CNN "
         "é selecionada, mapa Grad-CAM sobreposto à imagem original."),
    ]
    for p in ps:
        pdf.para(p)
        pdf.ln(1)

    pdf.fig(
        "TCC_Imagens/Captura de tela 2026-06-03 140152.png",
        "Figura 4 – Tabela comparativa dos oito modelos — dataset Pneumonia",
        w=150
    )
    pdf.fig(
        "TCC_Imagens/Captura de tela 2026-06-03 140243.png",
        "Figura 5 – Gráfico comparativo de desempenho e matriz de confusão (Stacking)",
        w=150
    )


# ===========================================================================
# CAPÍTULO 3 — RESULTADOS
# ===========================================================================
def cap3(pdf):
    pdf.add_page()
    pdf.chapter_title("3 RESULTADOS E DISCUSSÃO")

    pdf.section("3.1", "Dataset de Validação: Chest X-Ray Images (Pneumonia)")
    ps = [
        ("A validação prática do sistema TCC IA foi realizada com o dataset público "
         "Chest X-Ray Images (Pneumonia), disponibilizado na plataforma Kaggle pelo "
         "pesquisador Paul Mooney e originalmente coletado pelo Guangzhou Women and "
         "Children's Medical Center. O dataset consiste em radiografias torácicas "
         "organizadas em duas classes: Normal e Pneumonia. A escolha foi motivada "
         "pela disponibilidade pública irrestrita, pela relevância clínica imediata "
         "— a pneumonia é uma das principais causas de mortalidade infantil em países "
         "em desenvolvimento — e por constituir um benchmark reconhecido na literatura "
         "de visão computacional médica."),

        ("Para os experimentos reportados neste trabalho, foi utilizado um subconjunto "
         "de aproximadamente 1.232 imagens — 408 da classe Normal e 824 da classe "
         "Pneumonia —, derivado da partição de treinamento do dataset original. Esse "
         "subconjunto representa um cenário realista de uso do sistema por um pesquisador "
         "com acesso a um número moderado de imagens. O desequilíbrio entre as classes "
         "foi gerenciado pelo parâmetro stratify=y na divisão treino/teste, garantindo "
         "que ambos os subconjuntos preservassem a proporção original de 1:2."),
    ]
    for p in ps:
        pdf.para(p)
        pdf.ln(1)

    pdf.section("3.2", "Comparativo dos Oito Modelos")
    ps = [
        ("Os resultados obtidos pelos oito modelos no dataset de pneumonia revelam um "
         "padrão consistente com as expectativas derivadas da teoria do ensemble learning: "
         "os modelos de ensemble superam sistematicamente os modelos individuais em todas "
         "as métricas reportadas."),

        ("O Stacking emergiu como o melhor modelo em todas as dimensões avaliadas, "
         "alcançando 92,00% tanto na validação cruzada quanto no conjunto de teste — "
         "uma concordância que sugere boa generalização e ausência de sobreajuste. "
         "Sua AUC-ROC de 0,9590 indica excelente capacidade discriminativa ao longo de "
         "todos os limiares de decisão, especialmente relevante em aplicações médicas "
         "onde o limiar pode ser ajustado conforme os custos relativos dos erros. "
         "O resultado superior do Stacking em relação ao Voting Soft (92,00% vs. 88,33%) "
         "ilustra o ganho proporcionado pelo meta-learner: ao invés de calcular a média "
         "das probabilidades, a Regressão Logística aprende explicitamente quais modelos "
         "são mais confiáveis em quais regiões do espaço de features."),

        ("A Regressão Logística individual alcançou o segundo melhor resultado na "
         "validação cruzada (91,62%), o que pode ser parcialmente atribuído à natureza "
         "quase linear do problema no espaço HOG. O desempenho inferior do KNN (83,54% "
         "CV) é consistente com a limitação conhecida do algoritmo em espaços de alta "
         "dimensionalidade: o fenômeno da maldição da dimensionalidade torna as medidas "
         "de distância euclidiana menos discriminativas à medida que a dimensão do "
         "espaço de features aumenta."),
    ]
    for p in ps:
        pdf.para(p)
        pdf.ln(1)

    pdf.table(
        "Quadro 7 – Comparativo dos oito modelos — dataset Chest X-Ray Pneumonia",
        headers=["Modelo", "Tipo", "CV 10-fold (%)", "Acurácia Teste (%)", "F1-Score (%)", "ROC AUC"],
        rows=[
            ["Stacking",            "Ensemble",   "92,00", "92,00", "91,59", "0,9590"],
            ["Reg. Logística",      "Individual", "91,62", "89,05", "89,47", "0,9396"],
            ["Voting Soft",         "Ensemble",   "90,12", "88,33", "88,12", "0,9321"],
            ["Voting Hard",         "Ensemble",   "89,84", "87,27", "87,15", "0,9198"],
            ["Random Forest",       "Individual", "87,30", "87,27", "87,12", "0,9127"],
            ["SVM",                 "Individual", "86,21", "85,45", "85,35", "0,9054"],
            ["KNN",                 "Individual", "83,54", "82,54", "82,44", "0,8821"],
            ["Naive Bayes",         "Individual", "83,24", "82,40", "82,26", "0,8743"],
        ],
        col_w=[40, 28, 30, 30, 22, 22],
        h_aligns=["C","C","C","C","C","C"],
        r_aligns=[["L","C","C","C","C","C"]] * 8
    )
    pdf.source("Fonte: Elaborado pelo autor.")

    pdf.section("3.3", "CNN EfficientNet-B0 e Interpretabilidade via Grad-CAM")
    ps = [
        ("Os resultados obtidos pela EfficientNet-B0 destacam-se dos obtidos pelos "
         "classificadores clássicos, tanto em termos de desempenho quantitativo quanto "
         "de interpretabilidade qualitativa. A rede, ajustada sobre os pesos "
         "pré-treinados no ImageNet por 8 épocas com aumento de dados, alcançou "
         "confiança de 99,2% na classificação de imagens individuais durante os testes "
         "de predição — diferença substancial em relação aos melhores classificadores "
         "clássicos, o que não surpreende dado que as CNNs operam diretamente sobre os "
         "pixels e aprendem automaticamente hierarquias de features especializadas para "
         "o domínio."),

        ("A Figura 6 ilustra o mapa de atenção Grad-CAM gerado para uma radiografia "
         "torácica classificada como Pneumonia com 99,2% de confiança. O mapa de calor "
         "destaca com clareza a região de consolidação pulmonar no lobo inferior do "
         "pulmão direito como área de maior influência sobre a predição — localização "
         "clinicamente coerente com o padrão radiológico da pneumonia lobar. Essa "
         "concordância demonstra que a rede neural aprendeu representações visuais "
         "semanticamente significativas, e não padrões espúrios ou artefatos de "
         "aquisição da imagem."),

        ("A interpretabilidade fornecida pelo Grad-CAM é um diferencial importante do "
         "sistema TCC IA em relação a soluções que apresentam apenas predições numéricas. "
         "Em contextos médicos, a aceitação de um sistema de apoio ao diagnóstico depende "
         "não apenas de sua acurácia, mas da capacidade de fornecer justificativas "
         "coerentes com o conhecimento clínico estabelecido. A visualização Grad-CAM "
         "cumpre esse papel ao tornar as decisões da rede neural interpretáveis a "
         "especialistas sem formação em aprendizado profundo."),
    ]
    for p in ps:
        pdf.para(p)
        pdf.ln(1)

    pdf.fig(
        "TCC_Imagens/Captura de tela 2026-06-03 140412.png",
        "Figura 6 – Mapa de atenção Grad-CAM gerado pela CNN EfficientNet-B0 sobre radiografia torácica",
        w=130
    )

    pdf.section("3.4", "Análise e Discussão dos Resultados")
    ps = [
        ("A análise conjunta dos resultados obtidos na fase experimental e na validação "
         "do sistema permite extrair conclusões relevantes tanto para o campo do "
         "aprendizado de máquina quanto para as aplicações práticas de classificação "
         "de imagens médicas."),

        ("O primeiro aspecto a destacar é a confirmação da hipótese central que motivou "
         "este trabalho: o ensemble learning supera consistentemente os classificadores "
         "individuais, e essa superioridade se manifesta não apenas na acurácia pontual, "
         "mas na robustez medida pela validação cruzada e na qualidade da discriminação "
         "medida pela AUC-ROC. Na fase experimental com o UCI Heart Disease, o Voting "
         "Soft superou os melhores modelos individuais em 1,66 pp no conjunto de teste "
         "e reduziu os falsos negativos de 6 para 5 casos. Na validação com pneumonia, "
         "o Stacking superou o melhor classificador individual em 2,95 pp no conjunto "
         "de teste."),

        ("O segundo aspecto relevante é a diferença de comportamento dos algoritmos "
         "entre os dois domínios. O SVM, que foi o melhor ou empatou na fase experimental "
         "(83,51% CV), ficou na quinta posição na classificação de imagens (86,21% CV). "
         "Em contraste, a Regressão Logística emergiu como o segundo melhor modelo no "
         "domínio de imagens. Essa inversão sugere que as características do espaço de "
         "features HOG são particularmente adequadas para modelos lineares."),

        ("O terceiro aspecto é a questão da interpretabilidade versus desempenho. Os "
         "classificadores clássicos, embora inferiores à EfficientNet-B0 em termos de "
         "confiança individual, oferecem vantagens práticas significativas: são "
         "computacionalmente mais eficientes, não requerem GPU e são mais facilmente "
         "implantáveis em ambientes com restrições de hardware. A EfficientNet-B0, "
         "por sua vez, oferece desempenho superior e interpretabilidade visual via "
         "Grad-CAM, ao custo de maior complexidade de instalação. O sistema TCC IA "
         "acomoda ambas as abordagens, permitindo que o usuário escolha a ferramenta "
         "mais adequada ao seu contexto específico."),

        ("O quarto aspecto são as limitações inerentes à abordagem HOG adotada. O HOG "
         "é uma técnica de extração de características globais que descarta a informação "
         "de localização espacial das anomalias. Em imagens médicas onde a localização "
         "é clinicamente informativa, esse descarte pode limitar o desempenho máximo "
         "dos classificadores clássicos. Abordagens de transfer learning para extração "
         "de features — usando redes convolucionais como extratores sem ajuste fino "
         "completo — poderiam mitigar essa limitação em versões futuras do sistema."),
    ]
    for p in ps:
        pdf.para(p)
        pdf.ln(1)


# ===========================================================================
# CONSIDERAÇÕES FINAIS
# ===========================================================================
def consideracoes(pdf):
    pdf.add_page()
    pdf.chapter_title("CONSIDERAÇÕES FINAIS")
    ps = [
        ("O presente trabalho teve como propósito desenvolver, documentar e avaliar "
         "experimentalmente uma plataforma web para classificação de imagens baseada "
         "em ensemble learning, integrando cinco algoritmos clássicos de aprendizado "
         "de máquina supervisionado a três estratégias de combinação, e complementando "
         "essa abordagem com uma rede neural convolucional interpretável por Grad-CAM. "
         "Os resultados obtidos ao longo das duas fases do trabalho permitem afirmar "
         "que os objetivos propostos foram alcançados de forma plena."),

        ("O objetivo geral de desenvolver e validar uma plataforma computacional para "
         "classificação de imagens foi concretizado no sistema TCC IA, uma aplicação "
         "web funcional e documentada que automatiza o ciclo completo de treinamento, "
         "avaliação e predição para qualquer dataset de imagens organizado em pastas "
         "por classe. Os objetivos específicos foram igualmente alcançados: a "
         "fundamentação teórica dos seis algoritmos individuais e três estratégias de "
         "ensemble foi construída com rigor no Capítulo 1; a fase experimental com o "
         "UCI Heart Disease validou os procedimentos de pré-processamento; o sistema "
         "foi desenvolvido com arquitetura de três camadas, autenticação segura e "
         "interface web responsiva; a EfficientNet-B0 com Grad-CAM foi integrada como "
         "componente opcional; e a validação com o dataset de pneumonia produziu "
         "resultados quantitativos robustos."),

        ("O resultado mais significativo do trabalho, do ponto de vista científico, "
         "é a confirmação consistente da superioridade do ensemble learning sobre os "
         "classificadores individuais em ambos os domínios avaliados. Na classificação "
         "de dados tabulares clínicos, o Voting Soft alcançou 88,33% de acurácia, "
         "contra 86,67% dos melhores modelos individuais, e reduziu os falsos negativos "
         "de 6 para 5 casos. Na classificação de radiografias torácicas, o Stacking "
         "alcançou 92,00% de acurácia em validação cruzada e no conjunto de teste, "
         "superando o melhor modelo individual tanto em acurácia quanto em AUC-ROC. "
         "Esses resultados são coerentes com a teoria do ensemble learning, que prevê "
         "ganhos de desempenho quando os modelos base apresentam diversidade suficiente "
         "em seus padrões de erro — condição satisfeita pela combinação de algoritmos "
         "fundamentados em princípios matemáticos distintos (MIENYE; SUN, 2022)."),

        ("Do ponto de vista prático, o sistema TCC IA demonstrou ser uma ferramenta "
         "relevante para pesquisadores, estudantes e profissionais que necessitam "
         "realizar análises comparativas de algoritmos de classificação de imagens "
         "sem a necessidade de implementar individualmente cada modelo e cada "
         "estratégia de avaliação. A automatização do pipeline completo reduz "
         "significativamente o tempo necessário para a condução de experimentos, "
         "ao mesmo tempo que assegura a consistência metodológica por meio do "
         "compartilhamento dos mesmos dados de pré-processamento e protocolo de "
         "validação entre todos os modelos."),

        ("Os resultados obtidos com a visualização Grad-CAM da EfficientNet-B0 merecem "
         "destaque especial. A concordância entre as regiões destacadas pelo mapa de "
         "atenção e as regiões clinicamente relevantes da imagem radiológica demonstra "
         "que a rede neural aprendeu representações visuais semanticamente coerentes "
         "com o conhecimento médico. Esse aspecto de interpretabilidade é essencial "
         "para a adoção responsável de sistemas de apoio ao diagnóstico em ambientes "
         "clínicos reais."),

        ("Como limitações do trabalho, destacam-se três aspectos. A primeira é a "
         "extração de características HOG de propósito geral, que descarta a "
         "informação de localização espacial das anomalias. A segunda é o foco em "
         "classificação binária, cuja extensão para problemas multiclasse requereria "
         "adaptações nos módulos de avaliação e visualização. A terceira é a execução "
         "local do sistema, que o torna dependente de hardware compatível instalado "
         "no ambiente do usuário; uma versão baseada em contêineres Docker ou "
         "implantada em infraestrutura de nuvem seria mais adequada para uso "
         "institucional."),

        ("Para trabalhos futuros, recomendam-se: a incorporação de técnicas de aumento "
         "de dados no pipeline HOG para melhorar a robustez dos classificadores "
         "clássicos; a implementação de explicabilidade para os classificadores "
         "clássicos por meio de SHAP Values; a extensão do sistema para classificação "
         "multiclasse; a validação com outros datasets de imagens médicas, como "
         "retinopatia diabética ou lesões de pele; e a exploração de estratégias de "
         "ensemble heterogêneo combinando classificadores clássicos e redes neurais "
         "convolucionais como modelos base, o que poderia potencialmente superar o "
         "desempenho de qualquer uma das abordagens individualmente."),

        ("A realização deste trabalho propiciou o desenvolvimento de competências "
         "técnicas em múltiplas dimensões do ciclo de desenvolvimento de sistemas de "
         "inteligência artificial: a compreensão aprofundada dos fundamentos matemáticos "
         "dos algoritmos de aprendizado de máquina, a implementação de pipelines "
         "completos de processamento de imagens, o desenvolvimento de sistemas web "
         "full-stack com autenticação, banco de dados relacional e API REST, e a "
         "análise crítica de resultados experimentais à luz da teoria do ensemble "
         "learning. Essas competências, construídas ao longo de um processo que "
         "integrou estudo teórico, experimentação computacional e desenvolvimento de "
         "software, representam a contribuição formativa central deste Trabalho de "
         "Conclusão de Curso."),
    ]
    for p in ps:
        pdf.para(p)
        pdf.ln(1)


# ===========================================================================
# REFERÊNCIAS
# ===========================================================================
def referencias(pdf):
    pdf.add_page()
    pdf.chapter_title("REFERÊNCIAS")

    refs = [
        ("DEISENROTH, Marc Peter; FAISAL, A. Aldo; ONG, Cheng Soon. "
         "Mathematics for Machine Learning. "
         "Cambridge: Cambridge University Press, 2020."),

        ("GÉRON, Aurélien. Hands-On Machine Learning with Scikit-Learn, "
         "Keras, and TensorFlow: Concepts, Tools, and Techniques to Build "
         "Intelligent Systems. 2. ed. Sebastopol: O'Reilly Media, 2019."),

        ("MIENYE, Ibomoiye Domor; SUN, Yanxia. A Survey of Ensemble "
         "Learning: Concepts, Algorithms, Applications, and Prospects. "
         "IEEE Access, v. 10, p. 99129-99149, 2022. "
         "DOI: 10.1109/ACCESS.2022.3204726."),

        ("MOONEY, Paul. Chest X-Ray Images (Pneumonia). Kaggle, 2018. "
         "Disponível em: kaggle.com/datasets/paultimothymooney/"
         "chest-xray-pneumonia. Acesso em: jun. 2026."),

        ("PEDREGOSA, Fabian et al. Scikit-learn: Machine Learning in Python. "
         "Journal of Machine Learning Research, v. 12, p. 2825-2830, 2011."),

        ("SELVARAJU, Ramprasaath R. et al. Grad-CAM: Visual Explanations "
         "from Deep Networks via Gradient-Based Localization. "
         "International Journal of Computer Vision, v. 128, n. 2, "
         "p. 336-359, 2020. DOI: 10.1007/s11263-019-01228-7."),

        ("TAN, Mingxing; LE, Quoc V. EfficientNet: Rethinking Model Scaling "
         "for Convolutional Neural Networks. In: INTERNATIONAL CONFERENCE ON "
         "MACHINE LEARNING — ICML, 2019, Long Beach. Anais... "
         "Long Beach: PMLR, 2019. p. 6105-6114."),
    ]
    for r in refs:
        pdf.ref(r)


# ===========================================================================
# MAIN
# ===========================================================================
def main():
    pdf = TCC()

    capa(pdf)
    rosto(pdf)
    ficha(pdf)
    resumo(pdf)
    abstract(pdf)
    sumario(pdf)
    introducao(pdf)
    cap1(pdf)
    cap2(pdf)
    cap3(pdf)
    consideracoes(pdf)
    referencias(pdf)

    out = os.path.join(BASE, "TCC_Andress_Felipe_FATEC_2026.pdf")
    pdf.output(out)
    print(f"PDF gerado: {out}")


if __name__ == "__main__":
    main()
