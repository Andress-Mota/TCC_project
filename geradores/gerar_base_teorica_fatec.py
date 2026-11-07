"""
Base Teorica: Processo e Treinamento de Dados em Aprendizado de Maquina
Formato FATEC 2022 — sem graficos, apenas fundamentacao bibliografica.
"""
import os
from fpdf import FPDF

MARGIN_L  = 20.0
MARGIN_R  = 20.0
MARGIN_T  = 25.0
MARGIN_B  = 20.0
PAGE_W    = 210.0
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R
FONT      = "Arial"
SZ_BODY   = 11
SZ_SMALL  = 10
SZ_TITLE  = 12
LH        = 7.0
LH_SM     = 6.0
LH_TBL    = 5.5
INDENT    = 12.5

BASE = "c:/Users/andre/Documents/TCC project"

FONTS = {
    "":   "C:/Windows/Fonts/arial.ttf",
    "B":  "C:/Windows/Fonts/arialbd.ttf",
    "I":  "C:/Windows/Fonts/ariali.ttf",
    "BI": "C:/Windows/Fonts/arialbi.ttf",
}


class Doc(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        for style, path in FONTS.items():
            if os.path.exists(path):
                self.add_font("Arial", style, path)
        self.set_margins(MARGIN_L, MARGIN_T, MARGIN_R)
        self.set_auto_page_break(True, MARGIN_B)

    def header(self): pass

    def footer(self):
        self.set_y(-15)
        self.set_font(FONT, "", SZ_SMALL)
        self.cell(0, 10, str(self.page_no()), align="C")

    def _font(self, bold=False, italic=False, size=SZ_BODY):
        self.set_font(FONT, ("B" if bold else "") + ("I" if italic else ""), size)

    def para(self, txt, indent=True, align="J", bold=False, italic=False,
             size=SZ_BODY, lh=None, before=0, after=0):
        if before: self.ln(before)
        lh = lh or (LH if size >= SZ_BODY else LH_SM)
        self._font(bold, italic, size)
        x = MARGIN_L + (INDENT if indent else 0)
        self.set_x(x)
        self.multi_cell(CONTENT_W - (INDENT if indent else 0), lh, txt, align=align)
        if after: self.ln(after)

    def center(self, txt, bold=False, italic=False, size=SZ_BODY, lh=None):
        lh = lh or (LH if size >= SZ_BODY else LH_SM)
        self._font(bold, italic, size)
        self.set_x(MARGIN_L)
        self.multi_cell(CONTENT_W, lh, txt, align="C")

    def section(self, num, title):
        self.ln(4)
        self._font(bold=True, size=SZ_BODY)
        label = f"{num} {title}".upper() if num else title.upper()
        self.set_x(MARGIN_L)
        self.multi_cell(CONTENT_W, LH, label, align="L")
        self.ln(1)

    def subsection(self, num, title):
        self.ln(2)
        self._font(bold=True, size=SZ_BODY)
        self.set_x(MARGIN_L)
        self.multi_cell(CONTENT_W, LH, f"{num} {title}", align="L")
        self.ln(1)

    def ref_entry(self, bold_part, rest):
        self._font(bold=True, size=SZ_BODY)
        wb = self.get_string_width(bold_part)
        self.set_x(MARGIN_L)
        self.cell(wb, LH, bold_part)
        self._font(size=SZ_BODY)
        self.multi_cell(CONTENT_W - wb, LH, rest, align="J")
        self.ln(1)


# =============================================================================
# DOCUMENTO
# =============================================================================
pdf = Doc()
pdf.add_page()

# ── TITULO ────────────────────────────────────────────────────────────────────
pdf.center(
    "BASE TEORICA SOBRE PROCESSO E TREINAMENTO DE DADOS EM "
    "APRENDIZADO DE MAQUINA APLICADO AO DIAGNOSTICO DE DOENCAS CARDIACAS",
    bold=True, size=SZ_TITLE, lh=7.5
)
pdf.ln(4)
pdf.center("Andre Felipe de Oliveira", italic=True, size=SZ_SMALL)
pdf.center("Faculdade de Tecnologia de Guaratingueta - FATEC Guaratingueta", size=SZ_SMALL)
pdf.center("andressmota78@gmail.com", size=SZ_SMALL)
pdf.ln(6)

# ── RESUMO ────────────────────────────────────────────────────────────────────
pdf._font(bold=True, size=SZ_BODY)
pdf.set_x(MARGIN_L)
pdf.cell(CONTENT_W, LH, "Resumo", align="L")
pdf.ln(1)
pdf.para(
    "Este trabalho apresenta a fundamentacao teorica dos processos de tratamento "
    "de dados e treinamento de modelos em aprendizado de maquina supervisionado, "
    "com foco em aplicacoes de classificacao clinica. Sao abordados os fundamentos "
    "matematicos do processo de aprendizado a partir de exemplos, as etapas do "
    "pipeline de dados — coleta, limpeza, normalizacao e particao —, os mecanismos "
    "de treinamento por otimizacao, os algoritmos K-Nearest Neighbors, Support "
    "Vector Machine e Ensemble Learning, e os protocolos de avaliacao por validacao "
    "cruzada e metricas de desempenho. Toda a fundamentacao e referenciada "
    "exclusivamente nas obras disponiveis: Giraldi (2021), Geron (2019), "
    "Mienye e Sun (2022) e Uddin et al. (2022).",
    indent=False
)
pdf.para(
    "Palavras-chave: Aprendizado de Maquina; Treinamento de Modelos; "
    "Processamento de Dados; KNN; SVM; Ensemble Learning; Validacao Cruzada.",
    indent=False, italic=True
)
pdf.ln(4)

# ── 1. INTRODUCAO ─────────────────────────────────────────────────────────────
pdf.section("1", "Introducao")
pdf.para(
    "O aprendizado de maquina e a area da inteligencia artificial dedicada ao "
    "desenvolvimento de algoritmos que aprendem padroes a partir de dados empiricos, "
    "sem que suas regras sejam explicitamente programadas (GERON, 2019). A aplicacao "
    "desses algoritmos ao diagnostico medico tem crescido significativamente, "
    "especialmente em doencas cardiovasculares — principal causa de mortalidade "
    "global — onde a identificacao precoce de padroes clinicos de risco pode "
    "fundamentar intervencoes terapeuticas mais oportunas."
)
pdf.para(
    "O desempenho de qualquer modelo de aprendizado de maquina e diretamente "
    "condicionado pela qualidade do processo que antecede o treinamento: a coleta, "
    "a limpeza, a normalizacao e a particao adequada dos dados. Giraldi (2021, p. 96) "
    "define o processo de aprendizado a partir de tres elementos fundamentais: o "
    "conjunto de dados D, a maquina de aprendizado M e o estagio de treinamento. "
    "A negligencia em qualquer dessas etapas compromete a capacidade de generalizacao "
    "do modelo resultante."
)
pdf.para(
    "Este documento apresenta a base teorica que sustenta o pipeline completo de "
    "aprendizado de maquina supervisionado, desde o tratamento dos dados brutos ate "
    "a avaliacao final do modelo treinado. O objetivo nao e apresentar resultados "
    "experimentais, mas sim consolidar o embasamento conceitual necessario para "
    "compreender, reproduzir e criticar as escolhas metodologicas adotadas no "
    "projeto de diagnostico de doencas cardiacas."
)

# ── 2. FUNDAMENTOS DO APRENDIZADO DE MAQUINA ─────────────────────────────────
pdf.section("2", "Fundamentos do Aprendizado de Maquina")

pdf.subsection("2.1", "Categorias de Aprendizado de Maquina")
pdf.para(
    "O aprendizado de maquina classifica-se em quatro categorias principais, "
    "conforme a natureza dos dados disponiveis e o objetivo do processo "
    "(GIRALDI, 2021, p. 99):"
)
pdf.para(
    "(i) Aprendizado supervisionado: o algoritmo recebe um conjunto de amostras "
    "rotuladas e o objetivo e aprender um mapeamento das amostras para os seus "
    "respectivos rotulos. E a categoria mais adotada em classificacao clinica, "
    "onde cada paciente e associado a um diagnostico conhecido (GIRALDI, 2021, p. 99).",
    indent=True
)
pdf.para(
    "(ii) Aprendizado nao supervisionado: o conjunto de dados nao contem rotulos; "
    "o algoritmo descobre estruturas intrinsecas nos dados — agrupamentos, "
    "representacoes comprimidas ou distribuicoes de probabilidade — sem orientacao "
    "externa (GIRALDI, 2021, p. 99).",
    indent=True
)
pdf.para(
    "(iii) Aprendizado semi-supervisionado: combina um conjunto pequeno de amostras "
    "rotuladas com grande quantidade de amostras nao rotuladas. E util quando a "
    "rotulacao manual e custosa, como em imagens medicas (GIRALDI, 2021, p. 99).",
    indent=True
)
pdf.para(
    "(iv) Aprendizado por reforco: o algoritmo aprende por tentativa e erro, "
    "recebendo sinais de recompensa ou penalidade do ambiente, sem instrucao direta "
    "sobre a acao correta (GIRALDI, 2021, p. 100).",
    indent=True
)
pdf.para(
    "No contexto do diagnostico de doencas cardiacas, o aprendizado supervisionado "
    "e o paradigma adequado: cada registro clinico do dataset ja possui rotulo "
    "diagnostico determinado por especialistas, configurando um problema de "
    "classificacao binaria — saudavel ou doente."
)

pdf.subsection("2.2", "O Problema de Aprendizado a partir de Exemplos")
pdf.para(
    "Giraldi (2021, p. 96) formaliza o problema de aprendizado a partir de exemplos "
    "em tres elementos fundamentais: o conjunto de dados D, que representa as amostras "
    "empiricas do fenomeno; a maquina de aprendizado M, que encapsula um espaco "
    "funcional por meio de seus parametros internos; e o estagio de treinamento, "
    "que e o processo pelo qual M ajusta seus parametros com base em D. "
    "Matematicamente, o espaco de dados e representado por D contido em R^m, "
    "onde m e o numero de atributos de cada amostra."
)
pdf.para(
    "Para o problema de reconhecimento de padroes — no qual a maquina deve ser "
    "capaz de classificar corretamente amostras fora do conjunto de treinamento — "
    "o processo de aprendizado e formalizado como a minimizacao de uma funcao de "
    "erro sobre os dados de treinamento (GIRALDI, 2021, p. 97):"
)
pdf.para(
    "Err(z; D) = (1/|D|) SOMA_{i=1}^{|D|} L(M(x_i; z) - d_i)",
    indent=False, italic=True, align="C"
)
pdf.para(
    "onde z e o vetor de parametros da maquina, d_i e a saida desejada para "
    "a amostra x_i, e L e uma metrica de similaridade ou funcao de perda adequada "
    "ao problema. A minimizacao dessa funcional define o chamado problema de "
    "minimizacao do risco empirico, que orienta o processo de treinamento de "
    "praticamente todos os algoritmos de aprendizado supervisionado (GIRALDI, 2021, p. 97)."
)

pdf.subsection("2.3", "O que as Maquinas Aprendem")
pdf.para(
    "Giraldi (2021, p. 99) sistematiza quatro problemas fundamentais de aprendizado "
    "de maquina que decorrem da minimizacao do funcional de perda:"
)
pdf.para(
    "1. Sintese de Dados (modelo generativo): encontrar uma funcao que reproduza "
    "a distribuicao dos dados observados, possibilitando a geracao de novas amostras "
    "sinteticas coerentes com o fenomeno estudado.",
    indent=True
)
pdf.para(
    "2. Reconhecimento de Padroes: apos o treinamento, a maquina deve classificar "
    "corretamente amostras que nao fazem parte do conjunto de treinamento D, "
    "generalizando o conhecimento extraido dos dados rotulados.",
    indent=True
)
pdf.para(
    "3. Estimacao de Regressao: estimar a dependencia funcional baseada nos dados "
    "empiricos, ou seja, aprender uma funcao f: R^m -> R tal que f(x_i) = y_i "
    "para as amostras de treinamento (GIRALDI, 2021, p. 99).",
    indent=True
)
pdf.para(
    "4. Estimacao de Densidade: aprender a distribuicao de probabilidade que gerou "
    "os dados observados, sem necessariamente associar rotulos as amostras.",
    indent=True
)
pdf.para(
    "O diagnostico de doencas cardiacas enquadra-se no problema de Reconhecimento "
    "de Padroes: o modelo treinado deve classificar corretamente novos pacientes "
    "que nao estavam presentes no conjunto de treinamento, generalizando os "
    "padroes clinicos aprendidos a partir dos dados historicos."
)

# ── 3. PIPELINE DE PROCESSAMENTO DE DADOS ─────────────────────────────────────
pdf.section("3", "Pipeline de Processamento de Dados")

pdf.subsection("3.1", "Coleta e Qualidade dos Dados")
pdf.para(
    "O ponto de partida de qualquer projeto de aprendizado de maquina e a obtencao "
    "de dados de qualidade adequada. Uddin et al. (2022) enfatizam que a "
    "representatividade do conjunto de dados e a ausencia de vieses de coleta sao "
    "pre-requisitos para que o modelo treinado seja valido clinicamente. No contexto "
    "de diagnostico cardiaco, o Cleveland Heart Disease Dataset — repositorio UCI "
    "Machine Learning — e amplamente adotado como benchmark justamente pela sua "
    "procedencia clinica controlada e ampla validacao na literatura especializada "
    "(UDDIN et al., 2022)."
)
pdf.para(
    "Dados reais apresentam imperfeicoes sistematicas que precisam ser tratadas "
    "antes do treinamento: valores ausentes (missing values), outliers, "
    "inconsistencias de codificacao e desbalanceamento de classes. Cada um desses "
    "problemas afeta diretamente a qualidade do modelo resultante. Giraldi (2021, p. 149) "
    "lista as etapas basicas de preparacao de dados: identificacao de excecoes e "
    "informacoes ausentes; limpeza por remocao de amostras incorretas ou inconsistentes; "
    "e normalizacao dos dados antes do treinamento."
)

pdf.subsection("3.2", "Limpeza de Dados")
pdf.para(
    "A limpeza de dados compreende a identificacao e o tratamento de registros "
    "incompletos ou incorretos. Registros com valores faltantes podem ser tratados "
    "por tres estrategias principais: (i) remocao do registro, adequada quando a "
    "proporcao de dados ausentes e pequena e a remocao nao introduz vies; "
    "(ii) imputacao pela media ou mediana do atributo; (iii) imputacao por modelos "
    "preditivos que estimam o valor ausente com base nos demais atributos (GERON, 2019). "
    "A escolha entre essas estrategias deve considerar o percentual de dados ausentes, "
    "o mecanismo que gerou a ausencia (aleatoria ou sistematica) e o impacto "
    "potencial no balanceamento das classes."
)
pdf.para(
    "No dataset Cleveland, os 6 registros com valores ausentes (de um total de 303) "
    "representam apenas 1,98% do dataset, justificando a remocao direta sem risco "
    "significativo de vies. Apos a limpeza, restam 297 registros validos para "
    "treinamento e avaliacao dos modelos."
)

pdf.subsection("3.3", "Normalizacao de Dados")
pdf.para(
    "A normalizacao e uma etapa critica quando os atributos do dataset possuem "
    "escalas numericas heterogeneas. Sem normalizacao, atributos com magnitude "
    "elevada dominam o calculo de distancias, tornando os demais atributos "
    "irrelevantes para o processo de aprendizado — problema especialmente critico "
    "para algoritmos baseados em distancia como o KNN (GERON, 2019)."
)
pdf.para(
    "Giraldi (2021, p. 149) descreve o procedimento de normalizacao min-max, que "
    "transforma cada atributo u para o intervalo [0, 1] por meio da operacao:"
)
pdf.para(
    "x_til_uv = (x_uv - x_u,min) / (x_u,max - x_u,min)",
    indent=False, italic=True, align="C"
)
pdf.para(
    "onde x_u,min e x_u,max sao, respectivamente, o valor minimo e maximo do "
    "atributo u no conjunto de treinamento. Alternativamente, a normalizacao "
    "Z-score (ou padronizacao) transforma cada atributo j para media zero e "
    "desvio padrao unitario:"
)
pdf.para(
    "z_ij = (x_ij - media_j) / sigma_j",
    indent=False, italic=True, align="C"
)
pdf.para(
    "onde media_j e sigma_j sao a media e o desvio padrao do atributo j calculados "
    "exclusivamente sobre o conjunto de treinamento (GERON, 2019). E fundamental "
    "que os parametros de normalizacao sejam calculados apenas no conjunto de "
    "treinamento e depois aplicados ao conjunto de teste, pois calcular esses "
    "parametros sobre o dataset completo constitui data leakage — vazamento de "
    "informacao que produz estimativas de desempenho artificialmente otimistas."
)

pdf.subsection("3.4", "Particao dos Dados: Treino, Validacao e Teste")
pdf.para(
    "Antes do treinamento, o conjunto de dados D deve ser dividido em subconjuntos "
    "disjuntos com finalidades distintas. Giraldi (2021, p. 109) define formalmente "
    "essa divisao em tres partes: conjunto de treinamento D_tr, conjunto de "
    "validacao D_val e conjunto de teste D_te. Proporcoes tipicas sao "
    "50:25:25 ou 60:20:20 para treinamento, validacao e teste, respectivamente."
)
pdf.para(
    "O conjunto de treinamento D_tr e usado para ajustar os parametros do modelo "
    "por meio da minimizacao da funcao de perda. O conjunto de validacao D_val "
    "e utilizado para a selecao de hiperparametros e para monitorar o processo "
    "de treinamento, evitando overfitting. O conjunto de teste D_te e reservado "
    "para a avaliacao final e imparcial do modelo treinado — deve ser utilizado "
    "apenas uma vez, apos a conclusao de todas as decisoes de projeto (GIRALDI, 2021, p. 109)."
)
pdf.para(
    "Em datasets de tamanho moderado, a simples divisao treino/teste e sujeita "
    "a alta variancia em funcao da particao aleatoria escolhida. Nesse caso, "
    "Giraldi (2021, p. 110) recomenda o protocolo de validacao cruzada k-fold "
    "como alternativa estatisticamente mais robusta, detalhada na Secao 5.1 "
    "deste documento."
)

pdf.subsection("3.5", "Codificacao da Variavel Alvo")
pdf.para(
    "A variavel alvo do dataset Cleveland possui originalmente cinco niveis de "
    "gravidade (0 a 4). Para o problema de classificacao binaria — que distingue "
    "pacientes saudaveis de pacientes com algum grau de doenca cardiaca — e "
    "necessaria a binarizacao: y=0 (saudavel) quando o valor original e 0, e "
    "y=1 (doente) para qualquer valor entre 1 e 4 (UDDIN et al., 2022). "
    "Essa transformacao simplifica o espaco de saida do classificador e e "
    "consistente com a aplicacao clinica de triagem, na qual o objetivo principal "
    "e distinguir casos que requerem investigacao adicional daqueles que nao requerem."
)

# ── 4. PROCESSO DE TREINAMENTO ────────────────────────────────────────────────
pdf.section("4", "Processo de Treinamento de Modelos")

pdf.subsection("4.1", "Fundamentos Matematicos do Treinamento")
pdf.para(
    "O processo de treinamento de um modelo de aprendizado de maquina e formalmente "
    "definido como a busca pelo vetor de parametros otimos z* que minimiza a "
    "funcao de perda sobre o conjunto de treinamento (GIRALDI, 2021, p. 97). "
    "Para algoritmos parametricos — como o SVM e a Regressao Logistica —, "
    "esse processo envolve a resolucao de um problema de otimizacao:"
)
pdf.para(
    "z* = argmin_{z} Err(z; D_tr)",
    indent=False, italic=True, align="C"
)
pdf.para(
    "A solucao desse problema pode ser obtida por metodos analiticos (solucao "
    "de forma fechada, quando existe) ou por metodos numericos iterativos, como "
    "o gradiente descendente estocastico (SGD). Giraldi (2021, p. 106) descreve "
    "o procedimento SGD por minibatch, no qual, a cada iteracao t, um subconjunto "
    "B do conjunto de treinamento e amostrado aleatoriamente e o gradiente da "
    "funcao de perda e calculado sobre esse subconjunto para atualizar os parametros:"
)
pdf.para(
    "z_{t+1} = z_t - eta * grad_z L(z_t; B)",
    indent=False, italic=True, align="C"
)
pdf.para(
    "onde eta e a taxa de aprendizado, que controla o tamanho do passo na "
    "direcao oposta ao gradiente. A escolha de eta e um hiperparametro critico: "
    "valores muito altos causam instabilidade e divergencia; valores muito "
    "baixos resultam em convergencia lenta e risco de ficar preso em minimos "
    "locais (GIRALDI, 2021, p. 107)."
)

pdf.subsection("4.2", "Overfitting, Underfitting e o Trade-off Vies-Variancia")
pdf.para(
    "O principal desafio do processo de treinamento e garantir que o modelo "
    "aprenda os padroes genuinos dos dados, sem memorizar os ruidos especificos "
    "do conjunto de treinamento. Giraldi (2021, p. 112) define overfitting como "
    "o fenomeno no qual os parametros calculados durante o treinamento adaptam-se "
    "a detalhes irrelevantes das amostras de treinamento, comprometendo a "
    "capacidade de generalizacao para novos dados. O fenomeno oposto, underfitting, "
    "ocorre quando o modelo e excessivamente simplista para capturar a estrutura "
    "real dos dados."
)
pdf.para(
    "Matematicamente, o erro esperado de um classificador sobre novos dados "
    "decompoe-se em tres componentes: vies, variancia e ruido irredutivel "
    "(GERON, 2019):"
)
pdf.para(
    "Erro(x) = Vies^2 + Variancia + epsilon",
    indent=False, italic=True, align="C"
)
pdf.para(
    "Modelos com alto vies (underfitting) ignoram estruturas relevantes dos dados; "
    "modelos com alta variancia (overfitting) ajustam-se excessivamente aos dados "
    "de treinamento. O objetivo do processo de treinamento e encontrar o ponto de "
    "equilibrio entre esses dois extremos — o chamado trade-off vies-variancia "
    "(GERON, 2019). Tecnicas de regularizacao — como o parametro C no SVM e o "
    "parametro K no KNN — controlam explicitamente esse trade-off."
)

pdf.subsection("4.3", "Regularizacao e Hiperparametros")
pdf.para(
    "A regularizacao e um conjunto de tecnicas que reduzem a complexidade efetiva "
    "do modelo, penalizando parametros de grande magnitude e favorecendo solucoes "
    "mais generalizaveis. Giraldi (2021, p. 97) inclui termos de regularizacao R "
    "na funcao de perda:"
)
pdf.para(
    "L(z; D) = (1/|D|) SOMA L(M(x_i; z) - d_i) + SOMA_{tau} varsigma_tau * R_tau(z; D)",
    indent=False, italic=True, align="C"
)
pdf.para(
    "onde varsigma_tau controla o peso da penalizacao sobre os parametros. "
    "Hiperparametros — como K no KNN, o parametro C e o tipo de kernel no SVM, "
    "ou o numero de dobras na validacao cruzada — nao sao aprendidos durante o "
    "treinamento, mas definidos a priori pelo projetista do sistema. A selecao "
    "sistematica de hiperparametros, por meio de busca em grade (grid search) "
    "ou validacao cruzada, e etapa indispensavel para maximizar a capacidade de "
    "generalizacao do modelo (GERON, 2019)."
)

# ── 5. ALGORITMOS DE CLASSIFICACAO ───────────────────────────────────────────
pdf.section("5", "Algoritmos de Classificacao")

pdf.subsection("5.1", "K-Nearest Neighbors (KNN)")
pdf.para(
    "O K-Nearest Neighbors e um algoritmo de aprendizado supervisionado "
    "nao-parametrico e nao-generativo, classificado como lazy learner (aprendiz "
    "pregucoso): nao constroi um modelo parametrico durante o treinamento, "
    "armazenando todo o conjunto de treinamento na memoria e adiando o calculo "
    "para o momento da predicao (GERON, 2019). Sua premissa fundamental e que "
    "amostras com atributos similares tendem a pertencer a mesma classe."
)
pdf.para(
    "O mecanismo de classificacao opera da seguinte forma: dado um novo ponto "
    "x_q a ser classificado, o algoritmo calcula a distancia entre x_q e todas "
    "as amostras do conjunto de treinamento; identifica os K vizinhos mais "
    "proximos N_K(x_q); e atribui a x_q a classe mais frequente entre esses K "
    "vizinhos — voto majoritario. Formalmente (GERON, 2019):"
)
pdf.para(
    "y'_q = argmax_c SOMA_{i pertence N_K(x_q)} Indicadora[y_i = c]",
    indent=False, italic=True, align="C"
)
pdf.para(
    "A medida de distancia mais comum e a distancia Euclidiana, definida entre "
    "dois pontos x e y em R^m por (GIRALDI, 2021, p. 97-98):"
)
pdf.para(
    "d_e(x, y) = raiz( SOMA_{j=1}^{m} (x_j - y_j)^2 )",
    indent=False, italic=True, align="C"
)
pdf.para(
    "A sensibilidade do KNN a escala dos atributos decorre diretamente dessa "
    "formula: atributos com magnitude numerica elevada dominam o calculo, "
    "tornando os demais irrelevantes. Essa e a razao pela qual a normalizacao "
    "Z-score e condicao obrigatoria antes da aplicacao do KNN (GERON, 2019)."
)
pdf.para(
    "O parametro K e o principal hiperparametro do KNN e controla o trade-off "
    "vies-variancia diretamente: valores pequenos de K (ex.: K=1) produzem "
    "fronteiras de decisao altamente irregulares, suscetiveis a overfitting; "
    "valores grandes de K suavizam as fronteiras, mas introduzem vies "
    "(underfitting). A determinacao empirica do K otimo via validacao cruzada "
    "e o metodo recomendado (GERON, 2019)."
)

pdf.subsection("5.2", "Support Vector Machine (SVM)")
pdf.para(
    "O Support Vector Machine e um classificador supervisionado parametrico que "
    "busca o hiperplano de maxima margem no espaco de features — o plano que "
    "separa as duas classes com a maior distancia possivel em relacao aos pontos "
    "mais proximos de cada classe (GIRALDI, 2021, p. 161). Dado um conjunto de "
    "treinamento S = {(x_i, y_i), x_i pertence R^n, y_i pertence {-1, +1}}, "
    "o SVM busca o vetor psi e o limiar b que satisfazem:"
)
pdf.para(
    "<x_i, psi> + b >= 1, para y_i = +1",
    indent=False, italic=True, align="C"
)
pdf.para(
    "<x_j, psi> + b <= -1, para y_j = -1",
    indent=False, italic=True, align="C"
)
pdf.para(
    "Os pontos de treinamento que se encontram exatamente sobre os planos de "
    "margem sao denominados vetores de suporte (support vectors) — sao os pontos "
    "mais proximos ao hiperplano otimo e determinam completamente a solucao "
    "(GIRALDI, 2021, p. 166). A distancia entre os planos de margem e a "
    "quantidade a ser maximizada, o que equivale a minimizar |psi|."
)
pdf.para(
    "Na pratica, dados reais raramente sao linearmente separaveis. O SVM com "
    "variaveis de folga (slack variables) xi_i — tambem chamado C-SVM — "
    "relaxa a separabilidade perfeita ao permitir que algumas amostras violem "
    "a margem, penalizando cada violacao com um custo C (GIRALDI, 2021, p. 169-170):"
)
pdf.para(
    "min |psi|^2 / 2 + C * SOMA xi_i",
    indent=False, italic=True, align="C"
)
pdf.para(
    "O parametro C e o principal hiperparametro do C-SVM: valores altos de C "
    "privilegiam a classificacao correta de todos os pontos de treinamento "
    "(baixo vies, alta variancia); valores baixos de C admitem mais erros de "
    "treinamento em troca de margens maiores e maior capacidade de generalizacao "
    "(GIRALDI, 2021, p. 170). A escolha C=0,1 adotada neste projeto reflete "
    "forte regularizacao, adequada para datasets medicos com ruido."
)
pdf.para(
    "Para dados nao linearmente separaveis no espaco original, o SVM emprega o "
    "truque do kernel (kernel trick): substitui o produto interno entre amostras "
    "por uma funcao kernel k(x_i, x_j) que computa implicitamente o produto "
    "interno em um espaco de features de alta dimensao (GIRALDI, 2021, p. 166-167). "
    "O kernel RBF (Radial Basis Function), dado por k(x_i, x_j) = exp(-gamma * "
    "|x_i - x_j|^2), e amplamente adotado por sua capacidade de modelar "
    "fronteiras de decisao nao lineares complexas sem especificar explicitamente "
    "o mapeamento para o espaco de alta dimensao (GERON, 2019)."
)

pdf.subsection("5.3", "Ensemble Learning")
pdf.para(
    "Metodos de ensemble combinam as previsoes de multiplos classificadores "
    "para obter desempenho superior ao de qualquer modelo individual. Mienye e "
    "Sun (2022) revisaram extensivamente essa familia de metodos, demonstrando "
    "que o ganho do ensemble e teoricamente garantido quando os erros dos "
    "classificadores base sao suficientemente descorrelacionados."
)
pdf.para(
    "O fundamento matematico do ensemble e a reducao da variancia por agregacao. "
    "Para M classificadores com erro medio epsilon e correlacao media rho entre "
    "seus erros, o erro esperado do ensemble e dado por (MIENYE; SUN, 2022):"
)
pdf.para(
    "E_ensemble = rho * epsilon + (1 - rho) * epsilon / M",
    indent=False, italic=True, align="C"
)
pdf.para(
    "Quando rho = 0 (erros completamente independentes), E_ensemble = epsilon/M, "
    "ou seja, o erro decresce linearmente com o numero de modelos. Na pratica, "
    "alguma correlacao sempre existe, mas o ganho e mensuravel desde que os "
    "classificadores base difiram em seus vieses de aprendizado "
    "(MIENYE; SUN, 2022)."
)
pdf.para(
    "As tres principais estrategias de ensemble sao (MIENYE; SUN, 2022): "
    "(i) Hard Voting — cada classificador emite um voto para a classe predita "
    "e a classe majoritaria vence; (ii) Soft Voting — cada classificador "
    "fornece um vetor de probabilidades por classe e as probabilidades sao "
    "agregadas (media simples ou ponderada); (iii) Stacking — as saidas dos "
    "classificadores base sao usadas como atributos de entrada para um "
    "meta-modelo (meta-learner) que aprende a combinar as previsoes de forma "
    "otima. O Stacking e o metodo mais expressivo dos tres, pois o meta-modelo "
    "pode aprender pesos assimetricos para diferentes regioes do espaco de "
    "features."
)
pdf.para(
    "A eficacia do ensemble depende criticamente da heterogeneidade dos "
    "classificadores base. Mienye e Sun (2022) documentam que a combinacao de "
    "algoritmos com hipoteses distintas — como o KNN (baseado em vizinhanca "
    "local) e o SVM (baseado em hiperplano global de maxima margem) — produz "
    "erros parcialmente descorrelacionados, criando as condicoes necessarias "
    "para ganho real na combinacao."
)

# ── 6. AVALIACAO DE MODELOS ───────────────────────────────────────────────────
pdf.section("6", "Avaliacao de Modelos")

pdf.subsection("6.1", "Validacao Cruzada Estratificada")
pdf.para(
    "A validacao cruzada k-fold e o protocolo estatisticamente mais robusto para "
    "avaliar a capacidade de generalizacao de classificadores em datasets de "
    "tamanho moderado (GIRALDI, 2021, p. 110). O conjunto D e particionado em K "
    "subconjuntos disjuntos; para cada particao i (i=1,...,K), um modelo e "
    "treinado sobre a uniao dos demais K-1 subconjuntos (D \\ D_i) e avaliado "
    "sobre D_i. A estimativa final da metrica de desempenho e a media das K "
    "avaliacoes independentes."
)
pdf.para(
    "A variante estratificada (StratifiedKFold) garante que cada dobra mantenha "
    "a mesma proporcao de classes do dataset completo — propriedade essencial "
    "em problemas com desbalanceamento de classes, comuns em aplicacoes medicas "
    "(GERON, 2019). Isso evita que uma dobra contenha amostras predominantemente "
    "de uma classe, o que produziria estimativas de desempenho enganosas."
)
pdf.para(
    "As principais vantagens da validacao cruzada em relacao a simples divisao "
    "treino/teste sao (GIRALDI, 2021, p. 110; GERON, 2019): (i) aproveitamento "
    "de todas as amostras disponsiveis tanto para treinamento quanto para "
    "avaliacao; (ii) reducao da variancia da estimativa de desempenho em relacao "
    "a uma unica particao aleatoria; (iii) menor sensibilidade a particoes "
    "desfavoraveis que poderiam produzir estimativas otimistas ou pessimistas."
)

pdf.subsection("6.2", "Metricas de Desempenho")
pdf.para(
    "A avaliacao de classificadores binarios e realizada por meio de um conjunto "
    "de metricas derivadas da matriz de confusao. Giraldi (2021, p. 111) define "
    "formalmente as quantidades basicas para problemas de N classes, que no caso "
    "binario se reduzem a quatro valores:"
)
pdf.para(
    "Verdadeiro Positivo (VP): numero de amostras doentes corretamente "
    "classificadas como doentes.",
    indent=True
)
pdf.para(
    "Falso Negativo (FN): numero de amostras doentes incorretamente "
    "classificadas como saudaveis — erro de maior custo clinico, pois "
    "representa doentes que nao receberiam tratamento.",
    indent=True
)
pdf.para(
    "Falso Positivo (FP): numero de amostras saudaveis incorretamente "
    "classificadas como doentes.",
    indent=True
)
pdf.para(
    "Verdadeiro Negativo (VN): numero de amostras saudaveis corretamente "
    "classificadas como saudaveis.",
    indent=True
)
pdf.para(
    "A partir dessas quantidades, Giraldi (2021, p. 112) define a acuracia "
    "como a fracao de classificacoes corretas sobre o total de amostras:"
)
pdf.para(
    "Acuracia = (VP + VN) / (VP + VN + FP + FN)",
    indent=False, italic=True, align="C"
)
pdf.para(
    "A acuracia e uma metrica intuitiva, porem pode ser enganosa em datasets "
    "desbalanceados. Por isso, metricas complementares sao essenciais "
    "(GERON, 2019):"
)
pdf.para(
    "Precisao = VP / (VP + FP): das predicoes positivas, qual fracao e "
    "realmente positiva (minimiza falsos alarmes).",
    indent=True
)
pdf.para(
    "Recall (Sensibilidade) = VP / (VP + FN): dos casos positivos reais, "
    "qual fracao foi detectada (minimiza casos nao detectados).",
    indent=True
)
pdf.para(
    "F1-Score = 2 * Precisao * Recall / (Precisao + Recall): media harmonica "
    "entre precisao e recall, util quando ambas as metricas sao igualmente "
    "importantes.",
    indent=True
)
pdf.para(
    "A curva ROC (Receiver Operating Characteristic) e a area sob ela "
    "(AUC-ROC) fornecem uma avaliacao do poder discriminativo do classificador "
    "independente do limiar de decisao. Um AUC-ROC de 1,0 indica discriminacao "
    "perfeita; 0,5 equivale a uma classificacao aleatoria (GERON, 2019). "
    "Em contexto clinico, onde o limiar de decisao pode ser ajustado conforme "
    "a sensibilidade desejada, o AUC-ROC e especialmente informativo e "
    "complementa a acuracia na avaliacao de classificadores medicos (UDDIN et al., 2022)."
)

# ── 7. CONSIDERACOES FINAIS ───────────────────────────────────────────────────
pdf.section("7", "Consideracoes Finais")
pdf.para(
    "Este documento consolidou a base teorica dos processos de tratamento de "
    "dados e treinamento de modelos em aprendizado de maquina supervisionado, "
    "com foco nos algoritmos e protocolos adotados no projeto de diagnostico "
    "de doencas cardiacas."
)
pdf.para(
    "Os conceitos fundamentais abordados formam uma cadeia logica: o processo "
    "de aprendizado e formalmente definido como a minimizacao de uma funcao de "
    "perda sobre dados empiricos (GIRALDI, 2021, p. 97); a qualidade desse "
    "processo depende criticamente do pre-processamento adequado dos dados — "
    "limpeza, normalizacao e particao correta —, sem o qual qualquer algoritmo "
    "produziria resultados comprometidos; o trade-off vies-variancia governa "
    "a selecao de hiperparametros em todos os algoritmos estudados, e sua "
    "compreensao e pre-requisito para a interpretacao correta dos resultados "
    "experimentais (GIRALDI, 2021, p. 112; GERON, 2019)."
)
pdf.para(
    "Os tres algoritmos abordados — KNN, SVM e Ensemble Learning — representam "
    "paradigmas distintos de classificacao: o KNN opera por similaridade local "
    "sem construir modelo parametrico; o SVM busca estrutura global de maxima "
    "margem no espaco de features transformado; os metodos de ensemble combinam "
    "multiplos modelos para reduzir a variancia agregada (MIENYE; SUN, 2022). "
    "A diversidade de hipoteses entre esses paradigmas e exatamente o que "
    "possibilita ganhos no ensemble: erros descorrelacionados se cancelam "
    "parcialmente na combinacao."
)
pdf.para(
    "A escolha do protocolo de avaliacao — validacao cruzada estratificada de "
    "10-dobras — e sustentada tanto pela limitacao do tamanho do dataset quanto "
    "pela necessidade de estimativas de desempenho com menor variancia "
    "(GIRALDI, 2021, p. 110). As metricas complementares — AUC-ROC, recall e "
    "F1-score — sao indispensaveis em diagnostico clinico, onde os custos de "
    "falso negativo (doente nao detectado) superam os de falso positivo "
    "(UDDIN et al., 2022)."
)

# ── REFERENCIAS ───────────────────────────────────────────────────────────────
pdf.section("", "Referencias")
pdf.ref_entry(
    "GERON, Aurelien. ",
    "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow: Concepts, "
    "Tools, and Techniques to Build Intelligent Systems. 2. ed. Sebastopol, CA: "
    "O'Reilly Media, 2019."
)
pdf.ref_entry(
    "GIRALDI, Gilson Antonio. ",
    "Machine Learning and Pattern Recognition. Lecture Notes — Graduate Course. "
    "Graduate Program in Nanobiosystems 2021. Petropolis, RJ: "
    "UFRJ-Fiocruz-INMETRO-LNCC, 2021."
)
pdf.ref_entry(
    "MIENYE, I. D.; SUN, Y. ",
    "A Survey of Ensemble Learning: Concepts, Algorithms, Applications, and Prospects. "
    "IEEE Access, v. 10, p. 99129-99149, 2022. "
    "DOI: 10.1109/ACCESS.2022.3207287."
)
pdf.ref_entry(
    "UDDIN, S.; HAQUE, I.; LU, H.; MONI, M. A.; GIDE, E. ",
    "Comparative performance analysis of K-nearest neighbour (KNN) algorithm "
    "and its different variants for disease prediction. "
    "Scientific Reports, v. 12, n. 6256, 2022. "
    "DOI: 10.1038/s41598-022-10358-x."
)

# ── SALVAR ────────────────────────────────────────────────────────────────────
out = BASE + "/artigos_relatorios/pdfs/Base_Teorica_FATEC.pdf"
pdf.output(out)
print(f"[OK] PDF gerado: {out}")
print(f"     Paginas: {pdf.page}")
