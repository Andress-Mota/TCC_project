#!/usr/bin/env python3
"""TCC FATEC-GT 2026 — Parte 4: Cap 2 completo + Cap 3 início"""
from tcc_parte1 import PDF, ML, MR, MT, MB, PW, CW, SB, ST, SS, SC, LH, LT, LC, IND

def cap2(pdf):
    pdf.ns()
    pdf.SL("2  METODOLOGIA")

    pdf.SUB("2.1  Visão Geral e Etapas do Trabalho")
    pdf.P(
        "A metodologia deste trabalho seguiu uma abordagem em dois eixos paralelos. "
        "O eixo de pesquisa científica consistiu no estudo teórico dos algoritmos, "
        "implementação em scripts Python independentes, validação com dataset "
        "público de referência (Cleveland Heart Disease Dataset) e análise "
        "comparativa fundamentada na literatura. O eixo de engenharia de software "
        "consistiu no desenvolvimento do sistema web integrado, compreendendo "
        "banco de dados, API REST, módulos de ML e frontend. Os dois eixos são "
        "complementares: os algoritmos validados no eixo de pesquisa foram "
        "diretamente integrados no sistema do eixo de engenharia."
    )
    pdf.P(
        "O desenvolvimento foi organizado em cinco fases sequenciais: (1) Revisão "
        "bibliográfica e fundamentação matemática (meses 1-2); (2) Implementação "
        "e validação dos algoritmos clássicos com dataset UCI (meses 3-4); "
        "(3) Desenvolvimento do banco de dados e API Flask (meses 4-5); "
        "(4) Implementação do módulo CNN e frontend (meses 5-6); (5) Testes "
        "integrados, documentação e elaboração do relatório (meses 6-7)."
    )

    pdf.SUB("2.2  Dataset: Cleveland Heart Disease")
    pdf.P(
        "O Cleveland Heart Disease Dataset é amplamente reconhecido como referência "
        "em pesquisas de aprendizado de máquina para diagnóstico cardíaco. Foi "
        "coletado na Cleveland Clinic Foundation (Cleveland, EUA) por pesquisadores "
        "liderados pelo Dr. Robert Detrano nos anos 1980 e disponibilizado "
        "publicamente no UCI Machine Learning Repository (JANOSI et al., 1988). "
        "É um dos datasets mais citados na literatura de aprendizado de máquina "
        "médico, com mais de 2.000 citações documentadas."
    )
    pdf.SSUB("2.2.1  Estatísticas do Dataset")
    pdf.TABLE(
        "Tabela 2.1 – Estatísticas do Cleveland Heart Disease Dataset",
        ["Característica","Valor"],
        [
            ["Total de registros (original)","303"],
            ["Registros após limpeza","297 (6 removidos por NaN)"],
            ["Número de atributos preditores","13"],
            ["Variável alvo (original)","5 classes: 0,1,2,3,4"],
            ["Variável alvo (binarizada)","2 classes: 0=Saudável, 1=Doente"],
            ["Saudáveis (y=0) após binarização","160 (53,9%)"],
            ["Doentes (y=1) após binarização","137 (46,1%)"],
            ["Desbalanceamento","Moderado (proporção 1,17:1)"],
            ["Período de coleta","1987-1989"],
            ["Local","Cleveland Clinic Foundation, EUA"],
        ],
        cw=[90,70], fsz=10
    )
    pdf.SRC("Fonte: JANOSI et al. (1988); UCI Machine Learning Repository.")
    pdf.SSUB("2.2.2  Descrição Detalhada dos Atributos")
    pdf.TABLE(
        "Tabela 2.2 – Descrição detalhada dos 13 atributos preditores",
        ["Atrib.","Descrição","Tipo","Min","Max","Média"],
        [
            ["age","Idade (anos)","Numérico","29","77","54,4"],
            ["sex","Sexo: 1=masc., 0=fem.","Binário","0","1","0,68"],
            ["cp","Dor torácica: 0=assint., 1=angina atípica, 2=não-anginosa, 3=angina típica","Categ.","0","3","0,97"],
            ["trestbps","Pressão arterial repouso (mmHg)","Numérico","94","200","131,7"],
            ["chol","Colesterol sérico (mg/dl)","Numérico","126","564","246,7"],
            ["fbs","Glicemia em jejum > 120 mg/dl","Binário","0","1","0,15"],
            ["restecg","ECG repouso: 0=normal, 1=ST-T anormal, 2=HVE","Categ.","0","2","0,99"],
            ["thalach","Freq. card. máx. (bpm)","Numérico","71","202","149,6"],
            ["exang","Angina por exercício: 1=sim","Binário","0","1","0,33"],
            ["oldpeak","Depressão ST por exercício","Numérico","0","6,2","1,04"],
            ["slope","Inclinação ST: 0=ascendente, 1=plano, 2=descendente","Categ.","0","2","1,60"],
            ["ca","Vasos principais (fluoroscopia): 0-3","Ordinal","0","3","0,67"],
            ["thal","Tálio: 0=normal, 1=defeito fixo, 2=defeito reversível","Categ.","0","3","4,73"],
        ],
        cw=[20,58,18,12,12,20], fsz=8
    )
    pdf.SRC("Fonte: JANOSI et al. (1988). Estatísticas calculadas sobre os 297 registros limpos.")

    pdf.SUB("2.3  Análise Exploratória dos Dados")
    pdf.P(
        "Antes do treinamento dos modelos, foi realizada análise exploratória dos "
        "dados para compreender a distribuição dos atributos e a separabilidade "
        "das classes. Essa análise fundamentou as decisões metodológicas de "
        "pré-processamento e modelagem."
    )
    pdf.SSUB("2.3.1  Distribuição das Classes")
    pdf.P(
        "Após binarização, a distribuição das classes é: 160 saudáveis (53,9%) e "
        "137 doentes (46,1%), com razão de desbalanceamento de 1,17:1. Esse nível "
        "de desbalanceamento é moderado — não justifica técnicas de oversampling "
        "como SMOTE para o protocolo experimental desta pesquisa, embora possa ser "
        "endereçado em trabalhos futuros. No particionamento estratificado 80/20, "
        "o conjunto de treinamento contém 128 saudáveis e 109 doentes (237 total), "
        "e o conjunto de teste contém 32 saudáveis e 28 doentes (60 total)."
    )
    pdf.SSUB("2.3.2  Atributos mais Preditivos")
    pdf.P(
        "A análise de correlação ponto-biserial entre cada atributo numérico e a "
        "variável alvo binarizada revela os atributos mais discriminativos. Os "
        "atributos com maior poder preditivo observado são:"
    )
    pdf.TABLE(
        "Tabela 2.3 – Correlação dos atributos com a variável alvo (binarizada)",
        ["Atributo","Correlação","Direção","Interpretação clínica"],
        [
            ["thal","0,52","Positiva","Defeito no teste com tálio = fortemente associado a doença"],
            ["ca","0,47","Positiva","Mais vasos ocluídos = maior risco"],
            ["cp","0,41","Negativa","Angina típica (tipo 3) = maior risco"],
            ["oldpeak","0,43","Positiva","Maior depressão ST = maior isquemia"],
            ["thalach","0,42","Negativa","Menor freq. cardíaca máx. = pior prognóstico"],
            ["exang","0,44","Positiva","Angina por exercício = risco elevado"],
            ["slope","0,35","Positiva","Slope descendente = maior risco"],
            ["sex","0,28","Positiva","Sexo masculino = maior prevalência"],
            ["age","0,23","Positiva","Idade maior = maior risco"],
            ["chol","0,08","Fraca","Correlação fraca com target"],
        ],
        cw=[26,30,22,82], fsz=9
    )
    pdf.SRC("Fonte: Dados calculados pelo autor.")
    pdf.P(
        "Observa-se que o atributo cp (tipo de dor torácica) apresenta correlação "
        "negativa com o target binarizado porque o tipo 3 (angina típica) está "
        "fortemente associado a doença, mas foi codificado como 3 — maior valor "
        "numérico. Na prática, cp=0 (assintomático) é o mais fortemente associado "
        "a doença cardíaca silenciosa, enquanto cp=3 (angina típica) é o esperado "
        "por clínicos como sinal de doença mas pode ser sinal de angina estável "
        "tratável. Essa aparente contradição ilustra a complexidade das relações "
        "não-lineares que os algoritmos precisam capturar."
    )
    pdf.SSUB("2.3.3  Tratamento de Valores Ausentes")
    pdf.P(
        "O dataset original de 303 registros contém 6 registros com valores "
        "ausentes nos atributos ca e thal — os dois atributos derivados de "
        "procedimentos diagnósticos específicos (fluoroscopia e cintilografia "
        "com tálio). Esses registros foram removidos inteiramente, pois imputação "
        "desses valores poderia introduzir viés clinicamente inaceitável: "
        "ausência de dados nessas variáveis indica que o procedimento não foi "
        "realizado (potencialmente por razões clínicas relevantes), não sendo "
        "adequado imputar valores artificiais. Os 297 registros restantes "
        "foram utilizados em todos os experimentos."
    )

    pdf.np()
    pdf.SUB("2.4  Pipeline de Pré-processamento")
    pdf.P(
        "O pipeline de pré-processamento foi implementado de forma sistemática "
        "para garantir reprodutibilidade e prevenir data leakage. As três etapas "
        "são aplicadas na ordem estrita: remoção de ausentes, binarização do "
        "target, particionamento estratificado e normalização."
    )
    pdf.SSUB("2.4.1  Binarização da Variável Alvo")
    pdf.P(
        "A variável alvo original usa 5 valores (0-4), onde 0 significa ausência "
        "de doença e 1-4 representam graus crescentes de comprometimento cardíaco "
        "(1=leve, 2=moderado, 3=sério, 4=grave). A binarização adotada foi:"
    )
    pdf.QUO(
        "y_bin = 0  se y_orig = 0  (Saudavel: sem evidencia de doenca)\n"
        "y_bin = 1  se y_orig > 0  (Doente: qualquer grau de comprometimento)"
    )
    pdf.P(
        "Essa decisão é metodologicamente justificada por três razões: (1) "
        "alinha o problema à pergunta clínica central da triagem ('o paciente "
        "deve ser encaminhado ao cardiologista?'); (2) reduz a ambiguidade "
        "entre classes intermediárias clinicamente próximas (ex.: grau 1 vs. "
        "grau 2), que mesmo especialistas humanos distinguem com dificuldade; "
        "(3) aumenta o número de exemplos por classe, melhorando as estimativas "
        "de desempenho. O impacto da binarização no desempenho foi verificado: "
        "o modelo multiclasse obteve acurácia de ~65%, enquanto o binário "
        "alcançou 82-88% com os mesmos algoritmos."
    )
    pdf.SSUB("2.4.2  Particionamento Estratificado")
    pdf.P(
        "O dataset de 297 registros foi dividido em:"
    )
    pdf.TABLE(
        "Tabela 2.4 – Distribuição das partições após divisão estratificada",
        ["Partição","Total","Saudáveis","Doentes","% Saudáveis"],
        [
            ["Treinamento (80%)","237","128","109","54,0%"],
            ["Teste (20%)","60","32","28","53,3%"],
            ["Total","297","160","137","53,9%"],
        ],
        cw=[40,20,30,25,45], fsz=10
    )
    pdf.SRC("Fonte: Dados do experimento (random_state=42).")
    pdf.P(
        "O parâmetro stratify=y garante que a proporção Saudável/Doente seja "
        "aproximadamente preservada em ambas as partições (53,9% no total, "
        "54,0% no treino, 53,3% no teste). O random_state=42 garante "
        "reprodutibilidade total: qualquer re-execução do código produz "
        "exatamente as mesmas partições."
    )
    pdf.SSUB("2.4.3  Normalização Z-score e Prevenção de Data Leakage")
    pdf.P(
        "A normalização é aplicada após o particionamento, com parâmetros "
        "estimados EXCLUSIVAMENTE sobre X_train:"
    )
    pdf.QUO(
        "# Calcula parametros no treino\n"
        "scaler = StandardScaler()\n"
        "X_train_s = scaler.fit_transform(X_train)  # fit + transform\n\n"
        "# Aplica os mesmos parametros ao teste (SEM re-estimar)\n"
        "X_test_s  = scaler.transform(X_test)       # apenas transform"
    )
    pdf.P(
        "Cada atributo j tem sua media (mu_j) e desvio padrão (sigma_j) "
        "calculados sobre os 237 exemplos de treinamento. Esses parâmetros são "
        "então aplicados ao conjunto de teste — que 'não existe' para o modelo "
        "durante o treinamento. Se os parâmetros fossem calculados sobre todo "
        "o dataset (303 ou 297 exemplos), as estatísticas do teste contaminariam "
        "o pré-processamento, produzindo estimativas de desempenho que não se "
        "reproduzem em dados reais de produção."
    )

    pdf.np()
    pdf.SUB("2.5  Extração de Features HOG para Imagens")
    pdf.P(
        "Para o sistema de classificação de imagens (aplicação prática), o "
        "pipeline de pré-processamento é distinto do usado na validação com "
        "dados tabulares. Cada imagem passa por extração HOG para obter o "
        "vetor de features numérico que alimenta os classificadores clássicos."
    )
    pdf.P(
        "O pipeline de extração é implementado nas funções load_images_from_folder() "
        "e preprocess_single_image() do módulo backend/ml/preprocessor.py. "
        "A função load_images_from_folder() percorre as subpastas do dataset "
        "(uma subpasta por classe), carrega cada imagem em escala de cinza via "
        "cv2.imread(img_path, cv2.IMREAD_GRAYSCALE), redimensiona para 128x128 "
        "via cv2.resize() e extrai HOG via skimage.feature.hog() com parâmetros: "
        "orientations=9, pixels_per_cell=(16,16), cells_per_block=(2,2), "
        "visualize=True. O resultado é um array numpy X de shape (n, 324) "
        "e array y de rótulos inteiros (0, 1, 2, ..., K-1)."
    )
    pdf.P(
        "Formatos de imagem suportados: JPG, JPEG, PNG, BMP, TIFF, TIF e WebP. "
        "Arquivos com outras extensões são ignorados com log de aviso. Imagens "
        "corrompidas ou ilegíveis também são ignoradas. O sistema valida que "
        "cada classe possui ao menos 1 imagem válida, lançando ValueError "
        "caso contrário. A estrutura de pastas esperada é:"
    )
    pdf.QUO(
        "dataset/\n"
        "  classe_a/\n"
        "    img001.jpg\n"
        "    img002.png\n"
        "    ...\n"
        "  classe_b/\n"
        "    img001.jpg\n"
        "    ...\n"
        "  [classe_c/  ...]"
    )
    pdf.P(
        "Datasets compactados em ZIP, TAR, TAR.GZ, TGZ ou TAR.BZ2 são "
        "automaticamente extraídos para um diretório temporário com a mesma "
        "estrutura. O sistema suporta ao menos 2 e até dezenas de classes, "
        "limitado apenas pela memória disponível."
    )

    pdf.np()
    pdf.SUB("2.6  Protocolo de Treinamento e Otimização de Hiperparâmetros")
    pdf.P(
        "O protocolo de treinamento segue o pipeline implementado na função "
        "train_and_evaluate() do módulo backend/ml/ensemble.py:"
    )
    pdf.SSUB("2.6.1  Fluxo de Treinamento")
    pdf.BULL([
        "Passo 1: Divisão estratificada treino/teste (80/20, random_state=42);",
        "Passo 2: Busca do melhor K para KNN via GridSearchCV + StratifiedKFold(5), "
        "K in {1,...,20}, n_jobs=-1 para paralelismo;",
        "Passo 3: Construção dos 5 modelos base com Pipeline(StandardScaler + Classificador): "
        "KNN(n_neighbors=k_best), SVC(C=0.1, kernel='rbf', gamma='scale', probability=True), "
        "RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42), "
        "LogisticRegression(max_iter=1000, random_state=42), GaussianNB();",
        "Passo 4: Construção dos 3 modelos ensemble: VotingClassifier(voting='hard'), "
        "VotingClassifier(voting='soft'), StackingClassifier(estimators=[...], "
        "final_estimator=LogisticRegression(), cv=5, n_jobs=-1);",
        "Passo 5: Para cada um dos 8 modelos — treino no conjunto de treinamento, "
        "avaliação no teste, validação cruzada 10-fold no dataset completo;",
        "Passo 6: Cálculo das métricas (acurácia, precisão, revocação, F1, ROC-AUC, matriz de confusão);",
        "Passo 7: Serialização dos modelos em arquivo .pkl;",
        "Passo 8: Persistência dos resultados no banco de dados MySQL.",
    ])
    pdf.SSUB("2.6.2  Justificativa da Grade de Hiperparâmetros")
    pdf.P(
        "Para o KNN, a grade K in {1,...,20} cobre o intervalo onde o trade-off "
        "viés-variância é mais sensível para o tamanho de dataset empregado "
        "(237 exemplos de treinamento). Valores de K próximos de 20 já representam "
        "~8,4% do dataset de treinamento — suficiente para capturar estrutura "
        "global sem overfitting local. Na análise paramétrica ampliada "
        "(pesquisa da Fase 1), o intervalo foi estendido para K in {1,...,49}."
    )
    pdf.P(
        "Para o SVM, os valores C in {0.1, 1, 10} cobrem três décadas de "
        "regularização, kernel in {rbf, linear} cobre os dois casos mais comuns "
        "em dados tabulares, e gamma in {scale, auto} são as duas configurações "
        "automáticas do scikit-learn. A grade de 12 combinações (x5 dobras) "
        "é computacionalmente acessível (fracção de segundo para n=237)."
    )
    pdf.SSUB("2.6.3  Treinamento Assíncrono no Sistema")
    pdf.P(
        "No sistema web, o treinamento é executado em uma thread daemon separada "
        "para não bloquear o servidor Flask (que deve continuar respondendo a "
        "outras requisições durante o treinamento, que pode durar minutos). "
        "Um dicionário global training_progress mantém o estado de cada sessão: "
        "etapa atual, porcentagem de conclusão e status "
        "('pending'/'training'/'completed'/'error'). O frontend realiza polling "
        "a cada 500ms no endpoint GET /api/sessions/{id}/status, exibindo barra "
        "de progresso animada em tempo real."
    )

    pdf.np()
    pdf.SUB("2.7  Protocolo de Avaliação Estatística")
    pdf.P(
        "O protocolo de avaliação foi definido com rigor para garantir comparações "
        "justas entre todos os algoritmos e estimativas confiáveis de desempenho."
    )
    pdf.SSUB("2.7.1  Hierarquia de Métricas")
    pdf.P(
        "As métricas foram organizadas em ordem decrescente de confiabilidade:"
    )
    pdf.TABLE(
        "Quadro 2.1 – Hierarquia de métricas por confiabilidade",
        ["Prioridade","Métrica","Por que usar como principal"],
        [
            ["1ª (principal)","Acurácia CV 10-fold ± desvio","Estimativa mais robusta; usa todos os dados"],
            ["2ª","AUC-ROC","Independente do limiar; discriminação global"],
            ["3ª","Acurácia no teste hold-out","Mais intuitiva; avalia em dados separados"],
            ["4ª","Precisão e Revocação","Diagnóstico de erros por tipo (FP vs. FN)"],
            ["5ª","F1-Score","Equilíbrio entre precisão e revocação"],
            ["6ª","Matriz de confusão","Diagnóstico completo por classe"],
        ],
        cw=[28,52,80], fsz=9
    )
    pdf.SRC("Fonte: Elaborado pelo autor com base em Géron (2019).")
    pdf.P(
        "A validação cruzada de 10 dobras é a métrica primária por três razões: "
        "(1) utiliza todos os 297 exemplos tanto para treinamento quanto para "
        "avaliação (ao contrário do teste hold-out que usa apenas 60); "
        "(2) a média de 10 avaliações independentes reduz a variância da estimativa; "
        "(3) é padrão na literatura para datasets de tamanho moderado. "
        "O desvio padrão entre dobras quantifica a estabilidade do modelo: "
        "alto desvio indica sensibilidade à partição dos dados."
    )
    pdf.SSUB("2.7.2  Aleatoriedade e Reprodutibilidade")
    pdf.P(
        "Todos os experimentos utilizam random_state=42 para garantir reprodutibilidade "
        "perfeita: qualquer desenvolvedor que execute os scripts obterá exatamente "
        "os mesmos resultados. Os parâmetros com randomização explícita são: "
        "train_test_split (random_state=42), StratifiedKFold (shuffle=True, "
        "random_state=42), GridSearchCV (cv=StratifiedKFold(5, shuffle=True, "
        "random_state=42)), RandomForestClassifier (random_state=42), "
        "SVC (random_state=42), LogisticRegression (random_state=42)."
    )

    pdf.np()
    pdf.SUB("2.8  Ambiente Computacional")
    pdf.P(
        "Os experimentos foram conduzidos no seguinte ambiente computacional:"
    )
    pdf.TABLE(
        "Tabela 2.5 – Configuração do ambiente computacional",
        ["Componente","Especificação"],
        [
            ["Sistema Operacional","Windows 11 Home Single Language"],
            ["Linguagem","Python 3.11+"],
            ["Framework ML","scikit-learn (última versão estável)"],
            ["Framework DL","PyTorch + torchvision"],
            ["Processamento de Imagens","OpenCV (opencv-python), scikit-image, Pillow"],
            ["Framework Web","Flask + Flask-CORS + Flask-Limiter"],
            ["Servidor WSGI","Waitress (porta 5000)"],
            ["Banco de Dados","MySQL 8.0+"],
            ["Frontend","HTML5 + CSS3 + JavaScript (Chart.js para gráficos)"],
            ["Criptografia","cryptography (Fernet/AES-128), werkzeug (bcrypt)"],
            ["Ambiente Virtual","Python venv"],
            ["IDE","Visual Studio Code"],
        ],
        cw=[60,100], fsz=9
    )
    pdf.SRC("Fonte: Elaborado pelo autor.")

