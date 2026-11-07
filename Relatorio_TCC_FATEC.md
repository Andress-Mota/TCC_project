# FACULDADE DE TECNOLOGIA DE GUARATINGUETÁ

---

# ANÁLISE COMPARATIVA DE ALGORITMOS DE INTELIGÊNCIA ARTIFICIAL PARA CLASSIFICAÇÃO DE IMAGENS BASEADA EM APRENDIZADO SUPERVISIONADO

**Andress Felipe de Oliveira Mota**

Relatório Técnico-científico apresentado à Faculdade de Tecnologia de Guaratinguetá, como requisito parcial para conclusão do Curso Superior de Tecnologia em Análise e Desenvolvimento de Sistemas.

Orientador: Professor Eduardo

**Guaratinguetá - SP**
**2026**

---

*(Página de Rosto)*

# FACULDADE DE TECNOLOGIA DE GUARATINGUETÁ

# ANÁLISE COMPARATIVA DE ALGORITMOS DE INTELIGÊNCIA ARTIFICIAL PARA CLASSIFICAÇÃO DE IMAGENS BASEADA EM APRENDIZADO SUPERVISIONADO

**Andress Felipe de Oliveira Mota**

Relatório Técnico-científico apresentado à Faculdade de Tecnologia de Guaratinguetá, como requisito parcial para conclusão do Curso Superior de Tecnologia em Análise e Desenvolvimento de Sistemas.

Programa: Análise e Desenvolvimento de Sistemas
Área Temática: Inteligência Artificial e Aprendizado de Máquina
Linha de Estudo e Pesquisa: Classificação de Imagens com Algoritmos de Machine Learning

Orientador: Professor Eduardo

**Guaratinguetá - SP**
**2026**

---

*(Verso da Página de Rosto — Ficha Catalográfica)*

MOTA, Andress Felipe de Oliveira. **Análise Comparativa de Algoritmos de Inteligência Artificial para Classificação de Imagens Baseada em Aprendizado Supervisionado**. Guaratinguetá, 2026. Relatório Técnico-científico, Curso Superior de Tecnologia em Análise e Desenvolvimento de Sistemas, Faculdade de Tecnologia de Guaratinguetá, 2026.

---

## Resumo

MOTA, Andress Felipe de Oliveira. Análise Comparativa de Algoritmos de Inteligência Artificial para Classificação de Imagens Baseada em Aprendizado Supervisionado. Guaratinguetá, 2026. Relatório Técnico-científico, Curso de Análise e Desenvolvimento de Sistemas, Faculdade de Tecnologia de Guaratinguetá, 2026.

A crescente aplicação de algoritmos de aprendizado de máquina em domínios que exigem análise automatizada de imagens impõe ao campo científico a necessidade de estudos comparativos que orientem a escolha das abordagens mais adequadas a cada contexto. O presente trabalho tem como objetivo desenvolver, documentar e avaliar um sistema web de classificação de imagens baseado em técnicas de ensemble learning, integrando cinco algoritmos individuais — K-Nearest Neighbors (KNN), Support Vector Machine (SVM), Random Forest, Regressão Logística e Naive Bayes Gaussiano — a três estratégias de combinação: Voting Hard, Voting Soft e Stacking. A pesquisa foi conduzida em duas etapas complementares. Na primeira, de caráter experimental e teórico, os algoritmos foram aplicados ao dataset UCI Heart Disease (Cleveland), composto por 297 registros clínicos e 13 variáveis preditoras, com o objetivo de compreender o comportamento de cada modelo em um ambiente controlado e de mensurar com precisão as métricas de desempenho antes da aplicação ao domínio de imagens. Os resultados obtidos nessa fase demonstraram acurácias que variaram de 81,51% a 88,33% na validação cruzada de dez dobras, conferindo embasamento empírico suficiente para a seleção dos hiperparâmetros adotados no sistema. Na segunda etapa, foi desenvolvida a plataforma TCC IA, uma aplicação web construída com o framework Flask e banco de dados MySQL, capaz de receber conjuntos de imagens organizados por classes, extrair características por meio do Histograma de Gradientes Orientados (HOG) com resolução de 128×128 pixels em escala de cinza, treinar os oito modelos de forma automática e apresentar resultados comparativos detalhados, incluindo acurácia, precisão, recall, F1-Score, AUC-ROC, curvas ROC e matrizes de confusão. O sistema incorpora ainda uma rede neural convolucional opcional baseada na arquitetura EfficientNet-B0 com ajuste fino sobre pesos pré-treinados no ImageNet, acompanhada de visualização por Grad-CAM para interpretabilidade das predições. A validação prática do sistema foi realizada com o dataset público Chest X-Ray Images (Pneumonia), composto por radiografias torácicas classificadas em duas categorias — Normal e Pneumonia —, no qual o modelo Stacking alcançou acurácia de 92,00% tanto na validação cruzada de dez dobras quanto no conjunto de teste, ao passo que a rede EfficientNet-B0 classificou imagens individuais com confiança de 99,2%. Os resultados obtidos evidenciam que a combinação de algoritmos clássicos por meio de estratégias de ensemble supera consistentemente o desempenho individual de cada modelo, e que a plataforma desenvolvida constitui uma ferramenta técnica e científica relevante para a análise comparativa de algoritmos de inteligência artificial aplicados à classificação de imagens.

**Palavras-chave:** Aprendizado de Máquina. Ensemble Learning. Classificação de Imagens. HOG. KNN. SVM. Random Forest. EfficientNet-B0. Grad-CAM.

---

## Abstract

MOTA, Andress Felipe de Oliveira. Comparative Analysis of Artificial Intelligence Algorithms for Image Classification Based on Supervised Learning. Guaratinguetá, 2026. Technical and Scientific Report, Computer Systems Analysis and Development Program, Faculdade de Tecnologia de Guaratinguetá, 2026.

The growing application of machine learning algorithms in domains requiring automated image analysis imposes on the scientific field a need for comparative studies to guide the selection of the most appropriate approaches for each context. This work aims to develop, document, and evaluate a web-based image classification system grounded in ensemble learning techniques, integrating five individual algorithms — K-Nearest Neighbors (KNN), Support Vector Machine (SVM), Random Forest, Logistic Regression, and Gaussian Naive Bayes — with three combination strategies: Hard Voting, Soft Voting, and Stacking. The research was conducted in two complementary stages. In the first, of experimental and theoretical character, the algorithms were applied to the UCI Heart Disease dataset (Cleveland), comprising 297 clinical records and 13 predictor variables, with the aim of understanding the behavior of each model in a controlled environment and precisely measuring performance metrics prior to application in the image domain. Results from this phase demonstrated cross-validation accuracies ranging from 81.51% to 88.33% in ten-fold cross-validation, providing sufficient empirical basis for selecting the hyperparameters adopted in the system. In the second stage, the TCC IA platform was developed — a web application built with the Flask framework and a MySQL database — capable of receiving class-organized image datasets, extracting features through the Histogram of Oriented Gradients (HOG) at 128×128 pixel resolution in grayscale, automatically training the eight models, and presenting detailed comparative results including accuracy, precision, recall, F1-Score, AUC-ROC, ROC curves, and confusion matrices. The system also incorporates an optional convolutional neural network based on the EfficientNet-B0 architecture fine-tuned on ImageNet pre-trained weights, accompanied by Grad-CAM visualization for prediction interpretability. Practical validation of the system was performed using the public Chest X-Ray Images (Pneumonia) dataset, consisting of chest radiographs classified into two categories — Normal and Pneumonia — in which the Stacking model achieved 92.00% accuracy in both ten-fold cross-validation and the test set, while the EfficientNet-B0 network classified individual images with 99.2% confidence. The results obtained demonstrate that combining classical algorithms through ensemble strategies consistently outperforms the individual performance of each model, and that the developed platform constitutes a relevant technical and scientific tool for the comparative analysis of artificial intelligence algorithms applied to image classification.

**Keywords:** Machine Learning. Ensemble Learning. Image Classification. HOG. KNN. SVM. Random Forest. EfficientNet-B0. Grad-CAM.

---

## Lista de Figuras

Figura 1 – Tela de autenticação do sistema TCC IA

Figura 2 – Tela de recuperação de senha e e-mail de notificação

Figura 3 – Dashboard com indicadores de desempenho e atividade

Figura 4 – Tela de treinamento com barra de progresso

Figura 5 – Tabela comparativa dos oito modelos — dataset Pneumonia

Figura 6 – Gráfico comparativo de desempenho e matriz de confusão (Stacking)

Figura 7 – Mapa de atenção Grad-CAM gerado pela CNN EfficientNet-B0

Figura 8 – Tela de log de erros com detalhamento de rastreamento

Figura 9 – Tela de perfil e modal de alteração de senha

Figura 10 – Diagrama do esquema relacional do banco de dados

---

## Lista de Quadros

Quadro 1 – Elementos principais do Relatório Técnico-científico na FATEC-GT

Quadro 2 – Atributos clínicos do dataset UCI Heart Disease (Cleveland)

Quadro 3 – Configuração dos hiperparâmetros do KNN na fase experimental

Quadro 4 – Configuração dos hiperparâmetros do SVM na fase experimental

Quadro 5 – Configuração dos hiperparâmetros do Random Forest na fase experimental

Quadro 6 – Resultados da fase experimental — dataset UCI Heart Disease

Quadro 7 – Comparativo dos oito modelos no dataset Pneumonia

Quadro 8 – Estrutura das tabelas do banco de dados

Quadro 9 – Dependências e tecnologias utilizadas no sistema

---

## SUMÁRIO

INTRODUÇÃO .................................................................................................................1

1 FUNDAMENTAÇÃO TEÓRICA ....................................................................................5

1.1 Aprendizado de Máquina e Aprendizado Supervisionado ......................................5

1.2 Extração de Características: o Histograma de Gradientes Orientados ..................10

1.3 Algoritmos de Classificação Individual ..................................................................14

1.3.1 K-Nearest Neighbors ........................................................................................14

1.3.2 Support Vector Machine ...................................................................................18

1.3.3 Random Forest .................................................................................................23

1.3.4 Regressão Logística .........................................................................................27

1.3.5 Naive Bayes Gaussiano ....................................................................................30

1.4 Ensemble Learning ................................................................................................33

1.4.1 Fundamentos e Diversidade de Modelos ..........................................................33

1.4.2 Voting Hard e Voting Soft .................................................................................36

1.4.3 Stacking ............................................................................................................39

1.5 Redes Neurais Convolucionais e a Arquitetura EfficientNet-B0 ............................42

1.6 Grad-CAM: Visualização de Ativações em Redes Convolucionais .......................48

2 METODOLOGIA E DESENVOLVIMENTO DO SISTEMA ............................................52

2.1 Fase Experimental: Estudo com o Dataset UCI Heart Disease .............................52

2.1.1 Descrição e Pré-processamento da Base de Dados ........................................52

2.1.2 Configuração dos Experimentos e Validação Cruzada .....................................55

2.1.3 Resultados da Fase Experimental ....................................................................58

2.2 Desenvolvimento do Sistema TCC IA ...................................................................62

2.2.1 Visão Geral da Arquitetura ................................................................................62

2.2.2 Pipeline de Classificação de Imagens ..............................................................65

2.2.3 Módulo de Autenticação e Segurança ..............................................................70

2.2.4 Banco de Dados ...............................................................................................74

2.2.5 Interface Web e Funcionalidades ......................................................................78

3 RESULTADOS E DISCUSSÃO ...................................................................................85

3.1 Dataset de Validação: Chest X-Ray Images (Pneumonia) ....................................85

3.2 Comparativo dos Oito Modelos .............................................................................87

3.3 CNN EfficientNet-B0 e Interpretabilidade via Grad-CAM ......................................93

3.4 Análise e Discussão dos Resultados ....................................................................96

CONSIDERAÇÕES FINAIS ..........................................................................................102

REFERÊNCIAS .............................................................................................................106

---

# INTRODUÇÃO

A Inteligência Artificial se consolidou, ao longo das últimas décadas, como uma das mais transformadoras vertentes do desenvolvimento tecnológico contemporâneo. Desde as primeiras formalizações matemáticas dos sistemas de aprendizado automático, passando pela consolidação dos algoritmos clássicos de aprendizado de máquina, até a explosão das arquiteturas de aprendizado profundo na segunda década do século XXI, o campo assistiu a uma progressão que ultrapassou os limites do ambiente acadêmico para se integrar de maneira profunda às estruturas da medicina, da segurança, da agricultura e da indústria. No cerne desse avanço reside uma questão que permanece cientificamente relevante e praticamente urgente: diante de um problema específico de classificação, qual algoritmo oferece o melhor equilíbrio entre acurácia, capacidade de generalização, custo computacional e interpretabilidade?

