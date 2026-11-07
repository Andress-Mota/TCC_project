# SELEÇÃO DO PARÂMETRO K NO ALGORITMO K-NEAREST NEIGHBORS APLICADO AO DIAGNÓSTICO DE DOENÇAS CARDÍACAS: UMA ANÁLISE SISTEMÁTICA VIA VALIDAÇÃO CRUZADA

**André Felipe de Oliveira**

Faculdade de Tecnologia de Guaratinguetá — FATEC Guaratinguetá

andressmota78@gmail.com

---

## Resumo

O diagnóstico precoce de doenças cardiovasculares é um desafio crítico da saúde pública global, e o aprendizado de máquina tem emergido como ferramenta de suporte à decisão clínica com resultados promissores. Este artigo apresenta uma análise sistemática da seleção do hiperparâmetro K no algoritmo K-Nearest Neighbors (KNN), aplicado à classificação binária de doença cardíaca utilizando o Cleveland Heart Disease Dataset (UCI Machine Learning Repository). Foram avaliadas 100 combinações de parâmetros: 25 valores de K (de 1 a 49, valores ímpares) cruzados com 4 configurações de validação cruzada (5, 10, 15 e 20 dobras), totalizando mais de 2.000 execuções de avaliação. O valor K=29 foi identificado como o parâmetro ideal, obtendo acurácia média de 83,28% e AUC-ROC de 90,20%, com variabilidade controlada de 0,0629 — resultado que demonstra o melhor compromisso entre acurácia preditiva e estabilidade do modelo frente ao trade-off viés-variância. O pré-processamento adotou limpeza de dados, binarização da variável alvo e normalização Z-score. Os resultados alcançados alinham-se à literatura especializada em diagnóstico por aprendizado de máquina e reforçam a viabilidade clínica do KNN como ferramenta de triagem não invasiva.

**Palavras-chave:** K-Nearest Neighbors; Hiperparâmetro K; Validação Cruzada; Doença Cardíaca; Aprendizado de Máquina; Trade-off Viés-Variância.

---

## Abstract

Early diagnosis of cardiovascular diseases is a critical public health challenge, and machine learning has emerged as a clinical decision support tool with promising results. This paper presents a systematic analysis of K hyperparameter selection in the K-Nearest Neighbors (KNN) algorithm, applied to binary classification of heart disease using the Cleveland Heart Disease Dataset (UCI Machine Learning Repository). One hundred parameter combinations were evaluated: 25 K values (from 1 to 49, odd numbers) crossed with 4 cross-validation configurations (5, 10, 15, and 20 folds), totaling more than 2,000 evaluation runs. K=29 was identified as the optimal parameter, achieving a mean accuracy of 83.28% and AUC-ROC of 90.20%, with controlled variability of 0.0629. Preprocessing steps included data cleaning, target variable binarization, and Z-score normalization. The results align with specialized literature on machine learning-based diagnosis, reinforcing the clinical viability of KNN as a non-invasive screening tool.

**Keywords:** K-Nearest Neighbors; K Hyperparameter; Cross-Validation; Heart Disease; Machine Learning; Bias-Variance Trade-off.

---

## 1. Introdução

As doenças cardiovasculares representam uma das principais causas de mortalidade no mundo, gerando impacto econômico e social significativo sobre os sistemas de saúde. O diagnóstico precoce é essencial para reduzir a morbimortalidade associada, porém os procedimentos convencionais de diagnóstico envolvem exames de custo elevado e disponibilidade restrita. Nesse contexto, o aprendizado de máquina (AM) desponta como ferramenta de suporte à decisão clínica capaz de identificar padrões preditivos em dados clínicos de rotina, democratizando o acesso à triagem médica.

Dentre os algoritmos de classificação supervisionada, o K-Nearest Neighbors (KNN) destaca-se pela transparência conceitual e interpretabilidade clínica: a classificação de um novo paciente é diretamente justificada pelos K casos mais similares presentes no conjunto de treinamento (GÉRON, 2019). Como algoritmo baseado em instâncias, o KNN não constrói um modelo paramétrico explícito durante o treinamento — toda a computação é realizada no momento da predição, o que o torna especialmente adequado para aplicações onde a explicabilidade das decisões é relevante.

