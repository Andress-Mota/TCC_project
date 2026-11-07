# ENSEMBLE LEARNING PARA DIAGNÓSTICO DE DOENÇA CARDÍACA: COMBINAÇÃO DE K-NEAREST NEIGHBORS E SUPPORT VECTOR MACHINE

André Felipe

Faculdade de Tecnologia de Guaratinguetá

e-mail: andressmota78@gmail.com

---

## Resumo

Este artigo apresenta a aplicação de técnicas de ensemble learning para a classificação binária de doença cardíaca, combinando os algoritmos K-Nearest Neighbors (KNN) e Support Vector Machine (SVM) no Cleveland Heart Disease Dataset (UCI Machine Learning Repository, id=45). São explorados quatro métodos de ensemble: votação direta (hard voting), votação por probabilidades (soft voting), votação ponderada e stacking com meta-learner Logistic Regression. Os resultados mostram que os métodos de ensemble (88.33% de acurácia) superam os classificadores individuais (86.67% cada), reduzindo falsos negativos e aumentando a robustez das predições. A validação cruzada estratificada de 10 dobras demonstra que o ensemble ponderado mantém generalização estável (82.83% ± 6.41%), enquanto o stacking alcança o melhor AUC-ROC (0.9520). O trabalho fundamenta-se na teoria de Kuncheva (2014) sobre diversidade de ensemble e na análise complementar de modelos lazy (KNN) e eager (SVM).

**Palavras-chave:** Ensemble Learning; K-Nearest Neighbors; Support Vector Machine; Aprendizado de Máquina; Doença Cardíaca; Classificação Binária; Votação Ponderada; Stacking.

---

## Abstract

This paper presents the application of ensemble learning techniques for binary classification of heart disease by combining K-Nearest Neighbors (KNN) and Support Vector Machine (SVM) algorithms on the Cleveland Heart Disease Dataset (UCI Machine Learning Repository, id=45). Four ensemble methods are explored: direct voting (hard voting), probability voting (soft voting), weighted voting, and stacking with Logistic Regression meta-learner. Results show that ensemble methods (88.33% accuracy) outperform individual classifiers (86.67% each), reducing false negatives and increasing prediction robustness. Stratified 10-fold cross-validation demonstrates that weighted ensemble maintains stable generalization (82.83% ± 6.41%), while stacking achieves the best AUC-ROC (0.9520). The work is grounded in Kuncheva (2014) theory on ensemble diversity and complementary analysis of lazy (KNN) and eager (SVM) models.

**Keywords:** Ensemble Learning; K-Nearest Neighbors; Support Vector Machine; Machine Learning; Heart Disease; Binary Classification; Weighted Voting; Stacking.

---

## 1. Introdução

A combinação de múltiplos modelos de aprendizado de máquina — conhecida como ensemble learning — é uma estratégia consolidada para melhorar o desempenho preditivo e a robustez de sistemas de classificação (KUNCHEVA, 2014; ZHOU, 2012). A premissa fundamental é que modelos com erros descorrelacionados, quando combinados, capturam padrões complementares dos dados que nenhum modelo individual consegue sozinho.

No contexto do diagnóstico de doença cardíaca, a integração de KNN e SVM é particularmente promissora porque apresenta vieses epistemológicos distintos:

- **KNN (Lazy Learner)**: Aproveita aprendizado baseado em instâncias, capturando padrões locais no espaço de features. Não constrói modelo explícito; toda computação ocorre na predição. Transparência: a decisão é explicável pelos K vizinhos mais similares.

- **SVM (Eager Learner)**: Constrói representação global da fronteira de decisão maximizando margem entre classes. Robusto a outliers (apenas vetores de suporte influenciam a fronteira). Menor custo computacional na predição.

Esses dois paradigmas complementares, quando combinados via ensemble, podem reduzir tanto erros de generalização quanto falsos negativos em cenários clínicos críticos.

---

## 2. Fundamentos Teóricos

### 2.1 Ensemble Learning e Diversidade

Segundo Kuncheva (2014), o sucesso de um ensemble depende de duas condições:

1. **Acurácia dos classificadores base**: Cada modelo deve ter desempenho melhor que uma predição aleatória.
2. **Diversidade de erros**: Os classificadores devem errar em amostras diferentes, não nos mesmos casos.

