import pandas as pd
import numpy as np
from ucimlrepo import fetch_ucirepo
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# ==============================================================================
#  CONFIGURAÇÕES
#  Flags e hiperparâmetros centralizados aqui para facilitar ajustes no TCC.
# ==============================================================================

# True  → problema binário: 0 = Saudável, 1 = Doente  (recomendado para SVM)
# False → 5 classes originais (0–4) do dataset UCI
MODO_BINARIO = True

# True  → otimiza C, kernel e gamma automaticamente via GridSearchCV
# False → usa os valores manuais definidos abaixo
OTIMIZAR_SVM = True

# Hiperparâmetros manuais (usados somente se OTIMIZAR_SVM = False)
C_MANUAL      = 1.0          # penalidade por erro de classificação
KERNEL_MANUAL = 'rbf'        # função de kernel: 'linear', 'rbf', 'poly', 'sigmoid'
GAMMA_MANUAL  = 'scale'      # coeficiente do kernel: 'scale', 'auto' ou float

# Grade de busca quando OTIMIZAR_SVM = True
# C alto → fronteira mais rígida (menos tolerância a erros)
# C baixo → fronteira mais suave (mais tolerância, menos overfitting)
PARAM_GRID = {
    'C'      : [0.1, 1, 10, 100],
    'kernel' : ['linear', 'rbf', 'poly'],
    'gamma'  : ['scale', 'auto'],
}

TEST_SIZE    = 0.2   # 20 % dos dados reservados para teste final
RANDOM_STATE = 42    # semente aleatória — garante reprodutibilidade dos resultados

# ==============================================================================
#  CARREGAMENTO E LIMPEZA DOS DADOS
#  Usa a mesma base UCI Heart Disease (id=45) do arquivo KNearestNeighbors.py.
#  As 13 features clínicas são as mesmas usadas na literatura para este dataset.
# ==============================================================================
print("Carregando base de dados UCI Heart Disease (id=45)...")
heart_disease = fetch_ucirepo(id=45)

# Separar features (X) e target (y)
X_raw = heart_disease.data['features']
y_raw = heart_disease.data['targets'].values.ravel()

# Selecionar apenas as 13 colunas clínicas relevantes
# (remove colunas extras que o UCI pode retornar)
colunas = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
           'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']

X_raw = X_raw[colunas]

# Remover linhas com qualquer valor faltante (NaN) em X ou y
# O SVM não aceita NaN — remoção é mais segura do que imputação para este dataset
mask_valido = X_raw.notna().all(axis=1) & pd.notna(y_raw)
X     = X_raw[mask_valido].reset_index(drop=True)
y_orig = pd.Series(y_raw[mask_valido]).reset_index(drop=True)

removidos = len(X_raw) - len(X)
print(f"Dados após limpeza: {len(X)} registros válidos "
      f"(removidos {removidos} com valores faltantes)")

# ==============================================================================
#  BINARIZAÇÃO DO TARGET (opcional)
#  O dataset original tem 5 classes (0–4) de severidade da doença.
#  Para classificação binária: 0 = sem doença, qualquer valor > 0 = doença.
#  SVMs tendem a ter melhor desempenho com menos classes.
# ==============================================================================
if MODO_BINARIO:
    y            = (y_orig > 0).astype(int)
    desc_classes = {0: "Saudável", 1: "Doente"}
    titulo_modo  = "BINÁRIO (0 = Saudável / 1 = Doente)"
else:
    y            = y_orig.copy()
    desc_classes = {0: "Sem doença", 1: "Risco baixo", 2: "Risco médio",
                    3: "Risco médio-alto", 4: "Risco elevado"}
    titulo_modo  = "MULTICLASSE (0–4)"

# ==============================================================================
#  PRÉ-PROCESSAMENTO — NORMALIZAÇÃO
#  CRÍTICO para SVM: o algoritmo usa distâncias no espaço de features.
#  Sem normalização, features com valores grandes (ex.: colesterol ~200)
#  dominariam features pequenas (ex.: sexo = 0/1), distorcendo a fronteira.
#  StandardScaler transforma cada feature para média=0 e desvio padrão=1.
# ==============================================================================
scaler   = StandardScaler()
X_scaled = scaler.fit_transform(X)   # fit + transform no conjunto completo

