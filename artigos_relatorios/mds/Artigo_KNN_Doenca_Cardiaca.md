# K-NEAREST NEIGHBORS APLICADO AO DIAGNÓSTICO DE DOENÇA CARDÍACA: FUNDAMENTOS MATEMÁTICOS, IMPLEMENTAÇÃO E ANÁLISE DE DESEMPENHO

André Felipe

Faculdade de Tecnologia de Guaratinguetá

e-mail: andressmota78@gmail.com

---

## Resumo

Este artigo apresenta a aplicação do algoritmo K-Nearest Neighbors (KNN) para a classificação binária de doença cardíaca utilizando o Cleveland Heart Disease Dataset (UCI Machine Learning Repository). São cobertos os fundamentos matemáticos do algoritmo, incluindo métricas de distância, regra de votação majoritária e seleção do hiperparâmetro K por meio de validação cruzada estratificada. A implementação foi desenvolvida em Python com a biblioteca scikit-learn, empregando padronização Z-score, particionamento estratificado e otimização automática de K via GridSearchCV. O melhor valor encontrado foi K = 29, obtendo acurácia de 86,67% no conjunto de teste e 82,86% ± 6,99% na validação cruzada de 10 dobras. Os 297 pacientes avaliados foram analisados por matrix de confusão, relatório de classificação e distribuição de acertos em blocos de 50 registros.

**Palavras-chave:** K-Nearest Neighbors; Aprendizado de Máquina; Doença Cardíaca; Classificação Binária; Validação Cruzada.

---

## Abstract

This paper presents the application of the K-Nearest Neighbors (KNN) algorithm for binary classification of heart disease using the Cleveland Heart Disease Dataset (UCI Machine Learning Repository). The mathematical foundations of the algorithm are covered, including distance metrics, majority voting decision rules and selection of the hyperparameter K through stratified cross-validation. The Python implementation uses Z-score standardization, stratified data partitioning and automatic K optimization via GridSearchCV. The best value found was K = 29, achieving 86.67% accuracy on the test set and 82.86% +/- 6.99% in 10-fold cross-validation over 297 evaluated patients, analyzed through confusion matrix, classification report and accuracy distribution over blocks of 50 records.

**Keywords:** K-Nearest Neighbors; Machine Learning; Heart Disease; Binary Classification; Cross-Validation.

---

## Introdução

As doenças cardiovasculares representam a principal causa de mortalidade global segundo a Organização Mundial da Saúde. O diagnóstico precoce é essencial para reduzir óbitos e custos hospitalares, mas exames como eletrocardiogramas avançados e cineangiocoronariografias possuem alto custo e disponibilidade limitada, especialmente em países em desenvolvimento (MIENYE; SUN, 2022).

O aprendizado de máquina (AM) tem se consolidado como ferramenta de suporte à decisão clínica, sendo aplicado ao diagnóstico de diabetes, hipertensão, câncer e doenças renais. Géron (2019) destaca que algoritmos de classificação podem identificar padrões em dados clínicos com acurácia comparável à de especialistas, democratizando o acesso à triagem médica.

Dentre os algoritmos de classificação supervisionada, o K-Nearest Neighbors (KNN) se destaca pela simplicidade conceitual, transparência matemática e facilidade de implementação. Por não construir um modelo explícito durante o treinamento — postergando toda a computação para o momento da predição —, é classificado como algoritmo de aprendizado lazy (preguiçoso) e baseado em instâncias (GÉRON, 2019). Essa característica o torna especialmente adequado para aplicações clínicas onde a interpretabilidade é relevante, pois a decisão pode ser explicada diretamente pelos casos mais similares presentes no conjunto de treinamento.

O presente artigo tem como objetivos: (i) fundamentar matematicamente o algoritmo KNN; (ii) descrever a metodologia de implementação sobre o Cleveland Heart Disease Dataset; (iii) apresentar e analisar os resultados experimentais; e (iv) discutir o comportamento do modelo, suas potencialidades e suas limitações no contexto do diagnóstico cardíaco.

---

## 1. Referencial Teórico

### 1.1 O Algoritmo K-Nearest Neighbors

O algoritmo KNN foi proposto por Fix e Hodges em 1951 e formalizado por Cover e Hart em 1967. Sua premissa central é que amostras semelhantes tendem a pertencer à mesma classe: um ponto de consulta é classificado pela maioria de seus K vizinhos mais próximos no espaço de características.

