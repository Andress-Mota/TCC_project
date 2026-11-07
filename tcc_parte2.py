#!/usr/bin/env python3
"""TCC FATEC-GT 2026 — Parte 2: Introdução + Cap 1 seções 1.1-1.5"""
from tcc_parte1 import PDF, ML, MR, MT, MB, PW, CW, SB, ST, SS, SC, LH, LT, LC, IND

def introducao(pdf):
    pdf.ns()
    pdf.SL("INTRODUÇÃO")
    pdf.P(
        "A humanidade gera hoje mais de 2,5 quintilhões de bytes de dados diariamente, "
        "e estima-se que mais de 80% desse volume consiste em dados não estruturados — "
        "imagens, vídeos, áudios e textos. No domínio das imagens digitais, a "
        "capacidade de classificar automaticamente objetos, padrões, rostos, lesões "
        "médicas ou defeitos industriais representa uma das fronteiras mais ativas da "
        "Inteligência Artificial contemporânea. A partir do surgimento das Redes "
        "Neurais Convolucionais modernas com o AlexNet em 2012, que reduziu a taxa de "
        "erro no desafio ImageNet de 26% para 15,3% em um único ano, o campo de visão "
        "computacional experimentou uma revolução tecnológica sem precedentes "
        "(GÉRON, 2019)."
    )
    pdf.P(
        "Contudo, o ecossistema de algoritmos disponíveis para classificação é vasto "
        "e heterogêneo. Métodos clássicos como K-Nearest Neighbors (KNN) e Support "
        "Vector Machine (SVM) possuem décadas de fundamentação matemática sólida e "
        "continuam amplamente utilizados em aplicações práticas, especialmente quando "
        "o volume de dados é limitado ou quando a interpretabilidade das decisões é "
        "requisito crítico. Algoritmos de ensemble, como Random Forest, Hard Voting "
        "e Stacking, combinam múltiplos modelos para superar as limitações de cada "
        "classificador individual. Redes Neurais Convolucionais profundas, como a "
        "família EfficientNet, dominam benchmarks em larga escala ao custo de maior "
        "complexidade computacional e menor interpretabilidade intrínseca."
    )
    pdf.P(
        "A questão central que motiva este trabalho é: como comparar, de forma "
        "rigorosa e reprodutível, o desempenho desses algoritmos distintos aplicados "
        "a um mesmo problema de classificação de imagens? Essa comparação exige não "
        "apenas a implementação correta de cada algoritmo, mas também um protocolo "
        "de avaliação padronizado, uma representação numérica das imagens adequada "
        "(feature extraction), e uma plataforma que integre o ciclo completo de "
        "treinamento, avaliação e inferência de forma acessível."
    )
    pdf.P(
        "O presente trabalho endereça esse problema por dois caminhos complementares. "
        "Primeiro, realiza uma investigação científica aprofundada sobre os fundamentos "
        "matemáticos de cada algoritmo — partindo das equações de otimização do SVM "
        "às arquiteturas de redes convolucionais com EfficientNet-B0 — e valida "
        "experimentalmente cada modelo com o Cleveland Heart Disease Dataset (UCI, "
        "id=45), um dataset de referência amplamente utilizado na literatura de "
        "diagnóstico por aprendizado de máquina. Segundo, desenvolve um sistema web "
        "completo que permite ao usuário aplicar esses algoritmos a qualquer conjunto "
        "de imagens organizado por classes, visualizando métricas comparativas "
        "detalhadas em uma interface responsiva e segura."
    )
    pdf.P(
        "A relevância do trabalho extrapola o âmbito acadêmico. Sistemas de "
        "reconhecimento de imagens são utilizados em medicina para detectar tumores "
        "e doenças cardíacas em exames de imagem; na segurança pública para "
        "reconhecimento facial; na indústria 4.0 para inspeção automática de "
        "qualidade; e na agricultura de precisão para detecção de pragas e doenças "
        "em lavouras. Compreender profundamente os fundamentos e limitações de cada "
        "abordagem é condição necessária para selecionar e implantar modelos de "
        "forma responsável e eficiente (RUSSELL; NORVIG, 2020)."
    )
    pdf.P(
        "Do ponto de vista da engenharia de software, o sistema desenvolvido integra "
        "múltiplas tecnologias: Python para o processamento de dados e machine "
        "learning, Flask para a API REST, MySQL para persistência, "
        "HTML/CSS/JavaScript para a interface, bibliotecas scikit-learn e PyTorch "
        "para os modelos de aprendizado, e OpenCV com scikit-image para o "
        "processamento de imagens. A segurança da plataforma foi implementada com "
        "criptografia Fernet (AES-128) para proteção de emails, hashing bcrypt para "
        "senhas, verificação de identidade por email, e controle de acesso baseado "
        "em sessões autenticadas."
    )
    pdf.BL(0.5)
    pdf.SUB("Justificativa")
    pdf.P(
        "A escolha de comparar KNN, SVM, Random Forest, Regressão Logística, Naive "
        "Bayes, métodos de Ensemble e EfficientNet-B0 não é arbitrária. Esses "
        "algoritmos representam os principais paradigmas do aprendizado de máquina "
        "supervisionado: aprendizado baseado em instâncias (KNN), maximização de "
        "margem (SVM), aprendizado de conjunto por árvores (Random Forest), modelos "
        "lineares probabilísticos (Regressão Logística e Naive Bayes), combinação de "
        "classificadores (Ensemble) e aprendizado profundo por gradiente (CNN). "
        "Sua comparação em condições experimentais idênticas — mesmo dataset, mesmo "
        "protocolo de avaliação, mesma representação de features — fornece insights "
        "genuínos sobre as vantagens e limitações de cada abordagem."
    )
    pdf.P(
        "Adicionalmente, a construção de uma plataforma web que automatize e "
        "democratize esse processo comparativo representa contribuição prática "
        "relevante para pesquisadores, docentes e profissionais que precisam avaliar "
        "algoritmos de ML para classificação de imagens sem necessidade de escrever "
        "código do zero. O sistema implementa reaprendizado ativo — retreinamento com "
        "predições incorretas corrigidas pelo usuário — funcionalidade que eleva a "
        "plataforma além de um simples comparador de algoritmos."
    )
    pdf.BL(0.5)
    pdf.SUB("Objetivos Gerais")
    pdf.P(
        "Estudar, implementar, comparar e avaliar o desempenho de diferentes "
        "algoritmos matemáticos de Inteligência Artificial aplicados à classificação "
        "supervisionada de imagens digitais, integrando os modelos em um sistema web "
        "funcional que permita análise quantitativa e qualitativa de cada abordagem."
    )
    pdf.BL(0.3)
    pdf.SUB("Objetivos Específicos")
    pdf.BULL([
        "Fundamentar matematicamente os algoritmos KNN, SVM, Random Forest, "
        "Regressão Logística, Naive Bayes Gaussiano, Ensemble Learning e "
        "EfficientNet-B0, abordando as equações de otimização, formulações duais "
        "e propriedades de generalização de cada abordagem;",
        "Realizar análise paramétrica sistemática do KNN, avaliando 100 combinações "
        "de parâmetros (valores de K x configurações de validação cruzada) para "
        "identificar K ótimo fundamentado no trade-off viés-variância;",
        "Implementar todos os algoritmos em Python, utilizando scikit-learn para "
        "os modelos clássicos e ensemble, e PyTorch com torchvision para a rede "
        "neural convolucional EfficientNet-B0;",
        "Desenvolver módulo de extração de features baseado em Histograma de "
        "Gradientes Orientados (HOG) para representação numérica de imagens, "
        "e integrar a técnica Grad-CAM para interpretabilidade da CNN;",
        "Projetar e implementar banco de dados relacional MySQL com esquema "
        "normalizado para persistência de usuários, sessões de treinamento, "
        "resultados de modelos, predições e logs de sistema;",
        "Desenvolver API REST em Flask com mais de 30 endpoints para operações de "
        "autenticação, treinamento assíncrono, predição, visualização e exportação;",
        "Implementar interface web responsiva em HTML/CSS/JavaScript com sete páginas "
        "funcionais, suporte a temas claro/escuro e visualizações interativas "
        "(curvas ROC, matrizes de confusão, Grad-CAM);",
        "Implementar sistema de autenticação com múltiplas camadas de segurança: "
        "criptografia Fernet (AES-128), hashing bcrypt, verificação de email, "
        "rate limiting e isolamento de dados por usuário;",
        "Validar os algoritmos clássicos com o Cleveland Heart Disease Dataset e "
        "documentar resultados comparativos com a literatura especializada;",
        "Implementar funcionalidade de reaprendizado ativo baseado em feedback do "
        "usuário sobre predições incorretas.",
    ])
    pdf.BL(0.5)
    pdf.SUB("Organização do Relatório")
    pdf.P(
        "O presente relatório está organizado em quatro capítulos textuais. O "
        "Capítulo 1 apresenta o referencial teórico, cobrindo em profundidade os "
        "fundamentos matemáticos de cada algoritmo implementado, desde o "
        "K-Nearest Neighbors até a arquitetura EfficientNet-B0 com Grad-CAM. O "
        "Capítulo 2 descreve a metodologia adotada, incluindo a caracterização do "
        "dataset, a análise exploratória dos dados, o pipeline de pré-processamento, "
        "o protocolo de avaliação estatística e o ambiente computacional utilizado. "
        "O Capítulo 3 detalha o desenvolvimento completo do sistema, abrangendo "
        "requisitos, arquitetura, banco de dados, API REST, módulos de ML e CNN, "
        "interface web e segurança. O Capítulo 4 apresenta os resultados obtidos "
        "em todos os algoritmos e realiza a discussão comparativa fundamentada na "
        "literatura. As Considerações Finais sintetizam as contribuições científicas "
        "e de engenharia, e apontam direções para trabalhos futuros. Os apêndices "
        "documentam os pseudocódigos, o schema SQL e a documentação completa da API."
    )

