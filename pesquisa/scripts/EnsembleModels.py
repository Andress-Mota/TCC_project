"""
ENSEMBLE LEARNING PARA DIAGNÓSTICO DE DOENÇA CARDÍACA
Combinação de K-Nearest Neighbors e Support Vector Machine

Fundamentação teórica:
- Ensemble methods combinam múltiplos modelos para melhorar generalização (Kuncheva, 2014)
- Modelos com baixa correlação de erros produzem melhores ensembles (Polikar, 2006)
- KNN (lazy learner, local) + SVM (eager learner, global) possuem vieses diferentes
- Votação majoritária (Hard Voting) é robusta quando modelos concordam
- Votação suave (Soft Voting) aproveita probabilidades para decisão mais refined
- Stacking com meta-learner pode aprender pesos ótimos dos classificadores base

Estratégias implementadas:
1. Hard Voting: Cada modelo vota, classe vencedora decide
2. Soft Voting: Média das probabilidades preditas
3. Stacking: Logistic Regression treina nos outputs dos classificadores base
"""

import pandas as pd
import numpy as np
from ucimlrepo import fetch_ucirepo
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score, cross_val_predict
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score, roc_curve
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================================================================
#  CONFIGURAÇÕES
# ==============================================================================
MODO_BINARIO    = True      # 0 = Saudável, 1 = Doente
TEST_SIZE       = 0.2
RANDOM_STATE    = 42
VISUALIZAR      = True      # Gerar gráficos de ROC e comparações

# ==============================================================================
#  1. CARREGAMENTO E PREPARAÇÃO DOS DADOS
# =========================0=====================================================
print("\n" + "="*80)
print("ENSEMBLE: K-NEAREST NEIGHBORS + SUPPORT VECTOR MACHINE")
print("="*80)
print("\n[1] CARREGAMENTO E PREPARACAO DOS DADOS")
print("-" * 50)

print("   -> Baixando dataset UCI Heart Disease (id=45)...")
heart_disease = fetch_ucirepo(id=45)
print("   -> Dataset baixado com sucesso!")

X_raw = heart_disease.data['features']
y_raw = heart_disease.data['targets'].values.ravel()

print(f"   -> Dimensões originais: {X_raw.shape[0]} registros x {X_raw.shape[1]} features")
print(f"   -> Features disponíveis: {list(X_raw.columns)}")

# Selecionar colunas relevantes
colunas = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
           'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
X_raw = X_raw[colunas]
print(f"   -> Selecionadas {len(colunas)} features clínicas relevantes")

# Limpeza de dados
print("\n   -> Iniciando limpeza de dados...")
mask_valido = X_raw.notna().all(axis=1) & pd.notna(y_raw)
X = X_raw[mask_valido].reset_index(drop=True)
y_orig = pd.Series(y_raw[mask_valido]).reset_index(drop=True)

removidos = len(X_raw) - len(X)
print(f"   -> Registros após limpeza: {len(X)} (removidos {removidos} com valores faltantes)")

# Distribuição original das classes
distribuicao_orig = pd.Series(y_orig).value_counts().sort_index()
print(f"   -> Distribuição original das classes: {distribuicao_orig.to_dict()}")

# Binarização
if MODO_BINARIO:
    y = (y_orig > 0).astype(int)
    desc_classes = {0: "Saudável", 1: "Doente"}
    print("   -> Convertendo para classificação BINÁRIA (0 = Saudável, 1 = Doente)")
else:
    y = y_orig.copy()
    desc_classes = {0: "Sem doença", 1: "Risco baixo", 2: "Risco médio",
                    3: "Risco médio-alto", 4: "Risco elevado"}
    print("   -> Mantendo classificação MULTICLASSE (0-4)")

distribuicao_final = pd.Series(y).value_counts().sort_index()
print(f"   -> Distribuição final das classes: {distribuicao_final.to_dict()}")

# Normalização
print("\n   -> Aplicando normalização Z-score (StandardScaler)...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("   -> Normalização concluída!")

# Particionamento
print(f"\n   -> Particionando dados: {TEST_SIZE*100:.0f}% para teste, {100-TEST_SIZE*100:.0f}% para treino")
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)