# Dividir em treino (80%) e teste (20%) com estratificação
# stratify=y garante proporção igual de classes em treino e teste
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y,
    test_size    = TEST_SIZE,
    random_state = RANDOM_STATE,
    stratify     = y
)

print(f"\nDivisão treino/teste: {len(X_train)} treino / {len(X_test)} teste")
print(f"Distribuição de classes no treino: {dict(pd.Series(y_train).value_counts().sort_index())}")

# ==============================================================================
#  OTIMIZAÇÃO DE HIPERPARÂMETROS (GridSearchCV + StratifiedKFold)
#  Testa todas as combinações de C, kernel e gamma.
#  StratifiedKFold(5) divide o treino em 5 folds mantendo proporção de classes.
#  A combinação com maior acurácia média nos 5 folds é escolhida.
#  n_jobs=-1 usa todos os núcleos da CPU em paralelo.
# ==============================================================================
if OTIMIZAR_SVM:
    print("\nOtimizando hiperparâmetros do SVM (GridSearchCV 5-fold)...")
    print("Combinações testadas:", np.prod([len(v) for v in PARAM_GRID.values()]),
          "× 5 folds =",
          np.prod([len(v) for v in PARAM_GRID.values()]) * 5, "treinos")

    cv   = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    grid = GridSearchCV(
        SVC(random_state=RANDOM_STATE, probability=False),
        PARAM_GRID,
        cv      = cv,
        scoring = 'accuracy',
        n_jobs  = 1,
        verbose = 0,
    )
    grid.fit(X_train, y_train)

    # Extrair os melhores parâmetros encontrados
    MELHOR_C      = grid.best_params_['C']
    MELHOR_KERNEL = grid.best_params_['kernel']
    MELHOR_GAMMA  = grid.best_params_['gamma']

    print(f"\nMelhores parâmetros encontrados:")
    print(f"  C      = {MELHOR_C}")
    print(f"  kernel = {MELHOR_KERNEL}")
    print(f"  gamma  = {MELHOR_GAMMA}")
    print(f"  Acurácia CV média: {grid.best_score_*100:.2f}%")

    # Exibir top-5 combinações de hiperparâmetros
    resultados = pd.DataFrame(grid.cv_results_)
    top5 = resultados.nlargest(5, 'mean_test_score')[
        ['param_C', 'param_kernel', 'param_gamma', 'mean_test_score', 'std_test_score']
    ].reset_index(drop=True)

    print("\nTop-5 combinações de hiperparâmetros na validação cruzada:")
    print(f"  {'#':<4} {'C':<8} {'kernel':<10} {'gamma':<8} {'Acurácia CV':<14} {'Desvio'}")
    print(f"  {'-'*55}")
    for i, row in top5.iterrows():
        print(f"  {i+1:<4} {str(row['param_C']):<8} {str(row['param_kernel']):<10} "
              f"{str(row['param_gamma']):<8} {row['mean_test_score']*100:.2f}%"
              f"          ±{row['std_test_score']*100:.2f}%")
else:
    # Usar os hiperparâmetros definidos manualmente no topo do arquivo
    MELHOR_C      = C_MANUAL
    MELHOR_KERNEL = KERNEL_MANUAL
    MELHOR_GAMMA  = GAMMA_MANUAL
    print(f"\nHiperparâmetros manuais: C={MELHOR_C}, kernel={MELHOR_KERNEL}, gamma={MELHOR_GAMMA}")

# ==============================================================================
#  TREINAMENTO FINAL DO MODELO SVM
#  Treina com os melhores hiperparâmetros encontrados (ou manuais)
#  usando TODO o conjunto de treino (sem folds).
# ==============================================================================
print("\nTreinando o modelo SVM final...")
model = SVC(
    C            = MELHOR_C,
    kernel       = MELHOR_KERNEL,
    gamma        = MELHOR_GAMMA,
    random_state = RANDOM_STATE,
)
model.fit(X_train, y_train)

