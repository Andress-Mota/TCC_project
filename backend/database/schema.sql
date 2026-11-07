-- =============================================================
--  TCC — Classificação de Imagens com Ensemble Learning
--  Banco de dados: tcc_imagens
--
--  Como executar no MySQL Workbench:
--    1. File > Open SQL Script → selecione este arquivo
--    2. Clique em "Run SQL Script" (raio duplo ⚡⚡)
--    3. Charset: utf8mb4
-- =============================================================

CREATE DATABASE IF NOT EXISTS tcc_imagens
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE tcc_imagens;

-- ── USUÁRIOS ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    name                VARCHAR(100)  NOT NULL,
    email               TEXT          NOT NULL,
    email_hash          VARCHAR(64)   NOT NULL UNIQUE,
    password_hash       VARCHAR(255)  NOT NULL,
    email_verified      BOOLEAN       NOT NULL DEFAULT FALSE,
    verification_code   VARCHAR(10)   DEFAULT NULL,
    reset_token         VARCHAR(100)  DEFAULT NULL,
    reset_token_expires DATETIME      DEFAULT NULL,
    created_at          TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

-- ── SESSÕES DE TREINO ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS training_sessions (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    user_id      INT           DEFAULT NULL,
    name         VARCHAR(200)  DEFAULT NULL,
    dataset_path VARCHAR(500),
    status       ENUM('pending','training','completed','error','cancelled') DEFAULT 'pending',
    total_images INT           DEFAULT 0,
    classes      TEXT,
    created_at   TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- ── RESULTADOS DOS MODELOS ────────────────────────────────────
CREATE TABLE IF NOT EXISTS model_results (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    session_id      INT           NOT NULL,
    model_name      VARCHAR(100),
    model_type      ENUM('individual','ensemble'),
    cv_mean         FLOAT,
    cv_std          FLOAT,
    test_accuracy   FLOAT,
    precision_score FLOAT,
    recall_score    FLOAT,
    f1_score        FLOAT,
    roc_auc         FLOAT,
    roc_data        LONGTEXT,
    confusion_matrix TEXT,
    FOREIGN KEY (session_id) REFERENCES training_sessions(id) ON DELETE CASCADE
);

-- ── PREDIÇÕES ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS predictions (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    session_id      INT           NOT NULL,
    model_name      VARCHAR(100),
    image_name      VARCHAR(255),
    predicted_class VARCHAR(100),
    confidence      FLOAT,
    feedback        ENUM('correct','incorrect') DEFAULT NULL,
    correct_class   VARCHAR(100)  DEFAULT NULL,
    hog_features    LONGTEXT      DEFAULT NULL,
    created_at      TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES training_sessions(id) ON DELETE CASCADE
);

-- ── PREFERÊNCIAS DO USUÁRIO ───────────────────────────────────
CREATE TABLE IF NOT EXISTS preferences (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT     NOT NULL UNIQUE,
    theme_light BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ── LOGS DE ERRO DO SISTEMA ───────────────────────────────────
CREATE TABLE IF NOT EXISTS error_logs (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    level       ENUM('ERROR','WARNING','CRITICAL') NOT NULL DEFAULT 'ERROR',
    origin      VARCHAR(100)  NOT NULL DEFAULT 'sistema',
    message     TEXT          NOT NULL,
    traceback   LONGTEXT,
    session_id  INT           DEFAULT NULL,
    user_id     INT           DEFAULT NULL,
    created_at  TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES training_sessions(id) ON DELETE SET NULL,
    FOREIGN KEY (user_id)    REFERENCES users(id)             ON DELETE SET NULL
);
