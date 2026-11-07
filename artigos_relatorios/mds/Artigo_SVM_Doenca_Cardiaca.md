# SUPPORT VECTOR MACHINE APLICADO AO DIAGNÓSTICO DE DOENÇA CARDÍACA: FUNDAMENTOS MATEMÁTICOS, IMPLEMENTAÇÃO E ANÁLISE DE DESEMPENHO

André Felipe

Faculdade de Tecnologia de Guaratinguetá

e-mail: andressmota78@gmail.com

---

## Resumo

Este artigo apresenta a aplicação do algoritmo Support Vector Machine (SVM) para a classificação binária de doença cardíaca utilizando o Cleveland Heart Disease Dataset (UCI Machine Learning Repository, id=45). São cobertos os fundamentos matemáticos do algoritmo, incluindo a formulação do problema de otimização de margem máxima, a introdução de variáveis de folga para margens suaves, o truque do kernel e as funções RBF, linear e polinomial. A implementação foi desenvolvida em Python com a biblioteca scikit-learn, empregando padronização Z-score, particionamento estratificado e otimização automática dos hiperparâmetros C, kernel e gamma via GridSearchCV. A melhor combinação encontrada foi C = 0,1, kernel RBF e gamma = scale, obtendo acurácia de 86,67% no conjunto de teste e 83,51% ± 7,66% na validação cruzada de 10 dobras. Os 297 pacientes avaliados foram analisados por matriz de confusão, relatório de classificação e distribuição de acertos em blocos de 50 registros.

**Palavras-chave:** Support Vector Machine; Kernel RBF; Aprendizado de Máquina; Doença Cardíaca; Classificação Binária; Validação Cruzada.

---

## Abstract

This paper presents the application of the Support Vector Machine (SVM) algorithm for binary classification of heart disease using the Cleveland Heart Disease Dataset (UCI Machine Learning Repository, id=45). The mathematical foundations of the algorithm are covered, including the maximum-margin optimization formulation, soft-margin slack variables, the kernel trick, and RBF, linear and polynomial kernel functions. The Python implementation uses Z-score standardization, stratified data partitioning and automatic hyperparameter optimization of C, kernel and gamma via GridSearchCV. The best combination found was C = 0.1, RBF kernel and gamma = scale, achieving 86.67% accuracy on the test set and 83.51% +/- 7.66% in 10-fold cross-validation over 297 evaluated patients, analyzed via confusion matrix, classification report and accuracy distribution over 50-record blocks.

**Keywords:** Support Vector Machine; RBF Kernel; Machine Learning; Heart Disease; Binary Classification; Cross-Validation.

---

## Introdução

As doenças cardiovasculares representam a principal causa de mortalidade global segundo a Organização Mundial da Saúde. No Brasil, respondem por mais de 300 mil óbitos por ano, muitos dos quais poderiam ser evitados ou minimizados com diagnóstico precoce (MIENYE; SUN, 2022). O diagnóstico clínico preciso depende de exames de alta complexidade e custo — como cineangiocoronariografia e cintilografia miocárdica —, cujo acesso é restrito em sistemas de saúde pública. Nesse contexto, ferramentas de triagem automatizada baseadas em aprendizado de máquina (AM) representam uma alternativa promissora para auxiliar profissionais de saúde na identificação de pacientes em risco a partir de dados clínicos de rotina.

O aprendizado de máquina tem se consolidado como ferramenta de suporte à decisão clínica em diversas especialidades. Géron (2019) destaca que algoritmos de classificação supervisionada são capazes de identificar padrões em dados clínicos multidimensionais com acurácia comparável à de especialistas, democratizando o acesso à triagem diagnóstica e reduzindo a carga sobre sistemas de saúde sobrecarregados.

Dentre os algoritmos de classificação supervisionada, o Support Vector Machine (SVM) se destaca pelo sólido embasamento teórico na teoria estatística da aprendizagem — notadamente a teoria de Vapnik-Chervonenkis (VC) — e pela capacidade demonstrada de generalização eficaz mesmo em espaços de alta dimensionalidade. Introduzido por Cortes e Vapnik (1995) na forma atual com margens suaves, o SVM formula o problema de classificação como um problema de otimização convexa que busca o hiperplano decisório de margem máxima entre as classes, combinando garantias teóricas de generalização com desempenho prático competitivo (CORTES; VAPNIK, 1995).

Ao contrário de algoritmos que buscam predições locais com base em vizinhança — como o K-Nearest Neighbors (KNN) — o SVM constrói uma representação global das fronteiras de decisão definida por um subconjunto mínimo de amostras de treinamento denominadas vetores de suporte. Essa característica confere ao modelo robustez a ruídos e outliers, uma vez que a maioria das amostras é irrelevante para a geometria da fronteira de decisão após o treinamento (RUSSELL; NORVIG, 2020).

O presente artigo tem como objetivos: (i) fundamentar matematicamente o algoritmo SVM desde a formulação de margem rígida até a formulação de margem suave e o truque do kernel; (ii) descrever a metodologia de implementação sobre o Cleveland Heart Disease Dataset; (iii) apresentar e analisar os resultados experimentais; e (iv) discutir o comportamento do modelo, suas potencialidades e limitações no contexto do diagnóstico cardíaco, comparando-o com o classificador KNN conforme previsto na literatura.

---

## 1. Referencial Teórico

### 1.1 O Algoritmo Support Vector Machine