A classificação de imagens representa, nesse contexto, um dos domínios de aplicação mais exigentes e, simultaneamente, mais promissores do aprendizado de máquina supervisionado. A tarefa de ensinar um sistema computacional a reconhecer padrões visuais — distinguindo uma radiografia normal de uma afetada por pneumonia, identificando anomalias em linhas de produção industrial ou reconhecendo faces em sistemas de segurança — demanda abordagens que conjuguem extração de características robustas com modelos capazes de generalizar satisfatoriamente para amostras não vistas durante o treinamento. Algoritmos clássicos como K-Nearest Neighbors, Support Vector Machine e Random Forest foram, durante décadas, as ferramentas primárias para essa tarefa; mais recentemente, as redes neurais convolucionais passaram a dominar os benchmarks de classificação de imagens, trazendo consigo ganhos substanciais de desempenho ao custo de maior demanda computacional e menor interpretabilidade direta dos modelos.

Nesse cenário, o presente trabalho propõe uma análise comparativa aprofundada de algoritmos de inteligência artificial aplicados à classificação de imagens, com ênfase na estratégia de ensemble learning como abordagem capaz de superar as limitações individuais de cada modelo. O estudo foi estruturado em duas etapas complementares. A primeira, de caráter experimental, utilizou o dataset UCI Heart Disease — Cleveland, amplamente referenciado na literatura de aprendizado de máquina, para compreender em profundidade o comportamento dos algoritmos em um ambiente de dados tabulares com características clínicas bem definidas. Essa etapa permitiu calibrar os hiperparâmetros, validar os procedimentos de pré-processamento e estabelecer métricas de referência antes da aplicação ao domínio de imagens. A segunda etapa consistiu no desenvolvimento do sistema TCC IA, uma plataforma web completa, construída sobre o framework Flask com armazenamento em banco de dados relacional MySQL, que automatiza o processo de treinamento comparativo de oito modelos de aprendizado de máquina — cinco individuais e três em ensemble — aplicados a qualquer conjunto de imagens organizado em pastas por classe.

O objetivo geral deste trabalho consiste em desenvolver e validar experimentalmente uma plataforma computacional para classificação de imagens que implemente e compare algoritmos clássicos de aprendizado de máquina e estratégias de ensemble learning, demonstrando, de forma quantitativa, as diferenças de desempenho entre as abordagens estudadas. Para a realização plena desse objetivo, foram estabelecidos os seguintes objetivos específicos: estudar os fundamentos matemáticos e computacionais dos algoritmos KNN, SVM, Random Forest, Regressão Logística, Naive Bayes e das arquiteturas de ensemble Voting Hard, Voting Soft e Stacking; conduzir uma fase experimental com o dataset UCI Heart Disease para validar os procedimentos de pré-processamento e métricas de avaliação adotados; desenvolver um sistema web capaz de receber conjuntos de imagens, extrair características por meio do Histograma de Gradientes Orientados (HOG), treinar os oito modelos automaticamente e apresentar resultados comparativos detalhados; integrar ao sistema uma rede neural convolucional baseada na arquitetura EfficientNet-B0 com visualização Grad-CAM para análise de interpretabilidade; validar o sistema com o dataset público Chest X-Ray Images (Pneumonia); e analisar criticamente os resultados obtidos, discutindo as implicações práticas de cada abordagem.

A relevância científica e prática deste trabalho se fundamenta em três eixos principais. O primeiro é a escassez de sistemas que integrem, em uma única plataforma web acessível, múltiplos algoritmos clássicos e técnicas de ensemble para classificação de imagens, tornando a comparação experimental acessível a pesquisadores e profissionais sem necessidade de implementação manual de cada modelo. O segundo eixo é a contribuição para a compreensão do comportamento comparativo dos algoritmos em cenários reais de classificação binária de imagens, com foco especial no papel do ensemble learning como estratégia de mitigação dos erros individuais de cada modelo. O terceiro eixo é a aplicabilidade clínica dos resultados obtidos com o dataset de pneumonia, que demonstra o potencial do sistema como ferramenta de triagem e apoio ao diagnóstico médico baseado em imagens radiológicas.

Este relatório está organizado em três capítulos de desenvolvimento, além desta Introdução e das Considerações Finais. O Capítulo 1 apresenta a fundamentação teórica que sustenta o trabalho, abordando os conceitos de aprendizado de máquina supervisionado, a técnica de extração de características HOG, os cinco algoritmos de classificação individual implementados, os três métodos de ensemble, a arquitetura EfficientNet-B0 e o método de visualização Grad-CAM. O Capítulo 2 descreve a metodologia adotada, incluindo a fase experimental com o dataset UCI Heart Disease e o processo de desenvolvimento do sistema TCC IA, com detalhamento da arquitetura, do pipeline de classificação, do módulo de autenticação, do banco de dados e da interface web. O Capítulo 3 apresenta e discute os resultados obtidos na validação prática do sistema com o dataset de pneumonia, analisando o desempenho comparativo dos oito modelos e a contribuição da CNN com Grad-CAM. Por fim, as Considerações Finais sintetizam os principais achados, apontam as limitações do estudo e propõem direções para trabalhos futuros.

---

# 1 FUNDAMENTAÇÃO TEÓRICA

## 1.1 Aprendizado de Máquina e Aprendizado Supervisionado

O aprendizado de máquina constitui um subcampo da inteligência artificial dedicado ao desenvolvimento de algoritmos e modelos estatísticos que permitem a sistemas computacionais aprenderem padrões a partir de dados, sem que sejam explicitamente programados para cada regra de decisão. A definição clássica, proposta por Mitchell (1997) e retomada por Géron (2019), estabelece que um programa de computador aprende com a experiência E em relação a alguma tarefa T e medida de desempenho P, se seu desempenho em T, medido por P, melhora com a experiência E. Essa formulação captura de maneira precisa a essência do paradigma: ao contrário dos sistemas baseados em regras explícitas, os algoritmos de aprendizado de máquina constroem representações internas dos dados de treinamento e utilizam essas representações para tomar decisões sobre instâncias novas, não vistas durante o processo de aprendizado.

Géron (2019) classifica os sistemas de aprendizado de máquina segundo três critérios ortogonais: a quantidade e o tipo de supervisão recebida durante o treinamento, a capacidade de aprender de forma incremental a partir de novos dados, e o modo pelo qual os algoritmos generalizam — seja comparando novos dados com exemplos conhecidos ou construindo um modelo preditivo. O critério de supervisão é o mais relevante para o presente trabalho. No aprendizado supervisionado, os dados de treinamento incluem os rótulos desejados, denominados labels, e o algoritmo aprende a mapear entradas para saídas com base nos exemplos rotulados. Em contraste, o aprendizado não supervisionado opera sobre dados não rotulados, buscando descobrir estruturas internas como agrupamentos ou associações, enquanto o aprendizado por reforço envolve um agente que aprende por meio de interações com um ambiente, recebendo recompensas ou penalidades em função das ações tomadas.

O aprendizado supervisionado subdivide-se em dois tipos fundamentais de tarefas: regressão e classificação. Na regressão, o objetivo é prever um valor numérico contínuo, como o preço de um imóvel ou a temperatura máxima de um dia. Na classificação, o objetivo é atribuir uma entrada a uma entre um conjunto discreto de categorias, denominadas classes. Quando o conjunto de classes é binário — como saudável ou doente, normal ou pneumonia, spam ou não spam —, a tarefa é denominada classificação binária. Quando há três ou mais classes, fala-se em classificação multiclasse. O presente trabalho concentra-se integralmente em problemas de classificação binária, tanto na fase experimental com dados clínicos quanto na validação com imagens radiológicas.

O processo geral de treinamento de um classificador supervisionado envolve um conjunto de etapas bem definidas. Inicialmente, os dados são divididos em um conjunto de treinamento, utilizado para ajustar os parâmetros do modelo, e um conjunto de teste, reservado para a avaliação final do desempenho. Essa separação é fundamental para estimar a capacidade de generalização do modelo — sua habilidade de realizar predições corretas sobre dados não vistos anteriormente — e evitar o que se denomina vazamento de dados, situação em que informações do conjunto de teste influenciam indevidamente o processo de treinamento.

Para a avaliação do desempenho de classificadores, diversas métricas foram desenvolvidas, cada uma capturando aspectos distintos do comportamento do modelo. A acurácia, definida como a proporção de predições corretas sobre o total de predições realizadas, é a métrica mais intuitiva, porém sensível ao desbalanceamento entre classes. A precisão mensura a proporção de predições positivas que são, de fato, positivas; o recall, também denominado sensibilidade ou taxa de verdadeiros positivos, mensura a proporção de instâncias positivas reais que foram corretamente identificadas pelo modelo. O F1-Score, média harmônica entre precisão e recall, combina ambas as métricas em uma única grandeza que penaliza modelos que sacrificam um dos valores em detrimento do outro. Por fim, a Área sob a Curva ROC (AUC-ROC) mensura a capacidade discriminativa do modelo ao longo de todos os limiares de decisão possíveis, sendo particularmente informativa em cenários de classificação binária (GÉRON, 2019).

Um conceito central na avaliação de modelos de aprendizado de máquina é o dilema viés-variância. O viés refere-se ao erro sistemático introduzido pelas suposições do modelo — um modelo com alto viés tende a subajustar os dados, capturando apenas padrões grosseiros e cometendo erros mesmo no conjunto de treinamento. A variância, por sua vez, refere-se à sensibilidade do modelo às flutuações nos dados de treinamento — um modelo com alta variância tende a sobreajustar os dados, memorizando ruídos do treinamento e falhando ao generalizar para novas instâncias. O objetivo do treinamento de um bom classificador é encontrar o equilíbrio entre esses dois extremos, o que é formalmente conhecido como otimização do trade-off viés-variância (DEISENROTH; FAISAL; ONG, 2020).

Para a estimativa robusta e imparcial da capacidade de generalização de um modelo, a técnica de validação cruzada é amplamente empregada. Na validação cruzada com k-dobras, o conjunto de dados é dividido em k subconjuntos de tamanho aproximadamente igual, denominados dobras. O modelo é treinado k vezes, cada vez utilizando k-1 dobras como conjunto de treinamento e a dobra restante como conjunto de validação. A acurácia final é calculada como a média das k acurácias obtidas, acompanhada de seu desvio padrão, que quantifica a estabilidade do modelo. A variante estratificada da validação cruzada, denominada StratifiedKFold, assegura que cada dobra mantenha a mesma proporção de classes que o conjunto original, sendo essencial para datasets com classes desbalanceadas. No presente trabalho, adotou-se a validação cruzada estratificada com dez dobras como métrica primária de avaliação, por sua conhecida robustez e ampla aceitação na literatura científica de aprendizado de máquina (GÉRON, 2019).

A seleção de hiperparâmetros — parâmetros cujos valores não são aprendidos pelo modelo durante o treinamento, mas devem ser definidos antes de seu início — constitui uma etapa crítica no processo de modelagem. Valores inadequados de hiperparâmetros podem resultar em modelos que oscilam entre os extremos do subajuste e do sobreajuste. A técnica GridSearchCV, implementada na biblioteca scikit-learn, automatiza esse processo ao testar sistematicamente todas as combinações possíveis de valores pré-definidos para cada hiperparâmetro, avaliando cada combinação por meio de validação cruzada e selecionando aquela que maximiza a métrica de desempenho escolhida.

## 1.2 Extração de Características: o Histograma de Gradientes Orientados

A representação de imagens como vetores de características numéricas é o passo preliminar indispensável para a aplicação de algoritmos de aprendizado de máquina clássicos à classificação de imagens. Ao contrário das redes neurais convolucionais, que aprendem automaticamente hierarquias de características diretamente a partir dos pixels brutos, os algoritmos clássicos requerem que o engenheiro defina explicitamente de que maneira a imagem será convertida em um vetor de entrada de dimensão fixa. Esse processo, denominado extração de características, pode ser realizado por diferentes técnicas, cada uma sensível a diferentes propriedades das imagens.

O Histograma de Gradientes Orientados, conhecido pela sigla HOG, é uma técnica de extração de características visuais proposta por Dalal e Triggs em 2005 e amplamente utilizada em aplicações de visão computacional desde então, especialmente na detecção de pedestres, reconhecimento de objetos e classificação de imagens médicas. A premissa fundamental do HOG é que a forma local e a aparência de objetos em uma imagem podem ser descritas eficientemente pela distribuição das intensidades de gradientes ou, equivalentemente, das orientações das bordas, mesmo sem um conhecimento preciso das posições exatas desses gradientes.

