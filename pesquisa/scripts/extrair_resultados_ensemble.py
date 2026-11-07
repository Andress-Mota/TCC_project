"""
Extrai os resultados numericos do ensemble KNN+SVM e salva em JSON.
"""
import json, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")

from ucimlrepo import fetch_ucirepo
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             classification_report, roc_auc_score)
from sklearn.linear_model import LogisticRegression

RANDOM_STATE = 42

# ── Dados ──────────────────────────────────────────────────────────────────────
heart_disease = fetch_ucirepo(id=45)
X_raw = heart_disease.data['features']
y_raw = heart_disease.data['targets'].values.ravel()

colunas = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
           'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
X_raw = X_raw[colunas]

mask = X_raw.notna().all(axis=1) & pd.notna(y_raw)
X = X_raw[mask].reset_index(drop=True)
y_orig = pd.Series(y_raw[mask]).reset_index(drop=True)
y = (y_orig > 0).astype(int)

scaler = StandardScaler()
X_sc = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_sc, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y)

# ── Modelos base ──────────────────────────────────────────────────────────────
knn = KNeighborsClassifier(n_neighbors=29)
knn.fit(X_train, y_train)
y_pred_knn   = knn.predict(X_test)
y_proba_knn  = knn.predict_proba(X_test)[:, 1]

svm = SVC(C=0.1, kernel='rbf', gamma='scale', probability=True, random_state=RANDOM_STATE)
svm.fit(X_train, y_train)
y_pred_svm   = svm.predict(X_test)
y_proba_svm  = svm.predict_proba(X_test)[:, 1]

# ── Hard Voting ───────────────────────────────────────────────────────────────
y_pred_hard = np.where((y_pred_knn + y_pred_svm) >= 1, 1, 0)

# ── Soft Voting ───────────────────────────────────────────────────────────────
y_proba_soft   = (y_proba_knn + y_proba_svm) / 2
y_pred_soft    = (y_proba_soft >= 0.5).astype(int)

y_proba_wgt    = 0.45 * y_proba_knn + 0.55 * y_proba_svm
y_pred_wgt     = (y_proba_wgt >= 0.5).astype(int)

# ── Stacking ──────────────────────────────────────────────────────────────────
X_meta_train = np.hstack([
    knn.predict_proba(X_train)[:, 1].reshape(-1, 1),
    svm.predict_proba(X_train)[:, 1].reshape(-1, 1)
])
meta = LogisticRegression(random_state=RANDOM_STATE, max_iter=200)
meta.fit(X_meta_train, y_train)

X_meta_test    = np.hstack([y_proba_knn.reshape(-1, 1), y_proba_svm.reshape(-1, 1)])
y_pred_stk     = meta.predict(X_meta_test)
y_proba_stk    = meta.predict_proba(X_meta_test)[:, 1]

# ── Validacao Cruzada 10-fold ─────────────────────────────────────────────────
cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=RANDOM_STATE)

def cv_ensemble(X, y, cv, tipo):
    scores = []
    for tr, va in cv.split(X, y):
        k_ = KNeighborsClassifier(n_neighbors=29)
        s_ = SVC(C=0.1, kernel='rbf', gamma='scale', probability=True)
        k_.fit(X[tr], y[tr]); s_.fit(X[tr], y[tr])
        pk = k_.predict_proba(X[va])[:, 1]
        ps = s_.predict_proba(X[va])[:, 1]
        if tipo == 'hard':
            yp = np.where((k_.predict(X[va]) + s_.predict(X[va])) >= 1, 1, 0)
        elif tipo == 'soft':
            yp = ((pk + ps) / 2 >= 0.5).astype(int)
        elif tipo == 'wgt':
            yp = (0.45*pk + 0.55*ps >= 0.5).astype(int)
        else:  # stacking
            Xm_tr = np.hstack([k_.predict_proba(X[tr])[:, 1].reshape(-1,1),
                                s_.predict_proba(X[tr])[:, 1].reshape(-1,1)])
            m_ = LogisticRegression(random_state=RANDOM_STATE, max_iter=200)
            m_.fit(Xm_tr, y[tr])
            yp = m_.predict(np.hstack([pk.reshape(-1,1), ps.reshape(-1,1)]))
        scores.append(accuracy_score(y[va], yp))
    return np.array(scores)

cv_knn  = cross_val_score(KNeighborsClassifier(n_neighbors=29), X_sc, y, cv=cv)
cv_svm  = cross_val_score(SVC(C=0.1, kernel='rbf', gamma='scale', probability=True),
                          X_sc, y, cv=cv)
