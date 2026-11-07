import pandas as pd
import numpy as np
from ucimlrepo import fetch_ucirepo
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import (train_test_split, GridSearchCV,
                                     StratifiedKFold, cross_val_score)
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# ==============================================================================
#  CONFIGURACOES
# ==============================================================================
TEST_SIZE    = 0.2
RANDOM_STATE = 42

OTIMIZAR_KNN = True
K_RANGE      = range(1, 31)
K_FIXO       = 14

SVM_C      = 0.1
SVM_KERNEL = 'rbf'
SVM_GAMMA  = 'scale'

RF_N_EST  = 50
RF_DEPTH  = 10

# ==============================================================================
#  CARREGAMENTO E LIMPEZA
# ==============================================================================
print("Carregando dados UCI Heart Disease...")
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
#  DIVISAO TREINO/TESTE
# ==============================================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)

# ==============================================================================
#  OTIMIZACAO DO K PARA KNN
# ==============================================================================
if OTIMIZAR_KNN:
    print("Otimizando K para KNN (GridSearchCV 5-fold)...")
    scaler_tmp = StandardScaler()
    X_train_sc = scaler_tmp.fit_transform(X_train)
    cv_grid    = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    grid_knn   = GridSearchCV(
        KNeighborsClassifier(), {'n_neighbors': list(K_RANGE)},
        cv=cv_grid, scoring='accuracy', n_jobs=1
    )
    grid_knn.fit(X_train_sc, y_train)
    K_MELHOR = grid_knn.best_params_['n_neighbors']
    print(f"Melhor K: {K_MELHOR}  (CV: {grid_knn.best_score_*100:.2f}%)")
else:
    K_MELHOR = K_FIXO

# ==============================================================================
#  DEFINICAO DOS MODELOS BASE
#  Cinco modelos com logicas completamente diferentes para maximizar diversidade:
#   - KNN      : baseado em distancia, nao-parametrico
#   - SVM      : maximiza margem, baseado em kernel
#   - RF       : arvores de decisao com bagging
#   - LogReg   : modelo linear probabilistico
#   - NaiveBayes: probabilidade condicional independente (suposicao oposta aos outros)
# ==============================================================================
knn_pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('knn',    KNeighborsClassifier(n_neighbors=K_MELHOR))
])

svm_pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('svm',    SVC(C=SVM_C, kernel=SVM_KERNEL, gamma=SVM_GAMMA,
                   probability=True, random_state=RANDOM_STATE))
])

rf_modelo = RandomForestClassifier(
    n_estimators=RF_N_EST, max_depth=RF_DEPTH, random_state=RANDOM_STATE
)

logreg_pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('lr',     LogisticRegression(max_iter=1000, random_state=RANDOM_STATE))
])

nb_pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('nb',     GaussianNB())
])

# ==============================================================================
#  ENSEMBLE — VOTING (5 modelos)
# ==============================================================================
estimadores_5 = [
    ('knn',    knn_pipe),
    ('svm',    svm_pipe),
    ('rf',     rf_modelo),
    ('logreg', logreg_pipe),
    ('nb',     nb_pipe),
]

ensemble_hard5 = VotingClassifier(estimators=estimadores_5, voting='hard')
ensemble_soft5 = VotingClassifier(estimators=estimadores_5, voting='soft')

# ==============================================================================
#  ENSEMBLE — STACKING
#  Os 5 modelos base geram previsoes que alimentam um meta-modelo.
#  O meta-modelo (LogReg) aprende como combinar os 5 de forma otima.
#  cv=5 garante que o meta-modelo seja treinado em dados que os base nunca viram.
# ==============================================================================
stacking = StackingClassifier(
    estimators=estimadores_5,
    final_estimator=LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
    cv=5,
    n_jobs=1
)

# ==============================================================================
#  TREINAMENTO
# ==============================================================================
print("\nTreinando modelos...")

# Modelos individuais exibidos na comparacao do TCC
individuais = {
    'KNN'          : knn_pipe,
    'SVM'          : svm_pipe,
    'Random Forest': rf_modelo,
}

# Ensembles (LR e NB sao usados internamente, nao aparecem individualmente)
ensembles = {
    'Voting Hard (5)': ensemble_hard5,
    'Voting Soft (5)': ensemble_soft5,
    'Stacking'       : stacking,
}

todos = {**individuais, **ensembles}

for nome, modelo in todos.items():
    print(f"  -> {nome}...")
    modelo.fit(X_train, y_train)

