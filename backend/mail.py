import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import GMAIL_SENDER, GMAIL_APP_PASSWORD

_CARD = (
    "background:#121A2F;color:#E8ECF3;border-radius:12px;"
    "padding:32px;max-width:480px;margin:0 auto;font-family:'Segoe UI',sans-serif"
)
_MONO = (
    "background:#0B1020;border:1px solid #243055;border-radius:8px;"
    "padding:20px 24px;text-align:center;margin:20px 0"
)


def _send(to: str, subject: str, html: str):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From']    = f'TCC IA <{GMAIL_SENDER}>'
    msg['To']      = to
    msg.attach(MIMEText(html, 'html', 'utf-8'))
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10) as smtp:
        smtp.login(GMAIL_SENDER, GMAIL_APP_PASSWORD)
        smtp.sendmail(GMAIL_SENDER, to, msg.as_string())


def send_verification_email(to: str, code: str):
    html = f"""
    <div style="{_CARD}">
      <h2 style="color:#5B8CFF;margin:0 0 8px">Verificação de E-mail</h2>
      <p style="color:#9BA7C2;margin:0 0 20px">
        Use o código abaixo para ativar sua conta no sistema <strong>TCC IA</strong>.
      </p>
      <div style="{_MONO}">
        <span style="font-family:monospace;font-size:34px;font-weight:800;
                     letter-spacing:10px;color:#D9B66B">{code}</span>
      </div>
      <p style="color:#9BA7C2;font-size:12px;margin:0">
        Válido por 24 horas. Não compartilhe este código.
      </p>
    </div>"""
    try:
        _send(to, 'TCC IA — Código de verificação', html)
    except Exception as e:
        print(f"\n{'='*50}")
        print(f"[MAIL] Falha ao enviar e-mail para {to}: {e}")
        print(f"[MAIL] CÓDIGO DE VERIFICAÇÃO: {code}")
        print(f"{'='*50}\n")


def send_reset_email(to: str, token: str):
    html = f"""
    <div style="{_CARD}">
      <h2 style="color:#5B8CFF;margin:0 0 8px">Recuperação de Senha</h2>
      <p style="color:#9BA7C2;margin:0 0 20px">
        Use o token abaixo para redefinir sua senha no sistema <strong>TCC IA</strong>.
      </p>
      <div style="{_MONO}">
        <span style="font-family:monospace;font-size:13px;font-weight:700;
                     word-break:break-all;color:#D9B66B">{token}</span>
      </div>
      <p style="color:#9BA7C2;font-size:12px;margin:0">
        Válido por 1 hora. Se não foi você, ignore este e-mail.
      </p>
    </div>"""
    try:
        _send(to, 'TCC IA — Token de recuperação de senha', html)
    except Exception as e:
        print(f"\n{'='*50}")
        print(f"[MAIL] Falha ao enviar e-mail para {to}: {e}")
        print(f"[MAIL] TOKEN DE RECUPERAÇÃO: {token}")
        print(f"{'='*50}\n")


def send_async(fn, *args):
    threading.Thread(target=fn, args=args, daemon=True).start()
