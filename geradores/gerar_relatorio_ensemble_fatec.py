"""
Relatorio Tecnico: Ensemble KNN+SVM para Diagnostico de Doencas Cardiacas
Formato FATEC 2022 — Arial 11pt, margens 2cm (esq/dir/baixo) e 2.5cm (topo),
espacamento 1.5, recuo de paragrafo 1.25cm.
"""
import json, os
from fpdf import FPDF

# ── Constantes FATEC 2022 ─────────────────────────────────────────────────────
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
SZ_CAP    = 10
LH        = 7.0
LH_SM     = 6.0
LH_TBL    = 5.5
INDENT    = 12.5

BASE  = "c:/Users/andre/Documents/TCC project"
GDIR  = BASE + "/artigos_relatorios/graficos_ensemble"

FONTS = {
    "":   "C:/Windows/Fonts/arial.ttf",
    "B":  "C:/Windows/Fonts/arialbd.ttf",
    "I":  "C:/Windows/Fonts/ariali.ttf",
    "BI": "C:/Windows/Fonts/arialbi.ttf",
}

with open(BASE + "/artigos_relatorios/ensemble_results.json", encoding="utf-8") as f:
    RES = json.load(f)


# ── Classe PDF ────────────────────────────────────────────────────────────────
class Relatorio(FPDF):
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
        s = ("B" if bold else "") + ("I" if italic else "")
        self.set_font(FONT, s, size)

    def para(self, txt, indent=True, align="J", bold=False, italic=False,
             size=SZ_BODY, lh=None, before=0, after=0):
        if before: self.ln(before)
        lh = lh or (LH if size >= SZ_BODY else LH_SM)
        self._font(bold, italic, size)
        x = MARGIN_L + (INDENT if indent else 0)
        w = CONTENT_W - (INDENT if indent else 0)
        self.set_x(x)
        self.multi_cell(w, lh, txt, align=align)
        if after: self.ln(after)

    def center(self, txt, bold=False, italic=False, size=SZ_BODY, lh=None):
        lh = lh or (LH if size >= SZ_BODY else LH_SM)
        self._font(bold, italic, size)
        self.set_x(MARGIN_L)
        self.multi_cell(CONTENT_W, lh, txt, align="C")

    def section(self, num, title, level=1):
        self.ln(4)
        self._font(bold=True, size=SZ_BODY)
        label = f"{num} {title}".upper() if level == 1 else f"{num} {title}"
        self.set_x(MARGIN_L)
        self.multi_cell(CONTENT_W, LH, label, align="L")
        self.ln(1)

    def subsection(self, num, title):
        self.ln(2)
        self._font(bold=True, size=SZ_BODY)
        self.set_x(MARGIN_L)
        self.multi_cell(CONTENT_W, LH, f"{num} {title}", align="L")
        self.ln(1)

    def source_line(self, txt="Fonte: Dados do experimento."):
        self._font(italic=True, size=SZ_CAP)
        self.set_x(MARGIN_L)
        self.multi_cell(CONTENT_W, LH_SM, txt, align="L")
        self.ln(3)

    def table(self, headers, rows, col_widths, h_aligns=None, r_aligns=None):
        h_aligns = h_aligns or ["C"] * len(headers)
        r_aligns = r_aligns or [["L"] + ["C"] * (len(headers) - 1)] * len(rows)
        self._font(bold=True, size=SZ_SMALL)
        self.set_x(MARGIN_L)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], LH_TBL + 2, h, border=1, align=h_aligns[i])
        self.ln()
        self._font(size=SZ_SMALL)
        for ri, row in enumerate(rows):
            self.set_x(MARGIN_L)
            aligns = r_aligns[ri] if isinstance(r_aligns[0], list) else r_aligns
            for i, cell in enumerate(row):
                self.cell(col_widths[i], LH_TBL + 2, str(cell), border=1, align=aligns[i])
            self.ln()
        self.ln(2)

    def fig_page(self, fname, fig_num, legenda):
        """Insere uma figura em pagina propria: titulo acima, fonte abaixo."""
        self.add_page()
        path = GDIR + "/" + fname
        # Titulo ACIMA (norma FATEC)
        self._font(bold=True, size=SZ_CAP)
        prefix = fig_num + " - "
        wp = self.get_string_width(prefix)
        self.set_x(MARGIN_L)
        self.cell(wp, LH_SM, prefix)
        self._font(bold=False, size=SZ_CAP)
        self.multi_cell(CONTENT_W - wp, LH_SM, legenda, align="J")
        self.ln(2)
        # Imagem
        if os.path.exists(path):
            self.image(path, x=MARGIN_L, w=CONTENT_W)
        else:
            self._font(italic=True, size=SZ_SMALL)
            self.set_x(MARGIN_L)
            self.cell(CONTENT_W, LH, f"[Arquivo nao encontrado: {fname}]", align="C")
        self.ln(2)
        # Fonte ABAIXO
        self._font(italic=True, size=SZ_CAP)
        self.set_x(MARGIN_L)
        self.cell(CONTENT_W, LH_SM,
                  "Fonte: Gerado pelos autores com base nos dados experimentais.", align="L")

    def ref_entry(self, bold_part, rest):
        self._font(bold=True, size=SZ_BODY)
        wb = self.get_string_width(bold_part)
        self.set_x(MARGIN_L)
        self.cell(wb, LH, bold_part)
        self._font(size=SZ_BODY)
        self.multi_cell(CONTENT_W - wb, LH, rest, align="J")
        self.ln(1)


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTRUCAO DO RELATORIO
# ═══════════════════════════════════════════════════════════════════════════════
pdf = Relatorio()
pdf.add_page()