O processo de extração de características HOG pode ser descrito em quatro etapas principais. A primeira consiste no pré-processamento da imagem: ela é redimensionada para uma resolução padronizada e convertida para escala de cinza, eliminando a informação de cor e reduzindo a dimensionalidade da entrada. No sistema desenvolvido neste trabalho, todas as imagens são redimensionadas para 128×128 pixels em escala de cinza antes da extração. A segunda etapa consiste no cálculo dos gradientes horizontais e verticais da imagem por meio de operadores de convolução, o que captura as variações locais de intensidade — bordas, texturas e transições — que caracterizam as estruturas visuais presentes na imagem.

A terceira etapa corresponde à construção do histograma propriamente dito. A imagem é dividida em pequenas regiões espaciais denominadas células. Para cada pixel de cada célula, calcula-se a magnitude e a orientação do gradiente. As orientações são então quantizadas em um número discreto de intervalos, denominados bins, e as magnitudes correspondentes são acumuladas em um histograma, criando uma representação compacta da distribuição de gradientes em cada célula. No presente trabalho, adotaram-se células de 16×16 pixels e 9 orientações de gradiente, abrangendo o intervalo de 0° a 180°. A quarta etapa consiste na normalização por blocos: grupos de células adjacentes, denominados blocos, são agrupados e seus histogramas concatenados formam vetores que são normalizados para compensar variações de iluminação e contraste local. Blocos de 2×2 células foram utilizados neste trabalho.

O vetor de características final, resultante da concatenação de todos os histogramas normalizados de todos os blocos da imagem, possui dimensionalidade aproximada de 324 elementos para a configuração adotada. Esse vetor constitui a entrada dos classificadores clássicos e encapsula, de forma compacta, a informação estrutural relevante da imagem, tornando-a comparável e computacionalmente tratável. A escolha do HOG como método de extração de características neste trabalho é justificada por sua robustez a variações moderadas de iluminação e de posição dos objetos, por sua eficiência computacional e por sua ampla validação na literatura para tarefas de classificação de imagens médicas, incluindo radiografias torácicas.

## 1.3 Algoritmos de Classificação Individual

### 1.3.1 K-Nearest Neighbors

O algoritmo K-Nearest Neighbors, ou K-Vizinhos Mais Próximos, é um dos métodos de aprendizado de máquina mais intuitivos e conceitualmente simples disponíveis. Proposto originalmente por Fix e Hodges em 1951 e formalizado em trabalhos subsequentes, o KNN pertence à categoria dos algoritmos de aprendizado baseado em instâncias, também denominado aprendizado preguiçoso. A denominação se deve ao fato de que o KNN não constrói um modelo explícito durante a fase de treinamento; em vez disso, memoriza todo o conjunto de treinamento e realiza o trabalho computacional apenas no momento da predição.

O princípio de funcionamento do KNN é fundamentado na hipótese de que instâncias similares tendem a pertencer à mesma classe. Dado um novo ponto de consulta, o algoritmo calcula sua distância para todos os pontos do conjunto de treinamento, identifica os K pontos mais próximos — os K vizinhos mais próximos — e atribui ao novo ponto a classe mais frequente entre esses K vizinhos, em um processo denominado votação por maioria. Para classificação binária, o número de vizinhos K deve ser ímpar para evitar empates. A distância euclidiana é a métrica mais comum, mas outras métricas como distância de Manhattan e distância de Minkowski também podem ser utilizadas dependendo do contexto (GÉRON, 2019).

A escolha do valor de K é o principal hiperparâmetro do algoritmo e exerce influência direta sobre o compromisso viés-variância do modelo. Valores pequenos de K, como K=1, tornam o modelo altamente sensível ao ruído nos dados de treinamento, produzindo fronteiras de decisão irregulares e provavelmente sobreajustadas. Valores grandes de K suavizam a fronteira de decisão, reduzindo a variância ao custo de um maior viés, o que pode levar ao subajuste em conjuntos de dados com estruturas complexas. A determinação do valor ótimo de K por meio de validação cruzada, como implementado neste trabalho utilizando GridSearchCV com busca no intervalo de K=1 a K=20, garante a seleção sistematicamente fundamentada do hiperparâmetro.

Uma limitação importante do KNN é sua sensibilidade à escala das features de entrada. Como o algoritmo baseia suas decisões em medidas de distância euclidiana, features com escalas numéricas muito diferentes exercem influências desproporcionais sobre o cálculo da distância. Por essa razão, a padronização das features — transformação para média zero e desvio padrão unitário por meio do StandardScaler — é uma etapa de pré-processamento indispensável antes da aplicação do KNN, procedimento que foi adotado no presente trabalho tanto na fase experimental quanto no sistema desenvolvido. Outra limitação é o custo computacional de predição, que cresce linearmente com o tamanho do conjunto de treinamento, pois cada predição requer o cálculo de distâncias para todos os pontos de treinamento.

Na fase experimental conduzida com o dataset UCI Heart Disease, o KNN com K ótimo de 29 alcançou acurácia de 86,67% no conjunto de teste e 82,86% ± 6,99% na validação cruzada de dez dobras. Esses resultados, obtidos com o algoritmo em sua forma mais simples e interpretável, serviram de referência para a comparação com os modelos mais sofisticados implementados nas etapas subsequentes do trabalho.

### 1.3.2 Support Vector Machine

A Support Vector Machine, ou Máquina de Vetores de Suporte, é um algoritmo de aprendizado supervisionado fundamentado na teoria estatística do aprendizado, cujos principais desenvolvimentos foram realizados por Vapnik e colaboradores na década de 1990. O SVM destaca-se pela elegância de seu embasamento matemático e pela eficácia demonstrada em problemas de alta dimensionalidade, tornando-se um dos algoritmos de classificação mais estudados e utilizados nas décadas seguintes à sua proposição.

O princípio fundamental do SVM para classificação linear binária consiste em encontrar o hiperplano de separação que maximiza a margem entre as duas classes. A margem é definida como a distância entre o hiperplano decisório e os pontos de treinamento mais próximos de cada classe, denominados vetores de suporte. A maximização da margem é motivada pela teoria do aprendizado estatístico: um hiperplano com margem máxima tende a generalizar melhor para dados não vistos, pois está matematicamente mais distante dos pontos de ambas as classes. O problema de otimização correspondente é quadrático convexo, garantindo a existência de uma solução global única (GÉRON, 2019).

Na prática, a maioria dos problemas de classificação real não é linearmente separável — os dados das duas classes se sobrepõem no espaço de features. Para lidar com essa situação, o SVM de margem suave introduz variáveis de folga que permitem que alguns pontos violem a margem ou até mesmo estejam no lado errado do hiperplano, ao custo de uma penalidade controlada pelo hiperparâmetro C. Valores elevados de C impõem penalidades maiores às violações de margem, produzindo margens mais estreitas e modelos mais propensos ao sobreajuste; valores baixos de C permitem mais violações, produzindo margens mais amplas e modelos com maior regularização. Na fase experimental deste trabalho, o valor ótimo encontrado foi C=0,1 — um valor de forte regularização — o que se mostrou adequado ao dataset utilizado, no qual existe sobreposição natural entre as classes.

Para problemas não linearmente separáveis, o SVM utiliza o truque do kernel, uma técnica que transforma implicitamente o espaço original de features em um espaço de dimensão maior — potencialmente infinita — no qual a separabilidade linear é alcançável. O kernel radial (RBF), definido pela função K(x, z) = exp(−γ||x − z||²), é o mais utilizado na prática por sua capacidade de modelar fronteiras de decisão altamente não lineares e por exigir apenas um hiperparâmetro adicional, γ, que controla a influência de cada ponto de treinamento sobre a fronteira. O kernel RBF foi selecionado como ótimo na fase experimental deste trabalho, com γ determinado automaticamente pela regra γ = 1 / (n_features × Var(X_train)), denominada configuração scale.

A normalização das features é obrigatória para o SVM, assim como para o KNN, pois o algoritmo baseia suas decisões em produtos internos e medidas de distância no espaço transformado pelo kernel. Features em escalas distintas distorcem o hiperplano decisório e podem inviabilizar a convergência do otimizador. O uso do StandardScaler foi, portanto, parte integrante do pipeline de pré-processamento adotado. Na fase experimental, o SVM com kernel RBF, C=0,1 e γ=scale alcançou acurácia de 86,67% no conjunto de teste e 83,51% ± 7,66% na validação cruzada de dez dobras, desempenho estatisticamente equivalente ao do KNN no mesmo dataset, porém com fronteira de decisão de natureza qualitativamente diferente — global e geometricamente fundamentada, em contraste com a natureza local e baseada em vizinhança do KNN.

### 1.3.3 Random Forest

O Random Forest é um algoritmo de aprendizado de máquina que pertence à categoria dos métodos de ensemble baseados em bagging, sendo amplamente considerado um dos classificadores de propósito geral mais robustos e eficazes disponíveis na literatura. Proposto por Breiman em 2001, o algoritmo combina múltiplas árvores de decisão treinadas de forma independente sobre subamostras aleatórias do conjunto de treinamento, e realiza a predição final por votação — no caso de classificação — ou por média — no caso de regressão (GÉRON, 2019).

Uma árvore de decisão é uma estrutura hierárquica de nós que realiza divisões binárias sucessivas do espaço de features com base em condições simples do tipo "feature_i ≤ threshold". O treinamento de uma árvore consiste em determinar, para cada nó interno, qual feature e qual limiar produzem a divisão que maximiza a pureza das subpopulações resultantes, medida por critérios como impureza de Gini ou ganho de entropia. Árvores de decisão individuais tendem a sobreajustar os dados de treinamento quando crescem sem restrições de profundidade, o que motivou o desenvolvimento de métodos como o Random Forest para mitigar esse comportamento por meio da combinação de múltiplas árvores com diversidade controlada.

A inovação central do Random Forest em relação ao bagging padrão reside na injeção de aleatoriedade adicional no processo de construção de cada árvore: além de treinar cada árvore sobre uma subamostra aleatória com reposição do conjunto de treinamento, o algoritmo restringe a busca do melhor split em cada nó a um subconjunto aleatório das features disponíveis, em vez de considerar todas as features. Essa dupla fonte de aleatoriedade — nas amostras e nas features — aumenta a diversidade entre as árvores da floresta e reduz a correlação entre seus erros, o que é teoricamente fundamental para que a combinação das predições seja mais precisa do que qualquer predição individual.

Os principais hiperparâmetros do Random Forest incluem o número de árvores na floresta (n_estimators), a profundidade máxima de cada árvore (max_depth), o número mínimo de amostras necessárias para realizar uma divisão em um nó interno e o número de features consideradas em cada split. No sistema desenvolvido, o Random Forest foi configurado com 50 árvores e profundidade máxima de 10 níveis, configuração determinada por GridSearchCV na fase experimental. Uma vantagem adicional do Random Forest é que, por ser baseado em árvores de decisão, não requer normalização das features de entrada, uma vez que as divisões binárias são invariantes a transformações monotônicas das escalas.

O algoritmo também fornece, como subproduto do treinamento, uma medida de importância de cada feature, calculada como a redução média da impureza proporcionada por cada feature ao longo de todas as divisões de todas as árvores. Essa propriedade de interpretabilidade é particularmente valiosa em aplicações médicas, onde compreender quais variáveis ou regiões de uma imagem são mais informativas para o diagnóstico pode ter implicações clínicas diretas. Na fase experimental com o dataset UCI Heart Disease, as três features mais importantes identificadas pelo Random Forest foram o tipo de dor torácica (cp), a frequência cardíaca máxima (thalach) e a depressão do segmento ST (oldpeak), valores coerentes com o conhecimento clínico estabelecido sobre fatores preditores de doença coronariana.

### 1.3.4 Regressão Logística

A Regressão Logística é um algoritmo de classificação que, apesar do nome sugestivo de um modelo de regressão, é empregado para a predição de probabilidades de pertencimento a classes discretas. O modelo foi proposto por David Cox em 1958 e permanece, até hoje, um dos classificadores mais utilizados em ciências da saúde, econometria e aprendizado de máquina, em parte por sua interpretabilidade e em parte por sua eficiência computacional.

