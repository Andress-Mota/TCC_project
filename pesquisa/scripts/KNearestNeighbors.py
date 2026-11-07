import pandas as pd
import numpy as np
from ucimlrepo import fetch_ucirepo
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# ==============================================================================
#  CONFIGURACOES
# ==============================================================================
MODO_BINARIO   = True   # True  → 0 = saudável, 1 = doente (recomendado)
                        # False → 5 classes originais (0-4)
OTIMIZAR_K     = True   # True  → encontra o melhor K automaticamente via GridSearchCV
K_MANUAL       = 7      # usado apenas se OTIMIZAR_K = False
K_RANGE        = range(1, 31)  # intervalo de busca quando OTIMIZAR_K = True
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

# Remover linhas com valores faltantes
mask_valido = X_raw.notna().all(axis=1) & pd.notna(y_raw)
X = X_raw[mask_valido].reset_index(drop=True)
y_orig = pd.Series(y_raw[mask_valido]).reset_index(drop=True)

removidos = len(X_raw) - len(X)
print(f"Dados após limpeza: {len(X)} registros válidos (removidos {removidos} com valores faltantes)")

# Binarização opcional do target
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
#  PRÉ-PROCESSAMENTO
# ==============================================================================
scaler   = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)

# ==============================================================================
#  OTIMIZAÇÃO DE K  (GridSearchCV + StratifiedKFold)
# ==============================================================================
if OTIMIZAR_K:
    param_grid = {'n_neighbors': list(K_RANGE)}
    cv         = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    grid       = GridSearchCV(KNeighborsClassifier(), param_grid, cv=cv,
                              scoring='accuracy', n_jobs=-1)
    grid.fit(X_train, y_train)

    K_USADO    = grid.best_params_['n_neighbors']
    cv_scores  = grid.cv_results_['mean_test_score']
    print(f"\nMelhor K encontrado: {K_USADO}  "
          f"(acurácia CV média: {grid.best_score_*100:.2f}%)")

    # Exibir top-5 valores de K
    top5_idx = np.argsort(cv_scores)[::-1][:5]
    print("\nTop-5 valores de K na validação cruzada:")
    print(f"  {'K':<6} {'Acurácia CV'}")
    print(f"  {'-'*18}")
    for idx in top5_idx:
        k_val = list(K_RANGE)[idx]
        print(f"  {k_val:<6} {cv_scores[idx]*100:.2f}%")
else:
    K_USADO = K_MANUAL
    print(f"\nK manual definido: {K_USADO}")

# ==============================================================================
#  TREINAMENTO FINAL
# ==============================================================================
model = KNeighborsClassifier(n_neighbors=K_USADO)
model.fit(X_train, y_train)

# Previsões
y_pred_test = model.predict(X_test)
y_pred_all  = model.predict(X_scaled)

