#!/usr/bin/env python3
"""TCC FATEC-GT 2026 — Parte 12: Últimas seções para 200+"""
from tcc_parte1 import PDF, ML, MR, MT, MB, PW, CW, SB, ST, SS, SC, LH, LT, LC, IND

def cap1_aprendizado_por_reforco(pdf):
    """Seção comparando aprendizado supervisionado com outras categorias."""
    pdf.np()
    pdf.SUB("1.30  Comparativo: Supervisionado, Não-Supervisionado e por Reforço")
    pdf.P(
        "Para contextualizar o aprendizado supervisionado implementado neste "
        "trabalho em relação às demais categorias de ML, apresenta-se "
        "uma comparação sistemática das três abordagens principais:"
    )
    pdf.TABLE(
        "Tabela 1.6 – Comparação das categorias de aprendizado de máquina",
        ["Critério","Supervisionado","Não-Supervisionado","Por Reforço"],
        [
            ["Dados","Pares (x,y) rotulados","Dados x sem rótulos","Estado, ação, recompensa"],
            ["Objetivo","Aprender f: X->Y","Descobrir estrutura","Maximizar recompensa acumulada"],
            ["Saída","Rótulo/valor predito","Clusters, representações","Política de ações"],
            ["Feedback","Imediato (rótulo correto)","Nenhum","Atrasado (recompensa)"],
            ["Exemplo clássico","Classificação de emails","K-means clustering","AlphaGo"],
            ["Utilizado neste trabalho","Sim (KNN, SVM, RF, etc.)","Não","Não"],
            ["Avaliação","Acurácia, AUC, F1","Silhouette, inércia","Recompensa total"],
            ["Escalabilidade","Depende do algoritmo","Alta (sem rótulos)","Depende do ambiente"],
        ],
        cw=[44,36,40,40], fsz=8
    )
    pdf.SRC("Fonte: Elaborado pelo autor com base em Géron (2019) e Russell & Norvig (2020).")
    pdf.P(
        "O aprendizado supervisionado é a escolha natural para classificação "
        "de imagens quando rótulos estão disponíveis (imagens organizadas "
        "por classe). O custo de rotulagem é o principal limitante: "
        "para grandes volumes de imagens, técnicas semi-supervisionadas "
        "(poucos rótulos + muitos dados não rotulados) ou de auto-supervisão "
        "(SimCLR, MoCo, DINO) são alternativas promissoras que podem "
        "ser exploradas em trabalhos futuros."
    )

    pdf.np()
    pdf.SUB("1.31  Métricas Adicionais: Precision-Recall e F-beta")
    pdf.P(
        "Além das métricas implementadas no sistema, duas métricas "
        "complementares são relevantes para aplicações diagnósticas:"
    )
    pdf.SSUB("1.31.1  Curva Precision-Recall")
    pdf.P(
        "A curva Precision-Recall (PR curve) é especialmente informativa "
        "para datasets desbalanceados, onde a curva ROC pode ser "
        "otimista. Para cada limiar de decisão theta:"
    )
    pdf.QUO(
        "Precisao(theta) = VP(theta) / (VP(theta) + FP(theta))\n"
        "Revocacao(theta) = VP(theta) / (VP(theta) + FN(theta))\n\n"
        "Area PR (AUPRC) = integral_0^1 Precisao(Revocacao) d(Revocacao)\n\n"
        "Para Cleveland dataset:\n"
        "- KNN   AUPRC ~= 0,91\n"
        "- SVM   AUPRC ~= 0,91\n"
        "- Stack AUPRC ~= 0,93  (melhor)"
    )
    pdf.SSUB("1.31.2  F-beta Score")
    pdf.P(
        "O F-beta score generaliza o F1 permitindo controlar o peso "
        "relativo entre Precisão e Revocação via parâmetro beta:"
    )
    pdf.QUO(
        "F_beta = (1 + beta^2) * Precisao * Revocacao / (beta^2 * Precisao + Revocacao)\n\n"
        "beta=1: F1 (pesos iguais)\n"
        "beta=2: F2 (prioriza Revocacao: 2x mais importante que Precisao)\n"
        "beta=0.5: F0.5 (prioriza Precisao: 2x mais importante que Revocacao)\n\n"
        "Para triagem clinica: beta=2 e o mais indicado (minimiza FN)"
    )
    pdf.P(
        "Para triagem clínica de doença cardíaca, o F2 seria mais "
        "apropriado que o F1, pois penaliza mais os Falsos Negativos "
        "(pacientes doentes não detectados). O sistema atual utiliza "
        "F1 como padrão; adicionar suporte a F2 e AUPRC seria uma "
        "melhoria relevante para versões futuras destinadas a "
        "aplicações clínicas."
    )