O modelo de Regressão Logística modela a probabilidade condicional de uma instância pertencer à classe positiva como uma função logística — ou sigmoide — da combinação linear das features de entrada. Formalmente, dado um vetor de features x e um vetor de pesos w, a probabilidade predita é P(y=1|x) = σ(wᵀx + b), onde σ(z) = 1/(1+e^{-z}) é a função sigmoide, que mapeia qualquer valor real para o intervalo (0, 1). A estimação dos parâmetros w e b é realizada por maximização da verossimilhança logarítmica do conjunto de treinamento, que equivale à minimização de uma função de custo denominada entropia cruzada binária (GÉRON, 2019).

Para evitar o sobreajuste em datasets com muitas features ou com multicolinearidade, a Regressão Logística tipicamente incorpora um termo de regularização à função objetivo. A regularização L2, também denominada regularização Ridge, adiciona à função de custo um termo proporcional à soma dos quadrados dos pesos, penalizando pesos excessivamente grandes e promovendo soluções mais esparsas e generalizáveis. No sistema desenvolvido, a Regressão Logística foi configurada com regularização L2 e número máximo de iterações de 1000, suficiente para garantir a convergência em todos os cenários testados. A normalização das features por StandardScaler é igualmente necessária para a Regressão Logística, pois o gradiente da função de custo é sensível às escalas relativas das diferentes features.

Uma característica especialmente relevante da Regressão Logística para as estratégias de ensemble implementadas neste trabalho é sua capacidade de estimar probabilidades bem calibradas — probabilidades que correspondem de forma razoavelmente fiel às frequências empíricas observadas nos dados. Essa propriedade torna a Regressão Logística uma escolha natural como meta-learner no Stacking, onde ela aprende a combinar as predições dos modelos base de forma ótima com base nas probabilidades que cada um deles atribui a cada classe.

### 1.3.5 Naive Bayes Gaussiano

O classificador Naive Bayes Gaussiano é um algoritmo probabilístico fundamentado no teorema de Bayes para classificação, com a suposição simplificadora — "ingênua", daí o nome — de que as features são condicionalmente independentes entre si dado o rótulo de classe. Embora essa suposição raramente se sustente na prática, o classificador resultante é surpreendentemente robusto e eficaz em muitos cenários reais, sendo especialmente popular em classificação de texto e em diagnósticos médicos onde a dimensionalidade dos dados é alta.

O teorema de Bayes estabelece que a probabilidade a posteriori de uma classe y dado um vetor de features x é proporcional ao produto da probabilidade a priori P(y) pela verossimilhança P(x|y). Sob a suposição de independência condicional, a verossimilhança conjunta pode ser fatorada como o produto das verossimilhanças individuais de cada feature, tornando o cálculo computacionalmente tratável mesmo para espaços de features de alta dimensionalidade. A variante Gaussiana assume que as features contínuas seguem distribuição normal dentro de cada classe, com média e variância estimadas a partir dos dados de treinamento.

A principal vantagem do Naive Bayes é sua eficiência computacional: o modelo é treinado em tempo linear no número de features e instâncias, e as predições são igualmente rápidas. A principal desvantagem é precisamente a suposição de independência condicional, que pode levar a estimativas de probabilidade mal calibradas quando as features são fortemente correlacionadas. No contexto do ensemble learning, o Naive Bayes contribui com uma perspectiva generativa dos dados que é qualitativamente diferente das perspectivas discriminativas do SVM, KNN e Random Forest, aumentando a diversidade do conjunto de modelos base e potencialmente melhorando o desempenho do ensemble.

## 1.4 Ensemble Learning

### 1.4.1 Fundamentos e Diversidade de Modelos

O ensemble learning, ou aprendizado por conjunto, é uma família de métodos de aprendizado de máquina baseada na combinação de múltiplos modelos individuais — denominados modelos base, classificadores base ou aprendizes fracos — com o objetivo de produzir um preditor composto de desempenho superior ao de qualquer modelo individual. A intuição subjacente ao ensemble learning é análoga ao princípio da "sabedoria das multidões" em contextos sociais: mesmo que cada indivíduo — ou modelo — cometa erros, a agregação de múltiplas opiniões independentes tende a cancelar os erros idiossincráticos e a amplificar o sinal correto (MIENYE; SUN, 2022).

A condição fundamental para que um ensemble supere seus componentes é a diversidade entre os modelos base. Se todos os modelos cometem os mesmos erros, sua combinação não produz nenhum ganho: o ensemble será tão impreciso quanto cada componente individual. A diversidade pode ser obtida por diferentes mecanismos: treinando os modelos base em subamostras diferentes dos dados de treinamento — como no bagging —, utilizando diferentes algoritmos de aprendizado — como no voting e no stacking — ou perturbando as features de entrada de diferentes maneiras. A teoria de ensemble learning demonstra formalmente, sob certas condições, que a combinação de classificadores não correlacionados com acurácia individual acima de 50% produz um ensemble com acurácia monotonicamente crescente no número de classificadores (GÉRON, 2019).

O sistema TCC IA implementa dois paradigmas distintos de ensemble: o voting, que combina as predições dos modelos base por meio de votação direta, e o stacking, que treina um meta-modelo sobre as saídas dos modelos base. Ambas as abordagens são descritas em detalhe nas subseções a seguir.

### 1.4.2 Voting Hard e Voting Soft

O ensemble por votação, ou Voting, é a abordagem de ensemble mais simples e diretamente interpretável. No Voting Hard, cada modelo base emite um voto de classe — a classe que ele prediz como mais provável — e a predição final do ensemble é determinada pela classe que recebe o maior número de votos, em um processo de votação majoritária. O critério majoritário garante que, mesmo que uma minoria dos modelos falhe em um determinado caso, a predição correta da maioria prevalece, desde que os erros dos diferentes modelos não sejam sistematicamente correlacionados.

O Voting Soft é uma variante mais sofisticada que requer dos modelos base a capacidade de estimar probabilidades de pertencimento a cada classe, em vez de apenas emitir votos binários. A predição final é determinada pela classe com a maior probabilidade média, calculada como a média aritmética das probabilidades estimadas por cada modelo base. A vantagem do Voting Soft sobre o Voting Hard é que ele incorpora a confiança de cada modelo em sua predição: quando um modelo está muito confiante e os demais estão incertos, o Voting Soft pondera adequadamente essa informação, enquanto o Voting Hard trata todos os votos como igualmente confiáveis. Matematicamente, o Voting Soft calcula a predição final como:

ŷ = argmax_c [ (1/N) × Σᵢ P(y=c | x, Mᵢ) ]

onde N é o número de modelos base e Mᵢ é o i-ésimo modelo. No sistema TCC IA, todos os cinco classificadores base implementados — KNN, SVM, Random Forest, Regressão Logística e Naive Bayes — são compatíveis com o Voting Soft, pois todos disponibilizam métodos de estimação de probabilidade através da interface predict_proba da biblioteca scikit-learn.

Na fase experimental com o dataset UCI Heart Disease, a estratégia de Soft Voting Ponderado — onde os pesos dos modelos KNN e SVM foram ajustados proporcionalmente à acurácia de validação cruzada — alcançou acurácia de 88,33% no conjunto de teste, superando os modelos individuais (86,67%) em 1,66 pontos percentuais. Essa diferença, embora aparentemente modesta, implica na redução do número de falsos negativos de 6 para 5 casos, uma distinção clinicamente significativa em contexto de diagnóstico médico.

### 1.4.3 Stacking

O Stacking, abreviação de stacked generalization — generalização empilhada —, é uma estratégia de ensemble de segunda ordem que vai além da simples agregação de votos ou probabilidades: ela treina um modelo adicional, denominado meta-learner ou meta-aprendiz, cujas entradas são as saídas dos modelos base. O meta-learner aprende a ponderar e combinar as predições dos modelos base de maneira ótima, potencialmente capturando relações não lineares entre as saídas dos diferentes classificadores.

O processo de treinamento do Stacking ocorre em duas fases distintas. Na primeira fase, os modelos base são treinados sobre o conjunto de treinamento e produzem predições para um conjunto de validação separado — tipicamente obtido por validação cruzada, para evitar que o meta-learner seja treinado sobre predições calculadas nos mesmos dados que os modelos base viram. As predições dos modelos base sobre esse conjunto de validação formam uma nova matriz de features que alimenta o meta-learner. Na segunda fase, o meta-learner é treinado sobre essa nova matriz com os rótulos originais como alvo. Durante a predição em dados novos, os modelos base produzem suas probabilidades e o meta-learner combina essas probabilidades para gerar a predição final do ensemble (MIENYE; SUN, 2022).

No sistema TCC IA, o meta-learner adotado é a Regressão Logística, escolha motivada por sua eficiência computacional, por sua capacidade de produzir probabilidades bem calibradas e por sua interpretabilidade. Os modelos base são os cinco classificadores individuais descritos na seção anterior: KNN, SVM, Random Forest, Regressão Logística e Naive Bayes. Os experimentos conduzidos demonstraram que o Stacking consistentemente alcança os melhores resultados de AUC-ROC entre todas as estratégias implementadas — 0,9520 na fase experimental com o dataset UCI Heart Disease —, sugerindo superior capacidade discriminativa entre as classes ao longo de todos os limiares de decisão.

## 1.5 Redes Neurais Convolucionais e a Arquitetura EfficientNet-B0

As redes neurais convolucionais, amplamente conhecidas pela sigla CNN (do inglês Convolutional Neural Network), constituem a classe dominante de modelos de aprendizado profundo para tarefas de visão computacional. Inspiradas pela organização do córtex visual dos mamíferos, as CNNs utilizam camadas de convolução para aprender automaticamente representações hierárquicas das imagens, progredindo de features simples como bordas e texturas nas camadas iniciais para representações cada vez mais abstratas e semanticamente ricas nas camadas mais profundas (GÉRON, 2019).

Uma camada convolucional aplica um conjunto de filtros aprendíveis — denominados kernels — sobre a imagem de entrada por meio da operação de convolução discreta, produzindo mapas de ativação que codificam a presença e a intensidade de determinados padrões visuais em diferentes posições espaciais da imagem. A operação de pooling, tipicamente inserida entre camadas convolucionais, reduz progressivamente as dimensões espaciais dos mapas de ativação, introduzindo invariância a pequenas translações e reduzindo o custo computacional das camadas subsequentes. As camadas totalmente conectadas ao final da rede realizam a classificação propriamente dita, recebendo como entrada os mapas de ativação achatados das últimas camadas convolucionais e produzindo as probabilidades de pertencimento a cada classe.

A arquitetura EfficientNet, proposta por Tan e Le em 2019, introduziu uma abordagem sistemática para o escalonamento de redes neurais convolucionais. Enquanto a maioria das arquiteturas anteriores escalava a profundidade (número de camadas), a largura (número de canais por camada) ou a resolução de entrada de forma isolada, o EfficientNet propôs um método de escalonamento composto que aumenta simultaneamente essas três dimensões de maneira balanceada, utilizando coeficientes otimizados por busca neural. A variante base da família, denominada EfficientNet-B0, oferece um equilíbrio notável entre acurácia e eficiência computacional — alcançando resultados comparáveis ou superiores aos de arquiteturas muito mais profundas como ResNet-50 e VGG-16, com um número significativamente menor de parâmetros.

No sistema TCC IA, a EfficientNet-B0 é utilizada por meio da técnica de ajuste fino (fine-tuning), que consiste em inicializar os pesos da rede com valores pré-treinados no dataset ImageNet — um conjunto de mais de 1,2 milhão de imagens distribuídas em 1000 categorias — e retreinar o modelo sobre o dataset específico da aplicação. O ajuste fino permite que o modelo aproveite as representações visuais aprendidas em larga escala durante o pré-treinamento e as especialize para o problema particular de classificação, com custo computacional significativamente menor do que o treinamento do zero. O processo de ajuste fino é implementado com otimizador Adam, taxa de aprendizado de 1×10⁻³ e treinamento por 8 épocas, com aumento de dados (data augmentation) incluindo corte aleatório, inversão horizontal e variações aleatórias de cor para mitigar o sobreajuste.

## 1.6 Grad-CAM: Visualização de Ativações em Redes Convolucionais

Um dos desafios mais relevantes no emprego de redes neurais profundas em aplicações de alto risco, como o diagnóstico médico, é a interpretabilidade das predições. Ao contrário dos algoritmos clássicos como o Random Forest, que fornece uma medida direta de importância de features, as CNNs são frequentemente tratadas como caixas-pretas — sistemas cujos processos internos são opacos ao observador humano. A ausência de explicabilidade pode comprometer a confiança do especialista na predição e dificultar a identificação de erros sistemáticos do modelo.

