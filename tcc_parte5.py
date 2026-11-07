#!/usr/bin/env python3
"""TCC FATEC-GT 2026 — Parte 5: Cap 3 banco de dados + API completa"""
from tcc_parte1 import PDF, ML, MR, MT, MB, PW, CW, SB, ST, SS, SC, LH, LT, LC, IND

def cap3_db(pdf):
    pdf.np()
    pdf.SUB("3.3  Banco de Dados MySQL")
    pdf.P(
        "O banco de dados utiliza MySQL 8.0+ com charset utf8mb4 (suporte a Unicode "
        "completo, incluindo emojis) e motor InnoDB, que oferece suporte completo a "
        "transações ACID, chaves estrangeiras com restrições de integridade "
        "referencial e índices secundários para otimização de consultas. O esquema "
        "é denominado 'tcc_imagens' e composto por seis tabelas relacionadas, "
        "conforme o Diagrama Entidade-Relacionamento da Figura 2."
    )
    pdf.SSUB("3.3.1  Tabela users")
    pdf.P(
        "Armazena os dados de autenticação e identificação dos usuários. "
        "O design de segurança desta tabela merece atenção especial:"
    )
    pdf.QUO(
        "CREATE TABLE users (\n"
        "  id                  INT AUTO_INCREMENT PRIMARY KEY,\n"
        "  name                VARCHAR(100) NOT NULL,\n"
        "  email               TEXT NOT NULL,           -- Criptografado (Fernet)\n"
        "  email_hash          VARCHAR(64) UNIQUE,      -- SHA-256 do email\n"
        "  password_hash       VARCHAR(255) NOT NULL,   -- bcrypt\n"
        "  email_verified      TINYINT(1) DEFAULT 0,\n"
        "  verification_code   VARCHAR(10),\n"
        "  verification_expiry DATETIME,\n"
        "  reset_token         VARCHAR(100),\n"
        "  reset_token_expires DATETIME,\n"
        "  created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n"
        ")"
    )
    pdf.P(
        "A separação entre email (criptografado com Fernet/AES-128) e email_hash "
        "(digest SHA-256) resolve o problema de busca em dados criptografados: "
        "o campo criptografado permite recuperar o email original (para exibição "
        "e envio de emails), enquanto o hash permite verificar se um email já "
        "está cadastrado (busca por unicidade) sem precisar descriptografar todos "
        "os registros. O índice UNIQUE sobre email_hash garante unicidade no "
        "nível do banco de dados."
    )
    pdf.P(
        "O verification_code armazena o código de 6 dígitos enviado por email "
        "para verificação de cadastro. O verification_expiry define a janela de "
        "validade (24 horas após envio). O reset_token é o token hexadecimal "
        "de 32 caracteres para redefinição de senha, com validade de 1 hora "
        "armazenada em reset_token_expires."
    )
    pdf.SSUB("3.3.2  Tabela training_sessions")
    pdf.QUO(
        "CREATE TABLE training_sessions (\n"
        "  id           INT AUTO_INCREMENT PRIMARY KEY,\n"
        "  user_id      INT,\n"
        "  name         VARCHAR(200),\n"
        "  dataset_path VARCHAR(500),\n"
        "  status       ENUM('pending','training','completed','error','cancelled')\n"
        "               DEFAULT 'pending',\n"
        "  total_images INT DEFAULT 0,\n"
        "  classes      TEXT,                           -- JSON array de classes\n"
        "  created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
        "  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,\n"
        "  INDEX idx_ts_user (user_id)\n"
        ")"
    )
    pdf.P(
        "O campo status usa ENUM com 5 valores que refletem o ciclo de vida "
        "completo de uma sessão: 'pending' (criada, aguardando início), "
        "'training' (pipeline em execução na thread), 'completed' (concluída "
        "com sucesso, resultados disponíveis), 'error' (falha durante o "
        "treinamento, detalhes em error_logs), 'cancelled' (cancelada pelo "
        "usuário antes da conclusão). ON DELETE SET NULL garante que a "
        "exclusão do usuário não delete as sessões — mantendo o histórico "
        "mesmo se o usuário for removido."
    )
    pdf.P(
        "O campo classes armazena a lista de classes em formato JSON "
        "(ex.: '[\"gato\",\"cachorro\",\"passaro\"]'), permitindo recuperar "
        "os nomes das classes para exibição nas predições sem necessidade de "
        "consulta ao sistema de arquivos."
    )
    pdf.SSUB("3.3.3  Tabela model_results")
    pdf.QUO(
        "CREATE TABLE model_results (\n"
        "  id              INT AUTO_INCREMENT PRIMARY KEY,\n"
        "  session_id      INT NOT NULL,\n"
        "  model_name      VARCHAR(100) NOT NULL,\n"
        "  model_type      ENUM('individual','ensemble') DEFAULT 'individual',\n"
        "  cv_mean         FLOAT,   -- Acuracia media na CV 10-fold\n"
        "  cv_std          FLOAT,   -- Desvio padrao na CV 10-fold\n"
        "  test_accuracy   FLOAT,   -- Acuracia no conjunto de teste\n"
        "  precision_score FLOAT,   -- Precisao (weighted)\n"
        "  recall_score    FLOAT,   -- Revocacao (weighted)\n"
        "  f1_score        FLOAT,   -- F1-Score (weighted)\n"
        "  roc_auc         FLOAT,   -- Area sob a curva ROC\n"
        "  roc_data        LONGTEXT,-- JSON: {fpr, tpr, auc} ou {classes, curves}\n"
        "  confusion_matrix TEXT,   -- JSON: matriz como lista de listas\n"
        "  FOREIGN KEY (session_id) REFERENCES training_sessions(id) ON DELETE CASCADE,\n"
        "  INDEX idx_mr_session (session_id)\n"
        ")"
    )
    pdf.P(
        "O campo roc_data armazena os dados da curva ROC em JSON para renderização "
        "dinâmica no frontend via Chart.js. Para classificação binária, o JSON "
        "contém: {fpr: [0,...,1], tpr: [0,...,1], auc: 0.9520}. Para multiclasse, "
        "contém uma lista de curvas (uma por classe, abordagem One-vs-Rest). "
        "O uso de LONGTEXT permite armazenar curvas com muitos pontos sem "
        "truncamento. ON DELETE CASCADE garante que ao excluir uma sessão, "
        "todos os seus resultados de modelos são automaticamente removidos."
    )
    pdf.SSUB("3.3.4  Tabela predictions")
    pdf.QUO(
        "CREATE TABLE predictions (\n"
        "  id              INT AUTO_INCREMENT PRIMARY KEY,\n"
        "  session_id      INT NOT NULL,\n"
        "  model_name      VARCHAR(100),\n"
        "  image_name      VARCHAR(255),\n"
        "  predicted_class VARCHAR(100),\n"
        "  confidence      FLOAT,         -- Probabilidade [0,1]\n"
        "  feedback        ENUM('none','correct','incorrect') DEFAULT 'none',\n"
        "  correct_class   VARCHAR(100),  -- Preenchido quando feedback='incorrect'\n"
        "  hog_features    LONGTEXT,      -- JSON: vetor HOG de 324 dimensoes\n"
        "  created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
        "  FOREIGN KEY (session_id) REFERENCES training_sessions(id) ON DELETE CASCADE,\n"
        "  INDEX idx_pred_session (session_id)\n"
        ")"
    )
    pdf.P(
        "O campo hog_features armazena o vetor HOG de 324 dimensões em JSON, "
        "possibilitando o reaprendizado ativo: quando o usuário marca uma "
        "predição como 'incorrect' e fornece a classe correta, o vetor HOG "
        "já extraído é reutilizado na sessão de retreinamento, evitando "
        "re-extração da imagem original (que pode não estar mais disponível "
        "no disco). O campo confidence armazena a probabilidade da classe "
        "predita no intervalo [0,1], exibida como porcentagem na interface."
    )
    pdf.SSUB("3.3.5  Tabelas preferences e error_logs")
    pdf.QUO(
        "CREATE TABLE preferences (\n"
        "  id          INT AUTO_INCREMENT PRIMARY KEY,\n"
        "  user_id     INT UNIQUE NOT NULL,\n"
        "  theme_light TINYINT(1) DEFAULT 0,  -- 0=escuro, 1=claro\n"
        "  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE\n"
        ");\n\n"
        "CREATE TABLE error_logs (\n"
        "  id         INT AUTO_INCREMENT PRIMARY KEY,\n"
        "  level      ENUM('ERROR','WARNING','CRITICAL') DEFAULT 'ERROR',\n"
        "  origin     VARCHAR(100),   -- 'treinamento','predicao','autenticacao',...\n"
        "  message    TEXT,\n"
        "  traceback  LONGTEXT,       -- Stack trace completo\n"
        "  session_id INT,\n"
        "  user_id    INT,\n"
        "  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
        "  FOREIGN KEY (session_id) REFERENCES training_sessions(id) ON DELETE SET NULL,\n"
        "  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,\n"
        "  INDEX idx_el_user_id (user_id)\n"
        ")"
    )
    pdf.P(
        "O campo origin categoriza a origem do erro em 6 domínios: 'treinamento' "
        "(erros no pipeline de ML), 'predicao' (erros na classificação de imagens), "
        "'autenticacao' (tentativas inválidas, falhas de verificação), 'perfil' "
        "(atualizações de dados do usuário), 'sistema' (erros gerais do servidor) "
        "e 'gradcam' (erros na geração de mapas de calor). O traceback completo "
        "em LONGTEXT permite diagnóstico preciso de falhas em produção."
    )

