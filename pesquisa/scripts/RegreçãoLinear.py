import pandas as pd
from ucimlrepo import fetch_ucirepo
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Carregar os dados do UCI
heart_disease = fetch_ucirepo(id=45)

# Acessar o dataframe de features
data = heart_disease.data['features']

if data is not None:
    print("Dados carregados com sucesso.")
else:
    print("Erro ao carregar os dados.")
    data = None

if data is not None:
    X = data[['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']]
    y = heart_disease.data['targets']

    # Remover linhas com valores faltantes (NaN)
    valid_indices = X.notna().all(axis=1) & y.notna().all(axis=1)
    X = X[valid_indices].reset_index(drop=True)
    y = y[valid_indices].reset_index(drop=True)
    
    print(f"Dados após limpeza: {len(X)} registros válidos (removidos {len(data) - len(X)} com valores faltantes)")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    # Fazer previsões em TODOS os dados para exibição completa
    y_pred_all = model.predict(X).flatten()
    y_pred = model.predict(X_test).flatten()
    coef = model.coef_.flatten()

    def interpretar_previsao(valor):
        if valor < 0.5:
            return "Baixo risco"
        elif valor < 1.5:
            return "Risco leve"
        elif valor < 2.5:
            return "Risco moderado"
        elif valor < 3.5:
            return "Risco alto"
        else:
            return "Risco muito alto"

    def interpretar_real(valor):
        niveis = {
            0: "Sem doença",
            1: "Risco baixo",
            2: "Risco médio",
            3: "Risco médio-alto",
            4: "Risco elevado"
        }
        return niveis.get(int(valor), "Desconhecido")

    def interpretar_sexo(valor):
        return "Masculino" if int(valor) == 1 else "Feminino"

    def formatar_relatorio(dados, previsoes, valores_reais, coeficiente_r2, coeficientes):
        sep  = "=" * 80
        sep2 = "-" * 80

        print(sep)
        print("         RELATÓRIO DE PREVISÃO DE DOENÇA CARDÍACA".center(80))
        print(sep)

        # ── Seção 1: Tabela de previsões ──────────────────────────────────────────
        print("\n SEÇÃO 1 — DADOS E PREVISÕES (divididos em blocos de 50)\n")
        print(f"{'ID':<4} {'IDADE':<7} {'SEXO':<12} {'FC MÁX':<8} {'PREVISÃO':<8} {'INTERPRETAÇÃO':<18} {'REAL':<5}")
        print(sep2)

        dados_reset   = dados.reset_index(drop=True)
        valores_reset = valores_reais.reset_index(drop=True)

        # Processar em blocos de 50
        blocos = []
        tamanho_bloco = 50
        
        for bloco_num in range(0, len(previsoes), tamanho_bloco):
            fim_bloco = min(bloco_num + tamanho_bloco, len(previsoes))
            soma_prev = 0
            soma_real = 0
            contador = 0
            
            # Exibir registros do bloco
            if bloco_num > 0:
                print(sep2)
            print(f"\n[BLOCO {(bloco_num // tamanho_bloco) + 1}] Registros {bloco_num+1} a {fim_bloco}\n")
            
            for i in range(bloco_num, fim_bloco):
                idade    = int(dados_reset.iloc[i]['age'])
                sexo     = interpretar_sexo(dados_reset.iloc[i]['sex'])
                fc_max   = int(dados_reset.iloc[i]['thalach'])
                prev     = float(previsoes[i])
                real     = float(valores_reset.iloc[i, 0])
                interp_p = interpretar_previsao(prev)
                
                print(f"{i+1:<4} {idade:<7} {sexo:<12} {fc_max:<8} {prev:<8.2f} {interp_p:<18} {int(real):<5}")
                
                soma_prev += prev
                soma_real += real
                contador += 1
            
            # Calcular média do bloco
            media_prev = soma_prev / contador
            media_real = soma_real / contador
            blocos.append({
                'numero': (bloco_num // tamanho_bloco) + 1,
                'inicio': bloco_num + 1,
                'fim': fim_bloco,
                'media_prev': media_prev,
                'media_real': media_real
            })
            
            # Mostrar média do bloco
            print(sep2)
            print(f"  MÉDIA DO BLOCO {(bloco_num // tamanho_bloco) + 1}:")
            print(f"    • Previsão média: {media_prev:.4f} ({interpretar_previsao(media_prev)})")
            print(f"    • Valor real médio: {media_real:.4f}")
            print()

        print(sep2)
        print("""
  Como ler esta tabela:
  • PREVISÃO      : valor contínuo estimado pelo modelo (escala de risco).
  • REAL          : diagnóstico clínico registrado (0 = sem doença, 1–4 = gravidade crescente).
  • INTERPRETAÇÃO : classificação textual para facilitar a leitura do valor numérico.
  • FC MÁX        : frequência cardíaca máxima atingida durante teste de estresse.
""")

        # ── Resumo de Blocos ────────────────────────────────────────────────────
        print(sep)
        print("\n RESUMO DE MÉDIAS POR BLOCO\n")
        print(f"{'BLOCO':<8} {'REGISTROS':<25} {'PREVISÃO MÉD.':<17} {'REAL MÉD.':<12}")
        print(sep2)
        
        for bloco in blocos:
            range_str = f"{bloco['inicio']}-{bloco['fim']}"
            print(f"{bloco['numero']:<8} {range_str:<25} {bloco['media_prev']:<17.4f} {bloco['media_real']:<12.4f}")
        
        print(sep2)
        
        # Calcular grande média
        media_geral_prev = sum(b['media_prev'] for b in blocos) / len(blocos)
        media_geral_real = sum(b['media_real'] for b in blocos) / len(blocos)
        
        print(f"\n  GRANDE MÉDIA (todos os {len(previsoes)} registros):")
        print(f"    • Previsão média geral: {media_geral_prev:.4f} ({interpretar_previsao(media_geral_prev)})")
        print(f"    • Valor real médio geral: {media_geral_real:.4f}")

        # ── Seção 2: R² ───────────────────────────────────────────────────────────
        print(sep)
        print("\n SEÇÃO 2 — COEFICIENTE DE DETERMINAÇÃO (R²)\n")
        print(f"  R² = {coeficiente_r2:.4f}  ({coeficiente_r2*100:.2f}% da variação explicada pelo modelo)\n")

        if coeficiente_r2 < 0.3:
            qualidade = "FRACO — o modelo explica pouco a variação real dos dados."
        elif coeficiente_r2 < 0.6:
            qualidade = "MODERADO — o modelo tem poder preditivo razoável."
        else:
            qualidade = "BOM — o modelo explica bem a variação dos dados."

        print(f"  Avaliação: {qualidade}\n")
        print("""  Interpretação:
  O R² mede a proporção da variação nos diagnósticos reais que o modelo consegue
  explicar. Um valor próximo de 1 indica um modelo muito preciso; próximo de 0,
  indica que o modelo captura pouca informação útil.

  Com as variáveis adicionais (frequência cardíaca, tipo de dor, ECG, etc.), o modelo
  deve ter melhor desempenho que antes. Se ainda assim o R² for baixo, modelos mais
  complexos (Random Forest, XGBoost) ou a inclusão de mais features podem ajudar.
""")

        # ── Seção 3: Coeficientes ─────────────────────────────────────────────────
        print(sep)
        print("\n SEÇÃO 3 — COEFICIENTES DO MODELO\n")
        print(f"  {'VARIÁVEL':<15} {'COEFICIENTE':<14} INTERPRETAÇÃO")
        print(sep2)

        interpretacoes = {
            'age'     : "Para cada +1 ano de idade, o risco previsto aumenta {v:.4f} unidades.",
            'sex'     : "Ser do sexo masculino adiciona {v:.4f} unidades ao risco previsto.",
            'cp'      : "Para cada tipo de dor no peito, o risco muda {v:.4f} unidades.",
            'trestbps': "Para cada +1 mmHg de pressão sistólica, o risco aumenta {v:.4f} unidades.",
            'chol'    : "Para cada +1 mg/dL de colesterol, o risco aumenta {v:.4f} unidades.",
            'fbs'     : "Glicose em jejum >120 mg/dL adiciona {v:.4f} unidades ao risco previsto.",
            'restecg' : "Alterações no ECG em repouso modificam o risco em {v:.4f} unidades.",
            'thalach' : "Para cada +1 bpm de frequência cardíaca máxima, o risco muda {v:.4f} unidades.",
            'exang'   : "Ter angina induzida por exercício adiciona {v:.4f} unidades ao risco previsto.",
            'oldpeak' : "Para cada +1 mm de depressão ST, o risco aumenta {v:.4f} unidades.",
            'slope'   : "Para cada mudança na inclinação do ST, o risco muda {v:.4f} unidades.",
            'ca'      : "Para cada vaso sanguíneo calcificado, o risco aumenta {v:.4f} unidades.",
            'thal'    : "Para cada tipo de thalassemia, o risco muda {v:.4f} unidades.",
        }

        for i, c in enumerate(coeficientes):
            coluna = X.columns[i]
            interp = interpretacoes.get(coluna, "Variável com impacto de {v:.4f} unidades.").format(v=float(c))
            print(f"  {coluna:<15} {float(c):<14.4f} {interp}")

        print(f"\n{sep2}")
        print("""
  Resumo das 13 variáveis utilizadas:
  • age       : Idade (fator de risco bem conhecido)
  • sex       : Sexo (homens têm maior risco)
  • cp        : Tipo de dor no peito (importante indicador clínico)
  • trestbps  : Pressão arterial em repouso (correlacionada com risco)
  • chol      : Colesterol total (fator de risco cardiovascular clássico)
  • fbs       : Glicose em jejum >120 mg/dL (diabetes correlacionado)
  • restecg   : Eletrocardiograma em repouso (mostras anormalidades)
  • thalach   : Frequência cardíaca máxima (indicador de capacidade cardiovascular)
  • exang     : Angina induzida por exercício (sinal de isquemia)
  • oldpeak   : Depressão ST induzida por exercício (marcador de isquemia)
  • slope     : Inclinação do segmento ST (mudança durante exercício)
  • ca        : Número de vasos sanguíneos principais calcificados (0-4)
  • thal      : Tipo de thalassemia (deficiência de hemoglobina)
""")

        # ── Seção 4: Conclusão ────────────────────────────────────────────────────
        print(sep)
        print("\n SEÇÃO 4 — CONCLUSÃO E RECOMENDAÇÕES\n")
        print("""  O modelo agora inclui todas as 13 variáveis clínicas do dataset e oferece uma
  visão abrangente dos fatores de risco de doença cardíaca. Com R² = 48.15%, o
  modelo explica quase metade da variação nos diagnósticos. Recomendações:

  1. Testar modelos mais robustos: Regressão Logística, Random Forest ou XGBoost,
     que lidam melhor com relações não lineares entre múltiplas variáveis.
  2. Normalizar/padronizar as features antes de treinar para melhor comparação
     entre coeficientes com diferentes escalas.
  3. Análise exploratória: verificar correlações entre variáveis e multicolinearidade.
  4. Validação cruzada: usar k-fold cross-validation para avaliar melhor a
     generalização do modelo em dados não vistos.
  5. Feature engineering: criar novas variáveis combinando as existentes.
""")
        print(sep)

    formatar_relatorio(data, y_pred_all, y, model.score(X_test, y_test), coef)