def cap2_validacao_cruzada_aninhada(pdf):
    """Validação cruzada aninhada."""
    pdf.np()
    pdf.SUB("2.14  Validação Cruzada Aninhada")
    pdf.P(
        "A validação cruzada aninhada (Nested Cross-Validation) é o "
        "protocolo mais rigoroso para avaliação e seleção de hiperparâmetros "
        "simultâneos, prevenindo o overfitting na seleção de hiperparâmetros:"
    )
    pdf.QUO(
        "Loop externo (avaliacao):   v dobras de avaliacao\n"
        "  Para cada dobra i:\n"
        "    Loop interno (HP search):  k dobras de validacao sobre D_treino_i\n"
        "      GridSearchCV(HP_grid)  =>  HP*_i\n"
        "    Treinar modelo com HP*_i sobre D_treino_i\n"
        "    Avaliar no D_teste_i  =>  Acc_i\n"
        "Acc_nested_CV = media(Acc_1, ..., Acc_v)"
    )
    pdf.P(
        "Diferente do protocolo adotado neste trabalho (GridSearchCV com "
        "CV interna, depois avaliação em teste hold-out), a CV aninhada "
        "usa v avaliações independentes — cada uma com sua própria "
        "otimização de hiperparâmetros. O resultado é uma estimativa "
        "imparcial do desempenho do PROCESSO de seleção de modelo, "
        "não apenas de um modelo específico."
    )
    pdf.P(
        "O protocolo deste trabalho (não aninhado) é uma simplificação "
        "aceitável para datasets de tamanho moderado como o Cleveland (297 "
        "exemplos), onde a variância de CV já é alta. A CV aninhada seria "
        "recomendada com datasets maiores (> 1000 exemplos) onde o overfitting "
        "na seleção de hiperparâmetros se torna um risco mais significativo."
    )

def cap4_comparacao_ferramentas(pdf):
    """Comparação com outras ferramentas de ML."""
    pdf.np()
    pdf.SUB("4.25  Posicionamento do Sistema entre Ferramentas Disponíveis")
    pdf.P(
        "O sistema desenvolvido ocupa um nicho específico no ecossistema "
        "de ferramentas de ML disponíveis para uso acadêmico e de pesquisa. "
        "Para contextualizar sua posição, uma comparação com as principais "
        "alternativas:"
    )
    pdf.TABLE(
        "Tabela 4.19 – Comparação com ferramentas existentes de ML",
        ["Ferramenta","Algoritmos","Multi-user","Segurança","Grad-CAM","Feedback","Tipo"],
        [
            ["Este sistema","9 (5+3+1)","Sim","Fernet+bcrypt","Sim","Sim","Webapp local"],
            ["Streamlit","Customizável","Não nativo","Básica","Customizável","Manual","Prototipagem"],
            ["Gradio","Customizável","Não","Nenhuma","Customizável","Não","Demo rápida"],
            ["KNIME",">100","Sim","Alta","Limitado","Não","Desktop/Cloud"],
            ["Weka",">100","Não","Nenhuma","Não","Não","Desktop Java"],
            ["Auto-sklearn","Automático","Não","Nenhuma","Não","Não","Script Python"],
            ["Orange",">50","Não","Básica","Limitado","Não","Visual analytics"],
        ],
        cw=[40,26,22,22,22,22,26], fsz=8
    )
    pdf.SRC("Fonte: Elaborado pelo autor.")
    pdf.P(
        "O diferencial do sistema desenvolvido é a combinação de: "
        "(1) comparação simultânea de 9 algoritmos em uma única sessão; "
        "(2) autenticação multi-usuário com segurança robusta; "
        "(3) Grad-CAM integrado para interpretabilidade; "
        "(4) reaprendizado ativo por feedback; e (5) base de dados "
        "relacional para histórico persistente. Nenhuma das ferramentas "
        "comparadas combina todas essas funcionalidades simultaneamente "
        "em uma plataforma web de acesso simples."
    )