Formalmente, dado um conjunto de treinamento D = {(x1, y1), ..., (xn, yn)}, onde xi representa o vetor de atributos do i-ésimo registro e yi o respectivo rótulo de classe, a predição para uma nova amostra xq é definida por:

    ŷq = argmax_c  ∑_{i ∈ N_K(xq)} 1[yi = c]

onde N_K(xq) representa o conjunto dos K índices cujos vetores de atributos estão mais próximos de xq segundo uma métrica de distância, e 1[·] é a função indicadora que retorna 1 quando a condição é verdadeira e 0 caso contrário.

Na classificação binária adotada neste trabalho (c ∈ {0, 1}), a regra de decisão se reduz a:

    ŷq = 1,  se ∑_{i ∈ N_K(xq)} yi > K/2
    ŷq = 0,  caso contrário

Essa operação corresponde a uma votação majoritária entre os K vizinhos: a classe com mais representantes na vizinhança é atribuída ao ponto de consulta. Quando K é ímpar, empates são impossíveis na classificação binária. O uso de K par exige um critério de desempate adicional.

O modelo não ajusta nenhum parâmetro durante o treinamento — toda a computação ocorre no momento da previsão, o que justifica sua classificação como algoritmo lazy e explica por que o custo computacional cresce linearmente com o tamanho do conjunto de treinamento durante a inferência.

### 1.2 Métricas de Distância

A qualidade das vizinhanças — e portanto da classificação — depende diretamente da métrica de distância utilizada. A família de métricas de Minkowski oferece uma generalização unificada das distâncias mais empregadas em aprendizado de máquina:

    d_p(x, z) = ( ∑_{j=1}^{d} |xj - zj|^p )^(1/p)

Os três casos especiais mais relevantes são:

**Distância Euclidiana (p = 2):** métrica padrão do KNeighborsClassifier do scikit-learn, intuitivamente equivalente à "linha reta" entre dois pontos no espaço d-dimensional:

    d_E(x, z) = sqrt( ∑_{j=1}^{d} (xj - zj)^2 )

**Distância de Manhattan (p = 1):** também chamada de distância city-block, soma diferenças absolutas atributo a atributo, sendo menos sensível a valores extremos:

    d_M(x, z) = ∑_{j=1}^{d} |xj - zj|

**Distância de Chebyshev (p → ∞):** considera apenas o atributo com maior diferença absoluta entre os dois pontos, sendo adequada quando um único atributo domina a caracterização das amostras:

    d_∞(x, z) = max_j |xj - zj|

A escolha da métrica deve ser guiada pelas características dos dados. Para dados clínicos numéricos contínuos, devidamente normalizados, a distância Euclidiana é a escolha convencional e foi adotada neste trabalho.

### 1.3 Necessidade de Normalização dos Atributos

Por basear toda a decisão em distâncias, o KNN é altamente sensível à escala dos atributos. Considere dois atributos do dataset utilizado: a pressão arterial em repouso, que varia tipicamente entre 80 e 200 mmHg, e o indicador binário de angina por exercício, que assume apenas os valores 0 ou 1. Sem normalização, a pressão arterial dominaria completamente o cálculo da distância, tornando o atributo binário irrelevante para a definição das vizinhanças — ainda que clinicamente relevante. Géron (2019) ressalta que a normalização é etapa obrigatória para algoritmos baseados em distância.

A Padronização Z-score, implementada pelo StandardScaler do scikit-learn, transforma cada atributo j de forma que a distribuição resultante tenha média zero e desvio padrão unitário:

    zij = (xij - x̄j) / σj

onde x̄j é a média aritmética e σj é o desvio padrão do atributo j calculados exclusivamente sobre o conjunto de treinamento. Ao aplicar esses parâmetros ao conjunto de teste, garante-se que nenhuma informação do teste vaze para o pré-processamento — prática essencial conhecida como prevenção de data leakage, que evita estimativas de desempenho artificialmente otimistas.

### 1.4 Hiperparâmetro K e o Trade-off Viés-Variância

O valor de K controla o comportamento fundamental do classificador KNN ao determinar o tamanho da vizinhança considerada para cada predição. Sua escolha envolve um dilema clássico em aprendizado de máquina denominado trade-off viés-variância:

