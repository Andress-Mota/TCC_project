const API = 'http://localhost:5000/api';

// ── VERIFICAÇÃO DE SESSÃO ──────────────────────────────────────────────────────

async function checkAuth() {
  try {
    const res  = await fetch(`${API}/auth/me`, { credentials: 'include' });
    const data = await res.json();
    if (!data.authenticated) {
      window.location.href = '/auth';
      return false;
    }
    document.getElementById('user-name').textContent = data.name;
    return true;
  } catch {
    window.location.href = '/auth';
    return false;
  }
}

// ── LOGOUT ─────────────────────────────────────────────────────────────────────

async function doLogout() {
  // Mostra tela de transição
  const screen = document.getElementById('logout-screen');
  screen.classList.remove('hidden');

  // Faz logout no servidor em paralelo
  fetch(`${API}/auth/logout`, { method: 'POST', credentials: 'include' });

  // Aguarda a animação do dragão (~2.4s) depois faz fade out e redireciona
  setTimeout(() => {
    screen.classList.add('fade-out');
    setTimeout(() => {
      localStorage.removeItem('theme');
      window.location.href = '/auth';
    }, 700);
  }, 2800);
}

document.getElementById('btn-logout').addEventListener('click', doLogout);
document.getElementById('btn-logout-mobile').addEventListener('click', doLogout);

// ── TROCAR SENHA ───────────────────────────────────────────────────────────────

document.getElementById('btn-change-password').addEventListener('click', openChangePasswordModal);

function closeModal() { hide('modal-change-pwd'); }

document.getElementById('btn-cp-save').addEventListener('click', async () => {
  const current = document.getElementById('cp-current').value.trim();
  const newPwd  = document.getElementById('cp-new').value.trim();
  const confirm = document.getElementById('cp-confirm').value.trim();

  hide('cp-error'); hide('cp-success');

  if (!current || !newPwd || !confirm) {
    showModalMsg('cp-error', 'Preencha todos os campos.'); return;
  }
  if (newPwd !== confirm) {
    showModalMsg('cp-error', 'As senhas não coincidem.'); return;
  }

  const btn = document.getElementById('btn-cp-save');
  btn.disabled = true;
  try {
    const res  = await fetch(`${API}/auth/change-password`, {
      method:      'POST',
      headers:     { 'Content-Type': 'application/json' },
      credentials: 'include',
      body:        JSON.stringify({ current_password: current, new_password: newPwd }),
    });
    const data = await res.json();
    if (!res.ok) { showModalMsg('cp-error', data.error); return; }
    showModalMsg('cp-success', 'Senha alterada com sucesso!');
    setTimeout(closeModal, 2000);
  } catch {
    showModalMsg('cp-error', 'Erro ao conectar com o servidor.');
  } finally {
    btn.disabled = false;
  }
});

function showModalMsg(id, msg) {
  const el = document.getElementById(id);
  el.textContent = msg;
  el.classList.remove('hidden');
}

// ── MODAL: OLHO + FORÇA ────────────────────────────────────────────────────────

function cpToggleEye(inputId, btn) {
  const input = document.getElementById(inputId);
  const isPass = input.type === 'password';
  input.type = isPass ? 'text' : 'password';
  btn.querySelector('i').className = isPass ? 'bi bi-eye-slash-fill' : 'bi bi-eye-fill';
}

const CP_RULES = [
  { id: 'cp-rule-len',   pattern: /.{8,}/        },
  { id: 'cp-rule-upper', pattern: /[A-Z]/         },
  { id: 'cp-rule-lower', pattern: /[a-z]/         },
  { id: 'cp-rule-num',   pattern: /\d/            },
  { id: 'cp-rule-spec',  pattern: /[^A-Za-z0-9]/ },
];

document.getElementById('cp-new').addEventListener('input', function () {
  const val  = this.value;
  let passed = 0;
  CP_RULES.forEach(rule => {
    const ok = rule.pattern.test(val);
    const li = document.getElementById(rule.id);
    li.classList.toggle('ok', ok);
    li.querySelector('i').className = ok ? 'bi bi-check-circle-fill' : 'bi bi-x-circle-fill';
    if (ok) passed++;
  });
  const pct  = (passed / CP_RULES.length) * 100;
  const fill = document.getElementById('cp-strength-fill');
  fill.style.width      = pct + '%';
  fill.style.background = pct <= 20  ? '#FF7A59'
                        : pct <= 60  ? '#D9B66B'
                        :              '#39C6B4';
});

function openChangePasswordModal() {
  ['cp-current', 'cp-new', 'cp-confirm'].forEach(id => document.getElementById(id).value = '');
  // reset olhos
  ['cp-current', 'cp-new', 'cp-confirm'].forEach(id => {
    const inp = document.getElementById(id);
    inp.type = 'password';
    const eye = inp.parentElement.querySelector('.eye-btn i');
    if (eye) eye.className = 'bi bi-eye-fill';
  });
  // reset força
  document.getElementById('cp-strength-fill').style.width = '0%';
  CP_RULES.forEach(rule => {
    const li = document.getElementById(rule.id);
    li.classList.remove('ok');
    li.querySelector('i').className = 'bi bi-x-circle-fill';
  });
  hide('cp-error'); hide('cp-success');
  show('modal-change-pwd');
}

// ── TEMA CLARO / ESCURO ────────────────────────────────────────────────────────

async function initTheme() {
  updateIcons(document.documentElement.classList.contains('light'));
  try {
    const res  = await fetch(`${API}/preferences`);
    const data = await res.json();
    data.theme_light ? applyLight() : applyDark();
  } catch {
    applyLight();
  }
}

document.getElementById('theme-toggle').addEventListener('click', async () => {
  const isLight = document.documentElement.classList.contains('light');
  isLight ? applyDark() : applyLight();
  try {
    await fetch(`${API}/preferences`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ theme_light: !isLight }),
    });
  } catch { }
});

function applyLight() {
  document.documentElement.classList.add('light');
  localStorage.setItem('theme', 'light');
  updateIcons(true);
}

function applyDark() {
  document.documentElement.classList.remove('light');
  localStorage.setItem('theme', 'dark');
  updateIcons(false);
}

function updateIcons(isLight) {
  document.getElementById('theme-icon').className        = isLight ? 'bi bi-moon-fill' : 'bi bi-sun-fill';
  document.getElementById('theme-icon-mobile').className = isLight ? 'bi bi-moon-fill' : 'bi bi-sun-fill';
  document.getElementById('theme-label').textContent     = isLight ? 'Modo Escuro' : 'Modo Claro';
}

document.getElementById('theme-toggle-mobile').addEventListener('click', async () => {
  const isLight = document.documentElement.classList.contains('light');
  isLight ? applyDark() : applyLight();
  try {
    await fetch(`${API}/preferences`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ theme_light: !isLight }),
    });
  } catch { }
});

checkAuth().then(ok => { if (ok) { initTheme(); loadDashboard(); renderTrainSteps(); } });

let chartInstance = null;
let pollTimer     = null;
let cmData        = {};
let rocChart      = null;
let rocData       = {};

// ── PERFIL ─────────────────────────────────────────────────────────────────────

async function loadProfile() {
  try {
    const res  = await fetch(`${API}/profile`, { credentials: 'include' });
    const user = await res.json();

    document.getElementById('profile-name').value          = user.name;
    document.getElementById('profile-email').value         = user.email;
    document.getElementById('profile-display-name').textContent = user.name;
    document.getElementById('profile-display-email').textContent = user.email;
    document.getElementById('profile-avatar').textContent  = user.name.charAt(0).toUpperCase();
    document.getElementById('profile-since').textContent   = fmtBR(user.created_at);

    const badge = document.getElementById('profile-verified-badge');
    if (user.email_verified) {
      badge.textContent  = 'E-mail verificado';
      badge.className    = 'badge badge-best';
    } else {
      badge.textContent  = 'E-mail não verificado';
      badge.className    = 'badge badge-individual';
    }
    badge.classList.remove('hidden');
  } catch { }
}

document.getElementById('btn-save-profile').addEventListener('click', async () => {
  const name  = document.getElementById('profile-name').value.trim();
  const email = document.getElementById('profile-email').value.trim();
  hide('profile-error'); hide('profile-success');

  const btn = document.getElementById('btn-save-profile');
  btn.disabled = true;
  try {
    const res  = await fetch(`${API}/profile`, {
      method: 'PUT', headers: { 'Content-Type': 'application/json' },
      credentials: 'include', body: JSON.stringify({ name, email }),
    });
    const data = await res.json();
    if (!res.ok) {
      document.getElementById('profile-error').textContent = data.error;
      show('profile-error');
      return;
    }
    document.getElementById('profile-success').textContent = data.message;
    show('profile-success');
    await loadProfile();
  } catch {
    document.getElementById('profile-error').textContent = 'Erro ao salvar.';
    show('profile-error');
  } finally { btn.disabled = false; }
});

