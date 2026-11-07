import os
import io
import csv
import json
import pickle
import tempfile
import threading
import secrets
import time
import logging
import traceback as tb_module
import numpy as np
from datetime import datetime, timedelta
from functools import wraps

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%H:%M:%S',
)
log = logging.getLogger('app')

from flask import Flask, request, jsonify, send_from_directory, session, Response
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException

from config import SECRET_KEY
from database.db import get_connection, init_db, save_error
from crypto import encrypt_email, decrypt_email, hash_email, validate_password
from mail import send_verification_email, send_reset_email, send_async
from ml.preprocessor import load_images_from_folder, preprocess_single_image
from ml.ensemble import train_and_evaluate, predict_image

try:
    from ml.cnn_model import train_cnn, save_cnn, gradcam_overlay
    _CNN_AVAILABLE = True
except ImportError:
    _CNN_AVAILABLE = False
    log.warning("torch/torchvision não instalado — CNN/Grad-CAM desabilitada")

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
app.secret_key = SECRET_KEY
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
CORS(app, supports_credentials=True,
     methods=['GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'])

ALLOWED_EXT = {'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'tif', 'webp'}

try:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    limiter = Limiter(app=app, key_func=get_remote_address,
                      default_limits=[], storage_uri="memory://")
    _limit_login = limiter.limit("10 per minute")
except Exception:
    def _limit_login(f): return f


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Não autenticado.'}), 401
        return f(*args, **kwargs)
    return decorated


def _log_error(origin, exc, session_id=None, user_id=None):
    tb_text = tb_module.format_exc()
    save_error('ERROR', origin, str(exc), tb_text, session_id=session_id, user_id=user_id)



@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'Arquivo muito grande. Limite máximo: 50 MB.'}), 413


@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return jsonify({'error': e.description}), e.code
    tb_text = tb_module.format_exc()
    try:
        uid = session.get('user_id')
    except Exception:
        uid = None
    save_error('ERROR', 'sistema', str(e), tb_text, user_id=uid)
    log.error(f"Erro nao tratado: {e}", exc_info=True)
    return jsonify({'error': 'Erro interno do servidor.'}), 500

@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/auth')
def auth_page():
    return send_from_directory(FRONTEND_DIR, 'auth.html')

BASE_DIR     = os.path.dirname(__file__)
MODEL_FOLDER = os.path.join(BASE_DIR, 'models')
os.makedirs(MODEL_FOLDER, exist_ok=True)

# progresso em memória: { session_id: {status, progress, message, _uid, _done_at} }
_status = {}


def _cleanup_status():
    while True:
        time.sleep(300)
        now = datetime.now().timestamp()
        stale = [k for k, v in list(_status.items())
                 if v.get('_done_at') and (now - v['_done_at']) > 300]
        for k in stale:
            _status.pop(k, None)

threading.Thread(target=_cleanup_status, daemon=True).start()


# ─── AUTENTICAÇÃO ─────────────────────────────────────────────────────────────

@app.route('/api/auth/register', methods=['POST'])
def register():
    data     = request.get_json()
    name     = (data.get('name')     or '').strip()
    email    = (data.get('email')    or '').strip().lower()
    password = (data.get('password') or '').strip()

    if not name or not email or not password:
        return jsonify({'error': 'Todos os campos são obrigatórios.'}), 400

    pwd_errors = validate_password(password)
    if pwd_errors:
        return jsonify({'error': pwd_errors[0], 'errors': pwd_errors}), 400

    e_hash    = hash_email(email)
    e_enc     = encrypt_email(email)
    pwd_hash  = generate_password_hash(password)
    v_code    = str(secrets.randbelow(900000) + 100000)

    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM users WHERE email_hash=%s", (e_hash,))
    if cur.fetchone():
        cur.close(); conn.close()
        return jsonify({'error': 'E-mail já cadastrado.'}), 409

    cur.execute(
        "INSERT INTO users (name, email, email_hash, password_hash, verification_code) "
        "VALUES (%s,%s,%s,%s,%s)",
        (name, e_enc, e_hash, pwd_hash, v_code)
    )
    conn.commit()
    user_id = cur.lastrowid
    cur.execute("INSERT INTO preferences (user_id, theme_light) VALUES (%s, TRUE)", (user_id,))
    conn.commit()
    cur.close(); conn.close()

    send_async(send_verification_email, email, v_code)

    return jsonify({
        'message': 'Cadastro realizado. Verifique seu e-mail.',
        'user_id': user_id,
        'name':    name,
    })


@app.route('/api/auth/resend-verification', methods=['POST'])
def resend_verification():
    data    = request.get_json()
    user_id = data.get('user_id')

    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cur.fetchone()

    if not user:
        cur.close(); conn.close()
        return jsonify({'error': 'Usuário não encontrado.'}), 404

    if user['email_verified']:
        cur.close(); conn.close()
        return jsonify({'error': 'E-mail já verificado.'}), 400

    v_code = str(secrets.randbelow(900000) + 100000)
    cur.execute("UPDATE users SET verification_code=%s WHERE id=%s", (v_code, user_id))
    conn.commit()
    cur.close(); conn.close()

    plain_email = decrypt_email(user['email'])
    send_async(send_verification_email, plain_email, v_code)
    return jsonify({'message': 'Código reenviado para seu e-mail.'})


