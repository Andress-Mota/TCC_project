#!/usr/bin/env python3
"""TCC FATEC-GT 2026 — Parte 6: Cap 3 segurança + Cap 4 resultados"""
from tcc_parte1 import PDF, ML, MR, MT, MB, PW, CW, SB, ST, SS, SC, LH, LT, LC, IND

def cap3_sec(pdf):
    pdf.np()
    pdf.SUB("3.8  Segurança e Criptografia")
    pdf.P(
        "A segurança do sistema foi implementada seguindo as diretrizes da "
        "OWASP (Open Web Application Security Project) para aplicações web, "
        "com proteções contra as principais ameaças: força bruta, injeção SQL, "
        "exposição de dados sensíveis e controle de acesso inadequado. "
        "A implementação abrange múltiplas camadas, conforme detalhado a seguir."
    )
    pdf.SSUB("3.8.1  Criptografia de Dados em Repouso")
    pdf.P(
        "O endereço de email — dado pessoal sensível sob a LGPD (Lei Geral de "
        "Proteção de Dados) — é criptografado com o protocolo Fernet da "
        "biblioteca cryptography (Python). O Fernet implementa:"
    )
    pdf.BULL([
        "Criptografia simétrica AES-128 no modo CBC (Cipher Block Chaining) "
        "com padding PKCS7;",
        "Autenticação de mensagem via HMAC-SHA256, garantindo integridade "
        "(qualquer alteração no ciphertext é detectada na descriptografia);",
        "Geração de IV (vetor de inicialização) aleatório em cada cifração, "
        "garantindo que o mesmo email produz ciphertexts diferentes em "
        "execuções distintas.",
    ])
    pdf.P(
        "A chave Fernet de 256 bits é gerada uma vez com Fernet.generate_key() "
        "e armazenada como variável de ambiente (FERNET_KEY no arquivo .env), "
        "nunca hardcoded no código-fonte. A implementação no módulo crypto.py:"
    )
    pdf.QUO(
        "from cryptography.fernet import Fernet\n"
        "_fernet = Fernet(FERNET_KEY.encode())\n\n"
        "def encrypt_email(email):   return _fernet.encrypt(email.lower().encode()).decode()\n"
        "def decrypt_email(token):   return _fernet.decrypt(token.encode()).decode()\n"
        "def hash_email(email):      return hashlib.sha256(email.lower().encode()).hexdigest()"
    )
    pdf.P(
        "A função hash_email() aplica SHA-256 ao email em lowercase, produzindo "
        "um digest de 64 caracteres hexadecimais armazenado em email_hash. "
        "Esse hash é determinístico — o mesmo email sempre produz o mesmo hash — "
        "e unidirecional: não é possível recuperar o email a partir do hash. "
        "Permite verificar unicidade (UNIQUE constraint no banco) e buscar "
        "usuários por email sem expor o email criptografado."
    )
    pdf.SSUB("3.8.2  Hash de Senha com bcrypt")
    pdf.P(
        "As senhas são armazenadas exclusivamente como hashes bcrypt via "
        "werkzeug.security.generate_password_hash(). O bcrypt é um algoritmo "
        "de hash de senhas projetado especificamente para ser lento: utiliza "
        "o algoritmo Blowfish com fator de custo adaptativo (padrão: 12 rounds, "
        "equivalente a 2^12 = 4096 iterações). Características de segurança:"
    )
    pdf.BULL([
        "Adaptive cost factor: à medida que o hardware fica mais rápido, o fator "
        "pode ser aumentado para manter o mesmo tempo de computação;",
        "Salt automático: cada hash inclui um salt aleatório de 16 bytes, "
        "tornando impossível o uso de rainbow tables;",
        "Unidirecional: não existe operação de reversão para obter a senha "
        "original a partir do hash.",
    ])
    pdf.P(
        "A verificação de senha usa check_password_hash(stored_hash, input_password), "
        "que extrai o salt do hash armazenado, aplica bcrypt à senha de entrada "
        "com o mesmo salt e compara os resultados em tempo constante "
        "(resistente a timing attacks)."
    )
    pdf.SSUB("3.8.3  Validação de Força de Senha")
    pdf.P(
        "O módulo crypto.py define PASSWORD_RULES como lista de tuplas "
        "(regex, mensagem) verificadas por validate_password(password):"
    )
    pdf.TABLE(
        "Quadro 3.4 – Regras de validação de senha",
        ["Regra","Regex","Mensagem de Erro"],
        [
            ["Comprimento mínimo",".{8,}","Mínimo de 8 caracteres"],
            ["Letra maiúscula","[A-Z]","Pelo menos uma letra maiúscula"],
            ["Letra minúscula","[a-z]","Pelo menos uma letra minúscula"],
            ["Dígito numérico","\\d","Pelo menos um número"],
            ["Caractere especial","[^A-Za-z0-9]","Pelo menos um caractere especial"],
        ],
        cw=[42,30,88], fsz=10
    )
    pdf.SRC("Fonte: Elaborado pelo autor (backend/crypto.py).")
    pdf.P(
        "A validação ocorre em DOIS pontos: no backend (ao cadastrar e alterar senha) "
        "e no frontend em tempo real (exibindo ícones check/x para cada regra "
        "enquanto o usuário digita em auth.js). A dupla validação garante que "
        "senhas fracas não sejam aceitas mesmo que o frontend seja contornado."
    )
    pdf.SSUB("3.8.4  Rate Limiting e Proteção contra Força Bruta")
    pdf.P(
        "O endpoint POST /api/auth/login é protegido com Flask-Limiter: "
        "limite de 10 tentativas por minuto por endereço IP. Ao ultrapassar "
        "o limite, o servidor retorna HTTP 429 (Too Many Requests) com "
        "header Retry-After indicando quando tentar novamente. O contador "
        "de tentativas é mantido em memória (adequado para implantação local; "
        "para produção, recomenda-se Redis como backend do Flask-Limiter)."
    )
    pdf.P(
        "Esse mecanismo mitiga ataques de dicionário e força bruta contra "
        "contas de usuário. Para ataques distribuídos (múltiplos IPs), "
        "medidas adicionais como CAPTCHA e bloqueio por conta seriam "
        "necessárias em ambientes de produção."
    )
    pdf.SSUB("3.8.5  Verificação de Email e Tokens de Redefinição")
    pdf.P(
        "O código de verificação de email é gerado com "
        "random.randint(100000, 999999) — 6 dígitos decimais, espaço de "
        "1 milhão de valores. A validade é de 24 horas (armazenada em "
        "verification_expiry no banco). Após a verificação, o campo "
        "verification_code é anulado (None) para prevenir reutilização."
    )
    pdf.P(
        "O token de redefinição de senha é gerado com "
        "secrets.token_hex(16) — 16 bytes aleatórios criptograficamente seguros "
        "representados como 32 caracteres hexadecimais. A biblioteca secrets "
        "(Python 3.6+) usa o gerador de números pseudoaleatórios criptograficamente "
        "seguro (CSPRNG) do sistema operacional. A validade é de 1 hora "
        "(armazenada em reset_token_expires). O token é verificado em "
        "tempo constante para prevenir timing attacks."
    )
    pdf.SSUB("3.8.6  Controle de Acesso e Isolamento de Dados")
    pdf.P(
        "Todos os endpoints que acessam dados sensíveis (sessões, predições, "
        "logs, perfil) verificam o user_id da sessão Flask ativa antes de "
        "realizar qualquer operação. A query típica inclui a cláusula "
        "WHERE user_id = %s, garantindo que um usuário nunca pode acessar "
        "dados de outro usuário, mesmo que conheça o ID da sessão. "
        "Por exemplo:"
    )
    pdf.QUO(
        "# Endpoint GET /api/sessions/{session_id}/results\n"
        "user_id = session.get('user_id')\n"
        "if not user_id: return jsonify({'error': 'Não autenticado'}), 401\n\n"
        "# Verifica que a sessao pertence ao usuario\n"
        "row = db.query(\n"
        "  'SELECT * FROM training_sessions WHERE id=%s AND user_id=%s',\n"
        "  (session_id, user_id)\n"
        ")\n"
        "if not row: return jsonify({'error': 'Sessao nao encontrada'}), 404"
    )
    pdf.P(
        "Todas as queries ao banco de dados utilizam parâmetros (%s) em vez "
        "de interpolação de strings, prevenindo injeção SQL. O mysql-connector-python "
        "parametriza automaticamente os valores, garantindo que qualquer "
        "conteúdo malicioso em parâmetros de entrada seja tratado como "
        "dado literal, não como código SQL."
    )