# ==============================================================================
#  AVALIACAO — CROSS-VALIDATION 10-FOLD
# ==============================================================================
print("\nExecutando cross-validation 10-fold...")
cv_10      = StratifiedKFold(n_splits=10, shuffle=True, random_state=RANDOM_STATE)
resultados = {}

for nome, modelo in todos.items():
    scores = cross_val_score(modelo, X, y, cv=cv_10, scoring='accuracy')
    y_pred = modelo.predict(X_test)
    resultados[nome] = {
        'cv_mean' : scores.mean(),
        'cv_std'  : scores.std(),
        'acc_test': accuracy_score(y_test, y_pred),
        'y_pred'  : y_pred,
    }
    print(f"  {nome:<20}: CV={scores.mean()*100:.2f}%  Teste={accuracy_score(y_test,y_pred)*100:.2f}%")

# ==============================================================================
#  RELATORIO FINAL
# ==============================================================================
sep  = "=" * 75
sep2 = "-" * 75

print("\n" + sep)
print("  COMPARACAO FINAL — KNN / SVM / Random Forest / Ensembles".center(75))
print("  Dataset: UCI Heart Disease | Binario | Cross-val 10-fold".center(75))
print(sep)

melhor_cv   = max(resultados, key=lambda n: resultados[n]['cv_mean'])
melhor_test = max(resultados, key=lambda n: resultados[n]['acc_test'])

print(f"\n  {'MODELO':<22} {'CV (10-fold)':>13} {'DESVIO':>8} {'TESTE':>8}   TIPO")
print(f"  {sep2[:70]}")

tipos = {
    'KNN'            : 'individual',
    'SVM'            : 'individual',
    'Random Forest'  : 'individual',
    'Voting Hard (5)': 'ensemble',
    'Voting Soft (5)': 'ensemble',
    'Stacking'       : 'ensemble',
}

for nome, r in resultados.items():
    destaque = ''
    if nome == melhor_cv:
        destaque = ' <-- melhor CV'
    elif nome == melhor_test and nome != melhor_cv:
        destaque = ' <-- melhor Teste'
    print(f"  {nome:<22} {r['cv_mean']*100:>11.2f}%  {r['cv_std']*100:>6.2f}%  "
          f"{r['acc_test']*100:>6.2f}%   [{tipos[nome]}]{destaque}")

print(f"  {sep2[:70]}")
print("""
  Como interpretar:
   * CV (10-fold)    : metrica principal — 10 treinos em dados nunca vistos.
   * Desvio          : estabilidade; menor = mais confiavel.
   * Stacking        : meta-modelo (LR) aprende a combinacao otima dos 5 base.
   * Voting (5)      : KNN+SVM+RF+LR+NB votam — diversidade maxima.
   * LR e NB         : usados internamente no ensemble, nao comparados sozinhos.
""")

# Detalhe por modelo
print(sep)
print("  DETALHAMENTO POR MODELO (conjunto de teste)")
print(sep)

for nome, r in resultados.items():
    print(f"\n  [{nome}]  CV={r['cv_mean']*100:.2f}% +/-{r['cv_std']*100:.2f}%  |  Teste={r['acc_test']*100:.2f}%")
    cm = confusion_matrix(y_test, r['y_pred'])
    print(f"  {'':18} Pred=Saudavel  Pred=Doente")
    print(f"  {'Real=Saudavel':<18} {cm[0,0]:>12}  {cm[0,1]:>10}")
    print(f"  {'Real=Doente':<18} {cm[1,0]:>12}  {cm[1,1]:>10}")
    report = classification_report(y_test, r['y_pred'],
             target_names=['Saudavel', 'Doente'], zero_division=0)
    for linha in report.splitlines():
        print("  " + linha)
    print(sep2)

# Analise de erros
print(sep)
print("  ANALISE DE ERROS — MODELOS INDIVIDUAIS vs STACKING")
print(sep)

y_t = np.array(y_test)
for nome in ['KNN', 'SVM', 'Random Forest', 'Stacking']:
    erros = (np.array(resultados[nome]['y_pred']) != y_t).sum()
    print(f"  {nome:<22}: {erros} erros de {len(y_t)} ({erros/len(y_t)*100:.1f}%)")

preds_3 = [np.array(resultados[n]['y_pred']) for n in ['KNN', 'SVM', 'Random Forest']]
erros_todos = np.where(np.all([p != y_t for p in preds_3], axis=0))[0]
erros_stack = (np.array(resultados['Stacking']['y_pred']) != y_t)

print(f"\n  Casos em que KNN + SVM + RF erraram juntos : {len(erros_todos)}")
print(f"  Stacking corrigiu desses casos             : "
      f"{sum(not erros_stack[i] for i in erros_todos)}")
print(sep)