@app.route('/api/auth/verify-email', methods=['POST'])
def verify_email():
    data    = request.get_json()
    user_id = data.get('user_id')
    code    = (data.get('code') or '').strip()

    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cur.fetchone()

    if not user or user['verification_code'] != code:
        cur.close(); conn.close()
        return jsonify({'error': 'Código inválido.'}), 400

    cur.execute("UPDATE users SET email_verified=TRUE, verification_code=NULL WHERE id=%s",
                (user_id,))
    conn.commit()
    cur.close(); conn.close()

    session['user_id'] = user_id
    session['name']    = user['name']
    return jsonify({'message': 'E-mail verificado com sucesso.', 'name': user['name']})


@app.route('/api/auth/login', methods=['POST'])
@_limit_login
def login():
    data     = request.get_json()
    email    = (data.get('email')    or '').strip().lower()
    password = (data.get('password') or '').strip()

    if not email or not password:
        return jsonify({'error': 'Informe e-mail e senha.'}), 400

    e_hash = hash_email(email)
    conn   = get_connection()
    cur    = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE email_hash=%s", (e_hash,))
    user = cur.fetchone()
    cur.close(); conn.close()

    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'E-mail ou senha incorretos.'}), 401

    if not user['email_verified']:
        return jsonify({'error': 'E-mail ainda não verificado.', 'unverified': True,
                        'user_id': user['id']}), 403

    session.permanent = True
    session['user_id'] = user['id']
    session['name']    = user['name']
    return jsonify({'message': 'Login realizado.', 'name': user['name']})


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout realizado.'})


@app.route('/api/auth/me', methods=['GET'])
def me():
    if 'user_id' not in session:
        return jsonify({'authenticated': False}), 200
    return jsonify({'authenticated': True, 'name': session.get('name')})


@app.route('/api/auth/forgot-password', methods=['POST'])
def forgot_password():
    data  = request.get_json()
    email = (data.get('email') or '').strip().lower()

    e_hash = hash_email(email)
    conn   = get_connection()
    cur    = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM users WHERE email_hash=%s", (e_hash,))
    user = cur.fetchone()

    if not user:
        cur.close(); conn.close()
        return jsonify({'error': 'E-mail não encontrado.'}), 404

    token   = secrets.token_hex(16)
    expires = datetime.now() + timedelta(hours=1)
    cur.execute("UPDATE users SET reset_token=%s, reset_token_expires=%s WHERE id=%s",
                (token, expires, user['id']))
    conn.commit()
    cur.close(); conn.close()

    send_async(send_reset_email, email, token)

    return jsonify({'message': 'Token enviado para seu e-mail.'})


@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    data     = request.get_json()
    token    = (data.get('token')        or '').strip()
    password = (data.get('new_password') or '').strip()

    if not token or not password:
        return jsonify({'error': 'Token e nova senha são obrigatórios.'}), 400

    pwd_errors = validate_password(password)
    if pwd_errors:
        return jsonify({'error': pwd_errors[0]}), 400

    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE reset_token=%s", (token,))
    user = cur.fetchone()

    if not user or not user['reset_token_expires'] or \
       datetime.now() > user['reset_token_expires']:
        cur.close(); conn.close()
        return jsonify({'error': 'Token inválido ou expirado.'}), 400

    pwd_hash = generate_password_hash(password)
    cur.execute("UPDATE users SET password_hash=%s, reset_token=NULL, reset_token_expires=NULL WHERE id=%s",
                (pwd_hash, user['id']))
    conn.commit()
    cur.close(); conn.close()
    return jsonify({'message': 'Senha redefinida com sucesso.'})


@app.route('/api/auth/change-password', methods=['POST'])
@login_required
def change_password():
    data        = request.get_json()
    current_pwd = (data.get('current_password') or '').strip()
    new_pwd     = (data.get('new_password')     or '').strip()

    if not current_pwd or not new_pwd:
        return jsonify({'error': 'Preencha todos os campos.'}), 400

    pwd_errors = validate_password(new_pwd)
    if pwd_errors:
        return jsonify({'error': pwd_errors[0]}), 400

    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE id=%s", (session['user_id'],))
    user = cur.fetchone()

    if not check_password_hash(user['password_hash'], current_pwd):
        cur.close(); conn.close()
        return jsonify({'error': 'Senha atual incorreta.'}), 401

    cur.execute("UPDATE users SET password_hash=%s WHERE id=%s",
                (generate_password_hash(new_pwd), user['id']))
    conn.commit()
    cur.close(); conn.close()
    return jsonify({'message': 'Senha alterada com sucesso.'})


# ─── PERFIL ────────────────────────────────────────────────────────────────────

@app.route('/api/profile', methods=['GET'])
@login_required
def get_profile():
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name, email, email_verified, created_at FROM users WHERE id=%s",
                (session['user_id'],))
    user = cur.fetchone()
    cur.close(); conn.close()

    if user:
        user['email']      = decrypt_email(user['email'])
        user['created_at'] = user['created_at'].isoformat()
    return jsonify(user)