print(f"   -> Conjunto de treino: {len(X_train)} registros")
print(f"   -> Conjunto de teste: {len(X_test)} registros")

# Verificar estratificação
train_dist = pd.Series(y_train).value_counts().sort_index()
test_dist = pd.Series(y_test).value_counts().sort_index()
print(f"   -> Distribuição treino: {train_dist.to_dict()}")
print(f"   -> Distribuição teste: {test_dist.to_dict()}")

print("\n   ✓ FASE 1 CONCLUÍDA: Dados preparados com sucesso!")

# ==============================================================================
#  2. TREINAMENTO DOS MODELOS BASE
# ==============================================================================
print("\n[2] Treinando modelos base...")
print("   -> Esta fase treina os classificadores individuais (KNN e SVM)")
print("   -> Cada modelo será treinado no conjunto de treino e avaliado no conjunto de teste")

# KNN otimizado (K=29 conforme artigo)
print("\n  * KNearestNeighbors (K=29)...")
print("    -> Configurando KNN com 29 vizinhos (parâmetro otimizado)")
knn = KNeighborsClassifier(n_neighbors=29)
print("    -> Treinando modelo KNN...")
knn.fit(X_train, y_train)
print("    -> Treinamento KNN concluído!")

print("    -> Fazendo predições no conjunto de teste...")
y_pred_knn = knn.predict(X_test)
y_proba_knn = knn.predict_proba(X_test)[:, 1]  # Probabilidade da classe 1
acc_knn = accuracy_score(y_test, y_pred_knn)
print(f"    -> Acurácia KNN no conjunto de teste: {acc_knn:.4f}")
print(f"    -> Predições KNN: {np.bincount(y_pred_knn)} (Saudável/Doente)")

# SVM otimizado (C=0.1, kernel=RBF, gamma=scale conforme artigo)
print("\n  * Support Vector Machine (C=0.1, RBF, gamma=scale)...")
print("    -> Configurando SVM com C=0.1, kernel RBF e gamma=scale (parâmetros otimizados)")
svm = SVC(C=0.1, kernel='rbf', gamma='scale', probability=True, random_state=RANDOM_STATE)
print("    -> Treinando modelo SVM...")
svm.fit(X_train, y_train)
print("    -> Treinamento SVM concluído!")

print("    -> Fazendo predições no conjunto de teste...")
y_pred_svm = svm.predict(X_test)
y_proba_svm = svm.predict_proba(X_test)[:, 1]  # Probabilidade da classe 1
acc_svm = accuracy_score(y_test, y_pred_svm)
print(f"    -> Acurácia SVM no conjunto de teste: {acc_svm:.4f}")
print(f"    -> Predições SVM: {np.bincount(y_pred_svm)} (Saudável/Doente)")

print("\n   ✓ FASE 2 CONCLUÍDA: Modelos base treinados com sucesso!")

# ==============================================================================
#  3. ENSEMBLE - HARD VOTING
# ==============================================================================
print("\n[3] Ensemble - Hard Voting (votação por maioria)...")
print("   -> Método de ensemble mais simples: cada modelo 'vota' na classe")
print("   -> A classe com mais votos vence (maioria simples)")
print("   -> Se empate, a classe positiva (doente) é escolhida")

# Votação: cada modelo vota na sua classe predita.
# Com 2 modelos, maioria (>= 2) equivale a unanimidade; empate (soma=1) desempata
# pela probabilidade média — favorece a classe com maior confiança conjunta.
print("    -> Calculando votos dos modelos base...")
votos = y_pred_knn + y_pred_svm
y_proba_media_hard = (y_proba_knn + y_proba_svm) / 2
y_pred_ensemble_hard = np.where(
    votos == 2, 1,
    np.where(votos == 0, 0,
             (y_proba_media_hard >= 0.5).astype(int))  # desempate por probabilidade
)

acc_ensemble_hard = accuracy_score(y_test, y_pred_ensemble_hard)
print(f"    -> Acurácia Ensemble Hard Voting: {acc_ensemble_hard:.4f}")
print(f"    -> Predições Hard Voting: {np.bincount(y_pred_ensemble_hard)} (Saudável/Doente)")