document.getElementById('btn-open-change-pwd').addEventListener('click', openChangePasswordModal);

// ── NAVEGAÇÃO ──────────────────────────────────────────────────────────────────

document.querySelectorAll('.nav-btn, .bottom-nav-btn').forEach(btn => {
  btn.addEventListener('click', () => goTo(btn.dataset.page));
});

function goTo(page) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-btn, .bottom-nav-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('page-' + page).classList.add('active');
  document.querySelectorAll(`[data-page="${page}"]`).forEach(b => b.classList.add('active'));

  if (page === 'dashboard')  loadDashboard();
  if (page === 'treinar')    renderTrainSteps();
  if (page === 'resultados') loadSessions('result-session-select');
  if (page === 'testar')     loadSessions('test-session-select');
  if (page === 'historico')  loadSessions('hist-session-select');
  if (page === 'perfil')     loadProfile();
  if (page === 'logs')       loadLogs(1);
}

// ── DASHBOARD ──────────────────────────────────────────────────────────────────

let dashChart = null;

async function loadDashboard() {
  skeletonTable('dash-sessions-body', 4, 3);
  skeletonTable('dash-preds-body',    4, 3);
  try {
    const res  = await fetch(`${API}/dashboard`, { credentials: 'include' });
    const data = await res.json();

    countUp('dash-sessions',    data.total_sessions    || 0);
    countUp('dash-predictions', data.total_predictions || 0);
    document.getElementById('dash-best-acc').textContent   = data.best_accuracy ? data.best_accuracy + '%' : '—';
    document.getElementById('dash-best-model').textContent = data.best_model || '—';

    renderDashChart(data.model_averages);
    renderSessionsTable(data.recent_sessions);
    renderPredsTable(data.recent_predictions);
  } catch (e) { console.error('Erro ao carregar dashboard', e); }
}

function renderDashChart(models) {
  const labels  = models.map(m => m.model_name);
  const cvData  = models.map(m => m.avg_cv);
  const accData = models.map(m => m.avg_acc);
  const isDark  = !document.documentElement.classList.contains('light');
  const gridColor = isDark ? 'rgba(255,255,255,.08)' : 'rgba(0,0,0,.07)';
  const textColor = isDark ? '#9BA7C2' : '#5A6880';

  if (dashChart) dashChart.destroy();
  dashChart = new Chart(document.getElementById('dash-chart'), {
    type: 'bar',
    data: {
      labels,
      datasets: [
        { label: 'CV 10-fold (%)',     data: cvData,  backgroundColor: 'rgba(91,140,255,.75)',  borderRadius: 6 },
        { label: 'Acurácia Teste (%)', data: accData, backgroundColor: 'rgba(57,198,180,.75)', borderRadius: 6 },
      ],
    },
    options: {
      responsive: true,
      plugins: { legend: { labels: { color: textColor } } },
      scales: {
        x: { ticks: { color: textColor }, grid: { color: gridColor } },
        y: {
          ticks: { color: textColor, callback: v => v + '%' },
          grid: { color: gridColor },
          min: 0, max: 100,
        },
      },
    },
  });
}

function renderSessionsTable(sessions) {
  const tbody = document.getElementById('dash-sessions-body');
  if (!sessions.length) { tbody.innerHTML = '<tr><td colspan="4" style="color:var(--text-muted);text-align:center">Nenhuma sessão</td></tr>'; return; }
  tbody.innerHTML = sessions.map(s => {
    const statusColor = s.status === 'completed' ? 'var(--success)' : s.status === 'error' ? 'var(--error)' : 'var(--gold)';
    const statusLabel = s.status === 'completed' ? 'Concluída' : s.status === 'error' ? 'Erro' : 'Pendente';
    const nameHtml    = s.name
      ? `<strong>#${s.id}</strong> <span style="color:var(--text-muted);font-size:12px">— ${s.name}</span>`
      : `<strong>#${s.id}</strong>`;
    return `<tr>
      <td>${nameHtml}</td>
      <td>${s.total_images ?? '—'}</td>
      <td><span style="color:${statusColor};font-weight:700">${statusLabel}</span></td>
      <td style="color:var(--text-muted)">${fmtBR(s.created_at)}</td>
    </tr>`;
  }).join('');
}

function renderPredsTable(preds) {
  const tbody = document.getElementById('dash-preds-body');
  if (!preds.length) { tbody.innerHTML = '<tr><td colspan="4" style="color:var(--text-muted);text-align:center">Nenhuma predição</td></tr>'; return; }
  tbody.innerHTML = preds.map(p => `<tr>
    <td style="max-width:100px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title="${p.image_name}">${p.image_name}</td>
    <td style="color:var(--text-muted)">${p.model_name}</td>
    <td><strong>${p.predicted_class}</strong></td>
    <td style="color:var(--success)">${p.confidence?.toFixed(1)}%</td>
  </tr>`).join('');
}

// ── SESSÕES ────────────────────────────────────────────────────────────────────

function sessionLabel(s) {
  const base = `#${s.id} — ${s.total_images ?? '?'} imgs — ${fmtBR(s.created_at)}`;
  return s.name ? `${s.name}  (${base})` : base;
}

async function loadSessions(selectId) {
  try {
    const res  = await fetch(`${API}/sessions`, { credentials: 'include' });
    const data = await res.json();
    const sel  = document.getElementById(selectId);
    sel.innerHTML = '<option value="">-- selecione --</option>';
    data.filter(s => s.status === 'completed').forEach(s => {
      const opt = document.createElement('option');
      opt.value             = s.id;
      opt.textContent       = sessionLabel(s);
      opt.dataset.name      = s.name || '';
      opt.dataset.createdAt = s.created_at || '';
      opt.dataset.imgs      = s.total_images ?? '?';
      sel.appendChild(opt);
      sessionsCNNMap[s.id] = !!s.has_cnn;
    });
  } catch {
    console.error('Erro ao carregar sessões');
  }
}

// ── ETAPAS DO TREINAMENTO ──────────────────────────────────────────────────────

const TRAINING_STEPS = [
  { id: 'step-load',  label: 'Carregar imagens',          icon: 'bi-folder2-open',    match: /carregando imagens/i },
  { id: 'step-hog',   label: 'Extrair features HOG',      icon: 'bi-grid-3x3-gap',    match: /imagens carregadas|extraindo features/i },
  { id: 'step-opt',   label: 'Otimizar KNN (GridSearch)', icon: 'bi-sliders',         match: /otimizando k/i },
  { id: 'step-knn',   label: 'KNN',                       icon: 'bi-cpu',             match: /treinando knn/i },
  { id: 'step-svm',   label: 'SVM',                       icon: 'bi-cpu',             match: /treinando svm/i },
  { id: 'step-rf',    label: 'Random Forest',             icon: 'bi-diagram-3-fill',  match: /treinando random forest/i },
  { id: 'step-lr',    label: 'Logistic Regression',       icon: 'bi-cpu',             match: /treinando logistic/i },
  { id: 'step-nb',    label: 'Naive Bayes',               icon: 'bi-cpu',             match: /treinando naive/i },
  { id: 'step-vh',    label: 'Voting Hard',               icon: 'bi-people-fill',     match: /treinando voting hard/i },
  { id: 'step-vs',    label: 'Voting Soft',               icon: 'bi-people-fill',     match: /treinando voting soft/i },
  { id: 'step-st',    label: 'Stacking',                  icon: 'bi-stack',           match: /treinando stacking/i },
  { id: 'step-cnn',   label: 'CNN (EfficientNet-B0)',      icon: 'bi-eye-fill',        match: /cnn|efficientnet/i, cnnOnly: true },
  { id: 'step-save',  label: 'Salvar resultados',         icon: 'bi-database-fill',   match: /salvando resultados|cnn conclu/i },
];

function renderTrainSteps() {
  const list    = document.getElementById('train-steps-list');
  const badge   = document.getElementById('train-steps-status-badge');
  if (!list) return;
  const hasCnn  = document.getElementById('train-cnn-checkbox')?.checked;
  const visible = TRAINING_STEPS.filter(s => !s.cnnOnly || hasCnn);

  list.innerHTML = visible.map(s => `
    <div class="train-step waiting" id="${s.id}">
      <i class="bi ${s.icon} train-step-icon"></i>
      <span class="train-step-label">${s.label}</span>
      <span class="train-step-status"><i class="bi bi-circle"></i></span>
    </div>`).join('');

  if (badge) { badge.textContent = 'Aguardando'; badge.className = 'train-steps-badge'; }
}

