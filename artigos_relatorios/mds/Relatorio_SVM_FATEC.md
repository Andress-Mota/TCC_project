# RELATÓRIO TÉCNICO — SUPPORT VECTOR MACHINE APLICADO AO DIAGNÓSTICO DE DOENÇA CARDÍACA

**Autor:** André Felipe  
**Instituição:** Faculdade de Tecnologia de Guaratinguetá — FATEC  
**Dataset:** Cleveland Heart Disease Dataset — UCI Machine Learning Repository (id=45)  
**Algoritmo:** Support Vector Machine (SVM) com otimização automática de hiperparâmetros  
**Data de execução:** Abril de 2026

---

## 1. Objetivo

Este relatório documenta a aplicação do algoritmo Support Vector Machine (SVM) para classificação binária de doença cardíaca, registrando o conjunto de dados utilizado, o pipeline de pré-processamento, a otimização de hiperparâmetros, as métricas de desempenho e recomendações metodológicas para o Trabalho de Conclusão de Curso (TCC).

---

## 2. Base de Dados

| Item | Valor |
|---|---|
| Fonte | UCI Machine Learning Repository (id=45) |
| Nome | Cleveland Heart Disease Dataset |
| Registros originais | 303 |
| Registros removidos (valores ausentes) | 6 |
| **Registros válidos utilizados** | **297** |
| Atributos preditores | 13 (clínicos) |
| Variável alvo — original | 5 classes (0–4) |
| Variável alvo — binarizada | 0 = Saudável / 1 = Doente |

**Atributos clínicos utilizados:** age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal.

---

## 3. Pipeline de Pré-processamento

### 3.1 Binarização da Variável Alvo

```
y = 0  →  y_original = 0  (sem evidência de doença cardíaca)
y = 1  →  y_original > 0  (qualquer grau de comprometimento cardíaco)
```

### 3.2 Divisão Treino/Teste

| Conjunto | Registros | Distribuição de Classes |
|---|:---:|---|
| Treinamento | 237 (80%) | Saudável: 128 (54%) / Doente: 109 (46%) |
| Teste | 60 (20%) | Saudável: 32 / Doente: 28 |

Método: `train_test_split` com `stratify=y` e `random_state=42` — garante proporção de classes preservada e reprodutibilidade.

### 3.3 Normalização

Método: `StandardScaler` (padronização Z-score)

```
z = (x − μ_treino) / σ_treino
```

- Os parâmetros μ e σ foram calculados **exclusivamente** sobre o conjunto de treinamento.
- A mesma transformação foi aplicada ao conjunto de teste e ao conjunto completo.
- **Justificativa:** O SVM maximiza a margem geométrica com base em distâncias e produtos internos. Atributos em escalas distintas distorcem essas distâncias, enviesando o hiperplano decisório. A normalização é obrigatória.

---

## 4. Otimização de Hiperparâmetros

### 4.1 Grade de Busca

| Hiperparâmetro | Valores Testados |
|---|---|
| C | 0,1 / 1 / 10 / 100 |
| kernel | linear / rbf / poly |
| gamma | scale / auto |

**Total de combinações:** 4 × 3 × 2 = **24 configurações**  
**Método:** GridSearchCV com StratifiedKFold (5 dobras)  
**Total de modelos treinados:** 24 × 5 = **120 treinos**

### 4.2 Top-5 Resultados da Busca

| # | C | Kernel | Gamma | Acurácia CV (5-fold) | Desvio |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | **0,1** | **rbf** | **scale** | **82,27%** | **±5,28%** |
| 2 | 0,1 | rbf | auto | 82,27% | ±5,28% |
| 3 | 0,1 | linear | scale | 81,00% | ±6,98% |
| 4 | 0,1 | linear | auto | 81,00% | ±6,98% |
| 5 | 1,0 | poly | scale | 81,00% | ±4,68% |

### 4.3 Hiperparâmetros Ótimos Selecionados

| Parâmetro | Valor Ótimo | Significado |
|---|:---:|---|
| C | **0,1** | Forte regularização — margem larga com tolerância a violações |
| kernel | **rbf** | Fronteira não-linear no espaço de dimensão infinita |
| gamma | **scale** | γ = 1 / (n_features × Var(X_train)) — adaptativo à dispersão dos dados |

