# Guia de Testes — TCC IA
> Sistema de Classificação de Imagens com Ensemble Learning

---

## Pré-requisitos

- Flask rodando: `./start.bat`
- MySQL ativo com banco `tcc_imagens`
- Dataset de imagens separado por pastas (ex: `NORMAL/` e `PNEUMONIA/`)

---

## 1. AUTENTICAÇÃO

### 1.1 Criar conta
1. Acesse `http://localhost:5000/auth`
2. Clique em **Criar conta**
3. Preencha nome, e-mail e senha
4. Clique em **Cadastrar**
5. ✅ Deve redirecionar para a tela de verificação de e-mail

### 1.2 Verificação de e-mail
1. Verifique o e-mail cadastrado (ou o terminal do Flask se o e-mail falhar)
2. Digite o código de 6 dígitos recebido
3. Clique em **Verificar**
4. ✅ Deve redirecionar para o sistema (Dashboard)

### 1.3 Login
1. Acesse `/auth` e preencha e-mail e senha
2. Clique em **Entrar**
3. ✅ Deve abrir o Dashboard
4. ❌ Senha errada → mensagem "E-mail ou senha incorretos"
5. ❌ Conta não verificada → mensagem de aviso

### 1.4 Esqueci minha senha
1. Clique em **Esqueci minha senha**
2. Digite o e-mail cadastrado
3. ✅ Código de redefinição enviado (ou exibido no terminal)
4. Digite o código e a nova senha
5. ✅ Senha alterada, redireciona para login

### 1.5 Logout
1. Clique em **Sair** na sidebar (desktop) ou ícone de saída no header (mobile)
2. ✅ Redireciona para `/auth`
3. Tentar acessar `/` sem estar logado → redireciona para `/auth`

### 1.6 Sessão expirada (24h)
- Após 24 horas sem atividade, qualquer ação redireciona para login
- ✅ Comportamento esperado — sessão permanente de 24h

---

## 2. DASHBOARD

1. Faça login e observe os 4 cards:
   - **Sessões concluídas** — total de treinamentos do usuário
   - **Predições realizadas** — total de imagens classificadas
   - **Melhor acurácia** — maior acurácia registrada
   - **Modelo destaque** — modelo com melhor desempenho

2. Observe o gráfico de barras com acurácia média por modelo
3. Observe a tabela **Últimas sessões**
4. Observe a tabela **Últimas predições**
5. ✅ Com banco vazio: cards mostram `0` e `—`, tabelas mostram "Nenhuma sessão/predição"
6. ✅ Após treinar: dados preenchidos automaticamente

---

## 3. TREINAR MODELOS

1. Vá em **Treinar** na navegação
2. Digite o caminho completo do dataset:
   ```
   C:\Users\andre\Documents\dataset
   ```
   A pasta deve conter subpastas por classe:
   ```
   dataset/
   ├── NORMAL/
   │   ├── img001.jpg
   │   └── ...
   └── PNEUMONIA/
       ├── img002.jpg
       └── ...
   ```
3. Clique em **Iniciar Treinamento**
4. ✅ Barra de progresso aparece com mensagens de status
5. ✅ Ao concluir: mensagem de sucesso + notificação do navegador (se permitido)
6. ✅ Botão **Ver Resultados** aparece ao final

**Modelos treinados:** KNN, SVM, Random Forest, Logistic Regression, Naive Bayes, Voting Hard, Voting Soft, Stacking

---

## 4. RESULTADOS

1. Vá em **Resultados**
2. Selecione uma sessão concluída
3. Clique em **Carregar**

### 4.1 Tabela comparativa
- ✅ 8 colunas: Modelo, Tipo, CV 10-fold, Acurácia, Precisão, Recall, F1-Score, ROC AUC
- ✅ Badge **melhor** no modelo com maior CV
- ✅ Badge **ensemble** / **individual** por tipo

### 4.2 Curva ROC
- Selecione um modelo no seletor
- ✅ Gráfico de linha com FPR × TPR e valor de AUC
- ✅ Linha pontilhada de referência (classificador aleatório)
- Troque o modelo e veja o gráfico atualizar

### 4.3 Gráfico comparativo
- ✅ Barras lado a lado: CV 10-fold e Acurácia de Teste por modelo
- ✅ Cores adaptam ao tema claro/escuro

### 4.4 Matriz de confusão
- Selecione um modelo no seletor
- ✅ Grid colorido: verde (acertos) e vermelho (erros)
- Troque o modelo e veja atualizar

