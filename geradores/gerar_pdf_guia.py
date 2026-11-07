from fpdf import FPDF
from fpdf.enums import XPos, YPos

FONT_DIR  = 'C:/Windows/Fonts/'
ACCENT    = (91, 140, 255)
GOLD      = (185, 146, 42)
SUCCESS   = (39, 180, 160)
ERROR     = (220, 80, 50)
DARK      = (30, 42, 70)
MUTED     = (120, 135, 165)
WHITE     = (255, 255, 255)
LIGHT     = (240, 244, 255)
BORDER    = (196, 207, 235)

class PDF(FPDF):
    def setup_fonts(self):
        self.add_font('Arial', '',  FONT_DIR + 'arial.ttf')
        self.add_font('Arial', 'B', FONT_DIR + 'arialbd.ttf')
        self.add_font('Arial', 'I', FONT_DIR + 'ariali.ttf')
        self.add_font('Arial', 'BI', FONT_DIR + 'arialbi.ttf')

    def header(self):
        self.set_fill_color(*DARK)
        self.rect(0, 0, 210, 18, 'F')
        self.set_font('Arial', 'B', 11)
        self.set_text_color(*GOLD)
        self.set_xy(10, 4)
        self.cell(0, 10, 'TCC IA  -  Guia de Testes do Sistema', align='L')
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

    def check(self, txt, success=True):
        color = SUCCESS if success else ERROR
        icon  = '[OK]' if success else '[X]'
        self.set_x(14)
        self.set_font('Arial', 'B', 8)
        self.set_text_color(*color)
        self.cell(12, 5, icon)
        self.set_font('Arial', '', 9)
        self.set_text_color(*DARK)
        self.multi_cell(178, 5, txt, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def note(self, txt):
        self.set_fill_color(*LIGHT)
        self.set_draw_color(*BORDER)
        self.set_line_width(0.3)
        self.set_x(10)
        self.set_font('Arial', 'I', 8.5)
        self.set_text_color(*MUTED)
        self.multi_cell(190, 5, txt, border=1, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def table_header(self, cols, widths):
        self.set_fill_color(*DARK)
        self.set_text_color(*WHITE)
        self.set_font('Arial', 'B', 8)
        self.set_x(10)
        for col, w in zip(cols, widths):
            self.cell(w, 7, col, border=1, fill=True, align='C')
        self.ln()

    def table_row(self, cols, widths, fill=False, status_col=False):
        self.set_fill_color(*LIGHT)
        self.set_font('Arial', '', 8)
        self.set_x(10)
        for i, (col, w) in enumerate(zip(cols, widths)):
            if status_col and i == len(cols) - 1:
                self.set_text_color(*SUCCESS)
                self.set_font('Arial', 'B', 9)
            else:
                self.set_text_color(*DARK)
                self.set_font('Arial', '', 8)
            self.cell(w, 6, col, border=1, fill=fill, align='C' if i != 1 else 'L')
        self.ln()


pdf = PDF()
pdf.setup_fonts()
pdf.set_auto_page_break(auto=True, margin=16)
pdf.add_page()

# CAPA
pdf.set_fill_color(*DARK)
pdf.rect(0, 18, 210, 60, 'F')
pdf.set_font('Arial', 'B', 28)
pdf.set_text_color(*WHITE)
pdf.set_xy(0, 30)
pdf.cell(210, 14, 'GUIA DE TESTES', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font('Arial', 'B', 16)
pdf.set_text_color(*GOLD)
pdf.cell(210, 10, 'TCC IA - Sistema de Classificacao de Imagens', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font('Arial', '', 10)
pdf.set_text_color(*MUTED)
pdf.cell(210, 8, 'Ensemble Learning aplicado a imagens medicas', align='C')
pdf.ln(20)
pdf.note('Pre-requisitos: Flask rodando via start.bat  |  MySQL ativo com banco tcc_imagens  |  Dataset separado por classes')
pdf.ln(2)

# 1. AUTENTICACAO
pdf.section_title('1. AUTENTICACAO')
pdf.sub_title('1.1  Criar conta')
pdf.step(1, 'Acesse http://localhost:5000/auth')
pdf.step(2, 'Clique em "Criar conta"')
pdf.step(3, 'Preencha nome, e-mail e senha')
pdf.step(4, 'Clique em "Cadastrar"')
pdf.check('Redireciona para a tela de verificacao de e-mail')

pdf.sub_title('1.2  Verificacao de e-mail')
pdf.step(1, 'Verifique o e-mail cadastrado (ou o terminal do Flask se o envio falhar)')
pdf.step(2, 'Digite o codigo de 6 digitos recebido e clique em "Verificar"')
pdf.check('Redireciona para o Dashboard')

pdf.sub_title('1.3  Login')
pdf.step(1, 'Preencha e-mail e senha e clique em "Entrar"')
pdf.check('Abre o Dashboard com dados corretos')
pdf.check('Exibe "E-mail ou senha incorretos" com dados errados', success=False)
pdf.check('Exibe aviso de conta nao verificada se e-mail pendente', success=False)

pdf.sub_title('1.4  Esqueci minha senha')
pdf.step(1, 'Clique em "Esqueci minha senha" e informe o e-mail')
pdf.step(2, 'Receba o codigo por e-mail (ou no terminal do Flask)')
pdf.step(3, 'Digite o codigo e a nova senha')
pdf.check('Senha redefinida com sucesso, redireciona para login')

pdf.sub_title('1.5  Logout')
pdf.step(1, 'Clique em "Sair" na sidebar (desktop) ou botao no header (mobile)')
pdf.check('Redireciona para /auth e impede acesso sem login')

pdf.sub_title('1.6  Sessao de 24 horas')
pdf.check('Apos 24h sem atividade qualquer acao redireciona para login')

# 2. DASHBOARD
pdf.section_title('2. DASHBOARD')
pdf.step(1, 'Faca login e observe os 4 cards: Sessoes concluidas, Predicoes realizadas, Melhor acuracia, Modelo destaque')
pdf.step(2, 'Observe o grafico de barras com acuracia media por modelo')
pdf.step(3, 'Observe as tabelas "Ultimas sessoes" e "Ultimas predicoes"')
pdf.check('Com banco vazio: cards mostram 0 e travessao, tabelas mostram mensagem vazia')
pdf.check('Apos treinar: todos os dados sao preenchidos automaticamente')

# 3. TREINAR
pdf.section_title('3. TREINAR MODELOS')
pdf.step(1, 'Va em "Treinar" na navegacao')
pdf.step(2, 'Digite o caminho completo do dataset (ex: C:\\Users\\andre\\Documents\\dataset)')
pdf.note('A pasta deve conter subpastas por classe: dataset/NORMAL/  e  dataset/PNEUMONIA/')
pdf.step(3, 'Clique em "Iniciar Treinamento"')
pdf.check('Barra de progresso aparece com mensagens de status em tempo real')
pdf.check('Ao concluir: mensagem de sucesso + notificacao do navegador (se permitido)')
pdf.check('Botao "Ver Resultados" aparece ao final')
pdf.body('Modelos treinados: KNN, SVM, Random Forest, Logistic Regression, Naive Bayes, Voting Hard, Voting Soft, Stacking')

# 4. RESULTADOS
pdf.section_title('4. RESULTADOS')
pdf.step(1, 'Va em "Resultados", selecione uma sessao concluida e clique em "Carregar"')

pdf.sub_title('4.1  Tabela comparativa')
pdf.check('8 colunas: Modelo, Tipo, CV 10-fold, Acuracia, Precisao, Recall, F1-Score, ROC AUC')
pdf.check('Badge "melhor" no modelo com maior CV  |  Badge "ensemble" / "individual" por tipo')

pdf.sub_title('4.2  Curva ROC')
pdf.step(1, 'Selecione um modelo no seletor acima do grafico')
pdf.check('Grafico de linha FPR x TPR com valor de AUC na legenda')
pdf.check('Linha pontilhada de referencia (classificador aleatorio)')
pdf.check('Trocar o modelo atualiza o grafico instantaneamente')

pdf.sub_title('4.3  Grafico comparativo')
pdf.check('Barras lado a lado: CV 10-fold e Acuracia de Teste por modelo')
pdf.check('Cores adaptam ao tema claro/escuro')

pdf.sub_title('4.4  Matriz de confusao')
pdf.step(1, 'Selecione um modelo no seletor')
pdf.check('Grid colorido: verde (acertos) e vermelho (erros)')

pdf.sub_title('4.5  Exportar CSV')
pdf.step(1, 'Clique em "Exportar CSV" no cabecalho da tabela')
pdf.check('Download do arquivo resultados_sessao_X.csv com todas as metricas')

# 5. TESTAR
pdf.section_title('5. TESTAR IMAGEM')
pdf.step(1, 'Selecione uma sessao concluida e o modelo desejado (padrao: Stacking)')

pdf.sub_title('5.1  Imagem unica')
pdf.step(1, 'Selecione 1 imagem na area de upload')
pdf.check('Miniatura da imagem aparece abaixo da area')
pdf.step(2, 'Clique em "Classificar"')
pdf.check('Card com classe predita, confianca em % e modelo usado')

pdf.sub_title('5.2  Lote de imagens (batch)')
pdf.step(1, 'Selecione varias imagens de uma vez (Ctrl+clique)')
pdf.check('Miniaturas de todas as imagens aparecem')
pdf.step(2, 'Clique em "Classificar"')
pdf.check('Tabela com resultado individual de cada imagem')

# 6. HISTORICO
pdf.section_title('6. HISTORICO')
pdf.step(1, 'Selecione uma sessao e clique em "Carregar"')
pdf.check('Tabela com todas as predicoes: imagem, modelo, classe, confianca e data/hora')

# 7. PERFIL
pdf.section_title('7. PERFIL')
pdf.check('Nome, e-mail, data de cadastro e badge de verificacao visiveis')

pdf.sub_title('7.1  Editar dados')
pdf.step(1, 'Altere o nome e clique em "Salvar alteracoes"')
pdf.check('Nome atualizado na sidebar e no perfil')
pdf.check('Alterar e-mail exige nova verificacao')

pdf.sub_title('7.2  Trocar senha')
pdf.step(1, 'Clique em "Trocar Senha" e preencha os campos no modal')
pdf.check('Barra de forca da senha atualiza em tempo real')
pdf.check('Regras ficam verdes conforme criterios atendidos')
pdf.check('Senha alterada com mensagem de sucesso')

# 8. TEMA
pdf.section_title('8. TEMA CLARO / ESCURO')
pdf.step(1, 'Clique no botao de tema na sidebar (desktop) ou header (mobile)')
pdf.check('Interface alterna completamente entre claro e escuro')
pdf.check('Graficos atualizam as cores automaticamente')
pdf.check('Preferencia salva - persiste ao reabrir o sistema')

# 9. MOBILE
pdf.section_title('9. MOBILE  (tela menor ou igual a 768px)')
pdf.note('Redimensione o navegador ou use DevTools: F12 -> icone de celular')
pdf.check('Sidebar some completamente')
pdf.check('Header no topo com dragao, titulo "TCC IA", botao de tema e logout')
pdf.check('Barra de navegacao fixa na parte inferior com 6 itens')
pdf.check('Botao ativo destacado em azul')
pdf.check('Cards do Dashboard em grade 2x2')
pdf.check('Tela de login ocupa a tela toda (painel do dragao some)')

# 10. SEGURANCA
pdf.section_title('10. SEGURANCA')
pdf.table_header(['Teste', 'Resultado Esperado'], [90, 100])
rows = [
    ('Acessar / sem login',            'Redireciona para /auth'),
    ('11 logins errados seguidos',      'Bloqueio temporario (rate limit)'),
    ('Sessao apos 24h',                 'Redireciona para login'),
    ('Codigo de verificacao errado',    'Mensagem "Codigo invalido"'),
    ('Token de reset expirado',         'Mensagem de erro'),
]
for i, (a, b) in enumerate(rows):
    pdf.table_row([a, b], [90, 100], fill=(i % 2 == 0))

# RESUMO
pdf.ln(4)
pdf.section_title('RESUMO DAS FUNCIONALIDADES')
pdf.table_header(['#', 'Funcionalidade', 'Status'], [12, 158, 20])
features = [
    ('1',  'Cadastro e verificacao de e-mail'),
    ('2',  'Login / Logout'),
    ('3',  'Redefinicao de senha'),
    ('4',  'Sessao de 24 horas'),
    ('5',  'Dashboard com metricas'),
    ('6',  'Treinamento com 8 modelos'),
    ('7',  'Barra de progresso em tempo real'),
    ('8',  'Notificacao do navegador ao concluir'),
    ('9',  'Tabela com F1, Precisao, Recall, ROC AUC'),
    ('10', 'Curva ROC interativa'),
    ('11', 'Grafico comparativo por modelo'),
    ('12', 'Matriz de confusao'),
    ('13', 'Exportar resultados em CSV'),
    ('14', 'Predicao de imagem unica'),
    ('15', 'Predicao em lote (batch)'),
    ('16', 'Historico de predicoes por sessao'),
    ('17', 'Perfil editavel'),
    ('18', 'Trocar senha com barra de forca'),
    ('19', 'Tema claro / escuro persistente'),
    ('20', 'Interface responsiva (mobile)'),
    ('21', 'Rate limiting no login'),
    ('22', 'Sessoes isoladas por usuario'),
]
for i, (n, f) in enumerate(features):
    fill = i % 2 == 0
    pdf.set_fill_color(*LIGHT)
    pdf.set_x(10)
    pdf.set_text_color(*DARK)
    pdf.set_font('Arial', '', 8)
    pdf.cell(12, 6, n, border=1, fill=fill, align='C')
    pdf.cell(158, 6, f, border=1, fill=fill)
    pdf.set_text_color(*SUCCESS)
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(20, 6, '[OK]', border=1, fill=fill, align='C')
    pdf.ln()

pdf.output('GUIA_DE_TESTES.pdf')
print('PDF gerado com sucesso: GUIA_DE_TESTES.pdf')