---

## 5. Resultados de Desempenho

### 5.1 Métricas Globais

| Métrica | Valor | Observação |
|---|:---:|---|
| Acurácia — conjunto de teste (60 registros) | 86,67% | Dados nunca vistos pelo modelo |
| **Acurácia — cross-val 10-fold** | **83,51% ± 7,66%** | **Métrica principal — mais confiável** |
| Acurácia — conjunto completo (297 registros) | 86,20% | Estimativa ligeiramente otimista |
| Avaliação qualitativa | BOM | Classifica bem a maioria dos casos |

> **A acurácia de validação cruzada 10-fold é a métrica recomendada para reportar no TCC.** Ela avalia o modelo em dados não utilizados no treinamento em 10 partições independentes, fornecendo estimativa robusta e imparcial da capacidade de generalização.

### 5.2 Acurácia por Blocos de Registros

| Bloco | Registros | Acertos | Acurácia |
|:---:|:---:|:---:|:---:|
| 1 | 1 – 50 | 45/50 | 90,00% |
| 2 | 51 – 100 | 43/50 | 86,00% |
| 3 | 101 – 150 | 46/50 | **92,00%** |
| 4 | 151 – 200 | 42/50 | 84,00% |
| 5 | 201 – 250 | 43/50 | 86,00% |
| 6 | 251 – 297 | 37/47 | **78,72%** |
| **Total** | **1 – 297** | **256/297** | **86,20%** |

A variação entre blocos (78,72%–92,00%) reflete diferenças na composição local das amostras. O bloco 6 concentra os casos mais ambíguos do dataset — pacientes com perfis clínicos próximos à fronteira de decisão.

### 5.3 Matriz de Confusão (conjunto de teste, n = 60)

```
              Previsto: Saudável   Previsto: Doente
Real: Saudável      30  (VN)            2  (FP)
Real: Doente         6  (FN)           22  (VP)
```

| Tipo de Resultado | Quantidade | Interpretação Clínica |
|---|:---:|---|
| Verdadeiros Negativos (VN) | **30** | Saudáveis corretamente identificados |
| Falsos Positivos (FP) | 2 | Saudáveis erroneamente alertados (exames desnecessários) |
| **Falsos Negativos (FN)** | **6** | **Doentes não detectados — risco clínico crítico** |
| Verdadeiros Positivos (VP) | **22** | Doentes corretamente identificados |

**Taxa de Falsos Negativos:** 6/28 = **21,4%** → 1 em cada 5 pacientes doentes não é detectado.

### 5.4 Relatório de Classificação por Classe

| Classe | Precisão | Revocação | F1-Score | Suporte |
|---|:---:|:---:|:---:|:---:|
| Saudável (0) | 0,83 | **0,94** | 0,88 | 32 |
| Doente (1) | **0,92** | 0,79 | 0,85 | 28 |
| **Acurácia geral** | | | **0,87** | **60** |
| Média macro | 0,88 | 0,86 | 0,86 | 60 |
| Média ponderada | 0,87 | 0,87 | 0,87 | 60 |

**Leitura clínica das métricas:**
- **Precisão Doente = 0,92:** quando o modelo emite alerta de doença, está certo em 92% das vezes.
- **Revocação Doente = 0,79:** o modelo detecta 79% dos pacientes doentes (perde 21%).
- **Revocação Saudável = 0,94:** o modelo libera como saudável apenas pacientes genuinamente sem doença em 94% dos casos.

---

## 6. Análise dos Erros

### 6.1 Registros com Erro de Classificação (amostra representativa)

**Falsos Negativos — pacientes doentes classificados como saudáveis:**

| Registro | Idade | Sexo | FC Máx | Previsto | Real |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 17 | 48 | Masculino | 168 | Saudável | Doente |
| 34 | 59 | Masculino | 161 | Saudável | Doente |
| 45 | 61 | Feminino | 169 | Saudável | Doente |
| 81 | 45 | Masculino | 148 | Saudável | Doente |
| 144 | 58 | Masculino | 154 | Saudável | Doente |
| 170 | 53 | Masculino | 111 | Saudável | Doente |

**Padrão observado:** frequência cardíaca máxima em faixa intermediária (111–169 bpm), idades entre 45 e 61 anos — perfis clinicamente ambíguos que não afastam com clareza a presença de doença.

