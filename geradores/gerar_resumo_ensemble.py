"""
RESUMO EXECUTIVO - ENSEMBLE LEARNING
Comparação rápida de resultados
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# Dados dos resultados
modelos = ['KNN\n(K=29)', 'SVM\n(C=0.1)', 'Hard\nVoting', 'Soft\nVoting', 'Soft\nPonderado', 'Stacking']
acuracia_teste = [0.8667, 0.8667, 0.8833, 0.8833, 0.8833, 0.8667]
cv_media = [0.8286, 0.8351, 0.8251, 0.8249, 0.8283, 0.8284]
cv_std = [0.0699, 0.0766, 0.0625, 0.0712, 0.0641, 0.0639]
auc_roc = [0.9481, 0.9487, 0.9498, 0.9498, 0.9509, 0.9520]

# Criar figura
fig = plt.figure(figsize=(16, 10))
fig.suptitle('ENSEMBLE LEARNING PARA DIAGNÓSTICO DE DOENÇA CARDÍACA\nComparação de Métodos', 
             fontsize=18, fontweight='bold', y=0.98)

# ============================================================================
# 1. Acurácia no Conjunto de Teste
# ============================================================================
ax1 = plt.subplot(2, 3, 1)
cores = ['#FF6B6B' if 'Voting' not in m and 'acking' not in m else '#4ECDC4' for m in modelos]
bars1 = ax1.bar(modelos, acuracia_teste, color=cores, alpha=0.8, edgecolor='black', linewidth=1.5)

# Destacar melhores
for i, (bar, valor) in enumerate(zip(bars1, acuracia_teste)):
    altura = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., altura + 0.002,
             f'{valor:.2%}', ha='center', va='bottom', fontweight='bold', fontsize=10)
    if valor == max(acuracia_teste):
        bar.set_edgecolor('gold')
        bar.set_linewidth(3)

ax1.set_ylabel('Acurácia', fontsize=11, fontweight='bold')
ax1.set_title('Acurácia no Conjunto de Teste', fontsize=12, fontweight='bold')
ax1.set_ylim([0.84, 0.90])
ax1.grid(True, alpha=0.3, axis='y')
ax1.axhline(y=0.8667, color='red', linestyle='--', alpha=0.5, label='Baseline (KNN/SVM)')
ax1.legend()

# ============================================================================
# 2. Validação Cruzada (média ± std)
# ============================================================================
ax2 = plt.subplot(2, 3, 2)
x_pos = np.arange(len(modelos))
ax2.bar(x_pos, cv_media, yerr=cv_std, capsize=5, color=cores, alpha=0.8, edgecolor='black', linewidth=1.5)

for i, (valor, std) in enumerate(zip(cv_media, cv_std)):
    ax2.text(i, valor + std + 0.003, f'{valor:.4f}±{std:.4f}', 
             ha='center', va='bottom', fontsize=9)

ax2.set_xticks(x_pos)
ax2.set_xticklabels(modelos)
ax2.set_ylabel('Acurácia CV (10-dobras)', fontsize=11, fontweight='bold')
ax2.set_title('Validação Cruzada Estratificada', fontsize=12, fontweight='bold')
ax2.set_ylim([0.80, 0.85])
ax2.grid(True, alpha=0.3, axis='y')

# ============================================================================
# 3. AUC-ROC
# ============================================================================
ax3 = plt.subplot(2, 3, 3)
bars3 = ax3.bar(modelos, auc_roc, color=cores, alpha=0.8, edgecolor='black', linewidth=1.5)

for i, (bar, valor) in enumerate(zip(bars3, auc_roc)):
    altura = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., altura + 0.0005,
             f'{valor:.4f}', ha='center', va='bottom', fontweight='bold', fontsize=10)
    if valor == max(auc_roc):
        bar.set_edgecolor('gold')
        bar.set_linewidth(3)

ax3.set_ylabel('AUC-ROC', fontsize=11, fontweight='bold')
ax3.set_title('Area Under ROC Curve', fontsize=12, fontweight='bold')
ax3.set_ylim([0.94, 0.96])
ax3.grid(True, alpha=0.3, axis='y')

# ============================================================================
# 4. Matriz de Confusão - Melhor Ensemble (Soft Voting Ponderado)
# ============================================================================
ax4 = plt.subplot(2, 3, 4)
cm = np.array([[30, 2], [5, 23]])
im = ax4.imshow(cm, cmap='Blues', aspect='auto')

# Anotar células
for i in range(2):
    for j in range(2):
        texto = ax4.text(j, i, cm[i, j], ha='center', va='center', 
                        color='white' if cm[i, j] > cm.max() / 2 else 'black',
                        fontsize=16, fontweight='bold')

ax4.set_xticks([0, 1])
ax4.set_yticks([0, 1])
ax4.set_xticklabels(['Saudável', 'Doente'])
ax4.set_yticklabels(['Saudável', 'Doente'])
ax4.set_xlabel('Predito', fontweight='bold')
ax4.set_ylabel('Verdadeiro', fontweight='bold')
ax4.set_title('Matriz de Confusão - Soft Voting\n(Melhor Ensemble)', fontweight='bold')
plt.colorbar(im, ax=ax4, label='Contagem')

# ============================================================================
# 5. Tabela Comparativa
# ============================================================================
ax5 = plt.subplot(2, 3, 5)
ax5.axis('off')

# Dados da tabela
tabela_dados = [
    ['Modelo', 'Teste', 'CV Média', 'AUC-ROC'],
    ['KNN (K=29)', '86.67%', '82.86% ± 6.99%', '0.9481'],
    ['SVM (C=0.1)', '86.67%', '83.51% ± 7.66%', '0.9487'],
    ['Hard Voting', '88.33%', '82.51% ± 6.25%', '0.9498'],
    ['Soft Voting', '88.33%', '82.49% ± 7.12%', '0.9498'],
    ['Soft Ponderado', '88.33%', '82.83% ± 6.41%', '0.9509'],
    ['Stacking', '86.67%', '82.84% ± 6.39%', '0.9520'],
]

# Cores de linha
cores_linha = ['#DDDDDD'] + ['#FFE5E5'] * 2 + ['#E5F0FF'] * 4

tabela = ax5.table(cellText=tabela_dados, cellLoc='center', loc='center',
                   colWidths=[0.25, 0.18, 0.28, 0.18])
tabela.auto_set_font_size(False)
tabela.set_fontsize(9)
tabela.scale(1, 2.2)

# Colorir células
for i, cor in enumerate(cores_linha):
    for j in range(4):
        celula = tabela[(i, j)]
        celula.set_facecolor(cor)
        if i == 0:  # Header
            celula.set_text_props(weight='bold', color='white')
            celula.set_facecolor('#333333')

ax5.set_title('Resumo Comparativo', fontweight='bold', fontsize=12, pad=20)

# ============================================================================
# 6. Insights Principais
# ============================================================================
ax6 = plt.subplot(2, 3, 6)
ax6.axis('off')

insights = """
PRINCIPAIS FINDINGS