function updateTrainSteps(pct, msg, status) {
  const badge = document.getElementById('train-steps-status-badge');

  if (status === 'completed') {
    document.querySelectorAll('.train-step').forEach(el => {
      el.className = 'train-step done';
      el.querySelector('.train-step-status').innerHTML = '<i class="bi bi-check-circle-fill"></i>';
    });
    if (badge) { badge.textContent = 'Concluído'; badge.className = 'train-steps-badge badge-done'; }
    return;
  }
  if (status === 'cancelled') {
    if (badge) { badge.textContent = 'Cancelado'; badge.className = 'train-steps-badge badge-warn'; }
    return;
  }
  if (status === 'error') {
    if (badge) { badge.textContent = 'Erro'; badge.className = 'train-steps-badge badge-err'; }
  } else {
    if (badge) { badge.textContent = pct + '%'; badge.className = 'train-steps-badge badge-active'; }
  }

  const visible = TRAINING_STEPS.filter(s => document.getElementById(s.id));
  let activeIdx = -1;
  for (let i = 0; i < visible.length; i++) {
    if (visible[i].match.test(msg)) { activeIdx = i; break; }
  }
  if (activeIdx === -1) return;

  visible.forEach((s, i) => {
    const el = document.getElementById(s.id);
    if (!el) return;
    const statusEl = el.querySelector('.train-step-status');
    if (i < activeIdx) {
      el.className = 'train-step done';
      statusEl.innerHTML = '<i class="bi bi-check-circle-fill"></i>';
    } else if (i === activeIdx) {
      el.className = status === 'error' ? 'train-step step-error' : 'train-step active';
      statusEl.innerHTML = status === 'error'
        ? '<i class="bi bi-x-circle-fill"></i>'
        : '<span class="spinner" style="width:13px;height:13px;border-width:2px;flex-shrink:0"></span>';
    } else {
      el.className = 'train-step waiting';
      statusEl.innerHTML = '<i class="bi bi-circle"></i>';
    }
  });
}

// ── TREINO ─────────────────────────────────────────────────────────────────────

function updateClassesHint(classes) {
  const hint = document.getElementById('dataset-classes-hint');
  if (!hint) return;
  if (!classes || classes.length === 0) {
    hint.innerHTML = 'A pasta deve conter subpastas por classe:<br/><code>dataset/classe_a/</code> e <code>dataset/classe_b/</code>';
    return;
  }
  const tags = classes.map(c => `<code>${c}/</code>`).join(' · ');
  hint.innerHTML = `Classes detectadas: ${tags}`;
}

document.getElementById('btn-browse').addEventListener('click', async () => {
  const btn = document.getElementById('btn-browse');
  btn.disabled = true;
  btn.innerHTML = '<i class="bi bi-hourglass-split"></i> Abrindo...';
  try {
    const res  = await fetch(`${API}/pick-folder`, { credentials: 'include' });
    const data = await res.json();
    if (data.path) {
      document.getElementById('dataset-path').value = data.path;
      hide('extract-status');
      updateClassesHint(data.classes);
    }
  } catch {
    // silencia erros de rede
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<i class="bi bi-folder2-open"></i> Pasta';
  }
});

document.getElementById('btn-import-zip').addEventListener('click', async () => {
  const btn    = document.getElementById('btn-import-zip');
  const status = document.getElementById('extract-status');

  btn.disabled = true;
  btn.innerHTML = '<i class="bi bi-hourglass-split"></i> Abrindo...';

  status.className = 'extract-status extracting';
  status.innerHTML = '<i class="bi bi-arrow-repeat"></i> Selecione o arquivo...';
  show('extract-status');

  try {
    const res  = await fetch(`${API}/pick-zip`, { credentials: 'include' });
    const data = await res.json();

    if (data.error) {
      status.className = 'extract-status error';
      status.innerHTML = `<i class="bi bi-x-circle"></i> ${data.error}`;
      return;
    }
    if (!data.path) {
      hide('extract-status');
      return;
    }

    document.getElementById('dataset-path').value = data.path;
    updateClassesHint(data.classes);
    status.className = 'extract-status done';
    status.innerHTML = `<i class="bi bi-check-circle"></i> Extraído em: ${data.path}`;
  } catch {
    status.className = 'extract-status error';
    status.innerHTML = '<i class="bi bi-x-circle"></i> Erro ao comunicar com o servidor.';
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<i class="bi bi-file-zip"></i> .zip / .tar';
  }
});

document.getElementById('btn-train').addEventListener('click', async () => {
  const path = document.getElementById('dataset-path').value.trim();
  if (!path) { alert('Informe o caminho do dataset.'); return; }

  show('train-progress-box');
  hide('train-success');
  setProgress(0, 'Enviando requisição...');
  document.getElementById('btn-train').disabled = true;
  renderTrainSteps();

  const sessionName  = document.getElementById('train-session-name').value.trim();
  const trainCnn     = document.getElementById('train-cnn-checkbox').checked;
  try {
    const res  = await fetch(`${API}/train`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ dataset_path: path, name: sessionName || null, train_cnn: trainCnn }),
    });
    const data = await res.json();
    if (data.error) { alert(data.error); return; }
    startPolling(data.session_id);
  } catch (e) {
    alert('Erro ao conectar com o servidor: ' + e.message);
    document.getElementById('btn-train').disabled = false;
  }
});

let currentSessionId  = null;
let sessionsCNNMap    = {};   // session_id → has_cnn (bool)
let _currentImageFile = null; // File object of last single prediction (for Grad-CAM)
let _histSessId       = null;
let _histCurrentPage  = 1;
const _HIST_PER_PAGE  = 50;

function resetTrainUI() {
  document.getElementById('btn-train').disabled = false;
  document.getElementById('btn-cancel-train').disabled = false;
  currentSessionId = null;
}

function startPolling(sessionId) {
  currentSessionId = sessionId;
  clearInterval(pollTimer);
  if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission();
  }
  pollTimer = setInterval(async () => {
    try {
      const res  = await fetch(`${API}/status/${sessionId}`);
      const data = await res.json();

      setProgress(data.progress || 0, data.message || '');
      updateTrainSteps(data.progress || 0, data.message || '', data.status);

      if (data.status === 'completed') {
        clearInterval(pollTimer);
        resetTrainUI();
        document.getElementById('train-success-msg').textContent =
          `Sessão #${sessionId} finalizada com sucesso.`;
        show('train-success');
        if ('Notification' in window && Notification.permission === 'granted') {
          new Notification('TCC IA — Treinamento Concluído', {
            body: `Sessão #${sessionId} finalizada com sucesso.`,
            icon: '/favicon.svg',
          });
        }
      }

      if (data.status === 'error') {
        clearInterval(pollTimer);
        resetTrainUI();
        alert('Erro no treinamento: ' + data.message);
      }

      if (data.status === 'cancelled') {
        clearInterval(pollTimer);
        resetTrainUI();
        setProgress(0, 'Treinamento cancelado.');
      }
    } catch {
      clearInterval(pollTimer);
    }
  }, 2000);
}

document.getElementById('btn-cancel-train').addEventListener('click', async () => {
  if (!currentSessionId) return;
  const btn = document.getElementById('btn-cancel-train');
  btn.disabled = true;
  btn.textContent = 'Cancelando...';
  await fetch(`${API}/sessions/${currentSessionId}/cancel`, {
    method: 'POST', credentials: 'include'
  });
});

function setProgress(pct, msg) {
  const bar = document.getElementById('train-progress-bar');
  bar.style.width = pct + '%';
  document.getElementById('train-pct').textContent        = pct + '%';
  document.getElementById('train-status-msg').textContent = msg;
  if (pct >= 100) bar.classList.add('fire');
  else            bar.classList.remove('fire');
}

// ── RESULTADOS ─────────────────────────────────────────────────────────────────

document.getElementById('btn-load-results').addEventListener('click', async () => {
  const sid = document.getElementById('result-session-select').value;
  if (!sid) { toast('Selecione uma sessão.', 'error'); return; }

  btnLoading('btn-load-results', true);
  try {
    const res  = await fetch(`${API}/sessions/${sid}/results`);
    const data = await res.json();

    renderResultsTable(data.results);
    renderChart(data.results);
    renderCMSelect(data.results);
    renderROCSelect(data.results);
    show('results-content');
    toast('Resultados carregados!', 'success');
  } catch { toast('Erro ao carregar resultados.', 'error'); }
  finally  { btnLoading('btn-load-results', false, '<i class="bi bi-bar-chart-fill"></i> Carregar'); }
});

document.getElementById('btn-export-csv').addEventListener('click', () => {
  const sid = document.getElementById('result-session-select').value;
  if (!sid) return;
  const a = document.createElement('a');
  a.href     = `${API}/sessions/${sid}/export`;
  a.download = `resultados_sessao_${sid}.csv`;
  a.click();
});