# Análise de concordância
concordancia = np.mean(y_pred_knn == y_pred_svm)
print(f"    -> Taxa de concordância KNN-SVM: {concordancia:.4f}")
print("    -> Concordância alta (>0.8) indica que os modelos concordam na maioria das predições")

print("\n   ✓ FASE 3 CONCLUÍDA: Hard Voting implementado!")

# ==============================================================================
#  4. ENSEMBLE - SOFT VOTING
# ==============================================================================
print("\n[4] Ensemble - Soft Voting (média ponderada de probabilidades)...")
print("   -> Método mais sofisticado: usa probabilidades em vez de votos duros")
print("   -> Calcula média das probabilidades de cada modelo")
print("   -> Threshold de 0.5 decide a classe final")

# Soft voting: média simples das probabilidades
print("    -> Calculando média simples das probabilidades...")
y_proba_ensemble_soft = (y_proba_knn + y_proba_svm) / 2
y_pred_ensemble_soft = (y_proba_ensemble_soft >= 0.5).astype(int)

acc_ensemble_soft = accuracy_score(y_test, y_pred_ensemble_soft)
print(f"    -> Acurácia Ensemble Soft Voting: {acc_ensemble_soft:.4f}")
print(f"    -> Predições Soft Voting: {np.bincount(y_pred_ensemble_soft)} (Saudável/Doente)")

# Pesos derivados das acurácias de validação cruzada no conjunto de treino,
# normalizados para somar 1 — modelos que generalizam melhor recebem mais peso.
cv_weight = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
acc_cv_knn = cross_val_score(KNeighborsClassifier(n_neighbors=29), X_train, y_train, cv=cv_weight).mean()
acc_cv_svm = cross_val_score(SVC(C=0.1, kernel='rbf', gamma='scale', probability=True), X_train, y_train, cv=cv_weight).mean()
w_knn = acc_cv_knn / (acc_cv_knn + acc_cv_svm)
w_svm = acc_cv_svm / (acc_cv_knn + acc_cv_svm)
print(f"    -> Pesos derivados da CV: KNN={w_knn:.4f}, SVM={w_svm:.4f}")

y_proba_ensemble_weighted = w_knn * y_proba_knn + w_svm * y_proba_svm
y_pred_ensemble_weighted = (y_proba_ensemble_weighted >= 0.5).astype(int)

acc_ensemble_weighted = accuracy_score(y_test, y_pred_ensemble_weighted)
print(f"    -> Acurácia Ensemble Soft Voting Ponderado: {acc_ensemble_weighted:.4f}")
print(f"    -> Predições Soft Voting Ponderado: {np.bincount(y_pred_ensemble_weighted)} (Saudável/Doente)")
print("    -> Pesos calculados automaticamente pela performance de CV no treino")

print("\n   ✓ FASE 4 CONCLUÍDA: Soft Voting implementado!")

# ==============================================================================
#  5. ENSEMBLE - STACKING
# ==============================================================================
print("\n[5] Ensemble - Stacking com Logistic Regression...")
print("   -> Método mais avançado: usa um meta-modelo para aprender a combinar predições")
print("   -> Logistic Regression aprende a ponderar as saídas dos modelos base")
print("   -> Meta-features: probabilidades dos modelos KNN e SVM")

# Gerar meta-features via cross_val_predict para evitar vazamento de dados.
# Se usarmos predict() direto sobre X_train (já visto pelos modelos base), o
# meta-learner treina em predições "fáceis" — aprende a confiar em modelos
# que nunca erram no treino, causando overfitting.
# cross_val_predict gera predições out-of-fold: cada ponto é predito por um
# modelo que NÃO o viu no treino, simulando dados novos para o meta-learner.
print("    -> Gerando meta-features out-of-fold (cross_val_predict, 5 folds)...")
cv_meta = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

knn_meta = KNeighborsClassifier(n_neighbors=29)
svm_meta = SVC(C=0.1, kernel='rbf', gamma='scale', probability=True, random_state=RANDOM_STATE)

proba_knn_oof = cross_val_predict(knn_meta, X_train, y_train, cv=cv_meta, method='predict_proba')[:, 1]
proba_svm_oof = cross_val_predict(svm_meta, X_train, y_train, cv=cv_meta, method='predict_proba')[:, 1]