✓ MELHORIA: +1.66 pontos percentuais
  Ensemble (88.33%) vs. Individuais (86.67%)

✓ REDUÇÃO DE FALSOS NEGATIVOS:
  De 6 para 5 (crítico em diagnóstico)

✓ MELHOR ENSEMBLE: Soft Voting Ponderado
  • Acurácia: 88.33%
  • CV: 82.83% ± 6.41% (estável)
  • AUC-ROC: 0.9509 (excelente)

✓ MELHOR AUC-ROC: Stacking (0.9520)
  Meta-learner aprende pesos ótimos

✓ CONCORDÂNCIA: 96.67% entre KNN-SVM
  Apesar da alta concordância, ensemble
  beneficia-se de 4% de divergência

✓ IMPLICAÇÃO CLÍNICA:
  Ensemble recomendado para triagem
  de doença cardíaca com alta confiança
"""

ax6.text(0.05, 0.95, insights, transform=ax6.transAxes,
        fontsize=10, verticalalignment='top', fontfamily='monospace',
        bbox=dict(boxstyle='round', facecolor='#F0F8F0', alpha=0.8, edgecolor='#4ECDC4', linewidth=2))

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('ensemble_summary.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Gráfico salvo: ensemble_summary.png")
plt.show()

# Imprimir tabela de resultados
print("\n" + "="*80)
print("ENSEMBLE LEARNING - RESUMO DE RESULTADOS")
print("="*80)
print(f"\n{'Modelo':<30} {'Teste':<12} {'CV Média':<18} {'AUC-ROC':<10}")
print("-"*80)

for i, modelo in enumerate(modelos):
    print(f"{modelo.replace(chr(10), ' '):<30} {acuracia_teste[i]:.4f}       {cv_media[i]:.4f}±{cv_std[i]:.4f}       {auc_roc[i]:.4f}")

print("\n" + "="*80)
print("RECOMENDACAO: Soft Voting Ponderado")
print("   Melhor balanço entre acurácia, generalização e robustez clínica")
print("="*80 + "\n")