function renderResultsTable(results) {
  const tbody = document.querySelector('#results-table tbody');
  tbody.innerHTML = '';

  const best = results.reduce((a, b) => a.cv_mean > b.cv_mean ? a : b, results[0]);

  results.forEach(r => {
    const isBest    = r.model_name === best.model_name;
    const typeBadge = r.model_type === 'ensemble'
      ? '<span class="badge badge-ensemble">ensemble</span>'
      : '<span class="badge badge-individual">individual</span>';
    const bestBadge = isBest ? '<span class="badge badge-best">melhor</span>' : '';
    const fmt = (v) => v != null ? (v * 100).toFixed(2) + '%' : '—';

    tbody.innerHTML += `
      <tr>
        <td>${r.model_name} ${bestBadge}</td>
        <td>${typeBadge}</td>
        <td>${fmt(r.cv_mean)}</td>
        <td>${fmt(r.test_accuracy)}</td>
        <td>${fmt(r.precision_score)}</td>
        <td>${fmt(r.recall_score)}</td>
        <td>${fmt(r.f1_score)}</td>
        <td>${r.roc_auc != null ? r.roc_auc.toFixed(4) : '—'}</td>
      </tr>`;
  });
}

function renderChart(results) {
  const labels    = results.map(r => r.model_name);
  const cvData    = results.map(r => +(r.cv_mean * 100).toFixed(2));
  const testData  = results.map(r => +(r.test_accuracy * 100).toFixed(2));
  const isDark    = !document.documentElement.classList.contains('light');
  const gridColor = isDark ? 'rgba(255,255,255,.08)' : 'rgba(0,0,0,.07)';
  const textColor = isDark ? '#9BA7C2' : '#5A6880';

  if (chartInstance) chartInstance.destroy();

  const ctx = document.getElementById('results-chart').getContext('2d');
  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        { label: 'CV 10-fold (%)',     data: cvData,   backgroundColor: 'rgba(79,142,247,0.75)', borderRadius: 6 },
        { label: 'Acurácia Teste (%)', data: testData, backgroundColor: 'rgba(124,92,252,0.75)', borderRadius: 6 },
      ],
    },
    options: {
      responsive: true,
      plugins: { legend: { labels: { color: textColor } } },
      scales: {
        x: { ticks: { color: textColor }, grid: { color: gridColor } },
        y: {
          ticks: { color: textColor, callback: v => v + '%' },
          grid: { color: gridColor },
          min: 50, max: 100,
        },
      },
    },
  });
}

function renderROCSelect(results) {
  rocData = {};
  const sel = document.getElementById('roc-model-select');
  sel.innerHTML = '';
  results.forEach(r => {
    if (r.roc_data) {
      rocData[r.model_name] = r.roc_data;
      const opt = document.createElement('option');
      opt.value       = r.model_name;
      opt.textContent = r.model_name;
      sel.appendChild(opt);
    }
  });
  if (sel.value) renderROCChart(sel.value);
}

document.getElementById('roc-model-select').addEventListener('change', e => renderROCChart(e.target.value));

function renderROCChart(modelName) {
  const data = rocData[modelName];
  if (!data) return;

  const isDark    = !document.documentElement.classList.contains('light');
  const gridColor = isDark ? 'rgba(255,255,255,.08)' : 'rgba(0,0,0,.07)';
  const textColor = isDark ? '#9BA7C2' : '#5A6880';
  const scaleOpts = {
    ticks: { color: textColor },
    grid: { color: gridColor },
    min: 0, max: 1,
  };

  if (rocChart) rocChart.destroy();
  const ctx = document.getElementById('roc-chart').getContext('2d');

  let datasets;
  if (data.fpr) {
    datasets = [
      {
        label: `${modelName} (AUC = ${data.auc})`,
        data: data.fpr.map((f, i) => ({ x: f, y: data.tpr[i] })),
        borderColor: 'rgba(91,140,255,1)',
        backgroundColor: 'rgba(91,140,255,0.1)',
        fill: true, pointRadius: 0, tension: 0.1,
      },
      {
        label: 'Aleatório',
        data: [{ x: 0, y: 0 }, { x: 1, y: 1 }],
        borderColor: 'rgba(255,100,100,0.5)',
        borderDash: [6, 4], pointRadius: 0,
      },
    ];
  } else if (data.curves) {
    const colors = [
      'rgba(91,140,255,1)', 'rgba(57,198,180,1)', 'rgba(217,182,107,1)',
      'rgba(255,122,89,1)', 'rgba(149,97,255,1)', 'rgba(255,200,80,1)',
    ];
    datasets = data.curves.map((c, i) => ({
      label: `Classe ${c.class} (AUC = ${c.auc})`,
      data: c.fpr.map((f, j) => ({ x: f, y: c.tpr[j] })),
      borderColor: colors[i % colors.length],
      fill: false, pointRadius: 0, tension: 0.1,
    }));
    datasets.push({ label: 'Aleatório', data: [{ x: 0, y: 0 }, { x: 1, y: 1 }], borderColor: 'rgba(255,100,100,0.5)', borderDash: [6, 4], pointRadius: 0 });
  } else return;

  rocChart = new Chart(ctx, {
    type: 'line',
    data: { datasets },
    options: {
      responsive: true,
      plugins: { legend: { labels: { color: textColor } } },
      scales: {
        x: { type: 'linear', title: { display: true, text: 'Falso Positivo', color: textColor }, ...scaleOpts },
        y: { title: { display: true, text: 'Verdadeiro Positivo', color: textColor }, ...scaleOpts },
      },
    },
  });
}

function renderCMSelect(results) {
  cmData = {};
  const sel = document.getElementById('cm-model-select');
  sel.innerHTML = '';
  results.forEach(r => {
    if (r.confusion_matrix) {
      cmData[r.model_name] = r.confusion_matrix;
      const opt = document.createElement('option');
      opt.value       = r.model_name;
      opt.textContent = r.model_name;
      sel.appendChild(opt);
    }
  });
  renderCM(sel.value);
}

document.getElementById('cm-model-select').addEventListener('change', e => {
  renderCM(e.target.value);
});

function renderCM(modelName) {
  const mat = cmData[modelName];
  if (!mat) return;
  const container = document.getElementById('confusion-matrix-container');

  const size = mat.length;
  container.innerHTML = '';

  const grid = document.createElement('div');
  grid.className = 'cm-grid';
  grid.style.gridTemplateColumns = `80px repeat(${size}, 80px)`;

  // header row
  const blank = document.createElement('div');
  blank.className = 'cm-header';
  grid.appendChild(blank);

  for (let j = 0; j < size; j++) {
    const h = document.createElement('div');
    h.className = 'cm-header';
    h.textContent = `Pred ${j}`;
    grid.appendChild(h);
  }

  // data rows
  for (let i = 0; i < size; i++) {
    const rh = document.createElement('div');
    rh.className = 'cm-header';
    rh.textContent = `Real ${i}`;
    grid.appendChild(rh);

    for (let j = 0; j < size; j++) {
      const cell = document.createElement('div');
      cell.className = 'cm-cell ' + (i === j ? (i === 0 ? 'cm-tn' : 'cm-tp') : (i === 0 ? 'cm-fp' : 'cm-fn'));
      cell.textContent = mat[i][j];
      grid.appendChild(cell);
    }
  }

  container.appendChild(grid);
}

// ── TESTAR IMAGEM ──────────────────────────────────────────────────────────────

document.getElementById('train-cnn-checkbox').addEventListener('change', renderTrainSteps);

// Persiste e restaura o modelo selecionado
(function () {
  const sel = document.getElementById('test-model-select');
  const saved = localStorage.getItem('test-model-select');
  if (saved) {
    const opt = Array.from(sel.options).find(o => o.value === saved);
    if (opt) sel.value = saved;
  }
  sel.addEventListener('change', () => localStorage.setItem('test-model-select', sel.value));
})();

// Arquivos selecionados (unifica seleção por arquivo e por pasta)
let _testFiles = [];

