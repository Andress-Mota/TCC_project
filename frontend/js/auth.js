const API = 'http://localhost:5000/api';

let _pendingUserId = null;

// ── NAVEGAÇÃO ──────────────────────────────────────────────────────────────────

function goView(id) {
  document.querySelectorAll('.auth-view').forEach(v => v.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  clearMessages();
}

function clearMessages() {
  document.querySelectorAll('.msg-error, .msg-success').forEach(el => {
    el.classList.add('hidden');
    el.textContent = '';
  });
  const tb = document.getElementById('forgot-token-box');
  if (tb) tb.classList.add('hidden');
  const btForgot = document.getElementById('btn-forgot');
  if (btForgot) btForgot.classList.remove('hidden');
}

function showError(id, msg)   { const el = document.getElementById(id); el.textContent = msg; el.classList.remove('hidden'); }
function showSuccess(id, msg) { const el = document.getElementById(id); el.textContent = msg; el.classList.remove('hidden'); }

// ── MOSTRAR/OCULTAR SENHA ──────────────────────────────────────────────────────

function toggleEye(inputId, btn) {
  const input = document.getElementById(inputId);
  const isPass = input.type === 'password';
  input.type = isPass ? 'text' : 'password';
  btn.querySelector('i').className = isPass ? 'bi bi-eye-slash-fill' : 'bi bi-eye-fill';
}

// ── FORÇA DA SENHA ─────────────────────────────────────────────────────────────

const RULES = [
  { id: 'rule-len',   pattern: /.{8,}/,        label: 'Mínimo 8 caracteres' },
  { id: 'rule-upper', pattern: /[A-Z]/,         label: 'Uma maiúscula' },
  { id: 'rule-lower', pattern: /[a-z]/,         label: 'Uma minúscula' },
  { id: 'rule-num',   pattern: /\d/,            label: 'Um número' },
  { id: 'rule-spec',  pattern: /[^A-Za-z0-9]/, label: 'Um caractere especial' },
];

document.getElementById('reg-password').addEventListener('input', function () {
  const val    = this.value;
  let   passed = 0;

  RULES.forEach(rule => {
    const ok = rule.pattern.test(val);
    const li = document.getElementById(rule.id);
    li.classList.toggle('ok', ok);
    li.querySelector('i').className = ok ? 'bi bi-check-circle-fill' : 'bi bi-x-circle-fill';
    if (ok) passed++;
  });

  const pct    = (passed / RULES.length) * 100;
  const fill   = document.getElementById('strength-fill');
  fill.style.width = pct + '%';
  fill.style.background = pct <= 20  ? '#FF7A59'
                        : pct <= 60  ? '#D9B66B'
                        :              '#39C6B4';
});

// ── LOGIN ──────────────────────────────────────────────────────────────────────

document.getElementById('btn-login').addEventListener('click', async () => {
  const email    = document.getElementById('login-email').value.trim();
  const password = document.getElementById('login-password').value;

  if (!email || !password) { showError('login-error', 'Preencha e-mail e senha.'); return; }

  const btn = document.getElementById('btn-login');
  btn.disabled = true;
  try {
    const res  = await fetch(`${API}/auth/login`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      credentials: 'include', body: JSON.stringify({ email, password }),
    });
    const data = await res.json();

    if (res.status === 403 && data.unverified) {
      _pendingUserId = data.user_id;
      goView('view-verify');
      return;
    }
    if (!res.ok) { showError('login-error', data.error); return; }
    window.location.href = '/';
  } catch { showError('login-error', 'Erro ao conectar com o servidor.'); }
  finally  { btn.disabled = false; }
});

// ── CADASTRO ───────────────────────────────────────────────────────────────────

document.getElementById('btn-register').addEventListener('click', async () => {
  const name     = document.getElementById('reg-name').value.trim();
  const email    = document.getElementById('reg-email').value.trim();
  const password = document.getElementById('reg-password').value;
  const confirm  = document.getElementById('reg-confirm').value;

  if (!name || !email || !password || !confirm) {
    showError('reg-error', 'Preencha todos os campos.'); return;
  }
  if (password !== confirm) {
    showError('reg-error', 'As senhas não coincidem.'); return;
  }
  const failedRule = RULES.find(r => !r.pattern.test(password));
  if (failedRule) { showError('reg-error', failedRule.label + ' é obrigatório.'); return; }

  const btn = document.getElementById('btn-register');
  btn.disabled = true;
  try {
    const res  = await fetch(`${API}/auth/register`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      credentials: 'include', body: JSON.stringify({ name, email, password }),
    });
    const data = await res.json();
    if (!res.ok) { showError('reg-error', data.error); return; }

    _pendingUserId = data.user_id;
    goView('view-verify');
  } catch { showError('reg-error', 'Erro ao conectar com o servidor.'); }
  finally  { btn.disabled = false; }
});

