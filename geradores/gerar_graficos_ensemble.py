"""
Gera graficos individuais de alta resolucao para o relatorio ensemble FATEC.
"""
import json, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os

plt.rcParams.update({
    'font.family':    'DejaVu Sans',
    'font.size':      13,
    'axes.titlesize': 15,
    'axes.labelsize': 13,
    'legend.fontsize':12,
    'xtick.labelsize':12,
    'ytick.labelsize':12,
    'figure.dpi':     150,
    'savefig.dpi':    200,
    'axes.grid':      True,
    'grid.alpha':     0.35,
})

BASE    = "c:/Users/andre/Documents/TCC project"
OUT_DIR = BASE + "/artigos_relatorios/graficos_ensemble"
os.makedirs(OUT_DIR, exist_ok=True)

with open(BASE + "/artigos_relatorios/ensemble_results.json", encoding="utf-8") as f:
    d = json.load(f)

MODELOS_PT = {
    "KNN_K29":          "KNN (K=29)",
    "SVM_C01_RBF":      "SVM (C=0.1, RBF)",
    "Hard_Voting":      "Hard Voting",
    "Soft_Voting":      "Soft Voting",
    "Soft_Voting_Pond": "Soft Voting\nPonderado",
    "Stacking":         "Stacking",
}
CORES = {
    "KNN (K=29)":           "#e74c3c",
    "SVM (C=0.1, RBF)":     "#e74c3c",
    "Hard Voting":          "#27ae60",
    "Soft Voting":          "#2980b9",
    "Soft Voting\nPonderado":"#2980b9",
    "Stacking":             "#8e44ad",
}

# ── Grafico 1: Acuracia no conjunto de teste ──────────────────────────────────
print("[1] Acuracia no conjunto de teste...")
acc = d["acuracia_teste"]
labels = [MODELOS_PT[k] for k in acc]
vals   = list(acc.values())
cores  = ["#e74c3c", "#e74c3c", "#27ae60", "#2980b9", "#2980b9", "#8e44ad"]

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(labels, vals, color=cores, edgecolor='white', linewidth=1.5, width=0.6)
for bar, v in zip(bars, vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.003,
            f"{v*100:.2f}%", ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_ylim(0.80, 0.96)
ax.set_ylabel("Acuracia no Conjunto de Teste")
ax.set_title("Acuracia por Metodo no Conjunto de Teste (n=60)\n"
             "Vermelho = modelos base; Verde/Azul = ensemble simples; Roxo = stacking")
base_p = mpatches.Patch(color='#e74c3c', label='Modelos base (KNN, SVM)')
ens_p  = mpatches.Patch(color='#2980b9', label='Ensemble Voting')
stk_p  = mpatches.Patch(color='#8e44ad', label='Stacking')
ax.legend(handles=[base_p, ens_p, stk_p], loc='lower right')
plt.tight_layout()
plt.savefig(OUT_DIR + "/g1_acuracia_teste.png", bbox_inches='tight')
plt.close()
print("   -> g1_acuracia_teste.png")

# ── Grafico 2: AUC-ROC comparativo ───────────────────────────────────────────
print("[2] AUC-ROC comparativo...")
auc = d["auc_roc"]
labels2 = [MODELOS_PT[k] for k in auc]
vals2   = list(auc.values())
cores2  = ["#e74c3c", "#e74c3c", "#2980b9", "#2980b9", "#8e44ad"]

fig, ax = plt.subplots(figsize=(12, 6))
bars2 = ax.bar(labels2, vals2, color=cores2, edgecolor='white', linewidth=1.5, width=0.5)
for bar, v in zip(bars2, vals2):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
            f"{v*100:.2f}%", ha='center', va='bottom', fontsize=12, fontweight='bold')
ax.set_ylim(0.93, 0.97)
ax.set_ylabel("AUC-ROC")
ax.set_title("AUC-ROC por Metodo no Conjunto de Teste\n"
             "(maior = melhor capacidade discriminativa)")
ax.legend(handles=[base_p, ens_p, stk_p], loc='lower right')
plt.tight_layout()
plt.savefig(OUT_DIR + "/g2_auc_roc.png", bbox_inches='tight')
plt.close()
print("   -> g2_auc_roc.png")