function _renderPreviews(files) {
  const container = document.getElementById('preview-container');
  container.innerHTML = '';
  hide('predict-result');
  hide('predict-batch');

  const MAX_PREVIEW = 40;
  const shown = files.slice(0, MAX_PREVIEW);
  shown.forEach(file => {
    const src  = URL.createObjectURL(file);
    const wrap = document.createElement('div');
    wrap.style.cssText = 'position:relative;cursor:zoom-in';
    wrap.title = file.name;

    const img = document.createElement('img');
    img.src   = src;
    img.style.cssText = 'width:80px;height:80px;object-fit:cover;border-radius:8px;border:2px solid var(--border);display:block;transition:opacity .15s';
    img.addEventListener('mouseenter', () => img.style.opacity = '.75');
    img.addEventListener('mouseleave', () => img.style.opacity = '1');
    img.addEventListener('click', () => openLightbox(src, file.name));

    const icon = document.createElement('div');
    icon.innerHTML = '<i class="bi bi-zoom-in"></i>';
    icon.style.cssText = 'position:absolute;bottom:4px;right:4px;background:rgba(0,0,0,.55);color:#fff;font-size:12px;border-radius:4px;padding:2px 4px;pointer-events:none';

    wrap.appendChild(img);
    wrap.appendChild(icon);
    container.appendChild(wrap);
  });

  if (files.length > MAX_PREVIEW) {
    const more = document.createElement('div');
    more.style.cssText = 'width:80px;height:80px;border-radius:8px;border:2px dashed var(--border);display:flex;align-items:center;justify-content:center;font-size:13px;color:var(--text-muted);text-align:center';
    more.textContent = `+${files.length - MAX_PREVIEW}`;
    container.appendChild(more);
  }

  const countEl = document.getElementById('selected-count');
  if (files.length > 0) {
    countEl.textContent = `${files.length} imagem(ns) selecionada(s)`;
    countEl.style.display = 'block';
  } else {
    countEl.style.display = 'none';
  }
}

document.getElementById('test-image-input').addEventListener('change', e => {
  _testFiles = Array.from(e.target.files);
  document.getElementById('test-folder-input').value = '';
  _renderPreviews(_testFiles);
});

document.getElementById('test-folder-input').addEventListener('change', e => {
  const all = Array.from(e.target.files).filter(f => /\.(jpe?g|png|bmp|tiff?|webp)$/i.test(f.name));
  _testFiles = all;
  document.getElementById('test-image-input').value = '';
  _renderPreviews(_testFiles);
  if (all.length === 0) toast('Nenhuma imagem encontrada na pasta selecionada.', 'error');
});

document.getElementById('btn-pick-folder').addEventListener('click', () => {
  document.getElementById('test-folder-input').click();
});

document.getElementById('btn-predict').addEventListener('click', async () => {
  const sid   = document.getElementById('test-session-select').value;
  const model = document.getElementById('test-model-select').value;

  if (!sid)              { alert('Selecione uma sessão.'); return; }
  if (!_testFiles.length) { alert('Selecione ao menos uma imagem.'); return; }

  document.getElementById('btn-predict').disabled = true;
  hide('predict-result');
  hide('predict-batch');
  const _prevImg = document.getElementById('result-image-preview');
  if (_prevImg) { _prevImg.src = ''; _prevImg.classList.add('hidden'); }

  hide('augment-section');
  hide('augment-status');

  try {
    const form = new FormData();
    _testFiles.forEach(f => form.append('image', f));
    form.append('session_id', sid);
    form.append('model_name', model);

    const res  = await fetch(`${API}/predict`, { method: 'POST', body: form, credentials: 'include' });
    if (res.status === 413) {
      toast('Arquivo(s) muito grande(s). Limite máximo: 50 MB total.', 'error', 5000);
      return;
    }
    const data = await res.json();
    if (data.error) { toast(data.error, 'error'); return; }

    _initFeedback(data.classes, parseInt(sid));

    if (_testFiles.length === 1 && !data.batch) {
      _currentPredId    = data.prediction_id;
      _currentImageFile = _testFiles[0];
      document.getElementById('result-class-name').textContent = data.predicted_class;
      document.getElementById('result-confidence').textContent = data.confidence + '%';
      document.getElementById('result-model-name').textContent = data.model;

      const prevImg = document.getElementById('result-image-preview');
      if (prevImg) {
        prevImg.src = URL.createObjectURL(_testFiles[0]);
        prevImg.classList.remove('hidden');
      }
      _resetSingleFeedback();

      const hasCnn = sessionsCNNMap[parseInt(sid)];
      if (hasCnn) {
        hide('gradcam-result');
        hide('gradcam-loading');
        hide('gradcam-error');
        const btn = document.getElementById('btn-show-gradcam');
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-eye-fill"></i> Ver análise visual (Grad-CAM)';
        show('gradcam-section');
      } else {
        hide('gradcam-section');
      }

      show('predict-result');
    } else {
      const rows = data.results || [data];
      const classes = data.classes || [];
      const hasCnn  = sessionsCNNMap[parseInt(sid)];

      // Mapeia filename → File object para lightbox e Grad-CAM
      const fileMap = {};
      _testFiles.forEach(f => {
        fileMap[f.name] = f;
        fileMap[f.name.split('/').pop().split('\\').pop()] = f;
      });
      _batchFileMap = fileMap;
      _batchSessId  = parseInt(sid);

      // Classe "normal" é a que contém "normal" no nome (case-insensitive)
      const normalClass = classes.find(c => /normal/i.test(c)) || classes[0] || '';

      // Positivos (achados) primeiro; dentro de cada grupo, maior confiança primeiro
      const sorted = [...rows].sort((a, b) => {
        const aPos = a.predicted_class !== normalClass ? 0 : 1;
        const bPos = b.predicted_class !== normalClass ? 0 : 1;
        if (aPos !== bPos) return aPos - bPos;
        return b.confidence - a.confidence;
      });

      // Resumo por classe
      const counts = {};
      rows.forEach(r => { counts[r.predicted_class] = (counts[r.predicted_class] || 0) + 1; });
      const summaryEl = document.getElementById('batch-summary');
      summaryEl.innerHTML = Object.entries(counts).map(([cls, n]) => {
        const isNormal = /normal/i.test(cls);
        const bg = isNormal ? 'var(--success)' : 'var(--error)';
        return `<span style="display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border-radius:20px;background:${bg}18;border:1px solid ${bg};font-size:13px;font-weight:600">
          <span style="width:9px;height:9px;border-radius:50%;background:${bg};display:inline-block"></span>
          ${cls}: ${n} imagem(ns)
        </span>`;
      }).join('');

      // Mostra/oculta coluna Grad-CAM conforme disponibilidade
      const thGcam = document.getElementById('batch-th-gradcam');
      if (hasCnn) thGcam.classList.remove('hidden'); else thGcam.classList.add('hidden');

      const tbody = document.querySelector('#batch-table tbody');
      tbody.innerHTML = sorted.map(r => {
        const imgName    = r.image || r.image_name || r.filename || '—';
        const basename   = imgName.split('/').pop().split('\\').pop();
        const isNormal   = /normal/i.test(r.predicted_class);
        const classColor = isNormal ? 'var(--success)' : 'var(--error)';
        const file       = fileMap[imgName] || fileMap[basename];
        const thumbSrc   = file ? URL.createObjectURL(file) : null;

        const thumbCell = thumbSrc
          ? `<td style="padding:4px 8px">
               <img src="${thumbSrc}" title="${basename}" alt="${basename}"
                 style="width:48px;height:48px;object-fit:cover;border-radius:6px;cursor:zoom-in;border:1px solid var(--border)"
                 onclick="openLightbox('${thumbSrc}','${basename.replace(/'/g,"\\'")}')"/>
             </td>`
          : `<td style="padding:4px 8px;color:var(--text-muted);font-size:18px;text-align:center">
               <i class="bi bi-image" title="Imagem não disponível"></i>
             </td>`;

        const gcamCell = hasCnn
          ? `<td style="text-align:center">
               <button class="btn btn-secondary" style="padding:4px 10px;font-size:12px"
                 onclick="openBatchGradCAM('${imgName.replace(/'/g,"\\'")}')">
                 <i class="bi bi-eye-fill"></i>
               </button>
             </td>`
          : '';

        return `<tr>
          ${thumbCell}
          <td style="max-width:160px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title="${imgName}">${basename}</td>
          <td><strong style="color:${classColor}">${r.predicted_class}</strong></td>
          <td>${r.confidence}%</td>
          <td style="color:var(--text-muted)">${r.model}</td>
          ${_buildBatchFeedbackCell(r.prediction_id, r)}
          ${gcamCell}
        </tr>`;
      }).join('');

      show('predict-batch');
    }
  } catch (e) {
    toast('Erro: ' + e.message, 'error');
  } finally {
    btnLoading('btn-predict', false, '<i class="bi bi-lightning-fill"></i> Classificar');
  }
});

// ── HISTÓRICO ──────────────────────────────────────────────────────────────────

document.getElementById('btn-load-hist').addEventListener('click', () => {
  const sid = document.getElementById('hist-session-select').value;
  if (!sid) { toast('Selecione uma sessão.', 'error'); return; }
  _histSessId = sid;
  loadHistPredictions(sid, 1);
});

document.getElementById('btn-export-pred-csv').addEventListener('click', () => {
  if (!_histSessId) return;
  const a = document.createElement('a');
  a.href     = `${API}/sessions/${_histSessId}/predictions/export`;
  a.download = `predicoes_sessao_${_histSessId}.csv`;
  a.click();
});