// ── VERIFICAÇÃO DE E-MAIL ──────────────────────────────────────────────────────

async function resendCode() {
  if (!_pendingUserId) return;
  const btn = document.getElementById('btn-resend');
  btn.disabled = true;
  try {
    const res  = await fetch(`${API}/auth/resend-verification`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: _pendingUserId }),
    });
    const data = await res.json();
    if (res.ok) showSuccess('verify-success', data.message);
    else        showError('verify-error', data.error);
  } catch { showError('verify-error', 'Erro ao reenviar código.'); }
  finally {
    setTimeout(() => { btn.disabled = false; }, 30000);
  }
}

document.getElementById('btn-verify').addEventListener('click', async () => {
  const code = document.getElementById('verify-code-input').value.trim();
  if (!code) { showError('verify-error', 'Insira o código.'); return; }

  const btn = document.getElementById('btn-verify');
  btn.disabled = true;
  try {
    const res  = await fetch(`${API}/auth/verify-email`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      credentials: 'include', body: JSON.stringify({ user_id: _pendingUserId, code }),
    });
    const data = await res.json();
    if (!res.ok) { showError('verify-error', data.error); return; }
    showSuccess('verify-success', 'E-mail verificado! Redirecionando...');
    setTimeout(() => { window.location.href = '/'; }, 1500);
  } catch { showError('verify-error', 'Erro ao conectar com o servidor.'); }
  finally  { btn.disabled = false; }
});

// ── RECUPERAR SENHA ────────────────────────────────────────────────────────────

document.getElementById('btn-forgot').addEventListener('click', async () => {
  const email = document.getElementById('forgot-email').value.trim();
  if (!email) { showError('forgot-error', 'Informe seu e-mail.'); return; }

  const btn = document.getElementById('btn-forgot');
  btn.disabled = true;
  try {
    const res  = await fetch(`${API}/auth/forgot-password`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email }),
    });
    const data = await res.json();
    if (!res.ok) { showError('forgot-error', data.error); return; }

    document.getElementById('forgot-token-box').classList.remove('hidden');
    btn.classList.add('hidden');
  } catch { showError('forgot-error', 'Erro ao conectar com o servidor.'); }
  finally  { btn.disabled = false; }
});

// ── REDEFINIR SENHA ────────────────────────────────────────────────────────────

document.getElementById('btn-reset').addEventListener('click', async () => {
  const token    = document.getElementById('reset-token').value.trim();
  const password = document.getElementById('reset-password').value;
  const confirm  = document.getElementById('reset-confirm').value;

  if (!token || !password || !confirm) { showError('reset-error', 'Preencha todos os campos.'); return; }
  if (password !== confirm)            { showError('reset-error', 'As senhas não coincidem.'); return; }

  const failedRule = RULES.find(r => !r.pattern.test(password));
  if (failedRule) { showError('reset-error', failedRule.label + ' é obrigatório.'); return; }

  const btn = document.getElementById('btn-reset');
  btn.disabled = true;
  try {
    const res  = await fetch(`${API}/auth/reset-password`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token, new_password: password }),
    });
    const data = await res.json();
    if (!res.ok) { showError('reset-error', data.error); return; }
    showSuccess('reset-success', 'Senha redefinida! Redirecionando...');
    setTimeout(() => goView('view-login'), 2000);
  } catch { showError('reset-error', 'Erro ao conectar com o servidor.'); }
  finally  { btn.disabled = false; }
});

// ── ENTER ──────────────────────────────────────────────────────────────────────

document.getElementById('login-password').addEventListener('keydown', e => {
  if (e.key === 'Enter') document.getElementById('btn-login').click();
});
document.getElementById('reg-confirm').addEventListener('keydown', e => {
  if (e.key === 'Enter') document.getElementById('btn-register').click();
});
document.getElementById('verify-code-input').addEventListener('keydown', e => {
  if (e.key === 'Enter') document.getElementById('btn-verify').click();
});