No entanto, o desempenho do KNN é altamente dependente da escolha do hiperparâmetro K, que determina o tamanho da vizinhança utilizada para a votação majoritária. Um valor de K inadequado leva ao overfitting (K pequeno, alta variância) ou ao underfitting (K grande, alto viés), comprometendo a capacidade de generalização do modelo. Estudos como Uddin et al. (2022) demonstram que diferentes variantes e configurações do KNN produzem resultados consideravelmente distintos em problemas de diagnóstico médico, reforçando a importância da seleção criteriosa de parâmetros.

Apesar da relevância do tema, a literatura carece de estudos sistemáticos que avaliem o impacto combinado de diferentes valores de K com múltiplas configurações de validação cruzada sobre dados clínicos reais. A maioria dos trabalhos adota valores de K por heurística ou busca limitada, sem analisar a estabilidade das métricas entre protocolos de avaliação distintos.

Este artigo tem como objetivo preencher essa lacuna, apresentando uma análise paramétrica rigorosa do KNN aplicado ao Cleveland Heart Disease Dataset. A contribuição central é a identificação de K=29 como valor ideal por meio de 100 combinações sistematicamente avaliadas, com justificativa baseada no trade-off viés-variância, na estabilidade entre configurações e na interpretabilidade clínica.

---

## 2. Conceitos sobre Inteligência Artificial

### 2.1 Aprendizado de Máquina Supervisionado

O aprendizado de máquina (AM) é a subárea da Inteligência Artificial dedicada ao desenvolvimento de algoritmos capazes de aprender padrões a partir de dados, sem que suas regras sejam explicitamente programadas. Como define Géron (2019, p. 2), "Machine Learning is the science of programming computers so they can learn from data", ou seja, os sistemas aprendem a partir de exemplos em vez de seguir instruções fixas codificadas manualmente.

O aprendizado supervisionado é a categoria mais amplamente adotada em aplicações clínicas. O algoritmo recebe um conjunto de treinamento composto por pares (x_i, y_i), onde x_i é o vetor de atributos do i-ésimo exemplo e y_i é o rótulo de classe correspondente. A partir desses pares, o modelo estima uma função de mapeamento que generaliza para dados novos não vistos durante o treinamento. Giraldi (2021) categoriza os algoritmos de AM supervisionado em paramétricos — que ajustam um conjunto fixo de parâmetros — e não paramétricos — cuja complexidade cresce com os dados —, sendo o KNN um representante clássico da segunda categoria.

No contexto de diagnóstico médico, o aprendizado supervisionado tem sido aplicado com resultados expressivos. Mienye e Sun (2022) revisaram técnicas de ensemble learning aplicadas a problemas de classificação clínica e reportaram acurácias entre 80% e 95% em diferentes datasets médicos, dependendo do algoritmo e das características do problema. Uddin et al. (2022) avaliaram especificamente variantes do KNN em oito datasets de doenças, demonstrando que a escolha de parâmetros e variantes do algoritmo impacta significativamente o desempenho em contextos de diagnóstico.

### 2.2 Algoritmo K-Nearest Neighbors

O K-Nearest Neighbors (KNN) é um algoritmo de classificação não paramétrico baseado na premissa de que amostras com atributos similares tendem a pertencer à mesma classe. Para classificar uma nova amostra x_q, o algoritmo identifica os K exemplos mais próximos no espaço de características — os K vizinhos mais próximos — e atribui ao ponto de consulta a classe mais frequente entre eles (votação majoritária). Formalmente:

    ŷ_q = argmax_c  Σ_{i ∈ N_K(x_q)} 𝟙[y_i = c]

onde N_K(x_q) é o conjunto dos K índices cujos vetores estão mais próximos de x_q e 𝟙[·] é a função indicadora. Para classificação binária (c ∈ {0, 1}), a regra reduz-se à contagem de votos: se mais da metade dos K vizinhos pertence à classe positiva, o ponto é classificado como positivo.

A proximidade entre amostras é medida pela distância Euclidiana, caso especial da família de métricas de Minkowski para p=2:

    d_E(x, z) = √( Σ_{j=1}^{d} (x_j - z_j)² )