cv_hard = cv_ensemble(X_sc, np.array(y), cv, 'hard')
cv_soft = cv_ensemble(X_sc, np.array(y), cv, 'soft')
cv_wgt  = cv_ensemble(X_sc, np.array(y), cv, 'wgt')
cv_stk  = cv_ensemble(X_sc, np.array(y), cv, 'stacking')

# ── Metricas ──────────────────────────────────────────────────────────────────
cm_knn = confusion_matrix(y_test, y_pred_knn).tolist()
cm_svm = confusion_matrix(y_test, y_pred_svm).tolist()
cm_wgt = confusion_matrix(y_test, y_pred_wgt).tolist()
cm_stk = confusion_matrix(y_test, y_pred_stk).tolist()

cr_wgt = classification_report(y_test, y_pred_wgt,
                                target_names=["Saudavel", "Doente"],
                                output_dict=True)
cr_stk = classification_report(y_test, y_pred_stk,
                                target_names=["Saudavel", "Doente"],
                                output_dict=True)

concordancia = float(np.mean(y_pred_knn == y_pred_svm))

resultado = {
    "dataset": {
        "total_original": 303,
        "total_valido": int(mask.sum()),
        "removidos": 303 - int(mask.sum()),
        "classe_0_saudavel": 160,
        "classe_1_doente": 137,
        "treino": len(X_train),
        "teste": len(X_test)
    },
    "acuracia_teste": {
        "KNN_K29":            float(accuracy_score(y_test, y_pred_knn)),
        "SVM_C01_RBF":        float(accuracy_score(y_test, y_pred_svm)),
        "Hard_Voting":        float(accuracy_score(y_test, y_pred_hard)),
        "Soft_Voting":        float(accuracy_score(y_test, y_pred_soft)),
        "Soft_Voting_Pond":   float(accuracy_score(y_test, y_pred_wgt)),
        "Stacking":           float(accuracy_score(y_test, y_pred_stk)),
    },
    "auc_roc": {
        "KNN_K29":          float(roc_auc_score(y_test, y_proba_knn)),
        "SVM_C01_RBF":      float(roc_auc_score(y_test, y_proba_svm)),
        "Soft_Voting":      float(roc_auc_score(y_test, y_proba_soft)),
        "Soft_Voting_Pond": float(roc_auc_score(y_test, y_proba_wgt)),
        "Stacking":         float(roc_auc_score(y_test, y_proba_stk)),
    },
    "cv_10fold": {
        "KNN":   {"media": float(cv_knn.mean()),  "std": float(cv_knn.std()),  "scores": cv_knn.tolist()},
        "SVM":   {"media": float(cv_svm.mean()),  "std": float(cv_svm.std()),  "scores": cv_svm.tolist()},
        "Hard":  {"media": float(cv_hard.mean()), "std": float(cv_hard.std()), "scores": cv_hard.tolist()},
        "Soft":  {"media": float(cv_soft.mean()), "std": float(cv_soft.std()), "scores": cv_soft.tolist()},
        "Pond":  {"media": float(cv_wgt.mean()),  "std": float(cv_wgt.std()),  "scores": cv_wgt.tolist()},
        "Stack": {"media": float(cv_stk.mean()),  "std": float(cv_stk.std()),  "scores": cv_stk.tolist()},
    },
    "matrizes_confusao": {
        "KNN": cm_knn, "SVM": cm_svm,
        "Soft_Voting_Pond": cm_wgt, "Stacking": cm_stk
    },
    "relatorio_classificacao": {
        "Soft_Voting_Pond": cr_wgt,
        "Stacking": cr_stk
    },
    "meta_coeficientes": {
        "KNN": float(meta.coef_[0][0]),
        "SVM": float(meta.coef_[0][1])
    },
    "concordancia_knn_svm": concordancia
}

out = "c:/Users/andre/Documents/TCC project/artigos_relatorios/ensemble_results.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=2, ensure_ascii=False)

print("Salvo em:", out)
for k, v in resultado["acuracia_teste"].items():
    print(f"  {k:<25} {v:.4f}")
print("CV 10-fold:")
for k, v in resultado["cv_10fold"].items():
    print(f"  {k:<10} {v['media']:.4f} +- {v['std']:.4f}")
print("AUC-ROC:")
for k, v in resultado["auc_roc"].items():
    print(f"  {k:<25} {v:.4f}")
print("Concordancia KNN-SVM:", resultado["concordancia_knn_svm"])