O SVM foi introduzido por Boser, Guyon e Vapnik (1992) na formulação com kernel e consolidado por Cortes e Vapnik (1995) com a incorporação das margens suaves. Sua premissa central é encontrar, no espaço de características, o hiperplano decisório que maximiza a margem de separação entre as classes — ou seja, a maior distância possível entre o hiperplano e os pontos de treinamento mais próximos de cada classe.

Dado um conjunto de treinamento D = {(x₁, y₁), ..., (xₙ, yₙ)}, onde xᵢ ∈ ℝᵈ é o vetor de atributos e yᵢ ∈ {-1, +1} é o rótulo de classe, um hiperplano de separação em ℝᵈ é definido por:

    f(x) = wᵀx + b = 0

onde w ∈ ℝᵈ é o vetor normal ao hiperplano e b ∈ ℝ é o viés (bias). A classificação de um novo ponto xq é dada pelo sinal da função de decisão:

    ŷq = sinal( wᵀxq + b )

### 1.2 Maximização da Margem — Formulação de Margem Rígida

Para dados linearmente separáveis, a **margem geométrica** entre as duas classes é a distância entre os dois hiperplanos de suporte paralelos, definidos pelos pontos de treinamento mais próximos da fronteira:

    Hiperplano de suporte positivo:  wᵀxᵢ + b = +1   (para yᵢ = +1)
    Hiperplano de suporte negativo:  wᵀxᵢ + b = -1   (para yᵢ = -1)

A margem é a distância perpendicular entre esses dois hiperplanos, calculada pela norma euclidiana do vetor normal:

    Margem = 2 / ‖w‖

Maximizar a margem equivale a minimizar ‖w‖, ou de forma equivalente — por conveniência matemática — minimizar ½ ‖w‖². O problema de otimização primal de margem rígida é:

    min_{w,b}    ½ ‖w‖²

    sujeito a:   yᵢ(wᵀxᵢ + b) ≥ 1,   para todo i = 1, ..., n

Esse é um problema de programação quadrática (QP) convexo, com solução única e global garantida. A restrição yᵢ(wᵀxᵢ + b) ≥ 1 assegura que nenhum ponto de treinamento viola a margem.

### 1.3 Vetores de Suporte

A solução do problema de otimização apresenta uma propriedade fundamental: apenas os pontos de treinamento que satisfazem a restrição com igualdade — denominados **vetores de suporte** — têm influência sobre a posição e orientação do hiperplano ótimo. Formalmente, um ponto xᵢ é vetor de suporte quando:

    yᵢ(wᵀxᵢ + b) = 1

Todos os demais pontos, que satisfazem a restrição estritamente (com desigualdade), não contribuem para a definição do hiperplano. Essa propriedade de esparsidade, derivada das condições de Karush-Kuhn-Tucker (KKT), confere ao SVM robustez a outliers e pontos de ruído que estejam distantes da fronteira de decisão — ao contrário do KNN, que considera um conjunto fixo de vizinhos locais para cada predição.

O vetor de pesos w é expresso como combinação linear dos vetores de suporte:

    w = ∑_{i: αᵢ > 0}  αᵢ yᵢ xᵢ

onde αᵢ são os multiplicadores de Lagrange correspondentes. Apenas os vetores de suporte possuem αᵢ > 0.

### 1.4 Formulação Dual de Lagrange

Introduzindo os multiplicadores de Lagrange αᵢ ≥ 0, o problema primal é transformado em sua formulação dual:

    max_α    ∑_{i} αᵢ − ½ ∑_{i} ∑_{j} αᵢ αⱼ yᵢ yⱼ xᵢᵀxⱼ

    sujeito a:   ∑_{i} αᵢ yᵢ = 0
                 αᵢ ≥ 0,   para todo i

A formulação dual é vantajosa porque: (i) o problema cresce com o número de amostras n, não com a dimensionalidade d dos atributos; e (ii) os produtos internos xᵢᵀxⱼ podem ser substituídos por funções de kernel K(xᵢ, xⱼ), permitindo a classificação em espaços de alta dimensão implicitamente.

### 1.5 Formulação de Margem Suave — O Parâmetro C

O caso prático com dados reais raramente é linearmente separável no espaço original de atributos. Cortes e Vapnik (1995) introduziram **variáveis de folga** ξᵢ ≥ 0 que permitem que alguns pontos violem a margem, ao preço de uma penalidade proporcional ao parâmetro C:

    min_{w,b,ξ}    ½ ‖w‖² + C ∑_{i=1}^{n} ξᵢ

    sujeito a:   yᵢ(wᵀxᵢ + b) ≥ 1 − ξᵢ
                 ξᵢ ≥ 0,   para todo i

O hiperparâmetro **C > 0** controla o equilíbrio entre a maximização da margem e a penalidade por violações:

- **C pequeno** (ex.: C = 0,1): margem mais larga, maior tolerância a erros de classificação no conjunto de treinamento. O modelo prioriza generalização e aceita mais violações — comportamento equivalente a maior regularização. Tende a reduzir o risco de overfitting.

- **C grande** (ex.: C = 100): margem mais estreita, menor tolerância a erros. O modelo força a correta classificação de quase todos os pontos de treinamento, podendo decorar casos específicos e reduzir a capacidade de generalização — overfitting.

No experimento deste trabalho, o GridSearchCV identificou C = 0,1 como o valor ótimo, sugerindo que o dataset Cleveland se beneficia de maior regularização — provavelmente porque os dados de 297 pacientes apresentam sobreposição natural entre as classes Saudável e Doente no espaço de atributos clínicos.