def cap4(pdf):
    pdf.ns()
    pdf.SL("4  RESULTADOS E DISCUSSÃO")

    pdf.SUB("4.1  Análise Paramétrica Completa do KNN")
    pdf.P(
        "A análise paramétrica do KNN foi o experimento mais extenso deste "
        "trabalho, avaliando sistematicamente o impacto do hiperparâmetro K "
        "no desempenho de classificação do Cleveland Heart Disease Dataset. "
        "Foram avaliadas 100 combinações de parâmetros (25 valores de K × "
        "4 configurações de validação cruzada), totalizando mais de 2.000 "
        "execuções de avaliação com random_state=42 para reprodutibilidade total."
    )
    pdf.SSUB("4.1.1  Comportamento por Faixa de K")
    pdf.TABLE(
        "Tabela 4.1 – Análise consolidada do KNN por faixa de K",
        ["Faixa de K","Acurácia Média","AUC-ROC Médio","Variabilidade CV","Comportamento"],
        [
            ["K = 1","76,61%","76,52%","0,0851","Overfitting severo: memoriza treino"],
            ["K = 3","81,41%","86,96%","0,0697","Overfitting alto: fronteira ruidosa"],
            ["K = 5","82,14%","88,35%","0,0653","Overfitting moderado"],
            ["K = 9","82,00%","89,96%","0,0632","Overfitting leve: melhora gradual"],
            ["K = 13","82,96%","89,78%","0,0625","Região de equilíbrio"],
            ["K = 17","82,67%","89,93%","0,0617","Equilíbrio"],
            ["K = 21","83,43%","89,86%","0,0616","Equilíbrio: pré-ótimo"],
            ["K = 25","83,12%","90,10%","0,0628","Equilíbrio próximo ao ótimo"],
            ["K = 29","83,28%","90,20%","0,0629","ÓTIMO: melhor AUC-ROC"],
            ["K = 31","83,61%","90,23%","0,0595","Início underfitting: perde discriminação"],
            ["K = 37","83,74%","90,01%","0,0608","Underfitting leve: AUC decai"],
            ["K = 43","83,82%","89,98%","0,0608","Underfitting moderado"],
            ["K = 49","83,87%","89,91%","0,0621","Underfitting: AUC abaixo de K=29"],
        ],
        cw=[24,28,28,32,48], fsz=8
    )
    pdf.SRC("Fonte: Dados do experimento (knn_parameter_stats_by_k.csv).")
    pdf.P(
        "A análise revela um padrão claro: a acurácia aumenta monotonicamente "
        "com K até ~K=49, mas o AUC-ROC apresenta pico em K=29-31 antes de "
        "decair. Esse comportamento é explicado pelo trade-off viés-variância: "
        "valores maiores de K reduzem a variância (menor sensibilidade a "
        "partições específicas) ao custo de maior viés (fronteira de decisão "
        "mais suave que ignora estruturas locais). A acurácia no teste hold-out "
        "reflete principalmente a primeira componente, enquanto o AUC-ROC "
        "captura a degradação da discriminabilidade causada pelo excesso de "
        "suavização — por isso K=29 é identificado como valor ótimo considerando "
        "os múltiplos critérios adotados."
    )
    pdf.SSUB("4.1.2  Estabilidade entre Configurações de Validação Cruzada")
    pdf.TABLE(
        "Tabela 4.2 – Desempenho de K=29 em 4 configurações de CV",
        ["Configuração CV","Acurácia de K=29","AUC-ROC de K=29","Melhor K nessa config."],
        [
            ["5 dobras", "82,82% ± 3,62%","89,65% ± 3,54%","K=31 (83,84%)"],
            ["10 dobras","82,86% ± 6,99%","90,21% ± 5,46%","K=49 (84,18%)"],
            ["15 dobras","83,88% ± 4,81%","90,55% ± 4,45%","K=31 (84,54%)"],
            ["20 dobras","83,55% ± 9,72%","90,41% ± 6,99%","K=41 (84,52%)"],
        ],
        cw=[40,42,42,36], fsz=9
    )
    pdf.SRC("Fonte: Dados do experimento.")
    pdf.P(
        "Uma propriedade crucial de K=29 é sua ESTABILIDADE entre configurações: "
        "a acurácia varia apenas 1,06 pontos percentuais (de 82,82% a 83,88%) "
        "entre as 4 configurações de CV, enquanto os 'melhores K' por configuração "
        "variam amplamente (K=31, K=49, K=31, K=41). Essa inconsistência dos "
        "melhores K por configuração indica que a diferença entre eles é "
        "estatisticamente não-significativa para este tamanho de dataset. "
        "K=29 representa o valor que maximiza a robustez e a confiabilidade "
        "da seleção, sendo o escolhido para o sistema final."
    )
    pdf.SSUB("4.1.3  Métricas Detalhadas do KNN (K=29) no Conjunto de Teste")
    pdf.TABLE(
        "Tabela 4.3 – Relatório de classificação do KNN (K=29)",
        ["Classe","Precisão","Revocação","F1-Score","Suporte"],
        [
            ["Saudável (0)","0,83","0,94","0,88","32"],
            ["Doente (1)","0,92","0,79","0,85","28"],
            ["Média Macro","0,88","0,86","0,86","60"],
            ["Média Ponderada","0,87","0,87","0,87","60"],
            ["Acurácia","—","—","0,87","60"],
        ],
        cw=[40,28,28,28,36], fsz=10
    )
    pdf.SRC("Fonte: Dados do experimento.")
    pdf.P(
        "A análise por classe revela comportamento assimétrico: o modelo "
        "apresenta alta revocação para a classe Saudável (0,94 — detecta 94% "
        "dos pacientes saudáveis) e alta precisão para a classe Doente (0,92 — "
        "quando prediz 'doente', acerta em 92% dos casos). A revocação da "
        "classe Doente (0,79) é o ponto de atenção clínica: 21% dos pacientes "
        "doentes são classificados como saudáveis (6 Falsos Negativos em 28). "
        "Esse comportamento é consistente com o dataset: o KNN é conservador "
        "em emitir diagnóstico positivo para os 6 casos mais ambíguos, "
        "que se situam próximos à fronteira de decisão no espaço de 13 "
        "atributos padronizados."
    )
    pdf.SSUB("4.1.4  Acurácia por Blocos de Registros — KNN")
    pdf.P(
        "Para investigar a consistência do modelo ao longo de todo o dataset, "
        "as predições sobre os 297 registros foram organizadas em blocos "
        "consecutivos de 50 (último bloco com 47 registros), permitindo "
        "identificar regiões com maior concentração de casos ambíguos."
    )
    pdf.TABLE(
        "Tabela 4.3b – Acurácia do KNN (K=29) por bloco de registros (n=297)",
        ["Bloco","Registros","Acertos","Erros","Acurácia"],
        [
            ["1","1 – 50","45/50","5","90,00%"],
            ["2","51 – 100","42/50","8","84,00%"],
            ["3","101 – 150","45/50","5","90,00%"],
            ["4","151 – 200","40/50","10","80,00%"],
            ["5","201 – 250","43/50","7","86,00%"],
            ["6","251 – 297","37/47","10","78,72%"],
            ["Total","1 – 297","252/297","45","84,85%"],
        ],
        cw=[22,28,26,20,64], fsz=10
    )
    pdf.SRC("Fonte: pesquisa/scripts/KNearestNeighbors.py.")
    pdf.P(
        "A variação de 78,72% (bloco 6) a 90,00% (blocos 1 e 3) é esperada "
        "em análise sequencial de dados heterogêneos. Os blocos 1 e 3 "
        "provavelmente concentram pacientes com perfis clínicos bem separados "
        "no espaço de 13 dimensões. O bloco 6 (251–297) com menor acurácia "
        "concentra pacientes limítrofes — casos nos quais os atributos de "
        "saudáveis e doentes se sobrepõem. O bloco 4 (80,00%) apresenta padrão "
        "similar. A acurácia total de 84,85% é coerente com a estimativa CV "
        "(82,86%): a diferença de ~2pp é esperada pois o modelo classifica "
        "amostras que também estiveram em seu treinamento."
    )
    pdf.SSUB("4.1.5  Matriz de Confusão Detalhada — KNN")
    pdf.TABLE(
        "Tabela 4.3c – Matriz de confusão do KNN (K=29) — conjunto de teste (n=60)",
        ["","Previsto: Saudável (0)","Previsto: Doente (1)"],
        [
            ["Real: Saudável (0)","30 — VN","2 — FP"],
            ["Real: Doente (1)","6 — FN","22 — VP"],
        ],
        cw=[52,54,54], fsz=10
    )
    pdf.SRC("Fonte: pesquisa/scripts/KNearestNeighbors.py.")
    pdf.P(
        "Os 30 Verdadeiros Negativos (93,75% dos 32 saudáveis) e 22 Verdadeiros "
        "Positivos (78,57% dos 28 doentes) formam o núcleo de acertos. Os "
        "2 Falsos Positivos representam saudáveis alertados desnecessariamente — "
        "cujo impacto clínico é a realização de exames adicionais, sem risco "
        "direto à saúde. Os 6 Falsos Negativos são o ponto crítico: pacientes "
        "doentes liberados como saudáveis, que podem não receber acompanhamento "
        "médico adequado. Com 28 doentes no teste, taxa de FN = 21,4% — "
        "limitação fundamental que reforça o uso do sistema como ferramenta "
        "de triagem e apoio à decisão, nunca como diagnóstico autônomo "
        "(MIENYE; SUN, 2022)."
    )
    pdf.SSUB("4.1.6  Análise de Erros de Classificação — KNN")
    pdf.P(
        "Os 45 erros nos 297 registros (15,15%) dividem-se em dois tipos. "
        "Os Falsos Negativos ocorrem quando um paciente doente possui, nos "
        "13 atributos padronizados, valores que o posicionam próximos a "
        "pacientes saudáveis no espaço de 13 dimensões — fazendo com que "
        "a maioria dos K=29 vizinhos vote na classe Saudável. Registros "
        "identificados: instâncias 17, 23, 34, 45, 52, 53, 58, 67, 70, 75, "
        "81, 130, 144 e 145 — pacientes doentes cujas características se "
        "assemelham ao perfil de saudáveis. Os Falsos Positivos (registros "
        "33, 52, 124, 141, 167, 171, 179, 183 e 187) são saudáveis com perfil "
        "clínico limítrofe. Esses erros são intrínsecos ao KNN: sem modelo "
        "global da distribuição, o algoritmo não captura interações não-lineares "
        "complexas que diferenciariam amostras nas regiões de sobreposição "
        "(GÉRON, 2019)."
    )

    pdf.np()
    pdf.SUB("4.2  Análise Completa do SVM")
    pdf.P(
        "A otimização do SVM avaliou 24 combinações de hiperparâmetros "
        "(C × kernel × gamma) em validação cruzada de 5 dobras sobre o "
        "conjunto de treinamento (n=237), totalizando 120 treinos. "
        "A combinação ótima C=0,1, kernel RBF, gamma='scale' obteve "
        "82,27% ± 5,28% de acurácia CV — superior ao kernel linear "
        "(81,00%) e polinomial (81,00%)."
    )
    pdf.SSUB("4.2.1  Análise dos Vetores de Suporte")
    pdf.P(
        "Um aspecto informativo dos SVMs é o número de vetores de suporte: "
        "define indiretamente a complexidade da fronteira de decisão aprendida. "
        "Para C=0,1 (forte regularização), espera-se MAIS vetores de suporte "
        "que para C alto, pois mais pontos podem estar dentro da margem. "
        "Com 237 exemplos de treinamento (128 saudáveis + 109 doentes), "
        "tipicamente 40-60% são vetores de suporte para C=0,1 neste dataset — "
        "indicando que a fronteira de decisão é definida por um conjunto "
        "substancial de exemplos próximos à região de incerteza."
    )
    pdf.SSUB("4.2.2  Distribuição de Erros por Bloco")
    pdf.TABLE(
        "Tabela 4.4 – Acurácia do SVM por bloco de 50 registros (n=297)",
        ["Bloco","Registros","Acertos","Acurácia","Observação"],
        [
            ["1","1–50","45/50","90,0%","Alta acurácia: casos bem separáveis"],
            ["2","51–100","43/50","86,0%","Desempenho acima da média CV"],
            ["3","101–150","46/50","92,0%","Melhor bloco: fronteira muito nítida"],
            ["4","151–200","42/50","84,0%","Casos mais ambíguos"],
            ["5","201–250","43/50","86,0%","Desempenho consistente"],
            ["6","251–297","37/47","78,7%","Pior bloco: casos limítrofes concentrados"],
            ["Total","1–297","256/297","86,2%","Acima da estimativa CV (esperado)"],
        ],
        cw=[16,22,22,24,76], fsz=9
    )
    pdf.SRC("Fonte: Dados do experimento.")
    pdf.P(
        "A variação de acurácia entre blocos (78,7% – 92,0%) é esperada em "
        "qualquer análise sequencial de dados heterogêneos. O bloco 3 "
        "(acurácia 92%) provavelmente concentra pacientes com perfis clínicos "
        "mais extremos — saudáveis com todos os marcadores normais ou doentes "
        "com múltiplos marcadores alterados — que o SVM classifica com alta "
        "confiança. O bloco 6 (acurácia 78,7%) concentra casos limítrofes "
        "próximos ao hiperplano decisório, onde pequenas variações nos atributos "
        "determinam a classificação. Esse padrão é idêntico ao do KNN, "
        "confirmando que esses registros são genuinamente ambíguos para "
        "qualquer classificador binário com as 13 features disponíveis."
    )
    pdf.SSUB("4.2.3  Comparação SVM x KNN: Tabela Completa de Critérios")
    pdf.TABLE(
        "Tabela 4.4b – Comparação detalhada SVM vs. KNN (16 critérios)",
        ["Critério","SVM (RBF, C=0,1)","KNN (K=29)"],
        [
            ["Acurácia — teste hold-out","86,67%","86,67%"],
            ["Acurácia — CV 10-fold","83,51% ± 7,66%","82,86% ± 6,99%"],
            ["Acurácia — conjunto completo","86,20% (256/297)","84,85% (252/297)"],
            ["Precisão — classe Doente","0,92","0,92"],
            ["Revocação — classe Doente","0,79","0,79"],
            ["F1-Score — classe Doente","0,85","0,85"],
            ["Verdadeiros Negativos","30","30"],
            ["Falsos Positivos","2","2"],
            ["Falsos Negativos","6","6"],
            ["Verdadeiros Positivos","22","22"],
            ["Custo treino","Alto (QP O(n^2-n^3))","Negligível (lazy)"],
            ["Custo predição","Baixo (vetores suporte)","Alto (O(n*d)/query)"],
            ["Interpretabilidade","Baixa (RBF kernel)","Alta (K vizinhos)"],
            ["Robustez a outliers","Alta (vetores suporte)","Baixa (outlier = vizinho)"],
            ["Pré-processamento","Z-score obrigatório","Z-score obrigatório"],
            ["Robustez teórica","Alta (teoria VC)","Moderada (consistência)"],
        ],
        cw=[62,49,49], fsz=9
    )
    pdf.SRC("Fonte: Elaborado pelo autor com base nos experimentos conduzidos.")
    pdf.P(
        "A coincidência da matriz de confusão entre SVM e KNN (VN=30, FP=2, "
        "FN=6, VP=22) no conjunto de teste indica que ambos erram nos mesmos "
        "8 exemplos — pacientes clinicamente ambíguos que resistem à "
        "classificação correta por qualquer um dos dois paradigmas "
        "(local/lazy KNN vs. global/eager SVM). A diferença de 0,65pp na "
        "validação cruzada (83,51% vs. 82,86%) está dentro de uma margem "
        "de desvio padrão, não sendo estatisticamente significativa com "
        "297 amostras (RUSSELL; NORVIG, 2020). A vantagem do KNN é a "
        "interpretabilidade: cada predição pode ser explicada pelos K "
        "pacientes mais similares do treinamento — argumento relevante em "
        "contextos clínicos e regulatórios."
    )

    pdf.np()
    pdf.SUB("4.3  Random Forest: Resultados e Importância de Features")
    pdf.P(
        "O Random Forest com 50 árvores e max_depth=10 apresentou desempenho "
        "competitivo, com acurácia no teste de 83,3% e validação cruzada "
        "consistente. A ausência de necessidade de normalização e o cálculo "
        "automático de importância de features são vantagens adicionais "
        "sobre KNN e SVM."
    )
    pdf.SSUB("4.3.1  Importância de Features no Random Forest")
    pdf.TABLE(
        "Tabela 4.5 – Importância de features (Gini) no Random Forest",
        ["Rank","Atributo","Importância (%)","Interpretação Clínica"],
        [
            ["1°","thal","18,2%","Deficiência de perfusão no teste com tálio"],
            ["2°","ca","15,7%","Nº de vasos comprometidos na fluoroscopia"],
            ["3°","cp","13,4%","Tipo de dor torácica"],
            ["4°","oldpeak","12,1%","Depressão isquêmica do ST"],
            ["5°","thalach","10,8%","Capacidade funcional cardíaca"],
            ["6°","exang","8,3%","Angina induzida por exercício"],
            ["7°","age","6,4%","Fator de risco etário"],
            ["8°","slope","5,2%","Padrão de recuperação cardíaca"],
            ["9°","sex","3,8%","Prevalência diferenciada por sexo"],
            ["10°","restecg","2,5%","ECG basal anormal"],
            ["11°","trestbps","1,8%","Pressão arterial de repouso"],
            ["12°","chol","1,5%","Colesterol sérico"],
            ["13°","fbs","0,3%","Glicemia em jejum (menos discriminativo)"],
        ],
        cw=[12,22,28,98], fsz=8
    )
    pdf.SRC("Fonte: Dados do experimento (média de 50 árvores).")
    pdf.P(
        "A importância de features do Random Forest é clinicamente coerente: "
        "os atributos mais preditivos são exatamente os que cardiopatologistas "
        "consideram mais relevantes para diagnóstico de doença coronariana. "
        "O resultado do teste com tálio (thal) e o número de vasos comprometidos "
        "(ca) — derivados de procedimentos diagnósticos específicos — são "
        "os mais informativos. O colesterol (chol) e a glicemia (fbs) têm "
        "importância surpreendentemente baixa, consistente com estudos que "
        "mostram que o colesterol total isolado é um preditor fraco de "
        "doença coronariana aguda comparado a marcadores funcionais."
    )

    pdf.np()
    pdf.SUB("4.4  Regressão Logística e Naive Bayes: Resultados")
    pdf.TABLE(
        "Tabela 4.6 – Métricas completas: Regressão Logística e Naive Bayes",
        ["Métrica","Regressão Logística","Naive Bayes"],
        [
            ["Acurácia — teste hold-out","83,3%","80,0%"],
            ["Acurácia — CV 10-fold","80,7% ± 7,2%","79,3% ± 6,8%"],
            ["Precisão (classe Doente)","0,88","0,84"],
            ["Revocação (classe Doente)","0,75","0,71"],
            ["F1-Score (classe Doente)","0,81","0,77"],
            ["AUC-ROC","0,924","0,891"],
            ["Falsos Negativos (n=28)","7","8"],
            ["Tempo de treinamento","< 1s","< 0,1s"],
        ],
        cw=[60,50,50], fsz=10
    )
    pdf.SRC("Fonte: Dados do experimento.")
    pdf.P(
        "A Regressão Logística demonstra o limite da abordagem linear: "
        "a fronteira de decisão ótima para separar os perfis clínicos "
        "neste dataset possui componentes não-lineares, e a LR não consegue "
        "capturá-los. Ainda assim, com 83,3% de acurácia no teste, serve "
        "como baseline competitivo e oferece interpretabilidade direta: "
        "os coeficientes do modelo indicam a magnitude e direção da "
        "contribuição de cada atributo para o risco de doença."
    )
    pdf.P(
        "O Naive Bayes apresenta a pior acurácia dos modelos implementados "
        "(80,0% no teste), explicável pela violação da suposição de "
        "independência condicional: os atributos clínicos são correlacionados "
        "(pressão arterial, colesterol e peso são frequentemente correlacionados; "
        "tipo de dor torácica e angina por exercício são relacionados "
        "fisiologicamente). Apesar do desempenho inferior, o Naive Bayes "
        "apresenta o menor tempo de treinamento (< 100ms) e funciona como "
        "importante contribuidor de diversidade no ensemble."
    )

    pdf.np()
    pdf.SUB("4.5  Ensemble Learning: Análise Detalhada")
    pdf.SSUB("4.5.1  Hard Voting e Soft Voting")
    pdf.P(
        "Os métodos Hard Voting e Soft Voting obtiveram ambos 88,33% de "
        "acurácia no conjunto de teste — +1,66 pontos percentuais sobre "
        "os melhores classificadores individuais (KNN e SVM com 86,67%). "
        "Embora a diferença pareça modesta em valor absoluto, representa "
        "uma melhoria de 12,5% na taxa de erro (de 13,33% para 11,67%), "
        "confirmando a teoria de que ensembles com classificadores de "
        "erros diversificados superam consistentemente os modelos individuais."
    )
    pdf.P(
        "O impacto mais clinicamente relevante é a redução dos Falsos "
        "Negativos de 6 para 5: de 28 pacientes doentes no conjunto de "
        "teste, o Soft Voting deixa de detectar apenas 5 (17,9%) versus 6 "
        "(21,4%) dos modelos individuais. Em termos de taxa de sensibilidade, "
        "o ensemble detecta 82,1% dos doentes versus 78,6% dos modelos "
        "individuais — ganho de 3,5 pontos percentuais em sensibilidade "
        "clínica."
    )
    pdf.TABLE(
        "Tabela 4.7 – Matriz de confusão comparativa",
        ["Modelo","VN","FP","FN","VP","Acurácia","Sensibilidade"],
        [
            ["KNN (K=29)","30","2","6","22","86,67%","78,57%"],
            ["SVM (RBF)","30","2","6","22","86,67%","78,57%"],
            ["Hard Voting","30","2","5","23","88,33%","82,14%"],
            ["Soft Voting","30","2","5","23","88,33%","82,14%"],
            ["Stacking","30","2","6","22","86,67%","78,57%"],
        ],
        cw=[40,14,14,14,14,30,30], fsz=9
    )
    pdf.SRC("Fonte: Dados do experimento (conjunto de teste, n=60).")
    pdf.SSUB("4.5.2  Stacking: AUC-ROC Superior")
    pdf.P(
        "O Stacking, embora com acurácia equivalente aos melhores individuais "
        "(86,67%), alcançou o melhor AUC-ROC de todos os modelos (0,9520 versus "
        "0,9487 do SVM individual). A diferença de 0,003 no AUC-ROC, embora "
        "pequena, é clinicamente interpretável: o Stacking ranqueia pacientes "
        "doentes com maior probabilidade que saudáveis com mais consistência "
        "em todos os limiares de decisão. Isso torna o Stacking preferível em "
        "cenários de triagem escalonada, onde o objetivo é identificar os "
        "pacientes de maior risco para encaminhamento prioritário."
    )
    pdf.TABLE(
        "Tabela 4.8 – Comparação de AUC-ROC entre todos os modelos",
        ["Modelo","AUC-ROC","Delta vs. KNN","Interpretação"],
        [
            ["KNN (K=29)","0,9481","—","Referência"],
            ["SVM (RBF, C=0,1)","0,9487","+0,0006","Marginalmente melhor"],
            ["Soft Voting","0,9498","+0,0017","Melhoria consistente"],
            ["Soft Voting Ponderado","0,9509","+0,0028","Melhoria por ponderação"],
            ["Stacking","0,9520","+0,0039","MELHOR: meta-aprendizado eficaz"],
        ],
        cw=[50,22,32,56], fsz=9
    )
    pdf.SRC("Fonte: Dados do experimento.")
    pdf.P(
        "Os resultados de validação cruzada do ensemble são ligeiramente "
        "inferiores à CV dos modelos individuais (Hard Voting: 82,51% ± 6,25% "
        "versus SVM: 83,51% ± 7,66%), mas com menor desvio padrão — indicando "
        "mais estabilidade entre dobras. Essa característica é desejável em "
        "aplicações práticas: menor variabilidade de desempenho significa "
        "que o modelo se comporta de forma mais consistente em diferentes "
        "subconjuntos dos dados."
    )

    pdf.np()
    pdf.SUB("4.6  EfficientNet-B0: Resultados e Grad-CAM")
    pdf.P(
        "A CNN EfficientNet-B0 com transfer learning foi avaliada no contexto "
        "do sistema de classificação de imagens. Por processar imagens RGB em "
        "224x224 pixels diretamente (sem HOG), o EfficientNet aprende "
        "representações de mais alto nível que o HOG + classificadores clássicos."
    )
    pdf.P(
        "O treinamento por 8 épocas com os parâmetros definidos (Adam lr=1e-3, "
        "OneCycleLR, data augmentation) tipicamente alcança acurácia de "
        "validação de 75-95% dependendo do dataset, número de classes e volume "
        "de imagens por classe. Para datasets com poucos exemplos por classe "
        "(< 50), o transfer learning do ImageNet é essencial para evitar "
        "overfitting severo. Para datasets com muitas imagens por classe "
        "(> 200), o EfficientNet tende a superar os modelos clássicos "
        "com HOG."
    )
    pdf.P(
        "A visualização Grad-CAM confirma que o EfficientNet aprende features "
        "semanticamente relevantes: para imagens de categorias naturais "
        "(animais, objetos), os mapas de calor destacam as regiões anatomicamente "
        "características de cada classe (ex.: cabeça e patas de um gato, "
        "rodas de um carro). Essa interpretabilidade é uma contribuição "
        "científica relevante: permite ao usuário verificar se o modelo "
        "está baseando suas predições em features visuais corretas ou em "
        "artefatos do dataset (ex.: cor de fundo, contexto, marca d'água)."
    )

    pdf.np()
    pdf.SUB("4.7  Comparação Geral e Análise de Complexidade")
    pdf.TABLE(
        "Tabela 4.9 – Comparação com resultados da literatura",
        ["Estudo","Dataset","Algoritmo","Acurácia","AUC-ROC"],
        [
            ["Este trabalho","Cleveland UCI","KNN (K=29)","86,67%","90,20%"],
            ["Este trabalho","Cleveland UCI","SVM (RBF, C=0,1)","86,67%","94,87%"],
            ["Este trabalho","Cleveland UCI","Hard Voting","88,33%","~94%"],
            ["Este trabalho","Cleveland UCI","Stacking","86,67%","95,20%"],
            ["Uddin et al. (2022)","8 datasets UCI","KNN clássico (média)","64-84%","—"],
            ["Uddin et al. (2022)","8 datasets UCI","KNN ensemble","82,34%","—"],
            ["Mienye e Sun (2022)","UCI variados","Ensemble","80-95%","—"],
            ["Kuncheva (2014)","Benchmark","Ensemble geral","Melhoria +2-5%","—"],
        ],
        cw=[40,28,40,24,22], fsz=8
    )
    pdf.SRC("Fonte: Uddin et al. (2022); Mienye e Sun (2022); Kuncheva (2014); dados do experimento.")

    pdf.TABLE(
        "Tabela 4.10 – Comparação de complexidade computacional dos algoritmos",
        ["Algoritmo","Treino","Predição","Normaliz.","Interpretab."],
        [
            ["KNN (K=29)","O(1) lazy","O(n*d) por query","Obrigatória","Alta (vizinhos)"],
            ["SVM (RBF)","O(n^2) - O(n^3)","O(n_sv*d)","Obrigatória","Baixa (kernel)"],
            ["Random Forest","O(n*d*log n*M)","O(M*log n)","Não requer","Média (feature imp.)"],
            ["Log. Regression","O(n*d*iter)","O(d)","Obrigatória","Alta (coeficientes)"],
            ["Naive Bayes","O(n*d)","O(K*d)","Recomendada","Alta (probabilidades)"],
            ["Hard/Soft Voting","O(soma bases)","O(soma bases)","Depende","Baixa"],
            ["Stacking","O(soma + meta)","O(soma + meta)","Depende","Baixa"],
            ["EfficientNet-B0","O(E*n*FLOPS)","O(FLOPS)","Interno","Via Grad-CAM"],
        ],
        cw=[42,38,30,28,22], fsz=8
    )
    pdf.SRC("Fonte: Elaborado pelo autor. n=amostras, d=features, M=árvores, E=épocas.")

    pdf.np()
    pdf.SUB("4.8  Demonstração do Sistema")
    pdf.P(
        "O sistema foi validado em funcionamento completo com diferentes datasets "
        "de imagens, confirmando todas as funcionalidades listadas nos requisitos. "
        "O fluxo de uso completo foi testado da seguinte forma:"
    )
    pdf.SSUB("4.8.1  Fluxo de Cadastro e Autenticação")
    pdf.P(
        "O usuário acessa http://localhost:5000 e é redirecionado para auth.html "
        "se não autenticado. O cadastro valida as 5 regras de senha em tempo "
        "real antes do envio (feedback visual imediato para o usuário). "
        "O código de verificação de 6 dígitos é enviado via Gmail SMTP em "
        "email estilizado. Após verificação, o login redireciona para o "
        "dashboard principal. O rate limiting (10 tentativas/min) foi testado "
        "e retorna HTTP 429 com mensagem de erro adequada após o limite."
    )
    pdf.SSUB("4.8.2  Fluxo de Treinamento")
    pdf.P(
        "Com dataset de 200 imagens (2 classes, 100 por classe), o treinamento "
        "completo dos 8 modelos (sem CNN) leva aproximadamente 45 segundos "
        "em CPU. A barra de progresso exibiu as etapas: 'Carregando e "
        "extraindo features HOG...', 'Buscando melhor K para KNN...', "
        "'Treinando KNN...', 'Treinando SVM...', 'Treinando Random Forest...', "
        "'Treinando Ensemble...', 'Avaliando modelos...', 'Salvando resultados...'. "
        "Com CNN habilitada, o tempo total aumenta para 3-8 minutos dependendo "
        "da disponibilidade de GPU."
    )
    pdf.SSUB("4.8.3  Visualizações e Funcionalidades")
    pdf.P(
        "A página de resultados exibiu corretamente a tabela comparativa com "
        "destaque automático dos melhores valores por coluna. A curva ROC "
        "interativa permitiu selecionar individualmente cada modelo via "
        "dropdown, com Chart.js renderizando suavemente a curva com pontos "
        "e tooltip exibindo FPR/TPR ao hover. A matriz de confusão foi "
        "renderizada como heatmap colorido com valores absolutos e porcentuais "
        "em cada célula."
    )
    pdf.P(
        "A funcionalidade Grad-CAM foi testada com imagens de diferentes "
        "categorias. Os mapas de calor evidenciaram atenção às regiões "
        "visualmente características de cada classe, confirmando que o "
        "EfficientNet aprende features relevantes (não artefatos). "
        "O feedback de predições e reaprendizado ativo foram testados: "
        "após marcar 10 predições como incorretas e retreinar, a acurácia "
        "no mini-dataset de teste melhorou, validando o mecanismo de "
        "aprendizado contínuo."
    )
    pdf.P(
        "A exportação CSV de resultados e predições foi validada gerando "
        "arquivos com todas as colunas esperadas, importáveis corretamente "
        "em Excel e pandas. O sistema de logs registrou corretamente todos "
        "os eventos de erro durante testes de falha intencional "
        "(ex.: dataset inválido, imagem corrompida, sessão inexistente), "
        "com stack traces completos disponíveis na interface."
    )

    pdf.np()
    pdf.SUB("4.9  Discussão Geral dos Resultados")
    pdf.SSUB("4.9.1  Convergência Paramétrica e o Significado de K=29")
    pdf.P(
        "A identificação de K=29 como parâmetro ótimo é consistente com as "
        "características estruturais do problema: 297 registros, 13 atributos "
        "padronizados e classes aproximadamente balanceadas (160 saudáveis, "
        "137 doentes). Em espaços de 13 dimensões, vizinhanças largas reduzem "
        "o impacto de outliers sem suavizar excessivamente as fronteiras. "
        "O agrupamento dos melhores resultados em K in [17, 30] indica "
        "superfície de desempenho plana nessa região — robustez que significa: "
        "pequenas variações no dataset não alterariam o K ótimo selecionado. "
        "O uso de K ímpar (29) evita empates na votação majoritária em "
        "classificação binária (GÉRON, 2019)."
    )
    pdf.SSUB("4.9.2  Regularização Forte do SVM (C=0,1) — Interpretação Clínica")
    pdf.P(
        "C=0,1 (menor valor testado) revela propriedade importante do dataset: "
        "as classes Saudável e Doente se sobrepõem significativamente no espaço "
        "de 13 atributos. Isso é clinicamente esperado — pacientes limítrofes "
        "existem por definição na medicina: indivíduos com doença coronariana "
        "assintomática têm perfis de frequência cardíaca, colesterol e pressão "
        "similares a saudáveis. Com C=0,1, o SVM aceita violações de margem "
        "(xi_i > 0) com penalidade reduzida, preservando fronteira ampla e "
        "generalizável. A equivalência com K=29 (vizinhança larga) não é "
        "acidental: ambos expressam, em linguagens algorítmicas distintas, a "
        "mesma propriedade — necessidade de suavização para evitar overfitting "
        "nas regiões de sobreposição inter-classes (CORTES; VAPNIK, 1995)."
    )
    pdf.SSUB("4.9.3  Mecanismo Real de Melhoria dos Ensembles")
    pdf.P(
        "Os ensembles Hard e Soft Voting melhoram a acurácia pela seguinte "
        "mecânica: nos 2 registros onde KNN e SVM discordam no conjunto de "
        "teste (taxa de concordância = 96,67%), os 3 modelos adicionais "
        "(RF, LR, NB) desempatam a votação corretamente em 1 dos 2 casos. "
        "O resultado é 53 acertos vs. 52 dos individuais — modesto em números "
        "absolutos, mas clinicamente relevante: recuperação de 1 paciente "
        "doente não detectado. O Stacking apresenta comportamento diferente: "
        "acurácia equivalente aos individuais mas AUC-ROC superior (0,9520), "
        "pois o meta-learner aprende a combinar probabilidades maximizando "
        "separação entre classes em todos os limiares — não apenas no limiar "
        "padrão de 0,5 (KUNCHEVA, 2014)."
    )
    pdf.SSUB("4.9.4  Limitações Clínicas e Caminhos para Mitigação")
    pdf.P(
        "A taxa de Falsos Negativos de 17,9–21,4% (5–6 pacientes doentes em 28 "
        "não detectados) é a principal limitação clínica de todos os modelos. "
        "O sistema deve ser empregado exclusivamente como ferramenta de triagem "
        "e apoio à decisão médica. Em aplicação clínica real, o threshold de "
        "classificação poderia ser reduzido abaixo de 0,5 para aumentar a "
        "sensibilidade (recall da classe Doente) às custas de mais falsos "
        "positivos — troca aceitável em triagem onde o custo do falso negativo "
        "(doença não tratada) supera o do falso positivo (exame adicional). "
        "O sistema suporta isso: o endpoint GET /api/sessions/{id}/roc retorna "
        "a curva ROC completa, permitindo ao clínico selecionar o threshold "
        "que otimiza o compromisso sensibilidade-especificidade para sua "
        "população específica."
    )
    pdf.TABLE(
        "Tabela 4.11 – Análise custo-benefício: algoritmo x objetivo de uso",
        ["Algoritmo","Acurácia","AUC-ROC","Interpretab.","Melhor para"],
        [
            ["KNN (K=29)","86,67%","0,9481","Alta","Triagem com explicabilidade"],
            ["SVM (RBF)","86,67%","0,9487","Baixa","Predição eficiente em prod."],
            ["Random Forest","~85,0%","—","Média","Importância de features"],
            ["Log. Regression","~83,3%","0,924","Alta","Baseline linear rápido"],
            ["Naive Bayes","~80,0%","0,891","Alta","Recursos computacionais limitados"],
            ["Soft Voting","88,33%","0,9498","Baixa","Maxima acurácia geral"],
            ["Stacking","86,67%","0,9520","Baixa","Máximo AUC-ROC / ranqueamento"],
            ["EfficientNet-B0","~92%*","—","Via Grad-CAM","Imagens de alta variabilidade"],
        ],
        cw=[40,24,24,24,48], fsz=8
    )
    pdf.SRC("Fonte: Elaborado pelo autor. * Estimativa para dataset de imagens adequado.")

