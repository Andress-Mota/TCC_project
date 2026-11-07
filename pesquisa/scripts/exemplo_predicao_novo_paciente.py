"""
EXEMPLO PRÁTICO: Usando o Ensemble para Predição em Novo Paciente
Demonstra como usar o modelo treinado para diagnosticar um novo caso
"""

import pandas as pd
import numpy as np
from ucimlrepo import fetch_ucirepo
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

print("\n" + "="*80)
print("ENSEMBLE LEARNING - EXEMPLO DE PREDIÇÃO EM NOVO PACIENTE")
print("="*80)

# ==============================================================================
#  PASSO 1: TREINAR O ENSEMBLE (usar dados históricos)
# ==============================================================================
print("\n[1] Treinando ensemble com dados históricos...")

# Carregar dados
heart_disease = fetch_ucirepo(id=45)
X_raw = heart_disease.data['features']
y_raw = heart_disease.data['targets'].values.ravel()

colunas = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
           'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
X_raw = X_raw[colunas]

# Limpeza
mask_valido = X_raw.notna().all(axis=1) & pd.notna(y_raw)
X = X_raw[mask_valido].reset_index(drop=True)
y = pd.Series(y_raw[mask_valido]).reset_index(drop=True)
y = (y > 0).astype(int)  # Binarizar

# Normalizar
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(f"  ✓ Dados carregados: {len(X)} pacientes históricos")

# Treinar modelos base
print("\n  Treinando KNN (K=29)...")
knn = KNeighborsClassifier(n_neighbors=29)
knn.fit(X_scaled, y)

print("  Treinando SVM (C=0.1, RBF)...")
svm = SVC(C=0.1, kernel='rbf', gamma='scale', probability=True, random_state=42)
svm.fit(X_scaled, y)

# Meta-learner para stacking
print("  Treinando meta-learner (Stacking)...")
y_proba_knn = knn.predict_proba(X_scaled)[:, 1].reshape(-1, 1)
y_proba_svm = svm.predict_proba(X_scaled)[:, 1].reshape(-1, 1)
X_meta = np.hstack([y_proba_knn, y_proba_svm])
meta_model = LogisticRegression(random_state=42, max_iter=200)
meta_model.fit(X_meta, y)

print("  ✓ Ensemble treinado!")

# ==============================================================================
#  PASSO 2: DADOS DO NOVO PACIENTE
# ==============================================================================
print("\n[2] Novo Paciente - Dados Clínicos")
print("     " + "-"*60)

# Exemplo 1: Paciente com baixo risco
novo_paciente_1 = {
    'age': 45,           # Idade 45 anos
    'sex': 1,            # Homem (1 = male)
    'cp': 0,             # Tipo de dor torácica: típica
    'trestbps': 120,     # Pressão sanguínea: 120 mmHg
    'chol': 200,         # Colesterol: 200 mg/dL
    'fbs': 0,            # Glicemia em jejum: < 120 mg/dL (não)
    'restecg': 0,        # ECG de repouso: normal
    'thalach': 85,       # Freq. cardíaca máxima: 85 bpm
    'exang': 0,          # Angina ao exercício: não
    'oldpeak': 0.0,      # Depressão ST: 0 mm
    'slope': 1,          # Slope ST: crescente (1 = upsloping)
    'ca': 0,             # Artérias calcificadas: 0
    'thal': 2,           # Thalassemia: normal (2 = normal)
}

# Exemplo 2: Paciente com risco elevado
novo_paciente_2 = {
    'age': 65,           # Idade 65 anos
    'sex': 1,            # Homem
    'cp': 3,             # Tipo de dor torácica: assintomático (piora prognóstico)
    'trestbps': 140,     # Pressão sanguínea: 140 mmHg (elevada)
    'chol': 280,         # Colesterol: 280 mg/dL (elevado)
    'fbs': 1,            # Glicemia em jejum: > 120 mg/dL (sim, diabetes)
    'restecg': 1,        # ECG de repouso: anormal
    'thalach': 100,      # Freq. cardíaca máxima: 100 bpm
    'exang': 1,          # Angina ao exercício: sim
    'oldpeak': 2.5,      # Depressão ST: 2.5 mm (elevada)
    'slope': 2,          # Slope ST: plano (2 = flat)
    'ca': 2,             # Artérias calcificadas: 2
    'thal': 3,           # Thalassemia: reversível (3 = reversible defect)
}