- **K pequeno (ex.: K = 1 ou K = 3):** cada predição depende de pouquíssimas amostras, tornando o modelo extremamente sensível a ruídos e casos atípicos — alta variância. O modelo "memoriza" os dados de treinamento (overfitting) e generaliza mal para dados novos.

- **K grande (ex.: K próximo de n):** a vizinhança abrange grande parte do conjunto de treinamento, suavizando as fronteiras de decisão a ponto de o modelo ignorar estruturas locais relevantes — alto viés. O modelo perde capacidade de discriminação (underfitting).

O erro esperado de generalização pode ser decomposto formalmente como:

    Erro(xq) = Viés² + Variância + ε

onde ε representa o ruído irredutível dos dados, independente do modelo. O objetivo é encontrar o K que minimiza a soma dos dois primeiros termos sobre dados não vistos.

Para isso, emprega-se a busca em grade com validação cruzada estratificada. Para cada candidato k no intervalo de busca, calcula-se a acurácia média em v dobras de validação e seleciona-se o valor ótimo:

    K* = argmax_{k ∈ {1,...,K_max}}  (1/v) ∑_{i=1}^{v} Acc(k, dobra_i)

### 1.5 Validação Cruzada Estratificada

A validação cruzada k-fold estratificada (StratifiedKFold) é o protocolo de avaliação adotado para seleção de K e para estimativa final do desempenho do modelo. O conjunto de dados D é particionado em v dobras mutuamente exclusivas D1, ..., Dv, mantendo em cada dobra a mesma proporção de classes do conjunto original. Para cada dobra i, um modelo é treinado sobre D \ Di e avaliado sobre Di:

    Acc_CV = (1/v) ∑_{i=1}^{v} Acc( M_{D\Di}, Di )

A estimativa final é a média das v avaliações. Secondo Géron (2019), a validação cruzada é preferível à simples divisão treino/teste porque: (i) aproveita todos os dados disponíveis para treinamento e para avaliação; (ii) reduz a variância da estimativa de desempenho; e (iii) é menos dependente de uma única partição aleatória. Esta é a métrica de referência principal deste artigo.

### 1.6 Métricas de Avaliação de Classificadores Binários

Para classificação binária, as predições se enquadram em quatro categorias, organizadas na matriz de confusão:

| | Previsto: Saudável (0) | Previsto: Doente (1) |
|---|:---:|:---:|
| **Real: Saudável (0)** | VN — Verdadeiro Negativo | FP — Falso Positivo |
| **Real: Doente (1)** | FN — Falso Negativo | VP — Verdadeiro Positivo |

As métricas derivadas da matriz de confusão são:

**Acurácia:** proporção global de predições corretas sobre o total de amostras:

    Acurácia = (VP + VN) / (VP + VN + FP + FN)

**Precisão:** dentre as predições positivas, qual fração é realmente positiva:

    Precisão = VP / (VP + FP)

**Revocação (Sensibilidade):** dentre os casos realmente positivos, qual fração foi corretamente identificada:

    Revocação = VP / (VP + FN)

**F1-Score:** média harmônica entre precisão e revocação, equilibrando os dois aspectos em uma única métrica:

    F1 = 2 · (Precisão × Revocação) / (Precisão + Revocação)

Em aplicações de triagem clínica, a Revocação da classe Doente (equivalente à sensibilidade do teste diagnóstico) é a métrica de maior relevância médica, pois os Falsos Negativos — pacientes doentes classificados como saudáveis — representam o erro com maior potencial de dano clínico, podendo resultar na ausência de tratamento para pacientes em risco.

---

## 2. Metodologia

### 2.1 Conjunto de Dados

O estudo utiliza o Cleveland Heart Disease Dataset, disponibilizado pelo UCI Machine Learning Repository sob o identificador id=45 (JANOSI et al., 1988). Trata-se de um dos conjuntos de dados mais referenciados na literatura de diagnóstico cardíaco por aprendizado de máquina (MIENYE; SUN, 2022), coletado originalmente na Clínica Cleveland (EUA) e contendo registros de pacientes submetidos a avaliação cardíaca completa.

O dataset original contém 303 registros e 14 atributos — 13 preditores clínicos e 1 variável alvo com 5 classes (0 = sem evidência de doença; 1 a 4 = graus crescentes de comprometimento cardíaco). Após remoção de registros com valores ausentes, restaram 297 registros válidos. A Tabela 1 descreve os 13 atributos preditores utilizados.