Na formulação dual correspondente, as condições KKT se tornam:

    0 ≤ αᵢ ≤ C,   ∑_{i} αᵢ yᵢ = 0

O upper bound C nos multiplicadores αᵢ é a consequência direta da variável de folga ξᵢ na formulação primal.

### 1.6 O Truque do Kernel

Para dados não linearmente separáveis no espaço original ℝᵈ, o SVM utiliza uma transformação φ: ℝᵈ → ℋ que mapeia as amostras para um espaço de Hilbert de maior dimensão ℋ, onde a separabilidade linear é possível. A fronteira de decisão não-linear em ℝᵈ corresponde a uma fronteira linear no espaço ℋ.

O **truque do kernel** (Boser, Guyon e Vapnik, 1992) evita o cálculo explícito da transformação φ, substituindo diretamente os produtos internos na formulação dual por uma **função de kernel** K(xᵢ, xⱼ):

    K(xᵢ, xⱼ) = φ(xᵢ)ᵀ φ(xⱼ)

O produto interno no espaço transformado ℋ é calculado indiretamente usando apenas os vetores originais em ℝᵈ, sem materializar φ(xᵢ) — que pode ter dimensão infinita. O desenvolvimento central do SVM em sua formulação kernelizada substitui xᵢᵀxⱼ → K(xᵢ, xⱼ) tanto no problema dual quanto na função de decisão:

    f(x) = sinal( ∑_{i: αᵢ > 0} αᵢ yᵢ K(xᵢ, x) + b )

Para que uma função K(·,·) seja um kernel válido, ela deve ser **semidefinida positiva** — condição que garante a existência do espaço ℋ correspondente (condição de Mercer, 1909).

### 1.7 Funções de Kernel

#### 1.7.1 Kernel Linear

    K(xᵢ, xⱼ) = xᵢᵀxⱼ

O kernel linear não realiza nenhuma transformação: corresponde ao SVM clássico no espaço original de atributos. É interpretável — o vetor de pesos w define a importância de cada atributo — e eficiente computacionalmente. Recomendado quando o número de atributos é grande em relação ao número de amostras, ou quando os dados são aproximadamente linearmente separáveis. No experimento deste artigo, o kernel linear obteve 81,00% de acurácia CV, ficando abaixo do kernel RBF.

#### 1.7.2 Kernel Polinomial

    K(xᵢ, xⱼ) = (γ xᵢᵀxⱼ + r)^d

onde d é o grau do polinômio, γ controla a escala dos produtos internos e r é o coeficiente independente. O kernel polinomial de grau d captura interações entre atributos de até ordem d, aumentando a expressividade da fronteira de decisão. Para o dataset Cleveland, o kernel polinomial obteve 81,00% de acurácia CV — desempenho equivalente ao kernel linear, sugerindo que as interações polinomiais polinomiais não acrescentam discriminabilidade relevante para os dados clínicos utilizados.

#### 1.7.3 Kernel RBF (Radial Basis Function)

O kernel RBF — também denominado kernel gaussiano — é o mais amplamente utilizado em aplicações de aprendizado de máquina (GÉRON, 2019):

    K(xᵢ, xⱼ) = exp(−γ ‖xᵢ − xⱼ‖²)

onde γ > 0 controla a "largura" da função gaussiana no espaço de atributos. Geometricamente, K(xᵢ, xⱼ) representa o grau de similaridade entre xᵢ e xⱼ: quando as amostras são idênticas, K = 1; quando são muito diferentes (‖xᵢ − xⱼ‖ → ∞), K → 0.

O kernel RBF corresponde implicitamente a um mapeamento φ para um espaço de Hilbert de **dimensão infinita** — garantido pela expansão em série de Taylor da função exponencial — sem o custo computacional de calcular explicitamente representações infinitas. Essa propriedade confere ao kernel RBF capacidade de aproximar qualquer fronteira de decisão contínua, sendo o kernel padrão para dados tabulares clínicos.

### 1.8 O Parâmetro Gamma no Kernel RBF

O parâmetro **γ** controla a extensão da influência de cada amostra de treinamento sobre a fronteira de decisão:

- **γ grande** → gaussiana estreita → cada amostra influencia apenas vizinhos muito próximos → fronteira de decisão altamente irregular, capturando variações locais → risco de overfitting, comportamento similar ao KNN com K pequeno.

- **γ pequeno** → gaussiana larga → cada amostra influencia regiões amplas do espaço → fronteira suave e global → risco de underfitting.

O scikit-learn oferece dois modos automáticos de definição de γ:

    gamma = 'scale':  γ = 1 / (n_features × Var(X_train))
    gamma = 'auto' :  γ = 1 / n_features

O modo **'scale'** — selecionado como ótimo no experimento — normaliza γ pela variância do conjunto de treinamento, tornando-o adaptativo à dispersão dos dados padronizados. Para o dataset Cleveland (13 atributos padronizados com variância unitária), 'scale' e 'auto' produziram acurácias idênticas (82,27%), o que é esperado quando `Var(X_train) ≈ 1` após a padronização Z-score, pois nesse caso `1/(n_features × 1) ≈ 1/n_features`.

### 1.9 Necessidade de Normalização dos Atributos