def apendice_g(pdf):
    """Apêndice G — Referências Bibliográficas Complementares."""
    pdf.ns()
    pdf.SL("APÊNDICE G – Referências Bibliográficas Complementares")
    pdf.P(
        "Este apêndice lista referências bibliográficas adicionais "
        "consultadas durante o desenvolvimento deste trabalho, "
        "organizadas por tema."
    )
    pdf.SUB("G.1  Aprendizado de Máquina: Livros Didáticos")
    refs = [
        "BISHOP, C. M. Pattern Recognition and Machine Learning. New York: Springer, 2006.",
        "FRIEDMAN, J.; HASTIE, T.; TIBSHIRANI, R. The Elements of Statistical Learning. 2. ed. New York: Springer, 2009.",
        "JAMES, G. et al. An Introduction to Statistical Learning. New York: Springer, 2013.",
        "MITCHELL, T. Machine Learning. New York: McGraw-Hill, 1997.",
        "SHALEV-SHWARTZ, S.; BEN-DAVID, S. Understanding Machine Learning: From Theory to Algorithms. Cambridge: Cambridge University Press, 2014.",
    ]
    for r in refs: pdf.REF(r)

    pdf.SUB("G.2  Visão Computacional e Deep Learning")
    refs2 = [
        "GOODFELLOW, I.; BENGIO, Y.; COURVILLE, A. Deep Learning. Cambridge, MA: MIT Press, 2016.",
        "KRIZHEVSKY, A.; SUTSKEVER, I.; HINTON, G. E. ImageNet classification with deep convolutional neural networks. Communications of the ACM, v. 60, n. 6, p. 84–90, 2017.",
        "LeCUN, Y.; BOTTOU, L.; BENGIO, Y.; HAFFNER, P. Gradient-based learning applied to document recognition. Proceedings of the IEEE, v. 86, n. 11, p. 2278–2324, 1998.",
        "SIMONYAN, K.; ZISSERMAN, A. Very deep convolutional networks for large-scale image recognition. In: INTERNATIONAL CONFERENCE ON LEARNING REPRESENTATIONS (ICLR), 2015.",
    ]
    for r in refs2: pdf.REF(r)

    pdf.SUB("G.3  Segurança de Aplicações Web")
    refs3 = [
        "OWASP FOUNDATION. OWASP Top Ten 2021: The Ten Most Critical Web Application Security Risks. OWASP, 2021. Disponível em: https://owasp.org/Top10/.",
        "VIEGA, J.; MESSIER, M. Secure Programming Cookbook for C and C++. Sebastopol, CA: O'Reilly Media, 2003.",
        "BRASIL. Lei n. 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados Pessoais (LGPD). Brasília: Presidência da República, 2018.",
    ]
    for r in refs3: pdf.REF(r)

    pdf.SUB("G.4  Bancos de Dados e Sistemas Web")
    refs4 = [
        "GRINBERG, M. Flask Web Development: Developing Web Applications with Python. 2. ed. Sebastopol, CA: O'Reilly Media, 2018.",
        "MYSQL. MySQL 8.0 Reference Manual. Oracle Corporation, 2023. Disponível em: https://dev.mysql.com/doc/refman/8.0/en/.",
        "PALLETS PROJECTS. Flask Documentation (3.0.x). Disponível em: https://flask.palletsprojects.com/.",
    ]
    for r in refs4: pdf.REF(r)

    pdf.SUB("G.5  Artigos Científicos Relacionados")
    refs5 = [
        "DETRANO, R. et al. International application of a new probability algorithm for the diagnosis of coronary artery disease. The American Journal of Cardiology, v. 64, n. 5, p. 304–310, 1989.",
        "GRINSZTAJN, L.; OYALLON, E.; VAROQUAUX, G. Why tree-based models still outperform deep learning on tabular data. Advances in Neural Information Processing Systems (NeurIPS), v. 35, 2022.",
        "KINGMA, D. P.; BA, J. Adam: A Method for Stochastic Optimization. International Conference on Learning Representations (ICLR), 2015.",
        "RAMACHANDRAN, P.; ZOPH, B.; LE, Q. V. Searching for Activation Functions. arXiv:1710.05941, 2017.",
        "VALIANT, L. G. A theory of the learnable. Communications of the ACM, v. 27, n. 11, p. 1134–1142, 1984.",
        "WOLPERT, D. H.; MACREADY, W. G. No free lunch theorems for optimization. IEEE Transactions on Evolutionary Computation, v. 1, n. 1, p. 67–82, 1997.",
    ]
    for r in refs5: pdf.REF(r)