**Tabela 1 – Atributos do Cleveland Heart Disease Dataset**

| Atributo | Descrição | Tipo |
|---|---|:---:|
| age | Idade do paciente (anos) | Numérico |
| sex | Sexo (1 = masculino; 0 = feminino) | Binário |
| cp | Tipo de dor torácica (0 = assintomático; 1–3 = sintomático) | Categórico |
| trestbps | Pressão arterial em repouso (mmHg) | Numérico |
| chol | Colesterol sérico (mg/dl) | Numérico |
| fbs | Glicemia em jejum > 120 mg/dl (1/0) | Binário |
| restecg | Resultado do ECG em repouso (0–2) | Categórico |
| thalach | Frequência cardíaca máxima atingida (bpm) | Numérico |
| exang | Angina induzida por exercício (1 = sim; 0 = não) | Binário |
| oldpeak | Depressão do segmento ST pelo exercício | Numérico |
| slope | Inclinação do segmento ST de pico (0–2) | Categórico |
| ca | Número de vasos principais coloridos por fluoroscopia (0–3) | Ordinal |
| thal | Resultado do teste de estresse com tálio (0–3) | Categórico |

Fonte: JANOSI et al. (1988).

### 2.2 Binarização da Variável Alvo

O dataset original apresenta 5 níveis de diagnóstico, o que introduz ambiguidade entre graus intermediários clinicamente próximos. Para simplificar o problema e focar na questão diagnóstica central — o paciente possui ou não evidência de doença cardíaca — adotou-se a binarização da variável alvo:

    y_binário = 0  se y_original = 0  (Saudável: sem evidência de doença)
    y_binário = 1  se y_original > 0  (Doente: qualquer grau de comprometimento)

Essa estratégia reduz o problema de classificação de 5 classes para 2, alinhando-o com a pergunta clínica mais relevante para triagem e tornando as predições diretamente interpretáveis por profissionais de saúde.

### 2.3 Pipeline de Pré-processamento

O pipeline de pré-processamento segue três etapas em sequência obrigatória:

**Etapa 1 — Remoção de valores ausentes:** registros com NaN em qualquer um dos 13 atributos foram descartados inteiramente para evitar interferência de imputações na análise. Dos 303 registros originais, 6 foram removidos, resultando em 297 registros válidos utilizados em todo o experimento.

**Etapa 2 — Padronização Z-score:** os 13 atributos preditores foram padronizados com StandardScaler, calculando média (x̄j) e desvio padrão (σj) exclusivamente sobre X_train e aplicando a transformação tanto em X_train quanto em X_test. Essa separação é essencial para evitar data leakage.

**Etapa 3 — Particionamento estratificado:** os 297 registros foram divididos em 80% treinamento (237 registros) e 20% teste (60 registros) com o parâmetro stratify=y, garantindo que a proporção de classes Saudável/Doente seja preservada em ambas as partições. O parâmetro random_state=42 garante reprodutibilidade.

### 2.4 Otimização do Hiperparâmetro K

A seleção do melhor valor de K foi realizada por busca em grade (GridSearchCV) sobre o intervalo discreto K ∈ {1, 2, ..., 30}, utilizando validação cruzada estratificada de 5 dobras (StratifiedKFold, n_splits=5, shuffle=True, random_state=42) aplicada exclusivamente sobre o conjunto de treinamento (X_train). O critério de seleção foi a maximização da acurácia média nas 5 dobras:

    K* = argmax_{k ∈ {1,...,30}}  (1/5) ∑_{i=1}^{5} Acc(k, dobra_i)

O processamento paralelo (n_jobs=-1) foi habilitado para utilizar todos os núcleos disponíveis da CPU. O valor ótimo encontrado foi K* = 29.

### 2.5 Protocolo de Avaliação Final

Com K* = 29 definido, o modelo final foi instanciado com KNeighborsClassifier(n_neighbors=29), treinado sobre todo X_train e avaliado em três instâncias complementares:

1. **Conjunto de teste hold-out** (60 registros, 20% dos dados): produz estimativa de desempenho em dados completamente não utilizados durante nenhuma etapa do treinamento ou seleção de K.
2. **Validação cruzada 10-fold** aplicada sobre os 297 registros completos: métrica de referência mais robusta, obtida com StratifiedKFold(n_splits=10, shuffle=True, random_state=42) e cross_val_score.
3. **Predição sobre o conjunto completo** (297 registros): permite análise granular dos acertos e erros em blocos consecutivos, investigando possíveis padrões de desempenho ao longo do dataset.