# Exemplo 3: Paciente intermediário
novo_paciente_3 = {
    'age': 55,
    'sex': 0,            # Mulher (0 = female)
    'cp': 1,
    'trestbps': 130,
    'chol': 230,
    'fbs': 0,
    'restecg': 0,
    'thalach': 95,
    'exang': 0,
    'oldpeak': 0.5,
    'slope': 1,
    'ca': 1,
    'thal': 2,
}

# ==============================================================================
#  PASSO 3: PRÉ-PROCESSAMENTO DO NOVO DADO
# ==============================================================================
print("\n[3] Pré-processamento (Normalização Z-score)")

def processar_paciente(dados_dict, scaler, nome="Paciente"):
    """Converte e normaliza dados de um novo paciente"""
    # Converter para DataFrame
    df = pd.DataFrame([dados_dict], columns=colunas)
    # Normalizar
    df_scaled = scaler.transform(df)
    print(f"     ✓ {nome}: Dados normalizados")
    return df, df_scaled

df1, X1_scaled = processar_paciente(novo_paciente_1, scaler, "Paciente 1 (Baixo Risco)")
df2, X2_scaled = processar_paciente(novo_paciente_2, scaler, "Paciente 2 (Alto Risco)")
df3, X3_scaled = processar_paciente(novo_paciente_3, scaler, "Paciente 3 (Intermediário)")

# ==============================================================================
#  PASSO 4: PREDIÇÕES USANDO ENSEMBLE
# ==============================================================================
print("\n[4] Predições do Ensemble")
print("     " + "-"*60)

def prever_ensemble(X_scaled, knn, svm, meta_model, nome=""):
    """
    Prediz usando ensemble e retorna resultados detalhados
    """
    
    # Predições individuais
    p_knn = knn.predict_proba(X_scaled)[0, 1]
    p_svm = svm.predict_proba(X_scaled)[0, 1]
    
    # Ensemble: Soft Voting Ponderado (RECOMENDADO)
    p_ensemble_ponderado = 0.45 * p_knn + 0.55 * p_svm
    y_pred_ensemble = int(p_ensemble_ponderado >= 0.5)
    
    # Ensemble: Soft Voting Simples
    p_ensemble_simples = (p_knn + p_svm) / 2
    
    # Ensemble: Stacking
    X_meta = np.array([[p_knn, p_svm]])
    y_proba_stacking = meta_model.predict_proba(X_meta)[0]
    p_stacking = y_proba_stacking[1]
    y_pred_stacking = meta_model.predict(X_meta)[0]
    
    # Ensemble: Hard Voting
    y_pred_knn = knn.predict(X_scaled)[0]
    y_pred_svm = svm.predict(X_scaled)[0]
    y_pred_hard = int((y_pred_knn + y_pred_svm) >= 1)
    
    return {
        'p_knn': p_knn,
        'p_svm': p_svm,
        'p_ensemble_ponderado': p_ensemble_ponderado,
        'y_pred_ensemble': y_pred_ensemble,
        'p_ensemble_simples': p_ensemble_simples,
        'p_stacking': p_stacking,
        'y_pred_stacking': y_pred_stacking,
        'y_pred_hard': y_pred_hard,
    }

# Prever para os 3 pacientes
print("\n[PACIENTE 1 - BAIXO RISCO ESPERADO]")
print("Dados: Idade 45, sem sintomas severos, colesterol normal, sem CAD")
resultado1 = prever_ensemble(X1_scaled, knn, svm, meta_model)

print("\n  Probabilidades Individuais:")
print(f"    KNN (K=29):           P(Doença) = {resultado1['p_knn']:.4f} ({resultado1['p_knn']*100:.2f}%)")
print(f"    SVM (C=0.1, RBF):     P(Doença) = {resultado1['p_svm']:.4f} ({resultado1['p_svm']*100:.2f}%)")

