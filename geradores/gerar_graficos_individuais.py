"""
Gera os 6 graficos da analise KNN como imagens individuais
de alta resolucao para uso no artigo FATEC.
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import os

# ─── Configuracao visual ───────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family':      'DejaVu Sans',
    'font.size':        13,
    'axes.titlesize':   15,
    'axes.labelsize':   13,
    'legend.fontsize':  12,
    'xtick.labelsize':  12,
    'ytick.labelsize':  12,
    'figure.dpi':       150,
    'savefig.dpi':      200,
    'axes.grid':        True,
    'grid.alpha':       0.35,
})

BASE    = "c:/Users/andre/Documents/TCC project"
OUT_DIR = BASE + "/artigos_relatorios/graficos_knn_individuais"
os.makedirs(OUT_DIR, exist_ok=True)

FOLDS_OPTIONS = [5, 10, 15, 20]
CORES_FOLDS   = {5: '#1f77b4', 10: '#ff7f0e', 15: '#2ca02c', 20: '#d62728'}
MARCADORES    = {5: 'o', 10: 's', 15: '^', 20: 'D'}
FIGW, FIGH    = 12, 7   # inches — grande e legivel

# ─── Carrega dados ─────────────────────────────────────────────────────────────
print("[*] Carregando dados...")
df = pd.read_csv(BASE + "/artigos_relatorios/knn_parameter_analysis_results.csv")
stats = pd.read_csv(BASE + "/artigos_relatorios/knn_parameter_stats_by_k.csv")

# Parseia cv_scores (string -> lista de floats)
def parse_scores(s):
    s = s.strip()
    if s.startswith('['):
        return list(map(float, s.strip('[]').split()))
    return list(map(float, ast.literal_eval(s)))

df['cv_scores_list'] = df['cv_scores'].apply(parse_scores)

# ─── Grafico 1: Acuracia vs K ──────────────────────────────────────────────────
print("[1] Acuracia vs K...")
fig, ax = plt.subplots(figsize=(FIGW, FIGH))
for folds in FOLDS_OPTIONS:
    sub = df[df['folds'] == folds].sort_values('k')
    ax.plot(sub['k'], sub['accuracy_mean'],
            label=f'{folds} dobras',
            color=CORES_FOLDS[folds],
            marker=MARCADORES[folds], markersize=5, linewidth=2.2)
    ax.fill_between(sub['k'],
                    sub['accuracy_mean'] - sub['accuracy_std'],
                    sub['accuracy_mean'] + sub['accuracy_std'],
                    color=CORES_FOLDS[folds], alpha=0.10)

ax.axvline(x=29, color='red', linestyle='--', linewidth=2.0, label='K=29 (selecionado)')
ax.set_xlabel('Valor de K')
ax.set_ylabel('Acuracia Media (Validacao Cruzada)')
ax.set_title('Acuracia Media vs Valor de K\npara 4 Configuracoes de Validacao Cruzada')
ax.legend(loc='lower right')
ax.set_xticks(df['k'].unique()[::2])
plt.tight_layout()
plt.savefig(OUT_DIR + "/g1_acuracia_vs_k.png", bbox_inches='tight')
plt.close()
print("   -> salvo g1_acuracia_vs_k.png")

# ─── Grafico 2: AUC-ROC vs K ──────────────────────────────────────────────────
print("[2] AUC-ROC vs K...")
fig, ax = plt.subplots(figsize=(FIGW, FIGH))
for folds in FOLDS_OPTIONS:
    sub = df[df['folds'] == folds].sort_values('k')
    ax.plot(sub['k'], sub['auc_mean'],
            label=f'{folds} dobras',
            color=CORES_FOLDS[folds],
            marker=MARCADORES[folds], markersize=5, linewidth=2.2)
    ax.fill_between(sub['k'],
                    sub['auc_mean'] - sub['auc_std'],
                    sub['auc_mean'] + sub['auc_std'],
                    color=CORES_FOLDS[folds], alpha=0.10)

ax.axvline(x=29, color='red', linestyle='--', linewidth=2.0, label='K=29 (selecionado)')
ax.set_xlabel('Valor de K')
ax.set_ylabel('AUC-ROC Medio (Validacao Cruzada)')
ax.set_title('AUC-ROC Medio vs Valor de K\npara 4 Configuracoes de Validacao Cruzada')
ax.legend(loc='lower right')
ax.set_xticks(df['k'].unique()[::2])
plt.tight_layout()
plt.savefig(OUT_DIR + "/g2_auc_vs_k.png", bbox_inches='tight')
plt.close()
print("   -> salvo g2_auc_vs_k.png")

# ─── Grafico 3: Estabilidade (desvio padrao) vs K ─────────────────────────────
print("[3] Estabilidade vs K...")
fig, ax = plt.subplots(figsize=(FIGW, FIGH))
for folds in FOLDS_OPTIONS:
    sub = df[df['folds'] == folds].sort_values('k')
    ax.plot(sub['k'], sub['accuracy_std'],
            label=f'{folds} dobras',
            color=CORES_FOLDS[folds],
            marker=MARCADORES[folds], markersize=5, linewidth=2.2)

ax.axvline(x=29, color='red', linestyle='--', linewidth=2.0, label='K=29 (selecionado)')
ax.set_xlabel('Valor de K')
ax.set_ylabel('Desvio Padrao da Acuracia')
ax.set_title('Variabilidade da Acuracia vs Valor de K\n(menor = modelo mais estavel)')
ax.legend(loc='upper left')
ax.set_xticks(df['k'].unique()[::2])
plt.tight_layout()
plt.savefig(OUT_DIR + "/g3_estabilidade_vs_k.png", bbox_inches='tight')
plt.close()
print("   -> salvo g3_estabilidade_vs_k.png")

# ─── Grafico 4: Boxplot K=29 vs outros K ─────────────────────────────────────
print("[4] Boxplot K=29 vs outros...")
k29_scores   = df[df['k'] == 29]['cv_scores_list'].explode().astype(float).dropna().tolist()
outros_scores = df[df['k'] != 29]['cv_scores_list'].explode().astype(float).dropna().tolist()

fig, ax = plt.subplots(figsize=(FIGW * 0.65, FIGH))
bp = ax.boxplot(
    [k29_scores, outros_scores],
    labels=['K=29\n(selecionado)', 'Demais K'],
    patch_artist=True,
    widths=0.5,
    medianprops=dict(color='red', linewidth=2.5),
)
bp['boxes'][0].set_facecolor('#4ECDC4')
bp['boxes'][1].set_facecolor('#95A5A6')
ax.set_ylabel('Acuracia por Fold')
ax.set_title('Distribuicao da Acuracia: K=29 vs Demais Valores de K')
ax.annotate(f'Mediana K=29\n{np.median(k29_scores):.3f}',
            xy=(1, np.median(k29_scores)),
            xytext=(1.3, np.median(k29_scores) + 0.01),
            fontsize=11, color='red',
            arrowprops=dict(arrowstyle='->', color='red'))
plt.tight_layout()
plt.savefig(OUT_DIR + "/g4_boxplot_k29.png", bbox_inches='tight')
plt.close()
print("   -> salvo g4_boxplot_k29.png")

# ─── Grafico 5: Heatmap K x dobras ───────────────────────────────────────────
print("[5] Heatmap K x dobras...")
heatmap_data = df.pivot(index='k', columns='folds', values='accuracy_mean')

fig, ax = plt.subplots(figsize=(FIGW * 0.7, FIGH * 1.5))
sns.heatmap(
    heatmap_data,
    annot=True, fmt='.3f',
    cmap='RdYlGn',
    linewidths=0.4,
    linecolor='white',
    cbar_kws={'label': 'Acuracia Media', 'shrink': 0.8},
    ax=ax,
    annot_kws={'size': 9}
)
# Destaca linha K=29
k_values = list(heatmap_data.index)
if 29 in k_values:
    row_idx = k_values.index(29)
    ax.add_patch(plt.Rectangle((0, row_idx), len(heatmap_data.columns), 1,
                                fill=False, edgecolor='red', lw=3))

ax.set_xlabel('Numero de Dobras (CV)', labelpad=10)
ax.set_ylabel('Valor de K', labelpad=10)
ax.set_title('Heatmap: Acuracia Media por K e Configuracao de CV\n(contorno vermelho = K=29)')
plt.tight_layout()
plt.savefig(OUT_DIR + "/g5_heatmap.png", bbox_inches='tight')
plt.close()
print("   -> salvo g5_heatmap.png")

# ─── Grafico 6: Barplot por faixa de K ───────────────────────────────────────
print("[6] Barplot faixas de K...")
faixas = [
    ('K=1-9\n(Overfitting)',  1,  9,  '#E74C3C'),
    ('K=11-19\n(Transicao)', 11, 19,  '#F39C12'),
    ('K=21-29\n(Equilibrio)',21, 29,  '#27AE60'),
    ('K=31-39\n(Transicao)', 31, 39,  '#3498DB'),
    ('K=41-49\n(Underfitting)',41,49, '#9B59B6'),
]
labels    = [f[0] for f in faixas]
acuracias = [stats[(stats['k'] >= f[1]) & (stats['k'] <= f[2])]['acc_mean'].mean()
             for f in faixas]
cores_bar = [f[3] for f in faixas]

fig, ax = plt.subplots(figsize=(FIGW, FIGH))
bars = ax.bar(labels, acuracias, color=cores_bar, edgecolor='white',
              linewidth=1.5, width=0.55)

# Destaca K=21-29
bars[2].set_edgecolor('red')
bars[2].set_linewidth(3.5)

for bar, val in zip(bars, acuracias):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.001,
            f'{val:.4f}', ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_ylim(0.79, 0.86)
ax.set_ylabel('Acuracia Media')
ax.set_title('Acuracia Media por Faixa de K\n(contorno vermelho = faixa com K=29 selecionado)')
plt.tight_layout()
plt.savefig(OUT_DIR + "/g6_barplot_faixas.png", bbox_inches='tight')
plt.close()
print("   -> salvo g6_barplot_faixas.png")

print(f"\n[OK] 6 graficos salvos em: {OUT_DIR}")