def cap3_api(pdf):
    pdf.np()
    pdf.SUB("3.4  Backend — API REST Flask")
    pdf.P(
        "O backend é implementado em Python com Flask, composto pelo arquivo "
        "principal backend/app.py (1.299 linhas), módulos auxiliares "
        "(config.py, crypto.py, mail.py) e o pacote backend/ml/. "
        "A API REST expõe mais de 30 endpoints organizados em 7 grupos "
        "funcionais, todos retornando JSON com código HTTP apropriado."
    )
    pdf.SSUB("3.4.1  Inicialização e Configuração")
    pdf.P(
        "A aplicação Flask é inicializada com CORS (Flask-CORS para permitir "
        "requisições do frontend no mesmo host), rate limiting (Flask-Limiter "
        "com backend em memória para desenvolvimento local), e sessões permanentes "
        "com lifetime de 24 horas. A chave secreta (SECRET_KEY) é lida de variável "
        "de ambiente e usada para assinar os cookies de sessão, tornando-os "
        "tamper-proof. Um tratador global de exceções (app.errorhandler(Exception)) "
        "captura qualquer erro não tratado, registra-o em error_logs e retorna "
        "resposta JSON estruturada com código HTTP 500."
    )
    pdf.SSUB("3.4.2  Grupo Autenticação (/api/auth/)")
    pdf.TABLE(
        "Tabela 3.1 – Endpoints de autenticação",
        ["Método","Rota","Comportamento","Código HTTP"],
        [
            ["POST","/api/auth/register","Valida senha (5 regras), verifica unicidade via email_hash, criptografa email, gera hash bcrypt, cria user, envia código 6 dígitos","201/400/409"],
            ["POST","/api/auth/login","Verifica email_hash, decripta email, compara bcrypt, inicia sessão. Rate limit: 10/min por IP","200/400/401/429"],
            ["POST","/api/auth/logout","Limpa session Flask","200"],
            ["POST","/api/auth/verify-email","Verifica código 6 dígitos e validade (24h). Marca email_verified=1","200/400/410"],
            ["POST","/api/auth/resend-verification","Gera novo código e reenvia email","200/400"],
            ["POST","/api/auth/forgot-password","Gera token 32-char hex (secrets.token_hex), define expiração 1h, envia email","200/404"],
            ["POST","/api/auth/reset-password","Valida token não expirado, valida nova senha, atualiza hash bcrypt","200/400/410"],
            ["POST","/api/auth/change-password","Requer autenticação. Verifica senha atual, valida nova","200/400/401"],
            ["GET","/api/auth/me","Retorna user_id, name, email_verified se sessão ativa","200/401"],
        ],
        cw=[16,46,72,26], fsz=8
    )
    pdf.SRC("Fonte: Elaborado pelo autor.")
    pdf.SSUB("3.4.3  Grupo Treinamento (/api/train, /api/sessions/)")
    pdf.TABLE(
        "Tabela 3.2 – Endpoints de treinamento e gerenciamento de sessões",
        ["Método","Rota","Descrição"],
        [
            ["POST","/api/train","Inicia treinamento assíncrono. Parâmetros: dataset_path, session_name (opt.), use_cnn (bool)"],
            ["GET","/api/sessions","Lista todas as sessões do usuário com status e datas"],
            ["GET","/api/sessions/{id}/status","Progresso em tempo real: etapa, porcentagem, status"],
            ["GET","/api/sessions/{id}/results","Métricas completas dos modelos treinados"],
            ["POST","/api/sessions/{id}/cancel","Sinaliza cancelamento da thread de treinamento"],
            ["POST","/api/sessions/{id}/delete","Remove sessão, modelos .pkl/.pt e predições do banco"],
            ["PUT","/api/sessions/{id}/name","Renomeia a sessão"],
            ["GET","/api/sessions/{id}/roc","Dados JSON da curva ROC para Chart.js"],
            ["GET","/api/sessions/{id}/export","Download CSV com 8 métricas por modelo"],
        ],
        cw=[16,46,98], fsz=8
    )
    pdf.SRC("Fonte: Elaborado pelo autor.")
    pdf.P(
        "O endpoint POST /api/train implementa o seguinte fluxo: (1) autentica "
        "o usuário via sessão; (2) valida que dataset_path existe e é um diretório "
        "com ao menos 2 subpastas; (3) cria registro em training_sessions com "
        "status='pending'; (4) inicia thread daemon: executa load_images_from_folder(), "
        "train_and_evaluate() e, opcionalmente, cnn_train(); (5) atualiza status "
        "para 'training', depois 'completed' ou 'error'; (6) persiste todos os "
        "resultados em model_results; (7) serializa modelos em "
        "backend/models/session_{id}.pkl e session_{id}_cnn.pt. "
        "O frontend realiza polling a cada 500ms no endpoint de status."
    )
    pdf.SSUB("3.4.4  Grupo Predição (/api/predict, /api/predictions/)")
    pdf.TABLE(
        "Tabela 3.3 – Endpoints de predição e feedback",
        ["Método","Rota","Descrição"],
        [
            ["POST","/api/predict","Upload de 1 ou N imagens. Extrai HOG, carrega .pkl, prediz. Armazena em predictions"],
            ["GET","/api/sessions/{id}/predictions","Histórico paginado. Params: page, per_page (default 50)"],
            ["POST","/api/predictions/{id}/feedback","Marca predição como correct/incorrect. Se incorrect: salva correct_class"],
            ["POST","/api/predictions/{id}/delete","Remove predição específica"],
            ["GET","/api/sessions/{id}/predictions/export","Download CSV do histórico completo de predições"],
            ["POST","/api/sessions/{id}/augment-train","Retreina com predições incorretas adicionadas ao dataset original"],
            ["POST","/api/gradcam","Gera mapa de calor Grad-CAM via CNN. Retorna imagem JPEG como bytes"],
        ],
        cw=[16,46,98], fsz=8
    )
    pdf.SRC("Fonte: Elaborado pelo autor.")
    pdf.P(
        "O endpoint POST /api/predict aceita imagens via multipart/form-data "
        "(campo 'images[]'). Para cada imagem: (1) salva temporariamente em "
        "backend/uploads/; (2) extrai vetor HOG via preprocess_single_image(); "
        "(3) carrega o modelo serializado da sessão selecionada; (4) chama "
        "model.predict() e model.predict_proba(); (5) obtém classe e confiança; "
        "(6) insere em predictions com hog_features serializado em JSON; "
        "(7) remove arquivo temporário. Para lote, retorna lista de resultados; "
        "para imagem única, retorna objeto com classe, confiança e modelo."
    )
    pdf.SSUB("3.4.5  Grupo Dashboard e Utilitários")
    pdf.TABLE(
        "Tabela 3.4 – Endpoints de dashboard e utilitários",
        ["Método","Rota","Descrição"],
        [
            ["GET","/api/dashboard","Estatísticas: total sessões, predições, melhor acurácia, melhor modelo, médias por algoritmo"],
            ["GET","/api/profile","Dados do usuário: name, email (decriptado), email_verified, created_at"],
            ["PUT","/api/profile","Atualiza name e/ou email (email change dispara reverificação)"],
            ["GET","/api/preferences","Retorna theme_light do usuário"],
            ["POST","/api/preferences","Atualiza preferência de tema"],
            ["GET","/api/error-logs","Logs paginados com filtros: level, origin, page"],
            ["POST","/api/error-logs/clear","Remove todos os logs do usuário"],
            ["DELETE","/api/error-logs/{id}","Remove log específico"],
            ["GET","/api/pick-folder","Abre diálogo de seleção de pasta (tkinter) no servidor"],
            ["GET","/api/pick-zip","Abre diálogo de arquivo e extrai ZIP/TAR para temp dir"],
        ],
        cw=[16,46,98], fsz=8
    )
    pdf.SRC("Fonte: Elaborado pelo autor.")
    pdf.P(
        "O endpoint GET /api/dashboard executa uma consulta SQL agrupada que calcula, "
        "por usuário autenticado: (1) contagem de sessões com status='completed'; "
        "(2) contagem total de predições em todas as sessões; (3) sessão com "
        "maior test_accuracy em model_results; (4) médias de test_accuracy "
        "agrupadas por model_name (para o gráfico de barras comparativo). "
        "Todos os dados são retornados em um único objeto JSON."
    )
    pdf.P(
        "Os endpoints GET /api/pick-folder e GET /api/pick-zip utilizam a "
        "biblioteca tkinter (incluída na distribuição padrão do Python) para "
        "abrir um diálogo nativo de seleção de arquivo/pasta no servidor local. "
        "Essa abordagem é viável porque o sistema roda localmente (servidor e "
        "cliente na mesma máquina). Para implantação em servidor remoto, essa "
        "funcionalidade seria substituída por upload direto de arquivo ou "
        "especificação de caminho relativo."
    )

