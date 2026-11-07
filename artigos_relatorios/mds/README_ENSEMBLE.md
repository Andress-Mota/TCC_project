# GUIA COMPLETO: ENSEMBLE LEARNING PARA DIAGNOSTICO DE DOENCA CARDIACA

## Indice
1. [Visão Geral](#visão-geral)
2. [Métodos de Ensemble Implementados](#métodos-de-ensemble-implementados)
3. [Como Executar](#como-executar)
4. [Interpretação dos Resultados](#interpretação-dos-resultados)
5. [Recomendações Clínicas](#recomendações-clínicas)
6. [Estrutura de Arquivos](#estrutura-de-arquivos)

---

## Visao Geral

Este projeto implementa **4 estratégias de ensemble learning** que combinam:
- **K-Nearest Neighbors (KNN)**: Modelo lazy learner, baseado em instâncias
- **Support Vector Machine (SVM)**: Modelo eager learner, baseado em margem máxima

### Resultados Alcançados

| Métrica | KNN/SVM Individual | Melhor Ensemble | Melhoria |
|---------|-------------------|-----------------|---------|
| **Acurácia** | 86.67% | **88.33%** | +1.66pp |
| **Falsos Negativos** | 6 | **5** | -1 caso crítico |
| **CV (10-dobras)** | 82.86-83.51% | **82.83%** | Estável |
| **AUC-ROC** | 0.9481-0.9487 | **0.9520** (Stacking) | +0.39pp |

---

## Metodos de Ensemble Implementados

### 1. **Hard Voting (Votacao Direta)**
```
Mecanismo: Cada modelo vota na classe, vencedor é maioria simples
Fórmula: ŷ = argmax_c Σ[h_i(x) = c]

Vantagens:
- Simples e interpretável
- Robusto a outliers probabilísticos

Desvantagens:
- Ignora confiança (probabilidade) das predições
```

**Resultado neste projeto**: 88.33% de acurácia

---

### 2. **Soft Voting - Simples (Média de Probabilidades)**
```
Mecanismo: Média simples de probabilidades preditas
Fórmula: P_ensemble(y=c|x) = (1/M) Σ P_i(y=c|x)

Vantagens:
- Incorpora confiança das predições
- Mantém informação de probabilidade

Desvantagens:
- Assume que probabilidades dos modelos são comparáveis
```

**Resultado neste projeto**: 88.33% de acurácia

---

### 3. **Soft Voting - Ponderado (Recomendado)**
```
Mecanismo: Média ponderada das probabilidades
Fórmula: P_ensemble(y=c|x) = Σ w_i * P_i(y=c|x) / Σ w_i

Pesos utilizados:
- KNN: 0.45 (45%)
- SVM: 0.55 (55%)

Justificativa dos pesos:
KNN CV: 82.86% ± 6.99%
SVM CV: 83.51% ± 7.66%
→ SVM tem melhor generalização, recebe peso maior

Vantagens:
- Aproveita força de cada modelo
- Balanceado: não descarta nenhum modelo
- Generalização mantida (82.83% ± 6.41% em CV)

Desvantagens:
- Requer conhecimento prévio de desempenho individual
```

**Resultado neste projeto**: 88.33% de acurácia - RECOMENDADO

---

### 4. **Stacking com Meta-learner Logistic Regression (Melhor AUC-ROC)**
```
Nível 0 (Base):
- KNN e SVM geram meta-features: [(P_KNN, P_SVM)]

Nível 1 (Meta):
- Logistic Regression treina nas meta-features
- Aprende pesos ótimos: KNN (2.1565), SVM (3.2311)

Vantagens:
- Aprende combinação não-linear
- Meta-learner pode capturar patterns complexos
- Melhor AUC-ROC (0.9520)

Desvantagens:
- Risco de overfitting do meta-learner
- Requer validação cruzada cuidadosa
- Menos interpretável que votação
```

**Resultado neste projeto**: 86.67% acurácia, MAS 0.9520 AUC-ROC (melhor!)

---

## Computador

### Prerequisitos
```bash
pip install pandas numpy scikit-learn matplotlib seaborn ucimlrepo
```

### 1. Executar Ensemble Completo
```bash
python EnsembleModels.py
```

**Saída esperada**:
- Comparação de 6 modelos (KNN, SVM, Hard Voting, Soft Voting, Soft Ponderado, Stacking)
- Validação cruzada 10-dobras
- Matrizes de confusão
- Curvas ROC
- Gráficos em `ensemble_comparison.png`

---

### 2. Gerar Resumo Visual
```bash
python gerar_resumo_ensemble.py
```

**Saída esperada**:
- Gráfico comparativo em `ensemble_summary.png`
- Tabelas de resultados
- Insights principais impressos no terminal

---

### 3. Usar o Ensemble Programaticamente

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import numpy as np

# Treinar modelos base
knn = KNeighborsClassifier(n_neighbors=29)
svm = SVC(C=0.1, kernel='rbf', gamma='scale', probability=True)

knn.fit(X_train, y_train)
svm.fit(X_train, y_train)

# Predições no novo dado
X_novo = [...]  # Array 1x13

# Opção 1: Hard Voting
y_pred_knn = knn.predict(X_novo)[0]
y_pred_svm = svm.predict(X_novo)[0]
y_pred_ensemble = int((y_pred_knn + y_pred_svm) >= 1)

# Opção 2: Soft Voting Ponderado (RECOMENDADO)
p_knn = knn.predict_proba(X_novo)[0, 1]
p_svm = svm.predict_proba(X_novo)[0, 1]
p_ensemble = 0.45 * p_knn + 0.55 * p_svm
y_pred_ensemble = int(p_ensemble >= 0.5)

print(f"Probabilidade de Doença: {p_ensemble:.2%}")
print(f"Predição: {'Doente' if y_pred_ensemble == 1 else 'Saudável'}")
```

---

## Interpretacao dos Resultados

### Matriz de Confusão - Soft Voting Ponderado

```
                  Predito
              Saudável  Doente
Verdadeiro:
Saudável        30        2      └─ 2 falsos positivos
Doente           5       23      └─ 5 falsos negativos
```

**Métricas Derivadas**:
- **Sensibilidade (Recall para Doente)**: 23/28 = 82% → 82% dos doentes foram identificados
- **Especificidade (Recall para Saudável)**: 30/32 = 94% → 94% dos saudáveis foram identificados
- **Precisão (Doente)**: 23/25 = 92% → 92% dos que predizemos doentes estavam corretos
- **Precisão (Saudável)**: 30/35 = 86% → 86% dos que predizemos saudáveis estavam corretos

### Interpretação Clínica

❌ **Falso Negativo (5 casos)**: Paciente doente classificado como saudável
   - CRÍTICO: Paciente não recebe tratamento necessário
   - Prioridade: Minimizar ao máximo
   - Ensemble reduziu de 6 para 5

✓ **Falso Positivo (2 casos)**: Paciente saudável classificado como doente
   - MENOS CRÍTICO: Paciente passa por testes adicionais
   - Custo: Investigação desnecessária
   - Número muito baixo: Excelente especificidade

**Conclusão**: O ensemble mantém alta especificidade (94%) enquanto reduz falsos negativos — perfil ideal para triagem clínica.

---

## Recomendacoes Clinicas

### ✓ Quando Usar Cada Modelo

| Cenário | Modelo Recomendado | Razão |
|---------|-------------------|-------|
| **Triagem de Rotina** | Soft Voting Ponderado | Melhor acurácia (88.33%), generaliza bem (82.83% CV) |
| **Maximizar Detecção** | KNN ou SVM Individual | Recall para doentes: 82% |
| **Máxima Confiança** | Stacking | Melhor AUC-ROC (0.9520) |
| **Sistema Rápido** | SVM Sozinho | Menor custo computacional na predição |
| **Interpretabilidade** | Hard Voting | Simples entender: "votação por maioria" |

### Fluxo de Paciente Proposto

```
1. [Coleta de Dados Clínicos]
   └─ 13 atributos: age, sex, cp, trestbps, chol, fbs, restecg, 
      thalach, exang, oldpeak, slope, ca, thal

2. [Ensemble Soft Voting Ponderado]
   ├─ KNN prediz P_KNN
   ├─ SVM prediz P_SVM
   └─ P_ensemble = 0.45 * P_KNN + 0.55 * P_SVM

3. [Decisão Clínica]
   ├─ P_ensemble ≥ 0.5: "RISCO DE DOENÇA"
   │  └─ Encaminhar para cardiologista
   │  └─ Realizar exames confirmatórios
   │
   └─ P_ensemble < 0.5: "BAIXO RISCO"
      └─ Acompanhamento de rotina
      └─ Reteste em 12-24 meses
```

### Limiares Ajustáveis

Se quiser **priorizar sensibilidade** (minimizar falsos negativos):
```python
# Reduzir limiar de 0.5 para 0.4
limiar = 0.4
y_pred = int(p_ensemble >= limiar)
# Resultado: Detecta mais doentes, mas mais falsos positivos
```

Se quiser **priorizar especificidade** (minimizar falsos positivos):
```python
# Aumentar limiar de 0.5 para 0.6
limiar = 0.6
y_pred = int(p_ensemble >= limiar)
# Resultado: Menos falsos positivos, mas alguns doentes não são detectados
```

---

## 📁 Estrutura de Arquivos

```
TCC project/
├── KNearestNeighbors.py              [Modelos individuais]
├── SupportVectorMachine.py
├── EnsembleModels.py                 [Implementação do ensemble ⭐]
├── gerar_resumo_ensemble.py          [Gráficos de resumo]
│
├── Artigo_KNN_Doenca_Cardiaca.md     [Documentação]
├── Artigo_SVM_Doenca_Cardiaca.md
├── Artigo_Ensemble_Doenca_Cardiaca.md [NOVO: Teórico e resultados]
├── README_ENSEMBLE.md                [ESTE ARQUIVO]
│
├── ensemble_comparison.png           [Gráficos gerados]
├── ensemble_summary.png
├── knn_output.txt                    [Logs anteriores]
├── output_full.txt
│
└── dados/
    └── [Dataset UCI Heart Disease]
```

---

## Detalhes Tecnicos

### Hardware Utilizado
- CPU: Intel Core i7/i5
- RAM: 8GB+
- Tempo de execução (~): EnsembleModels.py = ~2-3 min (CV inclusa)

### Dependências Críticas
- `scikit-learn ≥ 1.0`: Modelos ML, CV, métricas
- `pandas ≥ 1.0`: Manipulação de dados
- `numpy`: Operações numéricas
- `matplotlib`, `seaborn`: Visualizações
- `ucimlrepo`: Download automático dataset UCI

### Reprodutibilidade
Todos os scripts incluem `random_state=42` para garantir resultados determinísticos. Para replicar:
```bash
python EnsembleModels.py  # Mesmos resultados sempre
```

---

## Proximos Passos Propostos

1. **Expandir Ensemble**:
   - Adicionar Random Forest + Gradient Boosting
   - Testar XGBoost como meta-learner no stacking
   - Explorar ensemble com 5+ algoritmos

2. **Otimização de Hiperparâmetros**:
   - GridSearch conjunto nos 6 hiperparâmetros do ensemble
   - Bayesian Optimization para achar pesos ótimos

3. **Validação Externa**:
   - Testar em outro dataset de doença cardíaca (ex: Framingham)
   - Validação clínica prospectiva com pacientes reais

4. **Análise de Importância**:
   - Explorar qual feature é mais relevante via SHAP values
   - Feature importance por modelo

5. **Implementação em Produção**:
   - Flask/Django API para predições online
   - Mobile app para triagem em campo
   - Dashboard para monitoramento de performance

---

## 📞 Suporte e Perguntas

**Como interpretar probabilidades?**
- P_ensemble = 0.75 → 75% de risco de doença → Recomendar investigação

**Por que SVM tem peso maior (55% vs 45%)?**
- CV do SVM foi 83.51%, KNN foi 82.86% → SVM generaliza melhor

**Posso usar outros algoritmos (Random Forest, XGBoost)?**
- SIM! Substitua a sintaxe dentro de `EnsembleModels.py`
- Trade-off: Mais algoritmos = mais acurácia, mas menos interpretabilidade

**Dataset é suficientemente grande?**
- 297 pacientes é modesto. Resultados melhoram muito com 1000+

---

## 📐 Fórmulas Matemáticas de Referência

### Hard Voting
$$\hat{y} = \text{argmax}_{c} \sum_{i=1}^{M} \mathbb{1}[h_i(x) = c]$$

### Soft Voting Ponderado
$$P_{\text{ensemble}}(y=c|x) = \frac{\sum_{i=1}^{M} w_i \cdot P_i(y=c|x)}{\sum_{i=1}^{M} w_i}$$

onde $w_1 = 0.45$ (KNN), $w_2 = 0.55$ (SVM)

### Stacking
$$Z = [P_1(y|X), P_2(y|X)]$$
$$\hat{y} = g(Z)$$

onde $g$ é Logistic Regression.

### AUC-ROC
$$\text{ROC}(t) = \left(\frac{\text{FP}}{FP+TN}, \frac{\text{TP}}{TP+FN}\right)$$
$$\text{AUC} = \int_0^1 \text{ROC}(t) \, dt$$

---

## 🎓 Citações Relevantes

1. **Kuncheva, L. I.** (2014). *Combining Pattern Classifiers: Methods and Algorithms*. John Wiley & Sons.
   - Teoria fundamental de ensemble learning

2. **Zhou, Z.-H.** (2012). *Ensemble Methods: Foundations and Algorithms*. CRC Press.
   - Diversidade e redundância em ensembles

3. **Polikar, R.** (2006). "Ensemble based systems in decision making". *IEEE Circuits and Systems Magazine*, 6(3), 21–45.
   - Aplicações clínicas de ensembles

4. **Cortes, C.; Vapnik, V.** (1995). "Support-vector networks". *Machine Learning*, 20(3), 273–297.
   - Algoritmo SVM original

---

## Versao e Historico

- **v1.0 (2026-04-20)**: Versão inicial
  - 4 métodos de ensemble
  - Validação cruzada 10-dobras
  - Documentação completa
  - Gráficos comparativos

---

**Última atualização**: 20 de Abril de 2026
**Autor**: André Felipe
**Instituição**: Faculdade de Tecnologia de Guaratinguetá