async function loadHistPredictions(sid, page = 1) {
  _histCurrentPage = page;
  btnLoading('btn-load-hist', true);
  skeletonTable('hist-table', 5, 5);
  show('hist-content');

  try {
    const res  = await fetch(
      `${API}/sessions/${sid}/predictions?page=${page}&per_page=${_HIST_PER_PAGE}`,
      { credentials: 'include' }
    );
    const data = await res.json();
    if (!res.ok) { toast(data.error || 'Erro ao carregar histórico.', 'error'); return; }

    const preds = data.predictions || [];
    const total = data.total || 0;

    const countEl = document.getElementById('hist-total-count');
    if (countEl) countEl.textContent = total ? `(${total} predições)` : '';

    const tbody = document.querySelector('#hist-table tbody');
    tbody.innerHTML = '';

    if (!preds.length) {
      tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;color:var(--text-muted)">Nenhuma predição ainda.</td></tr>';
    } else {
      preds.forEach(p => {
        let fbHtml = '<span style="color:var(--text-muted)">—</span>';
        if (p.feedback === 'correct') {
          fbHtml = '<span style="color:var(--success);font-weight:700"><i class="bi bi-check-lg"></i> Correto</span>';
        } else if (p.feedback === 'incorrect') {
          const cc = p.correct_class ? ` (${p.correct_class})` : '';
          fbHtml = `<span style="color:var(--error);font-weight:700"><i class="bi bi-x-lg"></i> Errado${cc}</span>`;
        }
        tbody.innerHTML += `<tr>
          <td style="max-width:140px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title="${p.image_name}">${p.image_name}</td>
          <td style="color:var(--text-muted)">${p.model_name}</td>
          <td><strong>${p.predicted_class}</strong></td>
          <td style="color:var(--success)">${(p.confidence * 100).toFixed(1)}%</td>
          <td>${fbHtml}</td>
          <td style="color:var(--text-muted);white-space:nowrap">${fmtBR(p.created_at)}</td>
        </tr>`;
      });
    }
    renderHistPagination(total, _HIST_PER_PAGE, page, sid);
  } catch { toast('Erro ao carregar histórico.', 'error'); }
  finally  { btnLoading('btn-load-hist', false, '<i class="bi bi-clock-history"></i> Carregar'); }
}

function renderHistPagination(total, perPage, currentPage, sid) {
  const totalPages = Math.ceil(total / perPage);
  const el = document.getElementById('hist-pagination');
  if (!el) return;
  if (totalPages <= 1) { el.innerHTML = ''; return; }
  el.innerHTML = Array.from({ length: totalPages }, (_, i) => i + 1).map(i =>
    `<button class="page-btn${i === currentPage ? ' active' : ''}"
             onclick="loadHistPredictions('${sid}', ${i})">${i}</button>`
  ).join('');
}

// ── FEEDBACK DE PREDIÇÃO ───────────────────────────────────────────────────────

let _currentPredId     = null;
let _currentSessId     = null;
let _currentClasses    = [];
let _batchFileMap      = {};     // filename → File (para lightbox e Grad-CAM em lote)
let _batchSessId       = null;   // session_id do último resultado em lote
let _incorrectSubmitted = false; // se já há feedback incorreto na sessão atual

function _initFeedback(classes, sessionId) {
  _currentClasses = classes || [];
  _currentSessId  = sessionId;
  _incorrectSubmitted = false;

  // Popula o select de classe correta
  const sel = document.getElementById('correct-class-select');
  sel.innerHTML = _currentClasses.map(c => `<option value="${c}">${c}</option>`).join('');
}

function _resetSingleFeedback() {
  show('feedback-single');
  ['btn-fb-correct','btn-fb-incorrect'].forEach(id => {
    const b = document.getElementById(id);
    b.disabled = false;
    b.classList.remove('feedback-used');
  });
  hide('wrong-class-picker');
  hide('feedback-single-done');
}

function showWrongPicker() {
  show('wrong-class-picker');
}

async function submitSingleFeedback(type) {
  if (!_currentPredId) return;

  const correctClass = type === 'incorrect'
    ? document.getElementById('correct-class-select').value
    : null;

  document.getElementById('btn-fb-correct').disabled   = true;
  document.getElementById('btn-fb-incorrect').disabled = true;

  try {
    const res = await fetch(`${API}/predictions/${_currentPredId}/feedback`, {
      method:      'POST',
      headers:     { 'Content-Type': 'application/json' },
      credentials: 'include',
      body:        JSON.stringify({ feedback: type, correct_class: correctClass }),
    });
    if (!res.ok) { toast('Erro ao registrar feedback.', 'error'); return; }

    hide('wrong-class-picker');
    const done = document.getElementById('feedback-single-done');
    const editBtn = `<br><button class="btn btn-secondary" style="margin-top:8px;font-size:12px"
        onclick="_resetSingleFeedback()"><i class="bi bi-pencil-fill"></i> Editar</button>`;
    if (type === 'correct') {
      done.innerHTML = '<i class="bi bi-check-circle-fill" style="color:var(--success)"></i> Obrigado! Feedback registrado.' + editBtn;
    } else {
      done.innerHTML = `<i class="bi bi-exclamation-circle-fill" style="color:var(--error)"></i> `
                     + `Registrado como incorreto. Classe correta: <strong>${correctClass}</strong>` + editBtn;
      _incorrectSubmitted = true;
      _showAugmentSection();
    }
    show('feedback-single-done');
  } catch {
    toast('Erro ao enviar feedback.', 'error');
    document.getElementById('btn-fb-correct').disabled   = false;
    document.getElementById('btn-fb-incorrect').disabled = false;
  }
}

async function submitBatchFeedback(predId, type, correctClass, rowEl) {
  try {
    const res = await fetch(`${API}/predictions/${predId}/feedback`, {
      method:      'POST',
      headers:     { 'Content-Type': 'application/json' },
      credentials: 'include',
      body:        JSON.stringify({ feedback: type, correct_class: correctClass || null }),
    });
    if (!res.ok) { toast('Erro ao registrar feedback.', 'error'); return; }

    const cell = rowEl.querySelector('.batch-feedback-cell');
    if (type === 'correct') {
      cell.innerHTML = '<span style="color:var(--success);font-weight:700"><i class="bi bi-check-lg"></i> Correto</span>';
    } else {
      cell.innerHTML = `<span style="color:var(--error);font-weight:700"><i class="bi bi-x-lg"></i> Errado`
                     + (correctClass ? ` (${correctClass})` : '') + `</span>`;
      _incorrectSubmitted = true;
      _showAugmentSection();
    }
  } catch {
    toast('Erro ao enviar feedback.', 'error');
  }
}

function _buildBatchFeedbackCell(predId, row) {
  if (!_currentClasses.length) return '<td class="batch-feedback-cell">—</td>';

  const opts = _currentClasses.map(c => `<option value="${c}">${c}</option>`).join('');
  return `<td class="batch-feedback-cell" style="white-space:nowrap">
    <button class="btn-feedback btn-feedback-ok" style="padding:3px 10px;font-size:12px"
            onclick="submitBatchFeedback(${predId},'correct',null,this.closest('tr'))">
      <i class="bi bi-check-lg"></i>
    </button>
    <select class="batch-correct-class" style="width:auto;display:inline-block;padding:4px 8px;font-size:12px;margin:0 4px">
      ${opts}
    </select>
    <button class="btn-feedback btn-feedback-err" style="padding:3px 10px;font-size:12px"
            onclick="submitBatchFeedback(${predId},'incorrect',this.previousElementSibling.value,this.closest('tr'))">
      <i class="bi bi-x-lg"></i>
    </button>
  </td>`;
}

function _showAugmentSection() {
  if (!_currentSessId) return;
  show('augment-section');
  document.getElementById('augment-name').placeholder =
    `Ex: Sessão #${_currentSessId} melhorada com feedback`;
}

document.getElementById('btn-augment-train').addEventListener('click', async () => {
  const name = document.getElementById('augment-name').value.trim();
  const btn  = document.getElementById('btn-augment-train');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Iniciando...';

  try {
    const res  = await fetch(`${API}/sessions/${_currentSessId}/augment-train`, {
      method:      'POST',
      headers:     { 'Content-Type': 'application/json' },
      credentials: 'include',
      body:        JSON.stringify({ name }),
    });
    const data = await res.json();
    if (!res.ok) { toast(data.error, 'error'); return; }

    const status = document.getElementById('augment-status');
    status.innerHTML = `<i class="bi bi-check-circle-fill"></i> Retreino iniciado! `
                     + `Sessão <strong>#${data.session_id}</strong> criada. `
                     + `<a href="#" onclick="goTo('treinar');return false" style="color:var(--accent)">Acompanhar progresso</a>`;
    show('augment-status');
    toast(`Sessão #${data.session_id} criada com dados de feedback!`, 'success');
    startPolling(data.session_id);
    goTo('treinar');
  } catch {
    toast('Erro ao iniciar retreino.', 'error');
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<i class="bi bi-cpu-fill"></i> Iniciar Retreino';
  }
});