# Cross-validation no conjunto completo (avaliação mais robusta)
cv_final = StratifiedKFold(n_splits=10, shuffle=True, random_state=RANDOM_STATE)
scores_cv = cross_val_score(model, X_scaled, y, cv=cv_final, scoring='accuracy')

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
def formatar_relatorio(dados, previsoes, valores_reais, k,
                       scores_cv, y_train, y_test, y_pred_test):

    sep  = "=" * 90
    sep2 = "-" * 90

    print(sep)
    print("       RELATÓRIO DE CLASSIFICAÇÃO DE DOENÇA CARDÍACA - KNN".center(90))
    print(f"       Modo: {titulo_modo}".center(90))
    print(sep)

    # ------------------------------------------------------------------
    # Seção 1 – Tabela de previsões em blocos de 50
    # ------------------------------------------------------------------
    print("\n SEÇÃO 1 – DADOS E PREVISÕES (divididos em blocos de 50)\n")
    print(f"{'ID':<5} {'IDADE':<7} {'SEXO':<12} {'FC MÁX':<8} "
          f"{'PREV.':<6} {'INTERPRETAÇÃO':<20} {'REAL':<6} {'ACERTO'}")
    print(sep2)

    dados_r  = dados.reset_index(drop=True)
    reais_r  = pd.Series(valores_reais).reset_index(drop=True)
    prev_arr = np.array(previsoes)

    tamanho_bloco = 50
    blocos = []

    for inicio in range(0, len(prev_arr), tamanho_bloco):
        fim          = min(inicio + tamanho_bloco, len(prev_arr))
        acertos_bloco = 0

        if inicio > 0:
            print(sep2)
        num_bloco = inicio // tamanho_bloco + 1
        print(f"\n[BLOCO {num_bloco}] Registros {inicio+1} a {fim}\n")

        for i in range(inicio, fim):
            idade  = int(dados_r.iloc[i]['age'])
            sexo   = interpretar_sexo(dados_r.iloc[i]['sex'])
            fc_max = int(dados_r.iloc[i]['thalach'])
            prev   = int(prev_arr[i])
            real   = int(reais_r.iloc[i])
            interp = interpretar_classe(prev)
            acerto = "SIM" if prev == real else "NÃO"

            print(f"{i+1:<5} {idade:<7} {sexo:<12} {fc_max:<8} "
                  f"{prev:<6} {interp:<20} {real:<6} {acerto}")

            if prev == real:
                acertos_bloco += 1

        total_bloco   = fim - inicio
        ac_bloco      = acertos_bloco / total_bloco
        blocos.append(dict(num=num_bloco, ini=inicio+1, fim=fim,
                           acertos=acertos_bloco, total=total_bloco, ac=ac_bloco))

        print(sep2)
        print(f"  ACURÁCIA DO BLOCO {num_bloco}: "
              f"{acertos_bloco}/{total_bloco} acertos ({ac_bloco*100:.2f}%)")
        print()

    # Legenda
    print(sep2)
    print("""
 Como ler esta tabela:
  * PREV. : classe prevista pelo KNN.
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

    acertos_totais   = sum(b['acertos'] for b in blocos)
    total_registros  = sum(b['total']   for b in blocos)
    ac_geral         = acertos_totais / total_registros

    print(sep2)
    print(f"\n  ACURÁCIA GERAL ({total_registros} registros): "
          f"{acertos_totais}/{total_registros} = {ac_geral*100:.2f}%")

    # ------------------------------------------------------------------
    # Seção 3 – Avaliação do modelo
    # ------------------------------------------------------------------
    print(sep)
    print("\n SEÇÃO 3 – AVALIAÇÃO DO MODELO\n")
    print(f"  K utilizado (vizinhos)       : {k}")
    print(f"  Modo de classificação        : {titulo_modo}")
    print(f"  Total de registros           : {total_registros}")
    print()
    print(f"  Acurácia no conjunto de TESTE: {accuracy_score(y_test, y_pred_test)*100:.2f}%  "
          f"({len(y_test)} registros)")
    print(f"  Acurácia cross-val (10-fold) : {scores_cv.mean()*100:.2f}% "
          f"± {scores_cv.std()*100:.2f}%   ← métrica mais confiável")
    print(f"  Acurácia em TODOS os dados   : {ac_geral*100:.2f}%")
    print()

    # Qualidade
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

    # Matriz de confusão
    print("  Matriz de confusão (conjunto de teste):\n")
    cm     = confusion_matrix(y_test, y_pred_test)
    labels = sorted(desc_classes.keys())
    header = "         " + "".join(f"  Pred={l}" for l in labels)
    print(header)
    for i, row_label in enumerate(labels):
        linha = f"  Real={row_label}  " + "".join(f"  {cm[i,j]:6}" for j in range(len(labels)))
        print(linha)
    print()

    # Relatório de classificação
    print("  Relatório de classificação (conjunto de teste):\n")
    nomes = [desc_classes[l] for l in labels]
    print(classification_report(y_test, y_pred_test, target_names=nomes, zero_division=0))

    # ------------------------------------------------------------------
    # Seção 4 – Recomendações
    # ------------------------------------------------------------------
    print(sep)
    print("\n SEÇÃO 4 – RECOMENDAÇÕES PARA O TCC\n")
    print(f"""  1. O K={k} foi {'otimizado automaticamente via GridSearchCV' if OTIMIZAR_K else 'definido manualmente'}.
     Use sempre cross-validation para escolher K – evita overfitting.

  2. {'Binarização aplicada: reduz o problema de 5 classes para 2,' if MODO_BINARIO else 'Modo multiclasse ativo: considere binarizar (MODO_BINARIO = True)'}
     {'melhorando significativamente a acurácia e a interpretabilidade.' if MODO_BINARIO else 'para ganhar ~10–15 pontos percentuais de acurácia.'}

  3. A acurácia de cross-val ({scores_cv.mean()*100:.1f}%) é a métrica mais honesta para reportar
     no TCC – ela avalia o modelo em dados que ele nunca viu durante o treino.

  4. Para comparação no TCC, teste também:
       - Random Forest   → sklearn.ensemble.RandomForestClassifier
       - Gradient Boosting → sklearn.ensemble.GradientBoostingClassifier
     Ambos costumam superar KNN neste dataset.

  5. Variáveis mais relevantes neste dataset (literatura):
       cp (tipo de dor torácica), thal, ca, oldpeak, exang.
     Considere reportar a importância das variáveis se usar Random Forest.
""")
    print(sep)


# ==============================================================================
#  EXECUÇÃO DO RELATÓRIO
# ==============================================================================
formatar_relatorio(
    dados       = X,
    previsoes   = y_pred_all,
    valores_reais = y,
    k           = K_USADO,
    scores_cv   = scores_cv,
    y_train     = y_train,
    y_test      = y_test,
    y_pred_test = y_pred_test,
)