**Falsos Positivos — pacientes saudáveis classificados como doentes:**

| Registro | Idade | Sexo | FC Máx | Previsto | Real |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 33 | 64 | Masculino | 158 | Doente | Saudável |
| 53 | 44 | Masculino | 153 | Doente | Saudável |

### 6.2 Explicação Geométrica dos Erros

No SVM com kernel RBF, erros de classificação correspondem a pontos localizados no lado errado do hiperplano decisório ótimo — denominados violações de margem (ξᵢ > 0). Com C = 0,1 (forte regularização), o modelo aceita essas violações com penalidade reduzida para preservar a integridade global da margem máxima. Isso é necessário porque o espaço dos 13 atributos clínicos do dataset Cleveland apresenta sobreposição natural entre as distribuições das classes Saudável e Doente.

---

## 7. Comparação com KNN

| Métrica | SVM (RBF, C=0,1) | KNN (K=29) | Diferença |
|---|:---:|:---:|:---:|
| Acurácia — teste | **86,67%** | 86,67% | 0,00 pp |
| Cross-val 10-fold | **83,51% ± 7,66%** | 82,86% ± 6,99% | +0,65 pp |
| Acurácia — todos os dados | **86,20%** | 84,85% | +1,35 pp |
| Falsos Negativos | 6 | 6 | 0 |
| Falsos Positivos | 2 | 2 | 0 |
| F1-Score Doente | 0,85 | 0,85 | 0,00 |

**Conclusão da comparação:** os dois modelos apresentam desempenho estatisticamente equivalente neste dataset. A diferença de 0,65 pp na validação cruzada está dentro de uma margem de desvio padrão de ambos os modelos e não é significativa com 297 amostras.

**Diferenças qualitativas importantes:**

| Aspecto | SVM (kernel RBF) | KNN (K=29) |
|---|---|---|
| Tipo de fronteira | Global (hiperplano no espaço RBF) | Local (votação de vizinhos) |
| Robustez a outliers | Alta (apenas vetores de suporte definem fronteira) | Baixa (outliers viram vizinhos) |
| Interpretabilidade | Baixa com kernel RBF | Alta (explica por pacientes similares) |
| Custo de predição | Baixo (apenas vetores de suporte) | Alto (O(n×d) por query) |
| Treinamento | Alto (problema de otimização QP) | Negligível (lazy learning) |

---

## 8. Recomendações para o TCC

### 8.1 Hiperparâmetros e Justificativas

1. **Use sempre GridSearchCV para selecionar C, kernel e gamma.** Esse procedimento garante que os valores escolhidos sejam justificados por dados de validação cruzada, não por tentativa e erro. O resultado encontrado (C=0,1, RBF, gamma=scale) pode ser reportado com rigor científico.

2. **Justifique o kernel RBF escolhido:** a superioridade sobre o kernel linear (82,27% vs. 81,00%) evidencia que a fronteira de decisão ótima possui componentes não-lineares no espaço de 13 atributos clínicos. O truque do kernel mapeia implicitamente os dados para um espaço de dimensão infinita onde a separabilidade linear é alcançada.

3. **Justifique C=0,1 (forte regularização):** o valor mais baixo da grade sendo o ótimo indica que o dataset se beneficia de margem ampla, compatível com a sobreposição clínica natural entre pacientes limítrofes. Forçar C alto geraria overfitting nessa região ambígua.

### 8.2 Normalização

4. **A padronização Z-score é obrigatória para o SVM** — não é etapa opcional. O SVM maximiza a margem geométrica usando distâncias euclidianas; features não normalizadas distorcem essas distâncias e produzem fronteiras erradas.

5. **Calcule os parâmetros de normalização apenas sobre X_train** e aplique-os ao X_test. Isso evita data leakage e garante que a estimativa de desempenho seja válida para dados novos.

### 8.3 Métricas a Reportar

6. **Métrica principal para o TCC: validação cruzada 10-fold → 83,51% ± 7,66%.** Sempre reporte média ± desvio-padrão. Essa é a estimativa mais honesta da capacidade de generalização.