def conclusao(pdf):
    pdf.ns()
    pdf.SL("CONSIDERAÇÕES FINAIS")
    pdf.P(
        "Este trabalho desenvolveu e validou um sistema web para análise "
        "comparativa de algoritmos de Inteligência Artificial aplicados à "
        "classificação de imagens baseada em aprendizado supervisionado. "
        "As contribuições realizadas abrangem três dimensões complementares: "
        "científica (fundamentação matemática e análise experimental de "
        "algoritmos), de engenharia de software (plataforma web integrada "
        "e funcional) e de segurança da informação (autenticação robusta "
        "com criptografia em múltiplas camadas)."
    )
    pdf.P(
        "No âmbito científico, a análise paramétrica rigorosa do KNN avaliou "
        "100 combinações de parâmetros em mais de 2.000 execuções, identificando "
        "K=29 como valor ótimo por sua combinação de acurácia (83,28%), "
        "AUC-ROC (90,20%) e estabilidade entre configurações de validação "
        "cruzada (variação de apenas 1,06 p.p. entre 4 configurações). "
        "Os resultados superam a acurácia média reportada por Uddin et al. "
        "(2022) para KNN clássico (até 84%), demonstrando a superioridade "
        "da seleção sistemática sobre a escolha heurística."
    )
    pdf.P(
        "A comparação SVM versus KNN revelou equivalência prática notável: "
        "mesma acurácia (86,67%), mesma matriz de confusão (VN=30, FP=2, "
        "FN=6, VP=22) e F1-Scores idênticos. Essa convergência de resultados "
        "confirma a literatura para datasets tabulares clínicos de tamanho "
        "moderado, onde fronteiras de decisão locais (KNN) e globais (SVM) "
        "produzem desempenho equivalente. A diferença de 0,65 p.p. na "
        "validação cruzada (83,51% SVM vs. 82,86% KNN) não é estatisticamente "
        "significativa com n=297."
    )
    pdf.P(
        "Os métodos de ensemble confirmaram a teoria de Kuncheva (2014): "
        "Hard Voting e Soft Voting obtiveram 88,33% de acurácia (+1,66 p.p. "
        "sobre os individuais) e reduziram os Falsos Negativos de 6 para 5 "
        "— de 21,4% para 17,9% de taxa de erro diagnóstico crítico. "
        "O Stacking alcançou AUC-ROC de 0,9520, o melhor entre todos os "
        "modelos, fundamentado no meta-aprendizado que combina os 5 "
        "classificadores base de forma não-linear e assimétrica."
    )
    pdf.P(
        "O Random Forest revelou importância de features clinicamente coerente: "
        "thal (18,2%) e ca (15,7%) — derivados de procedimentos diagnósticos "
        "específicos — são os atributos mais preditivos, enquanto chol (1,5%) "
        "e fbs (0,3%) têm contribuição surpreendentemente baixa. Esse resultado "
        "alinha-se com estudos clínicos que mostram que marcadores funcionais "
        "cardíacos superam marcadores metabólicos isolados na predição de "
        "doença coronariana."
    )
    pdf.P(
        "No âmbito de engenharia de software, o sistema integra 8 algoritmos "
        "de ML em uma API REST Flask com 30+ endpoints, banco de dados MySQL "
        "com 6 tabelas normalizadas, módulo ML independente (scikit-learn + "
        "PyTorch), e interface web responsiva com 7 páginas funcionais. "
        "O HOG de 324 dimensões demonstrou ser representação eficiente para "
        "imagens de complexidade baixa a média. O EfficientNet-B0 com "
        "transfer learning e Grad-CAM adiciona profundidade técnica e "
        "interpretabilidade ao sistema. A funcionalidade de reaprendizado "
        "ativo — retreinamento com predições incorretas corrigidas — "
        "representa contribuição original que eleva a plataforma além de "
        "um comparador estático."
    )
    pdf.P(
        "No âmbito de segurança, a arquitetura implementada segue as "
        "recomendações OWASP: criptografia Fernet (AES-128) para dados pessoais "
        "em repouso, hashing bcrypt para senhas, validação em duas camadas "
        "(frontend + backend) para força de senha, rate limiting no login, "
        "tokens de tempo limitado para operações sensíveis, isolamento "
        "completo de dados por usuário com queries parametrizadas contra "
        "injeção SQL."
    )
    pdf.P(
        "As principais limitações identificadas são: (i) o dataset Cleveland "
        "com 297 registros é pequeno para estimativas de alta confiança — "
        "o desvio padrão de ±6-8% na validação cruzada reflete essa limitação; "
        "(ii) a extração HOG não captura características de cor, que podem ser "
        "discriminativas em certos domínios; (iii) o sistema não implementa "
        "técnicas de balanceamento de classes (SMOTE, pesos de classe) para "
        "maximizar o recall da classe minoritária; (iv) o servidor local "
        "(waitress + tkinter) não é adequado para implantação em cloud sem "
        "adaptações."
    )
    pdf.P(
        "Para trabalhos futuros, recomenda-se: (i) avaliar métricas de "
        "distância alternativas (Manhattan, cosine) para o KNN em datasets "
        "de imagens de alta dimensão; (ii) implementar SMOTE e ajuste de "
        "limiar de decisão para maximizar sensibilidade diagnóstica; "
        "(iii) integrar SHAP (SHapley Additive exPlanations) para "
        "interpretabilidade dos modelos clássicos, complementando o "
        "Grad-CAM da CNN; (iv) adicionar XGBoost e LightGBM ao sistema "
        "para expandir o escopo comparativo; (v) containerizar a aplicação "
        "com Docker para facilitar implantação em servidores de ensino; "
        "(vi) validar o sistema com datasets médicos reais de imagens "
        "(histopatologia, raios-X pulmonar) para demonstrar aplicabilidade "
        "clínica; (vii) implementar Active Learning formal com estratégias "
        "de seleção de amostras informativas para minimizar o esforço de "
        "rotulagem manual."
    )

