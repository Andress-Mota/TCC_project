import os
import numpy as np
import logging
from joblib import parallel_backend
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, label_binarize
from sklearn.model_selection import (
    train_test_split, StratifiedKFold,
    cross_val_score, GridSearchCV
)
from sklearn.metrics import (
    accuracy_score, confusion_matrix, classification_report,
    roc_curve, auc, roc_auc_score
)

log = logging.getLogger(__name__)

RANDOM_STATE = 42
TEST_SIZE    = 0.2

# n_jobs>1 com o backend padrão (loky) abre processos separados, e cada um
# precisa reimportar os módulos do projeto — inclusive torch (via ml.cnn_model).
# Em máquinas com pouca RAM livre isso falha dentro do worker (o mesmo erro de
# "arquivo de paginação muito pequeno") e o joblib reporta como "falha ao
# un-serialize", escondendo a causa real. Por isso paralelizamos com threads
# (mesmo processo, nada para reimportar) em vez de processos.
_SAFE_N_JOBS = min(4, os.cpu_count() or 1)


def _build_base_models(k=14, svm_c=0.1, rf_n=50, rf_depth=10):
    knn = Pipeline([('sc', StandardScaler()),
                    ('knn', KNeighborsClassifier(n_neighbors=k))])
    svm = Pipeline([('sc', StandardScaler()),
                    ('svm', SVC(C=svm_c, kernel='rbf', gamma='scale',
                                probability=True, random_state=RANDOM_STATE))])
    rf  = RandomForestClassifier(
        n_estimators=rf_n, max_depth=rf_depth, random_state=RANDOM_STATE)
    logreg = Pipeline([('sc', StandardScaler()),
                       ('lr', LogisticRegression(max_iter=1000,
                                                 random_state=RANDOM_STATE))])
    nb = Pipeline([('sc', StandardScaler()), ('nb', GaussianNB())])
    return knn, svm, rf, logreg, nb


def _find_best_k(X_train, y_train):
    from sklearn.preprocessing import StandardScaler as SS
    log.info("  Buscando melhor K (1-20) via GridSearchCV 5-fold...")
    scaler = SS()
    Xs = scaler.fit_transform(X_train)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    grid = GridSearchCV(
        KNeighborsClassifier(),
        {'n_neighbors': list(range(1, 21))},
        cv=cv, scoring='accuracy', n_jobs=_SAFE_N_JOBS
    )
    with parallel_backend('threading', n_jobs=_SAFE_N_JOBS):
        grid.fit(Xs, y_train)
    best_k = grid.best_params_['n_neighbors']
    log.info(f"  Melhor K encontrado: {best_k} (score CV: {grid.best_score_:.4f})")
    return best_k


def _compute_roc(modelo, X_test, y_test, classes):
    try:
        n_classes = len(classes)
        if not hasattr(modelo, 'predict_proba'):
            return None, None

        y_prob = modelo.predict_proba(X_test)

        if n_classes == 2:
            fpr, tpr, _ = roc_curve(y_test, y_prob[:, 1])
            roc_auc_val = auc(fpr, tpr)
            roc_data = {
                'fpr': fpr.tolist(),
                'tpr': tpr.tolist(),
                'auc': round(roc_auc_val, 4),
            }
        else:
            y_bin = label_binarize(y_test, classes=list(range(n_classes)))
            roc_data = {'classes': classes, 'curves': []}
            aucs = []
            for i in range(n_classes):
                fpr, tpr, _ = roc_curve(y_bin[:, i], y_prob[:, i])
                auc_val = auc(fpr, tpr)
                aucs.append(auc_val)
                roc_data['curves'].append({
                    'class': classes[i],
                    'fpr': fpr.tolist(),
                    'tpr': tpr.tolist(),
                    'auc': round(auc_val, 4),
                })
            roc_auc_val = float(np.mean(aucs))
            roc_data['auc'] = round(roc_auc_val, 4)

        return round(roc_auc_val, 4), roc_data
    except Exception:
        return None, None