O SVM baseia todas as suas decisões em **distâncias e produtos internos** no espaço de atributos. O kernel RBF, em particular, computa `‖xᵢ − xⱼ‖²` — a distância euclidiana ao quadrado entre dois pontos — de modo que atributos com magnitudes muito distintas dominam esse cálculo. Considere, no dataset Cleveland, a presença simultânea do colesterol sérico (tipicamente entre 150–350 mg/dl) e do atributo binário de angina por exercício (0 ou 1): sem normalização, o colesterol dominaria completamente a geometria da margem, tornando o atributo binário irrelevante.

A padronização Z-score (StandardScaler) aplica a transformação:

    zᵢⱼ = (xᵢⱼ − x̄ⱼ) / σⱼ

onde x̄ⱼ e σⱼ são estimados exclusivamente sobre o conjunto de treinamento. Após a transformação, cada atributo possui média zero e desvio padrão unitário, contribuindo igualmente para o cálculo das distâncias que definem a geometria da margem. Géron (2019) enfatiza que, para o SVM, a normalização não é opcional — é requisito obrigatório para o correto funcionamento do algoritmo.

Uma implicação prática é que os parâmetros de normalização devem ser calculados **apenas sobre o conjunto de treinamento** e aplicados ao conjunto de teste, evitando o **data leakage** — a contaminação das estatísticas de treino por informação do teste. Ignorar esse protocolo implica estimativas de desempenho artificialmente otimistas, incompatíveis com o desempenho real em produção.

### 1.10 Validação Cruzada Estratificada e Métricas de Avaliação

Os protocolos de avaliação do SVM neste artigo são idênticos aos utilizados para o KNN: validação cruzada estratificada k-fold (StratifiedKFold) para seleção de hiperparâmetros via GridSearchCV (5 dobras) e para estimativa final de desempenho (10 dobras). A acurácia da validação cruzada 10-fold é adotada como **métrica de referência principal**, pois fornece estimativa imparcial da capacidade de generalização do modelo ao avaliar em 10 partições independentes dos dados.

As métricas de avaliação para classificação binária — derivadas da matriz de confusão — são:

    Acurácia  = (VP + VN) / (VP + VN + FP + FN)
    Precisão  = VP / (VP + FP)
    Revocação = VP / (VP + FN)
    F1-Score  = 2 × (Precisão × Revocação) / (Precisão + Revocação)

onde VP = Verdadeiros Positivos, VN = Verdadeiros Negativos, FP = Falsos Positivos e FN = Falsos Negativos.

Em aplicações de triagem clínica, os **Falsos Negativos** (pacientes doentes classificados como saudáveis) representam o erro de maior impacto clínico, pois levam à privação de tratamento para pacientes em risco real. Por isso, a **revocação da classe Doente** (sensibilidade diagnóstica) é a métrica de maior relevância médica neste contexto.

---

## 2. Metodologia

### 2.1 Conjunto de Dados

O estudo utiliza o Cleveland Heart Disease Dataset, disponibilizado pelo UCI Machine Learning Repository sob o identificador id=45 (JANOSI et al., 1988). Esse dataset é um dos mais referenciados na literatura de diagnóstico cardíaco por aprendizado de máquina (MIENYE; SUN, 2022), coletado originalmente na Clínica Cleveland (EUA) e contendo registros de pacientes submetidos a avaliação cardíaca completa.

O dataset original contém 303 registros e 14 atributos — 13 preditores clínicos e 1 variável alvo com 5 classes (0 = sem evidência de doença; 1 a 4 = graus crescentes de comprometimento cardíaco). Após remoção de registros com valores ausentes (NaN), restaram 297 registros válidos. A Tabela 1 descreve os 13 atributos preditores utilizados.

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

O dataset original apresenta 5 níveis de diagnóstico, com ambiguidade natural entre graus intermediários clinicamente próximos. Para alinhar o problema à questão diagnóstica central — o paciente possui ou não evidência de doença cardíaca — adotou-se a binarização:

    y_binário = 0  se y_original = 0  (Saudável: sem evidência de doença)
    y_binário = 1  se y_original > 0  (Doente: qualquer grau de comprometimento)

Após binarização, a distribuição no conjunto de treinamento foi: 128 pacientes saudáveis (54%) e 109 doentes (46%), configurando um problema de classes aproximadamente balanceadas que não exige estratégias de balanceamento artificial.

### 2.3 Pipeline de Pré-processamento

O pipeline de pré-processamento segue três etapas obrigatórias:

**Etapa 1 — Remoção de valores ausentes:** registros com NaN em qualquer atributo foram descartados. Dos 303 registros originais, 6 foram removidos, resultando em 297 registros válidos.

**Etapa 2 — Padronização Z-score:** os 13 atributos foram padronizados com StandardScaler, calculando x̄ⱼ e σⱼ exclusivamente sobre X_train e aplicando a transformação tanto em X_train quanto em X_test. A separação evita data leakage — garantia essencial de que as estimativas de desempenho sejam válidas para dados novos.

**Etapa 3 — Particionamento estratificado:** os 297 registros foram divididos em 80% treinamento (237 registros) e 20% teste (60 registros) com estratificação por classe (stratify=y, random_state=42), preservando a proporção Saudável/Doente em ambas as partições.

### 2.4 Otimização de Hiperparâmetros

A busca pelo conjunto ótimo de hiperparâmetros foi realizada por busca em grade exaustiva (GridSearchCV) sobre o espaço:

    C      ∈ {0,1;  1;  10;  100}
    kernel ∈ {'linear',  'rbf',  'poly'}
    gamma  ∈ {'scale',  'auto'}