# ── Grafico 3: Boxplot CV 10-fold ─────────────────────────────────────────────
print("[3] Boxplot validacao cruzada 10-fold...")
cv = d["cv_10fold"]
ordem = ["KNN", "SVM", "Hard", "Soft", "Pond", "Stack"]
labels3 = ["KNN\n(K=29)", "SVM\n(C=0.1)", "Hard\nVoting", "Soft\nVoting",
           "Soft Pond.", "Stacking"]
dados3 = [cv[k]["scores"] for k in ordem]
medias3= [cv[k]["media"] for k in ordem]
stds3  = [cv[k]["std"]   for k in ordem]
cores3 = ["#e74c3c", "#e74c3c", "#27ae60", "#2980b9", "#2980b9", "#8e44ad"]

fig, ax = plt.subplots(figsize=(12, 7))
bp = ax.boxplot(dados3, labels=labels3, patch_artist=True,
                medianprops=dict(color='black', linewidth=2.5), widths=0.5)
for patch, c in zip(bp['boxes'], cores3):
    patch.set_facecolor(c); patch.set_alpha(0.7)
for i, (m, s) in enumerate(zip(medias3, stds3), 1):
    ax.text(i, m + 0.002, f"{m*100:.2f}%\n+-{s*100:.2f}%",
            ha='center', va='bottom', fontsize=10, fontweight='bold')
ax.set_ylim(0.60, 1.02)
ax.set_ylabel("Acuracia por Fold")
ax.set_title("Distribuicao da Acuracia na Validacao Cruzada Estratificada (10-dobras)\n"
             "Media e desvio padrao acima de cada diagrama")
plt.tight_layout()
plt.savefig(OUT_DIR + "/g3_cv_boxplot.png", bbox_inches='tight')
plt.close()
print("   -> g3_cv_boxplot.png")

# ── Grafico 4: Matrizes de confusao 2x2 ──────────────────────────────────────
print("[4] Matrizes de confusao...")
cms = {
    "KNN (K=29)":           np.array(d["matrizes_confusao"]["KNN"]),
    "SVM (C=0.1, RBF)":     np.array(d["matrizes_confusao"]["SVM"]),
    "Soft Voting Ponderado":np.array(d["matrizes_confusao"]["Soft_Voting_Pond"]),
    "Stacking":             np.array(d["matrizes_confusao"]["Stacking"]),
}
cmaps = ["Blues", "Oranges", "Greens", "Purples"]

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle("Matrizes de Confusao — Conjunto de Teste (n=60)",
             fontsize=15, fontweight='bold')
for ax, (titulo, cm), cmap in zip(axes.flat, cms.items(), cmaps):
    tn, fp, fn, tp = cm.ravel()
    prec = tp/(tp+fp) if (tp+fp) > 0 else 0
    rec  = tp/(tp+fn) if (tp+fn) > 0 else 0
    f1   = 2*prec*rec/(prec+rec) if (prec+rec) > 0 else 0
    acc  = (tp+tn)/(tp+tn+fp+fn)
    sns.heatmap(cm, annot=True, fmt='d', cmap=cmap, ax=ax, cbar=False,
                xticklabels=["Saudavel", "Doente"],
                yticklabels=["Saudavel", "Doente"],
                annot_kws={"size": 18, "weight": "bold"})
    ax.set_title(f"{titulo}\nAcc={acc:.4f}  F1={f1:.4f}", fontsize=12)
    ax.set_ylabel("Real"); ax.set_xlabel("Predito")

plt.tight_layout()
plt.savefig(OUT_DIR + "/g4_confusao.png", bbox_inches='tight')
plt.close()
print("   -> g4_confusao.png")

# ── Grafico 5: Precision / Recall / F1 comparativo ───────────────────────────
print("[5] Precision / Recall / F1...")
modelos_cr = ["KNN\n(K=29)", "SVM\n(C=0.1)", "Soft Voting\nPonderado", "Stacking"]