X_meta_train_proba = np.hstack([proba_knn_oof.reshape(-1, 1), proba_svm_oof.reshape(-1, 1)])
print(f"    -> Meta-features out-of-fold criadas: {X_meta_train_proba.shape[0]} amostras, {X_meta_train_proba.shape[1]} features")

# Treinar meta-learner (Logistic Regression) nas meta-features out-of-fold
print("    -> Treinando meta-learner (Logistic Regression)...")
meta_model = LogisticRegression(random_state=RANDOM_STATE, max_iter=200)
meta_model.fit(X_meta_train_proba, y_train)
print("    -> Meta-learner treinado!")

# Predições no conjunto de teste usando meta-features
print("    -> Gerando predições finais com stacking...")
X_meta_test_proba = np.hstack([y_proba_knn.reshape(-1, 1), y_proba_svm.reshape(-1, 1)])
y_pred_ensemble_stacking = meta_model.predict(X_meta_test_proba)

acc_ensemble_stacking = accuracy_score(y_test, y_pred_ensemble_stacking)
print(f"    -> Acurácia Ensemble Stacking: {acc_ensemble_stacking:.4f}")
print(f"    -> Predições Stacking: {np.bincount(y_pred_ensemble_stacking)} (Saudável/Doente)")

# Coeficientes do meta-learner mostram pesos aprendidos
print(f"    -> Coeficientes do meta-learner: KNN={meta_model.coef_[0][0]:.4f}, SVM={meta_model.coef_[0][1]:.4f}")
print("    -> Coeficientes mostram como o meta-learner pondera cada modelo base")

print("\n   ✓ FASE 5 CONCLUÍDA: Stacking implementado!")

# ==============================================================================
#  6. VALIDAÇÃO CRUZADA
# ==============================================================================
print("\n[6] Validação Cruzada Estratificada (10-dobras)...")
print("   -> Técnica fundamental para avaliar generalização do modelo")
print("   -> Divide dados em 10 partes mantendo proporção das classes")
print("   -> Cada fold é usado como teste uma vez, outros 9 como treino")
print("   -> Resultado: média ± desvio padrão das 10 execuções")

cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=RANDOM_STATE)
print("    -> Configurada validação cruzada estratificada com 10 dobras")

# Para ensemble, precisamos recalcular a cada fold
def avaliar_ensemble_cv(X, y, cv, tipo='soft'):
    """Avalia ensemble em CV estratificada"""
    scores = []

    for fold_idx, (train_idx, val_idx) in enumerate(cv.split(X, y)):
        X_train_fold, X_val_fold = X[train_idx], X[val_idx]
        y_train_fold, y_val_fold = y[train_idx], y[val_idx]

        # Treinar modelos na fold
        knn_fold = KNeighborsClassifier(n_neighbors=29)
        knn_fold.fit(X_train_fold, y_train_fold)

        svm_fold = SVC(C=0.1, kernel='rbf', gamma='scale', probability=True)
        svm_fold.fit(X_train_fold, y_train_fold)

        # Obter predições na validação
        if tipo == 'hard':
            y_pred_knn_fold = knn_fold.predict(X_val_fold)
            y_pred_svm_fold = svm_fold.predict(X_val_fold)
            votos_fold = y_pred_knn_fold + y_pred_svm_fold
            proba_media_fold = (knn_fold.predict_proba(X_val_fold)[:, 1] +
                                svm_fold.predict_proba(X_val_fold)[:, 1]) / 2
            y_pred_fold = np.where(
                votos_fold == 2, 1,
                np.where(votos_fold == 0, 0,
                         (proba_media_fold >= 0.5).astype(int))
            )

        elif tipo == 'soft_simple':
            y_proba_knn_fold = knn_fold.predict_proba(X_val_fold)[:, 1]
            y_proba_svm_fold = svm_fold.predict_proba(X_val_fold)[:, 1]
            y_proba_fold = (y_proba_knn_fold + y_proba_svm_fold) / 2
            y_pred_fold = (y_proba_fold >= 0.5).astype(int)

        elif tipo == 'soft_weighted':
            y_proba_knn_fold = knn_fold.predict_proba(X_val_fold)[:, 1]
            y_proba_svm_fold = svm_fold.predict_proba(X_val_fold)[:, 1]
            y_proba_fold = 0.45 * y_proba_knn_fold + 0.55 * y_proba_svm_fold
            y_pred_fold = (y_proba_fold >= 0.5).astype(int)

        elif tipo == 'stacking':
            y_proba_knn_fold = knn_fold.predict_proba(X_val_fold)[:, 1]
            y_proba_svm_fold = svm_fold.predict_proba(X_val_fold)[:, 1]
            X_meta_val = np.hstack([y_proba_knn_fold.reshape(-1, 1), y_proba_svm_fold.reshape(-1, 1)])

            meta_fold = LogisticRegression(random_state=RANDOM_STATE, max_iter=200)
            X_meta_train_fold = np.hstack([
                knn_fold.predict_proba(X_train_fold)[:, 1].reshape(-1, 1),
                svm_fold.predict_proba(X_train_fold)[:, 1].reshape(-1, 1)
            ])
            meta_fold.fit(X_meta_train_fold, y_train_fold)

            y_pred_fold = meta_fold.predict(X_meta_val)

        # Calcular acurácia
        score = accuracy_score(y_val_fold, y_pred_fold)
        scores.append(score)

    return np.array(scores)