Total de combinações: 4 × 3 × 2 = 24 configurações, cada uma avaliada em 5 dobras de validação cruzada estratificada (StratifiedKFold, n_splits=5, shuffle=True, random_state=42), totalizando 120 treinos. O critério de seleção foi a maximização da acurácia média nas 5 dobras, aplicada exclusivamente sobre o conjunto de treinamento (X_train).

    (C*, kernel*, γ*) = argmax_{(C,k,γ) ∈ Grade}  (1/5) ∑_{i=1}^{5} Acc(modelo, dobra_i)

### 2.5 Protocolo de Avaliação Final

Com os hiperparâmetros ótimos definidos, o modelo final SVC(C=0,1, kernel='rbf', gamma='scale') foi treinado sobre todo X_train e avaliado em três instâncias:

1. **Conjunto de teste hold-out** (60 registros): estimativa de desempenho em dados não vistos em nenhuma etapa.
2. **Validação cruzada 10-fold** sobre os 297 registros: métrica de referência principal, obtida com StratifiedKFold(n_splits=10, shuffle=True, random_state=42) e cross_val_score.
3. **Predição sobre o conjunto completo** (297 registros): análise granular por blocos consecutivos de 50 registros.

O Algoritmo 1 sintetiza o pseudocódigo da implementação:

**Algoritmo 1 – SVM para Classificação de Doença Cardíaca**

```
Entrada : Dataset UCI Heart Disease (id=45)
          Grade de busca: C ∈ {0,1; 1; 10; 100}, kernel ∈ {linear, rbf, poly},
                          gamma ∈ {scale, auto}
Saída   : Modelo SVM otimizado; relatório de classificação completo

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
        X_scaled = scaler.transform(X)
7.  OTIMIZAR hiperparâmetros via GridSearchCV + StratifiedKFold(5):
        grid = GridSearchCV(SVC(), PARAM_GRID, cv=StratifiedKFold(5))
        grid.fit(X_train_scaled, y_train)
        C* = 0,1;  kernel* = 'rbf';  gamma* = 'scale'
8.  TREINAR modelo final:
        model = SVC(C=0,1, kernel='rbf', gamma='scale').fit(X_train_scaled, y_train)
9.  AVALIAR desempenho:
        a) y_pred_test = model.predict(X_test_scaled)
           acc_teste = accuracy_score(y_test, y_pred_test)
        b) scores_cv = cross_val_score(model, X_scaled, y,
                           cv=StratifiedKFold(10), scoring='accuracy')
        c) y_pred_all = model.predict(X_scaled)
10. GERAR confusion_matrix(y_test, y_pred_test)
    GERAR classification_report(y_test, y_pred_test)
```

---

## 3. Resultados e Discussão

### 3.1 Otimização de Hiperparâmetros

A Tabela 2 apresenta as 5 melhores combinações de hiperparâmetros identificadas pelo GridSearchCV na validação cruzada de 5 dobras:

**Tabela 2 – Top-5 combinações de hiperparâmetros na validação cruzada (5-fold)**

| Posição | C | Kernel | Gamma | Acurácia CV | Desvio |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | **0,1** | **rbf** | **scale** | **82,27%** | **±5,28%** |
| 2 | 0,1 | rbf | auto | 82,27% | ±5,28% |
| 3 | 0,1 | linear | scale | 81,00% | ±6,98% |
| 4 | 0,1 | linear | auto | 81,00% | ±6,98% |
| 5 | 1,0 | poly | scale | 81,00% | ±4,68% |

O resultado mais importante deste ranking é a convergência das duas melhores configurações para **C = 0,1 com kernel RBF**, independentemente do valor de gamma ('scale' vs. 'auto'). Como discutido na Seção 1.8, a equivalência entre os dois modos de gamma após a padronização Z-score era esperada teoricamente, e os resultados a confirmam empiricamente.

O valor ótimo C = 0,1 — o menor da grade testada — indica que o modelo se beneficia de **forte regularização** para este dataset. Essa observação é clinicamente plausível: as 13 variáveis clínicas do dataset Cleveland incluem atributos com sobreposição natural entre as distribuições das classes Saudável e Doente (por exemplo, a frequência cardíaca máxima pode ser alta tanto em jovens saudáveis quanto em cardiopatas com certos perfis). Forçar uma fronteira de decisão rígida (C alto) levaria ao overfitting nesses casos limítrofes.

O kernel RBF superou o kernel linear (82,27% vs. 81,00%), confirmando que a fronteira de decisão ótima para separar os perfis clínicos possui componentes **não-lineares** no espaço de 13 atributos padronizados. O mapeamento implícito para o espaço de dimensão infinita do kernel RBF captura interações não-lineares entre atributos clínicos — como a combinação de idade avançada, tipo de dor torácica e depressão do segmento ST — que o kernel linear não consegue discriminar.

O menor desvio padrão observado para o kernel polinomial (±4,68% vs. ±5,28% do RBF) sugere que o kernel polinomial gera fronteiras mais estáveis entre dobras, embora com acurácia média inferior. Isso pode refletir que as interações polinomiais capturam padrões menos ruidosos, porém também menos discriminativos, para este conjunto específico de dados.

### 3.2 Acurácia por Blocos de Registros

A Tabela 3 apresenta a distribuição de acurácia do modelo SVM ao longo dos 297 registros organizados em blocos consecutivos de 50:

**Tabela 3 – Acurácia do SVM (C=0,1, RBF, gamma=scale) por bloco de registros**

