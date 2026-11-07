import pandas as pd
import numpy as np
from ucimlrepo import fetch_ucirepo
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold, cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# ==============================================================================
#  CONFIGURACOES
# ==============================================================================
TEST_SIZE      = 0.2
RANDOM_STATE   = 42

N_EST_RANGE    = [50, 100, 200, 300, 500]
DEPTH_RANGE    = [None, 5, 10, 15, 20]

# ==============================================================================
#  DADOS
# ==============================================================================
heart_disease = fetch_ucirepo(id=45)
X_raw = heart_disease.data['features']
y_raw = heart_disease.data['targets'].values.ravel()

colunas = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
           'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
X_raw = X_raw[colunas]

mask = X_raw.notna().all(axis=1) & pd.notna(y_raw)
X    = X_raw[mask].reset_index(drop=True)
y    = (pd.Series(y_raw[mask]) > 0).astype(int).reset_index(drop=True)

print(f"Registros validos: {len(X)}  |  Doentes: {y.sum()}  |  Saudaveis: {(y==0).sum()}")

# ==============================================================================
#  DIVISAO (sem normalizacao — RF nao e baseado em distancia)
# ==============================================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)

# ==============================================================================
#  OTIMIZACAO DE HIPERPARAMETROS
# ==============================================================================
print("Otimizando Random Forest via GridSearchCV (5-fold)...")
cv_grid = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
grid    = GridSearchCV(
    RandomForestClassifier(random_state=RANDOM_STATE),
    {'n_estimators': N_EST_RANGE, 'max_depth': DEPTH_RANGE},
    cv=cv_grid, scoring='accuracy', n_jobs=1
)
grid.fit(X_train, y_train)

n_est_best  = grid.best_params_['n_estimators']
depth_best  = grid.best_params_['max_depth']
print(f"Melhores params: n_estimators={n_est_best}, max_depth={depth_best}")
print(f"Acuracia CV 5-fold: {grid.best_score_*100:.2f}%")

# ==============================================================================
#  MODELO FINAL
# ==============================================================================
model = RandomForestClassifier(
    n_estimators=n_est_best, max_depth=depth_best, random_state=RANDOM_STATE
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
cv_10  = StratifiedKFold(n_splits=10, shuffle=True, random_state=RANDOM_STATE)
scores = cross_val_score(model, X, y, cv=cv_10, scoring='accuracy')

# ==============================================================================
#  RELATORIO
# ==============================================================================
sep  = "=" * 65
sep2 = "-" * 65

print(sep)
print("  RANDOM FOREST - CLASSIFICACAO DE DOENCA CARDIACA".center(65))
print(sep)
print(f"  n_estimators           : {n_est_best}")
print(f"  max_depth              : {depth_best}")
print(f"  Acuracia no teste      : {accuracy_score(y_test, y_pred)*100:.2f}%  ({len(y_test)} registros)")
print(f"  Cross-val (10-fold)    : {scores.mean()*100:.2f}% +/- {scores.std()*100:.2f}%")
print()

cm = confusion_matrix(y_test, y_pred)
print("  Matriz de confusao (teste):")
print(f"  {'':16} Pred=Saudavel  Pred=Doente")
print(f"  {'Real=Saudavel':<16} {cm[0,0]:>12}  {cm[0,1]:>10}")
print(f"  {'Real=Doente':<16} {cm[1,0]:>12}  {cm[1,1]:>10}")
print()
print("  Relatorio de classificacao:")
print(classification_report(y_test, y_pred,
      target_names=['Saudavel', 'Doente'], zero_division=0))

print(sep)
print("  IMPORTANCIA DAS VARIAVEIS (Feature Importance)")
print(sep2)

importancias = model.feature_importances_
ranking      = sorted(zip(colunas, importancias), key=lambda x: x[1], reverse=True)
barra_max    = 35

print(f"  {'VARIAVEL':<12} {'IMPORT.':>10}   BARRA")
print(f"  {sep2[:55]}")
for var, imp in ranking:
    barra = int(imp / ranking[0][1] * barra_max)
    print(f"  {var:<12} {imp*100:>8.2f}%   {'#' * barra}")
print(sep)