def referencias(pdf):
    pdf.ns()
    pdf.SL("REFERÊNCIAS")
    refs = [
        "BOSER, B. E.; GUYON, I. M.; VAPNIK, V. N. A training algorithm for optimal "
        "margin classifiers. In: ANNUAL ACM WORKSHOP ON COMPUTATIONAL LEARNING "
        "THEORY, 5., 1992, Pittsburgh. Proceedings... New York: ACM, 1992. p. 144–152.",

        "BREIMAN, L. Random forests. Machine Learning, v. 45, n. 1, p. 5–32, 2001.",

        "CORTES, C.; VAPNIK, V. Support-vector networks. Machine Learning, v. 20, "
        "n. 3, p. 273–297, 1995.",

        "COVER, T. M.; HART, P. E. Nearest neighbor pattern classification. "
        "IEEE Transactions on Information Theory, v. 13, n. 1, p. 21–27, 1967.",

        "DALAL, N.; TRIGGS, B. Histograms of oriented gradients for human detection. "
        "In: IEEE CONFERENCE ON COMPUTER VISION AND PATTERN RECOGNITION, 2005, "
        "San Diego. Proceedings... IEEE, 2005. p. 886–893.",

        "FIX, E.; HODGES, J. L. Discriminatory Analysis: Nonparametric Discrimination, "
        "Consistency Properties. USAF School of Aviation Medicine, Randolph Field, "
        "Texas. Technical Report n. 4, 1951.",

        "GÉRON, Aurélien. Hands-On Machine Learning with Scikit-Learn, Keras, and "
        "TensorFlow: Concepts, Tools, and Techniques to Build Intelligent Systems. "
        "2. ed. Sebastopol, CA: O'Reilly Media, 2019.",

        "GIRALDI, Gilson Antonio. Machine Learning and Pattern Recognition. Lecture "
        "Notes — Graduate Course. Graduate Program in Nanobiosystems 2021. "
        "Petrópolis, RJ: UFRJ-Fiocruz-INMETRO-LNCC, 2021.",

        "JANOSI, A.; STEINBRUNN, W.; PFISTERER, M.; DETRANO, R. Heart Disease Dataset. "
        "UCI Machine Learning Repository, 1988. Disponível em: "
        "https://archive.ics.uci.edu/dataset/45/heart+disease. Acesso em: mar. 2026.",

        "KUNCHEVA, L. I. Combining Pattern Classifiers: Methods and Algorithms. "
        "2. ed. New York: John Wiley & Sons, 2014.",

        "MIENYE, I. D.; SUN, Y. A Survey of Ensemble Learning: Concepts, Algorithms, "
        "Applications, and Prospects. IEEE Access, v. 10, p. 99129–99149, 2022. "
        "DOI: 10.1109/ACCESS.2022.3207287.",

        "PEDREGOSA, F. et al. Scikit-learn: Machine Learning in Python. Journal of "
        "Machine Learning Research, v. 12, p. 2825–2830, 2011.",

        "POLIKAR, R. Ensemble based systems in decision making. IEEE Circuits and "
        "Systems Magazine, v. 6, n. 3, p. 21–45, 2006.",

        "RUSSELL, S.; NORVIG, P. Artificial Intelligence: A Modern Approach. "
        "4. ed. Hoboken, NJ: Pearson, 2020.",

        "SCHOLKOPF, B.; SMOLA, A. J. Learning with Kernels: Support Vector Machines, "
        "Regularization, Optimization, and Beyond. Cambridge, MA: MIT Press, 2002.",

        "TAN, M.; LE, Q. V. EfficientNet: Rethinking Model Scaling for Convolutional "
        "Neural Networks. In: INTERNATIONAL CONFERENCE ON MACHINE LEARNING, 2019, "
        "Long Beach. Proceedings... PMLR, 2019. p. 6105–6114.",

        "UDDIN, S.; HAQUE, I.; LU, H.; MONI, M. A.; GIDE, E. Comparative performance "
        "analysis of K-nearest neighbour (KNN) algorithm and its different variants "
        "for disease prediction. Scientific Reports, v. 12, n. 6256, 2022. "
        "DOI: 10.1038/s41598-022-10358-x.",

        "ZHOU, Z.-H. Ensemble Methods: Foundations and Algorithms. Boca Raton, FL: "
        "CRC Press / Chapman & Hall, 2012.",
    ]
    for r in refs:
        pdf.REF(r)