print("    -> Executando validação cruzada para todos os métodos...")
# Avaliar todos os métodos em CV
cv_scores_knn = cross_val_score(KNeighborsClassifier(n_neighbors=29), X_scaled, y, cv=cv, scoring='accuracy')
cv_scores_svm = cross_val_score(SVC(C=0.1, kernel='rbf', gamma='scale', probability=True), X_scaled, y, cv=cv, scoring='accuracy')
cv_scores_hard = avaliar_ensemble_cv(X_scaled, y, cv, tipo='hard')
cv_scores_soft_simple = avaliar_ensemble_cv(X_scaled, y, cv, tipo='soft_simple')
cv_scores_soft_weighted = avaliar_ensemble_cv(X_scaled, y, cv, tipo='soft_weighted')
cv_scores_stacking = avaliar_ensemble_cv(X_scaled, y, cv, tipo='stacking')

print("\n    RESULTADOS DA VALIDAÇÃO CRUZADA (10-dobras):")
print(f"    KNN              : {cv_scores_knn.mean():.4f} ± {cv_scores_knn.std():.4f}")
print(f"    SVM              : {cv_scores_svm.mean():.4f} ± {cv_scores_svm.std():.4f}")
print(f"    Hard Voting      : {cv_scores_hard.mean():.4f} ± {cv_scores_hard.std():.4f}")
print(f"    Soft Voting      : {cv_scores_soft_simple.mean():.4f} ± {cv_scores_soft_simple.std():.4f}")
print(f"    Soft Weighted    : {cv_scores_soft_weighted.mean():.4f} ± {cv_scores_soft_weighted.std():.4f}")
print(f"    Stacking         : {cv_scores_stacking.mean():.4f} ± {cv_scores_stacking.std():.4f}")
print("    -> Valores mais altos e desvios menores indicam melhor performance")

print("\n   ✓ FASE 6 CONCLUÍDA: Validação cruzada realizada!")

# ==============================================================================
#  7. MÉTRICAS DETALHADAS
# ==============================================================================
print("\n[7] Matriz de Confusão - Conjunto de Teste")
print("   -> Mostra detalhadamente os tipos de erro do modelo")
print("   -> Verdadeiro Positivo (VP): Doentes corretamente identificados")
print("   -> Falso Positivo (FP): Saudáveis incorretamente classificados como doentes")
print("   -> Verdadeiro Negativo (VN): Saudáveis corretamente identificados")
print("   -> Falso Negativo (FN): Doentes incorretamente classificados como saudáveis")

print("\n  K-NEAREST NEIGHBORS:")
cm_knn = confusion_matrix(y_test, y_pred_knn)
print(cm_knn)
tn_knn, fp_knn, fn_knn, tp_knn = cm_knn.ravel()
print(f"    VP: {tp_knn}, FP: {fp_knn}, VN: {tn_knn}, FN: {fn_knn}")

