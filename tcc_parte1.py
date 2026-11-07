#!/usr/bin/env python3
"""TCC FATEC-GT 2026 — Parte 1: Base class, capa, resumo, listas, sumário"""
import os
from fpdf import FPDF

ML=30.0; MR=20.0; MT=30.0; MB=20.0
PW=210.0; CW=PW-ML-MR
SB=11; ST=14; SS=11; SC=10
LH=7.5; LT=6.0; LC=6.0; IND=12.5

FONTS={"":"C:/Windows/Fonts/arial.ttf","B":"C:/Windows/Fonts/arialbd.ttf",
       "I":"C:/Windows/Fonts/ariali.ttf","BI":"C:/Windows/Fonts/arialbi.ttf"}

class PDF(FPDF):
    def __init__(self):
        super().__init__("P","mm","A4")
        for s,p in FONTS.items():
            if os.path.exists(p): self.add_font("Arial",s,p)
        self.set_margins(ML,MT,MR); self.set_auto_page_break(True,MB)
        self._cf=None; self._nn=True
    def header(self): self.set_y(MT)
    def footer(self): pass
    def _pn(self):
        if self._cf is None or self._nn: return
        n=self.page-self._cf+1; py=self.get_y()
        self.set_y(12); self.set_font("Arial","",SB)
        self.cell(CW,5,str(n),align="R"); self.set_y(py)
    def nc(self):  # new cover
        self._nn=True; self.add_page()
    def ns(self):  # new section (no printed number)
        self._nn=True; self.add_page(); self.set_y(MT)
    def np(self):  # new page (printed number)
        self._nn=False; self.add_page(); self._pn(); self.set_y(MT)
    def sc(self): self._cf=self.page  # start counting

    def P(self,t,ind=True,al="J"):
        self.set_font("Arial","",SB)
        x=ML+(IND if ind else 0); w=CW-(IND if ind else 0)
        self.set_x(x); self.multi_cell(w,LH,t,align=al); self.set_x(ML)
    def B(self,t,ind=True,al="J"):
        self.set_font("Arial","B",SB)
        x=ML+(IND if ind else 0); w=CW-(IND if ind else 0)
        self.set_x(x); self.multi_cell(w,LH,t,align=al); self.set_x(ML)
    def I(self,t,ind=True,al="J"):
        self.set_font("Arial","I",SB)
        x=ML+(IND if ind else 0); w=CW-(IND if ind else 0)
        self.set_x(x); self.multi_cell(w,LH,t,align=al); self.set_x(ML)
    def BL(self,n=1): self.ln(LH*n)
    def SL(self,t):
        self.set_font("Arial","B",ST); self.set_x(ML)
        self.multi_cell(CW,LT,t,align="L"); self.ln(LH)
    def SUB(self,t):
        self.ln(3); self.set_font("Arial","B",SS); self.set_x(ML)
        self.multi_cell(CW,LT,t,align="L"); self.ln(3)
    def SSUB(self,t):
        self.ln(2); self.set_font("Arial","BI",SS); self.set_x(ML)
        self.multi_cell(CW,LT,t,align="L"); self.ln(2)
    def SSSUB(self,t):
        self.ln(1); self.set_font("Arial","I",SS); self.set_x(ML)
        self.multi_cell(CW,LT,t,align="L"); self.ln(1)
    def CAP(self,t):
        self.set_font("Arial","B",SC); self.set_x(ML)
        self.multi_cell(CW,LC,t,align="C")
    def SRC(self,t):
        self.set_font("Arial","",SC); self.set_x(ML)
        self.multi_cell(CW,LC,t,align="C"); self.ln(3)
    def QUO(self,t):
        self.set_font("Arial","",SC); self.set_x(ML+40)
        self.multi_cell(CW-40,LC,t,align="J"); self.set_x(ML); self.ln(2)
    def REF(self,t):
        self.set_font("Arial","",SB); self.set_x(ML)
        self.multi_cell(CW,6.5,t,align="L"); self.ln(2)
    def BULL(self,items,ind=True):
        self.set_font("Arial","",SB)
        for it in items:
            self.set_x(ML+(IND if ind else 5))
            self.multi_cell(CW-(IND if ind else 5),LH,"• "+it,align="J")
            self.set_x(ML)
    def TABLE(self,cap,hdrs,rows,cw=None,fsz=10):
        n=len(hdrs)
        if cw is None: cw=[CW/n]*n
        lh=6.0; self.CAP(cap); self.ln(1)
        self.set_font("Arial","B",fsz); self.set_x(ML)
        for i,h in enumerate(hdrs): self.cell(cw[i],lh,h,border=1,align="C")
        self.ln()
        self.set_font("Arial","",fsz)
        for row in rows:
            if self.get_y()+lh>297-MB: self.add_page(); self.set_font("Arial","",fsz)
            self.set_x(ML)
            for i,v in enumerate(row): self.cell(cw[i],lh,str(v),border=1,align="C")
            self.ln()
        self.ln(2)
    def ALGO(self,title,lines):
        """Pseudocódigo em caixa."""
        self.ln(2); self.set_font("Arial","B",SC)
        self.set_x(ML); self.multi_cell(CW,LC,title,align="L")
        self.set_font("Arial","",SC)
        x0=ML; y0=self.get_y(); total_h=len(lines)*LC+4
        for line in lines:
            self.set_x(x0+3)
            self.multi_cell(CW-6,LC,line,align="L")
        y1=self.get_y()
        self.rect(x0,y0-1,CW,y1-y0+2)
        self.ln(3)