def cap1_s1(pdf):
    """1.1 IA e evolução histórica"""
    pdf.ns()
    pdf.SL("1  REFERENCIAL TEÓRICO")
    pdf.SUB("1.1  Inteligência Artificial: Conceitos e Evolução Histórica")
    pdf.P(
        "A Inteligência Artificial (IA) é definida por Russell e Norvig (2020, p. 1) "
        "como o estudo de agentes que recebem percepções do ambiente e realizam ações. "
        "A origem formal do campo data de 1956, com a Conferência de Dartmouth, onde "
        "John McCarthy cunhou o termo 'Artificial Intelligence'. Nesse evento, "
        "pesquisadores como Marvin Minsky, Claude Shannon e Herbert Simon "
        "estabeleceram as bases de uma nova disciplina que buscava replicar "
        "computacionalmente as capacidades cognitivas humanas."
    )
    pdf.P(
        "A trajetória histórica da IA é marcada por ciclos alternados de entusiasmo "
        "e desencanto — os chamados 'Invernos da IA'. O primeiro inverno (1974-1980) "
        "decorreu da incapacidade dos sistemas simbólicos da época de lidar com "
        "ambiguidade e escala. O segundo inverno (1987-1993) coincidiu com a falência "
        "do mercado de sistemas especialistas. O renascimento atual, a partir dos "
        "anos 2000 e especialmente após 2012, deve-se à convergência de três fatores: "
        "disponibilidade de grandes volumes de dados (Big Data), aumento exponencial "
        "do poder computacional com GPUs, e desenvolvimento de algoritmos de "
        "aprendizado profundo mais eficazes (GÉRON, 2019)."
    )
    pdf.P(
        "As abordagens da IA podem ser organizadas em quatro paradigmas. O paradigma "
        "simbólico (ou GOFAI — Good Old-Fashioned AI) representa o conhecimento por "
        "regras lógicas explícitas e sistemas especialistas. O paradigma conexionista "
        "modela a inteligência como redes de neurônios artificiais interconectados, "
        "inspirados no sistema nervoso biológico. O paradigma evolucionário utiliza "
        "mecanismos de seleção natural para otimizar soluções. O paradigma estatístico "
        "— dominante na IA moderna — formula a aprendizagem como problemas de "
        "inferência e otimização sobre distribuições de probabilidade. O aprendizado "
        "de máquina (ML) pertence a esse último paradigma e é a tecnologia central "
        "deste trabalho."
    )
    pdf.P(
        "O aprendizado de máquina, como subárea da IA, é organizado em três grandes "
        "categorias conforme a natureza do feedback de aprendizagem. O aprendizado "
        "supervisionado utiliza pares (entrada, saída) rotulados para aprender uma "
        "função de mapeamento. O aprendizado não supervisionado identifica padrões "
        "em dados não rotulados, como clustering e redução de dimensionalidade. "
        "O aprendizado por reforço otimiza uma política de ações baseada em "
        "recompensas e penalidades recebidas do ambiente. Este trabalho concentra-se "
        "no aprendizado supervisionado, especificamente em problemas de classificação "
        "de imagens."
    )
    pdf.P(
        "No contexto do aprendizado supervisionado, Giraldi (2021) distingue ainda "
        "entre algoritmos paramétricos — que assumem uma forma funcional específica "
        "para o mapeamento (ex.: Regressão Logística, que assume uma fronteira de "
        "decisão linear) — e não paramétricos — cuja complexidade cresce com os dados "
        "(ex.: KNN, que armazena todos os pontos de treinamento). Cada categoria "
        "apresenta vantagens e desvantagens em termos de viés, variância, "
        "complexidade computacional e interpretabilidade."
    )

    pdf.SUB("1.2  Visão Computacional e Classificação de Imagens")
    pdf.P(
        "A Visão Computacional é o campo da IA dedicado ao desenvolvimento de "
        "sistemas capazes de interpretar e compreender imagens e vídeos digitais. "
        "Uma imagem digital pode ser representada matematicamente como uma função "
        "I: Z² → R (escala de cinza) ou I: Z² → R³ (colorida), onde cada ponto "
        "(i,j) do domínio corresponde a um pixel com intensidade ou vetor de cores. "
        "A classificação de imagens é o problema de atribuir a uma imagem I uma "
        "categoria c pertencente a um conjunto discreto de classes C = {c1,...,cK}."
    )
    pdf.P(
        "O desafio fundamental da classificação de imagens é a disparidade entre "
        "a representação bruta — um array numérico de pixels — e a representação "
        "semântica — o conceito que a imagem representa. Um cachorro fotografado "
        "de frente, de lado, à noite ou sob neve gera arrays de pixels radicalmente "
        "diferentes, mas deve ser classificado como 'cachorro' em todos os casos. "
        "Esse problema de invariância a transformações (translação, rotação, escala, "
        "iluminação) é o que torna a classificação de imagens genuinamente desafiadora."
    )
    pdf.P(
        "As abordagens para classificação de imagens evoluíram de descritores manuais "
        "de features — como o Histograma de Gradientes Orientados (HOG), descrito na "
        "Seção 1.11, e o SIFT (Scale-Invariant Feature Transform) — para arquiteturas "
        "de aprendizado profundo que aprendem automaticamente representações "
        "hierárquicas. Ambas as abordagens são implementadas neste trabalho: HOG como "
        "extrator de features para os classificadores clássicos, e EfficientNet-B0 "
        "como rede convolucional com aprendizado automático de representações."
    )
    pdf.P(
        "O pipeline típico de classificação de imagens por aprendizado supervisionado "
        "compreende as seguintes etapas: (1) coleta e rotulagem do dataset; "
        "(2) pré-processamento (normalização, redimensionamento, augmentation); "
        "(3) extração de features (manual ou automática); (4) treinamento do "
        "classificador; (5) avaliação em dados de teste; e (6) inferência em "
        "novos exemplos. O sistema desenvolvido neste trabalho implementa e "
        "automatiza todas essas etapas para múltiplos algoritmos simultâneos."
    )

    pdf.SUB("1.3  Aprendizado de Máquina Supervisionado")
    pdf.P(
        "O aprendizado supervisionado é formalizado como o problema de aprender uma "
        "função h: X → Y (hipótese) a partir de um conjunto de treinamento "
        "D = {(x1,y1),...,(xn,yn)}, onde xi pertence ao espaço de entrada X e "
        "yi pertence ao espaço de saída Y. O objetivo é que a hipótese h generalize "
        "bem para exemplos não vistos durante o treinamento, minimizando o risco "
        "esperado (erro de generalização):"
    )
    pdf.QUO(
        "R(h) = E_{(x,y)~P}[L(h(x), y)]"
    )
    pdf.P(
        "onde L é a função de perda e P é a distribuição de probabilidade "
        "desconhecida sobre X x Y. Como P não é conhecida, utiliza-se o risco "
        "empírico (training error) como substituto:"
    )
    pdf.QUO(
        "R_emp(h) = (1/n) * sum_{i=1}^{n} L(h(xi), yi)"
    )
    pdf.P(
        "O princípio de minimização do risco empírico (ERM) consiste em encontrar a "
        "hipótese h* que minimiza R_emp sobre um espaço de hipóteses H. O problema "
        "fundamental é que minimizar R_emp não garante minimizar R(h), especialmente "
        "quando H é muito expressivo — configurando o fenômeno de overfitting."
    )

    pdf.SSUB("1.3.1  O Dilema Viés-Variância")
    pdf.P(
        "O erro esperado de generalização de um classificador pode ser decomposto "
        "em três componentes fundamentais (GÉRON, 2019; GIRALDI, 2021):"
    )
    pdf.QUO(
        "Erro(x) = Vies^2 + Variancia + Ruido_irredutivel\n\n"
        "Vies = |E[h(x)] - f(x)|      (erro sistematico)\n"
        "Variancia = E[(h(x) - E[h(x)])^2]   (sensibilidade ao dataset)\n"
        "Ruido = sigma^2              (irreducivel, inerente aos dados)"
    )
    pdf.P(
        "O viés mede o quanto o modelo é sistematicamente errado: um classificador "
        "linear aplicado a dados não-lineares terá alto viés independente do dataset. "
        "A variância mede a sensibilidade do modelo às flutuações do dataset de "
        "treinamento: um modelo muito complexo treinado em amostras diferentes pode "
        "produzir predições muito distintas. O ruído irredutível é inerente aos dados "
        "e não pode ser eliminado por nenhum algoritmo."
    )
    pdf.P(
        "O dilema (trade-off) viés-variância implica que reduzir um dos componentes "
        "tipicamente aumenta o outro. Modelos simples (ex.: Regressão Logística em "
        "dados não-lineares) têm alto viés e baixa variância. Modelos complexos "
        "(ex.: KNN com K=1, árvores de decisão profundas) têm baixo viés e alta "
        "variância. O objetivo da regularização e da validação cruzada é encontrar "
        "o modelo com complexidade ideal que minimiza a soma dos três componentes "
        "no conjunto de validação."
    )

    pdf.SSUB("1.3.2  Aprendizado Generalizado e Regularização")
    pdf.P(
        "Para controlar o overfitting, diversas técnicas de regularização são "
        "empregadas. A regularização L2 (Ridge) adiciona ao critério de otimização "
        "um termo proporcional à norma quadrática dos parâmetros: "
        "L_reg = L + lambda||w||^2, penalizando parâmetros grandes e induzindo "
        "soluções mais suaves. A regularização L1 (Lasso) utiliza a norma L1, "
        "promovendo esparsidade nos parâmetros. O parâmetro C no SVM é o inverso "
        "do coeficiente de regularização L2 — C pequeno equivale a regularização "
        "forte. O KNN controla a complexidade via K: K grande equivale a maior "
        "suavização (regularização implícita)."
    )
    pdf.P(
        "A Teoria de Vapnik-Chervonenkis (VC) fornece o arcabouço teórico para "
        "limitar o risco de generalização. A VC dimension (dimensão VC) mede a "
        "capacidade expressiva de um espaço de hipóteses H. Para H com dimensão "
        "VC finita d, com probabilidade 1-delta sobre a escolha do dataset:"
    )
    pdf.QUO(
        "R(h) <= R_emp(h) + sqrt( (1/n) * (d*ln(2n/d) + ln(1/delta)) )"
    )
    pdf.P(
        "Esse limite (bound de generalização) justifica que algoritmos com menor "
        "dimensão VC tendem a generalizar melhor para um dado tamanho de dataset. "
        "O SVM maximiza a margem exatamente para minimizar a dimensão VC efetiva, "
        "fundamentando teoricamente sua capacidade de generalização."
    )

    pdf.SSUB("1.3.3  Validação Cruzada Estratificada")
    pdf.P(
        "A validação cruzada k-fold estratificada (StratifiedKFold) é o protocolo "
        "padrão para estimativa imparcial do desempenho e seleção de hiperparâmetros. "
        "O conjunto D é particionado em v dobras D1,...,Dv mutuamente exclusivas, "
        "mantendo em cada dobra a mesma proporção de classes do conjunto original "
        "(estratificação). Para cada dobra i:"
    )
    pdf.QUO(
        "M_i = train(D \\ D_i)          (modelo treinado sem a dobra i)\n"
        "Acc_i = evaluate(M_i, D_i)   (avaliado na dobra i)\n"
        "Acc_CV = (1/v) * sum_{i=1}^{v} Acc_i"
    )
    pdf.P(
        "As vantagens sobre a simples divisão treino/teste são: (1) todos os dados "
        "são usados tanto para treinamento quanto para avaliação; (2) a estimativa "
        "é menos dependente de uma única partição aleatória; (3) fornece medida de "
        "variabilidade via desvio padrão entre dobras. Para v=10 (10-fold), que é "
        "o protocolo adotado neste trabalho como métrica principal, o bias da "
        "estimativa é pequeno e a variância é controlada (GÉRON, 2019). O desvio "
        "padrão entre dobras é tão informativo quanto a média: alta variância entre "
        "dobras indica que o desempenho do modelo depende fortemente da partição "
        "dos dados, sinalizando dataset pequeno ou fronteiras de decisão instáveis."
    )