print("\n  Ensemble - Soft Voting Ponderado (RECOMENDADO):")
print(f"    P(Doença) = 0.45 × {resultado1['p_knn']:.4f} + 0.55 × {resultado1['p_svm']:.4f}")
print(f"    P(Doença) = {resultado1['p_ensemble_ponderado']:.4f} ({resultado1['p_ensemble_ponderado']*100:.2f}%)")
print(f"    Decisão:   {'RISCO DE DOENCA' if resultado1['y_pred_ensemble'] == 1 else 'BAIXO RISCO'}")

print("\n  Ensemble - Soft Voting Simples:")
print(f"    P(Doença) = {resultado1['p_ensemble_simples']:.4f} ({resultado1['p_ensemble_simples']*100:.2f}%)")

print("\n  Ensemble - Stacking:")
print(f"    P(Doença) = {resultado1['p_stacking']:.4f} ({resultado1['p_stacking']*100:.2f}%)")
print(f"    Decisão:   {'⚠️  RISCO DE DOENÇA' if resultado1['y_pred_stacking'] == 1 else '✓ BAIXO RISCO'}")

print("\n  Ensemble - Hard Voting:")
print(f"    KNN vota: {'Doente' if resultado1['p_knn'] >= 0.5 else 'Saudável'}")
print(f"    SVM vota: {'Doente' if resultado1['p_svm'] >= 0.5 else 'Saudável'}")
print(f"    Decisão (maioria): {'DOENTE' if resultado1['y_pred_hard'] == 1 else 'SAUDÁVEL'}")

# ============================================================================
print("\n" + "="*80)
print("[PACIENTE 2 - ALTO RISCO ESPERADO]")
print("Dados: Idade 65, múltiplos fatores de risco (HTA, dislipidemia, diabetes, CAD)")
resultado2 = prever_ensemble(X2_scaled, knn, svm, meta_model)

print("\n  Probabilidades Individuais:")
print(f"    KNN (K=29):           P(Doença) = {resultado2['p_knn']:.4f} ({resultado2['p_knn']*100:.2f}%)")
print(f"    SVM (C=0.1, RBF):     P(Doença) = {resultado2['p_svm']:.4f} ({resultado2['p_svm']*100:.2f}%)")

print("\n  Ensemble - Soft Voting Ponderado (RECOMENDADO):")
print(f"    P(Doença) = 0.45 × {resultado2['p_knn']:.4f} + 0.55 × {resultado2['p_svm']:.4f}")
print(f"    P(Doença) = {resultado2['p_ensemble_ponderado']:.4f} ({resultado2['p_ensemble_ponderado']*100:.2f}%)")
print(f"    Decisão:   {'RISCO DE DOENCA' if resultado2['y_pred_ensemble'] == 1 else 'BAIXO RISCO'}")

print("\n  Ensemble - Stacking:")
print(f"    P(Doença) = {resultado2['p_stacking']:.4f} ({resultado2['p_stacking']*100:.2f}%)")
print(f"    Decisão:   {'⚠️  RISCO DE DOENÇA' if resultado2['y_pred_stacking'] == 1 else '✓ BAIXO RISCO'}")

# ============================================================================
print("\n" + "="*80)
print("[PACIENTE 3 - RISCO INTERMEDIÁRIO]")
print("Dados: Idade 55, mulher, alguns fatores de risco moderados")
resultado3 = prever_ensemble(X3_scaled, knn, svm, meta_model)

print("\n  Probabilidades Individuais:")
print(f"    KNN (K=29):           P(Doença) = {resultado3['p_knn']:.4f} ({resultado3['p_knn']*100:.2f}%)")
print(f"    SVM (C=0.1, RBF):     P(Doença) = {resultado3['p_svm']:.4f} ({resultado3['p_svm']*100:.2f}%)")

print("\n  Ensemble - Soft Voting Ponderado (RECOMENDADO):")
print(f"    P(Doença) = 0.45 × {resultado3['p_knn']:.4f} + 0.55 × {resultado3['p_svm']:.4f}")
print(f"    P(Doença) = {resultado3['p_ensemble_ponderado']:.4f} ({resultado3['p_ensemble_ponderado']*100:.2f}%)")
print(f"    Decisão:   {'RISCO DE DOENCA' if resultado3['y_pred_ensemble'] == 1 else 'BAIXO RISCO'}")