| Bloco | Registros | Acertos | Acurácia |
|:---:|:---:|:---:|:---:|
| 1 | 1 – 50 | 45/50 | 90,00% |
| 2 | 51 – 100 | 43/50 | 86,00% |
| 3 | 101 – 150 | 46/50 | 92,00% |
| 4 | 151 – 200 | 42/50 | 84,00% |
| 5 | 201 – 250 | 43/50 | 86,00% |
| 6 | 251 – 297 | 37/47 | 78,72% |
| **Total** | **1 – 297** | **256/297** | **86,20%** |

A variação de acurácia entre blocos — de 78,72% (bloco 6) a 92,00% (bloco 3) — é esperada em qualquer análise sequencial de dados heterogêneos. O bloco 3 (101–150), com maior acurácia, provavelmente concentra pacientes com perfis clínicos mais distantes da fronteira de decisão, tornando a classificação mais confiante. O bloco 6 (251–297), com menor acurácia (78,72%), possivelmente contém uma concentração maior de casos limítrofes — pacientes com perfis clínicos que se situam próximos ao hiperplano decisório no espaço de atributos.

É relevante notar que a distribuição de acurácia por blocos do SVM (78,72%–92,00%) é similar à do KNN com K=29 (78,72%–90,00%), com o SVM apresentando desempenho superior no bloco 3 (92,00% vs. 90,00% do KNN). Ambos os modelos apresentam o bloco 6 como o de menor acurácia, sugerindo que esses registros finais do dataset contêm casos genuinamente mais difíceis de classificar, independentemente do algoritmo empregado.

### 3.3 Métricas Consolidadas do Modelo

A Tabela 4 apresenta o resumo completo do desempenho do classificador SVM:

**Tabela 4 – Resumo de desempenho do classificador SVM (C=0,1, kernel=rbf, gamma=scale)**

| Métrica | Valor |
|---|:---:|
| Acurácia — conjunto de teste (hold-out 20%) | 86,67% |
| **Acurácia — validação cruzada 10-fold** *(métrica principal)* | **83,51% ± 7,66%** |
| Acurácia — conjunto completo (297 registros) | 86,20% |
| C (parâmetro de regularização) | 0,1 |
| Kernel | RBF |
| Gamma | scale |
| Tamanho do conjunto de treinamento | 237 registros |
| Tamanho do conjunto de teste | 60 registros |
| Total de registros avaliados | 297 registros |

A **validação cruzada 10-fold** (83,51% ± 7,66%) é a **métrica de referência para fins de TCC**, pois estima a capacidade de generalização do modelo de forma imparcial: em cada uma das 10 iterações, o modelo é avaliado em uma dobra que não participou do treinamento, e a média dessas 10 avaliações fornece estimativa robusta do desempenho em dados reais novos (GÉRON, 2019). O desvio padrão de ±7,66% reflete a variabilidade natural entre dobras para um dataset de tamanho moderado (297 registros).

A comparação com o KNN (validação cruzada de 10-fold: 82,86% ± 6,99%) revela que o **SVM apresenta acurácia média marginalmente superior** (83,51% vs. 82,86%), com desvio padrão ligeiramente maior (7,66% vs. 6,99%). A diferença de 0,65 pontos percentuais se encontra dentro de uma única margem de desvio padrão de ambos os modelos, não sendo estatisticamente significativa com o tamanho de dataset disponível. Isso é consistente com a literatura: para datasets tabulares clínicos de tamanho moderado com atributos mistos (contínuos, binários e categóricos), SVMs e KNNs frequentemente têm desempenho comparável (RUSSELL; NORVIG, 2020).

Ambos os modelos atingiram **a mesma acurácia de 86,67% no conjunto de teste hold-out**, confirmando a equivalência prática de desempenho neste cenário experimental específico.

### 3.4 Matriz de Confusão

A Tabela 5 apresenta a matriz de confusão obtida sobre os 60 registros do conjunto de teste:

**Tabela 5 – Matriz de confusão (conjunto de teste, n=60)**

| | Previsto: Saudável (0) | Previsto: Doente (1) |
|---|:---:|:---:|
| **Real: Saudável (0)** | **30** — VN | 2 — FP |
| **Real: Doente (1)** | 6 — FN | **22** — VP |

A matriz revela quatro categorias de resultado:

- **30 Verdadeiros Negativos (VN):** pacientes saudáveis corretamente identificados — o maior grupo individual de acertos. O modelo acerta 30/32 = 93,75% dos pacientes saudáveis.

- **22 Verdadeiros Positivos (VP):** pacientes doentes corretamente identificados. O modelo acerta 22/28 = 78,57% dos pacientes doentes.

- **2 Falsos Positivos (FP):** pacientes saudáveis classificados como doentes. Em contexto clínico, esse erro leva a exames adicionais desnecessários mas não representa risco direto à saúde.

- **6 Falsos Negativos (FN):** pacientes doentes classificados como saudáveis — o erro de maior impacto clínico. Com 28 pacientes doentes no conjunto de teste, os 6 FN equivalem a uma **taxa de Falsos Negativos de 21,4%**, indicando que o modelo não detecta aproximadamente 1 em cada 5 pacientes com doença cardíaca.

A relação entre Falsos Positivos (2) e Falsos Negativos (6) evidencia que o modelo é **assimetricame conservador**: prefere classificar como saudável quando há incerteza, gerando mais erros de omissão (FN) do que de comissão (FP). Para uma ferramenta de triagem clínica, a redução de Falsos Negativos é prioritária — o que pode ser endereçado ajustando o limiar de decisão ou utilizando a probabilidade de pertencimento à classe (com probability=True no SVC).