def cap1_knn(pdf):
    """1.4 KNN completo"""
    pdf.np()
    pdf.SUB("1.4  Algoritmo K-Nearest Neighbors (KNN)")
    pdf.P(
        "O algoritmo K-Nearest Neighbors (KNN) foi proposto independentemente por "
        "Evelyn Fix e Joseph Hodges em 1951 em relatório técnico para a Força Aérea "
        "dos EUA e posteriormente formalizado por Cover e Hart em 1967 no artigo "
        "'Nearest Neighbor Pattern Classification', publicado no IEEE Transactions "
        "on Information Theory. Sua premissa central é intuitivamente simples: "
        "amostras com atributos similares tendem a pertencer à mesma classe. "
        "Operacionalmente, para classificar um novo ponto de consulta xq, o "
        "algoritmo identifica os K pontos de treinamento mais próximos de xq "
        "segundo uma métrica de distância e atribui a xq a classe mais frequente "
        "nessa vizinhança (COVER; HART, 1967)."
    )
    pdf.SSUB("1.4.1  Formulação Matemática Formal")
    pdf.P(
        "Dado um conjunto de treinamento D = {(x1,y1),...,(xn,yn)}, onde "
        "xi pertence a R^d e yi pertence a {c1,...,cK}, define-se a vizinhança "
        "N_K(xq) como o conjunto dos K índices i cujos xi são mais próximos de xq "
        "segundo a métrica de distância adotada:"
    )
    pdf.QUO(
        "N_K(xq) = { i_1,...,i_K }  tal que  d(x_{i_j}, xq) <= d(x_i, xq)\n"
        "                             para todo i fora de N_K(xq)"
    )
    pdf.P(
        "A regra de decisão do KNN é a votação majoritária sobre a vizinhança:"
    )
    pdf.QUO(
        "y_hat_q = argmax_{c in C}  sum_{i in N_K(xq)} 1[yi = c]"
    )
    pdf.P(
        "Para classificação binária (C = {0,1}), a regra simplifica a:"
    )
    pdf.QUO(
        "y_hat_q = 1,  se  sum_{i in N_K(xq)} yi > K/2\n"
        "y_hat_q = 0,  caso contrario"
    )
    pdf.P(
        "Para K ímpar (como K=29 adotado neste trabalho), empates são impossíveis "
        "na classificação binária. O modelo não possui fase de treinamento no sentido "
        "paramétrico: todo o conjunto D é armazenado integralmente e utilizado na "
        "predição, classificando o KNN como algoritmo lazy (preguiçoso) ou "
        "instance-based (baseado em instâncias) por Géron (2019). O custo "
        "computacional de predição é O(n*d) por ponto de consulta — linear no "
        "tamanho do dataset — o que pode ser limitante para conjuntos muito grandes."
    )
    pdf.SSUB("1.4.2  Métricas de Distância: Família de Minkowski")
    pdf.P(
        "A qualidade das vizinhanças — e portanto da classificação — depende "
        "diretamente da métrica de distância utilizada. A família de métricas de "
        "Minkowski fornece uma generalização unificada:"
    )
    pdf.QUO(
        "d_p(x,z) = ( sum_{j=1}^{d} |xj - zj|^p )^(1/p)   para p >= 1"
    )
    pdf.P(
        "Os quatro casos especiais mais empregados em aprendizado de máquina são:"
    )
    pdf.TABLE(
        "Quadro 1.1 – Métricas de distância da família de Minkowski",
        ["Métrica","p","Fórmula","Quando usar"],
        [
            ["Manhattan","1","sum|xj-zj|","Dados esparsos, menos sensível a outliers"],
            ["Euclidiana","2","sqrt(sum(xj-zj)^2)","Dados contínuos normalizados (padrão)"],
            ["Chebyshev","inf","max_j|xj-zj|","Quando um atributo domina"],
            ["Minkowski","p","(sum|xj-zj|^p)^(1/p)","Generalização paramétrica"],
        ],
        cw=[30,12,52,66], fsz=9
    )
    pdf.SRC("Fonte: Elaborado pelo autor com base em Géron (2019).")
    pdf.P(
        "A distância Euclidiana (p=2) é o padrão do KNeighborsClassifier do "
        "scikit-learn e foi adotada neste trabalho. Geometricamente, corresponde "
        "ao comprimento da reta entre dois pontos no espaço d-dimensional. A "
        "distância de Manhattan (p=1) soma as diferenças absolutas dimensão a "
        "dimensão, sendo menos sensível a valores extremos em uma única dimensão. "
        "A distância de Chebyshev (p->inf) considera apenas a dimensão com maior "
        "diferença absoluta — adequada quando um único atributo é determinante para "
        "a similaridade. Para os dados clínicos numéricos e contínuos do Cleveland "
        "dataset, devidamente normalizados, a distância Euclidiana é a escolha "
        "convencional e teoricamente justificada."
    )
    pdf.SSUB("1.4.3  Importância da Normalização (Padronização Z-score)")
    pdf.P(
        "Por basear toda a decisão em distâncias, o KNN é extremamente sensível "
        "à escala dos atributos. Considere dois atributos do Cleveland dataset: "
        "o colesterol sérico (chol), que varia tipicamente entre 150 e 350 mg/dl, "
        "e o indicador binário de angina por exercício (exang), que assume apenas "
        "os valores 0 ou 1. Sem normalização, a contribuição desses dois atributos "
        "para a distância Euclidiana seria:"
    )
    pdf.QUO(
        "d(x,z)^2 = (chol_x - chol_z)^2 + (exang_x - exang_z)^2 + ...\n"
        "         = (por ex. 200)^2     +  (por ex. 1)^2         + ...\n"
        "         = 40000               +  1                      + ..."
    )
    pdf.P(
        "O atributo colesterol domina completamente a distância, tornando o atributo "
        "exang clinicamente irrelevante para a definição das vizinhanças — ainda que "
        "seja um preditor importante de doença cardíaca. Géron (2019) enfatiza que "
        "a normalização é etapa obrigatória para algoritmos baseados em distância."
    )
    pdf.P(
        "A Padronização Z-score (StandardScaler do scikit-learn) transforma cada "
        "atributo j de forma que a distribuição resultante tenha média zero e desvio "
        "padrão unitário:"
    )
    pdf.QUO(
        "z_{ij} = (x_{ij} - x_bar_j) / sigma_j\n\n"
        "onde  x_bar_j = (1/n_train) * sum_{i=1}^{n_train} x_{ij}\n"
        "e    sigma_j  = sqrt( (1/n_train) * sum_{i=1}^{n_train} (x_{ij} - x_bar_j)^2 )"
    )
    pdf.P(
        "Os parâmetros x_bar_j e sigma_j são estimados EXCLUSIVAMENTE sobre o "
        "conjunto de treinamento e depois aplicados ao conjunto de teste. Essa "
        "separação é essencial para prevenir data leakage: se os parâmetros fossem "
        "calculados sobre todo o dataset, as estatísticas de teste contaminam o "
        "pré-processamento, produzindo estimativas de desempenho artificialmente "
        "otimistas que não refletem o desempenho real em produção."
    )
    pdf.SSUB("1.4.4  O Hiperparâmetro K e o Trade-off Viés-Variância")
    pdf.P(
        "O valor de K controla o compromisso fundamental do KNN entre viés e "
        "variância. A análise das fronteiras de decisão ilustra o impacto de K:"
    )
    pdf.P(
        "K=1 (vizinho mais próximo): cada ponto de treinamento define sua própria "
        "região de Voronoi. A fronteira de decisão é altamente irregular, "
        "contornando cada ponto individualmente. O modelo memoriza perfeitamente "
        "o conjunto de treinamento (acurácia treino = 100%) mas generaliza mal. "
        "O erro de viés é zero (para qualquer função aprendível) mas a variância "
        "é máxima. Na análise paramétrica deste trabalho, K=1 obteve acurácia "
        "média de apenas 76,61% com variabilidade de 0,0851 — o pior resultado."
    )
    pdf.P(
        "K=n (todos os vizinhos): a predição é sempre a classe majoritária do "
        "dataset inteiro, independente de x. A fronteira de decisão é trivial — "
        "uma constante. Alto viés (ignora toda a estrutura local dos dados) mas "
        "variância zero (a predição não muda com o dataset). Inútil para "
        "classificação prática."
    )
    pdf.P(
        "K ótimo: equilibra os dois componentes. Para o Cleveland dataset, K=29 "
        "representa uma vizinhança suficientemente grande para suavizar o ruído "
        "local (reduzindo variância) sem abraçar regiões tão amplas que ignorem a "
        "estrutura local dos dados (mantendo viés controlado). A escolha via "
        "GridSearchCV com validação cruzada estratificada é a abordagem correta e "
        "foi a adotada neste trabalho."
    )
    pdf.P(
        "A fórmula de decomposição do erro esperado para o classificador KNN "
        "em classificação binária (Cover; Hart, 1967) é:"
    )
    pdf.QUO(
        "E[erro(xq)] ~= 2 * P_Bayes(xq) * (1 - P_Bayes(xq))  quando n -> inf, K -> inf, K/n -> 0\n\n"
        "onde P_Bayes(xq) = P(y=1|xq) eh a probabilidade de Bayes (erro irredutivel)\n"
        "Este resultado prova que, assintoticamente, o erro do KNN eh no maximo\n"
        "o DOBRO do erro de Bayes — cota fundamental para qualquer classificador."
    )
    pdf.SSUB("1.4.5  Seleção Automática de K: GridSearchCV")
    pdf.P(
        "A seleção do K ótimo por validação cruzada é formulada como:"
    )
    pdf.QUO(
        "K* = argmax_{k in {1,...,K_max}}  (1/v) * sum_{i=1}^{v} Acc(k, Dobra_i)"
    )
    pdf.P(
        "onde K_max define o intervalo de busca e v é o número de dobras de "
        "validação cruzada. No scikit-learn, isso é implementado por GridSearchCV "
        "com estimator=KNeighborsClassifier(), param_grid={'n_neighbors': range(1,21)}, "
        "cv=StratifiedKFold(5) e scoring='accuracy'. O processamento paralelo via "
        "n_jobs=-1 utiliza todos os núcleos da CPU disponíveis."
    )
    pdf.P(
        "Na análise paramétrica sistemática conduzida neste trabalho, o intervalo "
        "foi expandido para K in {1,3,5,...,49} (25 valores ímpares) cruzados com "
        "v in {5, 10, 15, 20} dobras, totalizando 100 combinações e mais de 2.000 "
        "execuções de avaliação. O critério de seleção adotou múltiplos critérios "
        "simultâneos: (1) acurácia média consolidada nas 4 configurações de CV; "
        "(2) AUC-ROC médio; (3) variabilidade CV (desvio padrão entre dobras); "
        "(4) estabilidade entre configurações de CV; (5) posicionamento no "
        "trade-off viés-variância."
    )
    pdf.SSUB("1.4.6  Limitações do KNN")
    pdf.P(
        "Apesar da simplicidade e transparência, o KNN apresenta limitações "
        "relevantes: (1) Custo de predição O(n*d): cresce linearmente com o "
        "tamanho do dataset e número de features — impraticável para n > 10^6; "
        "(2) Maldição da dimensionalidade: em espaços de alta dimensão (d >> 1), "
        "todos os pontos tornam-se igualmente distantes, degradando a qualidade "
        "das vizinhanças; (3) Sensibilidade ao ruído: atributos irrelevantes ou "
        "ruidosos distorcem as distâncias, impactando as vizinhanças; (4) Memória: "
        "o modelo armazena todo o dataset de treinamento, demandando memória "
        "proporcional a n. Estruturas de dados como KD-trees e Ball-trees (usadas "
        "pelo scikit-learn) reduzem o custo de busca para O(log n) em baixas "
        "dimensões, mas perdem eficiência em dimensões altas."
    )