// ── DELETAR / EXPORTAR SESSÃO ──────────────────────────────────────────────────

let _deleteSessionPending = null;

function confirmDeleteSession(selectId) {
  const sel = document.getElementById(selectId);
  if (!sel || !sel.value) { toast('Selecione uma sessão primeiro.', 'error'); return; }
  const sid   = sel.value;
  const name  = sel.options[sel.selectedIndex]?.dataset.name;
  const label = name ? `"${name}"` : `#${sid}`;
  _deleteSessionPending = { sid, label };
  document.getElementById('modal-delete-msg').textContent = `Deseja excluir a sessão ${label}?`;
  show('modal-delete-session');
}

function closeDeleteModal() {
  hide('modal-delete-session');
  _deleteSessionPending = null;
}

document.getElementById('btn-delete-confirm').addEventListener('click', async () => {
  if (!_deleteSessionPending) return;
  const { sid, label } = _deleteSessionPending;
  closeDeleteModal();

  try {
    const res  = await fetch(`${API}/sessions/${sid}/delete`, { method: 'POST', credentials: 'include' });
    const data = await res.json();
    if (!res.ok) { toast(data.error || 'Erro ao excluir sessão.', 'error'); return; }

    ['result-session-select', 'test-session-select', 'hist-session-select'].forEach(id => {
      const s = document.getElementById(id);
      if (!s) return;
      Array.from(s.options).forEach(o => { if (o.value == sid) o.remove(); });
    });
    delete sessionsCNNMap[parseInt(sid)];
    if (_histSessId == sid) { _histSessId = null; hide('hist-content'); }
    toast(`Sessão ${label} excluída.`, 'success');
  } catch { toast('Erro ao excluir sessão.', 'error'); }
});

// ── RENOMEAR SESSÃO ────────────────────────────────────────────────────────────

let _renameSourceSelectId = null;

function openRenameModal(selectId) {
  const sel = document.getElementById(selectId);
  if (!sel || !sel.value) {
    toast('Selecione uma sessão primeiro.', 'error');
    return;
  }
  _renameSourceSelectId = selectId;
  const sid      = sel.value;
  const curName  = sel.options[sel.selectedIndex]?.dataset.name || '';
  document.getElementById('rename-session-subtitle').textContent = `Sessão #${sid}`;
  document.getElementById('rename-session-input').value = curName;
  hide('rename-session-error');
  show('modal-rename-session');
  setTimeout(() => document.getElementById('rename-session-input').focus(), 80);
}

function closeRenameModal() { hide('modal-rename-session'); }

document.getElementById('btn-rename-save').addEventListener('click', async () => {
  const sel = document.getElementById(_renameSourceSelectId);
  if (!sel || !sel.value) return;
  const sid  = sel.value;
  const name = document.getElementById('rename-session-input').value.trim();

  const btn = document.getElementById('btn-rename-save');
  btn.disabled = true;
  hide('rename-session-error');

  try {
    const res  = await fetch(`${API}/sessions/${sid}/name`, {
      method:      'PUT',
      headers:     { 'Content-Type': 'application/json' },
      credentials: 'include',
      body:        JSON.stringify({ name }),
    });
    const data = await res.json();
    if (!res.ok) {
      document.getElementById('rename-session-error').textContent = data.error;
      show('rename-session-error');
      return;
    }

    // Atualiza o option no select que originou a ação
    const opt = sel.options[sel.selectedIndex];
    const sid_num   = parseInt(sid);
    const imgs      = opt.dataset.imgs ?? '?';
    const createdAt = opt.dataset.createdAt ?? '';
    const fakeSession = { id: sid_num, name, total_images: imgs, created_at: createdAt };
    opt.textContent  = sessionLabel(fakeSession);
    opt.dataset.name = name;

    // Atualiza nos demais selects (se a sessão aparecer lá também)
    ['result-session-select', 'test-session-select', 'hist-session-select'].forEach(id => {
      if (id === _renameSourceSelectId) return;
      const other = document.getElementById(id);
      if (!other) return;
      Array.from(other.options).forEach(o => {
        if (o.value == sid) {
          o.textContent  = sessionLabel(fakeSession);
          o.dataset.name = name;
        }
      });
    });

    closeRenameModal();
    toast(name ? `Sessão renomeada para "${name}".` : 'Nome removido.', 'success');
  } catch {
    document.getElementById('rename-session-error').textContent = 'Erro ao salvar.';
    show('rename-session-error');
  } finally {
    btn.disabled = false;
  }
});

document.getElementById('rename-session-input').addEventListener('keydown', e => {
  if (e.key === 'Enter') document.getElementById('btn-rename-save').click();
});

// ── LOGS DE ERRO ───────────────────────────────────────────────────────────────

let logsCurrentPage = 1;
let logsCache       = {};

const ORIGIN_LABEL = {
  treinamento:  'Treinamento',
  predicao:     'Predição',
  autenticacao: 'Autenticação',
  sistema:      'Sistema',
  perfil:       'Perfil',
};

async function loadLogs(page = 1) {
  logsCurrentPage = page;
  const level  = document.getElementById('logs-filter-level').value;
  const origin = document.getElementById('logs-filter-origin').value;

  const params = new URLSearchParams({ page, per_page: 20 });
  if (level)  params.set('level',  level);
  if (origin) params.set('origin', origin);

  skeletonTable('logs-body', 7, 5);

  try {
    const res  = await fetch(`${API}/error-logs?${params}`, { credentials: 'include' });
    const data = await res.json();
    logsCache = {};
    data.logs.forEach(l => { logsCache[l.id] = l; });
    renderLogsTable(data.logs);
    renderLogsPagination(data.total, data.per_page, data.page);
  } catch {
    toast('Erro ao carregar logs.', 'error');
  }
}

function renderLogsTable(logs) {
  const tbody = document.getElementById('logs-body');
  if (!logs.length) {
    tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;color:var(--text-muted);padding:24px">Nenhum erro registrado.</td></tr>';
    return;
  }
  tbody.innerHTML = logs.map(l => {
    const lvlClass = l.level === 'CRITICAL' ? 'badge-critical'
                   : l.level === 'WARNING'  ? 'badge-warning'
                   :                          'badge-error';
    const msg      = (l.message || '—').length > 65
                   ? escHtml(l.message.slice(0, 65)) + '…'
                   : escHtml(l.message || '—');
    const origin   = escHtml(ORIGIN_LABEL[l.origin] || l.origin);
    return `<tr>
      <td><strong>#${l.id}</strong></td>
      <td><span class="badge ${lvlClass}">${l.level}</span></td>
      <td><span class="badge badge-individual" style="font-size:11px">${origin}</span></td>
      <td style="max-width:240px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap"
          title="${escHtml(l.message || '')}">${msg}</td>
      <td style="color:var(--text-muted)">${l.session_id ? '#' + l.session_id : '—'}</td>
      <td style="color:var(--text-muted);white-space:nowrap">${fmtBR(l.created_at)}</td>
      <td style="display:flex;gap:6px">
        <button class="btn btn-secondary" style="font-size:11px;padding:4px 10px"
                onclick="openLogDetail(${l.id})">
          <i class="bi bi-eye"></i>
        </button>
        <button class="btn" style="font-size:11px;padding:4px 10px;background:rgba(255,122,89,.15);color:var(--error);border:1px solid rgba(255,122,89,.4)"
                onclick="deleteLog(${l.id})">
          <i class="bi bi-trash"></i>
        </button>
      </td>
    </tr>`;
  }).join('');
}

function renderLogsPagination(total, perPage, currentPage) {
  const totalPages = Math.ceil(total / perPage);
  const el = document.getElementById('logs-pagination');
  if (totalPages <= 1) { el.innerHTML = ''; return; }
  el.innerHTML = Array.from({ length: totalPages }, (_, i) => i + 1).map(i =>
    `<button class="page-btn${i === currentPage ? ' active' : ''}" onclick="loadLogs(${i})">${i}</button>`
  ).join('');
}

