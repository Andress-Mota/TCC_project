import pandas as pd
import numpy as np
from ucimlrepo import fetch_ucirepo
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold, cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# ==============================================================================
#  CONFIGURACOES
# ==============================================================================
MODO_BINARIO   = True   # True  → 0 = saudável, 1 = doente (recomendado)
                        # False → 5 classes originais (0-4)
OTIMIZAR_RF    = True   # True  → busca melhor n_estimators e max_depth via GridSearchCV
N_EST_MANUAL   = 100    # usado apenas se OTIMIZAR_RF = False
MAX_DEPTH_MAN  = None   # usado apenas se OTIMIZAR_RF = False
N_EST_RANGE    = [50, 100, 200, 300, 500]
MAX_DEPTH_RANGE= [None, 5, 10, 15, 20]
TEST_SIZE      = 0.2
RANDOM_STATE   = 42

# ==============================================================================
#  CARREGAMENTO E LIMPEZA
# ==============================================================================
heart_disease = fetch_ucirepo(id=45)

X_raw = heart_disease.data['features']
y_raw = heart_disease.data['targets'].values.ravel()

colunas = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
           'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']

X_raw = X_raw[colunas]

mask_valido = X_raw.notna().all(axis=1) & pd.notna(y_raw)
X = X_raw[mask_valido].reset_index(drop=True)
y_orig = pd.Series(y_raw[mask_valido]).reset_index(drop=True)

removidos = len(X_raw) - len(X)
print(f"Dados após limpeza: {len(X)} registros válidos (removidos {removidos} com valores faltantes)")

if MODO_BINARIO:
    y = (y_orig > 0).astype(int)
    desc_classes = {0: "Saudável", 1: "Doente"}
    titulo_modo  = "BINÁRIO (0 = Saudável / 1 = Doente)"
else:
    y = y_orig.copy()
    desc_classes = {0: "Sem doença", 1: "Risco baixo", 2: "Risco médio",
                    3: "Risco médio-alto", 4: "Risco elevado"}
    titulo_modo  = "MULTICLASSE (0–4)"

# ==============================================================================
#  DIVISÃO TREINO/TESTE  (sem normalização — RF não é baseado em distância)
# ==============================================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)

# ==============================================================================
#  OTIMIZAÇÃO DE HIPERPARÂMETROS  (GridSearchCV + StratifiedKFold)
# ==============================================================================
if OTIMIZAR_RF:
    param_grid = {
        'n_estimators': N_EST_RANGE,
        'max_depth'   : MAX_DEPTH_RANGE,
    }
    cv   = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    grid = GridSearchCV(
        RandomForestClassifier(random_state=RANDOM_STATE),
        param_grid, cv=cv, scoring='accuracy', n_jobs=-1
    )
    grid.fit(X_train, y_train)

    N_EST_USADO   = grid.best_params_['n_estimators']
    DEPTH_USADO   = grid.best_params_['max_depth']
    cv_grid_score = grid.best_score_

    print(f"\nMelhores hiperparâmetros encontrados:")
    print(f"  n_estimators : {N_EST_USADO}")
    print(f"  max_depth    : {DEPTH_USADO}")
    print(f"  Acurácia CV  : {cv_grid_score*100:.2f}%")

    print("\nTop-5 combinações na validação cruzada:")
    resultados_grid = pd.DataFrame(grid.cv_results_)
    top5 = resultados_grid.nlargest(5, 'mean_test_score')[
        ['param_n_estimators', 'param_max_depth', 'mean_test_score']
    ].reset_index(drop=True)
    print(f"  {'n_est':<8} {'max_depth':<12} {'Acurácia CV'}")
    print(f"  {'-'*30}")
    for _, row in top5.iterrows():
        depth_str = str(row['param_max_depth']) if row['param_max_depth'] is not None else 'None'
        print(f"  {int(row['param_n_estimators']):<8} {depth_str:<12} {row['mean_test_score']*100:.2f}%")
else:
    N_EST_USADO = N_EST_MANUAL
    DEPTH_USADO = MAX_DEPTH_MAN
    print(f"\nHiperparâmetros manuais: n_estimators={N_EST_USADO}, max_depth={DEPTH_USADO}")

# ==============================================================================
#  TREINAMENTO FINAL
# ==============================================================================
model = RandomForestClassifier(
    n_estimators=N_EST_USADO,
    max_depth=DEPTH_USADO,
    random_state=RANDOM_STATE
)
model.fit(X_train, y_train)

y_pred_test = model.predict(X_test)
y_pred_all  = model.predict(X)

cv_final  = StratifiedKFold(n_splits=10, shuffle=True, random_state=RANDOM_STATE)
scores_cv = cross_val_score(model, X, y, cv=cv_final, scoring='accuracy')