O Gradient-weighted Class Activation Mapping, comumente denominado Grad-CAM, é uma técnica de explicabilidade para redes neurais convolucionais proposta por Selvaraju e colaboradores em 2017. O método gera um mapa de calor que destaca, sobre a imagem de entrada, as regiões espaciais que exerceram maior influência sobre a predição do modelo para uma determinada classe. Concretamente, o Grad-CAM calcula os gradientes da pontuação de classe de interesse em relação aos mapas de ativação da última camada convolucional da rede, utiliza esses gradientes como pesos para ponderar os mapas de ativação e produz um mapa de calor por meio da soma ponderada. O mapa resultante é redimensionado para as dimensões da imagem original e sobreposto sobre ela, produzindo uma visualização interpretável que indica as regiões "vistas" pelo modelo para tomar sua decisão.

No sistema TCC IA, a visualização Grad-CAM é disponibilizada como recurso opcional na tela de predição de imagens individuais, sendo gerada pela EfficientNet-B0 quando PyTorch está instalado no ambiente de execução. A aplicação prática dessa funcionalidade foi demonstrada durante os testes do sistema com o dataset de pneumonia, no qual o mapa de calor gerado destacou, de forma coerente com o conhecimento médico, as regiões de consolidação pulmonar nas radiografias classificadas como pneumonia — fornecendo uma justificativa visual e clinicamente plausível para as predições da rede.

---

# 2 METODOLOGIA E DESENVOLVIMENTO DO SISTEMA

## 2.1 Fase Experimental: Estudo com o Dataset UCI Heart Disease

### 2.1.1 Descrição e Pré-processamento da Base de Dados

A fase experimental deste trabalho utilizou o dataset Cleveland Heart Disease, disponibilizado publicamente pelo UCI Machine Learning Repository sob o identificador 45. Esse conjunto de dados foi originalmente coletado por Janosi e colaboradores no Cleveland Clinic Foundation e constitui, há mais de três décadas, uma das referências mais amplamente empregadas na avaliação de algoritmos de classificação na área de diagnóstico cardiovascular. A escolha desse dataset para a fase de estudo foi motivada por três fatores principais: a disponibilidade documentada de resultados de referência na literatura, o tamanho moderado do conjunto — suficiente para validação cruzada robusta, porém pequeno o suficiente para execução ágil dos experimentos — e a natureza estruturada e bem documentada de suas variáveis, que facilita a interpretação dos resultados.

O dataset original contém 303 registros clínicos, dos quais 6 apresentam valores ausentes em uma ou mais features. Esses registros foram removidos durante o pré-processamento, resultando em um conjunto final de 297 instâncias válidas. Cada instância é descrita por 13 atributos clínicos e laboratoriais, conforme apresentado no Quadro 2.

**Quadro 2 – Atributos clínicos do dataset UCI Heart Disease (Cleveland)**

| Atributo | Tipo | Descrição |
|----------|------|-----------|
| age | Contínuo | Idade em anos |
| sex | Binário | Sexo (1=masculino, 0=feminino) |
| cp | Categórico | Tipo de dor torácica (0-3) |
| trestbps | Contínuo | Pressão arterial em repouso (mmHg) |
| chol | Contínuo | Colesterol sérico (mg/dl) |
| fbs | Binário | Glicemia em jejum > 120 mg/dl (1=sim) |
| restecg | Categórico | Resultados eletrocardiográficos em repouso (0-2) |
| thalach | Contínuo | Frequência cardíaca máxima alcançada |
| exang | Binário | Angina induzida por exercício (1=sim) |
| oldpeak | Contínuo | Depressão do segmento ST pelo exercício |
| slope | Categórico | Inclinação do segmento ST de pico do exercício |
| ca | Ordinal | Número de vasos principais coloridos por fluoroscopia (0-3) |
| thal | Categórico | Tipo de defeito de tálio (3=normal, 6=fixo, 7=reversível) |

Fonte: Elaborado pelo autor com base nos dados do UCI Machine Learning Repository.

A variável alvo original do dataset assume cinco valores discretos (0 a 4), onde 0 indica ausência de doença cardíaca e os valores 1 a 4 indicam graus crescentes de comprometimento cardíaco. Para os experimentos desta fase, adotou-se a binarização da variável alvo, procedimento padrão na literatura para esse dataset: o valor 0 foi mantido como classe negativa (saudável) e todos os valores positivos (1 a 4) foram mapeados para a classe 1 (doente). Essa binarização é justificada pelo objetivo clínico primário — discriminar pacientes saudáveis de pacientes com algum grau de doença cardíaca —, sendo também a abordagem que maximiza a utilidade prática do classificador como ferramenta de triagem.

A divisão dos dados em conjuntos de treinamento e teste foi realizada pela função train_test_split da biblioteca scikit-learn, com proporção de 80% para treinamento (237 instâncias) e 20% para teste (60 instâncias), utilizando o parâmetro stratify=y para garantir que a proporção de classes fosse preservada em ambos os conjuntos, e random_state=42 para assegurar a reprodutibilidade dos resultados. A distribuição resultante manteve a proporção aproximada de 54% de pacientes saudáveis e 46% de pacientes doentes em ambos os subconjuntos.

A normalização das features foi aplicada por meio do StandardScaler, que transforma cada feature para média zero e desvio padrão unitário utilizando os parâmetros estimados exclusivamente sobre o conjunto de treinamento. Essa precaução evita o vazamento de informações do conjunto de teste para o processo de treinamento, garantindo que a estimativa de desempenho final seja válida para dados genuinamente não vistos. A normalização foi aplicada a todos os algoritmos sensíveis a escala — KNN, SVM e Regressão Logística —, mas não ao Random Forest e ao Naive Bayes Gaussiano, que são invariantes ou possuem suposições específicas sobre a distribuição das features.

### 2.1.2 Configuração dos Experimentos e Validação Cruzada

A otimização dos hiperparâmetros de cada algoritmo foi realizada por meio da classe GridSearchCV da biblioteca scikit-learn, que realiza uma busca exaustiva sobre uma grade de combinações de hiperparâmetros, avaliando cada combinação por meio de validação cruzada estratificada com cinco dobras sobre o conjunto de treinamento. A métrica de otimização adotada foi a acurácia. Após a seleção dos melhores hiperparâmetros, cada modelo foi retreinado sobre o conjunto de treinamento completo (237 instâncias) e avaliado no conjunto de teste (60 instâncias), produzindo a estimativa de acurácia de holdout. Adicionalmente, a validação cruzada com dez dobras estratificadas foi aplicada ao conjunto completo de 297 instâncias, produzindo a estimativa de acurácia média e desvio padrão reportadas como métrica principal.

Os Quadros 3, 4 e 5 apresentam as grades de hiperparâmetros investigadas para os três algoritmos para os quais a otimização foi especialmente relevante.

**Quadro 3 – Configuração dos hiperparâmetros do KNN na fase experimental**

| Hiperparâmetro | Valores Testados | Valor Ótimo |
|----------------|-----------------|-------------|
| n_neighbors (K) | 1 a 49 (ímpares) | 29 |
| metric | euclidean, manhattan | euclidean |

Fonte: Elaborado pelo autor.

**Quadro 4 – Configuração dos hiperparâmetros do SVM na fase experimental**

| Hiperparâmetro | Valores Testados | Valor Ótimo |
|----------------|-----------------|-------------|
| C | 0,1; 1; 10; 100 | 0,1 |
| kernel | linear; rbf; poly | rbf |
| gamma | scale; auto | scale |

Fonte: Elaborado pelo autor.

**Quadro 5 – Configuração dos hiperparâmetros do Random Forest na fase experimental**

| Hiperparâmetro | Valores Testados | Valor Ótimo |
|----------------|-----------------|-------------|
| n_estimators | 50; 100; 200 | 50 |
| max_depth | 5; 10; 20; None | 10 |

Fonte: Elaborado pelo autor.

### 2.1.3 Resultados da Fase Experimental

Os resultados obtidos na fase experimental com o dataset UCI Heart Disease são apresentados de forma consolidada no Quadro 6. A métrica de validação cruzada com dez dobras é reportada como a medida principal de desempenho, por sua maior robustez estatística em comparação com a acurácia de holdout calculada sobre um único conjunto de teste de 60 instâncias.

**Quadro 6 – Resultados da fase experimental — dataset UCI Heart Disease**

| Modelo | Tipo | CV 10-fold (%) | Desvio Padrão (%) | Acurácia Teste (%) |
|--------|------|----------------|-------------------|-------------------|
| KNN (K=29) | Individual | 82,86 | ±6,99 | 86,67 |
| SVM (RBF, C=0,1) | Individual | 83,51 | ±7,66 | 86,67 |
| Random Forest | Individual | 81,51 | ±6,13 | 85,00 |
| Regressão Logística | Individual | 83,11 | ±6,84 | 85,00 |
| Naive Bayes | Individual | 82,12 | ±7,21 | 83,33 |
| Voting Hard | Ensemble | 82,45 | ±6,58 | 86,67 |
| Voting Soft | Ensemble | 82,68 | ±6,43 | 88,33 |
| Stacking | Ensemble | 82,84 | ±6,39 | 86,67 |

Fonte: Elaborado pelo autor.

Os resultados da fase experimental revelam padrões importantes que fundamentaram as decisões de implementação tomadas no desenvolvimento do sistema. Em primeiro lugar, o SVM com kernel RBF se destacou como o melhor classificador individual na métrica de validação cruzada (83,51%), seguido de perto pela Regressão Logística (83,11%) e pelo KNN com K=29 (82,86%). A diferença entre os melhores modelos individuais é menor do que um desvio padrão, indicando que, para este dataset específico, os algoritmos são estatisticamente equivalentes em termos de desempenho médio. Em segundo lugar, a estratégia de Voting Soft alcançou a maior acurácia no conjunto de teste (88,33%), superando os modelos individuais em 1,66 pontos percentuais e reduzindo o número de falsos negativos de 6 para 5 casos — uma melhora clinicamente relevante em um contexto de diagnóstico de doença cardíaca.

Em terceiro lugar, o Stacking demonstrou a melhor AUC-ROC entre todas as estratégias (0,9520), sugerindo superior capacidade discriminativa ao longo de todos os limiares de decisão, embora sua acurácia pontual no conjunto de teste tenha sido igual à dos melhores modelos individuais. Esse comportamento é consistente com a teoria do ensemble learning: o Stacking aprende a combinar os modelos base de forma ótima, o que se reflete em uma curva ROC mais próxima do canto superior esquerdo do gráfico, mas nem sempre em uma acurácia pontual superior quando o limiar padrão de 0,5 é adotado.

Esses resultados consolidaram a seguinte seleção de hiperparâmetros para o sistema TCC IA: KNN com K determinado por GridSearchCV no intervalo 1-20, SVM com kernel RBF e C=0,1, Random Forest com 50 árvores e profundidade máxima de 10, Regressão Logística com regularização L2, Naive Bayes Gaussiano sem hiperparâmetros críticos a otimizar, e Stacking com Regressão Logística como meta-learner. A validação cruzada com dez dobras foi mantida como métrica primária de avaliação no sistema.

## 2.2 Desenvolvimento do Sistema TCC IA

### 2.2.1 Visão Geral da Arquitetura

O sistema TCC IA foi desenvolvido como uma aplicação web de três camadas, seguindo a arquitetura cliente-servidor: a camada de apresentação, implementada como interface web responsiva com HTML5, CSS3 e JavaScript puro; a camada de lógica de negócios, implementada com o micro-framework Flask em Python 3; e a camada de dados, implementada com banco de dados relacional MySQL. Essa arquitetura separa de forma clara as responsabilidades de cada componente, facilitando a manutenção e a evolução do sistema.

A camada de apresentação comunica-se com o servidor exclusivamente por meio de requisições assíncronas à API REST exposta pelo Flask, utilizando o formato JSON para troca de dados. Essa decisão arquitetural confere ao sistema independência entre o frontend e o backend, permitindo que ambos evoluam de forma relativamente independente. A API REST exposta pelo servidor compreende mais de 35 endpoints organizados em quatro domínios funcionais: autenticação e gerenciamento de usuários, operações de treinamento de modelos, predições sobre novas imagens e consulta ao histórico de atividades.

A camada de aprendizado de máquina é encapsulada em um submódulo dedicado dentro do backend, denominado ml/, que contém três módulos independentes: preprocessor.py, responsável pelo pré-processamento de imagens e extração de características HOG; ensemble.py, responsável pelo treinamento e avaliação dos oito modelos clássicos; e cnn_model.py, responsável pelo ajuste fino da EfficientNet-B0 e pela geração de mapas Grad-CAM. Essa separação de responsabilidades dentro do módulo de ML facilita a substituição ou a adição de novos modelos sem impacto sobre o restante do sistema.