print("\n  SUPPORT VECTOR MACHINE:")
cm_svm = confusion_matrix(y_test, y_pred_svm)
print(cm_svm)
tn_svm, fp_svm, fn_svm, tp_svm = cm_svm.ravel()
print(f"    VP: {tp_svm}, FP: {fp_svm}, VN: {tn_svm}, FN: {fn_svm}")

print("\n  ENSEMBLE SOFT VOTING PONDERADO:")
cm_ensemble = confusion_matrix(y_test, y_pred_ensemble_weighted)
print(cm_ensemble)
tn_ens, fp_ens, fn_ens, tp_ens = cm_ensemble.ravel()
print(f"    VP: {tp_ens}, FP: {fp_ens}, VN: {tn_ens}, FN: {fn_ens}")

print("\n[8] Relatório de Classificação - Ensemble Soft Voting Ponderado")
print("   -> Precision: Das predições positivas, quantas são corretas")
print("   -> Recall: Dos casos positivos reais, quantos foram detectados")
print("   -> F1-Score: Média harmônica entre precision e recall")
print("   -> Support: Número de casos reais em cada classe")
print(classification_report(y_test, y_pred_ensemble_weighted, target_names=["Saudável", "Doente"]))

print("\n   ✓ FASES 7-8 CONCLUÍDAS: Métricas detalhadas calculadas!")

# ==============================================================================
#  9. AUC-ROC
# ==============================================================================
print("\n[9] AUC-ROC Score (curve under ROC)")
print("   -> Área sob a curva ROC: mede capacidade de discriminação do modelo")
print("   -> Valores próximos de 1.0 indicam excelente discriminação")
print("   -> Valor 0.5 representa performance aleatória")
print("   -> Importante para comparar modelos em problemas de classificação binária")

auc_knn = roc_auc_score(y_test, y_proba_knn)
auc_svm = roc_auc_score(y_test, y_proba_svm)
auc_soft = roc_auc_score(y_test, y_proba_ensemble_soft)
auc_weighted = roc_auc_score(y_test, y_proba_ensemble_weighted)
auc_stacking = roc_auc_score(y_test, meta_model.predict_proba(X_meta_test_proba)[:, 1])

print(f"  KNN              : {auc_knn:.4f}")
print(f"  SVM              : {auc_svm:.4f}")
print(f"  Soft Voting      : {auc_soft:.4f}")
print(f"  Soft Weighted    : {auc_weighted:.4f}")
print(f"  Stacking         : {auc_stacking:.4f}")

print("\n   ✓ FASE 9 CONCLUÍDA: AUC-ROC calculado!")

# ==============================================================================
#  10. COMPARAÇÃO RESUMIDA
# ==============================================================================
print("\n" + "="*80)
print("RESUMO COMPARATIVO - ACURÁCIA NO CONJUNTO DE TESTE")
print("="*80)

resultados = {
    "KNN (K=29)": acc_knn,
    "SVM (C=0.1, RBF)": acc_svm,
    "Hard Voting": acc_ensemble_hard,
    "Soft Voting": acc_ensemble_soft,
    "Soft Voting Ponderado": acc_ensemble_weighted,
    "Stacking": acc_ensemble_stacking,
}

for modelo, acc in sorted(resultados.items(), key=lambda x: x[1], reverse=True):
    print(f"  {modelo:.<40} {acc:.4f}")