def capa(pdf):
    pdf.nc()
    pdf.set_font("Arial","B",16); pdf.set_x(ML)
    pdf.multi_cell(CW,8,"FACULDADE DE TECNOLOGIA DE GUARATINGUETÁ",align="C")
    pdf.ln(55)
    pdf.set_font("Arial","B",18); pdf.set_x(ML)
    pdf.multi_cell(CW,9,
        "ANÁLISE COMPARATIVA DE ALGORITMOS DE\n"
        "INTELIGÊNCIA ARTIFICIAL PARA CLASSIFICAÇÃO\n"
        "DE IMAGENS BASEADA EM APRENDIZADO\n"
        "SUPERVISIONADO",align="C")
    pdf.ln(14)
    pdf.set_font("Arial","B",16); pdf.set_x(ML)
    pdf.multi_cell(CW,8,"André Felipe de Oliveira Mota",align="C")
    pdf.ln(22)
    pdf.set_font("Arial","",12); pdf.set_x(ML+80)
    pdf.multi_cell(CW-80,6,
        "Relatório Técnico-científico apresentado à\n"
        "Faculdade de Tecnologia de Guaratinguetá,\n"
        "como requisito parcial para conclusão do\n"
        "Curso Superior de Tecnologia em Análise\n"
        "e Desenvolvimento de Sistemas.\n\n"
        "Orientador: Prof. Dr. ...",align="J")
    pdf.ln(28)
    pdf.set_font("Arial","B",16); pdf.set_x(ML)
    pdf.multi_cell(CW,8,"Guaratinguetá – SP\n2026",align="C")

def verso(pdf):
    pdf.nc(); pdf.ln(180)
    pdf.set_font("Arial","",SB); pdf.set_x(ML)
    pdf.multi_cell(CW,6.5,
        "MOTA, André Felipe de Oliveira. Análise Comparativa de Algoritmos de "
        "Inteligência Artificial para Classificação de Imagens Baseada em Aprendizado "
        "Supervisionado. Guaratinguetá, 2026. Relatório Técnico-científico, Curso "
        "Superior de Tecnologia em Análise e Desenvolvimento de Sistemas, Faculdade "
        "de Tecnologia de Guaratinguetá, 2026.",align="L")