@app.route('/api/profile', methods=['PUT'])
@login_required
def update_profile():
    data     = request.get_json()
    new_name = (data.get('name')  or '').strip()
    new_email= (data.get('email') or '').strip().lower()

    if not new_name:
        return jsonify({'error': 'Nome não pode ser vazio.'}), 400

    conn = get_connection()
    cur  = conn.cursor(dictionary=True)

    cur.execute("SELECT email_hash FROM users WHERE id=%s", (session['user_id'],))
    current = cur.fetchone()

    if new_email and hash_email(new_email) != current['email_hash']:
        new_hash = hash_email(new_email)
        cur.execute("SELECT id FROM users WHERE email_hash=%s AND id != %s",
                    (new_hash, session['user_id']))
        if cur.fetchone():
            cur.close(); conn.close()
            return jsonify({'error': 'E-mail já em uso.'}), 409

        v_code = str(secrets.randbelow(900000) + 100000)
        e_enc  = encrypt_email(new_email)
        cur.execute(
            "UPDATE users SET name=%s, email=%s, email_hash=%s, "
            "email_verified=FALSE, verification_code=%s WHERE id=%s",
            (new_name, e_enc, new_hash, v_code, session['user_id'])
        )
        conn.commit()
        cur.close(); conn.close()
        session['name'] = new_name
        send_async(send_verification_email, new_email, v_code)
        return jsonify({'message': 'Perfil atualizado. Verifique o novo e-mail.',
                        'user_id': session['user_id']})

    cur.execute("UPDATE users SET name=%s WHERE id=%s", (new_name, session['user_id']))
    conn.commit()
    cur.close(); conn.close()
    session['name'] = new_name
    return jsonify({'message': 'Perfil atualizado com sucesso.'})


# ─── DASHBOARD ────────────────────────────────────────────────────────────────

@app.route('/api/dashboard', methods=['GET'])
@login_required
def dashboard():
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)

    uid = session['user_id']

    cur.execute("SELECT COUNT(*) as total FROM training_sessions WHERE status='completed' AND user_id=%s", (uid,))
    total_sessions = cur.fetchone()['total']

    cur.execute("""
        SELECT COUNT(*) as total FROM predictions p
        JOIN training_sessions ts ON p.session_id = ts.id WHERE ts.user_id=%s
    """, (uid,))
    total_predictions = cur.fetchone()['total']

    cur.execute("""
        SELECT mr.model_name, mr.test_accuracy FROM model_results mr
        JOIN training_sessions ts ON mr.session_id = ts.id
        WHERE ts.user_id=%s ORDER BY mr.test_accuracy DESC LIMIT 1
    """, (uid,))
    best = cur.fetchone()

    cur.execute("""
        SELECT mr.model_name,
               ROUND(AVG(mr.cv_mean)        * 100, 2) AS avg_cv,
               ROUND(AVG(mr.test_accuracy)  * 100, 2) AS avg_acc,
               ROUND(AVG(mr.f1_score)       * 100, 2) AS avg_f1,
               COUNT(*) AS sessions
        FROM model_results mr
        JOIN training_sessions ts ON mr.session_id = ts.id
        WHERE ts.user_id=%s
        GROUP BY mr.model_name ORDER BY avg_cv DESC
    """, (uid,))
    model_averages = cur.fetchall()

    cur.execute("""
        SELECT id, name, status, total_images, created_at
        FROM training_sessions WHERE user_id=%s ORDER BY created_at DESC LIMIT 6
    """, (uid,))
    recent_sessions = cur.fetchall()
    for r in recent_sessions:
        if r.get('created_at'): r['created_at'] = r['created_at'].isoformat()

    cur.execute("""
        SELECT p.image_name, p.model_name, p.predicted_class, p.confidence, p.created_at
        FROM predictions p JOIN training_sessions ts ON p.session_id = ts.id
        WHERE ts.user_id=%s ORDER BY p.created_at DESC LIMIT 6
    """, (uid,))
    recent_preds = cur.fetchall()
    for r in recent_preds:
        if r.get('created_at'): r['created_at'] = r['created_at'].isoformat()

    cur.close(); conn.close()
    return jsonify({
        'total_sessions':    total_sessions,
        'total_predictions': total_predictions,
        'best_accuracy':     round(best['test_accuracy'] * 100, 2) if best else 0,
        'best_model':        best['model_name'] if best else '—',
        'model_averages':    model_averages,
        'recent_sessions':   recent_sessions,
        'recent_predictions': recent_preds,
    })


# ─── SELETOR DE PASTA / ARQUIVO COMPACTADO ─────────────────────────────────────

def _find_dataset_root(base):
    """Entra em subpastas únicas para ignorar o wrapper do arquivo compactado."""
    entries = os.listdir(base)
    if len(entries) == 1 and os.path.isdir(os.path.join(base, entries[0])):
        return _find_dataset_root(os.path.join(base, entries[0]))
    return base


def _get_classes(folder):
    """Retorna subpastas (classes) ordenadas de um diretório de dataset."""
    try:
        return sorted([
            e for e in os.listdir(folder)
            if os.path.isdir(os.path.join(folder, e)) and not e.startswith('.')
        ])
    except Exception:
        return []

@app.route('/api/pick-folder', methods=['GET'])
@login_required
def pick_folder():
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', True)
    folder = filedialog.askdirectory(title='Selecione a pasta do dataset')
    root.destroy()
    if not folder:
        return jsonify({'path': None})
    path = folder.replace('/', '\\')
    return jsonify({'path': path, 'classes': _get_classes(path)})

@app.route('/api/pick-zip', methods=['GET'])
@login_required
def pick_zip():
    import tkinter as tk
    from tkinter import filedialog, messagebox
    import zipfile, tarfile, tempfile

    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', True)
    filepath = filedialog.askopenfilename(
        title='Selecione o arquivo compactado do dataset',
        filetypes=[
            ('Compactados', '*.zip *.tar *.tar.gz *.tar.bz2 *.tgz'),
            ('ZIP', '*.zip'),
            ('TAR', '*.tar *.tar.gz *.tar.bz2 *.tgz'),
        ]
    )
    root.destroy()

    if not filepath:
        return jsonify({'path': None})

    extract_dir = tempfile.mkdtemp(prefix='tcc_dataset_')

    try:
        if zipfile.is_zipfile(filepath):
            with zipfile.ZipFile(filepath, 'r') as zf:
                zf.extractall(extract_dir)
        elif tarfile.is_tarfile(filepath):
            with tarfile.open(filepath) as tf:
                tf.extractall(extract_dir)
        else:
            return jsonify({'error': 'Formato não suportado. Use .zip ou .tar.gz'}), 400
    except Exception as e:
        return jsonify({'error': f'Erro ao extrair: {str(e)}'}), 500

    dataset_root = _find_dataset_root(extract_dir)
    path = dataset_root.replace('/', '\\')
    return jsonify({'path': path, 'classes': _get_classes(path), 'extracted': True})