def cap3_ml_module(pdf):
    pdf.np()
    pdf.SUB("3.5  Módulo de Machine Learning")
    pdf.P(
        "O módulo de ML (backend/ml/) é organizado em três arquivos Python com "
        "responsabilidades bem definidas, sem dependências do framework Flask:"
    )
    pdf.SSUB("3.5.1  preprocessor.py — Extração de Features")
    pdf.P(
        "Implementa três funções principais:"
    )
    pdf.TABLE(
        "Quadro 3.3 – Funções do módulo preprocessor.py",
        ["Função","Assinatura","Responsabilidade"],
        [
            ["extract_hog","(img_gray) -> np.array(324,)","Aplica HOG sobre imagem grayscale 128x128; retorna vetor de 324 features"],
            ["load_images_from_folder","(dataset_path) -> (X, y, classes)","Percorre subpastas, carrega imagens, extrai HOG; retorna arrays para treinamento"],
            ["preprocess_single_image","(img_path) -> np.array(1,324)","Pré-processa imagem única para inferência; retorna vetor reshaped"],
        ],
        cw=[40,60,60], fsz=9
    )
    pdf.SRC("Fonte: Elaborado pelo autor.")
    pdf.P(
        "As constantes globais definem os parâmetros do pipeline: "
        "IMG_SIZE=(128,128), SUPPORTED_EXTENSIONS={'.jpg','.jpeg','.png', "
        "'.bmp','.tiff','.tif','.webp'}. O logging registra o número de "
        "imagens carregadas por classe, arquivos ignorados e warnings para "
        "imagens corrompidas. Levanta ValueError se o dataset tiver menos "
        "de 2 classes ou se alguma classe não tiver imagens válidas."
    )
    pdf.SSUB("3.5.2  ensemble.py — Treinamento e Avaliação")
    pdf.P(
        "A função principal train_and_evaluate(X, y, optimize_k=True, callback=None) "
        "executa o pipeline completo de treinamento e avaliação:"
    )
    pdf.QUO(
        "def train_and_evaluate(X, y, optimize_k=True, callback=None):\n"
        "  # 1. Divisao estratificada\n"
        "  X_tr, X_te, y_tr, y_te = train_test_split(\n"
        "      X, y, test_size=0.2, stratify=y, random_state=42)\n\n"
        "  # 2. Melhor K para KNN\n"
        "  k = _find_best_k(X_tr, y_tr) if optimize_k else 14\n\n"
        "  # 3. Modelos base\n"
        "  knn, svm, rf, logreg, nb = _build_base_models(k)\n\n"
        "  # 4. Ensemble\n"
        "  hard = VotingClassifier([('knn',knn),('svm',svm),...], voting='hard')\n"
        "  soft = VotingClassifier([...], voting='soft')\n"
        "  stack = StackingClassifier([...], final_estimator=LogisticRegression())\n\n"
        "  # 5. Treinar e avaliar cada modelo\n"
        "  results = []\n"
        "  for name, model in all_models:\n"
        "      model.fit(X_tr, y_tr)\n"
        "      metrics = _evaluate(model, X_te, y_te, classes)\n"
        "      cv_scores = cross_val_score(model, X, y, cv=StratifiedKFold(10))\n"
        "      results.append({name: metrics, cv: cv_scores})\n"
        "  return results"
    )
    pdf.P(
        "A função auxiliar _find_best_k(X_train, y_train) realiza a busca do "
        "melhor K via GridSearchCV com KNeighborsClassifier, intervalo de busca "
        "{1,...,20}, StratifiedKFold(5), scoring='accuracy' e n_jobs=-1. "
        "Aplica StandardScaler internamente apenas para a busca de K (a "
        "normalização para o modelo final está encapsulada no Pipeline). "
        "A função _compute_roc(modelo, X_test, y_test, classes) calcula a "
        "curva ROC: para binário, usa roc_curve + auc; para multiclasse, "
        "usa label_binarize + roc_curve por classe (One-vs-Rest) com "
        "macro-average da AUC."
    )
    pdf.SSUB("3.5.3  Persistência dos Modelos")
    pdf.P(
        "Os modelos scikit-learn são serializados com pickle.dump() em "
        "backend/models/session_{id}.pkl. O arquivo contém um dicionário com "
        "chaves: 'models' (dicionário nome->Pipeline sklearn), 'classes' "
        "(lista de nomes de classes), 'k' (valor de K usado no KNN). "
        "Para predição, o arquivo é carregado com pickle.load() e o método "
        "predict()/predict_proba() é chamado sobre o vetor HOG da imagem "
        "a classificar."
    )
    pdf.P(
        "Os modelos EfficientNet-B0 são salvos com torch.save() em formato "
        ".pt, contendo state_dict (parâmetros do modelo) e classes. "
        "Para carregamento, o modelo base é recriado com a mesma arquitetura, "
        "os pesos são carregados com model.load_state_dict() e o modelo é "
        "colocado em modo de avaliação (model.eval()). O dispositivo "
        "(CPU/CUDA) é detectado automaticamente."
    )

