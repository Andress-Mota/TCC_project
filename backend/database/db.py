import mysql.connector
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import DB_CONFIG


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def init_db():
    cfg_no_db = {k: v for k, v in DB_CONFIG.items() if k != 'database'}
    conn = mysql.connector.connect(**cfg_no_db)
    cursor = conn.cursor()

    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        sql = f.read()

    for statement in sql.split(';'):
        stmt = statement.strip()
        if stmt:
            cursor.execute(stmt)

    conn.commit()
    cursor.close()
    conn.close()
    _migrate_db()


def _column_exists(cursor, table, column):
    cursor.execute("""
        SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND COLUMN_NAME = %s
    """, (DB_CONFIG['database'], table, column))
    return cursor.fetchone()[0] > 0


def _index_exists(cursor, table, index_name):
    cursor.execute("""
        SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND INDEX_NAME = %s
    """, (DB_CONFIG['database'], table, index_name))
    return cursor.fetchone()[0] > 0


def _migrate_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    migrations = [
        ('training_sessions', 'user_id',
         "ALTER TABLE training_sessions ADD COLUMN user_id INT DEFAULT NULL AFTER id"),
        ('training_sessions', 'name',
         "ALTER TABLE training_sessions ADD COLUMN name VARCHAR(200) DEFAULT NULL AFTER user_id"),
        ('predictions', 'feedback',
         "ALTER TABLE predictions ADD COLUMN feedback ENUM('correct','incorrect') DEFAULT NULL"),
        ('predictions', 'correct_class',
         "ALTER TABLE predictions ADD COLUMN correct_class VARCHAR(100) DEFAULT NULL"),
        ('predictions', 'hog_features',
         "ALTER TABLE predictions ADD COLUMN hog_features LONGTEXT DEFAULT NULL"),
        ('model_results', 'precision_score',
         "ALTER TABLE model_results ADD COLUMN precision_score FLOAT AFTER test_accuracy"),
        ('model_results', 'recall_score',
         "ALTER TABLE model_results ADD COLUMN recall_score FLOAT AFTER precision_score"),
        ('model_results', 'f1_score',
         "ALTER TABLE model_results ADD COLUMN f1_score FLOAT AFTER recall_score"),
        ('model_results', 'roc_auc',
         "ALTER TABLE model_results ADD COLUMN roc_auc FLOAT AFTER f1_score"),
        ('model_results', 'roc_data',
         "ALTER TABLE model_results ADD COLUMN roc_data LONGTEXT AFTER roc_auc"),
    ]

    for table, column, sql in migrations:
        if not _column_exists(cursor, table, column):
            cursor.execute(sql)
            print(f'[DB] Coluna adicionada: {table}.{column}')

    cursor.execute("""
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
        )
    """)

    indexes = [
        ('training_sessions', 'idx_ts_user_id',    "CREATE INDEX idx_ts_user_id ON training_sessions(user_id)"),
        ('predictions',       'idx_pred_session',   "CREATE INDEX idx_pred_session ON predictions(session_id)"),
        ('model_results',     'idx_mr_session',     "CREATE INDEX idx_mr_session ON model_results(session_id)"),
        ('error_logs',        'idx_el_user_id',     "CREATE INDEX idx_el_user_id ON error_logs(user_id)"),
    ]
    for table, idx_name, sql in indexes:
        if not _index_exists(cursor, table, idx_name):
            cursor.execute(sql)
            print(f'[DB] Índice criado: {table}.{idx_name}')

    conn.commit()
    cursor.close()
    conn.close()


def save_error(level, origin, message, traceback_text=None, session_id=None, user_id=None):
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(
            "INSERT INTO error_logs (level, origin, message, traceback, session_id, user_id) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (level, origin, message, traceback_text, session_id, user_id)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception:
        pass  # nunca deixar o logging de erros derrubar a aplicação