def resumo(pdf):
    pdf.ns(); pdf.sc()
    pdf.set_font("Arial","",SB); pdf.set_x(ML)
    pdf.multi_cell(CW,6.5,
        "MOTA, André Felipe de Oliveira. Análise Comparativa de Algoritmos de "
        "Inteligência Artificial para Classificação de Imagens Baseada em Aprendizado "
        "Supervisionado. 2026. Relatório Técnico-científico, Curso de Análise e "
        "Desenvolvimento de Sistemas, Faculdade de Tecnologia de Guaratinguetá, 2026.",align="L")
    pdf.ln(5)
    pdf.set_font("Arial","B",SB); pdf.set_x(ML)
    pdf.multi_cell(CW,LT,"Resumo",align="C"); pdf.ln(2)
    pdf.P(
        "O avanço exponencial da disponibilidade de dados digitais e o crescimento do "
        "poder computacional têm transformado o panorama da Inteligência Artificial (IA), "
        "viabilizando aplicações de classificação automática de imagens em escalas antes "
        "inimagináveis. Diante desse cenário, a comparação rigorosa de algoritmos de "
        "aprendizado supervisionado torna-se indispensável para embasar decisões técnicas "
        "sobre qual abordagem adotar em cada contexto. Este trabalho apresenta o "
        "desenvolvimento de uma plataforma web para análise comparativa de algoritmos de "
        "IA aplicados à classificação de imagens digitais baseada em aprendizado "
        "supervisionado, integrando fundamentos matemáticos, implementação computacional "
        "e engenharia de software em uma única contribuição acadêmica. O sistema "
        "implementa cinco algoritmos individuais — K-Nearest Neighbors (KNN), Support "
        "Vector Machine (SVM), Random Forest, Regressão Logística e Naive Bayes "
        "Gaussiano — três métodos de ensemble — Votação Majoritária (Hard Voting), "
        "Votação por Probabilidades (Soft Voting) e Stacking com meta-aprendizado por "
        "Regressão Logística — e uma Rede Neural Convolucional (CNN) baseada em "
        "EfficientNet-B0 com transfer learning a partir do ImageNet."
    )
    pdf.P(
        "Para validação científica dos algoritmos clássicos, foi empregado o Cleveland "
        "Heart Disease Dataset (UCI Machine Learning Repository, id=45), composto por "
        "297 registros clínicos com 13 atributos preditores após limpeza de dados. A "
        "análise paramétrica do KNN avaliou sistematicamente 100 combinações de "
        "parâmetros (25 valores de K x 4 configurações de validação cruzada), "
        "totalizando mais de 2.000 execuções, identificando K=29 como valor ótimo com "
        "acurácia média de 83,28% e AUC-ROC de 90,20%. O SVM com kernel RBF e C=0,1 "
        "obteve 83,51% de acurácia na validação cruzada de 10 dobras, evidenciando "
        "equivalência prática com o KNN no dataset utilizado. Os métodos de ensemble "
        "superaram os classificadores individuais (88,33% versus 86,67% de acurácia no "
        "conjunto de teste), com o Stacking alcançando o melhor AUC-ROC (0,9520). A "
        "redução de falsos negativos de 6 para 5 casos pelo Soft Voting é clinicamente "
        "relevante no contexto de triagem diagnóstica."
    )
    pdf.P(
        "A extração de features das imagens utiliza o descritor Histograma de Gradientes "
        "Orientados (HOG), produzindo vetores de 324 dimensões a partir de imagens "
        "redimensionadas para 128x128 pixels. A rede neural EfficientNet-B0 processa "
        "imagens em 224x224 com data augmentation, utilizando otimizador Adam com "
        "scheduler OneCycleLR em 8 épocas de treinamento. A interpretabilidade da CNN "
        "é provida pelo Grad-CAM, que gera mapas de calor sobrepostos às imagens "
        "originais, identificando as regiões determinantes para cada classificação."
    )
    pdf.P(
        "O sistema web, desenvolvido em Python (Flask), MySQL e HTML/CSS/JavaScript, "
        "oferece: autenticação segura com criptografia simétrica Fernet (AES-128) para "
        "emails e hashing bcrypt para senhas; verificação de email por código de 6 "
        "dígitos; rate limiting de 10 tentativas por minuto no login; treinamento "
        "assíncrono com progresso em tempo real; visualização interativa de curvas ROC, "
        "matrizes de confusão e Grad-CAM; sistema de feedback com reaprendizado ativo; "
        "e exportação de resultados em CSV. A arquitetura multi-usuário garante "
        "isolamento completo de dados entre usuários via verificação de user_id em todas "
        "as operações sensíveis."
    )
    pdf.ln(2)
    pdf.set_font("Arial","B",SB); pdf.set_x(ML)
    pdf.multi_cell(CW,LH,
        "Palavras-chave: Aprendizado de Máquina Supervisionado; Classificação de "
        "Imagens; K-Nearest Neighbors; Support Vector Machine; Ensemble Learning; "
        "EfficientNet-B0; HOG; Flask; MySQL; Segurança da Informação.",align="L")
    pdf.ln(8)
    pdf.set_font("Arial","B",SB); pdf.set_x(ML)
    pdf.multi_cell(CW,LT,"Abstract",align="C"); pdf.ln(2)
    pdf.P(
        "The exponential growth in digital data availability and increased computational "
        "power have transformed the Artificial Intelligence landscape, enabling automatic "
        "image classification applications at previously unimaginable scales. In this "
        "context, rigorous comparison of supervised learning algorithms becomes "
        "indispensable for grounding technical decisions about which approach to adopt. "
        "This work presents the development of a web platform for comparative analysis "
        "of AI algorithms applied to supervised learning-based digital image "
        "classification, integrating mathematical foundations, computational "
        "implementation, and software engineering in a single academic contribution. "
        "The system implements five individual algorithms — K-Nearest Neighbors (KNN), "
        "Support Vector Machine (SVM), Random Forest, Logistic Regression, and Gaussian "
        "Naive Bayes — three ensemble methods — Hard Voting, Soft Voting, and Stacking "
        "with Logistic Regression meta-learning — and a Convolutional Neural Network "
        "(CNN) based on EfficientNet-B0 with transfer learning from ImageNet."
    )
    pdf.P(
        "For scientific validation of classical algorithms, the Cleveland Heart Disease "
        "Dataset (UCI Machine Learning Repository, id=45) was used, comprising 297 "
        "clinical records with 13 predictor attributes after data cleaning. The KNN "
        "parametric analysis systematically evaluated 100 parameter combinations (25 K "
        "values x 4 cross-validation configurations), totaling over 2,000 runs, "
        "identifying K=29 as optimal with 83.28% mean accuracy and 90.20% AUC-ROC. "
        "SVM with RBF kernel and C=0.1 achieved 83.51% accuracy in 10-fold cross-"
        "validation, showing practical equivalence with KNN on this dataset. Ensemble "
        "methods outperformed individual classifiers (88.33% vs 86.67% test accuracy), "
        "with Stacking achieving the best AUC-ROC (0.9520). The web system offers "
        "secure authentication with Fernet (AES-128) encryption, asynchronous training, "
        "interactive ROC curve and confusion matrix visualization, Grad-CAM heatmaps, "
        "active relearning, and CSV export."
    )
    pdf.ln(2)
    pdf.set_font("Arial","B",SB); pdf.set_x(ML)
    pdf.multi_cell(CW,LH,
        "Keywords: Supervised Machine Learning; Image Classification; K-Nearest "
        "Neighbors; Support Vector Machine; Ensemble Learning; EfficientNet-B0; "
        "HOG; Flask; MySQL; Information Security.",align="L")