def metricas_da_cm(cm_list):
    cm = np.array(cm_list)
    tn, fp, fn, tp = cm.ravel()
    prec = tp/(tp+fp) if (tp+fp) > 0 else 0
    rec  = tp/(tp+fn) if (tp+fn) > 0 else 0
    f1   = 2*prec*rec/(prec+rec) if (prec+rec) > 0 else 0
    return prec, rec, f1

cms_lista = [d["matrizes_confusao"]["KNN"],
             d["matrizes_confusao"]["SVM"],
             d["matrizes_confusao"]["Soft_Voting_Pond"],
             d["matrizes_confusao"]["Stacking"]]
precs, recs, f1s = zip(*[metricas_da_cm(c) for c in cms_lista])

x = np.arange(len(modelos_cr))
w = 0.25
fig, ax = plt.subplots(figsize=(12, 7))
b1 = ax.bar(x - w, precs, w, label='Precision', color='#3498db', edgecolor='white')
b2 = ax.bar(x,     recs,  w, label='Recall',    color='#2ecc71', edgecolor='white')
b3 = ax.bar(x + w, f1s,   w, label='F1-Score',  color='#e74c3c', edgecolor='white')
for bars in [b1, b2, b3]:
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.003,
                f"{bar.get_height():.3f}", ha='center', va='bottom', fontsize=10)
ax.set_xticks(x); ax.set_xticklabels(modelos_cr)
ax.set_ylim(0.78, 1.01)
ax.set_ylabel("Valor da Metrica")
ax.set_title("Precision, Recall e F1-Score por Metodo\n(classe positiva: Doente)")
ax.legend(loc='lower right')
plt.tight_layout()
plt.savefig(OUT_DIR + "/g5_prec_rec_f1.png", bbox_inches='tight')
plt.close()
print("   -> g5_prec_rec_f1.png")

# ── Grafico 6: Comparativo geral acuracia-AUC ─────────────────────────────────
print("[6] Comparativo geral Acuracia vs AUC-ROC...")
met6 = ["KNN\n(K=29)", "SVM\n(C=0.1)", "Soft Voting\nPonderado", "Stacking"]
acc6 = [d["acuracia_teste"]["KNN_K29"],
        d["acuracia_teste"]["SVM_C01_RBF"],
        d["acuracia_teste"]["Soft_Voting_Pond"],
        d["acuracia_teste"]["Stacking"]]
auc6 = [d["auc_roc"]["KNN_K29"],
        d["auc_roc"]["SVM_C01_RBF"],
        d["auc_roc"]["Soft_Voting_Pond"],
        d["auc_roc"]["Stacking"]]
cv6  = [d["cv_10fold"]["KNN"]["media"],
        d["cv_10fold"]["SVM"]["media"],
        d["cv_10fold"]["Pond"]["media"],
        d["cv_10fold"]["Stack"]["media"]]

x6 = np.arange(len(met6))
w6 = 0.28
fig, ax = plt.subplots(figsize=(12, 7))
b1 = ax.bar(x6 - w6, acc6, w6, label='Acuracia (teste)', color='#2980b9', edgecolor='white')
b2 = ax.bar(x6,      auc6, w6, label='AUC-ROC',         color='#27ae60', edgecolor='white')
b3 = ax.bar(x6 + w6, cv6,  w6, label='Acuracia CV-10',  color='#e67e22', edgecolor='white')
for bars in [b1, b2, b3]:
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.002,
                f"{bar.get_height()*100:.1f}%", ha='center', va='bottom', fontsize=9)
ax.set_xticks(x6); ax.set_xticklabels(met6)
ax.set_ylim(0.78, 1.01)
ax.set_ylabel("Valor da Metrica")
ax.set_title("Resumo Comparativo: Acuracia (Teste), AUC-ROC e Acuracia CV-10\n"
             "por Metodo de Ensemble")
ax.legend(loc='lower right')
plt.tight_layout()
plt.savefig(OUT_DIR + "/g6_comparativo_geral.png", bbox_inches='tight')
plt.close()
print("   -> g6_comparativo_geral.png")

print(f"\n[OK] 6 graficos salvos em: {OUT_DIR}")
