import pandas as pd
from ucimlrepo import fetch_ucirepo
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Carregar os dados do UCI
heart_disease = fetch_ucirepo(id=45)
data = heart_disease.data['features']

if data is not None:
    print("Dados carregados com sucesso.")
else:
    print("Erro ao carregar os dados.")
    data = None

if data is not None:
    X = data[['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']]
    y = heart_disease.data['targets'].values.ravel()

    # Remover linhas com valores faltantes (NaN)
    valid_indices = X.notna().all(axis=1) & pd.notna(y)
    X = X[valid_indices].reset_index(drop=True)
    y = y[valid_indices]
    
    print(f"Dados após limpeza: {len(X)} registros válidos (removidos {len(data) - len(X)} com valores faltantes)")

    # Normalizar os dados (essencial para KNN, pois é baseado em distância)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    print("\n" + "="*80)
    print("OTIMIZAÇÃO DE K PARA KNN".center(80))
    print("="*80)
    print("\nTestando diferentes valores de K...\n")
    print(f"{'K':<5} {'Acurácia Treino':<20} {'Acurácia Teste':<20} {'CV Score (5-fold)':<20}")
    print("-"*80)

    # Testar diferentes valores de K
    resultados = []
    k_values = [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 25, 29]

    for k in k_values:
        model = KNeighborsClassifier(n_neighbors=k)
        model.fit(X_train, y_train)
        
        # Acurácia no treino
        y_pred_train = model.predict(X_train)
        acc_train = accuracy_score(y_train, y_pred_train)
        
        # Acurácia no teste
        y_pred_test = model.predict(X_test)
        acc_test = accuracy_score(y_test, y_pred_test)
        
        # Validação cruzada (5-fold)
        cv_scores = cross_val_score(model, X_train, y_train, cv=5)
        cv_mean = cv_scores.mean()
        
        resultados.append({
            'k': k,
            'acc_train': acc_train,
            'acc_test': acc_test,
            'cv_mean': cv_mean,
            'model': model
        })
        
        print(f"{k:<5} {acc_train:<20.4f} {acc_test:<20.4f} {cv_mean:<20.4f}")

    print("-"*80)

    # Encontrar melhor K
    melhor = max(resultados, key=lambda x: x['cv_mean'])
    print(f"\nMELHOR K: {melhor['k']} com CV Score = {melhor['cv_mean']:.4f} ({melhor['cv_mean']*100:.2f}%)")
    print(f"  Acurácia no teste: {melhor['acc_test']:.4f} ({melhor['acc_test']*100:.2f}%)")

    print("\n" + "="*80)
    print("ANÁLISE DOS RESULTADOS".center(80))
    print("="*80)

    print(f"""
RESUMO:
  • Melhor K encontrado: {melhor['k']}
  • Acurácia no teste com K={melhor['k']}: {melhor['acc_test']*100:.2f}%
  • Score de validação cruzada: {melhor['cv_mean']*100:.2f}%
  
OBSERVAÇÕES:
  • Validação cruzada (CV Score) é mais confiável que acurácia simples
  • K pequeno (3-5) tende a overfitting (acurácia alta no treino, baixa no teste)
  • K grande tende a underfitting (acurácia baixa em geral)
  • O valor ideal equilibra treino e teste

RECOMENDAÇÃO:
  Use K={melhor['k']} para máxima acurácia generalizada no modelo final.
""")

    print("="*80)