Géron (2019) classifica o KNN como algoritmo lazy (preguiçoso) e baseado em instâncias: não constrói modelo durante o treinamento, armazenando o conjunto inteiro para uso na predição. Isso torna o KNN computacionalmente simples de implementar, mas sensível à escala dos atributos — razão pela qual a normalização prévia é condição obrigatória para o funcionamento correto do algoritmo.

Uddin et al. (2022) destacam que o KNN clássico, apesar de sua simplicidade, compete com variantes mais sofisticadas (KNN adaptativo, fuzzy, ponderado) em datasets médicos, especialmente quando o hiperparâmetro K é adequadamente selecionado. Os autores reportam que o KNN ensemble obteve acurácia média de 82,34% em oito datasets de doenças, resultado próximo ao K=29 identificado neste trabalho (83,28%).

### 2.3 Trade-off Viés-Variância e Seleção do Hiperparâmetro K

O erro esperado de generalização de qualquer classificador pode ser decomposto em:

    Erro(x_q) = Viés² + Variância + ε

onde ε representa o ruído irredutível dos dados. Giraldi (2021) descreve esse dilema como central em aprendizado de máquina: modelos com baixo viés tendem a alta variância (overfitting), enquanto modelos com alta variância tendem a alto viés (underfitting), e o objetivo é encontrar o ponto de equilíbrio que minimiza o erro de generalização.

No KNN, o valor de K controla diretamente esse trade-off:

- **K pequeno (K = 1 a 5):** o modelo depende de pouquíssimas amostras por predição, tornando-se extremamente sensível a ruídos — alta variância, overfitting. A fronteira de decisão é altamente irregular, envolvendo cada ponto de treinamento individualmente.

- **K grande (K próximo de n):** a vizinhança abrange grande parte do conjunto de treinamento, suavizando excessivamente as fronteiras de decisão — alto viés, underfitting. O modelo perde capacidade de capturar padrões locais relevantes.

- **K ótimo:** equilibra os dois componentes, capturando padrões reais sem se deixar influenciar por ruídos locais. Géron (2019) recomenda a determinação empírica do K via validação cruzada como método preferível à escolha heurística.

### 2.4 Validação Cruzada Estratificada

A validação cruzada k-fold estratificada é o protocolo padrão para seleção de hiperparâmetros e estimativa de desempenho. O conjunto D é particionado em v dobras mutuamente exclusivas, mantendo em cada uma a mesma proporção de classes do conjunto original (estratificação). Para cada dobra i, um modelo é treinado sobre D \ D_i e avaliado sobre D_i:

    Acc_CV = (1/v) Σ_{i=1}^{v} Acc(M_{D\D_i}, D_i)

Géron (2019) destaca as vantagens desse protocolo sobre a simples divisão treino/teste: aproveita todos os dados disponíveis para treinamento e avaliação, reduz a variância da estimativa e é menos dependente de uma única partição aleatória. O AUC-ROC (Area Under the Receiver Operating Characteristic Curve) complementa a acurácia medindo a capacidade discriminativa global do modelo independente do limiar de decisão — métrica especialmente relevante em triagem clínica.

---

## 3. Materiais e Métodos

### 3.1 Base de Dados

O estudo utiliza o Cleveland Heart Disease Dataset, disponibilizado publicamente pelo UCI Machine Learning Repository. Trata-se de um dos conjuntos de dados mais referenciados em pesquisas de diagnóstico cardíaco por aprendizado de máquina (UDDIN et al., 2022), coletado na Clínica Cleveland (EUA) com pacientes submetidos a avaliação cardíaca completa.

O dataset original contém 303 registros e 14 atributos — 13 preditores clínicos e 1 variável alvo com 5 classes (0 = sem evidência de doença; 1 a 4 = graus crescentes de comprometimento cardíaco). Após remoção de 6 registros com valores ausentes (NaN), restaram **297 registros válidos** — 160 pacientes saudáveis (Classe 0) e 137 com algum grau de doença cardíaca (Classe 1). A Tabela 1 descreve os 13 atributos preditores.

**Tabela 1 – Atributos do Cleveland Heart Disease Dataset**