def listas(pdf):
    # Lista de Figuras
    pdf.ns()
    pdf.SL("LISTA DE FIGURAS")
    itens_fig=[
        ("Figura 1","Arquitetura geral do sistema de três camadas","29"),
        ("Figura 2","Diagrama Entidade-Relacionamento do banco de dados MySQL","31"),
        ("Figura 3","Pipeline de extração de features HOG","26"),
        ("Figura 4","Fronteira de decisão do KNN para K=1, K=5 e K=29","46"),
        ("Figura 5","Curva de acurácia do KNN em função do parâmetro K","46"),
        ("Figura 6","Hiperplano de separação e vetores de suporte do SVM","50"),
        ("Figura 7","Comparação de kernels SVM: linear, RBF e polinomial","52"),
        ("Figura 8","Estrutura de uma árvore de decisão do Random Forest","55"),
        ("Figura 9","Diagrama de ensemble com Hard Voting, Soft Voting e Stacking","59"),
        ("Figura 10","Arquitetura EfficientNet-B0 e fluxo de transfer learning","63"),
        ("Figura 11","Exemplo de mapa de calor Grad-CAM sobreposto a imagem","65"),
        ("Figura 12","Pipeline completo HOG: célula, bloco, histograma e concatenação","68"),
        ("Figura 13","Curva ROC comparativa de todos os modelos","110"),
        ("Figura 14","Matrizes de confusão: KNN, SVM e Soft Voting","112"),
        ("Figura 15","Boxplot das acurácias de validação cruzada por modelo","115"),
        ("Figura 16","Tela principal (Dashboard) do sistema web","92"),
        ("Figura 17","Tela de treinamento com barra de progresso","95"),
        ("Figura 18","Tela de resultados com tabela comparativa e curva ROC","97"),
        ("Figura 19","Tela de teste de imagens com Grad-CAM","99"),
        ("Figura 20","Fluxo de autenticação e criptografia do sistema","103"),
    ]
    pdf.set_font("Arial","",SB)
    for fig,desc,pg in itens_fig:
        y0=pdf.get_y()
        pdf.set_x(ML); pdf.cell(CW-12,7,f"{fig} – {desc}",align="L")
        pdf.set_x(ML); pdf.set_y(y0)
        pdf.cell(CW,7,pg,align="R"); pdf.ln(7)
    # Lista de Tabelas
    pdf.ns()
    pdf.SL("LISTA DE TABELAS")
    itens_tab=[
        ("Tabela 1","Atributos do Cleveland Heart Disease Dataset","26"),
        ("Tabela 2","Divisão treino/teste estratificada após binarização","27"),
        ("Tabela 3","Resultados consolidados da análise paramétrica KNN por faixa de K","46"),
        ("Tabela 4","Top-5 valores de K na validação cruzada de 5 dobras","47"),
        ("Tabela 5","Acurácia do KNN (K=29) por bloco de 50 registros","48"),
        ("Tabela 6","Métricas consolidadas do KNN (K=29)","49"),
        ("Tabela 7","Relatório de classificação por classe – KNN","49"),
        ("Tabela 8","Top-5 combinações de hiperparâmetros SVM – validação 5-fold","52"),
        ("Tabela 9","Acurácia do SVM por bloco de 50 registros","53"),
        ("Tabela 10","Métricas consolidadas do SVM","53"),
        ("Tabela 11","Comparação SVM vs. KNN","55"),
        ("Tabela 12","Resultados do Random Forest por configuração","57"),
        ("Tabela 13","Acurácia e AUC-ROC: Regressão Logística e Naive Bayes","59"),
        ("Tabela 14","Resultados comparativos ensemble vs. individuais","61"),
        ("Tabela 15","Matriz de confusão detalhada – Soft Voting Ponderado","63"),
        ("Tabela 16","Análise do trade-off viés-variância por faixa de K","47"),
        ("Tabela 17","Schema completo – tabela users","31"),
        ("Tabela 18","Schema completo – tabela training_sessions","32"),
        ("Tabela 19","Schema completo – tabela model_results","33"),
        ("Tabela 20","Schema completo – tabela predictions","34"),
        ("Tabela 21","Endpoints da API REST organizados por domínio","83"),
        ("Tabela 22","Comparação com resultados da literatura","116"),
        ("Tabela 23","Comparação de complexidade computacional dos algoritmos","118"),
    ]
    pdf.set_font("Arial","",SB)
    for tab,desc,pg in itens_tab:
        y0=pdf.get_y()
        pdf.set_x(ML); pdf.cell(CW-12,7,f"{tab} – {desc}",align="L")
        pdf.set_x(ML); pdf.set_y(y0)
        pdf.cell(CW,7,pg,align="R"); pdf.ln(7)
    # Lista de Abreviaturas
    pdf.ns()
    pdf.SL("LISTA DE ABREVIATURAS E SIGLAS")
    abrv=[
        ("ABNT","Associação Brasileira de Normas Técnicas"),
        ("AUC","Area Under Curve (Área sob a Curva)"),
        ("API","Application Programming Interface"),
        ("CBC","Cipher Block Chaining (Modo de cifra em bloco encadeado)"),
        ("CNN","Convolutional Neural Network (Rede Neural Convolucional)"),
        ("CPU","Central Processing Unit"),
        ("CSV","Comma-Separated Values"),
        ("CUDA","Compute Unified Device Architecture"),
        ("FN","Falso Negativo"),
        ("FP","Falso Positivo"),
        ("GPU","Graphics Processing Unit"),
        ("HMAC","Hash-based Message Authentication Code"),
        ("HOG","Histogram of Oriented Gradients"),
        ("HTML","HyperText Markup Language"),
        ("HTTP","HyperText Transfer Protocol"),
        ("IA","Inteligência Artificial"),
        ("JSON","JavaScript Object Notation"),
        ("KKT","Karush–Kuhn–Tucker (condições de otimalidade)"),
        ("KNN","K-Nearest Neighbors (K Vizinhos mais Próximos)"),
        ("LGPD","Lei Geral de Proteção de Dados"),
        ("ML","Machine Learning (Aprendizado de Máquina)"),
        ("OMS","Organização Mundial da Saúde"),
        ("OWASP","Open Web Application Security Project"),
        ("QP","Quadratic Programming (Programação Quadrática)"),
        ("RBF","Radial Basis Function"),
        ("REST","Representational State Transfer"),
        ("RF","Random Forest"),
        ("ROC","Receiver Operating Characteristic"),
        ("SQL","Structured Query Language"),
        ("SMTP","Simple Mail Transfer Protocol"),
        ("SVM","Support Vector Machine"),
        ("UCI","University of California, Irvine"),
        ("VN","Verdadeiro Negativo"),
        ("VP","Verdadeiro Positivo"),
        ("WSGI","Web Server Gateway Interface"),
    ]
    for abr,exp in abrv:
        pdf.set_font("Arial","B",SB); pdf.set_x(ML)
        pdf.cell(30,LH,abr)
        pdf.set_font("Arial","",SB)
        pdf.multi_cell(CW-30,LH,exp,align="L")

