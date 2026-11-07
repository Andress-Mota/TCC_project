# Manual do Usuário — TCC IA
> Sistema de Classificação de Imagens com Ensemble Learning

---

## Visão Geral

O **TCC IA** é uma plataforma web que permite treinar e comparar modelos de Machine Learning para classificação de imagens médicas (ou qualquer dataset organizado por pastas). O sistema treina 8 modelos automaticamente — 5 individuais e 3 em ensemble — e apresenta métricas, gráficos e comparativos detalhados.

---

## Obtendo o Dataset

O sistema utiliza o dataset **Chest X-Ray Images (Pneumonia)**, disponível gratuitamente no Kaggle.

### Como baixar

1. Acesse: `https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia`
2. Crie uma conta gratuita no Kaggle (se ainda não tiver)
3. Clique em **Download** na página do dataset
4. Extraia o arquivo `.zip` baixado
5. Localize a pasta `chest_xray/` — ela já vem com a estrutura correta:

```
chest_xray/
├── train/
│   ├── NORMAL/
│   └── PNEUMONIA/
├── test/
│   ├── NORMAL/
│   └── PNEUMONIA/
└── val/
    ├── NORMAL/
    └── PNEUMONIA/
```

> Para treinar no sistema, use a pasta `train/` (maior volume de imagens). Exemplo: `C:\Users\andre\Downloads\chest_xray\train`

---

## Requisitos para Usar

Antes de acessar o sistema, certifique-se de que:

1. O servidor está rodando (`start.bat` executado na pasta do projeto)
2. O MySQL está ativo com o banco `tcc_imagens`
3. O dataset foi baixado e extraído conforme instruído acima

### Estrutura esperada do dataset

```
meu_dataset/
├── NORMAL/
│   ├── imagem1.jpg
│   ├── imagem2.png
│   └── ...
└── PNEUMONIA/
    ├── imagem1.jpg
    ├── imagem2.png
    └── ...
```

> As classes podem ter qualquer nome — o sistema detecta automaticamente os nomes das subpastas. Formatos aceitos: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`, `.tif`

---

## 1. Acesso ao Sistema

### 1.1 Criar uma conta

1. Acesse `http://localhost:5000/auth` no navegador
2. Clique em **Criar conta**
3. Preencha os campos:
   - **Nome**: seu nome completo
   - **E-mail**: endereço de e-mail válido
   - **Senha**: mínimo 8 caracteres com maiúscula, minúscula, número e caractere especial
   - **Confirmar senha**: repita a senha digitada
4. Acompanhe o indicador de força da senha (deve ficar verde)
5. Clique em **Cadastrar**

> Você será redirecionado automaticamente para a tela de verificação de e-mail.

### 1.2 Verificar o e-mail

1. Verifique a caixa de entrada do e-mail cadastrado
2. Localize o e-mail com o código de 6 dígitos
3. Digite o código no campo exibido na tela
4. Clique em **Verificar**

> Caso não receba o e-mail, clique em **Reenviar código**.

### 1.3 Fazer login

1. Acesse `http://localhost:5000/auth`
2. Preencha seu **e-mail** e **senha**
3. Clique em **Entrar**

> Você será redirecionado para o Dashboard.

### 1.4 Recuperar senha esquecida

1. Na tela de login, clique em **Esqueci a senha**
2. Digite seu e-mail cadastrado e clique em **Enviar link**
3. Verifique seu e-mail e copie o token recebido
4. Cole o token no campo, defina a nova senha e clique em **Redefinir**
5. Faça login com a nova senha

---

## 2. Dashboard

A página inicial exibe um **resumo geral** da sua atividade no sistema.

| Card | O que mostra |
|------|-------------|
| Sessões concluídas | Total de treinos finalizados |
| Predições realizadas | Total de imagens classificadas |
| Melhor acurácia | Maior acurácia obtida em qualquer sessão |
| Modelo destaque | Nome do modelo com melhor desempenho |

### Gráfico comparativo

Abaixo dos cards há um gráfico de barras com a **acurácia média** de cada modelo em todas as suas sessões, comparando:
- CV 10-fold (validação cruzada)
- Acurácia de teste

### Tabelas recentes

- **Últimas sessões**: data, caminho do dataset, total de imagens e status
- **Últimas predições**: imagem, modelo usado, classe prevista e confiança

---

## 3. Treinar um Modelo

Esta é a etapa principal — onde você envia um dataset e o sistema treina os modelos.

### Passo a passo

1. Clique em **Treinar** no menu lateral
2. No campo **Caminho do dataset**, cole o caminho completo da pasta raiz do seu dataset
   - Exemplo Windows: `C:\Users\andre\Documents\meu_dataset`
3. Clique em **Iniciar Treinamento**
4. Acompanhe a barra de progresso e as mensagens de status
5. Ao concluir, clique em **Ver Resultados**

### O que acontece durante o treino

O sistema executa automaticamente (nesta ordem):