### 4.5 Exportar CSV
- Clique em **Exportar CSV**
- ✅ Download do arquivo `resultados_sessao_X.csv` com todas as métricas

---

## 5. TESTAR IMAGEM

1. Vá em **Testar Imagem**
2. Selecione uma sessão concluída
3. Selecione o modelo desejado (padrão: Stacking)

### 5.1 Imagem única
1. Clique na área de upload e selecione **1 imagem**
2. ✅ Miniatura da imagem aparece abaixo
3. Clique em **Classificar**
4. ✅ Card de resultado: classe predita, confiança e modelo usado

### 5.2 Lote de imagens (batch)
1. Selecione **várias imagens** de uma vez (Ctrl+clique)
2. ✅ Miniaturas de todas as imagens aparecem
3. Clique em **Classificar**
4. ✅ Tabela com resultado individual de cada imagem

---

## 6. HISTÓRICO

1. Vá em **Histórico**
2. Selecione uma sessão
3. Clique em **Carregar**
4. ✅ Tabela com todas as predições: imagem, modelo, classe, confiança, data/hora

---

## 7. PERFIL

1. Vá em **Perfil**
2. ✅ Nome, e-mail, data de cadastro e badge de verificação visíveis

### 7.1 Editar dados
1. Altere o nome e clique em **Salvar alterações**
2. ✅ Nome atualizado na sidebar e no perfil
3. Altere o e-mail → ✅ nova verificação exigida

### 7.2 Trocar senha
1. Clique em **Trocar Senha**
2. ✅ Modal abre com campos e barra de força da senha
3. Preencha senha atual e nova senha
4. ✅ Regras de força ficam verdes conforme critérios atendidos
5. Clique em **Salvar** → ✅ mensagem de sucesso

---

## 8. TEMA CLARO / ESCURO

1. Clique no botão de tema na sidebar (desktop) ou header (mobile)
2. ✅ Interface muda completamente de tema
3. ✅ Gráficos atualizam as cores automaticamente
4. ✅ Preferência salva — ao reabrir o sistema o tema persiste

---

## 9. MOBILE (tela ≤ 768px)

Redimensione o navegador ou use DevTools (F12 → ícone de celular):

1. ✅ Sidebar some
2. ✅ Header aparece no topo com dragão, título "TCC IA", botão de tema e logout
3. ✅ Barra de navegação fixa na parte inferior com 6 itens
4. ✅ Botão ativo destacado em azul com brilho
5. ✅ Conteúdo ocupa a tela toda
6. ✅ Cards do Dashboard em grade 2×2
7. ✅ Tela de login ocupa a tela toda (painel do dragão some)

---

## 10. SEGURANÇA

| Teste | Resultado esperado |
|---|---|
| Acessar `/` sem login | Redireciona para `/auth` |
| Tentar 11 logins errados seguidos | Bloqueio temporário (rate limit) |
| Sessão após 24h | Redireciona para login |
| Código de verificação errado | Mensagem "Código inválido" |
| Token de reset expirado | Mensagem de erro |

---

## Resumo de funcionalidades

| # | Funcionalidade | Status |
|---|---|---|
| 1 | Cadastro e verificação de e-mail | ✅ |
| 2 | Login / Logout | ✅ |
| 3 | Redefinição de senha | ✅ |
| 4 | Sessão de 24 horas | ✅ |
| 5 | Dashboard com métricas | ✅ |
| 6 | Treinamento com 8 modelos | ✅ |
| 7 | Barra de progresso em tempo real | ✅ |
| 8 | Notificação do navegador | ✅ |
| 9 | Tabela com F1, Precisão, Recall, ROC AUC | ✅ |
| 10 | Curva ROC interativa | ✅ |
| 11 | Gráfico comparativo | ✅ |
| 12 | Matriz de confusão | ✅ |
| 13 | Exportar resultados em CSV | ✅ |
| 14 | Predição de imagem única | ✅ |
| 15 | Predição em lote (batch) | ✅ |
| 16 | Histórico de predições por sessão | ✅ |
| 17 | Perfil editável | ✅ |
| 18 | Trocar senha com barra de força | ✅ |
| 19 | Tema claro / escuro persistente | ✅ |
| 20 | Interface responsiva (mobile) | ✅ |
| 21 | Rate limiting no login | ✅ |
| 22 | Sessões isoladas por usuário | ✅ |