# ── TITULO ────────────────────────────────────────────────────────────────────
pdf.center(
    "ENSEMBLE LEARNING APLICADO AO DIAGNOSTICO DE DOENCAS CARDIACAS: "
    "COMBINACAO DE K-NEAREST NEIGHBORS E SUPPORT VECTOR MACHINE",
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
    "Este relatorio apresenta os resultados da aplicacao de metodos de ensemble "
    "learning para o diagnostico binario de doencas cardiacas, utilizando o Cleveland "
    "Heart Disease Dataset (UCI, 297 registros). Foram combinados dois classificadores "
    "otimizados — K-Nearest Neighbors com K=29 e Support Vector Machine com C=0,1 e "
    "kernel RBF — por meio de tres estrategias de ensemble: Hard Voting, Soft Voting "
    "(simples e ponderado) e Stacking com meta-learner de Regressao Logistica. "
    "Os resultados demonstram que Hard Voting e Soft Voting atingem acuracia de 88,33% "
    "no conjunto de teste, superando os modelos base (86,67% cada), enquanto o Stacking "
    "obteve AUC-ROC de 95,20% — o maior entre todos os metodos. A taxa de concordancia "
    "entre KNN e SVM foi de 96,67%, confirmando a complementaridade limitada mas "
    "suficiente para ganho na votacao. A validacao cruzada estratificada de 10-dobras "
    "registrou acuracias medias entre 82,49% e 83,51%, com o SVM individual apresentando "
    "o melhor desempenho medio.",
    indent=False
)
pdf.para(
    "Palavras-chave: Ensemble Learning; Hard Voting; Soft Voting; Stacking; "
    "KNN; SVM; Diagnostico Cardiaco; Aprendizado de Maquina.",
    indent=False, italic=True
)
pdf.ln(4)

# ── 1. INTRODUCAO ─────────────────────────────────────────────────────────────
pdf.section("1", "Introducao")
pdf.para(
    "O diagnostico precoce de doencas cardiovasculares e um desafio central da saude "
    "publica global. O aprendizado de maquina oferece ferramentas capazes de identificar "
    "padroes preditivos em dados clinicos de rotina, reduzindo a dependencia de exames "
    "invasivos de custo elevado. Contudo, nenhum algoritmo isolado e universalmente "
    "superior: cada metodo carrega hipoteses diferentes sobre a estrutura dos dados "
    "(MIENYE; SUN, 2022)."
)
pdf.para(
    "Algoritmos de ensemble combinam as previsoes de multiplos classificadores para "
    "obter maior acuracia e estabilidade do que qualquer modelo individual — desde que "
    "os erros dos classificadores base sejam suficientemente independentes "
    "(MIENYE; SUN, 2022). Essa abordagem e especialmente promissora quando se combina "
    "algoritmos com vieses distintos: o KNN, que captura padroes locais por similaridade, "
    "e o SVM, que busca um hiperplano global de maxima margem."
)
pdf.para(
    "Este relatorio documenta o desenvolvimento, implementacao e avaliacao completa de "
    "tres estrategias de ensemble — Hard Voting, Soft Voting e Stacking — aplicadas ao "
    "Cleveland Heart Disease Dataset. Os modelos base utilizados sao o KNN com K=29 e o "
    "SVM com C=0,1 e kernel RBF, ambos previamente otimizados em estudos anteriores "
    "deste projeto. O objetivo e verificar se a combinacao desses dois classificadores "
    "produz ganho mensuravel de desempenho e, em caso afirmativo, identificar qual "
    "estrategia de ensemble e mais eficaz."
)

# ── 2. CONCEITOS SOBRE IA ─────────────────────────────────────────────────────
pdf.section("2", "Conceitos sobre Inteligencia Artificial")

pdf.subsection("2.1", "Aprendizado de Maquina e Classificacao Supervisionada")
pdf.para(
    "O aprendizado de maquina subdivide-se em quatro categorias principais: "
    "supervisionado, nao supervisionado, semi-supervisionado e por reforco "
    "(GIRALDI, 2021, p. 99). Na classificacao supervisionada, um conjunto de amostras "
    "rotuladas e fornecido ao algoritmo, que aprende um mapeamento das caracteristicas "
    "dos exemplos para suas respectivas classes (GIRALDI, 2021, p. 99). O diagnostico "
    "de doencas cardiacas e tipicamente enquadrado como classificacao binaria: cada "
    "paciente e classificado como saudavel (Classe 0) ou doente (Classe 1)."
)
pdf.para(
    "O poder preditivo de um classificador depende tanto da qualidade dos dados quanto "
    "da adequacao do algoritmo a estrutura do problema. Mienye e Sun (2022) revisaram "
    "extensivamente os metodos de ensemble, documentando que combinacoes de algoritmos "
    "heterogeneos — que diferem em seu vies de aprendizado — superam consistentemente "
    "classificadores individuais em diversas tarefas de classificacao medica."
)