1. Leitura e pré-processamento das imagens (redimensionamento 128×128, escala de cinza)
2. Extração de features HOG
3. Divisão: 80% treino / 20% teste (estratificada)
4. Treinamento de 5 modelos individuais: **KNN**, **SVM**, **Random Forest**, **Regressão Logística**, **Naive Bayes**
5. Treinamento de 3 ensembles: **Voting Hard**, **Voting Soft**, **Stacking**
6. Validação cruzada 10-fold em todos os modelos
7. Geração de métricas, curvas ROC e matrizes de confusão

> O tempo de treinamento varia conforme o tamanho do dataset. Datasets maiores podem levar alguns minutos.

---

## 4. Resultados

Exibe todos os resultados de uma sessão de treino de forma comparativa.

### Como acessar

1. Clique em **Resultados** no menu lateral
2. Selecione a sessão desejada no seletor **Sessão de treino**

### Tabela de modelos

Cada linha representa um modelo com as seguintes métricas:

| Coluna | Descrição |
|--------|-----------|
| Modelo | Nome do modelo (🏆 marca o melhor) |
| Tipo | Individual ou Ensemble |
| CV 10-fold | Acurácia média na validação cruzada (%) |
| Acurácia Teste | Acurácia no conjunto de teste separado (%) |
| Precisão | Proporção de predições positivas corretas (%) |
| Recall | Proporção de positivos reais detectados (%) |
| F1-Score | Média harmônica entre precisão e recall (%) |
| ROC AUC | Área sob a curva ROC (0 a 1, quanto maior melhor) |

### Exportar resultados

Clique em **Exportar CSV** para baixar a tabela completa como planilha.

### Curva ROC

1. Selecione o modelo desejado no seletor **Curva ROC**
2. O gráfico exibe a relação entre taxa de verdadeiro positivo e falso positivo

> Quanto mais a curva se aproxima do canto superior esquerdo, melhor o modelo.

### Gráfico comparativo

Visualização em barras lado a lado dos valores de CV 10-fold e Acurácia Teste de todos os modelos da sessão.

### Matriz de Confusão

1. Selecione o modelo no seletor **Matriz de Confusão**
2. O grid exibe quantas imagens foram classificadas corretamente (diagonal) e onde houve erros

---

## 5. Testar uma Imagem

Usa um modelo já treinado para classificar novas imagens.

### Passo a passo

1. Clique em **Testar Imagem** no menu lateral
2. Selecione a **Sessão de treino** que contém o modelo desejado
3. Selecione o **Modelo** a ser usado
   - **Stacking** é recomendado por apresentar o melhor desempenho geral
4. Arraste imagens para a área de upload ou clique para selecionar arquivos
5. Clique em **Classificar**

### Resultado para 1 imagem

- **Classe predita**: o rótulo definido pelo modelo
- **Confiança**: percentual de certeza do modelo
- **Modelo utilizado**

### Resultado para múltiplas imagens

Uma tabela é exibida com cada imagem, sua classe predita e a confiança correspondente.

---

## 6. Histórico

Exibe todas as predições já realizadas, organizadas por sessão.

### Como usar

1. Clique em **Histórico** no menu lateral
2. Selecione uma sessão no filtro (ou deixe em branco para ver todas)
3. A tabela exibe:
   - Nome da imagem
   - Modelo usado
   - Classe predita
   - Confiança (%)
   - Data e hora da predição

---

## 7. Perfil

Permite visualizar e editar seus dados cadastrais.

### Editar nome ou e-mail

1. Clique em **Perfil** no menu lateral
2. Altere o campo desejado (**Nome** ou **E-mail**)
3. Clique em **Salvar alterações**

> Se alterar o e-mail, será necessário verificar o novo endereço com um código enviado automaticamente.

### Trocar senha

1. Na seção **Segurança**, clique em **Trocar Senha**
2. Preencha a senha atual e a nova senha (duas vezes)
3. Clique em **Salvar**

---

## 8. Preferências

### Tema claro / escuro

Clique no ícone de sol/lua no canto superior da barra lateral para alternar entre os temas. A preferência é salva automaticamente e mantida entre sessões.

---

## 9. Sair do Sistema

Clique em **Sair** no menu lateral (ícone de saída). A tela de encerramento será exibida e você será redirecionado para a tela de login.

---

## Dúvidas Frequentes

**O treinamento travou ou não avança?**
Verifique se o caminho do dataset está correto e se as pastas contêm imagens nos formatos suportados.

**Não recebi o e-mail de verificação.**
Verifique a pasta de spam. Se o servidor local não estiver configurado com SMTP, o código pode aparecer no terminal do Flask.

**Qual modelo devo usar para predição?**
O **Stacking** costuma ser o mais preciso. Você pode comparar os modelos na seção **Resultados** antes de escolher.

**Posso usar datasets com mais de 2 classes?**
O sistema foi desenvolvido para classificação binária. Datasets com mais classes podem não funcionar corretamente.

**Como interpretar o ROC AUC?**
Valores próximos de 1.0 indicam excelente desempenho. Valores abaixo de 0.7 indicam que o modelo tem dificuldade em distinguir as classes.

---

*Manual gerado para o TCC — Classificação de Imagens com Ensemble Learning*