7. **Reporte também a matriz de confusão** e destaque os Falsos Negativos: em contexto clínico, deixar de detectar doentes é mais crítico do que alarmar saudáveis.

8. **Para comparação com KNN no TCC:** os dois modelos são equivalentes neste dataset. Discuta as diferenças qualitativas — tipo de fronteira, interpretabilidade, robustez a outliers e custo computacional — como critérios de escolha em cenários reais, além da acurácia numérica.

### 8.4 Variáveis Mais Relevantes (literatura)

Segundo a literatura sobre o dataset Cleveland (JANOSI et al., 1988), as variáveis com maior poder discriminativo são:
- **cp** (tipo de dor torácica): principal preditor de doença cardíaca
- **thal** (teste de estresse com tálio): forte indicador diagnóstico
- **ca** (vasos coloridos por fluoroscopia): marcador direto de obstrução
- **oldpeak** (depressão do segmento ST): indicador de isquemia
- **exang** (angina por exercício): sintoma clínico direto

Para o SVM com kernel linear, os coeficientes do vetor de pesos w indicam a importância relativa de cada feature. Para o kernel RBF (caso deste experimento), a interpretabilidade direta não está disponível — pode-se usar SHAP values como alternativa.

---

## 9. Resumo Executivo

```
==============================================================================
RESUMO DO EXPERIMENTO — SVM APLICADO AO DIAGNÓSTICO CARDÍACO
==============================================================================

Dataset          : UCI Heart Disease (Cleveland, id=45)
Registros        : 297 válidos (303 originais − 6 com valores ausentes)
Divisão          : 237 treino (80%) / 60 teste (20%), estratificada

Hiperparâmetros  : C=0.1, kernel=rbf, gamma=scale (via GridSearchCV 5-fold)
Normalização     : StandardScaler (Z-score), ajustado apenas em X_train

DESEMPENHO:
  Acurácia — teste hold-out    : 86.67%  (52/60 acertos)
  Acurácia — cross-val 10-fold : 83.51% ± 7.66%   ← MÉTRICA PRINCIPAL
  Acurácia — todos os dados    : 86.20%  (256/297 acertos)

MATRIZ DE CONFUSÃO (teste):
  VN=30  FP=2   (Saudáveis: 32 reais, 32 preditos corretos)
  FN=6   VP=22  (Doentes  : 28 reais, 6 não detectados)

POR CLASSE (conjunto de teste):
  Saudável: Precisão=0.83  Recall=0.94  F1=0.88
  Doente  : Precisão=0.92  Recall=0.79  F1=0.85
  Acurácia global: 0.87

COMPARAÇÃO COM KNN (K=29):
  Acurácia teste  →  empate (86.67% vs 86.67%)
  Cross-val 10f   →  SVM superior por 0.65 pp (não significativo)
  Matriz confusão →  idêntica (VN=30, FP=2, FN=6, VP=22)

AVALIAÇÃO GERAL: BOM — classifica bem a maioria dos casos.
                 Usar como apoio ao diagnóstico, não substituto.
==============================================================================
```

---

## 10. Referências

BOSER, B. E.; GUYON, I. M.; VAPNIK, V. N. A training algorithm for optimal margin classifiers. **Proceedings of the 5th Annual ACM Workshop on COLT**, 1992. DOI: 10.1145/130385.130401.

CORTES, C.; VAPNIK, V. Support-vector networks. **Machine Learning**, v. 20, n. 3, p. 273–297, 1995. DOI: 10.1007/BF00994018.

GÉRON, Aurélien. **Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow**. 2. ed. O'Reilly Media, 2019.

JANOSI, A. et al. **Heart Disease Dataset**. UCI Machine Learning Repository, 1988. Disponível em: https://archive.ics.uci.edu/dataset/45/heart+disease.

MIENYE, I. D.; SUN, Y. A Survey of Ensemble Learning. **IEEE Access**, v. 10, p. 99129–99149, 2022.

PEDREGOSA, F. et al. Scikit-learn: Machine Learning in Python. **JMLR**, v. 12, p. 2825–2830, 2011.

RUSSELL, S.; NORVIG, P. **Artificial Intelligence: A Modern Approach**. 4. ed. Pearson, 2020.

SCHOLKOPF, B.; SMOLA, A. J. **Learning with Kernels**. MIT Press, 2002.