pdf.subsection("2.2", "Trade-off Vies-Variancia e Generalizacao")
pdf.para(
    "Todo classificador enfrenta o dilema entre vies e variancia. Modelos com alto "
    "vies (underfitting) falham ao capturar padroes relevantes dos dados; modelos com "
    "alta variancia (overfitting) memorizam o conjunto de treinamento e generalizam mal "
    "para novos casos — adaptando-se a detalhes irrelevantes que comprometem a "
    "generalizacao (GIRALDI, 2021, p. 112). O K otimo no KNN e o parametro C no SVM "
    "controlam esse dilema em seus respectivos espacos de hipoteses."
)
pdf.para(
    "Ensemble methods mitigam o overfitting ao combinar multiplos modelos: o erro "
    "medio de um ensemble e inferior ao erro esperado de um unico classificador quando "
    "os erros individuais sao descorrelacionados. Formalmente, para um ensemble de M "
    "classificadores com erro medio epsilon e correlacao media rho entre erros, o erro "
    "do ensemble e: E_ens = rho * epsilon + (1 - rho) * epsilon / M "
    "(MIENYE; SUN, 2022). Quanto menor rho, maior o beneficio do ensemble."
)

pdf.subsection("2.3", "Estrategias de Ensemble")
pdf.para(
    "As principais estrategias de ensemble para classificacao sao (MIENYE; SUN, 2022):"
)
pdf.para(
    "(i) Hard Voting: cada classificador base emite um voto para a classe predita; a "
    "classe majoritaria e a previsao final. Simples e robusto quando os modelos base "
    "tem desempenho similar.",
    indent=True
)
pdf.para(
    "(ii) Soft Voting: cada classificador fornece um vetor de probabilidades para cada "
    "classe; as probabilidades sao agregadas (media simples ou ponderada) e a classe "
    "com maior probabilidade media e selecionada. Aproveita mais informacao do que o "
    "voto duro.",
    indent=True
)
pdf.para(
    "(iii) Stacking (empilhamento): as previsoes dos classificadores base sao usadas "
    "como features de entrada para um meta-modelo (meta-learner), que aprende a "
    "combinar as saidas de forma otima. Permite que o meta-modelo pondere "
    "adaptativamente cada classificador base com base em seu desempenho diferencial "
    "(MIENYE; SUN, 2022).",
    indent=True
)

pdf.subsection("2.4", "Validacao Cruzada Estratificada")
pdf.para(
    "A validacao cruzada k-fold estratificada e o protocolo padrao para avaliacao "
    "honesta de classificadores em conjuntos de dados de tamanho moderado "
    "(GIRALDI, 2021, p. 108; GERON, 2019). O conjunto D e particionado em k dobras "
    "mantendo a proporcao original de classes em cada particao. Para cada dobra i, "
    "o modelo e treinado em D \\ D_i e avaliado em D_i; a metrica final e a media das "
    "k avaliacoes. O AUC-ROC (Area Under the Receiver Operating Characteristic Curve) "
    "complementa a acuracia ao medir a capacidade discriminativa do modelo "
    "independente do limiar de decisao, sendo especialmente relevante em diagnostico "
    "clinico onde os custos de falso positivo e falso negativo sao assimetricos."
)

# ── 3. MATERIAIS E METODOS ────────────────────────────────────────────────────
pdf.section("3", "Materiais e Metodos")

pdf.subsection("3.1", "Base de Dados")
pdf.para(
    "Utilizamos o Cleveland Heart Disease Dataset, disponibilizado pelo UCI Machine "
    "Learning Repository e amplamente adotado como benchmark em estudos de diagnostico "
    "cardiaco por aprendizado de maquina (UDDIN et al., 2022). O dataset original "
    "contem 303 registros e 13 atributos clinicos. Apos remocao de 6 registros com "
    "valores ausentes, restaram 297 instancias validas: 160 saudaveis (Classe 0) e "
    "137 com algum grau de doenca cardiaca (Classe 1), configurando um ligeiro "
    "desbalanceamento de classes (53,9% vs. 46,1%)."
)

# Tabela 1 - Dataset
pdf.ln(1)
pdf._font(bold=True, size=SZ_SMALL)
pdf.set_x(MARGIN_L)
pdf.cell(CONTENT_W, LH_SM, "Tabela 1 - Configuracao do dataset e particao dos dados", align="C")
pdf.ln(1)
pdf.table(
    ["Parametro", "Valor"],
    [
        ["Total de registros originais",  "303"],
        ["Registros removidos (NaN)",     "6"],
        ["Registros validos",             "297"],
        ["Classe 0 - Saudavel",           "160 (53,87%)"],
        ["Classe 1 - Doente",             "137 (46,13%)"],
        ["Conjunto de treino (80%)",      "237 registros"],
        ["Conjunto de teste (20%)",       "60 registros"],
        ["Estratificacao",                "Sim (StratifiedKFold)"],
    ],
    col_widths=[120, 45],
    h_aligns=["C", "C"],
    r_aligns=[["L", "C"]] * 8
)
pdf.source_line("Fonte: UCI Machine Learning Repository; dados do experimento.")