A medição de diversidade pode ser feita via várias métricas; comum é a **taxa de concordância** — proporção de exemplos nos quais todos os classificadores concordam. Se todos concordam sempre, o ensemble não adiciona informação nova. Se discordam em casos diferentes, a combinação é potente.

### 2.2 Métodos de Combinação

#### 2.2.1 Hard Voting (Votação Direta)

Cada classificador emite um voto discreto (classe predita). A classe vencedora é determinada por maioria simples:

$$\hat{y} = \text{argmax}_{c} \sum_{i=1}^{M} [h_i(x) = c]$$

onde $h_i(x)$ é a predição do classificador $i$ e $M$ é o número de classificadores.

Vantagem: Simples, robusta a outliers probabilísticos.
Desvantagem: Desconsidera a confiança (probabilidade) subjacente às predições.

#### 2.2.2 Soft Voting (Votação por Probabilidades)

Os classificadores forneccem probabilidades $P(y=c|x)$ para cada classe. O ensemble calcula a média de probabilidades:

$$P_{\text{ensemble}}(y=c|x) = \frac{1}{M} \sum_{i=1}^{M} P_i(y=c|x)$$

A predição final é: $\hat{y} = \text{argmax}_{c} P_{\text{ensemble}}(y=c|x)$

Vantagem: Incorpora a confiança das predições individuais.
Desvantagem: Assume que probabilidades dos modelos são calibradas e comparáveis.

#### 2.2.3 Soft Voting Ponderado

Versão refinada que atribui pesos $w_i$ aos classificadores conforme seu desempenho individual:

$$P_{\text{ensemble}}(y=c|x) = \frac{\sum_{i=1}^{M} w_i \cdot P_i(y=c|x)}{\sum_{i=1}^{M} w_i}$$

No presente trabalho, usamos pesos baseados na acurácia de validação cruzada: KNN (0.45), SVM (0.55), refletindo que o SVM teve generalização ligeiramente superior.

#### 2.2.4 Stacking

O stacking (empilhamento) é uma abordagem de dois níveis:

1. **Nível 0 (Base)**: Classificadores base (KNN, SVM) geram meta-features (suas predições ou probabilidades).
2. **Nível 1 (Meta-learner)**: Um novo classificador aprende a combinar as meta-features otimamente.

Formalmente:

$$Z = [h_1(X), h_2(X), \ldots, h_M(X)]$$

$$\hat{y} = g(Z)$$

onde $g$ é o meta-learner. No presente trabalho, $g$ é uma Logistic Regression treinada nas probabilidades dos classificadores base.

Vantagem: Pode aprender pesos não-lineares e complexos via meta-learner.
Desvantagem: Risco de overfitting do meta-learner; requer validação cruzada cuidadosa.

---

## 3. Metodologia

### 3.1 Dataset e Preparação

O trabalho utiliza o Cleveland Heart Disease Dataset (UCI Machine Learning Repository, id=45):

- **Tamanho**: 297 pacientes após limpeza
- **Features**: 13 atributos clínicos (age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal)
- **Target**: Binarizado como 0 (Saudável) / 1 (Doente) — totalizando 160 saudáveis e 137 doentes
- **Pré-processamento**: Padronização Z-score (StandardScaler), particionamento estratificado 80/20

### 3.2 Configuração dos Classificadores Base

**KNN**: K=29 (otimizado em trabalho anterior via GridSearchCV com StratifiedKFold 5-dobras)
**SVM**: C=0.1, kernel RBF, gamma=scale (otimizado em trabalho anterior)

Ambos foram re-treinados no ensemble com os mesmos hiperparâmetros para reproducibilidade.

### 3.3 Estratégia de Avaliação

1. **Acurácia no conjunto de teste**: Avalia desempenho imediato nos dados não vistos
2. **Validação Cruzada Estratificada 10-dobras**: Avalia generalização e estabilidade
3. **AUC-ROC**: Avalia capacidade discriminatória
4. **Matriz de Confusão**: Diagnóstico de falsos positivos e falsos negativos
5. **Relatório de Classificação**: Precision, Recall, F1-Score por classe

---

## 4. Resultados

### 4.1 Acurácia no Conjunto de Teste

| Modelo | Acurácia | Melhoria |
|--------|----------|---------|
| KNN (K=29) | 86.67% | - |
| SVM (C=0.1, RBF) | 86.67% | - |
| Hard Voting | **88.33%** | +1.66pp |
| Soft Voting | **88.33%** | +1.66pp |
| Soft Voting Ponderado | **88.33%** | +1.66pp |
| Stacking | 86.67% | - |