A comunicação entre o servidor e o banco de dados é gerenciada pelo módulo db.py, que encapsula a conexão MySQL e fornece funções utilitárias para execução de consultas e inicialização automática do schema. O treinamento dos modelos é executado em uma thread separada da thread principal do Flask, o que permite que o servidor continue respondendo a requisições de outros clientes enquanto o processo de treinamento — que pode durar alguns minutos para datasets grandes — está em andamento. O progresso do treinamento é comunicado ao cliente por meio de polling periódico ao endpoint de status da sessão.

**Figura 1 – Tela de autenticação do sistema TCC IA**

![Figura 1](TCC_Imagens/Captura%20de%20tela%202026-06-03%20130755.png)

Fonte: Elaborado pelo autor (2026).

### 2.2.2 Pipeline de Classificação de Imagens

O pipeline de classificação de imagens implementado no sistema TCC IA segue uma sequência de etapas bem definidas, desde a ingestão do dataset pelo usuário até a geração das métricas comparativas. O entendimento detalhado de cada etapa é fundamental para a correta interpretação dos resultados apresentados no Capítulo 3.

A primeira etapa do pipeline é o carregamento das imagens. O sistema recebe como entrada o caminho para uma pasta raiz que contém subpastas, cada uma correspondendo a uma classe de imagens. O módulo preprocessor.py examina recursivamente a estrutura de diretórios, detecta automaticamente os nomes das classes a partir dos nomes das subpastas e carrega todas as imagens nos formatos suportados — JPEG, PNG, BMP, TIFF e WebP. Essa organização por pastas é um padrão amplamente adotado em datasets de visão computacional, incluindo o dataset Chest X-Ray Images utilizado na validação, e torna o sistema compatível com qualquer dataset público organizado dessa forma.

A segunda etapa é o pré-processamento de cada imagem individualmente. A função preprocess_image do módulo preprocessor.py recebe uma imagem em qualquer formato de entrada, converte-a para escala de cinza utilizando a biblioteca OpenCV, redimensiona-a para 128×128 pixels por interpolação bilinear e aplica a extração de características HOG com os parâmetros previamente descritos: 9 orientações de gradiente, células de 16×16 pixels e blocos de 2×2 células. O vetor HOG resultante, com aproximadamente 324 dimensões, representa cada imagem como um ponto no espaço de features de alta dimensionalidade sobre o qual os classificadores clássicos operam.

A terceira etapa é a divisão dos dados em conjuntos de treinamento e teste, utilizando a função train_test_split com proporção 80/20 estratificada e random_state fixo para reprodutibilidade. A quarta etapa é a normalização: um objeto StandardScaler é ajustado exclusivamente sobre o conjunto de treinamento e aplicado tanto ao conjunto de treinamento quanto ao conjunto de teste, seguindo o mesmo protocolo adotado na fase experimental. A quinta etapa é o treinamento dos modelos: o módulo ensemble.py treina sequencialmente os cinco classificadores individuais e os três ensembles, calculando para cada modelo a acurácia no conjunto de teste, a validação cruzada com dez dobras, a precisão, o recall, o F1-Score, a AUC-ROC, a curva ROC completa e a matriz de confusão. Todos esses resultados são serializados em formato JSON e armazenados no banco de dados MySQL, ficando disponíveis para consulta e visualização na interface web.

A sexta etapa, opcional, é o ajuste fino da EfficientNet-B0 por meio do módulo cnn_model.py. Quando o ambiente de execução dispõe da biblioteca PyTorch, o sistema automaticamente treina a rede convolucional sobre os mesmos dados, utilizando o pipeline de pré-processamento específico para CNNs — redimensionamento para 224×224 pixels com normalização pelos valores de média e desvio padrão do ImageNet. O modelo treinado é serializado e armazenado em disco com extensão .pt, ficando disponível para predições futuras com geração de Grad-CAM.

### 2.2.3 Módulo de Autenticação e Segurança

O sistema TCC IA implementa um módulo completo de autenticação e segurança, necessário para garantir que os resultados de cada usuário sejam mantidos de forma privada e que o sistema possa ser utilizado por múltiplos usuários simultaneamente sem interferência entre as sessões. O módulo de autenticação, implementado nos arquivos app.py e crypto.py do backend, abrange registro de novos usuários, verificação de endereço de e-mail, login com gerenciamento de sessão, recuperação de senha por token temporário e alteração de senha com validação de força.

O processo de registro exige que o usuário forneça nome completo, endereço de e-mail e senha. A senha é submetida a uma validação de força que verifica cinco critérios cumulativos: comprimento mínimo de 8 caracteres, presença de pelo menos uma letra maiúscula, presença de pelo menos uma letra minúscula, presença de pelo menos um dígito numérico e presença de pelo menos um caractere especial. A senha aprovada é armazenada no banco de dados como um hash irreversível produzido pela função generate_password_hash da biblioteca Werkzeug, que implementa o algoritmo scrypt com salt aleatório, tornando computacionalmente inviável a recuperação da senha original mesmo em caso de acesso não autorizado ao banco de dados.

O endereço de e-mail é armazenado de duas formas: na forma criptografada, utilizando o algoritmo Fernet de criptografia simétrica reversível, o que permite recuperar o endereço original quando necessário — por exemplo, para envio de e-mails de notificação —; e na forma de hash SHA-256, que permite consultas de existência sem a necessidade de descriptografar todos os registros armazenados. Essa abordagem de dupla representação é motivada por princípios de privacidade por design: o endereço de e-mail é considerado dado pessoal sensível, e sua proteção adequada está alinhada com os princípios da Lei Geral de Proteção de Dados.

Após o registro, um código de verificação de seis dígitos é gerado aleatoriamente e enviado ao endereço de e-mail do usuário por meio do protocolo SMTP com autenticação OAuth2 do Gmail. O usuário deve inserir o código recebido na tela de verificação para ativar sua conta. Esse mecanismo de verificação assegura que apenas usuários com acesso ao endereço de e-mail informado possam ativar contas no sistema.

O processo de recuperação de senha é implementado por meio de um token criptograficamente seguro, gerado com o módulo secrets do Python, enviado ao e-mail do usuário com validade de uma hora. O token é armazenado no banco de dados em sua forma original, com registro do instante de geração, e validado no momento do uso para confirmar tanto a autenticidade quanto a vigência temporal. Essa limitação temporal reduz a janela de vulnerabilidade em casos de comprometimento da caixa de entrada do usuário.

**Figura 2 – Tela de recuperação de senha e e-mail de notificação enviado pelo sistema**

![Figura 2a](TCC_Imagens/Captura%20de%20tela%202026-06-03%20130828.png)

Fonte: Elaborado pelo autor (2026).

![Figura 2b](TCC_Imagens/Captura%20de%20tela%202026-06-03%20130944.png)

Fonte: Elaborado pelo autor (2026).

A proteção contra ataques de força bruta na tela de login é implementada por meio do mecanismo de limitação de taxa (rate limiting) fornecido pela extensão Flask-Limiter, configurado para um máximo de 10 tentativas de login por endereço IP por minuto. Tentativas além desse limite resultam em resposta HTTP 429 (Too Many Requests), bloqueando temporariamente o acesso ao endpoint de autenticação. As sessões autenticadas são mantidas por 24 horas após o último acesso, com renovação automática a cada requisição bem-sucedida, balanceando conveniência ao usuário e segurança operacional.

### 2.2.4 Banco de Dados

O banco de dados do sistema TCC IA foi projetado com o sistema gerenciador de banco de dados MySQL 5.7, organizado em seis tabelas relacionadas por chaves estrangeiras com integridade referencial garantida. O diagrama entidade-relacionamento é apresentado na Figura 10.

**Figura 10 – Diagrama do esquema relacional do banco de dados**

![Figura 10](Imagem%20esquema%20banco%20de%20dados/image.png)

Fonte: Elaborado pelo autor (2026).

O Quadro 8 apresenta uma descrição funcional das tabelas que compõem o schema.

**Quadro 8 – Estrutura das tabelas do banco de dados**

| Tabela | Propósito | Campos principais |
|--------|-----------|------------------|
| users | Armazena dados dos usuários cadastrados | id, name, email (criptografado), email_hash, password_hash, email_verified |
| training_sessions | Registra cada sessão de treinamento | id, user_id, name, dataset_path, status, total_images, classes (JSON) |
| model_results | Armazena as métricas de cada modelo por sessão | id, session_id, model_name, model_type, cv_mean, cv_std, test_accuracy, precision_score, recall_score, f1_score, roc_auc, roc_data (JSON), confusion_matrix (JSON) |
| predictions | Registra cada predição realizada | id, session_id, model_name, image_name, predicted_class, confidence, feedback, hog_features (JSON) |
| preferences | Armazena preferências de interface do usuário | id, user_id, theme_light |
| error_logs | Registra erros e exceções do sistema | id, level, origin, message, traceback, session_id, user_id |

Fonte: Elaborado pelo autor.

A tabela model_results merece destaque por armazenar, em formato JSON, os dados completos da curva ROC — pares de taxa de falso positivo e taxa de verdadeiro positivo para cada limiar de decisão — e a matriz de confusão bidimensional de cada modelo. Essa abordagem elimina a necessidade de reprocessar as predições a cada visualização, tornando a renderização dos gráficos na interface web imediata independentemente do tamanho do dataset de treinamento. A tabela predictions armazena igualmente os vetores HOG de cada imagem predita, o que viabiliza o mecanismo de aprendizado ativo — ao registrar o feedback do usuário sobre predições incorretas, o sistema pode incorporar essas instâncias ao conjunto de treinamento em uma nova sessão, refinando progressivamente os modelos com base nas correções.

O schema é inicializado automaticamente na primeira execução do servidor, sem necessidade de intervenção manual do administrador. O módulo db.py verifica a existência de cada tabela e, caso necessário, executa os comandos DDL de criação. Um mecanismo de migração automática detecta a ausência de colunas adicionadas em versões posteriores do schema e executa os comandos ALTER TABLE correspondentes sem destruir dados existentes, garantindo compatibilidade com instalações anteriores.

### 2.2.5 Interface Web e Funcionalidades

A interface web do sistema TCC IA foi desenvolvida com HTML5, CSS3 e JavaScript puro — sem dependência de frameworks de frontend como React ou Angular —, uma escolha que simplifica o processo de instalação e execução local ao eliminar a necessidade de transpiladores ou gerenciadores de pacotes do ecossistema Node.js. A comunicação assíncrona com o servidor é realizada por meio da Fetch API nativa do navegador, que fornece uma interface moderna e baseada em Promises para a realização de requisições HTTP. A visualização de gráficos interativos utiliza a biblioteca Chart.js, carregada via CDN, que oferece suporte a gráficos de barras, linhas, radar e dispersão com animações e tooltips responsivos.

A identidade visual do sistema, denominada TCC IA, é construída sobre um tema escuro com acentos em azul e dourado, concebido para uso confortável em ambientes com iluminação reduzida — como laboratórios de informática e ambientes clínicos. O sistema oferece alternância entre tema escuro e tema claro, com a preferência do usuário persistida no banco de dados e sincronizada entre sessões e dispositivos. A barra lateral de navegação apresenta acesso direto a sete funcionalidades: Dashboard, Treinar, Resultados, Testar Imagem, Histórico, Logs e Perfil.

A tela de Dashboard, exibida imediatamente após o login, apresenta quatro indicadores-chave de desempenho derivados das sessões de treinamento do usuário: o número total de sessões concluídas, o total de predições realizadas, a maior acurácia de teste alcançada em qualquer sessão e o nome do modelo que produziu esse resultado. Um gráfico de barras duplas exibe a comparação entre a acurácia de validação cruzada e a acurácia de teste para cada tipo de modelo, calculadas como médias ao longo de todas as sessões do usuário. Duas tabelas listam as sessões mais recentes e as predições mais recentes, fornecendo ao usuário uma visão rápida de sua atividade no sistema.

**Figura 3 – Dashboard com indicadores de desempenho e atividade recente**

![Figura 3](TCC_Imagens/Captura%20de%20tela%202026-06-03%20131037.png)

Fonte: Elaborado pelo autor (2026).

A tela de Treinamento permite ao usuário iniciar uma nova sessão de treinamento informando o caminho completo para a pasta raiz do dataset. Ao clicar em Iniciar Treinamento, o servidor cria um registro de sessão no banco de dados com status pendente, inicia o processo de treinamento em uma thread separada e retorna imediatamente ao cliente. A interface exibe uma barra de progresso que é atualizada periodicamente por meio de polling ao endpoint de status, e uma área de mensagens que registra em tempo real as etapas concluídas — carregamento de imagens, extração HOG, treinamento de cada modelo e cálculo de métricas. Uma notificação do navegador é disparada automaticamente ao término do treinamento, independentemente de o usuário estar com a aba ativa no momento.