A distribuição dos 8 erros totais é **idêntica à do KNN** (VN=30, FP=2, FN=6, VP=22), confirmando a equivalência numérica dos dois modelos no conjunto de teste com random_state=42. Essa coincidência sugere que esses 8 registros representam casos genuinamente ambíguos — pacientes limítrofes que desafiam qualquer classificador binário com as 13 variáveis disponíveis.

### 3.5 Relatório de Classificação por Classe

A Tabela 6 detalha as métricas individuais por classe:

**Tabela 6 – Relatório de classificação por classe (conjunto de teste, n=60)**

| Classe | Precisão | Revocação | F1-Score | Suporte |
|---|:---:|:---:|:---:|:---:|
| Saudável (0) | 0,83 | 0,94 | 0,88 | 32 |
| Doente (1) | 0,92 | 0,79 | 0,85 | 28 |
| **Acurácia geral** | | | **0,87** | **60** |
| Média macro | 0,88 | 0,86 | 0,86 | 60 |
| Média ponderada | 0,87 | 0,87 | 0,87 | 60 |

A análise por classe permite as seguintes observações:

**Classe Saudável (0) — revocação 0,94:** o modelo identifica corretamente 30 em 32 pacientes saudáveis. A alta revocação para a classe negativa indica que o modelo é conservador em emitir diagnósticos negativos incorretos.

**Classe Doente (1) — precisão 0,92:** quando o modelo afirma que um paciente está doente, está correto em 92% dos casos — apenas 2 FP entre 24 predições positivas. Esse valor elevado de precisão é clinicamente valioso: significa que o alerta de doença gerado pelo modelo é altamente confiável.

**Revocação da classe Doente (1) = 0,79:** o modelo detecta 79% dos pacientes doentes, perdendo 21% (6 FN). Esse é o ponto de atenção clínica mais relevante: em cada 5 pacientes doentes, 1 seria liberado como saudável. Para triagem em larga escala, a combinação com exames complementares é essencial.

**F1-Score equilibrado** (0,85 e 0,88): a pequena diferença entre as classes indica que o modelo não está fortemente enviesado para nenhuma delas, o que é favorável dado o balanceamento moderado do dataset (32 saudáveis vs. 28 doentes no conjunto de teste).

### 3.6 Análise dos Erros de Classificação

Os 41 erros identificados nos 297 registros (13,80% do total; 256 acertos/297) se distribuem em dois tipos:

**Falsos Negativos — doente classificado como saudável:** ocorrem quando o ponto xᵢ de um paciente doente está localizado, no espaço padronizado de 13 dimensões, no mesmo lado do hiperplano decisório que os pacientes saudáveis. Na terminologia geométrica do SVM, esses pontos estão além da margem do lado errado — configuram violações das variáveis de folga ξᵢ > 1. Com C = 0,1, o modelo aceita essas violações com penalidade reduzida, priorizando a estabilidade global da margem.

**Falsos Positivos — saudável classificado como doente:** análogos aos FN, mas no sentido contrário. São pacientes saudáveis que, pelo conjunto de atributos clínicos observados, se situam no lado "doente" do hiperplano otimizado.

Uma diferença fundamental entre SVM e KNN na geração de erros: no KNN, erros ocorrem quando os K vizinhos mais próximos votam na classe errada — o erro é puramente local, podendo ser causado por vizinhos de treinamento atípicos. No SVM, erros ocorrem quando um ponto está no lado errado do hiperplano global — causados pela estrutura global da fronteira de decisão, que é definida apenas pelos vetores de suporte. Isso significa que a adição ou remoção de amostras não-suporte ao conjunto de treinamento não altera as predições do SVM, garantindo maior estabilidade.

---

## 4. Discussão Comparativa: SVM e KNN

A comparação entre o SVM (C=0,1, kernel RBF, gamma=scale) e o KNN (K=29) sobre o mesmo dataset revela um quadro de equivalência prática com diferenças metodológicas substanciais:

**Tabela 7 – Comparação SVM vs. KNN no Cleveland Heart Disease Dataset**

| Critério | SVM (RBF, C=0,1) | KNN (K=29) |
|---|:---:|:---:|
| Acurácia — teste hold-out | **86,67%** | **86,67%** |
| Acurácia — cross-val 10-fold | **83,51% ± 7,66%** | 82,86% ± 6,99% |
| Acurácia — conjunto completo | 86,20% | 84,85% |
| Precisão — classe Doente | **0,92** | **0,92** |
| Revocação — classe Doente | **0,79** | **0,79** |
| F1-Score — classe Doente | **0,85** | **0,85** |
| Falsos Negativos (teste) | 6 | 6 |
| Custo computacional (treino) | Alto (QP convexo) | Negligível (lazy) |
| Custo computacional (predição) | Baixo (vetores de suporte) | Alto (O(n·d) por query) |
| Interpretabilidade | Moderada (kernel linear) / Baixa (RBF) | Alta (vizinhos explicam decisão) |
| Sensibilidade à normalização | Crítica | Crítica |
| Robustez a outliers | Alta (apenas vetores de suporte) | Baixa (outliers viram vizinhos) |

Os resultados confirmam a hipótese da literatura (GÉRON, 2019; RUSSELL; NORVIG, 2020): para datasets tabulares clínicos de tamanho moderado com features contínuas padronizadas, SVMs e KNNs alcançam desempenhos comparáveis. A vantagem do SVM reside na robustez teórica garantida pela teoria VC e na eficiência de predição baseada em vetores de suporte. A vantagem do KNN reside na transparência das decisões — cada predição pode ser justificada pelos K pacientes mais similares presentes no conjunto de treinamento, argumento de interpretabilidade relevante em contexto clínico.