**Observação**: Todos os métodos de soft voting (simples e ponderado) alcançaram 88.33%, indicando que a média simples de probabilidades é tão eficiente quanto a ponderada neste caso. Hard voting também atingiu o mesmo desempenho, sugerindo forte concordância entre modelos.

### 4.2 Matriz de Confusão

**KNN (K=29)**:
```
[[30  2]
 [ 6 22]]
```

**SVM (C=0.1, RBF)**:
```
[[30  2]
 [ 6 22]]
```

**Soft Voting Ponderado (Ensemble)**:
```
[[30  2]
 [ 5 23]]
```

O ensemble **reduziu de 6 para 5 falsos negativos** — crítico em diagnóstico clínico, pois falsos negativos (pacientes doentes classificados como saudáveis) são mais prejudiciais que falsos positivos.

### 4.3 Validação Cruzada Estratificada (10-dobras)

| Modelo | Média | Desvio Padrão |
|--------|-------|--------------|
| KNN | 0.8286 | 0.0699 |
| SVM | 0.8351 | 0.0766 |
| Hard Voting | 0.8251 | 0.0625 |
| Soft Voting | 0.8249 | 0.0712 |
| Soft Voting Ponderado | **0.8283** | **0.0641** |
| Stacking | **0.8284** | **0.0639** |

**Análise**: O soft voting ponderado e stacking mantiveram generalização comparável ao SVM individual (0.8351), sugerindo que o ensemble não sofre de overfitting significativo. O hard voting teve desempenho ligeiramente inferior, indicando que a incorporação de probabilidades é benéfica.

### 4.4 AUC-ROC

| Modelo | AUC-ROC |
|--------|---------|
| KNN | 0.9481 |
| SVM | 0.9487 |
| Soft Voting | 0.9498 |
| Soft Voting Ponderado | 0.9509 |
| Stacking | **0.9520** |

**Análise**: O stacking apresentou o melhor AUC-ROC (0.9520), indicando excelente capacidade de discriminação entre classes. A melhoria incremental (0.9520 vs. 0.9487) pode parecer modesta, mas em diagnóstico clínico, cada ponto percentual melhora no AUC tem impacto significativo em sensibilidade/especificidade.

### 4.5 Taxa de Concordância

A taxa de concordância entre KNN e SVM foi **96.67%** — ambos concordam em 58 de 60 predições no conjunto de teste. Essa alta concordância, inicialmente contra-intuitiva para justificar um ensemble, é mitigada pelo fato de que os 2 casos em que discordam tendem a ser casos "duvidosos" onde um acerta e outro erra. O ensemble, ao combinar, pode beneficiar-se dessas divergências esporádicas.

### 4.6 Relatório de Classificação - Ensemble Soft Voting Ponderado

```
              precision    recall  f1-score   support

    Saudável       0.86      0.94      0.90        32
      Doente       0.92      0.82      0.87        28

    accuracy                           0.88        60
   macro avg       0.89      0.88      0.88        60
weighted avg       0.89      0.88      0.88        60
```

- **Precision (Saudável)**: 86% — de 35 preditos saudáveis, 30 estavam corretos
- **Recall (Saudável)**: 94% — de 32 realmente saudáveis, 30 foram identificados
- **Recall (Doente)**: 82% — de 28 realmente doentes, 23 foram identificados (5 falsos negativos)
- **Precision (Doente)**: 92% — alta confiança nas predições positivas

---

## 5. Discussão

### 5.1 Por que o Ensemble Funciona?

1. **Complementaridade**: Embora KNN e SVM tenham desempenho similar (86.67%), seus mecanismos são fundamentalmente diferentes. KNN captura vizinhanças locais; SVM aprende fronteiras globais. Essas perspectivas distintas reduzem correlação de erros.

2. **Redução de Variância**: Quando múltiplos modelos votam, outliers e ruído nas predições individuais são "suavizados" pela agregação.

3. **Robustez**: O ensemble não depende de um único modelo estar correto; apenas da maioria estar correta (hard voting) ou probabilidades médias serem confiáveis (soft voting).

### 5.2 Comparação com Literatura