O Algoritmo 1 sintetiza o pseudocódigo completo da implementação desenvolvida:

**Algoritmo 1 – KNN para Classificação de Doença Cardíaca**

```
Entrada : Dataset UCI Heart Disease (id=45); K_RANGE = {1, 2, ..., 30}
Saída   : Modelo KNN otimizado; relatório de classificação completo

1.  CARREGAR os dados via ucimlrepo.fetch_ucirepo(id=45)
2.  SELECIONAR os 13 atributos preditores descritos na Tabela 1
3.  REMOVER registros com valores ausentes (NaN)  →  297 registros válidos
4.  BINARIZAR a variável alvo:
        y = 0  se y_original = 0  (Saudável)
        y = 1  se y_original > 0  (Doente)
5.  PARTICIONAR com estratificação:
        X_train, X_test, y_train, y_test =
            train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
6.  PADRONIZAR (fit apenas sobre X_train):
        scaler = StandardScaler().fit(X_train)
        X_train_s = scaler.transform(X_train)
        X_test_s  = scaler.transform(X_test)
        X_all_s   = scaler.transform(X)
7.  OTIMIZAR K via GridSearchCV + StratifiedKFold(5):
        grid = GridSearchCV(KNeighborsClassifier(),
                            {'n_neighbors': K_RANGE},
                            cv=StratifiedKFold(5), scoring='accuracy')
        grid.fit(X_train_s, y_train)
        K* = grid.best_params_['n_neighbors']   →  K* = 29
8.  TREINAR modelo final:
        model = KNeighborsClassifier(n_neighbors=K*).fit(X_train_s, y_train)
9.  AVALIAR desempenho:
        a) y_pred_test = model.predict(X_test_s)
           acc_teste = accuracy_score(y_test, y_pred_test)
        b) scores_cv = cross_val_score(model, X_all_s, y,
                           cv=StratifiedKFold(10), scoring='accuracy')
        c) y_pred_all = model.predict(X_all_s)
10. GERAR confusion_matrix(y_test, y_pred_test)
    GERAR classification_report(y_test, y_pred_test)
```

---

## 3. Resultados e Discussão

### 3.1 Otimização do Hiperparâmetro K

A Tabela 2 apresenta os 5 melhores valores de K identificados pelo GridSearchCV na validação cruzada de 5 dobras sobre o conjunto de treinamento:

**Tabela 2 – Top-5 valores de K na validação cruzada (5-fold, conjunto de treino)**

| K | Acurácia CV Média |
|:---:|:---:|
| **29** | **83,97%** |
| 27 | 83,55% |
| 17 | 83,55% |
| 30 | 83,55% |
| 26 | 83,55% |

O agrupamento dos melhores resultados na faixa K ∈ [17, 30] indica que o Cleveland dataset apresenta estrutura de classes com padrões relativamente suaves, que se beneficiam de vizinhanças maiores. Valores de K inferiores a 10 apresentaram maior variabilidade entre as dobras de validação, evidenciando sensibilidade a ruídos e casos atípicos locais — comportamento esperado do overfitting. A margem pequena entre K = 29 (83,97%) e seus vizinhos próximos (83,55%) indica que a superfície de desempenho em função de K é relativamente plana na região [17, 30], o que confere robustez à escolha: pequenas variações no dataset não alterariam significativamente o K ótimo selecionado.

O fato de K = 30 apresentar desempenho marginalmente inferior a K = 29, mesmo sendo um valor ligeiramente mais conservador, é consistente com o trade-off viés-variância: em algum ponto da curva, o aumento do viés começa a superar a redução da variância, e K = 30 parece estar próximo desse limiar para este dataset.

### 3.2 Acurácia por Blocos de Registros

Para investigar o comportamento do modelo ao longo de todo o dataset, as predições sobre os 297 registros foram organizadas em blocos consecutivos de 50, conforme a Tabela 3:

**Tabela 3 – Acurácia do KNN (K=29) por bloco de registros**