---

## Considerações Finais

Este artigo apresentou a fundamentação matemática completa, a implementação computacional e a análise experimental do algoritmo Support Vector Machine para classificação binária de doença cardíaca sobre o Cleveland Heart Disease Dataset.

Os principais resultados e conclusões são:

1. O SVM com C = 0,1, kernel RBF e gamma = scale, selecionado automaticamente por GridSearchCV com validação cruzada estratificada de 5 dobras, obteve **86,67% de acurácia no conjunto de teste** e **83,51% ± 7,66% na validação cruzada de 10 dobras** — a métrica de referência recomendada para o TCC por ser a estimativa mais confiável de generalização.

2. O **kernel RBF** superou os kernels linear e polinomial (82,27% vs. 81,00%), confirmando que a fronteira de decisão ótima para separação dos perfis clínicos neste dataset possui componentes não-lineares que o mapeamento implícito do kernel gaussiano para dimensão infinita consegue capturar.

3. O **valor ótimo C = 0,1** (forte regularização) indica que o dataset Cleveland se beneficia de margem ampla com tolerância a violações, evitando overfitting em uma região do espaço de atributos com sobreposição natural entre as classes. Essa é a principal diferença paramétrica do SVM em relação ao KNN: enquanto K ótimo = 29 indica vizinhança larga (equivalente a baixa variância/alto viés), C = 0,1 indica penalidade baixa por erros (equivalente a alta regularização/baixo overfitting).

4. A **padronização Z-score** é condição obrigatória para o correto funcionamento do SVM, pois o algoritmo maximiza a margem geométrica com base em distâncias e produtos internos no espaço de atributos. Sua aplicação estrita com parâmetros calculados apenas sobre o conjunto de treinamento é essencial para evitar data leakage.

5. A **comparação com o KNN** revela desempenho praticamente equivalente no dataset Cleveland: mesma acurácia no conjunto de teste (86,67%), mesma matriz de confusão (VN=30, FP=2, FN=6, VP=22) e F1-Scores idênticos (0,85 para Doente, 0,88 para Saudável). A acurácia da validação cruzada do SVM é marginalmente superior (83,51% vs. 82,86%), mas não estatisticamente significativa com 297 amostras. Essa equivalência confirma os resultados da literatura para datasets clínicos de tamanho moderado.

6. A **taxa de Falsos Negativos de 21,4%** (6 em 28 pacientes doentes) é a principal limitação clínica do modelo, compartilhada com o KNN, e reforça que ambos os algoritmos devem ser empregados como ferramentas de triagem e apoio à decisão médica, não como sistemas diagnósticos autônomos.

Como trabalho futuro, recomenda-se: (i) investigar o ajuste do limiar de decisão do SVM para reduzir a taxa de Falsos Negativos, utilizando SVC(probability=True) e curva ROC; (ii) avaliar o desempenho com kernel polinomial de grau 2 e 3 com ajuste fino de γ e r; (iii) aplicar seleção de atributos (ex.: eliminação recursiva com RFECV) para identificar o subconjunto mais discriminativo dos 13 preditores, potencialmente reduzindo ruído; e (iv) comparar SVM e KNN com algoritmos de ensemble — como Random Forest e XGBoost — em idêntico protocolo experimental, como passo natural de evolução metodológica para o TCC.

---

## Referências

BOSER, B. E.; GUYON, I. M.; VAPNIK, V. N. A training algorithm for optimal margin classifiers. In: **ANNUAL ACM WORKSHOP ON COMPUTATIONAL LEARNING THEORY**, 5., 1992, Pittsburgh. *Proceedings...* New York: ACM, 1992. p. 144–152. DOI: 10.1145/130385.130401.

CORTES, C.; VAPNIK, V. Support-vector networks. **Machine Learning**, v. 20, n. 3, p. 273–297, 1995. DOI: 10.1007/BF00994018.

GÉRON, Aurélien. **Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow: Concepts, Tools, and Techniques to Build Intelligent Systems**. 2. ed. Sebastopol, CA: O'Reilly Media, 2019.

JANOSI, A.; STEINBRUNN, W.; PFISTERER, M.; DETRANO, R. **Heart Disease Dataset**. UCI Machine Learning Repository, 1988. Disponível em: https://archive.ics.uci.edu/dataset/45/heart+disease. Acesso em: abr. 2026.

MIENYE, I. D.; SUN, Y. A Survey of Ensemble Learning: Concepts, Algorithms, Applications, and Prospects. **IEEE Access**, v. 10, p. 99129–99149, 2022. DOI: 10.1109/ACCESS.2022.3207287.

PEDREGOSA, F. et al. Scikit-learn: Machine Learning in Python. **Journal of Machine Learning Research**, v. 12, p. 2825–2830, 2011. Disponível em: https://jmlr.org/papers/v12/pedregosa11a.html. Acesso em: abr. 2026.

RUSSELL, S.; NORVIG, P. **Artificial Intelligence: A Modern Approach**. 4. ed. Hoboken, NJ: Pearson, 2020.

SCHOLKOPF, B.; SMOLA, A. J. **Learning with Kernels: Support Vector Machines, Regularization, Optimization, and Beyond**. Cambridge, MA: MIT Press, 2002.