# Previsões no conjunto de teste e em todos os dados (para o relatório)
y_pred_test = model.predict(X_test)
y_pred_all  = model.predict(X_scaled)

# ==============================================================================
#  VALIDAÇÃO CRUZADA FINAL (10-fold)
#  Avaliação mais robusta e honesta do modelo.
#  Treina e testa em 10 partições diferentes do dataset completo.
#  A média e o desvio padrão são a métrica recomendada para reportar no TCC.
# ==============================================================================
print("Executando validação cruzada final (10-fold)...")
cv_final  = StratifiedKFold(n_splits=10, shuffle=True, random_state=RANDOM_STATE)
scores_cv = cross_val_score(model, X_scaled, y, cv=cv_final, scoring='accuracy')

# ==============================================================================
#  FUNÇÕES AUXILIARES
# ==============================================================================
def interpretar_classe(valor):
    """Converte o código numérico da classe em texto legível."""
    return desc_classes.get(int(valor), "Desconhecido")

def interpretar_sexo(valor):
    """Converte o código numérico de sexo em texto (1=Masculino, 0=Feminino)."""
    return "Masculino" if int(valor) == 1 else "Feminino"

# ==============================================================================
#  RELATÓRIO FORMATADO
#  Mesmo formato do KNearestNeighbors.py para facilitar comparação no TCC.
# ==============================================================================
def formatar_relatorio(dados, previsoes, valores_reais,
                       scores_cv, y_train, y_test, y_pred_test):

    sep  = "=" * 90
    sep2 = "-" * 90

    print(sep)
    print("       RELATÓRIO DE CLASSIFICAÇÃO DE DOENÇA CARDÍACA - SVM".center(90))
    print(f"       Modo: {titulo_modo}".center(90))
    print(sep)

    # ------------------------------------------------------------------
    # Seção 1 – Tabela de previsões em blocos de 50 registros
    # Exibe: ID, idade, sexo, FC máxima, previsão, classe interpretada,
    #        valor real e se o modelo acertou.
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
        fim           = min(inicio + tamanho_bloco, len(prev_arr))
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

        total_bloco = fim - inicio
        ac_bloco    = acertos_bloco / total_bloco
        blocos.append(dict(num=num_bloco, ini=inicio+1, fim=fim,
                           acertos=acertos_bloco, total=total_bloco, ac=ac_bloco))

        print(sep2)
        print(f"  ACURÁCIA DO BLOCO {num_bloco}: "
              f"{acertos_bloco}/{total_bloco} acertos ({ac_bloco*100:.2f}%)")
        print()

    # Legenda da tabela
    print(sep2)
    print("""
 Como ler esta tabela:
  * PREV. : classe prevista pelo SVM.
  * REAL  : diagnóstico clínico registrado no dataset.
  * ACERTO: indica se o modelo classificou corretamente o paciente.
""")

    # ------------------------------------------------------------------
    # Seção 2 – Resumo de acurácia por bloco
    # Útil para identificar se o desempenho varia ao longo do dataset.
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
    # Seção 3 – Avaliação completa do modelo
    # Inclui: métricas de desempenho, matriz de confusão e
    # classification report (precisão, recall, F1 por classe).
    # ------------------------------------------------------------------
    print(sep)
    print("\n SEÇÃO 3 – AVALIAÇÃO DO MODELO\n")
    print(f"  Algoritmo                    : Support Vector Machine (SVM)")
    print(f"  Kernel utilizado             : {MELHOR_KERNEL}")
    print(f"  Parâmetro C                  : {MELHOR_C}")
    print(f"  Parâmetro gamma              : {MELHOR_GAMMA}")
    print(f"  Modo de classificação        : {titulo_modo}")
    print(f"  Total de registros           : {total_registros}")
    print(f"  Otimização de hiperparâmetros: "
          f"{'GridSearchCV (automático)' if OTIMIZAR_SVM else 'Manual'}")
    print()
    print(f"  Acurácia no conjunto de TESTE: "
          f"{accuracy_score(y_test, y_pred_test)*100:.2f}%  ({len(y_test)} registros)")
    print(f"  Acurácia cross-val (10-fold) : {scores_cv.mean()*100:.2f}% "
          f"+/- {scores_cv.std()*100:.2f}%   (metrica mais confiavel)")
    print(f"  Acurácia em TODOS os dados   : {ac_geral*100:.2f}%")
    print()

    # Classificação qualitativa do desempenho
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

    # Matriz de confusão:
    # Linhas = classe real, Colunas = classe prevista
    # Diagonal principal = acertos; fora da diagonal = erros
    print("  Matriz de confusão (conjunto de teste):\n")
    cm     = confusion_matrix(y_test, y_pred_test)
    labels = sorted(desc_classes.keys())
    header = "         " + "".join(f"  Pred={l}" for l in labels)
    print(header)
    for i, row_label in enumerate(labels):
        linha = f"  Real={row_label}  " + "".join(f"  {cm[i,j]:6}" for j in range(len(labels)))
        print(linha)
    print()

    # Classification report: precision, recall e F1-score por classe
    # Precision = dos que o modelo disse "doente", quantos eram de fato doentes
    # Recall    = dos que eram de fato doentes, quantos o modelo identificou
    # F1        = média harmônica entre precision e recall
    print("  Relatório de classificação (conjunto de teste):\n")
    nomes = [desc_classes[l] for l in labels]
    print(classification_report(y_test, y_pred_test, target_names=nomes, zero_division=0))

    # ------------------------------------------------------------------
    # Seção 4 – Recomendações para o TCC
    # Orientações acadêmicas sobre como interpretar e reportar os resultados.
    # ------------------------------------------------------------------
    print(sep)
    print("\n SEÇÃO 4 – RECOMENDAÇÕES PARA O TCC\n")

    otim_texto = "GridSearchCV automático" if OTIMIZAR_SVM else "manual"
    print(f"""  1. Hiperparâmetros otimizados via {otim_texto}: C={MELHOR_C}, \
kernel={MELHOR_KERNEL}, gamma={MELHOR_GAMMA}.
     Sempre use GridSearchCV para escolher hiperparâmetros — evita overfitting
     e garante que os valores sejam justificados por dados, não por tentativa e erro.

  2. Por que normalizar é obrigatório no SVM?
     O SVM maximiza a margem entre classes usando distâncias. Features não
     normalizadas enviesam esse cálculo. O StandardScaler garante que todas
     as features contribuam igualmente.

  3. A acurácia de cross-val ({scores_cv.mean()*100:.1f}% ± {scores_cv.std()*100:.1f}%) é a métrica mais \
honesta para reportar
     no TCC - avalia o modelo em dados que ele nunca viu durante o treino.
     Reporte sempre media +/- desvio-padrao.

  4. Comparação com KNN (recomendada para o TCC):
     - KNN: não-paramétrico, sensível a ruído, K otimizável
     - SVM: paramétrico, robusto em alta dimensão, depende de C e kernel
     SVMs geralmente superam KNN em datasets médios com features contínuas.

  5. Variáveis mais relevantes neste dataset (literatura):
       cp (tipo de dor torácica), thal, ca, oldpeak, exang.
     Para SVM com kernel linear, os coeficientes do hiperplano indicam
     a importância relativa de cada feature — considere reportar isso no TCC.
""")
    print(sep)


# ==============================================================================
#  EXECUÇÃO DO RELATÓRIO
# ==============================================================================
formatar_relatorio(
    dados         = X,
    previsoes     = y_pred_all,
    valores_reais = y,
    scores_cv     = scores_cv,
    y_train       = y_train,
    y_test        = y_test,
    y_pred_test   = y_pred_test,
)