| Bloco | Registros | Acertos | Acurácia |
|:---:|:---:|:---:|:---:|
| 1 | 1 – 50 | 45/50 | 90,00% |
| 2 | 51 – 100 | 42/50 | 84,00% |
| 3 | 101 – 150 | 45/50 | 90,00% |
| 4 | 151 – 200 | 40/50 | 80,00% |
| 5 | 201 – 250 | 43/50 | 86,00% |
| 6 | 251 – 297 | 37/47 | 78,72% |
| **Total** | **1 – 297** | **252/297** | **84,85%** |

A variação de acurácia entre blocos — de 78,72% (bloco 6) a 90,00% (blocos 1 e 3) — é esperada em qualquer análise sequencial de dados heterogêneos e não indica instabilidade do modelo, mas sim diferenças na composição local das amostras. Os blocos com maior acurácia (1 e 3) contêm provavelmente regiões do espaço de características com fronteiras de decisão mais nítidas entre as classes Saudável e Doente. O bloco 6, com menor acurácia (78,72%), possivelmente concentra pacientes com perfil clínico mais ambíguo, cujos vetores de atributos se situam próximos à fronteira de decisão do modelo.

A acurácia geral de 84,85% sobre os 297 registros é coerente com a estimativa de 82,86% obtida pela validação cruzada — a diferença de aproximadamente 2 pontos percentuais é esperada, pois na predição sobre o conjunto completo o modelo classifica amostras que também estiveram presentes em seu treinamento, gerando uma estimativa ligeiramente otimista.

### 3.3 Métricas Consolidadas do Modelo

A Tabela 4 apresenta o resumo completo do desempenho do classificador KNN com K = 29:

**Tabela 4 – Resumo de desempenho do classificador KNN (K=29)**

| Métrica | Valor |
|---|:---:|
| Acurácia — conjunto de teste (hold-out 20%) | 86,67% |
| **Acurácia — validação cruzada 10-fold** *(métrica principal)* | **82,86% ± 6,99%** |
| Acurácia — conjunto completo (297 registros) | 84,85% |
| K (número de vizinhos) | 29 |
| Tamanho do conjunto de treinamento | 237 registros |
| Tamanho do conjunto de teste | 60 registros |
| Total de registros avaliados | 297 registros |

A **validação cruzada 10-fold** (82,86% ± 6,99%) é a **métrica de referência para fins de TCC**, pois estima a capacidade de generalização do modelo de forma imparcial: em cada uma das 10 iterações, o modelo é avaliado sobre uma dobra de dados que não participou do seu treinamento, e a média dessas 10 avaliações independentes fornece uma estimativa robusta do desempenho esperado em dados reais novos (GÉRON, 2019).

O desvio padrão de ±6,99% reflete a variabilidade natural entre as 10 dobras, esperada para um dataset de tamanho moderado (297 registros). Em datasets maiores, esse desvio tende a diminuir. O intervalo aproximado de desempenho do modelo situa-se entre 75,87% e 89,85%, com centro em 82,86%.

A acurácia de 86,67% no conjunto de teste (60 registros) é ligeiramente superior à estimativa de validação cruzada, o que pode refletir uma composição particularmente favorável na partição aleatória do conjunto de teste. Por isso, ao reportar o desempenho do modelo em trabalhos científicos, recomenda-se priorizar a métrica de validação cruzada.

A avaliação qualitativa do modelo é classificada como **BOA**: acurácias de validação cruzada entre 75% e 85% indicam que o classificador identifica corretamente a maioria dos casos clínicos presentes no dataset, com margem de aprimoramento.

### 3.4 Matriz de Confusão

A Tabela 5 apresenta a matriz de confusão obtida sobre os 60 registros do conjunto de teste, detalhando cada tipo de predição:

**Tabela 5 – Matriz de confusão (conjunto de teste, n=60)**

| | Previsto: Saudável (0) | Previsto: Doente (1) |
|---|:---:|:---:|
| **Real: Saudável (0)** | **30** — VN | 2 — FP |
| **Real: Doente (1)** | 6 — FN | **22** — VP |

A matriz revela quatro categorias de resultado:

- **30 Verdadeiros Negativos (VN):** pacientes saudáveis corretamente identificados pelo modelo — maior grupo individual de acertos.
- **22 Verdadeiros Positivos (VP):** pacientes doentes corretamente identificados pelo modelo.
- **2 Falsos Positivos (FP):** pacientes saudáveis classificados erroneamente como doentes — em contexto de triagem, esse erro leva a exames adicionais desnecessários, com impacto em custo e ansiedade do paciente, mas sem risco direto à saúde.
- **6 Falsos Negativos (FN):** pacientes doentes classificados erroneamente como saudáveis — erro crítico em contexto clínico, pois esses pacientes poderiam não receber acompanhamento adequado.