function openLogDetail(id) {
  const l = logsCache[id];
  if (!l) { toast('Log não encontrado.', 'error'); return; }

  const lvlClass = l.level === 'CRITICAL' ? 'badge-critical'
                 : l.level === 'WARNING'  ? 'badge-warning'
                 :                          'badge-error';
  const origin   = escHtml(ORIGIN_LABEL[l.origin] || l.origin);

  document.getElementById('log-detail-content').innerHTML = `
    <div class="log-detail-meta">
      <span class="badge ${lvlClass}">${l.level}</span>
      <span class="badge badge-individual">${origin}</span>
      ${l.session_id ? `<span class="badge badge-ensemble">Sessão #${l.session_id}</span>` : ''}
      <span style="color:var(--text-muted);font-size:12px;margin-left:auto">${fmtBR(l.created_at)}</span>
    </div>
    <div style="margin-bottom:16px">
      <strong>Mensagem</strong>
      <p class="log-detail-msg">${escHtml(l.message || '—')}</p>
    </div>
    ${l.traceback
      ? `<div><strong>Traceback</strong><pre class="traceback-pre">${escHtml(l.traceback)}</pre></div>`
      : `<p style="color:var(--text-muted)">Sem traceback disponível.</p>`
    }
  `;
  show('modal-log-detail');
}

function closeLogModal() { hide('modal-log-detail'); }

async function deleteLog(id) {
  if (!confirm('Remover este registro de erro?')) return;
  try {
    await fetch(`${API}/error-logs/${id}`, { method: 'DELETE', credentials: 'include' });
    toast('Log removido.', 'success');
    loadLogs(logsCurrentPage);
  } catch {
    toast('Erro ao remover log.', 'error');
  }
}

document.getElementById('btn-load-logs').addEventListener('click', () => loadLogs(1));

document.getElementById('btn-clear-logs').addEventListener('click', async () => {
  if (!confirm('Limpar TODOS os logs de erro? Esta ação não pode ser desfeita.')) return;
  try {
    await fetch(`${API}/error-logs/clear`, { method: 'POST', credentials: 'include' });
    toast('Todos os logs foram removidos.', 'success');
    loadLogs(1);
  } catch {
    toast('Erro ao limpar logs.', 'error');
  }
});

// ── GRAD-CAM EM LOTE ──────────────────────────────────────────────────────────

async function openBatchGradCAM(imgName) {
  const basename = imgName.split('/').pop().split('\\').pop();
  const file = _batchFileMap[imgName] || _batchFileMap[basename];
  if (!file) { toast('Imagem não disponível em memória. Selecione as imagens novamente.', 'error'); return; }
  if (!_batchSessId) { toast('Sessão não identificada.', 'error'); return; }

  document.getElementById('bgcam-filename').textContent = basename;
  show('modal-batch-gradcam');
  show('bgcam-loading');
  hide('bgcam-error');
  hide('bgcam-result');

  try {
    const form = new FormData();
    form.append('session_id', _batchSessId);
    form.append('image', file);
    const res  = await fetch(`${API}/gradcam`, { method: 'POST', body: form, credentials: 'include' });
    const data = await res.json();
    if (!res.ok || data.error) {
      const el = document.getElementById('bgcam-error');
      el.textContent = data.error || 'Erro ao gerar Grad-CAM.';
      show('bgcam-error');
      return;
    }
    document.getElementById('bgcam-img').src = `data:image/jpeg;base64,${data.image_b64}`;
    document.getElementById('bgcam-pred').innerHTML =
      `CNN prediz: <strong>${data.pred_class}</strong> com <strong>${data.confidence}%</strong> de confiança.`;
    show('bgcam-result');
  } catch {
    const el = document.getElementById('bgcam-error');
    el.textContent = 'Erro ao conectar com o servidor.';
    show('bgcam-error');
  } finally {
    hide('bgcam-loading');
  }
}

function closeBatchGradCAMModal() {
  hide('modal-batch-gradcam');
  document.getElementById('bgcam-img').src = '';
}

// ── GRAD-CAM ───────────────────────────────────────────────────────────────────

async function loadGradCAM() {
  if (!_currentSessId || !_currentImageFile) return;

  const btn = document.getElementById('btn-show-gradcam');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Analisando...';
  hide('gradcam-result');
  hide('gradcam-error');
  show('gradcam-loading');

  try {
    const form = new FormData();
    form.append('session_id', _currentSessId);
    form.append('image', _currentImageFile);

    const res  = await fetch(`${API}/gradcam`, { method: 'POST', body: form, credentials: 'include' });
    const data = await res.json();

    if (!res.ok || data.error) {
      const errEl = document.getElementById('gradcam-error');
      errEl.textContent = data.error || 'Erro ao gerar Grad-CAM.';
      show('gradcam-error');
      return;
    }

    document.getElementById('gradcam-img').src = `data:image/jpeg;base64,${data.image_b64}`;
    document.getElementById('gradcam-pred').innerHTML =
      `CNN prediz: <strong>${data.pred_class}</strong> com <strong>${data.confidence}%</strong> de confiança.`;
    show('gradcam-result');
    btn.innerHTML = '<i class="bi bi-arrow-clockwise"></i> Atualizar Grad-CAM';
  } catch {
    const errEl = document.getElementById('gradcam-error');
    errEl.textContent = 'Erro ao conectar com o servidor.';
    show('gradcam-error');
    btn.innerHTML = '<i class="bi bi-eye-fill"></i> Ver análise visual (Grad-CAM)';
  } finally {
    hide('gradcam-loading');
    btn.disabled = false;
  }
}

// ── LIGHTBOX ───────────────────────────────────────────────────────────────────

let _lbScale = 1;

function openLightbox(src, label) {
  const img = document.getElementById('lightbox-img');
  img.src   = src;
  img.alt   = label || '';
  _lbScale  = 1;
  img.style.transform = 'scale(1)';
  img.style.cursor    = 'zoom-in';
  show('lightbox');
  document.addEventListener('keydown', _lbKeyHandler);
}

function closeLightbox(e) {
  if (e && e.target === document.getElementById('lightbox-img')) return;
  hide('lightbox');
  document.removeEventListener('keydown', _lbKeyHandler);
}

function _lbKeyHandler(e) {
  if (e.key === 'Escape') closeLightbox();
}

document.getElementById('lightbox-img').addEventListener('click', e => {
  e.stopPropagation();
  _lbScale = _lbScale === 1 ? 2.2 : 1;
  e.target.style.transform = `scale(${_lbScale})`;
  e.target.style.cursor    = _lbScale === 1 ? 'zoom-in' : 'zoom-out';
});

document.getElementById('lightbox').addEventListener('wheel', e => {
  e.preventDefault();
  _lbScale = Math.min(5, Math.max(0.5, _lbScale - e.deltaY * 0.002));
  const img = document.getElementById('lightbox-img');
  img.style.transform = `scale(${_lbScale})`;
  img.style.cursor    = _lbScale <= 1 ? 'zoom-in' : 'zoom-out';
}, { passive: false });

function escHtml(str) {
  return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

// Converte ISO date string para DD/MM/AAAA HH:MM
function fmtBR(iso) {
  if (!iso) return '—';
  const s = (iso || '').slice(0, 16).replace('T', ' ');
  const [date, time] = s.split(' ');
  if (!date || !date.includes('-')) return s;
  const [y, m, d] = date.split('-');
  return time ? `${d}/${m}/${y} ${time}` : `${d}/${m}/${y}`;
}

// ── HELPERS ────────────────────────────────────────────────────────────────────

function show(id) { document.getElementById(id).classList.remove('hidden'); }
function hide(id) { document.getElementById(id).classList.add('hidden'); }

// Toast
function toast(msg, type = 'info', duration = 3000) {
  const el = document.createElement('div');
  el.className = `toast toast-${type}`;
  el.textContent = msg;
  document.getElementById('toast-container').appendChild(el);
  setTimeout(() => {
    el.classList.add('hide');
    setTimeout(() => el.remove(), 350);
  }, duration);
}

// Spinner em botão
function btnLoading(id, loading, label = '') {
  const btn = document.getElementById(id);
  btn.disabled = loading;
  btn.innerHTML = loading
    ? `<span class="spinner"></span> Carregando...`
    : label;
}

// Skeleton em tbody
function skeletonTable(tbodyId, cols = 4, rows = 4) {
  const tbody = document.getElementById(tbodyId) || document.querySelector(`#${tbodyId} tbody`);
  if (!tbody) return;
  tbody.innerHTML = Array.from({ length: rows }, () =>
    `<tr class="skeleton-row">${Array.from({ length: cols }, () =>
      `<td><span>&nbsp;</span></td>`).join('')}</tr>`
  ).join('');
}

// Count-up animado
function countUp(id, target, suffix = '', decimals = 0) {
  const el = document.getElementById(id);
  if (!el || target === null || target === undefined) return;
  const duration = 800;
  const start    = performance.now();
  const from     = 0;
  function step(now) {
    const t   = Math.min((now - start) / duration, 1);
    const val = from + (target - from) * (t < .5 ? 2*t*t : -1+(4-2*t)*t);
    el.textContent = val.toFixed(decimals) + suffix;
    if (t < 1) requestAnimationFrame(step);
    else {
      el.textContent = target.toFixed(decimals) + suffix;
      el.style.animation = 'countPulse .3s ease';
      setTimeout(() => el.style.animation = '', 300);
    }
  }
  requestAnimationFrame(step);
}