pdf.subsection("3.2", "Pre-processamento")
pdf.para(
    "O pipeline de pre-processamento seguiu tres etapas: (i) Remocao de valores "
    "ausentes (NaN), preservando 297 de 303 registros; (ii) Binarizacao da variavel "
    "alvo — a variavel original com cinco niveis de gravidade (0-4) foi convertida "
    "para classificacao binaria: y=0 (saudavel) e y=1 (doente); (iii) Normalizacao "
    "Z-score (StandardScaler) aplicada aos 13 atributos clinicos, com parametros "
    "calculados exclusivamente sobre o conjunto de treinamento e aplicados ao conjunto "
    "de teste, evitando data leakage."
)

pdf.subsection("3.3", "Classificadores Base")
pdf.para(
    "Os dois classificadores base foram selecionados com base em suas hipoteses "
    "complementares sobre os dados:"
)
pdf.para(
    "KNN com K=29: classificador lazy nao-parametrico baseado em similaridade local. "
    "Classifica uma nova amostra pela classe majoritaria de seus 29 vizinhos mais "
    "proximos na distancia Euclidiana. O valor K=29 foi determinado por analise "
    "parametrica sistematica em estudo anterior deste projeto, obtendo acuracia de "
    "86,67% e AUC-ROC de 90,20% em validacao cruzada (GERON, 2019).",
    indent=True
)
pdf.para(
    "SVM com C=0,1 e kernel RBF: classificador eager parametrico que busca o "
    "hiperplano de maxima margem no espaco de features transformado pelo kernel "
    "radial basis function (RBF). O parametro C=0,1 impoe forte regularizacao, "
    "favorecendo maior margem em detrimento de classificacoes erradas no treino "
    "— comportamento adequado para datasets medicos com ruido.",
    indent=True
)

pdf.subsection("3.4", "Estrategias de Ensemble Implementadas")
pdf.para(
    "Foram implementadas tres estrategias de combinacao dos classificadores base, "
    "totalizando cinco variantes avaliadas:"
)

pdf.ln(1)
pdf._font(bold=True, size=SZ_SMALL)
pdf.set_x(MARGIN_L)
pdf.cell(CONTENT_W, LH_SM, "Tabela 2 - Estrategias de ensemble implementadas", align="C")
pdf.ln(1)
pdf.table(
    ["Metodo", "Descricao", "Pesos"],
    [
        ["Hard Voting",
         "Votacao por maioria: classe vencedora se soma de votos >= 1",
         "KNN=0.5, SVM=0.5"],
        ["Soft Voting (simples)",
         "Media aritmetica das probabilidades dos dois modelos",
         "KNN=0.5, SVM=0.5"],
        ["Soft Voting (ponderado)",
         "Media ponderada: peso maior ao SVM (melhor CV)",
         "KNN=0.45, SVM=0.55"],
        ["Stacking",
         "Regressao Logistica treina nos outputs (probabilidades) dos modelos base",
         "Aprendidos"],
    ],
    col_widths=[45, 98, 27],
    h_aligns=["C", "C", "C"],
    r_aligns=[["L", "L", "C"]] * 4
)
pdf.source_line("Fonte: Dados do experimento.")

pdf.subsection("3.5", "Protocolo de Avaliacao")
pdf.para(
    "Cada metodo foi avaliado por dois protocolos complementares: (i) avaliacao no "
    "conjunto de teste hold-out (20% dos dados, n=60), reportando acuracia, "
    "AUC-ROC, precision, recall e F1-score; (ii) validacao cruzada estratificada "
    "de 10-dobras sobre o conjunto completo (n=297), reportando media e desvio "
    "padrao da acuracia entre dobras. Para o Stacking, o meta-modelo foi treinado "
    "e avaliado dentro de cada dobra para evitar vazamento de informacao."
)

# ── 4. ESTUDO DE CASO: RESULTADOS ─────────────────────────────────────────────
pdf.section("4", "Resultados e Discussao")

pdf.subsection("4.1", "Acuracia no Conjunto de Teste")
pdf.para(
    "A Tabela 3 apresenta os resultados de acuracia no conjunto de teste (n=60) "
    "para todos os metodos avaliados."
)

