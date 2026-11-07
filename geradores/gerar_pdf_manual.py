from fpdf import FPDF
from fpdf.enums import XPos, YPos

FONT_DIR = 'C:/Windows/Fonts/'
ACCENT   = (91, 140, 255)
GOLD     = (185, 146, 42)
SUCCESS  = (39, 180, 160)
ERROR    = (220, 80, 50)
DARK     = (30, 42, 70)
MUTED    = (120, 135, 165)
WHITE    = (255, 255, 255)
LIGHT    = (240, 244, 255)
BORDER   = (196, 207, 235)

class PDF(FPDF):
    def setup_fonts(self):
        self.add_font('Arial', '',   FONT_DIR + 'arial.ttf')
        self.add_font('Arial', 'B',  FONT_DIR + 'arialbd.ttf')
        self.add_font('Arial', 'I',  FONT_DIR + 'ariali.ttf')
        self.add_font('Arial', 'BI', FONT_DIR + 'arialbi.ttf')

    def header(self):
        self.set_fill_color(*DARK)
        self.rect(0, 0, 210, 18, 'F')
        self.set_font('Arial', 'B', 11)
        self.set_text_color(*GOLD)
        self.set_xy(10, 4)
        self.cell(0, 10, 'TCC IA  -  Manual do Usuario', align='L')
        self.set_text_color(*MUTED)
        self.set_font('Arial', '', 8)
        self.set_xy(0, 5)
        self.cell(200, 8, f'Pagina {self.page_no()}', align='R')
        self.ln(14)

    def footer(self):
        self.set_y(-12)
        self.set_fill_color(*DARK)
        self.rect(0, self.get_y(), 210, 12, 'F')
        self.set_font('Arial', '', 8)
        self.set_text_color(*MUTED)
        self.cell(0, 10, 'TCC - Classificacao de Imagens com Ensemble Learning', align='C')

    def section_title(self, txt):
        self.ln(4)
        self.set_fill_color(*DARK)
        self.set_text_color(*WHITE)
        self.set_font('Arial', 'B', 12)
        self.set_x(10)
        self.cell(190, 9, f'  {txt}', fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def sub_title(self, txt):
        self.ln(2)
        self.set_text_color(*ACCENT)
        self.set_font('Arial', 'B', 10)
        self.set_x(10)
        self.cell(190, 7, txt, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(*ACCENT)
        self.set_line_width(0.4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)

    def body(self, txt):
        self.set_text_color(*DARK)
        self.set_font('Arial', '', 9)
        self.set_x(10)
        self.multi_cell(190, 5, txt)

    def step(self, num, txt):
        self.set_x(14)
        self.set_font('Arial', 'B', 9)
        self.set_text_color(*MUTED)
        self.cell(8, 5, f'{num}.', align='R')
        self.set_font('Arial', '', 9)
        self.set_text_color(*DARK)
        self.multi_cell(182, 5, f' {txt}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def tip(self, txt):
        self.set_fill_color(*LIGHT)
        self.set_draw_color(*BORDER)
        self.set_line_width(0.3)
        self.set_x(10)
        self.set_font('Arial', 'I', 8.5)
        self.set_text_color(*MUTED)
        self.multi_cell(190, 5, f'  Dica: {txt}', border=1, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def warning(self, txt):
        self.set_fill_color(255, 248, 230)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.3)
        self.set_x(10)
        self.set_font('Arial', 'I', 8.5)
        self.set_text_color(140, 100, 20)
        self.multi_cell(190, 5, f'  Atencao: {txt}', border=1, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def table_header(self, cols, widths):
        self.set_fill_color(*DARK)
        self.set_text_color(*WHITE)
        self.set_font('Arial', 'B', 8)
        self.set_x(10)
        for col, w in zip(cols, widths):
            self.cell(w, 7, col, border=1, fill=True, align='C')
        self.ln()

    def table_row(self, cols, widths, fill=False, bold_first=False):
        self.set_fill_color(*LIGHT)
        self.set_x(10)
        for i, (col, w) in enumerate(zip(cols, widths)):
            self.set_text_color(*DARK)
            if bold_first and i == 0:
                self.set_font('Arial', 'B', 8)
            else:
                self.set_font('Arial', '', 8)
            self.cell(w, 6, col, border=1, fill=fill, align='L' if i == 0 else 'C')
        self.ln()


pdf = PDF()
pdf.setup_fonts()
pdf.set_auto_page_break(auto=True, margin=16)
pdf.add_page()

# ── CAPA ──────────────────────────────────────────────────────────────────────
pdf.set_fill_color(*DARK)
pdf.rect(0, 18, 210, 68, 'F')
pdf.set_font('Arial', 'B', 30)
pdf.set_text_color(*WHITE)
pdf.set_xy(0, 32)
pdf.cell(210, 14, 'MANUAL DO USUARIO', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font('Arial', 'B', 16)
pdf.set_text_color(*GOLD)
pdf.cell(210, 10, 'TCC IA - Sistema de Classificacao de Imagens', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font('Arial', '', 10)
pdf.set_text_color(*MUTED)
pdf.cell(210, 8, 'Ensemble Learning aplicado a classificacao de imagens medicas', align='C')
pdf.ln(28)

pdf.set_font('Arial', '', 9)
pdf.set_text_color(*DARK)
pdf.set_x(10)
pdf.multi_cell(190, 5,
    'Este manual descreve como utilizar todas as funcionalidades do sistema TCC IA, '
    'desde o primeiro acesso ate a analise dos resultados dos modelos de Machine Learning.')
pdf.ln(4)
pdf.tip('Mantenha o servidor ativo (start.bat) e o MySQL rodando antes de acessar o sistema.')

# ── VISAO GERAL ───────────────────────────────────────────────────────────────
pdf.section_title('VISAO GERAL DO SISTEMA')
pdf.body(
    'O TCC IA e uma plataforma web para treinamento e comparacao de modelos de Machine Learning '
    'voltada a classificacao de imagens medicas. O sistema realiza automaticamente o treinamento '
    'de 8 modelos (5 individuais + 3 em ensemble), calcula metricas detalhadas e permite testar '
    'novas imagens com os modelos treinados.\n'
)
pdf.table_header(['Modelos Individuais', 'Modelos Ensemble'], [95, 95])
pdf.table_row(['KNN (K-Nearest Neighbors)',   'Voting Hard'],  [95, 95], fill=True)
pdf.table_row(['SVM (Support Vector Machine)', 'Voting Soft'], [95, 95])
pdf.table_row(['Random Forest',               'Stacking (recomendado)'], [95, 95], fill=True)
pdf.table_row(['Regressao Logistica',         ''],             [95, 95])
pdf.table_row(['Naive Bayes',                 ''],             [95, 95], fill=True)
pdf.ln(2)

pdf.sub_title('Estrutura esperada do dataset')
pdf.body(
    'O dataset deve estar organizado em subpastas, uma por classe:\n'
    '  meu_dataset/\n'
    '      NORMAL/      (imagem1.jpg, imagem2.png ...)\n'
    '      PNEUMONIA/   (imagem1.jpg, imagem2.png ...)\n\n'
    'Formatos aceitos: .jpg  .jpeg  .png  .bmp  .tiff  .tif'
)
pdf.warning('O sistema foi desenvolvido para classificacao binaria (2 classes).')

# ── 1. AUTENTICACAO ───────────────────────────────────────────────────────────
pdf.section_title('1.  ACESSO AO SISTEMA')

pdf.sub_title('1.1  Criar uma conta')
pdf.step(1, 'Acesse http://localhost:5000/auth no navegador')
pdf.step(2, 'Clique em "Criar conta"')
pdf.step(3, 'Preencha os campos: Nome, E-mail, Senha e Confirmar senha')
pdf.step(4, 'Acompanhe o indicador de forca da senha - deve ficar verde')
pdf.step(5, 'Clique em "Cadastrar"')
pdf.tip('A senha precisa ter no minimo 8 caracteres, uma maiuscula, uma minuscula, um numero e um caractere especial.')

pdf.sub_title('1.2  Verificar o e-mail')
pdf.step(1, 'Verifique a caixa de entrada do e-mail cadastrado')
pdf.step(2, 'Localize o e-mail com o codigo de 6 digitos')
pdf.step(3, 'Digite o codigo na tela e clique em "Verificar"')
pdf.tip('Caso nao receba o e-mail, clique em "Reenviar codigo".')

pdf.sub_title('1.3  Fazer login')
pdf.step(1, 'Acesse http://localhost:5000/auth')
pdf.step(2, 'Preencha seu e-mail e senha')
pdf.step(3, 'Clique em "Entrar"')

pdf.sub_title('1.4  Recuperar senha esquecida')
pdf.step(1, 'Na tela de login, clique em "Esqueci a senha"')
pdf.step(2, 'Digite seu e-mail e clique em "Enviar link"')
pdf.step(3, 'Copie o token recebido por e-mail')
pdf.step(4, 'Cole o token, defina a nova senha e clique em "Redefinir"')
pdf.step(5, 'Faca login com a nova senha')

# ── 2. DASHBOARD ──────────────────────────────────────────────────────────────
pdf.section_title('2.  DASHBOARD')
pdf.body('A pagina inicial exibe um resumo geral da sua atividade no sistema.\n')
pdf.table_header(['Card', 'O que mostra'], [60, 130])
rows_dash = [
    ('Sessoes concluidas',  'Total de treinos finalizados'),
    ('Predicoes realizadas','Total de imagens classificadas'),
    ('Melhor acuracia',     'Maior acuracia obtida em qualquer sessao'),
    ('Modelo destaque',     'Nome do modelo com melhor desempenho'),
]
for i, (a, b) in enumerate(rows_dash):
    pdf.table_row([a, b], [60, 130], fill=(i % 2 == 0), bold_first=True)
pdf.ln(2)
pdf.body(
    'Abaixo dos cards ha um grafico de barras com a acuracia media de cada modelo '
    'em todas as suas sessoes, comparando CV 10-fold e Acuracia de Teste.\n\n'
    'As tabelas "Ultimas sessoes" e "Ultimas predicoes" mostram as atividades mais recentes.'
)

# ── 3. TREINAR ────────────────────────────────────────────────────────────────
pdf.section_title('3.  TREINAR UM MODELO')

pdf.sub_title('Passo a passo')
pdf.step(1, 'Clique em "Treinar" no menu lateral')
pdf.step(2, 'No campo "Caminho do dataset", cole o caminho completo da pasta raiz')
pdf.step(3, 'Exemplo Windows:  C:\\Users\\andre\\Documents\\meu_dataset')
pdf.step(4, 'Clique em "Iniciar Treinamento"')
pdf.step(5, 'Acompanhe a barra de progresso e as mensagens de status')
pdf.step(6, 'Ao concluir, clique em "Ver Resultados"')

pdf.sub_title('O que acontece durante o treino')
pdf.body(
    '1. Leitura e pre-processamento das imagens (redimensionamento 128x128, escala de cinza)\n'
    '2. Extracao de features HOG\n'
    '3. Divisao: 80% treino / 20% teste (estratificada)\n'
    '4. Treinamento dos 5 modelos individuais + 3 ensembles\n'
    '5. Validacao cruzada 10-fold\n'
    '6. Calculo de metricas, curvas ROC e matrizes de confusao'
)
pdf.warning('O tempo de treino varia com o tamanho do dataset. Datasets grandes podem levar varios minutos.')

# ── 4. RESULTADOS ─────────────────────────────────────────────────────────────
pdf.section_title('4.  RESULTADOS')
pdf.step(1, 'Clique em "Resultados" no menu lateral')
pdf.step(2, 'Selecione a sessao desejada no seletor "Sessao de treino"')

pdf.sub_title('4.1  Tabela comparativa de modelos')
pdf.body('Cada linha representa um modelo com as seguintes metricas:\n')
pdf.table_header(['Coluna', 'Descricao'], [45, 145])
rows_tab = [
    ('Modelo',       'Nome do modelo (trofeu marca o melhor da sessao)'),
    ('Tipo',         'Individual ou Ensemble'),
    ('CV 10-fold',   'Acuracia media na validacao cruzada (%)'),
    ('Acuracia Teste','Acuracia no conjunto de teste separado (%)'),
    ('Precisao',     'Proporcao de predicoes positivas corretas (%)'),
    ('Recall',       'Proporcao de positivos reais detectados (%)'),
    ('F1-Score',     'Media harmonica entre precisao e recall (%)'),
    ('ROC AUC',      'Area sob a curva ROC (0 a 1 - quanto maior, melhor)'),
]
for i, (a, b) in enumerate(rows_tab):
    pdf.table_row([a, b], [45, 145], fill=(i % 2 == 0), bold_first=True)

pdf.sub_title('4.2  Exportar resultados')
pdf.step(1, 'Clique em "Exportar CSV" no cabecalho da tabela')
pdf.body('Faz o download de uma planilha com todas as metricas da sessao.')

pdf.sub_title('4.3  Curva ROC')
pdf.step(1, 'Selecione o modelo desejado no seletor "Curva ROC"')
pdf.body('O grafico exibe a relacao entre taxa de verdadeiro positivo (TPR) e falso positivo (FPR).')
pdf.tip('Quanto mais a curva se aproxima do canto superior esquerdo, melhor o modelo.')

pdf.sub_title('4.4  Grafico comparativo')
pdf.body('Barras lado a lado dos valores de CV 10-fold e Acuracia Teste de todos os modelos.')

pdf.sub_title('4.5  Matriz de Confusao')
pdf.step(1, 'Selecione o modelo no seletor "Matriz de Confusao"')
pdf.body('O grid mostra quantas imagens foram classificadas corretamente (diagonal) e os erros.')

# ── 5. TESTAR ─────────────────────────────────────────────────────────────────
pdf.section_title('5.  TESTAR UMA IMAGEM')
pdf.step(1, 'Clique em "Testar Imagem" no menu lateral')
pdf.step(2, 'Selecione a sessao de treino que contem o modelo desejado')
pdf.step(3, 'Selecione o modelo (Stacking e recomendado)')
pdf.step(4, 'Arraste imagens para a area de upload ou clique para selecionar arquivos')
pdf.step(5, 'Clique em "Classificar"')

pdf.sub_title('Resultado para 1 imagem')
pdf.body('Exibe: classe predita, confianca em % e nome do modelo utilizado.')

pdf.sub_title('Resultado para multiplas imagens (lote)')
pdf.body('Uma tabela e exibida com cada imagem, sua classe predita e confianca correspondente.')
pdf.tip('Use Ctrl+clique para selecionar varias imagens de uma vez na janela de arquivo.')

# ── 6. HISTORICO ──────────────────────────────────────────────────────────────
pdf.section_title('6.  HISTORICO')
pdf.step(1, 'Clique em "Historico" no menu lateral')
pdf.step(2, 'Selecione uma sessao no filtro (ou deixe em branco para ver todas)')
pdf.body('A tabela exibe: nome da imagem, modelo usado, classe predita, confianca e data/hora.')

# ── 7. PERFIL ─────────────────────────────────────────────────────────────────
pdf.section_title('7.  PERFIL')

pdf.sub_title('7.1  Editar nome ou e-mail')
pdf.step(1, 'Clique em "Perfil" no menu lateral')
pdf.step(2, 'Altere o campo desejado (Nome ou E-mail)')
pdf.step(3, 'Clique em "Salvar alteracoes"')
pdf.warning('Alterar o e-mail exige verificacao do novo endereco via codigo enviado automaticamente.')

pdf.sub_title('7.2  Trocar senha')
pdf.step(1, 'Na secao Seguranca, clique em "Trocar Senha"')
pdf.step(2, 'Preencha a senha atual e a nova senha (duas vezes)')
pdf.step(3, 'Clique em "Salvar"')
pdf.tip('O indicador de forca da senha atualiza em tempo real conforme voce digita.')

# ── 8. PREFERENCIAS ───────────────────────────────────────────────────────────
pdf.section_title('8.  PREFERENCIAS E TEMA')
pdf.body(
    'Clique no icone de sol/lua no canto superior da barra lateral para alternar entre '
    'tema claro e escuro. A preferencia e salva automaticamente e mantida entre sessoes.'
)

# ── 9. SAIR ───────────────────────────────────────────────────────────────────
pdf.section_title('9.  SAIR DO SISTEMA')
pdf.body(
    'Clique em "Sair" no menu lateral (icone de saida). A tela de encerramento e exibida '
    'e voce e redirecionado para a tela de login automaticamente.'
)

# ── FAQ ───────────────────────────────────────────────────────────────────────
pdf.section_title('DUVIDAS FREQUENTES')
pdf.table_header(['Duvida', 'Resposta'], [80, 110])
faqs = [
    ('O treino travou ou nao avanca?',
     'Verifique o caminho do dataset e se as pastas tem imagens nos formatos aceitos.'),
    ('Nao recebi o e-mail de verificacao.',
     'Verifique spam. Em servidor local, o codigo pode aparecer no terminal do Flask.'),
    ('Qual modelo usar para predicao?',
     'Stacking e o mais preciso. Compare na secao Resultados antes de escolher.'),
    ('Posso usar mais de 2 classes?',
     'O sistema foi feito para classificacao binaria. Mais classes podem nao funcionar.'),
    ('Como interpretar o ROC AUC?',
     'Proximo de 1.0 = otimo. Abaixo de 0.7 = modelo com dificuldade de distinguir classes.'),
    ('O servidor nao inicia?',
     'Verifique se o MySQL esta rodando e se o banco tcc_imagens foi criado.'),
]
for i, (q, a) in enumerate(faqs):
    pdf.table_row([q, a], [80, 110], fill=(i % 2 == 0))

pdf.ln(6)
pdf.set_font('Arial', 'I', 8)
pdf.set_text_color(*MUTED)
pdf.set_x(10)
pdf.cell(190, 5, 'Manual do Usuario - TCC IA - Classificacao de Imagens com Ensemble Learning', align='C')

pdf.output('MANUAL_DO_USUARIO.pdf')
print('PDF gerado com sucesso: MANUAL_DO_USUARIO.pdf')
