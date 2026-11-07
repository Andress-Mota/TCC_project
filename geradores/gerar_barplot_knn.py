import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Carregar dados dos resultados
df = pd.read_csv('c:/Users/andre/Documents/TCC project/artigos_relatorios/knn_parameter_stats_by_k.csv')

# Criar gráfico de coluna simples
fig, ax = plt.subplots(figsize=(14, 8))

# Selecionar valores de K para não ficar apertado
k_selection = df[df['k'].isin([1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49])]

# Gráfico de barras para acurácia
x = range(len(k_selection))
bars = ax.bar(x, k_selection['acc_mean'], color='steelblue', alpha=0.8, label='Acurácia Média', width=0.7)

# Adicionar linha de erro
ax.errorbar(x, k_selection['acc_mean'], yerr=k_selection['acc_std_across_folds'], fmt='none', color='black', capsize=5, linewidth=1.5)

# Destacar K=29
k29_idx = list(k_selection['k']).index(29)
bars[k29_idx].set_color('red')
bars[k29_idx].set_alpha(1.0)

# Labels e formatação
ax.set_xlabel('Valor de K', fontsize=14, fontweight='bold')
ax.set_ylabel('Acurácia Média', fontsize=14, fontweight='bold')
ax.set_title('Performance do KNN: Acurácia Média por Valor de K\n(K=29 em destaque)', fontsize=16, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(k_selection['k'].values, fontsize=12)
ax.set_ylim([0.7, 0.88])
ax.grid(axis='y', alpha=0.3)
ax.tick_params(axis='both', labelsize=12)

# Adicionar valor no topo de cada barra
for i, (idx, row) in enumerate(k_selection.iterrows()):
    height = row['acc_mean']
    ax.text(i, height + 0.002, f"{height:.4f}", ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('c:/Users/andre/Documents/TCC project/artigos_relatorios/knn_barplot.png', dpi=300, bbox_inches='tight')
print("Gráfico de coluna salvo: knn_barplot.png")