def cap3_cnn_front(pdf):
    pdf.np()
    pdf.SUB("3.6  Módulo de Deep Learning: CNN e Grad-CAM")
    pdf.P(
        "O módulo cnn_model.py implementa a classe _GradCAM e as funções "
        "de treinamento e inferência da CNN EfficientNet-B0. A disponibilidade "
        "do PyTorch é verificada na inicialização do módulo: se não instalado, "
        "a CNN é desabilitada sem afetar os algoritmos clássicos."
    )
    pdf.SSUB("3.6.1  Pipeline de Treinamento CNN")
    pdf.P(
        "O treinamento CNN segue o seguinte pipeline:"
    )
    pdf.BULL([
        "Carregamento via ImageFolder: lê imagens diretamente das subpastas do "
        "dataset, aplicando transformações _TRANSFORM_TRAIN (treino) ou "
        "_TRANSFORM_VAL (validação);",
        "Divisão 80/20 via indices aleatórios com random_state=42: "
        "Subset(dataset, train_indices) e Subset(dataset, val_indices);",
        "DataLoader com batch_size=32 e shuffle=True para treino;",
        "EfficientNet-B0 com pesos ImageNet + substituição do classificador "
        "final por Linear(1280, n_classes);",
        "8 épocas de treinamento: forward pass, cálculo da CrossEntropyLoss, "
        "backward pass, atualização Adam+OneCycleLR;",
        "Avaliação no conjunto de validação ao final de cada época;",
        "Salvar state_dict com maior acurácia de validação (early stopping implícito).",
    ])
    pdf.SSUB("3.6.2  Implementação do Grad-CAM")
    pdf.P(
        "A classe _GradCAM registra hooks no módulo model.features[-1] "
        "(última camada de features do EfficientNet-B0) para capturar "
        "ativações e gradientes durante o forward/backward pass:"
    )
    pdf.QUO(
        "class _GradCAM:\n"
        "  def __init__(self, model):\n"
        "    target = model.features[-1]\n"
        "    self._fwd = target.register_forward_hook(self._save_act)\n"
        "    self._bwd = target.register_full_backward_hook(self._save_grad)\n\n"
        "  def generate(self, img_tensor):\n"
        "    out = self.model(img_tensor)\n"
        "    idx = out.argmax(1).item()     # classe predita\n"
        "    out[0, idx].backward()         # gradientes para a classe\n"
        "    w = self._grads.mean(dim=(2,3))  # peso de cada canal\n"
        "    cam = relu( (w*self._acts).sum(dim=1) )  # mapa de ativacao\n"
        "    cam = normalize(cam)          # 0-1\n"
        "    return cam, idx, confidence"
    )
    pdf.P(
        "O mapa de calor resultante é redimensionado para o tamanho original "
        "da imagem de entrada (cv2.resize), convertido para colormap JET "
        "(cv2.COLORMAP_JET) na escala 0-255, e sobreposto à imagem original "
        "com proporção 55% original + 45% heatmap (cv2.addWeighted). "
        "O resultado é codificado como JPEG (qualidade 88) e retornado como "
        "bytes para o frontend, que exibe via blob URL na tag <img>."
    )

    pdf.np()
    pdf.SUB("3.7  Frontend — Interface Web")
    pdf.P(
        "O frontend é implementado em HTML5, CSS3 e JavaScript puro (sem "
        "frameworks como React ou Vue.js), composto por 6 arquivos: "
        "index.html (780 linhas), auth.html (238 linhas), css/style.css, "
        "css/auth.css, js/main.js e js/auth.js. A interface suporta temas "
        "escuro (padrão) e claro, com alternância persistida no banco de dados."
    )
    pdf.SSUB("3.7.1  Dashboard")
    pdf.P(
        "A página Dashboard (page-dashboard) é a tela inicial após autenticação. "
        "Exibe quatro cartões de métricas no topo (total de sessões concluídas, "
        "total de predições realizadas, melhor acurácia obtida e nome do "
        "melhor modelo), seguidos de um gráfico de barras horizontais com a "
        "acurácia média de cada algoritmo em todas as sessões do usuário "
        "(renderizado via Chart.js, dados obtidos de GET /api/dashboard). "
        "Na parte inferior, duas tabelas menores exibem as 6 sessões mais "
        "recentes e as 6 predições mais recentes, com links diretos para "
        "as páginas correspondentes."
    )
    pdf.SSUB("3.7.2  Treinamento")
    pdf.P(
        "A página de treinamento (page-treinar) oferece: campo de texto para "
        "o caminho do dataset com botão 'Selecionar Pasta' (dispara "
        "GET /api/pick-folder) e botão 'Carregar ZIP' (dispara "
        "GET /api/pick-zip); campo opcional para nome da sessão; checkbox "
        "'Incluir CNN (EfficientNet-B0)' com aviso de tempo adicional; "
        "botão 'Iniciar Treinamento'. Após iniciar, uma barra de progresso "
        "animada exibe a etapa atual ('Carregando imagens...', 'Treinando KNN...', "
        "etc.) atualizada via polling a cada 500ms. Ao concluir, exibe "
        "notificação de sucesso com link direto para os resultados."
    )
    pdf.SSUB("3.7.3  Resultados")
    pdf.P(
        "A página de resultados (page-resultados) exibe a tabela comparativa "
        "com 8 colunas de métricas por modelo: CV Média ± Desvio, Acurácia "
        "Teste, Precisão, Revocação, F1-Score e AUC-ROC. Células com o "
        "valor máximo em cada coluna são destacadas com fundo colorido "
        "(accent #5B8CFF). O seletor de sessão no topo permite navegar "
        "entre sessões com botões de renomear (ícone lápis, dispara modal "
        "inline) e excluir (ícone lixeira, dispara confirmação). "
        "Abaixo da tabela: gráfico interativo da curva ROC (selecionável "
        "por modelo via dropdown), matriz de confusão como heatmap colorido "
        "(escala de cor proporcional à frequência de cada célula), e "
        "botão de exportação CSV."
    )
    pdf.SSUB("3.7.4  Teste de Imagens")
    pdf.P(
        "A página de teste (page-testar) é a mais rica funcionalmente. "
        "O usuário seleciona a sessão e o modelo a usar. A área de upload "
        "aceita arrastar-e-soltar (drag-and-drop via eventos dragover e drop) "
        "ou seleção de arquivo (input type=file, accept='.jpg,.png,...', "
        "multiple=true). Para imagem única: exibe miniatura, classe predita "
        "com ícone e cor por confiança, barra de confiança proporcional, "
        "dois botões de feedback (Correta/Incorreta). Para múltiplas imagens: "
        "tabela de resultados com miniatura, classe e confiança por imagem. "
        "Botão 'Ver Grad-CAM' aparece apenas quando a sessão inclui CNN treinada: "
        "dispara POST /api/gradcam e exibe o mapa de calor num modal. "
        "A seção 'Reaprendizado Ativo' ao final permite selecionar predições "
        "marcadas como incorretas e retreinar todos os modelos com esses "
        "exemplos adicionados."
    )
    pdf.SSUB("3.7.5  Histórico, Logs e Perfil")
    pdf.P(
        "A página de histórico (page-historico) exibe todas as predições da "
        "sessão selecionada em tabela paginada (default 50 por página), com "
        "colunas: miniatura da imagem, nome do arquivo, modelo utilizado, "
        "classe predita, confiança em porcentagem, indicador de feedback "
        "(badge colorido: verde=correta, vermelho=incorreta, cinza=sem feedback) "
        "e data/hora. O botão de exportação CSV baixa o histórico completo."
    )
    pdf.P(
        "A página de logs (page-logs) exibe eventos de sistema com filtros "
        "por nível (ERROR/WARNING/CRITICAL via dropdown) e por origem "
        "(dropdown com os 6 domínios). Cada entrada mostra: badge de nível "
        "colorido, origem, resumo da mensagem e timestamp. Clique em qualquer "
        "entrada abre modal com a mensagem completa e o stack trace. "
        "Botão 'Limpar Todos' remove todos os logs do usuário (com confirmação). "
        "A página de perfil exibe nome, email (com ícone de verificado/pendente), "
        "data de cadastro e dois botões de ação: 'Editar Dados' (formulário inline "
        "para nome e email — mudança de email dispara reverificação automática) "
        "e 'Alterar Senha' (modal com campos senha atual e nova senha)."
    )
    pdf.SSUB("3.7.6  Autenticação (auth.html)")
    pdf.P(
        "O arquivo auth.html implementa 5 views em uma única página (SPA simples), "
        "alternadas via JavaScript sem recarregar a página: (1) Login: campos "
        "email e senha, links para 'Criar conta' e 'Esqueci a senha'; "
        "(2) Registro: campos nome, email, senha e confirmar senha, com "
        "indicador de força de senha em tempo real (5 regras com ícones "
        "check/x); (3) Verificação de email: campo de 6 dígitos (com "
        "auto-focus e auto-avanço entre campos), botão 'Reenviar código'; "
        "(4) Esqueci a senha: campo email, botão 'Enviar link'; "
        "(5) Redefinir senha: campos token, nova senha e confirmação."
    )