print("\n  Ensemble - Stacking:")
print(f"    P(Doença) = {resultado3['p_stacking']:.4f} ({resultado3['p_stacking']*100:.2f}%)")
print(f"    Decisão:   {'⚠️  RISCO DE DOENÇA' if resultado3['y_pred_stacking'] == 1 else '✓ BAIXO RISCO'}")

# ==============================================================================
#  PASSO 5: INTERPRETAÇÃO CLÍNICA
# ==============================================================================
print("\n" + "="*80)
print("[5] INTERPRETAÇÃO CLÍNICA E RECOMENDAÇÕES")
print("="*80)

def gerar_relatorio(resultado, paciente_num):
    """Gera relatório clínico recomendado"""
    p = resultado['p_ensemble_ponderado']
    
    print(f"\nPACIENTE {paciente_num}:")
    print(f"  Probabilidade de Doença: {p*100:.2f}%")
    
    if p < 0.3:
        recomendacao = """
        RISCO BAIXO (< 30%)
        Ações Recomendadas:
        • Acompanhamento de rotina
        • Reteste em 12-24 meses
        • Reforçar prevenção primária (dieta, exercício)
        • Monitorar fatores de risco (PA, colesterol)
        """
    elif p < 0.5:
        recomendacao = """
        RISCO INTERMEDIÁRIO (30-50%)
        Ações Recomendadas:
        • Consulta com cardiologista para avaliação
        • Considerar ECG de repouso (se não realizado)
        • Teste ergométrico ou ecocardiograma
        • Intensificar modificação de estilo de vida
        • Retest ensemble a cada 6 meses
        """
    elif p < 0.7:
        recomendacao = """
        RISCO MODERADO-ALTO (50-70%)
        Ações Recomendadas:
        • Referência urgente a cardiologista
        • Investigação diagnóstica: ECG, ecocardiograma, teste de esforço
        • Considerar trial coronário se sintomas presentes
        • Iniciar terapia medicamentosa preventiva
        • Monitoramento closely
        """
    else:
        recomendacao = """
        RISCO ALTO (> 70%)
        Ações Recomendadas:
        • REFERÊNCIA URGENTE A CARDIOLOGISTA
        • Investigação diagnóstica completa
        • ECG, Troponina (se sintomas agudos)
        • Ecocardiograma urgente
        • Possível cateterismo cardíaco
        • Terapia medicamentosa imediata
        """
    
    print(recomendacao)

gerar_relatorio(resultado1, 1)
gerar_relatorio(resultado2, 2)
gerar_relatorio(resultado3, 3)

# ==============================================================================
#  PASSO 6: RESUMO COMPARATIVO
# ==============================================================================
print("\n" + "="*80)
print("[6] COMPARAÇÃO DE RESULTADOS - SOFT VOTING PONDERADO")
print("="*80)

resultados_df = pd.DataFrame({
    'Paciente': ['Paciente 1\n(Baixo Risco)', 'Paciente 2\n(Alto Risco)', 'Paciente 3\n(Intermediário)'],
    'KNN': [f"{resultado1['p_knn']:.2%}", f"{resultado2['p_knn']:.2%}", f"{resultado3['p_knn']:.2%}"],
    'SVM': [f"{resultado1['p_svm']:.2%}", f"{resultado2['p_svm']:.2%}", f"{resultado3['p_svm']:.2%}"],
    'Ensemble': [f"{resultado1['p_ensemble_ponderado']:.2%}", f"{resultado2['p_ensemble_ponderado']:.2%}", f"{resultado3['p_ensemble_ponderado']:.2%}"],
    'Decisão': [
        'BAIXO RISCO' if resultado1['y_pred_ensemble'] == 0 else '⚠️ RISCO',
        'RISCO' if resultado2['y_pred_ensemble'] == 1 else 'BAIXO RISCO',
        ('RISCO' if resultado3['y_pred_ensemble'] == 1 else 'BAIXO RISCO'),
    ]
})

print("\n" + resultados_df.to_string(index=False))

print("\n" + "="*80)
print("✓ EXEMPLO COMPLETO FINALIZADO")
print("="*80 + "\n")