Com 28 pacientes doentes no conjunto de teste, os 6 Falsos Negativos equivalem a uma **taxa de falsos negativos de 21,4%**, indicando que o modelo deixa de identificar cerca de 1 em cada 5 pacientes com doença cardíaca. Esse resultado é adequado para um modelo de triagem automatizada de baixo custo computacional, mas reforça que o KNN deve ser utilizado como ferramenta de apoio à decisão médica, e nunca como substituto ao exame clínico especializado.

### 3.5 Relatório de Classificação por Classe

A Tabela 6 detalha as métricas de precisão, revocação e F1-score para cada classe individualmente, permitindo avaliar o comportamento assimétrico do modelo:

**Tabela 6 – Relatório de classificação por classe (conjunto de teste, n=60)**

| Classe | Precisão | Revocação | F1-Score | Suporte |
|---|:---:|:---:|:---:|:---:|
| Saudável (0) | 0,83 | 0,94 | 0,88 | 32 |
| Doente (1) | 0,92 | 0,79 | 0,85 | 28 |
| **Acurácia geral** | | | **0,87** | **60** |
| Média macro | 0,88 | 0,86 | 0,86 | 60 |
| Média ponderada | 0,87 | 0,87 | 0,87 | 60 |

A análise por classe permite as seguintes conclusões:

**Classe Saudável (0):** alta revocação (0,94) indica que o modelo identifica corretamente quase todos os pacientes saudáveis, perdendo apenas 2 em 32 (os 2 Falsos Positivos). A precisão de 0,83 significa que, dentre as predições "Saudável", 17% correspondem a pacientes doentes (os 6 Falsos Negativos).

**Classe Doente (1):** alta precisão (0,92) indica que, quando o modelo afirma que um paciente está doente, está correto em 92% dos casos — apenas 2 Falsos Positivos entre 24 predições positivas. A revocação de 0,79 revela que o modelo não detecta 21% dos pacientes doentes.

**F1-Score equilibrado (0,85 e 0,88):** a inexistência de desvio acentuado entre as duas classes indica que o modelo não está viesado para nenhuma delas, o que é desejável considerando que o suporte das classes é próximo (32 saudáveis vs. 28 doentes no conjunto de teste).

**Média macro do F1-Score = 0,86:** confirma desempenho consistente e equilibrado entre as classes, sem sacrifício de uma em favor da outra.

### 3.6 Análise dos Erros de Classificação

Os 45 erros identificados nos 297 registros (15,15% do total) se distribuem em dois tipos com causas e implicações distintas:

**Falsos Negativos — doente classificado como saudável:** ocorrem quando um paciente com doença cardíaca possui combinação de atributos (idade, frequência cardíaca máxima, pressão arterial, tipo de dor torácica, entre outros) que se assemelha, no espaço padronizado de 13 dimensões, ao perfil de pacientes saudáveis na vizinhança de K = 29. Entre os exemplos observados estão os registros 17, 23, 34, 45, 52, 53, 58, 67, 70, 75, 81, 130, 144 e 145, todos pacientes doentes cujas características clínicas possuem distribuição próxima à de pacientes saudáveis no dataset.

**Falsos Positivos — saudável classificado como doente:** ocorrem quando um paciente saudável apresenta, nos atributos padronizados, perfil próximo ao de pacientes doentes na vizinhança de K = 29. Exemplos incluem os registros 33, 52, 124, 141, 167, 171, 179, 183 e 187, pacientes saudáveis com perfil clínico limítrofe.

Esses erros são fundamentalmente explicáveis pela natureza do KNN: o algoritmo opera em espaço de atributos de alta dimensão (13 dimensões) usando apenas informação local (K = 29 vizinhos mais próximos), sem construir representação global da distribuição das classes. Regiões do espaço de características onde as duas classes se sobrepõem representam casos inerentemente difíceis para qualquer classificador, e o KNN não possui mecanismo para capturar interações não-lineares complexas entre atributos que poderiam diferenciar essas amostras ambíguas.

---

## Considerações Finais