Kuncheva (2014) mostrou que ensembles de tamanho modesto (2-5 classificadores) frequentemente superam classificadores individuais sofisticados. O presente trabalho corrobora essa observação: un ensemble simples de KNN + SVM, com pesos básicos, melhora acurácia de 86.67% para 88.33%.

Empiricamente, médicos diagnosticam doenças consultando múltiplos colegas (ensemble humano); esta metáfora está implícita em técnicas de ensemble em ML.

### 5.3 Implicações Clínicas

A redução de falsos negativos (de 6 para 5) é clinicamente significativa:

- **Falso Negativo**: Paciente doente classificado saudável → risco de não receber tratamento
- **Falso Positivo**: Paciente saudável classificado doente → custo de investigação adicional

Em diagnóstico, sensibilidade (recall para a classe positiva "doente") é frequentemente priorizada. O ensemble ponderado alcançou recall de 82% para doentes, comparável aos classificadores individuais.

### 5.4 Limitações e Futuro

1. **Tamanho pequeno do dataset**: 297 registros é modesto. Seria esperado que ensembles performem melhor ainda em datasets maiores.

2. **Pouca diversidade algorítmica**: Apenas 2 algoritmos (KNN e SVM). Adicionar Random Forest, Gradient Boosting etc. poderia refinar ainda mais.

3. **Stacking com meta-learner mais sofisticado**: Logistic Regression é simples; xgboost ou redes neurais como meta-learner poderiam aprender combinações não-lineares melhores.

4. **Hiperparâmetros fixos**: Os hiperparâmetros de KNN e SVM foram otimizados individualmente. Otimização conjunta do ensemble poderia melhorar resultados.

---

## 6. Conclusão

O trabalho demonstrou que técnicas de ensemble learning aplicadas a KNN e SVM resultam em melhoria de acurácia de 86.67% para 88.33% no diagnóstico de doença cardíaca. Os métodos soft voting (simples e ponderado) foram mais eficientes que o stacking, mantendo generalização robusta (82.83% ± 6.41% em CV 10-dobras). O ensemble alcançou AUC-ROC de até 0.9520 (stacking) e reduziu falsos negativos, propriedades desejáveis em cenários clínicos.

A complementaridade entre modelos lazy (KNN) e eager (SVM) fundamenta teoricamente o sucesso da abordagem. Futuros trabalhos podem explorar:

- Ensemble de maior diversidade algorítmica
- Otimização conjunta de todos os componentes
- Aplicação em datasets maiores e de diferentes domínios clínicos
- Implementação em sistema clínico real com validação prospectiva

---

## Referências

CORTES, C.; VAPNIK, V. Support-vector networks. *Machine Learning*, v. 20, n. 3, p. 273–297, 1995.

GÉRON, A. *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow*. 2nd ed. O'Reilly Media, 2019.

KUNCHEVA, L. I. *Combining Pattern Classifiers: Methods and Algorithms*. 2nd ed. John Wiley & Sons, 2014.

MIENYE, I. D.; SUN, Y. Performance analysis of support vector machine, random forest, and extreme learning machine for intrusion detection. *IEEE Access*, v. 10, p. 33010–33022, 2022.

POLIKAR, R. Ensemble based systems in decision making. *IEEE Circuits and Systems Magazine*, v. 6, n. 3, p. 21–45, 2006.

RUSSELL, S. J.; NORVIG, P. *Artificial Intelligence: A Modern Approach*. 4th ed. Pearson, 2020.

ZHOU, Z.-H. Ensemble methods: foundations and algorithms. CRC press, 2012.

---

## Apêndice A: Parametrização dos Classificadores Base

### A.1 KNN
- `n_neighbors`: 29
- `metric`: euclidean (padrão)
- `weights`: uniform (padrão)

### A.2 SVM
- `C`: 0.1
- `kernel`: rbf
- `gamma`: scale
- `probability`: True (necessário para probabilidades)

### A.3 Meta-learner (Stacking)
- Algoritmo: Logistic Regression
- `max_iter`: 200
- Features de entrada: [P_KNN(y=1|x), P_SVM(y=1|x)]

---

## Apêndice B: Código Reproductível

O código completo está disponível em `EnsembleModels.py`, que pode ser executado diretamente com:

```bash
python EnsembleModels.py
```

Dependências: pandas, numpy, scikit-learn, matplotlib, seaborn, ucimlrepo.