def cap3_inicio(pdf):
    pdf.ns()
    pdf.SL("3  DESENVOLVIMENTO DO SISTEMA")

    pdf.SUB("3.1  Levantamento de Requisitos")
    pdf.SSUB("3.1.1  Requisitos Funcionais")
    pdf.TABLE(
        "Quadro 3.1 – Requisitos Funcionais do Sistema",
        ["ID","Requisito","Prioridade"],
        [
            ["RF01","Cadastro de usuário com nome, email e senha","Alta"],
            ["RF02","Verificação de email por código de 6 dígitos enviado via SMTP","Alta"],
            ["RF03","Login com autenticação por sessão Flask e proteção brute-force","Alta"],
            ["RF04","Upload de dataset via seleção de pasta local ou arquivo compactado","Alta"],
            ["RF05","Treinamento assíncrono de 8 modelos com progresso em tempo real","Alta"],
            ["RF06","Treinamento opcional de CNN EfficientNet-B0","Média"],
            ["RF07","Visualização de métricas: acurácia, precisão, revocação, F1, AUC","Alta"],
            ["RF08","Curva ROC interativa por modelo (Chart.js)","Alta"],
            ["RF09","Matriz de confusão colorida por sessão","Alta"],
            ["RF10","Classificação de imagens individuais ou em lote com confiança","Alta"],
            ["RF11","Geração de mapa de calor Grad-CAM para predições CNN","Média"],
            ["RF12","Sistema de feedback: marcar predição como correta/incorreta","Média"],
            ["RF13","Reaprendizado ativo: retreinar com predições corrigidas","Média"],
            ["RF14","Exportação de resultados e histórico em CSV","Média"],
            ["RF15","Histórico paginado de predições por sessão","Baixa"],
            ["RF16","Log de erros de sistema filtráveis por nível e origem","Baixa"],
            ["RF17","Alternância entre tema escuro e claro com persistência","Baixa"],
            ["RF18","Edição de perfil: nome, email (com reverificação) e senha","Média"],
            ["RF19","Dashboard com estatísticas agregadas por usuário","Média"],
            ["RF20","Suporte a múltiplos usuários com isolamento de dados","Alta"],
        ],
        cw=[15,110,35], fsz=8
    )
    pdf.SRC("Fonte: Elaborado pelo autor.")

    pdf.SSUB("3.1.2  Requisitos Não-Funcionais")
    pdf.TABLE(
        "Quadro 3.2 – Requisitos Não-Funcionais do Sistema",
        ["ID","Requisito","Critério de Aceitação"],
        [
            ["RNF01","Segurança: emails criptografados com AES-128 (Fernet)","Emails ilegíveis no banco de dados"],
            ["RNF02","Segurança: senhas com bcrypt (fator custo 12)","Tempo de verificação > 100ms"],
            ["RNF03","Segurança: rate limiting no login","Máx. 10 tentativas/min por IP"],
            ["RNF04","Segurança: queries parametrizadas","Zero vulnerabilidades SQL Injection"],
            ["RNF05","Desempenho: treinamento dos 8 modelos","< 5 minutos para dataset típico"],
            ["RNF06","Desempenho: predição por imagem","< 200ms por imagem"],
            ["RNF07","Usabilidade: interface responsiva","Funcional em desktop e mobile"],
            ["RNF08","Disponibilidade: servidor local","Inicialização com duplo clique (start.bat)"],
            ["RNF09","Confiabilidade: treinamento assíncrono","Servidor Flask não bloqueia durante treino"],
            ["RNF10","Manutenibilidade: isolamento de módulos","Módulo ML independente do Flask"],
        ],
        cw=[18,80,62], fsz=8
    )
    pdf.SRC("Fonte: Elaborado pelo autor.")

    pdf.SUB("3.2  Arquitetura Geral do Sistema")
    pdf.P(
        "O sistema segue uma arquitetura em três camadas (three-tier architecture), "
        "padrão consolidado para aplicações web que separa responsabilidades "
        "de apresentação, lógica de negócios e dados:"
    )
    pdf.BULL([
        "Camada de Apresentação (Frontend): HTML5, CSS3, JavaScript puro. "
        "Responsável pela interface do usuário, navegação entre páginas, "
        "chamadas AJAX à API e renderização de visualizações (Chart.js);",
        "Camada de Lógica de Negócios (Backend): Python + Flask. "
        "Implementa a API REST, orquestra o pipeline de ML, gerencia "
        "autenticação/autorização, executa processamento assíncrono e "
        "aplica regras de segurança;",
        "Camada de Dados (Banco de Dados): MySQL 8.0. Persiste usuários, "
        "sessões de treinamento, resultados de modelos, predições, preferências "
        "e logs de erro com integridade referencial garantida por chaves "
        "estrangeiras.",
    ])
    pdf.P(
        "A comunicação entre frontend e backend utiliza o protocolo HTTP com "
        "troca de dados em formato JSON via API REST. As requisições são "
        "autenticadas por cookies de sessão gerenciados pelo Flask (sessão "
        "permanente com lifetime de 24 horas). O servidor WSGI Waitress substitui "
        "o servidor de desenvolvimento do Flask, oferecendo maior estabilidade "
        "e capacidade de múltiplas conexões simultâneas em ambiente local."
    )
    pdf.P(
        "O módulo de Machine Learning (ml/) é completamente independente do "
        "Flask: não importa módulos do framework web e pode ser executado "
        "isoladamente. Essa separação facilita testes unitários do módulo ML "
        "e permite reutilizá-lo em outros contextos (ex.: script de linha de "
        "comando, Jupyter Notebook, outro framework web)."
    )
    pdf.P(
        "O processamento assíncrono é implementado via threading nativo do "
        "Python (threading.Thread com daemon=True): o endpoint POST /api/train "
        "cria a sessão no banco de dados, valida o caminho do dataset e "
        "dispara uma thread em background que executa o pipeline completo "
        "de ML. O thread principal (Flask) retorna imediatamente a confirmação "
        "ao frontend, que inicia o polling de progresso. Um dicionário em "
        "memória (training_progress) com lock threading.Lock() rastreia "
        "o estado de cada sessão ativa."
    )