# ==============================================================================
#  FUNÇÕES AUXILIARES
# ==============================================================================
def interpretar_classe(valor):
    return desc_classes.get(int(valor), "Desconhecido")

def interpretar_sexo(valor):
    return "Masculino" if int(valor) == 1 else "Feminino"

# ==============================================================================
#  RELATÓRIO FORMATADO
# ==============================================================================
def formatar_relatorio():
    sep  = "=" * 90
    sep2 = "-" * 90

    print(sep)
    print("    RELATÓRIO DE CLASSIFICAÇÃO DE DOENÇA CARDÍACA - RANDOM FOREST".center(90))
    print(f"       Modo: {titulo_modo}".center(90))
    print(sep)

    # ------------------------------------------------------------------
    # Seção 1 – Tabela de previsões em blocos de 50
    # ------------------------------------------------------------------
    print("\n SEÇÃO 1 – DADOS E PREVISÕES (divididos em blocos de 50)\n")
    print(f"{'ID':<5} {'IDADE':<7} {'SEXO':<12} {'FC MÁX':<8} "
          f"{'PREV.':<6} {'INTERPRETAÇÃO':<20} {'REAL':<6} {'ACERTO'}")
    print(sep2)

    X_r      = X.reset_index(drop=True)
    y_r      = y.reset_index(drop=True)
    prev_arr = np.array(y_pred_all)

    tamanho_bloco = 50
    blocos = []

    for inicio in range(0, len(prev_arr), tamanho_bloco):
        fim           = min(inicio + tamanho_bloco, len(prev_arr))
        acertos_bloco = 0

        if inicio > 0:
            print(sep2)
        num_bloco = inicio // tamanho_bloco + 1
        print(f"\n[BLOCO {num_bloco}] Registros {inicio+1} a {fim}\n")

        for i in range(inicio, fim):
            idade  = int(X_r.iloc[i]['age'])
            sexo   = interpretar_sexo(X_r.iloc[i]['sex'])
            fc_max = int(X_r.iloc[i]['thalach'])
            prev   = int(prev_arr[i])
            real   = int(y_r.iloc[i])
            interp = interpretar_classe(prev)
            acerto = "SIM" if prev == real else "NÃO"

            print(f"{i+1:<5} {idade:<7} {sexo:<12} {fc_max:<8} "
                  f"{prev:<6} {interp:<20} {real:<6} {acerto}")

            if prev == real:
                acertos_bloco += 1

        total_bloco = fim - inicio
        ac_bloco    = acertos_bloco / total_bloco
        blocos.append(dict(num=num_bloco, ini=inicio+1, fim=fim,
                           acertos=acertos_bloco, total=total_bloco, ac=ac_bloco))

        print(sep2)
        print(f"  ACURÁCIA DO BLOCO {num_bloco}: "
              f"{acertos_bloco}/{total_bloco} acertos ({ac_bloco*100:.2f}%)")
        print()

    print(sep2)
    print("""
 Como ler esta tabela:
  * PREV. : classe prevista pelo Random Forest.
  * REAL  : diagnóstico clínico registrado.
  * ACERTO: indica se o modelo classificou corretamente o paciente.
""")

    # ------------------------------------------------------------------
    # Seção 2 – Resumo de acurácia por bloco
    # ------------------------------------------------------------------
    print(sep)
    print("\n SEÇÃO 2 – RESUMO DE ACURÁCIA POR BLOCO\n")
    print(f"{'BLOCO':<8} {'REGISTROS':<20} {'ACERTOS':<12} {'ACURÁCIA %'}")
    print(sep2)

    for b in blocos:
        print(f"{b['num']:<8} {str(b['ini'])+'-'+str(b['fim']):<20} "
              f"{str(b['acertos'])+'/'+str(b['total']):<12} {b['ac']*100:.2f}%")

    acertos_totais  = sum(b['acertos'] for b in blocos)
    total_registros = sum(b['total']   for b in blocos)
    ac_geral        = acertos_totais / total_registros

    print(sep2)
    print(f"\n  ACURÁCIA GERAL ({total_registros} registros): "
          f"{acertos_totais}/{total_registros} = {ac_geral*100:.2f}%")

    # ------------------------------------------------------------------
    # Seção 3 – Avaliação do modelo
    # ------------------------------------------------------------------
    print(sep)
    print("\n SEÇÃO 3 – AVALIAÇÃO DO MODELO\n")
    print(f"  Algoritmo                    : Random Forest")
    print(f"  n_estimators (árvores)       : {N_EST_USADO}")
    print(f"  max_depth                    : {DEPTH_USADO}")
    print(f"  Modo de classificação        : {titulo_modo}")
    print(f"  Total de registros           : {total_registros}")
    print()
    print(f"  Acurácia no conjunto de TESTE: {accuracy_score(y_test, y_pred_test)*100:.2f}%  "
          f"({len(y_test)} registros)")
    print(f"  Acurácia cross-val (10-fold) : {scores_cv.mean()*100:.2f}% "
          f"+/- {scores_cv.std()*100:.2f}%   (metrica mais confiavel)")
    print(f"  Acurácia em TODOS os dados   : {ac_geral*100:.2f}%")
    print()

    ref = scores_cv.mean()
    if ref < 0.60:
        qualidade = "FRACO – o modelo erra mais do que acerta."
    elif ref < 0.75:
        qualidade = "MODERADO – desempenho razoável, pode melhorar."
    elif ref < 0.85:
        qualidade = "BOM – classifica bem a maioria dos casos."
    else:
        qualidade = "EXCELENTE – alta precisão na classificação."

    print(f"  Avaliação: {qualidade}\n")

    labels = sorted(desc_classes.keys())
    print("  Matriz de confusão (conjunto de teste):\n")
    cm     = confusion_matrix(y_test, y_pred_test)
    header = "         " + "".join(f"  Pred={l}" for l in labels)
    print(header)
    for i, row_label in enumerate(labels):
        linha = f"  Real={row_label}  " + "".join(f"  {cm[i,j]:6}" for j in range(len(labels)))
        print(linha)
    print()

    print("  Relatório de classificação (conjunto de teste):\n")
    nomes = [desc_classes[l] for l in labels]
    print(classification_report(y_test, y_pred_test, target_names=nomes, zero_division=0))

    # ------------------------------------------------------------------
    # Seção 4 – Importância das variáveis  (exclusivo do Random Forest)
    # ------------------------------------------------------------------
    print(sep)
    print("\n SEÇÃO 4 – IMPORTÂNCIA DAS VARIÁVEIS (Feature Importance)\n")
    print("  Quanto maior o valor, mais a variável contribui para a decisão do modelo.\n")

    importancias = model.feature_importances_
    ranking = sorted(zip(colunas, importancias), key=lambda x: x[1], reverse=True)

    barra_max = 40
    print(f"  {'VARIÁVEL':<12} {'IMPORTÂNCIA':>12}   {'BARRA VISUAL'}")
    print(f"  {'-'*65}")
    for var, imp in ranking:
        barra  = int(imp / ranking[0][1] * barra_max)
        print(f"  {var:<12} {imp*100:>10.2f}%   {'#' * barra}")

    print(f"\n  Variável mais relevante : {ranking[0][0]}  ({ranking[0][1]*100:.2f}%)")
    print(f"  Variável menos relevante: {ranking[-1][0]}  ({ranking[-1][1]*100:.2f}%)")

    top3 = [v for v, _ in ranking[:3]]
    print(f"\n  Top-3 variáveis         : {', '.join(top3)}")
    print("""
  Interpretação clínica:
   * cp       – tipo de dor torácica (angina típica vs. atípica)
   * ca       – nº de vasos sanguíneos principais calcificados
   * thal     – tipo de talassemia (defeito cardíaco hereditário)
   * oldpeak  – depressão do segmento ST (isquemia durante exercício)
   * thalach  – frequência cardíaca máxima atingida
""")

    # ------------------------------------------------------------------
    # Seção 5 – Recomendações para o TCC
    # ------------------------------------------------------------------
    print(sep)
    print("\n SEÇÃO 5 – RECOMENDAÇÕES PARA O TCC\n")
    print(f"""  1. Random Forest usa {N_EST_USADO} árvores de decisão independentes e combina seus
     votos (bagging), o que reduz overfitting em relação a uma única árvore.

  2. {'Binarização aplicada: reduz o problema de 5 classes para 2,' if MODO_BINARIO else 'Modo multiclasse ativo: considere binarizar (MODO_BINARIO = True)'}
     {'melhorando significativamente a acurácia e a interpretabilidade.' if MODO_BINARIO else 'para ganhar ~10–15 pontos percentuais de acurácia.'}

  3. A acuracia de cross-val ({scores_cv.mean()*100:.1f}% +/- {scores_cv.std()*100:.1f}%) e a metrica mais honesta para
     reportar no TCC - avalia o modelo em dados nunca vistos durante o treino.

  4. Comparacao de modelos testados ate agora (binario, cross-val 10-fold):
       - Regressao Linear  : R2 aprox. 48%  (modelo base, regressao)
       - KNN               : ~82%           (ver saida do KNearestNeighbors.py)
       - SVM               : 83.5%          (C=0.1, kernel=rbf)
       - Random Forest     : {scores_cv.mean()*100:.1f}%          (n_estimators=50, max_depth=10)

  5. A Feature Importance (Seção 4) é um diferencial do RF: permite argumentar
     quais variáveis clínicas são mais determinantes para o diagnóstico.
""")
    print(sep)


# ==============================================================================
#  EXECUÇÃO
# ==============================================================================
formatar_relatorio()