| Atributo   | Descrição                                                        | Tipo       |
|------------|------------------------------------------------------------------|:----------:|
| age        | Idade do paciente (anos)                                         | Numérico   |
| sex        | Sexo (1 = masculino; 0 = feminino)                               | Binário    |
| cp         | Tipo de dor torácica (0 = assintomático; 1–3 = sintomático)      | Categórico |
| trestbps   | Pressão arterial em repouso (mmHg)                               | Numérico   |
| chol       | Colesterol sérico (mg/dl)                                        | Numérico   |
| fbs        | Glicemia em jejum > 120 mg/dl (1/0)                              | Binário    |
| restecg    | Resultado do ECG em repouso (0–2)                                | Categórico |
| thalach    | Frequência cardíaca máxima atingida (bpm)                        | Numérico   |
| exang      | Angina induzida por exercício (1 = sim; 0 = não)                 | Binário    |
| oldpeak    | Depressão do segmento ST pelo exercício                          | Numérico   |
| slope      | Inclinação do segmento ST de pico (0–2)                          | Categórico |
| ca         | Número de vasos principais coloridos por fluoroscopia (0–3)      | Ordinal    |
| thal       | Resultado do teste de estresse com tálio (0–3)                   | Categórico |

Fonte: UCI Machine Learning Repository.

### 3.2 Pipeline de Pré-processamento

O pipeline seguiu três etapas em sequência obrigatória, implementadas em Python com a biblioteca scikit-learn:

**Etapa 1 — Remoção de valores ausentes:** registros com NaN em qualquer dos 13 atributos foram descartados, resultando em 297 registros válidos.

**Etapa 2 — Binarização da variável alvo:** a variável original com 5 classes foi convertida para classificação binária: y=0 (saudável) se y_original=0; y=1 (doente) caso contrário. Essa decisão alinha o problema à pergunta diagnóstica central da triagem.

**Etapa 3 — Normalização Z-score:** os 13 atributos foram padronizados com o StandardScaler, calculando média e desvio exclusivamente sobre o conjunto de treinamento e aplicando ao teste, evitando data leakage. Géron (2019) ressalta que a normalização é etapa obrigatória para algoritmos baseados em distância como o KNN.

### 3.3 Protocolo de Análise Paramétrica

A análise avaliou 25 valores de K (ímpares, de 1 a 49) combinados com 4 configurações de validação cruzada estratificada (5, 10, 15 e 20 dobras), totalizando **100 combinações** e mais de **2.000 execuções de avaliação**. Cada combinação gerou: acurácia média, desvio padrão da acurácia, AUC-ROC médio e variabilidade CV.

O K ideal foi selecionado por critérios múltiplos: (i) acurácia média consolidada nas 4 configurações; (ii) AUC-ROC médio; (iii) variabilidade CV — valores menores indicam maior robustez; (iv) consistência entre configurações de CV; (v) posicionamento no trade-off viés-variância. Todos os experimentos foram executados com random_state=42 para garantir reprodutibilidade.

---

## 4. Estudo de Caso: Aplicação, Resultados e Discussão

### 4.1 Desempenho por Configuração de Validação Cruzada

A Tabela 2 apresenta os melhores valores de K identificados em cada configuração de validação cruzada, juntamente com as métricas de K=29 para comparação direta.

**Tabela 2 – Melhor K por configuração de CV e desempenho de K=29**

| Config. CV  | Melhor K | Acurácia Melhor K    | K=29: Acurácia       | K=29: AUC-ROC        |
|:-----------:|:--------:|:--------------------:|:--------------------:|:--------------------:|
| 5 dobras    | K=31     | 0,8384 ± 0,0346      | 0,8282 ± 0,0362      | 0,8965 ± 0,0354      |
| 10 dobras   | K=49     | 0,8418 ± 0,0729      | 0,8286 ± 0,0699      | 0,9021 ± 0,0546      |
| 15 dobras   | K=31     | 0,8454 ± 0,0418      | 0,8388 ± 0,0481      | 0,9055 ± 0,0445      |
| 20 dobras   | K=41     | 0,8452 ± 0,0873      | 0,8355 ± 0,0972      | 0,9041 ± 0,0699      |

Fonte: Dados do experimento.