def train_and_evaluate(X, y, optimize_k=True, callback=None):
    # set(y) sobre um array numpy produz numpy.int64, que json.dumps não
    # serializa (isso só aparece com >2 classes, onde classes_list acaba em
    # roc_data). Convertendo para int nativo do Python.
    classes_list = sorted(int(c) for c in set(y))
    log.info("=== TREINAMENTO E AVALIAÇÃO ===")
    log.info(f"Amostras: {len(X)} | Classes: {len(classes_list)} | Features HOG: {X.shape[1]}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE,
        random_state=RANDOM_STATE, stratify=y
    )
    log.info(f"Divisao treino/teste: {len(X_train)} / {len(X_test)} amostras")

    if callback:
        callback(20, 'Otimizando K para KNN...')

    log.info("--- Otimizacao KNN ---")
    k = _find_best_k(X_train, y_train) if optimize_k else 14
    knn, svm, rf, logreg, nb = _build_base_models(k=k)

    estimadores = [
        ('knn',    knn),
        ('svm',    svm),
        ('rf',     rf),
        ('logreg', logreg),
        ('nb',     nb),
    ]

    individuais = {'KNN': knn, 'SVM': svm, 'Random Forest': rf,
                   'Logistic Regression': logreg, 'Naive Bayes': nb}
    ensembles = {
        'Voting Hard': VotingClassifier(estimators=estimadores, voting='hard'),
        'Voting Soft': VotingClassifier(estimators=estimadores, voting='soft'),
        'Stacking': StackingClassifier(
            estimators=estimadores,
            final_estimator=LogisticRegression(max_iter=1000,
                                               random_state=RANDOM_STATE),
            cv=5, n_jobs=_SAFE_N_JOBS
        ),
    }

    todos  = {**individuais, **ensembles}
    cv_10  = StratifiedKFold(n_splits=10, shuffle=True, random_state=RANDOM_STATE)

    resultados       = {}
    modelos_treinados = {}
    total = len(todos)

    log.info("--- Treinando modelos ---")
    for i, (nome, modelo) in enumerate(todos.items()):
        tipo = "ensemble" if nome in ensembles else "individual"
        log.info(f"[{i+1}/{total}] {nome} ({tipo})...")

        if callback:
            pct = 40 + int((i / total) * 50)
            callback(pct, f'Treinando {nome}...')

        try:
            with parallel_backend('threading', n_jobs=_SAFE_N_JOBS):
                modelo.fit(X_train, y_train)
                scores = cross_val_score(modelo, X, y, cv=cv_10, scoring='accuracy')
            y_pred = modelo.predict(X_test)
            cm     = confusion_matrix(y_test, y_pred)
            report = classification_report(
                y_test, y_pred, output_dict=True, zero_division=0)

            weighted    = report.get('weighted avg', {})
            acc_test    = float(accuracy_score(y_test, y_pred))
            cv_mean     = float(scores.mean())
            cv_std      = float(scores.std())
            roc_auc_val, roc_data = _compute_roc(modelo, X_test, y_test, classes_list)

            log.info(f"  CV 10-fold: {cv_mean*100:.2f}% (+/- {cv_std*100:.2f}%) | "
                     f"Teste: {acc_test*100:.2f}% | "
                     f"F1: {weighted.get('f1-score', 0)*100:.2f}%"
                     + (f" | ROC AUC: {roc_auc_val:.4f}" if roc_auc_val else ""))

            resultados[nome] = {
                'cv_mean':          cv_mean,
                'cv_std':           cv_std,
                'acc_test':         acc_test,
                'precision':        float(weighted.get('precision', 0)),
                'recall':           float(weighted.get('recall', 0)),
                'f1':               float(weighted.get('f1-score', 0)),
                'roc_auc':          roc_auc_val,
                'roc_data':         roc_data,
                'confusion_matrix': cm.tolist(),
                'model_type':       tipo,
            }
            modelos_treinados[nome] = modelo

        except Exception as e:
            log.error(f"  ERRO ao treinar {nome}: {e}", exc_info=True)
            raise

    melhor = max(resultados, key=lambda n: resultados[n]['cv_mean'])
    log.info("--- Resumo final ---")
    for nome, r in sorted(resultados.items(), key=lambda x: -x[1]['cv_mean']):
        log.info(f"  {nome:22s}  CV: {r['cv_mean']*100:.2f}%  Teste: {r['acc_test']*100:.2f}%")
    log.info(f"Melhor modelo: {melhor} (CV: {resultados[melhor]['cv_mean']*100:.2f}%)")
    log.info("=== TREINAMENTO CONCLUIDO ===")

    return resultados, modelos_treinados, k


def predict_image(modelo, features):
    pred = int(modelo.predict(features)[0])
    if hasattr(modelo, 'predict_proba'):
        confidence = float(max(modelo.predict_proba(features)[0]))
    else:
        confidence = 1.0
    return pred, confidence