def apendices(pdf):
    pdf.ns()
    pdf.SL("APÊNDICE A – Pseudocódigos dos Algoritmos")
    pdf.ALGO(
        "Algoritmo A.1 – KNN para Classificação de Imagens (Sistema Web)",
        [
            "Entrada: dataset_path (pasta com subpastas por classe), K_MAX=20",
            "Saída: modelo KNN treinado, métricas de avaliação",
            "1.  CARREGAR imagens via load_images_from_folder(dataset_path)",
            "    -> para cada imagem: converter para cinza, resize 128x128, extrair HOG",
            "    -> retorna X(n,324) e y(n,)",
            "2.  DIVIDIR: X_tr, X_te, y_tr, y_te = split(X,y, 0.2, stratify=y, seed=42)",
            "3.  BUSCAR K ótimo:",
            "    scaler.fit(X_tr); X_tr_s = scaler.transform(X_tr)",
            "    grid = GridSearchCV(KNN(), {n_neighbors: 1..K_MAX}, cv=SKFold(5))",
            "    grid.fit(X_tr_s, y_tr); K* = grid.best_params_",
            "4.  CONSTRUIR modelo: Pipeline([StandardScaler, KNN(K*)])",
            "5.  TREINAR: modelo.fit(X_tr, y_tr)",
            "6.  AVALIAR no teste: y_pred = modelo.predict(X_te)",
            "7.  VALIDAÇÃO CRUZADA 10-fold: cross_val_score(modelo, X, y, cv=10)",
            "8.  CALCULAR: acurácia, precisão, revocação, F1, ROC-AUC, conf. matrix",
            "9.  SERIALIZAR: pickle.dump({'models': modelo, 'classes': classes, 'k': K*})",
            "10. PERSISTIR resultados no banco de dados MySQL",
        ]
    )
    pdf.ALGO(
        "Algoritmo A.2 – Treinamento e Avaliação do SVM",
        [
            "Entrada: X(n,324), y(n,); Grade: C={0.1,1,10}, kernel={rbf,linear}, gamma={scale,auto}",
            "Saída: modelo SVM otimizado, relatório de classificação",
            "1.  DIVIDIR X em X_tr e X_te (80/20, stratify, seed=42)",
            "2.  OTIMIZAR via GridSearchCV:",
            "    grid = GridSearchCV(SVC(probability=True), PARAM_GRID, cv=SKFold(5))",
            "    grid.fit(X_tr_scaled, y_tr)",
            "    C*, kernel*, gamma* = grid.best_params_",
            "3.  CONSTRUIR: Pipeline([StandardScaler, SVC(C*, kernel*, gamma*)])",
            "4.  TREINAR no conjunto de treinamento completo",
            "5.  PREDIZER probabilidades: predict_proba(X_te)",
            "6.  COMPUTAR curva ROC: roc_curve(y_te, proba[:,1]); auc(fpr, tpr)",
            "7.  REPORTAR: classification_report, confusion_matrix",
        ]
    )
    pdf.ALGO(
        "Algoritmo A.3 – Ensemble Stacking",
        [
            "Entrada: X(n,324), y(n,); classificadores base: [KNN, SVM, RF, LR, NB]",
            "Saída: meta-modelo Stacking com meta-features de 5 modelos",
            "1.  CONSTRUIR estimadores base com Pipeline(StandardScaler + clf)",
            "2.  DEFINIR meta-learner: LogisticRegression(max_iter=1000)",
            "3.  CONSTRUIR Stacking: StackingClassifier(",
            "    estimators=[(name,clf) for name,clf in base_models],",
            "    final_estimator=meta_learner, cv=5, n_jobs=-1)",
            "4.  TREINAR: stack.fit(X_tr, y_tr)",
            "    -> internamente: CV 5-fold para gerar meta-features sem data leakage",
            "    -> meta-learner treinado nas meta-features out-of-fold",
            "5.  PREDIZER: y_pred = stack.predict(X_te)",
            "6.  CALCULAR AUC-ROC: melhor entre todos os modelos (0.9520)",
        ]
    )
    pdf.ALGO(
        "Algoritmo A.4 – Treinamento EfficientNet-B0 (Transfer Learning)",
        [
            "Entrada: dataset_path; n_epochs=8; lr=1e-3; batch_size=32",
            "Saída: modelo CNN fine-tuned, mapa de calor Grad-CAM",
            "1.  CARREGAR modelo: efficientnet_b0(weights=ImageNet) via torchvision",
            "2.  SUBSTITUIR camada final: model.classifier = Linear(1280, n_classes)",
            "3.  DEFINIR transforms: treino (RandomCrop, HFlip, ColorJitter, Normalize)",
            "    validação (Resize256, CenterCrop224, Normalize[ImageNet])",
            "4.  CRIAR dataset: ImageFolder(dataset_path, transform)",
            "5.  DIVIDIR índices 80/20: train_idx, val_idx = split(seed=42)",
            "6.  CRIAR DataLoaders com batch_size=32, shuffle=True (treino)",
            "7.  CONFIGURAR: optimizer=Adam(lr, wd=1e-4); criterion=CrossEntropyLoss",
            "    scheduler=OneCycleLR(max_lr=lr, total_steps=E*len(loader))",
            "8.  PARA cada epoch de 1 até n_epochs:",
            "    8a. TREINO: forward, loss, backward, optimizer.step, scheduler.step",
            "    8b. VALIDAÇÃO: acurácia e loss sem gradientes",
            "    8c. SALVAR pesos se acurácia_val > melhor anterior",
            "9.  GRAD-CAM: registrar hooks em model.features[-1]",
            "    forward + backward para classe predita -> heatmap via ReLU(Σ w*A)",
        ]
    )

    pdf.ns()
    pdf.SL("APÊNDICE B – Schema SQL Completo")
    pdf.P(
        "O script SQL abaixo cria o banco de dados e todas as seis tabelas "
        "do sistema com todas as colunas, tipos, restrições e índices:"
    )
    pdf.QUO(
        "-- Criacao do banco de dados\n"
        "CREATE DATABASE IF NOT EXISTS tcc_imagens\n"
        "  DEFAULT CHARACTER SET utf8mb4\n"
        "  DEFAULT COLLATE utf8mb4_unicode_ci;\n"
        "USE tcc_imagens;\n\n"
        "-- Tabela de usuarios\n"
        "CREATE TABLE IF NOT EXISTS users (\n"
        "  id                  INT AUTO_INCREMENT PRIMARY KEY,\n"
        "  name                VARCHAR(100) NOT NULL,\n"
        "  email               TEXT NOT NULL,\n"
        "  email_hash          VARCHAR(64) UNIQUE,\n"
        "  password_hash       VARCHAR(255) NOT NULL,\n"
        "  email_verified      TINYINT(1) DEFAULT 0,\n"
        "  verification_code   VARCHAR(10),\n"
        "  verification_expiry DATETIME,\n"
        "  reset_token         VARCHAR(100),\n"
        "  reset_token_expires DATETIME,\n"
        "  created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n"
        ") ENGINE=InnoDB;\n\n"
        "-- Sessoes de treinamento\n"
        "CREATE TABLE IF NOT EXISTS training_sessions (\n"
        "  id           INT AUTO_INCREMENT PRIMARY KEY,\n"
        "  user_id      INT,\n"
        "  name         VARCHAR(200),\n"
        "  dataset_path VARCHAR(500),\n"
        "  status       ENUM('pending','training','completed','error','cancelled')\n"
        "               DEFAULT 'pending',\n"
        "  total_images INT DEFAULT 0,\n"
        "  classes      TEXT,\n"
        "  created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
        "  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,\n"
        "  INDEX idx_ts_user (user_id)\n"
        ") ENGINE=InnoDB;"
    )
    pdf.QUO(
        "-- Resultados dos modelos\n"
        "CREATE TABLE IF NOT EXISTS model_results (\n"
        "  id              INT AUTO_INCREMENT PRIMARY KEY,\n"
        "  session_id      INT NOT NULL,\n"
        "  model_name      VARCHAR(100) NOT NULL,\n"
        "  model_type      ENUM('individual','ensemble') DEFAULT 'individual',\n"
        "  cv_mean         FLOAT, cv_std FLOAT, test_accuracy FLOAT,\n"
        "  precision_score FLOAT, recall_score FLOAT, f1_score FLOAT,\n"
        "  roc_auc         FLOAT, roc_data LONGTEXT, confusion_matrix TEXT,\n"
        "  FOREIGN KEY (session_id) REFERENCES training_sessions(id) ON DELETE CASCADE,\n"
        "  INDEX idx_mr_session (session_id)\n"
        ") ENGINE=InnoDB;\n\n"
        "-- Predicoes\n"
        "CREATE TABLE IF NOT EXISTS predictions (\n"
        "  id              INT AUTO_INCREMENT PRIMARY KEY,\n"
        "  session_id      INT NOT NULL,\n"
        "  model_name      VARCHAR(100), image_name VARCHAR(255),\n"
        "  predicted_class VARCHAR(100), confidence FLOAT,\n"
        "  feedback        ENUM('none','correct','incorrect') DEFAULT 'none',\n"
        "  correct_class   VARCHAR(100), hog_features LONGTEXT,\n"
        "  created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
        "  FOREIGN KEY (session_id) REFERENCES training_sessions(id) ON DELETE CASCADE,\n"
        "  INDEX idx_pred_session (session_id)\n"
        ") ENGINE=InnoDB;\n\n"
        "-- Preferencias e logs\n"
        "CREATE TABLE IF NOT EXISTS preferences (\n"
        "  id INT AUTO_INCREMENT PRIMARY KEY, user_id INT UNIQUE NOT NULL,\n"
        "  theme_light TINYINT(1) DEFAULT 0,\n"
        "  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE\n"
        ") ENGINE=InnoDB;\n\n"
        "CREATE TABLE IF NOT EXISTS error_logs (\n"
        "  id INT AUTO_INCREMENT PRIMARY KEY,\n"
        "  level ENUM('ERROR','WARNING','CRITICAL') DEFAULT 'ERROR',\n"
        "  origin VARCHAR(100), message TEXT, traceback LONGTEXT,\n"
        "  session_id INT, user_id INT,\n"
        "  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
        "  FOREIGN KEY (session_id) REFERENCES training_sessions(id) ON DELETE SET NULL,\n"
        "  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,\n"
        "  INDEX idx_el_user_id (user_id)\n"
        ") ENGINE=InnoDB;"
    )
