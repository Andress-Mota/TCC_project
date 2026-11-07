from ucimlrepo import fetch_ucirepo

heart_disease = fetch_ucirepo(id=45)
X = heart_disease.data.features
y = heart_disease.data.targets

total = len(X)
completos = X.notna().all(axis=1).sum()

print(f"Total de registros no dataset: {total}")
print(f"Registros com dados completos: {completos}")
print(f"Registros com valores faltantes: {total - completos}")
print(f"\nPercentual de dados válidos: {(completos/total)*100:.1f}%")