# ─── TREINO ────────────────────────────────────────────────────────────────────

@app.route('/api/train', methods=['POST'])
@login_required
def train():
    data         = request.get_json()
    dataset_path = (data or {}).get('dataset_path', '').strip()
    name         = ((data or {}).get('name') or '').strip() or None
    train_cnn_flag = bool((data or {}).get('train_cnn', False)) and _CNN_AVAILABLE

    if not dataset_path or not os.path.isdir(dataset_path):
        return jsonify({'error': 'Caminho do dataset inválido ou inexistente.'}), 400

    conn   = get_connection()
    cur    = conn.cursor()
    user_id = session.get('user_id')
    cur.execute(
        "INSERT INTO training_sessions (user_id, name, dataset_path, status) VALUES (%s, %s, %s, 'pending')",
        (user_id, name, dataset_path)
    )
    conn.commit()
    session_id = cur.lastrowid
    cur.close()
    conn.close()

    _status[session_id] = {'status': 'pending', 'progress': 0, 'message': 'Aguardando início...', '_uid': user_id}

    t = threading.Thread(
        target=_run_training,
        args=(session_id, dataset_path, user_id),
        kwargs={'train_cnn_flag': train_cnn_flag},
        daemon=True
    )
    t.start()

    return jsonify({'session_id': session_id})