pdf.ln(1)
pdf._font(bold=True, size=SZ_SMALL)
pdf.set_x(MARGIN_L)
pdf.cell(CONTENT_W, LH_SM, "Tabela 3 - Acuracia no conjunto de teste (n=60)", align="C")
pdf.ln(1)
acc = RES["acuracia_teste"]
pdf.table(
    ["Metodo", "Acuracia", "Acertos/60", "Desempenho"],
    [
        ["KNN (K=29)",            f"{acc['KNN_K29']:.4f}",          "52/60", "Modelo base"],
        ["SVM (C=0.1, RBF)",      f"{acc['SVM_C01_RBF']:.4f}",      "52/60", "Modelo base"],
        ["Hard Voting",           f"{acc['Hard_Voting']:.4f}",       "53/60", "Ensemble (+1)"],
        ["Soft Voting",           f"{acc['Soft_Voting']:.4f}",       "53/60", "Ensemble (+1)"],
        ["Soft Voting Ponderado", f"{acc['Soft_Voting_Pond']:.4f}",  "53/60", "Ensemble (+1)"],
        ["Stacking",              f"{acc['Stacking']:.4f}",          "52/60", "Igual aos base"],
    ],
    col_widths=[65, 30, 30, 40],
    h_aligns=["C"] * 4,
    r_aligns=[["L", "C", "C", "L"]] * 6
)
pdf.source_line("Fonte: Dados do experimento.")

pdf.para(
    "Os resultados revelam que Hard Voting e ambas as variantes de Soft Voting "
    "superaram os modelos base em 1,67 pontos percentuais (88,33% vs. 86,67%), "
    "acertando um caso adicional no conjunto de teste. O Stacking manteve-se igual "
    "aos modelos base (86,67%), sugerindo que a Regressao Logistica nao encontrou "
    "combinacao linear das probabilidades superior a simples media. A taxa de "
    "concordancia entre KNN e SVM foi de 96,67% (58 de 60 amostras), o que limita "
    "o potencial maximo do ensemble — modelos com erros correlacionados tem ganho "
    "teorico reduzido."
)

pdf.subsection("4.2", "AUC-ROC")
auc = RES["auc_roc"]
pdf.para(
    "A Tabela 4 apresenta o AUC-ROC para os metodos onde probabilidades estao "
    "disponiveis. O AUC-ROC mede a capacidade discriminativa global do modelo "
    "independente do limiar de decisao, sendo especialmente relevante em contexto "
    "clinico onde o medico pode ajustar o ponto de corte conforme a sensibilidade "
    "desejada (GERON, 2019)."
)
pdf.ln(1)
pdf._font(bold=True, size=SZ_SMALL)
pdf.set_x(MARGIN_L)
pdf.cell(CONTENT_W, LH_SM, "Tabela 4 - AUC-ROC no conjunto de teste (n=60)", align="C")
pdf.ln(1)
pdf.table(
    ["Metodo", "AUC-ROC", "Interpretacao"],
    [
        ["KNN (K=29)",            f"{auc['KNN_K29']:.4f}",          "Excelente discriminacao"],
        ["SVM (C=0.1, RBF)",      f"{auc['SVM_C01_RBF']:.4f}",      "Excelente discriminacao"],
        ["Soft Voting",           f"{auc['Soft_Voting']:.4f}",       "Excelente (+0.0011)"],
        ["Soft Voting Ponderado", f"{auc['Soft_Voting_Pond']:.4f}",  "Excelente (+0.0022)"],
        ["Stacking",              f"{auc['Stacking']:.4f}",          "Melhor AUC (+0.0033)"],
    ],
    col_widths=[65, 35, 65],
    h_aligns=["C"] * 3,
    r_aligns=[["L", "C", "L"]] * 5
)
pdf.source_line("Fonte: Dados do experimento. Ganho relativo ao KNN base.")

pdf.para(
    "O Stacking obteve o maior AUC-ROC (95,20%), seguido pelo Soft Voting Ponderado "
    "(95,09%) e Soft Voting simples (94,98%). Os modelos base registraram AUC-ROC "
    "proximos: KNN com 94,81% e SVM com 94,87%. O ganho cumulativo do ensemble de "
    "votacao sobre o KNN base foi de +0,28 pontos percentuais em AUC-ROC. Embora "
    "numericamente pequeno, em contexto clinico esse ganho pode ter implicacao "
    "pratica ao deslocar o ponto de operacao da curva ROC."
)

pdf.subsection("4.3", "Validacao Cruzada Estratificada (10-Dobras)")
cv = RES["cv_10fold"]
pdf.para(
    "A validacao cruzada de 10-dobras fornece estimativa mais confiavel do desempenho "
    "esperado em dados novos, reduzindo o viés da particao aleatoria unica "
    "(GIRALDI, 2021, p. 108). A Tabela 5 consolida os resultados."
)