def cap1_svm(pdf):
    """1.5 SVM completo"""
    pdf.np()
    pdf.SUB("1.5  Support Vector Machine (SVM)")
    pdf.P(
        "O Support Vector Machine (SVM) representa uma das contribuições mais "
        "elegantes da teoria de aprendizado de máquina. Introduzido por Boser, "
        "Guyon e Vapnik (1992) na forma com kernel e consolidado por Cortes e "
        "Vapnik (1995) com a incorporação das margens suaves, o SVM formula o "
        "problema de classificação como um problema de otimização convexa com "
        "sólidas garantias teóricas de generalização derivadas da teoria de "
        "Vapnik-Chervonenkis (VC). Diferente do KNN, que toma decisões baseadas "
        "em vizinhança local, o SVM constrói uma representação global da fronteira "
        "de decisão definida por um subconjunto mínimo de amostras de treinamento — "
        "os vetores de suporte."
    )
    pdf.SSUB("1.5.1  Formulação Primal de Margem Rígida")
    pdf.P(
        "Para dados linearmente separáveis, dado um conjunto de treinamento "
        "D = {(x1,y1),...,(xn,yn)} com xi pertence a R^d e yi pertence a {-1,+1}, "
        "um hiperplano de separação em R^d é definido por:"
    )
    pdf.QUO(
        "f(x) = w^T*x + b = 0\n"
        "onde w pertence a R^d (vetor normal ao hiperplano) e b pertence a R (vies)"
    )
    pdf.P(
        "A margem geométrica entre as classes é a distância perpendicular entre os "
        "dois hiperplanos de suporte paralelos:"
    )
    pdf.QUO(
        "Hiperplano positivo:  w^T*xi + b = +1   (para yi = +1)\n"
        "Hiperplano negativo:  w^T*xi + b = -1   (para yi = -1)\n"
        "Margem = 2 / ||w||"
    )
    pdf.P(
        "Maximizar a margem equivale a minimizar ||w||, ou de forma equivalente, "
        "minimizar (1/2)||w||^2 (por conveniência matemática). O problema primal "
        "de margem rígida é:"
    )
    pdf.QUO(
        "min_{w,b}    (1/2)||w||^2\n"
        "sujeito a:   yi*(w^T*xi + b) >= 1,   para todo i = 1,...,n"
    )
    pdf.P(
        "Este é um problema de programação quadrática (QP) convexo, com solução "
        "única e global garantida pela convexidade do objetivo e linearidade das "
        "restrições. A convexidade do SVM é uma propriedade crucial: diferente de "
        "redes neurais com múltiplos mínimos locais, o SVM tem solução ótima global "
        "garantida para qualquer dataset."
    )
    pdf.SSUB("1.5.2  Vetores de Suporte e Condições KKT")
    pdf.P(
        "A solução do problema primal é caracterizada pelas condições de "
        "Karush-Kuhn-Tucker (KKT). Introduzindo multiplicadores de Lagrange "
        "alpha_i >= 0 para cada restrição:"
    )
    pdf.QUO(
        "L(w,b,alpha) = (1/2)||w||^2 - sum_{i=1}^{n} alpha_i * [yi*(w^T*xi + b) - 1]"
    )
    pdf.P(
        "As condições de estacionaridade de KKT fornecem:"
    )
    pdf.QUO(
        "(dL/dw = 0)  =>  w = sum_{i=1}^{n} alpha_i * yi * xi\n"
        "(dL/db = 0)  =>  sum_{i=1}^{n} alpha_i * yi = 0\n"
        "Complementaridade:  alpha_i * [yi*(w^T*xi + b) - 1] = 0"
    )
    pdf.P(
        "A condição de complementaridade KKT é a chave para entender os vetores "
        "de suporte: apenas os pontos que satisfazem a restrição COM IGUALDADE "
        "(yi*(w^T*xi+b) = 1) têm alpha_i > 0. Todos os demais pontos têm "
        "alpha_i = 0 e NÃO INFLUENCIAM a solução. Esses pontos com alpha_i > 0 "
        "são os vetores de suporte — tipicamente apenas 10-20% do dataset. "
        "Essa propriedade de esparsidade confere ao SVM robustez a outliers: "
        "pontos distantes da fronteira não afetam o hiperplano ótimo."
    )
    pdf.P(
        "O vetor de pesos ótimo é expresso APENAS em termos dos vetores de suporte:"
    )
    pdf.QUO(
        "w* = sum_{i: alpha_i > 0} alpha_i * yi * xi"
    )
    pdf.SSUB("1.5.3  Formulação Dual de Lagrange")
    pdf.P(
        "Substituindo as condições KKT no Lagrangiano, obtém-se o problema dual:"
    )
    pdf.QUO(
        "max_{alpha}  sum_i alpha_i - (1/2)*sum_i sum_j alpha_i*alpha_j*yi*yj*xi^T*xj\n"
        "sujeito a:   sum_i alpha_i*yi = 0\n"
        "             alpha_i >= 0,   para todo i"
    )
    pdf.P(
        "A formulação dual apresenta duas vantagens fundamentais: (1) o problema "
        "cresce com o número de amostras n, não com a dimensionalidade d dos "
        "atributos — vantajoso quando d >> n; (2) os produtos internos xi^T*xj "
        "podem ser substituídos por funções de kernel K(xi,xj) = phi(xi)^T*phi(xj), "
        "permitindo classificação não-linear sem calcular explicitamente a "
        "transformação phi (o kernel trick)."
    )
    pdf.SSUB("1.5.4  Formulação de Margem Suave: O Parâmetro C")
    pdf.P(
        "Para dados reais raramente linearmente separáveis, Cortes e Vapnik (1995) "
        "introduziram variáveis de folga xi_i >= 0 que permitem que alguns pontos "
        "violem a margem, a um custo proporcional ao parâmetro C:"
    )
    pdf.QUO(
        "min_{w,b,xi}    (1/2)||w||^2 + C * sum_{i=1}^{n} xi_i\n"
        "sujeito a:   yi*(w^T*xi + b) >= 1 - xi_i\n"
        "             xi_i >= 0,   para todo i"
    )
    pdf.P(
        "O hiperparâmetro C > 0 controla o equilíbrio entre maximização da margem "
        "e penalidade por violações:"
    )
    pdf.TABLE(
        "Quadro 1.2 – Impacto do parâmetro C no SVM",
        ["C","Margem","Tolerância","Comportamento","Risco"],
        [
            ["Pequeno (0.1)","Larga","Alta (aceita erros)","Forte regularização","Underfitting"],
            ["Médio (1.0)","Média","Moderada","Equilíbrio","—"],
            ["Grande (100)","Estreita","Baixa (força acertos)","Fraca regularização","Overfitting"],
        ],
        cw=[25,22,35,45,33], fsz=9
    )
    pdf.SRC("Fonte: Elaborado pelo autor com base em Cortes e Vapnik (1995).")
    pdf.P(
        "Para o Cleveland Heart Disease Dataset, o GridSearchCV identificou C=0,1 "
        "como valor ótimo — o menor valor na grade testada. Isso indica que o dataset "
        "beneficia-se de forte regularização, o que é clinicamente interpretável: "
        "as distribuições dos 13 atributos clínicos para pacientes saudáveis e "
        "doentes apresentam sobreposição natural em diversas dimensões (por ex., "
        "frequência cardíaca máxima pode ser alta em jovens saudáveis e em certos "
        "perfis de cardiopatas), e forçar uma fronteira rígida causaria overfitting."
    )
    pdf.SSUB("1.5.5  O Kernel Trick e Funções de Kernel")
    pdf.P(
        "Para dados não linearmente separáveis no espaço original R^d, o SVM aplica "
        "uma transformação implícita phi: R^d -> H para um espaço de Hilbert H de "
        "maior (possivelmente infinita) dimensão, onde a separabilidade linear se "
        "torna possível. O kernel trick (Boser; Guyon; Vapnik, 1992) evita o "
        "cálculo explícito de phi, substituindo os produtos internos na formulação "
        "dual por uma função de kernel:"
    )
    pdf.QUO(
        "K(xi, xj) = phi(xi)^T * phi(xj)"
    )
    pdf.P(
        "Para que K seja um kernel válido (Teorema de Mercer), K deve ser uma "
        "função semidefinida positiva: para qualquer conjunto de pontos x1,...,xn, "
        "a matriz de Gram G com G_{ij} = K(xi,xj) deve ser semidefinida positiva. "
        "As três funções de kernel avaliadas neste trabalho são:"
    )
    pdf.SSUB("1.5.5.1  Kernel Linear")
    pdf.P(
        "K_lin(xi,xj) = xi^T * xj. Não realiza nenhuma transformação: "
        "o SVM linear maximiza a margem no espaço original R^d. Interpretável "
        "(w define a importância de cada atributo), eficiente computacionalmente "
        "e recomendado quando n << d ou quando os dados são aproximadamente "
        "linearmente separáveis. No experimento, obteve 81,00% de acurácia CV."
    )
    pdf.SSUB("1.5.5.2  Kernel Polinomial")
    pdf.P(
        "K_poly(xi,xj) = (gamma * xi^T*xj + r)^d, onde d é o grau polinomial, "
        "gamma controla a escala e r é o termo independente. Captura interações "
        "entre atributos de até ordem d. Para o Cleveland dataset, o kernel "
        "polinomial obteve 81,00% — equivalente ao linear, sugerindo que as "
        "interações polinomiais não adicionam discriminabilidade relevante."
    )
    pdf.SSUB("1.5.5.3  Kernel RBF (Radial Basis Function)")
    pdf.P(
        "K_RBF(xi,xj) = exp(-gamma * ||xi - xj||^2), onde gamma > 0 controla a "
        "largura da gaussiana. O kernel RBF corresponde implicitamente a um "
        "mapeamento phi para um espaço de DIMENSÃO INFINITA, demonstrado pela "
        "expansão em série de Taylor de exp():"
    )
    pdf.QUO(
        "exp(-gamma*||x-z||^2) = sum_{k=0}^{inf} (gamma^k / k!) * <phi_k(x), phi_k(z)>"
    )
    pdf.P(
        "Geometricamente, K_RBF(xi,xj) mede a similaridade entre xi e xj: vale "
        "1 quando xi=xj (pontos idênticos) e decai para 0 quando "
        "||xi-xj|| -> inf (pontos muito distintos). O parâmetro gamma controla "
        "a velocidade de decaimento:"
    )
    pdf.TABLE(
        "Quadro 1.3 – Efeito do parâmetro gamma no Kernel RBF",
        ["gamma","Gaussiana","Influencia de cada ponto","Fronteira","Risco"],
        [
            ["Grande","Estreita","So vizinhos imediatos","Irregular (local)","Overfitting"],
            ["Otimo","Media","Equilibrada","Suave e discriminativa","—"],
            ["Pequeno","Larga","Grande regiao","Muito suave","Underfitting"],
        ],
        cw=[25,23,40,40,32], fsz=9
    )
    pdf.SRC("Fonte: Elaborado pelo autor.")
    pdf.P(
        "No scikit-learn, gamma='scale' calcula automaticamente: "
        "gamma = 1 / (n_features * Var(X_train)), tornando o parâmetro adaptativo "
        "à variância dos dados padronizados. Para o Cleveland dataset com 13 atributos "
        "padronizados (variância unitária), gamma='scale' = 1/13 ≈ 0,077. "
        "Essa configuração foi selecionada como ótima pelo GridSearchCV e obteve "
        "82,27% de acurácia CV — superando linear e polinomial (81,00%)."
    )
    pdf.SSUB("1.5.6  Algoritmo SMO (Sequential Minimal Optimization)")
    pdf.P(
        "A resolução do problema dual do SVM é realizada pelo algoritmo SMO "
        "(Sequential Minimal Optimization), proposto por Platt em 1998 e "
        "implementado internamente pelo LibSVM (utilizado pelo scikit-learn). "
        "O SMO decompõe o problema QP de tamanho n em subproblemas mínimos de "
        "tamanho 2, selecionando iterativamente o par de multiplicadores "
        "(alpha_i, alpha_j) que maior violação das condições KKT representa, "
        "e otimizando-os analiticamente. O algoritmo converge quando todas as "
        "condições KKT são satisfeitas dentro de uma tolerância epsilon."
    )
    pdf.P(
        "A complexidade do SVM é O(n^2) para o treinamento via SMO no caso médio, "
        "podendo chegar a O(n^3) no pior caso. Em contraste, a predição é O(n_sv * d), "
        "onde n_sv << n é o número de vetores de suporte — tornando o SVM "
        "tipicamente mais eficiente que o KNN na fase de inferência para datasets "
        "grandes. Para o Cleveland dataset com 297 amostras, o treinamento leva "
        "fracção de segundo."
    )
    pdf.SSUB("1.5.7  Probabilidades Calibradas no SVM")
    pdf.P(
        "O SVM clássico produz scores de decisão f(x) = w^T*phi(x)+b mas não "
        "estimativas de probabilidade diretamente. Para os métodos Soft Voting e "
        "Stacking, que requerem P(y=c|x), o scikit-learn utiliza calibração de "
        "Platt (probability=True): ajusta uma Regressão Logística sobre os scores "
        "de decisão em validação cruzada, transformando-os em probabilidades "
        "calibradas. Esse procedimento adiciona overhead computacional mas é "
        "necessário para os métodos probabilísticos de ensemble."
    )