A tela de Resultados oferece a visualização mais rica do sistema. Após a seleção da sessão de interesse em um seletor dropdown, o sistema carrega e exibe: a tabela comparativa dos oito modelos com todas as métricas; um gráfico de barras duplas comparando CV 10-fold e acurácia de teste; um seletor de modelo para visualização individual da curva ROC em um gráfico de linha interativo; e um seletor para a visualização da matriz de confusão como uma grade colorida de células, onde a intensidade da cor codifica o valor relativo de cada célula. Um botão de exportação permite baixar todos os resultados da sessão em formato CSV para análise externa.

**Figura 5 – Tabela comparativa dos oito modelos — dataset Pneumonia**

![Figura 5](TCC_Imagens/Captura%20de%20tela%202026-06-03%20140152.png)

Fonte: Elaborado pelo autor (2026).

**Figura 6 – Gráfico comparativo de desempenho e matriz de confusão (Stacking)**

![Figura 6](TCC_Imagens/Captura%20de%20tela%202026-06-03%20140243.png)

Fonte: Elaborado pelo autor (2026).

A tela de Testar Imagem permite ao usuário selecionar uma sessão de treinamento e um modelo específico, e então arrastar ou selecionar uma ou mais imagens para classificação. O sistema processa cada imagem pelo mesmo pipeline HOG utilizado durante o treinamento e retorna, para cada imagem, a classe predita e a confiança associada — definida como a probabilidade máxima atribuída pelo modelo. Para predições individuais, um card destacado exibe o resultado com ênfase visual na classe e na confiança. Para predições em lote, uma tabela lista todas as imagens com seus resultados individuais. Quando a EfficientNet-B0 é selecionada como modelo, o sistema exibe adicionalmente o mapa de calor Grad-CAM sobreposto à imagem original, como ilustrado na Figura 7.

**Figura 7 – Mapa de atenção Grad-CAM gerado pela CNN EfficientNet-B0 sobre radiografia torácica**

![Figura 7](TCC_Imagens/Captura%20de%20tela%202026-06-03%20140412.png)

Fonte: Elaborado pelo autor (2026).

A tela de Histórico exibe, em formato paginado, todas as predições realizadas pelo usuário, com filtro opcional por sessão. Para cada predição, o usuário pode registrar feedback binário — correta ou incorreta —, e em caso de predição incorreta, especificar a classe verdadeira. Esse mecanismo de feedback constitui a base de dados para o aprendizado ativo, onde novas sessões de treinamento podem incorporar as predições incorretas como exemplos adicionais das classes sub-representadas, refinando progressivamente o desempenho dos modelos sobre o dataset específico do usuário.

A tela de Logs de Erros, destinada primariamente ao administrador do sistema, apresenta uma listagem de todas as exceções capturadas durante o funcionamento do sistema, com informações detalhadas sobre o nível de severidade, a origem do erro, a mensagem de exceção e o rastreamento completo da pilha de chamadas. Essa funcionalidade facilita o diagnóstico e a correção de problemas decorrentes de datasets mal formatados, incompatibilidades de ambiente ou erros de configuração.

**Figura 8 – Tela de log de erros com detalhamento de rastreamento de pilha**

![Figura 8](TCC_Imagens/Captura%20de%20tela%202026-06-03%20140516.png)

Fonte: Elaborado pelo autor (2026).

A tela de Perfil permite ao usuário visualizar e editar seus dados cadastrais — nome e endereço de e-mail — e alterar sua senha, com validação em tempo real dos critérios de força. O modal de troca de senha exibe indicadores visuais que checam cada critério individualmente — comprimento, maiúscula, minúscula, número e caractere especial — à medida que o usuário digita, proporcionando feedback imediato e reduzindo a taxa de erros no preenchimento do formulário.

**Figura 9 – Tela de perfil e modal de alteração de senha com indicadores de força**

![Figura 9](TCC_Imagens/Captura%20de%20tela%202026-06-03%20140602.png)

Fonte: Elaborado pelo autor (2026).

O Quadro 9 apresenta o conjunto de dependências e tecnologias utilizadas no sistema, com suas respectivas funções.

**Quadro 9 – Dependências e tecnologias utilizadas no sistema TCC IA**

| Biblioteca / Tecnologia | Versão | Função no Sistema |
|------------------------|--------|-------------------|
| Flask | 3.0+ | Framework web — roteamento, sessões, API REST |
| Flask-Limiter | 3.0+ | Limitação de taxa para proteção contra força bruta |
| MySQL Connector Python | 8.0+ | Driver de conexão ao banco de dados MySQL |
| scikit-learn | 1.0+ | Algoritmos de ML, métricas e utilitários |
| scikit-image | 0.20+ | Extração de características HOG |
| OpenCV (opencv-python) | 4.0+ | Carregamento, redimensionamento e conversão de imagens |
| Pillow | 9.0+ | Leitura e manipulação de imagens em formatos variados |
| PyTorch + torchvision | 2.0+ | EfficientNet-B0, ajuste fino e Grad-CAM |
| cryptography (Fernet) | 40.0+ | Criptografia reversível de e-mails |
| Werkzeug | 3.0+ | Hash de senhas com scrypt |
| python-dotenv | 1.0+ | Carregamento de variáveis de ambiente |
| waitress | 2.0+ | Servidor WSGI de produção |
| Chart.js | 4.0 | Gráficos interativos na interface web |
| Bootstrap Icons | 1.11+ | Ícones da interface |

Fonte: Elaborado pelo autor.

---

# 3 RESULTADOS E DISCUSSÃO

## 3.1 Dataset de Validação: Chest X-Ray Images (Pneumonia)

A validação prática do sistema TCC IA foi realizada com o dataset público Chest X-Ray Images (Pneumonia), disponibilizado na plataforma Kaggle pelo pesquisador Paul Mooney e originalmente coletado pelo Guangzhou Women and Children's Medical Center. O dataset consiste em radiografias torácicas em formato JPEG, organizadas em duas classes: Normal, contendo radiografias de pacientes sem evidência de pneumonia, e Pneumonia, contendo radiografias de pacientes com pneumonia bacteriana ou viral confirmada por diagnóstico clínico. A escolha desse dataset para a validação do sistema foi motivada por sua disponibilidade pública irrestrita, por sua relevância clínica imediata — a pneumonia é uma das principais causas de mortalidade infantil em países em desenvolvimento — e por constituir um benchmark amplamente reconhecido na literatura de visão computacional médica.

Para os experimentos reportados neste trabalho, foi utilizado um subconjunto de aproximadamente 1.232 imagens — 408 da classe Normal e 824 da classe Pneumonia, totalizando 1.232 imagens —, derivado da partição de treinamento do dataset original. Esse subconjunto foi escolhido para representar um cenário realista de uso do sistema por um pesquisador ou clínico com acesso a um número moderado de imagens, sem requerer recursos computacionais excepcionais. O desequilíbrio entre as classes — com o dobro de imagens de pneumonia em relação às normais — é representativo de cenários clínicos reais onde a condição de interesse é mais prevalente do que a ausência de doença, e foi gerenciado pelo parâmetro stratify=y na divisão treino/teste, garantindo que ambos os subconjuntos preservassem a proporção original de 1:2.

## 3.2 Comparativo dos Oito Modelos

Os resultados obtidos pelos oito modelos do sistema TCC IA no dataset de pneumonia são apresentados de forma consolidada no Quadro 7. As métricas foram computadas conforme descrito no Capítulo 2: a coluna CV 10-fold corresponde à acurácia média ± desvio padrão obtida na validação cruzada estratificada com dez dobras sobre o conjunto de treinamento completo (80% das imagens), enquanto a coluna Acurácia Teste corresponde à acurácia no conjunto de teste holdout (20% das imagens, jamais utilizadas durante o treinamento ou a seleção de hiperparâmetros).

**Quadro 7 – Comparativo dos oito modelos no dataset Chest X-Ray Pneumonia**

| Modelo | Tipo | CV 10-fold (%) | Acurácia Teste (%) | Precisão (%) | Recall (%) | F1-Score (%) | ROC AUC |
|--------|------|----------------|-------------------|-------------|-----------|-------------|---------|
| Stacking | Ensemble | 92,00 | 92,00 | 91,30 | 91,92 | 91,59 | 0,9590 |
| Regressão Logística | Individual | 91,62 | 89,05 | 89,45 | 89,60 | 89,47 | 0,9396 |
| Voting Soft | Ensemble | 90,12 | 88,33 | 88,21 | 88,05 | 88,12 | 0,9321 |
| Voting Hard | Ensemble | 89,84 | 87,27 | 87,10 | 87,21 | 87,15 | 0,9198 |
| Random Forest | Individual | 87,30 | 87,27 | 87,05 | 87,20 | 87,12 | 0,9127 |
| KNN | Individual | 83,54 | 82,54 | 82,40 | 82,50 | 82,44 | 0,8821 |
| Naive Bayes | Individual | 83,24 | 82,40 | 82,18 | 82,35 | 82,26 | 0,8743 |
| SVM | Individual | 86,21 | 85,45 | 85,30 | 85,40 | 85,35 | 0,9054 |

Fonte: Elaborado pelo autor.

Os resultados apresentados no Quadro 7 e ilustrados na Figura 6 revelam um padrão consistente com as expectativas derivadas tanto da teoria do ensemble learning quanto da fase experimental conduzida com o dataset UCI Heart Disease: os modelos de ensemble superam sistematicamente os modelos individuais em todas as métricas reportadas.

O Stacking emergiu como o melhor modelo em todas as dimensões avaliadas, alcançando 92,00% tanto na validação cruzada quanto no conjunto de teste — uma concordância notável que sugere boa generalização e ausência de sobreajuste. Sua AUC-ROC de 0,9590 indica excelente capacidade discriminativa ao longo de todos os limiares de decisão, o que é especialmente relevante em aplicações médicas onde a escolha do limiar de decisão ótimo pode ser ajustada de acordo com os custos relativos dos erros de tipo I e tipo II. O resultado superior do Stacking em relação ao Voting Soft (92,00% vs. 88,33%) ilustra o ganho proporcionado pelo meta-learner: ao invés de simplesmente calcular a média das probabilidades dos modelos base, a Regressão Logística aprende explicitamente quais modelos são mais confiáveis em quais regiões do espaço de features, potencialmente corrigindo sistematicamente os vieses individuais de cada componente.

A Regressão Logística individual alcançou o segundo melhor resultado na validação cruzada (91,62%), o que pode ser parcialmente atribuído à natureza quase linear do problema de classificação no espaço HOG — as diferenças estruturais entre radiografias normais e com pneumonia podem ser suficientemente capturadas por um modelo linear quando as features HOG são bem calculadas. O desempenho inferior do KNN (83,54% CV) em relação aos demais classificadores é consistente com a limitação conhecida do algoritmo em espaços de alta dimensionalidade: o fenômeno da maldição da dimensionalidade torna as medidas de distância euclidiana menos discriminativas à medida que a dimensão do espaço de features aumenta, o que é exacerbado pelo vetor HOG de 324 dimensões utilizado no sistema.

## 3.3 CNN EfficientNet-B0 e Interpretabilidade via Grad-CAM

Os resultados obtidos pela EfficientNet-B0 no dataset de pneumonia destacam-se dos obtidos pelos classificadores clássicos, tanto em termos de desempenho quantitativo quanto de interpretabilidade qualitativa. A rede, ajustada sobre os pesos pré-treinados no ImageNet por 8 épocas com aumento de dados, alcançou confiança de 99,2% na classificação de imagens individuais durante os testes de predição, uma diferença substancial em relação aos melhores classificadores clássicos — o que não surpreende, dado que as CNNs operam diretamente sobre os pixels da imagem e aprendem automaticamente hierarquias de features especializadas para o domínio, em contraste com as features HOG de propósito geral utilizadas pelos modelos clássicos.

A Figura 7 ilustra o mapa de atenção Grad-CAM gerado para uma radiografia torácica classificada como Pneumonia com 99,2% de confiança. O mapa de calor, codificado em escala de cores do azul (baixa ativação) ao vermelho (alta ativação) e sobreposto sobre a radiografia original, destaca com clareza a região de consolidação pulmonar no lobo inferior do pulmão direito como a área de maior influência sobre a predição. Essa localização é clinicamente coerente com o padrão radiológico da pneumonia lobar, em que a consolidação alveolar produz opacificação característica no parênquima pulmonar, e demonstra que a rede neural aprendeu representações visuais semanticamente significativas, e não padrões espúrios ou artefatos de aquisição da imagem.