pdf.ln(1)
pdf._font(bold=True, size=SZ_SMALL)
pdf.set_x(MARGIN_L)
pdf.cell(CONTENT_W, LH_SM, "Tabela 5 - Validacao cruzada estratificada (10-dobras, n=297)", align="C")
pdf.ln(1)
pdf.table(
    ["Metodo", "Acuracia Media", "Desvio Padrao", "Min Fold", "Max Fold"],
    [
        ["KNN (K=29)",            f"{cv['KNN']['media']:.4f}",  f"+-{cv['KNN']['std']:.4f}",
         f"{min(cv['KNN']['scores']):.4f}",  f"{max(cv['KNN']['scores']):.4f}"],
        ["SVM (C=0.1, RBF)",      f"{cv['SVM']['media']:.4f}",  f"+-{cv['SVM']['std']:.4f}",
         f"{min(cv['SVM']['scores']):.4f}",  f"{max(cv['SVM']['scores']):.4f}"],
        ["Hard Voting",           f"{cv['Hard']['media']:.4f}", f"+-{cv['Hard']['std']:.4f}",
         f"{min(cv['Hard']['scores']):.4f}", f"{max(cv['Hard']['scores']):.4f}"],
        ["Soft Voting",           f"{cv['Soft']['media']:.4f}", f"+-{cv['Soft']['std']:.4f}",
         f"{min(cv['Soft']['scores']):.4f}", f"{max(cv['Soft']['scores']):.4f}"],
        ["Soft Voting Ponderado", f"{cv['Pond']['media']:.4f}", f"+-{cv['Pond']['std']:.4f}",
         f"{min(cv['Pond']['scores']):.4f}", f"{max(cv['Pond']['scores']):.4f}"],
        ["Stacking",              f"{cv['Stack']['media']:.4f}",f"+-{cv['Stack']['std']:.4f}",
         f"{min(cv['Stack']['scores']):.4f}",f"{max(cv['Stack']['scores']):.4f}"],
    ],
    col_widths=[55, 35, 30, 25, 25],
    h_aligns=["C"] * 5,
    r_aligns=[["L", "C", "C", "C", "C"]] * 6
)
pdf.source_line("Fonte: Dados do experimento.")

pdf.para(
    "Na validacao cruzada, o SVM individual apresentou a maior acuracia media "
    f"({cv['SVM']['media']:.4f}), seguido pelo KNN ({cv['KNN']['media']:.4f}). "
    "Interessantemente, os metodos de ensemble nao superaram os modelos base na "
    "validacao cruzada — o melhor ensemble foi o Soft Voting simples com "
    f"{cv['Soft']['media']:.4f}. Esse fenomeno ocorre porque, com alta concordancia "
    "entre KNN e SVM (96,67%), o ensemble raramente produz previsao diferente dos "
    "modelos individuais: a maioria das amostras ja era classificada corretamente "
    "por ambos os modelos, deixando pouco espaco para ganho na combinacao."
)

pdf.subsection("4.4", "Matrizes de Confusao e Metricas Detalhadas")
pdf.para(
    "A Tabela 6 detalha as matrizes de confusao dos quatro principais metodos "
    "no conjunto de teste (n=60: 32 saudaveis + 28 doentes). Os valores sao: "
    "VP (Verdadeiros Positivos), FN (Falsos Negativos), FP (Falsos Positivos), "
    "VN (Verdadeiros Negativos)."
)

pdf.ln(1)
pdf._font(bold=True, size=SZ_SMALL)
pdf.set_x(MARGIN_L)
pdf.cell(CONTENT_W, LH_SM, "Tabela 6 - Matrizes de confusao (conjunto de teste, n=60)", align="C")
pdf.ln(1)
cm = RES["matrizes_confusao"]

def mk(mat):
    tn, fp = mat[0][0], mat[0][1]
    fn, tp = mat[1][0], mat[1][1]
    prec = tp/(tp+fp) if (tp+fp) > 0 else 0
    rec  = tp/(tp+fn) if (tp+fn) > 0 else 0
    f1   = 2*prec*rec/(prec+rec) if (prec+rec) > 0 else 0
    return tn, fp, fn, tp, prec, rec, f1

r_knn = mk(cm["KNN"])
r_svm = mk(cm["SVM"])
r_wgt = mk(cm["Soft_Voting_Pond"])
r_stk = mk(cm["Stacking"])

pdf.table(
    ["Metodo", "VN", "FP", "FN", "VP", "Precision", "Recall", "F1-Score"],
    [
        ["KNN (K=29)",       str(r_knn[0]), str(r_knn[1]), str(r_knn[2]), str(r_knn[3]),
         f"{r_knn[4]:.4f}", f"{r_knn[5]:.4f}", f"{r_knn[6]:.4f}"],
        ["SVM (C=0.1, RBF)", str(r_svm[0]), str(r_svm[1]), str(r_svm[2]), str(r_svm[3]),
         f"{r_svm[4]:.4f}", f"{r_svm[5]:.4f}", f"{r_svm[6]:.4f}"],
        ["Soft Voting Pond.", str(r_wgt[0]), str(r_wgt[1]), str(r_wgt[2]), str(r_wgt[3]),
         f"{r_wgt[4]:.4f}", f"{r_wgt[5]:.4f}", f"{r_wgt[6]:.4f}"],
        ["Stacking",         str(r_stk[0]), str(r_stk[1]), str(r_stk[2]), str(r_stk[3]),
         f"{r_stk[4]:.4f}", f"{r_stk[5]:.4f}", f"{r_stk[6]:.4f}"],
    ],
    col_widths=[45, 14, 14, 14, 14, 25, 25, 19],
    h_aligns=["C"] * 8,
    r_aligns=[["L"] + ["C"] * 7] * 4
)
pdf.source_line("Fonte: Dados do experimento. VP=Verdadeiro Positivo (doente correto); "
                "FN=Falso Negativo (doente classificado como saudavel).")