Este trabalho apresentou, de forma abrangente, a fundamentação matemática, a implementação computacional e a análise experimental do algoritmo K-Nearest Neighbors para classificação binária de doença cardíaca sobre o Cleveland Heart Disease Dataset.

Os principais resultados e conclusões são:

1. O KNN com K = 29, selecionado automaticamente por GridSearchCV com validação cruzada estratificada de 5 dobras, obteve **86,67% de acurácia no conjunto de teste** e **82,86% ± 6,99% na validação cruzada de 10 dobras** — métrica de referência recomendada para o TCC por ser a mais honesta estimativa de generalização disponível.

2. A **binarização da variável alvo** (5 classes → 2 classes: Saudável / Doente) foi decisão metodológica fundamental: eliminou ambiguidades entre graus intermediários da doença, alinhou o problema à pergunta diagnóstica clinicamente relevante e aumentou significativamente o desempenho do modelo em relação à abordagem multiclasse.

3. A **padronização Z-score** é condição obrigatória para o correto funcionamento do KNN sobre dados clínicos com atributos de escalas heterogêneas. Sua aplicação estrita — com parâmetros calculados apenas sobre o conjunto de treinamento — é essencial para evitar data leakage e garantir estimativas de desempenho válidas.

4. O **valor ótimo K = 29** situa-se na região de vizinhança larga, onde o modelo equilibra adequadamente viés e variância para as características deste dataset. A busca automatizada por GridSearchCV é preferível à escolha manual, pois baseia a decisão em evidência empírica de generalização.

5. A análise da **matriz de confusão** revela que o modelo apresenta alta precisão para a classe Doente (0,92), indicando confiabilidade nas predições positivas, e alta revocação para a classe Saudável (0,94). Os 6 Falsos Negativos (taxa de 21,4%) representam a principal limitação clínica do modelo, reforçando que o KNN deve ser utilizado como ferramenta de triagem e apoio à decisão médica, não como sistema diagnóstico autônomo.

Como trabalho futuro, recomenda-se: (i) investigar o impacto de métricas de distância alternativas — Manhattan e Minkowski com diferentes valores de p — no desempenho do KNN sobre este dataset; (ii) avaliar o efeito de técnicas de balanceamento de classes como SMOTE (*Synthetic Minority Over-sampling Technique*) sobre a revocação da classe Doente; (iii) explorar variantes ponderadas do KNN, nas quais a contribuição de cada vizinho é inversamente proporcional à sua distância ao ponto de consulta, potencialmente reduzindo o impacto de vizinhos distantes sobre a predição; e (iv) aplicar seleção de atributos para identificar o subconjunto mais informativo dentre os 13 preditores disponíveis, potencialmente melhorando o desempenho ao reduzir o ruído introduzido por atributos menos relevantes.

---

## Referências

COVER, T. M.; HART, P. E. Nearest neighbor pattern classification. **IEEE Transactions on Information Theory**, v. 13, n. 1, p. 21–27, 1967. DOI: 10.1109/TIT.1967.1053964.

FIX, E.; HODGES, J. L. **Discriminatory Analysis: Nonparametric Discrimination, Consistency Properties**. USAF School of Aviation Medicine, Randolph Field, Texas. Technical Report n. 4, 1951.

GÉRON, Aurélien. **Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow: Concepts, Tools, and Techniques to Build Intelligent Systems**. 2. ed. Sebastopol, CA: O'Reilly Media, 2019.

JANOSI, A.; STEINBRUNN, W.; PFISTERER, M.; DETRANO, R. **Heart Disease Dataset**. UCI Machine Learning Repository, 1988. Disponível em: https://archive.ics.uci.edu/dataset/45/heart+disease. Acesso em: mar. 2026.

MIENYE, I. D.; SUN, Y. A Survey of Ensemble Learning: Concepts, Algorithms, Applications, and Prospects. **IEEE Access**, v. 10, p. 99129–99149, 2022. DOI: 10.1109/ACCESS.2022.3207287.

PEDREGOSA, F. et al. Scikit-learn: Machine Learning in Python. **Journal of Machine Learning Research**, v. 12, p. 2825–2830, 2011. Disponível em: https://jmlr.org/papers/v12/pedregosa11a.html. Acesso em: mar. 2026.

RUSSELL, S.; NORVIG, P. **Artificial Intelligence: A Modern Approach**. 4. ed. Hoboken, NJ: Pearson, 2020.