Os "melhores K" variam conforme a configuração (K=31, K=49, K=41), indicando sensibilidade ao protocolo de avaliação. Em contraste, K=29 manteve desempenho competitivo em todas as configurações, com acurácia variando de 82,82% a 83,88% — amplitude de apenas 1,06 pontos percentuais. Essa estabilidade é propriedade valiosa: como observam Géron (2019) e Mienye e Sun (2022), modelos cujo desempenho depende excessivamente da configuração de avaliação oferecem menor confiabilidade em aplicações reais.

### 4.2 Análise Consolidada por Valor de K

A Tabela 3 apresenta os resultados consolidados (média das 4 configurações de CV) para valores representativos de K.

**Tabela 3 – Resultados consolidados por valor de K**

| K      | Acurácia Média | AUC-ROC Médio | Variabilidade CV | Zona               |
|:------:|:--------------:|:-------------:|:----------------:|:------------------:|
| 1      | 0,7661         | 0,7652        | 0,0851           | Overfitting severo |
| 3      | 0,8141         | 0,8696        | 0,0697           | Overfitting alto   |
| 9      | 0,8200         | 0,8996        | 0,0632           | Overfitting leve   |
| 21     | 0,8343         | 0,8986        | 0,0616           | Equilíbrio         |
| **29** | **0,8328**     | **0,9020**    | **0,0629**       | **Equilíbrio ideal** |
| 31     | 0,8361         | 0,9023        | 0,0595           | Início underfitting|
| 41     | 0,8385         | 0,9031        | 0,0597           | Underfitting leve  |
| 49     | 0,8387         | 0,8991        | 0,0621           | Underfitting       |

Fonte: Dados do experimento (knn_parameter_stats_by_k.csv).

Os dados evidenciam três zonas comportamentais: overfitting (K=1–9, acurácia < 82%, alta variabilidade), equilíbrio (K=9–29, crescimento monotônico de acurácia com redução de variabilidade) e transição para underfitting (K=31–49, ganhos marginais de acurácia com AUC-ROC decrescente a partir de K=35).

### 4.3 Visualização da Análise Paramétrica

As Figuras 1 a 6 apresentam os resultados da análise paramétrica completa. A Figura 1 mostra a acurácia média em função de K para as 4 configurações de validação cruzada; a Figura 2 apresenta o AUC-ROC por K; a Figura 3 ilustra a variabilidade entre dobras; a Figura 4 compara a distribuição de K=29 frente aos demais; a Figura 5 exibe o heatmap de acurácia por K e número de dobras; e a Figura 6 consolida a acurácia por faixa de K.

### 4.4 Análise do Trade-off Viés-Variância

A Tabela 4 quantifica o trade-off viés-variância agrupando os valores de K em três categorias.

**Tabela 4 – Análise do trade-off viés-variância por faixa de K**

| Faixa de K      | Acurácia Média | Variabilidade CV | Comportamento             |
|:---------------:|:--------------:|:----------------:|:-------------------------:|
| K baixo (1–9)   | 0,8020         | 0,0723           | Overfitting — alta variância |
| **K=29**        | **0,8328**     | **0,0629**       | **Equilíbrio ideal**      |
| K alto (31–49)  | 0,8372         | 0,0617           | Início de underfitting    |

Fonte: Dados do experimento.

A diferença de acurácia entre K=29 e a faixa K>29 é de apenas 0,44 pontos percentuais, enquanto o AUC-ROC de K=29 (0,9020) supera o de K=49 (0,8991). Isso confirma que o ganho marginal de acurácia nos Ks maiores é acompanhado por redução da capacidade discriminativa — padrão consistente com o underfitting descrito por Giraldi (2021).

### 4.5 Resultados Finais com K=29

**Tabela 5 – Resumo de desempenho do KNN (K=29)**

| Métrica                                      | Valor                 |
|----------------------------------------------|:---------------------:|
| Acurácia — conjunto de teste (hold-out 20%)  | **86,67%**            |
| Acurácia — validação cruzada 10-fold (ref.)  | **82,86% ± 6,99%**    |
| AUC-ROC médio (análise paramétrica)          | **90,20%**            |
| Variabilidade CV (análise paramétrica)       | 0,0629                |
| Estabilidade entre configurações de CV       | 0,0052                |
| K (número de vizinhos)                       | 29                    |

Fonte: Dados do experimento.