pdf.para(
    "O Soft Voting Ponderado e o Stacking reduziram os Falsos Negativos (doentes "
    "classificados como saudaveis) de 6 para 5, em relacao aos modelos base. Em "
    "diagnostico clinico, reduzir FN e prioritario pois representa doentes que "
    "deixariam de receber tratamento. O Stacking, porem, introduziu um Falso Positivo "
    "adicional (FP=3 vs. FP=2), resultando na mesma acuracia final dos modelos base. "
    "Os coeficientes do meta-learner de Stacking foram KNN=2,16 e SVM=3,23, "
    "indicando que o meta-modelo aprendeu a dar peso maior ao SVM — coerente com "
    "seu melhor desempenho medio na validacao cruzada."
)

# ── FIGURAS ───────────────────────────────────────────────────────────────────
figuras = [
    ("g1_acuracia_teste.png", "Figura 1",
     "Acuracia no conjunto de teste por metodo. "
     "Vermelho = modelos base individuais; Verde/Azul = voting ensemble; "
     "Roxo = stacking. Hard Voting, Soft Voting e Soft Voting Ponderado "
     "atingem 88,33%, superando os modelos base em 1,67%."),
    ("g2_auc_roc.png", "Figura 2",
     "AUC-ROC por metodo no conjunto de teste. O Stacking obteve o maior "
     "AUC-ROC (95,20%), seguido pelo Soft Voting Ponderado (95,09%). "
     "Todos os metodos apresentam excelente capacidade discriminativa (>94%)."),
    ("g3_cv_boxplot.png", "Figura 3",
     "Distribuicao da acuracia na validacao cruzada estratificada de 10-dobras "
     "(n=297). Media e desvio padrao indicados acima de cada diagrama. "
     "O SVM individual apresenta a maior media (83,51%); os ensembles ficam "
     "proximos dos modelos base, evidenciando alta concordancia entre KNN e SVM."),
    ("g4_confusao.png", "Figura 4",
     "Matrizes de confusao dos quatro metodos principais no conjunto de teste. "
     "Diagonal principal = acertos; fora da diagonal = erros. "
     "Soft Voting Ponderado e Stacking reduzem Falsos Negativos de 6 para 5."),
    ("g5_prec_rec_f1.png", "Figura 5",
     "Precision, Recall e F1-Score para a classe positiva (Doente) por metodo. "
     "Soft Voting Ponderado apresenta o maior Recall (82,14%), reduzindo o risco "
     "de doentes nao detectados em relacao ao KNN e SVM individuais (78,57%)."),
    ("g6_comparativo_geral.png", "Figura 6",
     "Comparativo geral: acuracia no conjunto de teste, AUC-ROC e acuracia "
     "na validacao cruzada de 10-dobras, por metodo. O ensemble apresenta ganho "
     "consistente em acuracia de teste e AUC-ROC, mas nao na validacao cruzada — "
     "reflexo da alta concordancia entre os modelos base."),
]

for fname, fig_num, legenda in figuras:
    pdf.fig_page(fname, fig_num, legenda)

# retorno ao fluxo normal
pdf.add_page()

pdf.subsection("4.5", "Analise do Coeficiente de Meta-Learner")
meta = RES["meta_coeficientes"]
pdf.para(
    "No Stacking, a Regressao Logistica aprende os coeficientes que melhor combinam "
    "as probabilidades dos dois classificadores base para prever a classe real. "
    f"Os coeficientes obtidos foram: KNN = {meta['KNN']:.4f} e SVM = {meta['SVM']:.4f}. "
    "O coeficiente do SVM e aproximadamente 1,5x maior que o do KNN, indicando que "
    "o meta-modelo atribui maior confiabilidade as probabilidades do SVM. Esse resultado "
    "e coerente com o desempenho ligeiramente superior do SVM na validacao cruzada "
    f"({cv['SVM']['media']:.4f} vs. {cv['KNN']['media']:.4f} do KNN)."
)
pdf.para(
    "Ambos os coeficientes sao positivos e relativamente altos (>2), refletindo que "
    "ambos os modelos contribuem de forma significativa para a previsao final. A "
    "magnitude elevada e parcialmente decorrente da alta correlacao entre as "
    "probabilidades dos dois modelos (concordancia de 96,67%), que comprime a variacao "
    "no espaco de features do meta-modelo."
)

pdf.subsection("4.6", "Comparacao com a Literatura")
pdf.para(
    "A Tabela 7 contextualiza os resultados obtidos em relacao a literatura "
    "disponivel sobre KNN e ensemble em diagnostico cardiaco."
)