def _run_training(session_id, dataset_path, user_id=None, extra_X=None, extra_y=None, train_cnn_flag=False):
    conn = get_connection()
    cur  = conn.cursor()

    def update(pct, msg):
        if _status.get(session_id, {}).get('cancelled'):
            raise InterruptedError('Treinamento cancelado pelo usuário.')
        _status[session_id] = {'status': 'training', 'progress': pct, 'message': msg, '_uid': user_id}

    log.info(f"########## SESSAO {session_id} INICIADA ##########")
    log.info(f"Dataset: {dataset_path}")

    try:
        cur.execute("UPDATE training_sessions SET status='training' WHERE id=%s", (session_id,))
        conn.commit()
        update(5, 'Carregando imagens...')

        log.info("Etapa 1/4: Carregando imagens e extraindo features HOG")
        X, y, classes = load_images_from_folder(dataset_path)
        update(15, f'{len(X)} imagens carregadas. Extraindo features HOG...')
        log.info(f"Features prontas: shape={X.shape}")

        if extra_X is not None and len(extra_X) > 0:
            X = np.vstack([X, extra_X])
            y = np.append(y, extra_y)
            log.info(f"  +{len(extra_X)} amostras de feedback. Total: {len(X)}")
            update(18, f'{len(X)} amostras totais ({len(extra_X)} de feedback). Iniciando treino...')

        cur.execute(
            "UPDATE training_sessions SET total_images=%s, classes=%s WHERE id=%s",
            (len(X), json.dumps(classes), session_id)
        )
        conn.commit()

        if train_cnn_flag:
            log.info("Etapa 2/4: Treinando modelos sklearn (comprimido para 15-65%)")
            def _sklearn_cb(pct, msg):
                update(min(int(pct * 0.7), 65), msg)
            resultados, modelos, k = train_and_evaluate(X, y, callback=_sklearn_cb)
            update(65, 'Sklearn concluído. Iniciando CNN (EfficientNet-B0)...')

            log.info("Etapa CNN: Treinando EfficientNet-B0...")
            def _cnn_cb(pct, msg):
                update(65 + int(pct * 0.25), msg)  # 65-90%
            cnn_model_obj, cnn_acc = train_cnn(dataset_path, classes, callback=_cnn_cb, epochs=8)
            cnn_path = os.path.join(MODEL_FOLDER, f'session_{session_id}_cnn.pt')
            save_cnn(cnn_model_obj, classes, cnn_path)
            log.info(f"[CNN] Salva em {cnn_path} | val_acc={cnn_acc:.4f}")
            update(90, 'CNN concluída. Salvando resultados no banco...')
        else:
            log.info("Etapa 2/4: Treinando e avaliando modelos")
            resultados, modelos, k = train_and_evaluate(X, y, callback=update)
            update(92, 'Salvando resultados no banco...')

        log.info("Etapa 3/4: Salvando resultados no banco de dados")
        for nome, r in resultados.items():
            cur.execute(
                """INSERT INTO model_results
                   (session_id, model_name, cv_mean, cv_std, test_accuracy,
                    precision_score, recall_score, f1_score,
                    roc_auc, roc_data, model_type, confusion_matrix)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (session_id, nome, r['cv_mean'], r['cv_std'], r['acc_test'],
                 r['precision'], r['recall'], r['f1'],
                 r['roc_auc'], json.dumps(r['roc_data']) if r['roc_data'] else None,
                 r['model_type'], json.dumps(r['confusion_matrix']))
            )
        log.info(f"  {len(resultados)} modelos salvos no banco")

        log.info("Etapa 4/4: Salvando modelos treinados em disco")
        pkl_path = os.path.join(MODEL_FOLDER, f'session_{session_id}.pkl')
        with open(pkl_path, 'wb') as f:
            pickle.dump({'models': modelos, 'classes': classes, 'k': k}, f)
        log.info(f"  Modelos salvos em: {pkl_path}")

        cur.execute("UPDATE training_sessions SET status='completed' WHERE id=%s", (session_id,))
        conn.commit()

        _status[session_id] = {
            'status': 'completed', 'progress': 100,
            'message': 'Treinamento concluído com sucesso!',
            '_uid': user_id, '_done_at': datetime.now().timestamp()
        }
        log.info(f"########## SESSAO {session_id} CONCLUIDA COM SUCESSO ##########")

    except InterruptedError:
        log.warning(f"Sessao {session_id} cancelada pelo usuario")
        cur.execute("UPDATE training_sessions SET status='cancelled' WHERE id=%s", (session_id,))
        conn.commit()
        _status[session_id] = {'status': 'cancelled', 'progress': 0, 'message': 'Treinamento cancelado.', '_uid': user_id, '_done_at': datetime.now().timestamp()}
    except Exception as e:
        log.error(f"########## SESSAO {session_id} FALHOU ##########", exc_info=True)
        _log_error('treinamento', e, session_id=session_id, user_id=user_id)
        cur.execute("UPDATE training_sessions SET status='error' WHERE id=%s", (session_id,))
        conn.commit()
        _status[session_id] = {'status': 'error', 'progress': 0, 'message': str(e), '_uid': user_id, '_done_at': datetime.now().timestamp()}
    finally:
        cur.close()
        conn.close()


# ─── STATUS / SESSÕES ──────────────────────────────────────────────────────────

@app.route('/api/status/<int:session_id>', methods=['GET'])
@login_required
def get_status(session_id):
    st = _status.get(session_id)
    if st and st.get('_uid') is not None and st['_uid'] != session['user_id']:
        return jsonify({'error': 'Sem permissão.'}), 403
    return jsonify(st or {'status': 'unknown', 'progress': 0})

@app.route('/api/sessions/<int:session_id>/cancel', methods=['POST'])
@login_required
def cancel_training(session_id):
    st = _status.get(session_id)
    if st and st.get('_uid') is not None and st['_uid'] != session['user_id']:
        return jsonify({'error': 'Sem permissão.'}), 403
    if session_id in _status:
        _status[session_id]['cancelled'] = True
    return jsonify({'ok': True})


@app.route('/api/sessions', methods=['GET'])
@login_required
def get_sessions():
    user_id = session['user_id']
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM training_sessions WHERE user_id=%s ORDER BY created_at DESC",
        (user_id,)
    )
    rows = cur.fetchall()
    cur.close(); conn.close()
    for r in rows:
        if r.get('created_at'):
            r['created_at'] = r['created_at'].isoformat()
        cnn_path = os.path.join(MODEL_FOLDER, f'session_{r["id"]}_cnn.pt')
        r['has_cnn'] = os.path.exists(cnn_path)
    return jsonify(rows)


@app.route('/api/sessions/<int:session_id>/results', methods=['GET'])
@login_required
def get_results(session_id):
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM training_sessions WHERE id=%s AND user_id=%s",
                (session_id, session['user_id']))
    sess = cur.fetchone()
    if not sess:
        cur.close(); conn.close()
        return jsonify({'error': 'Sessão não encontrada.'}), 404
    cur.execute("SELECT * FROM model_results WHERE session_id=%s ORDER BY cv_mean DESC",
                (session_id,))
    results = cur.fetchall()
    cur.close()
    conn.close()

    if sess.get('created_at'):
        sess['created_at'] = sess['created_at'].isoformat()
    if sess.get('classes'):
        sess['classes'] = json.loads(sess['classes'])

    for r in results:
        if r.get('confusion_matrix'):
            r['confusion_matrix'] = json.loads(r['confusion_matrix'])

    return jsonify({'session': sess, 'results': results})


@app.route('/api/sessions/<int:session_id>/export', methods=['GET'])
@login_required
def export_results(session_id):
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT user_id FROM training_sessions WHERE id=%s", (session_id,))
    row = cur.fetchone()
    if not row or row['user_id'] != session['user_id']:
        cur.close(); conn.close()
        return jsonify({'error': 'Sem permissão.'}), 403
    cur.execute("SELECT * FROM model_results WHERE session_id=%s ORDER BY cv_mean DESC",
                (session_id,))
    results = cur.fetchall()
    cur.close(); conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Modelo', 'Tipo', 'CV Mean (%)', 'CV Std (%)', 'Acurácia Teste (%)',
                     'Precisão (%)', 'Recall (%)', 'F1-Score (%)', 'ROC AUC'])
    for r in results:
        writer.writerow([
            r['model_name'], r['model_type'],
            round((r['cv_mean']         or 0) * 100, 2),
            round((r['cv_std']          or 0) * 100, 2),
            round((r['test_accuracy']   or 0) * 100, 2),
            round((r['precision_score'] or 0) * 100, 2),
            round((r['recall_score']    or 0) * 100, 2),
            round((r['f1_score']        or 0) * 100, 2),
            round( r['roc_auc']         or 0,        4),
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename=sessao_{session_id}_resultados.csv'}
    )


@app.route('/api/sessions/<int:session_id>/roc', methods=['GET'])
@login_required
def get_roc(session_id):
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT user_id FROM training_sessions WHERE id=%s", (session_id,))
    row = cur.fetchone()
    if not row or row['user_id'] != session['user_id']:
        cur.close(); conn.close()
        return jsonify({'error': 'Sem permissão.'}), 403
    cur.execute(
        "SELECT model_name, roc_auc, roc_data FROM model_results WHERE session_id=%s",
        (session_id,)
    )
    rows = cur.fetchall()
    cur.close(); conn.close()
    for r in rows:
        r['roc_data'] = json.loads(r['roc_data']) if r.get('roc_data') else None
    return jsonify(rows)


# ─── PREDIÇÃO ──────────────────────────────────────────────────────────────────

@app.route('/api/predict', methods=['POST'])
@login_required
def predict():
    images = request.files.getlist('image')
    if not images or all(img.filename == '' for img in images):
        return jsonify({'error': 'Nenhuma imagem enviada.'}), 400

    session_id = request.form.get('session_id')
    model_name = request.form.get('model_name', 'Stacking')

    if not session_id:
        return jsonify({'error': 'session_id é obrigatório.'}), 400

    pkl_path = os.path.join(MODEL_FOLDER, f'session_{session_id}.pkl')
    if not os.path.exists(pkl_path):
        return jsonify({'error': 'Modelo não encontrado. Treine primeiro.'}), 404

    with open(pkl_path, 'rb') as f:
        data = pickle.load(f)

    modelos = data['models']
    classes = data['classes']

    if model_name not in modelos:
        return jsonify({'error': f'Modelo "{model_name}" não encontrado.'}), 400

    results = []
    conn = get_connection()
    cur  = conn.cursor()

    try:
        for image in images:
            if image.filename == '':
                continue
            ext = os.path.splitext(image.filename)[1].lstrip('.').lower()
            if ext not in ALLOWED_EXT:
                return jsonify({'error': f'Formato não suportado: .{ext}. Use: {", ".join(sorted(ALLOWED_EXT))}.'}), 400
            suffix = '.' + ext
            tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
            image.save(tmp.name)
            tmp.close()
            try:
                features             = preprocess_single_image(tmp.name)
                pred_idx, confidence = predict_image(modelos[model_name], features)
                predicted_class      = classes[pred_idx]
                cur.execute(
                    "INSERT INTO predictions "
                    "(session_id, model_name, image_name, predicted_class, confidence, hog_features) "
                    "VALUES (%s,%s,%s,%s,%s,%s)",
                    (session_id, model_name, image.filename, predicted_class, confidence,
                     json.dumps(features[0].tolist()))
                )
                results.append({
                    'image':           image.filename,
                    'predicted_class': predicted_class,
                    'confidence':      round(confidence * 100, 2),
                    'model':           model_name,
                    'prediction_id':   cur.lastrowid,
                })
            finally:
                os.unlink(tmp.name)

        conn.commit()
    except Exception as e:
        conn.rollback()
        _log_error('predicao', e, user_id=session.get('user_id'))
        return jsonify({'error': f'Erro ao processar imagem: {str(e)}'}), 500
    finally:
        cur.close(); conn.close()

    if len(results) == 1:
        return jsonify({**results[0], 'classes': classes})
    return jsonify({'batch': True, 'results': results, 'classes': classes})


# ─── PREFERÊNCIAS ─────────────────────────────────────────────────────────────

@app.route('/api/preferences', methods=['GET'])
@login_required
def get_preferences():
    user_id = session['user_id']
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM preferences WHERE user_id=%s", (user_id,))
    row = cur.fetchone()
    cur.close(); conn.close()
    return jsonify({'theme_light': bool(row['theme_light']) if row else True})


@app.route('/api/preferences', methods=['POST'])
@login_required
def set_preferences():
    data        = request.get_json()
    theme_light = bool(data.get('theme_light', True))
    user_id     = session['user_id']

    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("SELECT id FROM preferences WHERE user_id=%s", (user_id,))
    row = cur.fetchone()

    if row:
        cur.execute("UPDATE preferences SET theme_light=%s WHERE user_id=%s",
                    (theme_light, user_id))
    else:
        cur.execute("INSERT INTO preferences (user_id, theme_light) VALUES (%s,%s)",
                    (user_id, theme_light))

    conn.commit()
    cur.close(); conn.close()
    return jsonify({'theme_light': theme_light})


# ─── HISTÓRICO DE PREDIÇÕES ────────────────────────────────────────────────────

@app.route('/api/sessions/<int:session_id>/predictions', methods=['GET'])
@login_required
def get_predictions(session_id):
    page     = max(1, int(request.args.get('page', 1)))
    per_page = min(100, max(1, int(request.args.get('per_page', 50))))
    offset   = (page - 1) * per_page

    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT user_id FROM training_sessions WHERE id=%s", (session_id,))
    row = cur.fetchone()
    if not row or row['user_id'] != session['user_id']:
        cur.close(); conn.close()
        return jsonify({'error': 'Sem permissão.'}), 403
    cur.execute("SELECT COUNT(*) as total FROM predictions WHERE session_id=%s", (session_id,))
    total = cur.fetchone()['total']
    cur.execute(
        "SELECT id, session_id, model_name, image_name, predicted_class, confidence, "
        "feedback, correct_class, created_at "
        "FROM predictions WHERE session_id=%s ORDER BY created_at DESC LIMIT %s OFFSET %s",
        (session_id, per_page, offset)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    for r in rows:
        if r.get('created_at'):
            r['created_at'] = r['created_at'].isoformat()
    return jsonify({'predictions': rows, 'total': total, 'page': page, 'per_page': per_page})


# ─── FEEDBACK DE PREDIÇÃO ─────────────────────────────────────────────────────

@app.route('/api/predictions/<int:pred_id>/feedback', methods=['POST'])
@login_required
def prediction_feedback(pred_id):
    data          = request.get_json()
    feedback      = data.get('feedback')
    correct_class = (data.get('correct_class') or '').strip() or None

    if feedback not in ('correct', 'incorrect'):
        return jsonify({'error': 'feedback deve ser "correct" ou "incorrect".'}), 400
    if feedback == 'incorrect' and not correct_class:
        return jsonify({'error': 'correct_class é obrigatório quando feedback="incorrect".'}), 400

    conn = get_connection()
    cur  = conn.cursor()
    cur.execute(
        "UPDATE predictions SET feedback=%s, correct_class=%s WHERE id=%s",
        (feedback, correct_class, pred_id)
    )
    conn.commit()
    cur.close(); conn.close()
    return jsonify({'ok': True})


@app.route('/api/sessions/<int:session_id>/augment-train', methods=['POST'])
@login_required
def augment_train(session_id):
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM training_sessions WHERE id=%s AND user_id=%s",
                (session_id, session['user_id']))
    sess = cur.fetchone()
    if not sess:
        cur.close(); conn.close()
        return jsonify({'error': 'Sessão não encontrada.'}), 404

    cur.execute(
        "SELECT hog_features, correct_class FROM predictions "
        "WHERE session_id=%s AND feedback='incorrect' "
        "AND hog_features IS NOT NULL AND correct_class IS NOT NULL "
        "ORDER BY created_at DESC LIMIT 500",
        (session_id,)
    )
    feedback_rows = cur.fetchall()
    cur.close(); conn.close()

    if not feedback_rows:
        return jsonify({'error': 'Nenhum feedback de erro registrado para esta sessão.'}), 400

    classes = json.loads(sess['classes']) if sess.get('classes') else []
    extra_X, extra_y = [], []
    for row in feedback_rows:
        try:
            label = classes.index(row['correct_class'])
            extra_X.append(np.array(json.loads(row['hog_features'])))
            extra_y.append(label)
        except (ValueError, Exception):
            pass

    if not extra_X:
        return jsonify({'error': 'Nenhuma amostra de feedback válida (classes não reconhecidas).'}), 400

    data_req = request.get_json() or {}
    name     = (data_req.get('name') or '').strip() or \
               f"Sessão #{session_id} + {len(extra_X)} feedback(s)"
    uid      = session.get('user_id')

    conn = get_connection()
    cur  = conn.cursor()
    cur.execute(
        "INSERT INTO training_sessions (user_id, name, dataset_path, status) VALUES (%s,%s,%s,'pending')",
        (uid, name, sess['dataset_path'])
    )
    conn.commit()
    new_sid = cur.lastrowid
    cur.close(); conn.close()

    _status[new_sid] = {'status': 'pending', 'progress': 0, 'message': 'Aguardando início...', '_uid': uid}

    t = threading.Thread(
        target=_run_training,
        args=(new_sid, sess['dataset_path'], uid),
        kwargs={'extra_X': np.vstack(extra_X), 'extra_y': np.array(extra_y)},
        daemon=True
    )
    t.start()
    return jsonify({'session_id': new_sid})


# ─── RENOMEAR SESSÃO ──────────────────────────────────────────────────────────

@app.route('/api/sessions/<int:session_id>/name', methods=['PUT'])
@login_required
def rename_session(session_id):
    data = request.get_json()
    name = (data.get('name') or '').strip() or None

    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT user_id FROM training_sessions WHERE id=%s", (session_id,))
    row = cur.fetchone()
    if not row:
        cur.close(); conn.close()
        return jsonify({'error': 'Sessão não encontrada.'}), 404
    if row['user_id'] != session['user_id']:
        cur.close(); conn.close()
        return jsonify({'error': 'Sem permissão.'}), 403

    cur.execute("UPDATE training_sessions SET name=%s WHERE id=%s", (name, session_id))
    conn.commit()
    cur.close(); conn.close()
    return jsonify({'ok': True, 'name': name})


# ─── LOGS DE ERRO ─────────────────────────────────────────────────────────────

@app.route('/api/error-logs', methods=['GET'])
@login_required
def get_error_logs():
    page     = max(1, int(request.args.get('page',     1)))
    per_page = min(100, max(1, int(request.args.get('per_page', 20))))
    level    = request.args.get('level',  '').strip().upper()
    origin   = request.args.get('origin', '').strip()

    uid = session['user_id']
    where_clauses = ["(user_id = %s OR user_id IS NULL)"]
    params        = [uid]
    if level:
        where_clauses.append("level = %s");  params.append(level)
    if origin:
        where_clauses.append("origin = %s"); params.append(origin)
    where = "WHERE " + " AND ".join(where_clauses)

    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute(f"SELECT COUNT(*) as total FROM error_logs {where}", params)
    total = cur.fetchone()['total']
    cur.execute(
        f"SELECT id, level, origin, message, traceback, session_id, user_id, created_at "
        f"FROM error_logs {where} ORDER BY created_at DESC LIMIT %s OFFSET %s",
        params + [per_page, (page - 1) * per_page]
    )
    logs = cur.fetchall()
    cur.close(); conn.close()
    for l in logs:
        if l.get('created_at'):
            l['created_at'] = l['created_at'].isoformat()
    return jsonify({'logs': logs, 'total': total, 'page': page, 'per_page': per_page})


@app.route('/api/error-logs/clear', methods=['POST'])
@login_required
def clear_error_logs():
    uid = session['user_id']
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("DELETE FROM error_logs WHERE user_id = %s OR user_id IS NULL", (uid,))
    conn.commit()
    cur.close(); conn.close()
    return jsonify({'ok': True})


@app.route('/api/error-logs/<int:log_id>', methods=['DELETE'])
@login_required
def delete_error_log(log_id):
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("DELETE FROM error_logs WHERE id = %s", (log_id,))
    conn.commit()
    cur.close(); conn.close()
    return jsonify({'ok': True})


# ─── GRAD-CAM ─────────────────────────────────────────────────────────────────

@app.route('/api/gradcam', methods=['POST'])
@login_required
def get_gradcam():
    import base64

    session_id = request.form.get('session_id')
    img_file   = request.files.get('image')

    if not session_id or not img_file:
        return jsonify({'error': 'session_id e image são obrigatórios.'}), 400

    if not _CNN_AVAILABLE:
        return jsonify({'error': 'CNN não disponível (torch não instalado).'}), 503

    cnn_path = os.path.join(MODEL_FOLDER, f'session_{session_id}_cnn.pt')
    if not os.path.exists(cnn_path):
        return jsonify({'error': 'CNN não treinada para esta sessão.'}), 404

    pkl_path = os.path.join(MODEL_FOLDER, f'session_{session_id}.pkl')
    if not os.path.exists(pkl_path):
        return jsonify({'error': 'Modelo não encontrado.'}), 404

    with open(pkl_path, 'rb') as f:
        data = pickle.load(f)
    classes = data['classes']

    try:
        img_bytes  = img_file.read()
        pred_class, conf, jpeg_bytes = gradcam_overlay(cnn_path, img_bytes, classes)
        b64 = base64.b64encode(jpeg_bytes).decode('utf-8')
        return jsonify({
            'pred_class': pred_class,
            'confidence': round(conf * 100, 2),
            'image_b64':  b64,
        })
    except Exception as e:
        _log_error('gradcam', e, user_id=session.get('user_id'))
        return jsonify({'error': f'Erro ao gerar Grad-CAM: {str(e)}'}), 500


# ─── DELETE SESSÃO ────────────────────────────────────────────────────────────

@app.route('/api/sessions/<int:session_id>/delete', methods=['POST'])
@login_required
def delete_session(session_id):
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT user_id FROM training_sessions WHERE id=%s", (session_id,))
    row = cur.fetchone()
    if not row:
        cur.close(); conn.close()
        return jsonify({'error': 'Sessão não encontrada.'}), 404
    if row['user_id'] != session['user_id']:
        cur.close(); conn.close()
        return jsonify({'error': 'Sem permissão.'}), 403

    cur.execute("DELETE FROM predictions WHERE session_id=%s", (session_id,))
    cur.execute("DELETE FROM model_results WHERE session_id=%s", (session_id,))
    cur.execute("DELETE FROM training_sessions WHERE id=%s", (session_id,))
    conn.commit()
    cur.close(); conn.close()

    for fname in [f'session_{session_id}.pkl', f'session_{session_id}_cnn.pt']:
        fpath = os.path.join(MODEL_FOLDER, fname)
        if os.path.exists(fpath):
            try: os.remove(fpath)
            except Exception: pass

    _status.pop(session_id, None)
    return jsonify({'ok': True})


# ─── DELETE PREDIÇÃO ───────────────────────────────────────────────────────────

@app.route('/api/predictions/<int:pred_id>/delete', methods=['POST'])
@login_required
def delete_prediction(pred_id):
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT p.id FROM predictions p "
        "JOIN training_sessions ts ON p.session_id = ts.id "
        "WHERE p.id=%s AND ts.user_id=%s",
        (pred_id, session['user_id'])
    )
    row = cur.fetchone()
    if not row:
        cur.close(); conn.close()
        return jsonify({'error': 'Predição não encontrada ou sem permissão.'}), 404
    cur.execute("DELETE FROM predictions WHERE id=%s", (pred_id,))
    conn.commit()
    cur.close(); conn.close()
    return jsonify({'ok': True})


# ─── EXPORT PREDIÇÕES CSV ──────────────────────────────────────────────────────

@app.route('/api/sessions/<int:session_id>/predictions/export', methods=['GET'])
@login_required
def export_predictions(session_id):
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT user_id FROM training_sessions WHERE id=%s", (session_id,))
    row = cur.fetchone()
    if not row or row['user_id'] != session['user_id']:
        cur.close(); conn.close()
        return jsonify({'error': 'Sem permissão.'}), 403
    cur.execute(
        "SELECT image_name, model_name, predicted_class, confidence, feedback, correct_class, created_at "
        "FROM predictions WHERE session_id=%s ORDER BY created_at DESC",
        (session_id,)
    )
    rows = cur.fetchall()
    cur.close(); conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Imagem', 'Modelo', 'Classe Predita', 'Confiança (%)',
                     'Feedback', 'Classe Correta', 'Data/Hora'])
    for r in rows:
        writer.writerow([
            r['image_name'], r['model_name'], r['predicted_class'],
            round((r['confidence'] or 0) * 100, 2),
            r['feedback'] or '—', r['correct_class'] or '—',
            r['created_at'].strftime('%d/%m/%Y %H:%M') if r['created_at'] else '—',
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename=sessao_{session_id}_predicoes.csv'}
    )


# ─── INICIO ────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    print('[servidor] Rodando em http://localhost:5000 — Ctrl+C para parar')
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
