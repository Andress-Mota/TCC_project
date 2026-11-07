import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar dados
df = pd.read_csv('c:/Users/andre/Documents/TCC project/artigos_relatorios/knn_parameter_stats_by_k.csv')

# Configurar estilo
plt.style.use('default')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Gráfico 1: Acurácia vs K
ax1.errorbar(df['k'], df['acc_mean'], yerr=df['acc_std_across_folds'], fmt='o-', capsize=3)
ax1.set_xlabel('Valor de K')
ax1.set_ylabel('Acurácia Média')
ax1.set_title('Acurácia do KNN por Valor de K')
ax1.grid(True, alpha=0.3)

# Gráfico 2: AUC-ROC vs K
ax2.errorbar(df['k'], df['auc_mean'], yerr=df['auc_std_across_folds'], fmt='s-', color='orange', capsize=3)
ax2.set_xlabel('Valor de K')
ax2.set_ylabel('AUC-ROC Médio')
ax2.set_title('AUC-ROC do KNN por Valor de K')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('c:/Users/andre/Documents/TCC project/artigos_relatorios/knn_detailed_analysis.png', dpi=300, bbox_inches='tight')
print("Gráfico salvo como knn_detailed_analysis.png")