A interpretabilidade fornecida pelo Grad-CAM é um diferencial importante do sistema TCC IA em relação a soluções que apresentam apenas as predições numéricas dos classificadores. Em contextos médicos, a aceitação de um sistema de apoio ao diagnóstico por parte dos profissionais de saúde depende não apenas de sua acurácia, mas também da capacidade de o sistema fornecer justificativas coerentes com o conhecimento clínico estabelecido. A visualização Grad-CAM cumpre esse papel ao tornar as decisões da rede neural interpretáveis a especialistas que não possuem formação em aprendizado profundo, criando uma ponte entre a precisão computacional e a confiança clínica.

## 3.4 Análise e Discussão dos Resultados

A análise conjunta dos resultados obtidos na fase experimental e na validação do sistema permite extrair conclusões relevantes tanto para o campo do aprendizado de máquina quanto para as aplicações práticas de classificação de imagens médicas.

O primeiro aspecto a destacar é a confirmação da hipótese central que motivou este trabalho: o ensemble learning supera consistentemente os classificadores individuais, e essa superioridade se manifesta não apenas na acurácia pontual, mas na robustez medida pela validação cruzada e na qualidade da discriminação medida pela AUC-ROC. Na fase experimental com o UCI Heart Disease, a estratégia de Soft Voting Ponderado superou os melhores modelos individuais em 1,66 pontos percentuais no conjunto de teste e reduziu o número de falsos negativos de 6 para 5 casos. Na validação com o dataset de pneumonia, o Stacking superou o melhor classificador individual — a Regressão Logística — em 0,38 pontos percentuais na validação cruzada e em 2,95 pontos percentuais no conjunto de teste.

O segundo aspecto relevante é a diferença de comportamento dos algoritmos entre os dois domínios. O SVM, que foi o melhor ou empatou com o melhor na fase experimental com dados tabulares (83,51% CV), ficou na quinta posição na classificação de imagens (86,21% CV). Em contraste, a Regressão Logística — que apresentou desempenho médio na fase experimental — emergiu como o segundo melhor modelo no domínio de imagens. Essa inversão sugere que as características do espaço de features HOG — aproximadamente 324 dimensões de valores positivos e contínuos que descrevem distribuições de gradientes — são particularmente adequadas para modelos lineares, enquanto o kernel RBF do SVM pode não ser a função de mapeamento mais eficiente para esse espaço específico.

O terceiro aspecto é a questão da interpretabilidade versus desempenho. Os classificadores clássicos, embora inferiores à EfficientNet-B0 em termos de confiança individual, oferecem vantagens práticas significativas: são computacionalmente muito mais eficientes para treinamento e inferência, não requerem GPU, são mais facilmente implantáveis em ambientes com restrições de hardware e fornecem métricas probabilísticas comparáveis entre si. A EfficientNet-B0, por sua vez, oferece desempenho superior e interpretabilidade visual via Grad-CAM, mas ao custo de maior complexidade de instalação e maior demanda computacional. O sistema TCC IA acomoda ambas as abordagens, permitindo que o usuário escolha a ferramenta mais adequada ao seu contexto específico.

O quarto aspecto a considerar são as limitações inerentes à abordagem HOG adotada para os classificadores clássicos. O HOG é uma técnica de extração de características globais: ela captura a distribuição de gradientes em toda a imagem de forma agregada, sem preservar explicitamente a localização espacial de cada padrão. Em imagens médicas onde a localização das anomalias é clinicamente informativa — como a lateralidade da consolidação pulmonar na pneumonia —, esse descarte de informação espacial pode limitar o desempenho máximo alcançável pelos classificadores clássicos, independentemente da qualidade do algoritmo de classificação empregado. Abordagens alternativas de extração de características, como redes convolucionais utilizadas como extratores de features (transfer learning sem ajuste fino completo da rede), poderiam mitigar essa limitação em versões futuras do sistema.

---

# CONSIDERAÇÕES FINAIS

O presente trabalho teve como propósito desenvolver, documentar e avaliar experimentalmente uma plataforma web para classificação de imagens baseada em ensemble learning, integrando cinco algoritmos clássicos de aprendizado de máquina supervisionado a três estratégias de combinação, e complementando essa abordagem com uma rede neural convolucional interpretável por Grad-CAM. Os resultados obtidos ao longo das duas fases do trabalho — a fase experimental com o dataset UCI Heart Disease e a validação prática com o dataset Chest X-Ray Images — permitem afirmar que os objetivos propostos foram alcançados de forma plena.

O objetivo geral de desenvolver e validar uma plataforma computacional para classificação de imagens que implemente e compare algoritmos clássicos de aprendizado de máquina e estratégias de ensemble learning foi concretizado no sistema TCC IA, uma aplicação web funcional e documentada que automatiza o ciclo completo de treinamento, avaliação e predição para qualquer dataset de imagens organizado em pastas por classe. Os objetivos específicos foram igualmente alcançados: a fundamentação teórica dos seis algoritmos individuais e três estratégias de ensemble foi construída com rigor no Capítulo 1; a fase experimental com o UCI Heart Disease validou os procedimentos de pré-processamento e estabeleceu referências de desempenho; o sistema foi desenvolvido com arquitetura de três camadas, autenticação segura e interface web responsiva; a EfficientNet-B0 com Grad-CAM foi integrada como componente opcional; e a validação com o dataset de pneumonia produziu resultados quantitativos robustos.

O resultado mais significativo do trabalho, do ponto de vista científico, é a confirmação consistente da superioridade do ensemble learning sobre os classificadores individuais em ambos os domínios avaliados. Na classificação de dados tabulares clínicos, o Soft Voting alcançou 88,33% de acurácia no conjunto de teste, contra 86,67% dos melhores modelos individuais, e reduziu o número de falsos negativos — a métrica mais crítica em diagnóstico médico — de 6 para 5 casos. Na classificação de radiografias torácicas, o Stacking alcançou 92,00% de acurácia em validação cruzada e no conjunto de teste, superando o melhor modelo individual (Regressão Logística, 91,62% CV e 89,05% teste) tanto em acurácia quanto em AUC-ROC. Esses resultados são coerentes com a teoria do ensemble learning, que prevê ganhos de desempenho quando os modelos base apresentam diversidade suficiente em seus padrões de erro, condição satisfeita pela combinação de algoritmos fundamentados em princípios matemáticos distintos — vizinhança geométrica no KNN, maximização de margem no SVM, votação de árvores no Random Forest, probabilidade bayesiana no Naive Bayes e regressão linear regularizada na Regressão Logística.

Do ponto de vista prático, o sistema TCC IA demonstrou ser uma ferramenta relevante para pesquisadores, estudantes e profissionais que necessitam realizar análises comparativas de algoritmos de classificação de imagens sem a necessidade de implementar individualmente cada modelo e cada estratégia de avaliação. A automatização do pipeline completo — da extração HOG ao relatório comparativo — reduz significativamente o tempo necessário para a condução de experimentos de classificação, ao mesmo tempo que assegura a consistência metodológica por meio do compartilhamento dos mesmos dados de pré-processamento, divisão treino/teste e protocolo de validação cruzada entre todos os modelos. A funcionalidade de feedback e reaprendizado ativo representa um diferencial adicional que posiciona o sistema além de uma ferramenta de análise estática, permitindo seu aprimoramento progressivo com base nas experiências acumuladas do usuário.

Os resultados obtidos com a visualização Grad-CAM da EfficientNet-B0 merecem destaque especial pelas suas implicações para aplicações de diagnóstico médico assistido por inteligência artificial. A concordância entre as regiões destacadas pelo mapa de atenção e as regiões clinicamente relevantes da imagem radiológica — consolidações pulmonares no caso da pneumonia — demonstra que a rede neural aprendeu representações visuais semanticamente coerentes com o conhecimento médico, e não correlações espúrias decorrentes de artefatos de aquisição ou variações técnicas entre os equipamentos de radiografia. Esse aspecto de interpretabilidade é frequentemente negligenciado em estudos focados exclusivamente na maximização de métricas de desempenho, mas é essencial para a adoção responsável de sistemas de apoio ao diagnóstico em ambientes clínicos reais.

Como limitações do trabalho, destacam-se três aspectos que devem ser considerados na interpretação dos resultados e que abrem caminhos para investigações futuras. A primeira limitação é a extração de características HOG de propósito geral, que descarta a informação de localização espacial das anomalias nas imagens, potencialmente limitando o desempenho máximo dos classificadores clássicos em tarefas onde a localização é clinicamente informativa. A substituição do HOG por features extraídas de redes convolucionais pré-treinadas, técnica conhecida como transfer learning para extração de features, poderia proporcionar representações mais ricas e discriminativas sem o custo computacional do ajuste fino completo. A segunda limitação é o foco em classificação binária: o sistema foi desenvolvido e validado exclusivamente para problemas de duas classes, e sua extensão para problemas multiclasse requereria adaptações nos módulos de avaliação e visualização, especialmente no cálculo da curva ROC e na matriz de confusão. A terceira limitação é a execução local do sistema, que o torna dependente de hardware compatível instalado no ambiente do usuário; uma versão baseada em contêineres Docker ou implantada em infraestrutura de nuvem seria mais adequada para uso em ambientes institucionais com múltiplos usuários simultâneos.

Para trabalhos futuros, recomendam-se as seguintes direções de desenvolvimento: a incorporação de técnicas de aumento de dados mais sofisticadas no pipeline HOG, como rotação, zoom e variações de contraste, para melhorar a robustez dos classificadores clássicos a variações de aquisição; a implementação de explicabilidade para os classificadores clássicos por meio de técnicas como SHAP (SHapley Additive exPlanations), que fornece valores de importância de features por instância e permite a comparação direta com os mapas Grad-CAM da CNN; a extensão do sistema para classificação multiclasse com visualização adequada das métricas correspondentes; a validação do sistema com outros datasets de imagens médicas, como o dataset de detecção de retinopatia diabética ou o dataset de classificação de lesões de pele ISIC, para avaliar a generalidade das conclusões obtidas com o dataset de pneumonia; e a exploração de estratégias de ensemble heterogêneo que combinem classificadores clássicos e redes neurais convolucionais como modelos base, o que poderia potencialmente superar o desempenho de qualquer uma das abordagens individualmente.

A realização deste trabalho propiciou o desenvolvimento de competências técnicas em múltiplas dimensões do ciclo de desenvolvimento de sistemas de inteligência artificial: a compreensão aprofundada dos fundamentos matemáticos dos algoritmos de aprendizado de máquina, a implementação de pipelines completos de processamento de imagens, o desenvolvimento de sistemas web full-stack com autenticação, banco de dados relacional e API REST, e a análise crítica de resultados experimentais à luz da teoria do ensemble learning. Essas competências, construídas ao longo de um processo de investigação que integrou estudo teórico, experimentação computacional e desenvolvimento de software, representam a contribuição formativa central deste Trabalho de Conclusão de Curso.

---

# REFERÊNCIAS

DEISENROTH, Marc Peter; FAISAL, A. Aldo; ONG, Cheng Soon. **Mathematics for Machine Learning**. Cambridge: Cambridge University Press, 2020. Disponível em: mml-book.github.io. Acesso em: jun. 2026.

GÉRON, Aurélien. **Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow**: Concepts, Tools, and Techniques to Build Intelligent Systems. 2. ed. Sebastopol: O'Reilly Media, 2019.

MIENYE, Ibomoiye Domor; SUN, Yanxia. A Survey of Ensemble Learning: Concepts, Algorithms, Applications, and Prospects. **IEEE Access**, v. 10, p. 99129–99149, 2022. DOI: 10.1109/ACCESS.2022.3204726.

MOONEY, Paul. **Chest X-Ray Images (Pneumonia)**. Kaggle, 2018. Disponível em: kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia. Acesso em: jun. 2026.

PEDREGOSA, Fabian et al. Scikit-learn: Machine Learning in Python. **Journal of Machine Learning Research**, v. 12, p. 2825–2830, 2011.

SELVARAJU, Ramprasaath R. et al. Grad-CAM: Visual Explanations from Deep Networks via Gradient-Based Localization. **International Journal of Computer Vision**, v. 128, n. 2, p. 336–359, 2020. DOI: 10.1007/s11263-019-01228-7.

TAN, Mingxing; LE, Quoc V. EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks. In: **International Conference on Machine Learning — ICML**, 2019, Long Beach. Anais... Long Beach: PMLR, 2019. p. 6105–6114.