# ==============================================================================
#  11. VISUALIZAÇÕES
# ==============================================================================
if VISUALIZAR:
    print("\n[10] Gerando visualizações...")
    print("   -> Criando gráficos comparativos para análise visual")
    print("   -> Inclui: Curvas ROC, barras de acurácia, boxplots CV, matrizes de confusão")    
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle('Ensemble Learning: Comparação de Métodos', fontsize=16, fontweight='bold')
    
    # CurvasROC
    ax = axes[0, 0]
    fpr_knn, tpr_knn, _ = roc_curve(y_test, y_proba_knn)
    fpr_svm, tpr_svm, _ = roc_curve(y_test, y_proba_svm)
    fpr_weighted, tpr_weighted, _ = roc_curve(y_test, y_proba_ensemble_weighted)
    fpr_stacking, tpr_stacking, _ = roc_curve(y_test, meta_model.predict_proba(X_meta_test_proba)[:, 1])
    
    ax.plot(fpr_knn, tpr_knn, label=f'KNN (AUC={auc_knn:.3f})', linewidth=2)
    ax.plot(fpr_svm, tpr_svm, label=f'SVM (AUC={auc_svm:.3f})', linewidth=2)
    ax.plot(fpr_weighted, tpr_weighted, label=f'Soft Weighted (AUC={auc_weighted:.3f})', linewidth=2)
    ax.plot(fpr_stacking, tpr_stacking, label=f'Stacking (AUC={auc_stacking:.3f})', linewidth=2)
    ax.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Aleatório')
    ax.set_xlabel('Taxa Falso Positivo')
    ax.set_ylabel('Taxa Verdadeiro Positivo')
    ax.set_title('Curva ROC')
    ax.legend(loc='lower right', fontsize=9)
    ax.grid(True, alpha=0.3)
    
    # Acurácia Comparativa
    ax = axes[0, 1]
    modelos = list(resultados.keys())
    acuras = list(resultados.values())
    cores = ['#FF6B6B' if m.startswith(('KNN', 'SVM')) else '#4ECDC4' for m in modelos]
    bars = ax.barh(modelos, acuras, color=cores)
    ax.set_xlabel('Acurácia')
    ax.set_title('Acurácia no Conjunto de Teste')
    ax.set_xlim([0.8, 0.95])
    for i, (bar, acc) in enumerate(zip(bars, acuras)):
        ax.text(acc + 0.001, i, f'{acc:.4f}', va='center', fontsize=9)
    ax.grid(True, alpha=0.3, axis='x')
    
    # Validação Cruzada
    ax = axes[0, 2]
    cv_data = {
        'KNN': cv_scores_knn,
        'SVM': cv_scores_svm,
        'Hard': cv_scores_hard,
        'Soft': cv_scores_soft_simple,
        'Weighted': cv_scores_soft_weighted,
        'Stacking': cv_scores_stacking,
    }
    box_data = [cv_data[k] for k in cv_data.keys()]
    bp = ax.boxplot(box_data, labels=cv_data.keys(), patch_artist=True)
    for patch in bp['boxes']:
        patch.set_facecolor('#95E1D3')
    ax.set_ylabel('Acurácia')
    ax.set_title('Validação Cruzada (10-dobras)')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Matriz de Confusão - KNN
    ax = axes[1, 0]
    cm_knn = confusion_matrix(y_test, y_pred_knn)
    sns.heatmap(cm_knn, annot=True, fmt='d', cmap='Blues', ax=ax, cbar=False)
    ax.set_title('KNN - Matriz de Confusão')
    ax.set_ylabel('Verdadeiro')
    ax.set_xlabel('Predito')
    
    # Matriz de Confusão - SVM
    ax = axes[1, 1]
    cm_svm = confusion_matrix(y_test, y_pred_svm)
    sns.heatmap(cm_svm, annot=True, fmt='d', cmap='Oranges', ax=ax, cbar=False)
    ax.set_title('SVM - Matriz de Confusão')
    ax.set_ylabel('Verdadeiro')
    ax.set_xlabel('Predito')
    
    # Matriz de Confusão - Ensemble
    ax = axes[1, 2]
    cm_ensemble = confusion_matrix(y_test, y_pred_ensemble_weighted)
    sns.heatmap(cm_ensemble, annot=True, fmt='d', cmap='Greens', ax=ax, cbar=False)
    ax.set_title('Soft Voting Ponderado - Matriz de Confusão')
    ax.set_ylabel('Verdadeiro')
    ax.set_xlabel('Predito')
    
    plt.tight_layout()
    plt.savefig('ensemble_comparison.png', dpi=300, bbox_inches='tight')
    print("    -> Gráfico salvo como 'ensemble_comparison.png'")
    print("    -> Arquivo pronto para uso em relatórios e apresentações")
    plt.show()

    print("\n   ✓ FASE 10 CONCLUÍDA: Visualizações geradas!")
else:
    print("\n[10] Visualizações desabilitadas (VISUALIZAR=False)")
    print("   -> Para gerar gráficos, altere VISUALIZAR=True no início do script")

print("\n" + "="*80)
print("ANÁLISE CONCLUÍDA")
print("="*80 + "\n")
