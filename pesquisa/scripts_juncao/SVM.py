import pandas as pd
import numpy as np
from ucimlrepo import fetch_ucirepo
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# ==============================================================================
#  CONFIGURACOES
# ==============================================================================
TEST_SIZE    = 0.2
RANDOM_STATE = 42

PARAM_GRID = {
    'C'     : [0.1, 1, 10, 100],
    'kernel': ['linear', 'rbf', 'poly'],
    'gamma' : ['scale', 'auto'],
}

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
#  PRE-PROCESSAMENTO
# ==============================================================================
scaler   = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)

# ==============================================================================
#  OTIMIZACAO DE HIPERPARAMETROS
# ==============================================================================
print("Otimizando SVM via GridSearchCV (5-fold)...")
cv_grid = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
grid    = GridSearchCV(
    SVC(random_state=RANDOM_STATE),
    PARAM_GRID, cv=cv_grid, scoring='accuracy', n_jobs=1
)
grid.fit(X_train, y_train)

C_best      = grid.best_params_['C']
kernel_best = grid.best_params_['kernel']
gamma_best  = grid.best_params_['gamma']
print(f"Melhores params: C={C_best}, kernel={kernel_best}, gamma={gamma_best}")
print(f"Acuracia CV 5-fold: {grid.best_score_*100:.2f}%")

# ==============================================================================
#  MODELO FINAL
# ==============================================================================
model = SVC(C=C_best, kernel=kernel_best, gamma=gamma_best, random_state=RANDOM_STATE)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
cv_10  = StratifiedKFold(n_splits=10, shuffle=True, random_state=RANDOM_STATE)
scores = cross_val_score(model, X_scaled, y, cv=cv_10, scoring='accuracy')

# ==============================================================================
#  RELATORIO
# ==============================================================================
sep  = "=" * 65
sep2 = "-" * 65

print(sep)
print("  SVM - CLASSIFICACAO DE DOENCA CARDIACA (BINARIO)".center(65))
print(sep)
print(f"  C                      : {C_best}")
print(f"  Kernel                 : {kernel_best}")
print(f"  Gamma                  : {gamma_best}")
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