def sumario(pdf):
    pdf.ns()
    pdf.set_font("Arial","B",ST); pdf.set_x(ML)
    pdf.multi_cell(CW,LT,"SUMÁRIO",align="C"); pdf.ln(LH)
    entries=[
        (0,"INTRODUÇÃO","11"),
        (1,"1  REFERENCIAL TEÓRICO","15"),
        (2,"   1.1  Inteligência Artificial: Conceitos e Evolução Histórica","15"),
        (2,"   1.2  Visão Computacional e Classificação de Imagens","17"),
        (2,"   1.3  Aprendizado de Máquina Supervisionado","18"),
        (2,"   1.4  Algoritmo K-Nearest Neighbors (KNN)","20"),
        (2,"   1.5  Support Vector Machine (SVM)","24"),
        (2,"   1.6  Random Forest","29"),
        (2,"   1.7  Regressão Logística","31"),
        (2,"   1.8  Naive Bayes Gaussiano","32"),
        (2,"   1.9  Ensemble Learning","34"),
        (2,"   1.10 Redes Neurais Convolucionais e EfficientNet-B0","37"),
        (2,"   1.11 Histograma de Gradientes Orientados (HOG)","40"),
        (2,"   1.12 Métricas de Avaliação e Validação Cruzada","42"),
        (1,"2  METODOLOGIA","65"),
        (2,"   2.1  Visão Geral e Etapas do Trabalho","65"),
        (2,"   2.2  Dataset: Cleveland Heart Disease","66"),
        (2,"   2.3  Análise Exploratória dos Dados","67"),
        (2,"   2.4  Pipeline de Pré-processamento","69"),
        (2,"   2.5  Extração de Features HOG","71"),
        (2,"   2.6  Protocolo de Treinamento e Otimização","72"),
        (2,"   2.7  Protocolo de Avaliação Estatística","74"),
        (2,"   2.8  Ambiente Computacional","75"),
        (1,"3  DESENVOLVIMENTO DO SISTEMA","84"),
        (2,"   3.1  Levantamento de Requisitos","84"),
        (2,"   3.2  Arquitetura Geral do Sistema","85"),
        (2,"   3.3  Banco de Dados MySQL","87"),
        (2,"   3.4  Backend — API REST Flask","91"),
        (2,"   3.5  Módulo de Machine Learning","94"),
        (2,"   3.6  Módulo de Deep Learning: CNN e Grad-CAM","96"),
        (2,"   3.7  Frontend — Interface Web","98"),
        (2,"   3.8  Segurança e Criptografia","101"),
        (2,"   3.9  Desempenho e Escalabilidade","105"),
        (1,"4  RESULTADOS E DISCUSSÃO","125"),
        (2,"   4.1  Análise Paramétrica Completa do KNN","125"),
        (2,"   4.2  Análise Completa do SVM","129"),
        (2,"   4.3  Random Forest: Resultados e Importância de Features","131"),
        (2,"   4.4  Regressão Logística e Naive Bayes","132"),
        (2,"   4.5  Ensemble Learning: Análise Detalhada","133"),
        (2,"   4.6  EfficientNet-B0: Resultados e Grad-CAM","135"),
        (2,"   4.7  Comparação Geral e Análise de Complexidade","136"),
        (2,"   4.8  Demonstração do Sistema","137"),
        (2,"   4.9  Discussão Geral dos Resultados","139"),
        (0,"CONSIDERAÇÕES FINAIS","159"),
        (0,"REFERÊNCIAS","165"),
        (0,"APÊNDICE A – Pseudocódigos dos Algoritmos","173"),
        (0,"APÊNDICE B – Schema SQL Completo","175"),
        (0,"APÊNDICE C – Documentação Completa da API REST","178"),
    ]
    pdf.set_font("Arial","",SB)
    for bold,label,pg in entries:
        if bold==0: pdf.set_font("Arial","B",SB)
        elif bold==1: pdf.set_font("Arial","B",SB)
        else: pdf.set_font("Arial","",SB)
        y0=pdf.get_y()
        pdf.set_x(ML); pdf.cell(CW-10,7,label,align="L")
        pdf.set_x(ML); pdf.set_y(y0)
        pdf.set_font("Arial","",SB)
        pdf.cell(CW,7,pg,align="R"); pdf.ln(7)