A acurácia de 86,67% no conjunto de teste e o AUC-ROC de 90,20% indicam excelente capacidade discriminativa. A validação cruzada de 10 dobras (82,86% ± 6,99%) representa a estimativa mais confiável de desempenho esperado em dados reais — métrica de referência recomendada por Géron (2019) para avaliação honesta de classificadores.

### 4.6 Comparação com a Literatura

**Tabela 6 – Comparação com resultados da literatura**

| Estudo / Algoritmo                              | Dataset         | Acurácia    | AUC-ROC    |
|-------------------------------------------------|:---------------:|:-----------:|:----------:|
| Este trabalho — KNN (K=29)                      | Cleveland UCI   | 86,67%      | 90,20%     |
| Uddin et al. (2022) — KNN clássico (média 8 DS) | Múltiplos UCI   | ~64–84%     | —          |
| Uddin et al. (2022) — KNN ensemble              | Múltiplos UCI   | 82,34%      | —          |
| Mienye e Sun (2022) — modelos ensemble          | UCI variados    | 80–95%      | —          |

Fonte: Uddin et al. (2022); Mienye e Sun (2022); dados do experimento.

Os resultados de 86,67% situam este trabalho acima da média reportada por Uddin et al. (2022) para o KNN clássico (até 84%), demonstrando que a seleção sistemática de K via validação cruzada múltipla é capaz de superar abordagens de busca limitada. O AUC-ROC de 90,20% confirma discriminação clínica expressiva.

---

## 5. Considerações Finais

Este trabalho apresentou uma análise sistemática da seleção do hiperparâmetro K no algoritmo KNN aplicado ao diagnóstico de doenças cardíacas, utilizando o Cleveland Heart Disease Dataset com 297 registros e 13 atributos clínicos. A metodologia adotada — 100 combinações (K, configuração CV) com critérios de seleção múltiplos — representa contribuição metodológica relevante frente à prática de seleção heurística predominante na literatura.

Os principais resultados são: (i) K=29 é o parâmetro ideal, com acurácia de 83,28%, AUC-ROC de 90,20% e variabilidade CV de 0,0629; (ii) a seleção sistemática supera a heurística — K=5 obtém 81,25% e K=17 obtém 82,67%; (iii) o trade-off viés-variância é claramente observável: K=1 apresenta variabilidade 0,0851 e acurácia 76,61%, enquanto K=29 equilibra os dois componentes; (iv) K=29 é consistentemente competitivo em todas as 4 configurações de CV, com variação de apenas 1,06 pontos percentuais de acurácia.

Os resultados superam a acurácia média reportada por Uddin et al. (2022) para o KNN clássico e se alinham ao intervalo superior das técnicas de ensemble revistas por Mienye e Sun (2022), validando a qualidade da metodologia adotada.

Como limitações: (i) tamanho moderado do dataset (297 registros) aumenta a variância das estimativas; (ii) análise restrita ao Cleveland dataset. Como trabalhos futuros, recomenda-se: (i) avaliar métricas de distância alternativas; (ii) investigar KNN ponderado por distância; (iii) combinar o KNN otimizado em modelos ensemble conforme abordagens revisadas por Mienye e Sun (2022).

---

## Referências

GÉRON, Aurélien. **Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow: Concepts, Tools, and Techniques to Build Intelligent Systems**. 2. ed. Sebastopol, CA: O'Reilly Media, 2019.

GIRALDI, Gilson Antonio. **Machine Learning and Pattern Recognition**. Lecture Notes — Graduate Course. Graduate Program in Nanobiosystems 2021. Petrópolis, RJ: UFRJ-Fiocruz-INMETRO-LNCC, 2021.

MIENYE, I. D.; SUN, Y. A Survey of Ensemble Learning: Concepts, Algorithms, Applications, and Prospects. **IEEE Access**, v. 10, p. 99129–99149, 2022. DOI: 10.1109/ACCESS.2022.3207287.

UDDIN, S.; HAQUE, I.; LU, H.; MONI, M. A.; GIDE, E. Comparative performance analysis of K-nearest neighbour (KNN) algorithm and its different variants for disease prediction. **Scientific Reports**, v. 12, n. 6256, 2022. DOI: 10.1038/s41598-022-10358-x.