pdf.ln(1)
pdf._font(bold=True, size=SZ_SMALL)
pdf.set_x(MARGIN_L)
pdf.cell(CONTENT_W, LH_SM, "Tabela 7 - Comparacao com resultados da literatura", align="C")
pdf.ln(1)
pdf.table(
    ["Estudo / Metodo", "Dataset", "Acuracia", "Referencia"],
    [
        ["Este trabalho - Hard/Soft Voting",    "Cleveland UCI", "88,33%",  "—"],
        ["Este trabalho - KNN (K=29)",          "Cleveland UCI", "86,67%",  "—"],
        ["Este trabalho - SVM (C=0.1)",         "Cleveland UCI", "86,67%",  "—"],
        ["Uddin et al. - KNN classico",         "8 datasets UCI","64-84%",  "UDDIN et al., 2022"],
        ["Uddin et al. - KNN ensemble",         "8 datasets UCI","82,34%",  "UDDIN et al., 2022"],
        ["Uddin et al. - Hassanat KNN (melhor)","8 datasets UCI","83,62%",  "UDDIN et al., 2022"],
        ["Mienye; Sun - ensemble (max)",        "UCI variados",  "ate 95%", "MIENYE; SUN, 2022"],
    ],
    col_widths=[75, 35, 25, 30],
    h_aligns=["C"] * 4,
    r_aligns=[["L", "C", "C", "L"]] * 7
)
pdf.source_line("Fonte: Uddin et al. (2022); Mienye e Sun (2022); dados do experimento.")

pdf.para(
    "Os resultados de 88,33% com Hard Voting superam o KNN ensemble reportado por "
    "Uddin et al. (2022) com 82,34%, e tambem o KNN Hassanat — variante com melhor "
    "desempenho entre as 9 variantes do KNN avaliadas no estudo, com 83,62%. A "
    "acuracia obtida se aproxima do limite superior reportado por Mienye e Sun (2022) "
    "para ensembles mais complexos (ate 95%). O ganho de 1,67 pp sobre os modelos "
    "base confirma empiricamente o principio teorico de que ensemble de classificadores "
    "com erros parcialmente descorrelacionados produz melhor generalizacao "
    "(MIENYE; SUN, 2022)."
)

# ── 5. CONSIDERACOES FINAIS ───────────────────────────────────────────────────
pdf.section("5", "Consideracoes Finais")
pdf.para(
    "Este relatorio apresentou a implementacao e avaliacao completa de tres estrategias "
    "de ensemble — Hard Voting, Soft Voting e Stacking — combinando KNN (K=29) e SVM "
    "(C=0,1, RBF) para diagnostico binario de doenca cardiaca no Cleveland Heart "
    "Disease Dataset. A avaliacao cobriu acuracia, AUC-ROC, precision, recall, "
    "F1-score e validacao cruzada estratificada de 10-dobras."
)
pdf.para(
    "Os principais resultados sao: (i) Hard Voting e Soft Voting atingiram acuracia "
    "de 88,33% no conjunto de teste, ganho de 1,67 pp sobre os modelos base; "
    "(ii) o Stacking obteve o maior AUC-ROC (95,20%), 0,33 pp acima do KNN base; "
    "(iii) na validacao cruzada, o SVM individual foi o melhor (83,51%), e os ensembles "
    "ficaram proximos dos modelos base — reflexo da alta concordancia de 96,67% entre "
    "KNN e SVM; (iv) Soft Voting Ponderado e Stacking reduziram os Falsos Negativos "
    "de 6 para 5, melhorando o recall da classe doente de 78,57% para 82,14%; "
    "(v) o meta-learner de Stacking aprendeu peso SVM/KNN = 3,23/2,16, confirmando "
    "a maior confiabilidade das probabilidades do SVM."
)
pdf.para(
    "Como limitacoes: (i) a alta concordancia entre KNN e SVM (96,67%) limita o "
    "potencial do ensemble — classificadores mais heterogeneos (ex.: KNN + Random "
    "Forest) tenderiam a produzir ganhos maiores; (ii) o conjunto de teste reduzido "
    "(n=60) aumenta a variancia das estimativas de teste; (iii) apenas distancia "
    "Euclidiana foi avaliada para o KNN."
)
pdf.para(
    "Como trabalhos futuros, recomenda-se: (i) incluir classificadores mais "
    "heterogeneos no ensemble (Random Forest, XGBoost, Naive Bayes), potencialmente "
    "aumentando a descorrelacao de erros e o ganho do ensemble, conforme documentado "
    "por Mienye e Sun (2022); (ii) explorar boosting (AdaBoost, Gradient Boosting), "
    "que ajusta iterativamente os pesos das amostras mal classificadas; "
    "(iii) avaliar tecnicas de balanceamento de classes (SMOTE, undersampling) dado o "
    "leve desbalanceamento observado (53,9% vs. 46,1%); (iv) validar em datasets "
    "externos de maior dimensao para verificar generalizacao clinica."
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

# ── Salvar ────────────────────────────────────────────────────────────────────
out = BASE + "/artigos_relatorios/pdfs/Relatorio_Ensemble_FATEC.pdf"
pdf.output(out)
print(f"[OK] PDF gerado: {out}")
print(f"     Paginas: {pdf.page}")
