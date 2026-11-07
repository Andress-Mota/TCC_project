#!/usr/bin/env python3
"""TCC FATEC-GT 2026 — Parte 3: Cap 1 seções 1.6-1.12"""
from tcc_parte1 import PDF, ML, MR, MT, MB, PW, CW, SB, ST, SS, SC, LH, LT, LC, IND

def cap1_rf_lr_nb(pdf):
    """1.6 RF, 1.7 LR, 1.8 NB"""
    pdf.np()
    pdf.SUB("1.6  Random Forest")
    pdf.P(
        "O Random Forest, proposto por Leo Breiman em 2001, é um método de ensemble "
        "que combina múltiplas árvores de decisão treinadas sobre subconjuntos "
        "aleatórios dos dados e das features. A motivação central é que árvores "
        "de decisão individuais, quando treinadas até a profundidade máxima, "
        "apresentam altíssima variância — o modelo se ajusta perfeitamente ao "
        "conjunto de treinamento mas generaliza mal. A combinação de múltiplas "
        "árvores com erros decorrelacionados reduz a variância sem aumentar "
        "substancialmente o viés."
    )
    pdf.SSUB("1.6.1  Árvores de Decisão: Base do Random Forest")
    pdf.P(
        "Uma árvore de decisão particiona recursivamente o espaço de features "
        "R^d em regiões retangulares. Em cada nó interno, a melhor divisão "
        "é determinada por um critério de impureza. Para classificação, o critério "
        "mais comum é a impureza de Gini:"
    )
    pdf.QUO(
        "Gini(R) = 1 - sum_{k=1}^{K} p_k^2\n"
        "onde p_k = frequencia da classe k na regiao R"
    )
    pdf.P(
        "Alternativamente, a entropia de Shannon é usada como critério de divisão:"
    )
    pdf.QUO(
        "Entropia(R) = - sum_{k=1}^{K} p_k * log2(p_k)"
    )
    pdf.P(
        "A melhor divisão em cada nó é a que maximiza o ganho de informação "
        "(redução de impureza ponderada pelos filhos). A profundidade máxima "
        "(max_depth) e o número mínimo de amostras por folha controlam a "
        "complexidade da árvore e seu trade-off viés-variância."
    )
    pdf.SSUB("1.6.2  Bagging e Aleatorização de Features")
    pdf.P(
        "O Random Forest incorpora duas formas de aleatorização. Primeiro, "
        "bagging (Bootstrap Aggregating): cada árvore é treinada sobre uma "
        "amostra bootstrap do dataset original — amostragem com reposição de "
        "n amostras de um dataset de n registros. Em média, cada bootstrap "
        "contém aproximadamente 63,2% das amostras originais (as demais formam "
        "o out-of-bag set). Segundo, aleatorização de features: em cada nó de "
        "cada árvore, apenas um subconjunto aleatório de m features é considerado "
        "para a melhor divisão, onde m = sqrt(d) por padrão para classificação."
    )
    pdf.P(
        "A combinação dessas duas formas de aleatorização garante diversidade entre "
        "as árvores: cada árvore vê um subset diferente de amostras E um subset "
        "diferente de features em cada nó, reduzindo a correlação entre elas. "
        "A predição final é a média das predições das M árvores (para probabilidades) "
        "ou votação majoritária (para classes):"
    )
    pdf.QUO(
        "P(y=c|x) = (1/M) * sum_{m=1}^{M} P_m(y=c|x)\n"
        "y_hat = argmax_c P(y=c|x)"
    )
    pdf.SSUB("1.6.3  Importância de Features")
    pdf.P(
        "O Random Forest calcula a importância de cada feature como a redução "
        "total de impureza de Gini ponderada pela proporção de amostras que "
        "passam por splits naquela feature, somada sobre todas as árvores:"
    )
    pdf.QUO(
        "Importancia(j) = (1/M) * sum_{m=1}^{M} sum_{t in T_m: feature(t)=j} n_t/n * DeltaImpureza(t)"
    )
    pdf.P(
        "onde T_m é o conjunto de nós da árvore m, n_t é o número de amostras "
        "no nó t, n é o total de amostras, e DeltaImpureza(t) é a redução de "
        "impureza no nó t. Essa métrica permite identificar quais features clínicas "
        "são mais preditivas, fornecendo insight interpretável sobre o modelo."
    )
    pdf.SSUB("1.6.4  Configuração no Sistema")
    pdf.P(
        "No sistema desenvolvido, o Random Forest é configurado com n_estimators=50 "
        "(50 árvores) e max_depth=10. O parâmetro n_estimators controla o trade-off "
        "entre desempenho e tempo de treinamento: mais árvores melhoram a acurácia "
        "mas com retornos marginais decrescentes. O max_depth=10 limita a "
        "profundidade das árvores para prevenir overfitting. Ao contrário do KNN e "
        "SVM, o Random Forest NÃO requer normalização prévia dos dados, pois "
        "as decisões em cada nó são baseadas em comparações de thresholds de uma "
        "única feature por vez (invariante à escala)."
    )

    pdf.np()
    pdf.SUB("1.7  Regressão Logística")
    pdf.P(
        "A Regressão Logística, apesar do nome, é um algoritmo de classificação "
        "que modela a probabilidade posterior P(y=1|x) mediante a função sigmoide "
        "(logística) aplicada sobre uma combinação linear dos atributos. É um "
        "modelo paramétrico com fronteira de decisão linear em R^d."
    )
    pdf.SSUB("1.7.1  Modelo Probabilístico")
    pdf.P(
        "O modelo Regressão Logística define:"
    )
    pdf.QUO(
        "P(y=1|x; w,b) = sigma(w^T*x + b) = 1 / (1 + exp(-(w^T*x + b)))\n"
        "P(y=0|x; w,b) = 1 - sigma(w^T*x + b)"
    )
    pdf.P(
        "A função sigmoide sigma(z) = 1/(1+e^{-z}) mapeia qualquer valor real "
        "para o intervalo (0,1), interpretável como probabilidade. A fronteira "
        "de decisão (P=0,5) corresponde ao hiperplano w^T*x+b=0 — linear em R^d."
    )
    pdf.SSUB("1.7.2  Estimação dos Parâmetros: Máxima Verossimilhança")
    pdf.P(
        "Os parâmetros w e b são estimados por maximização da log-verossimilhança "
        "(equivalente à minimização da cross-entropy loss) com regularização L2:"
    )
    pdf.QUO(
        "L(w,b) = -(1/n)*sum_{i=1}^{n} [yi*log(p_i) + (1-yi)*log(1-p_i)] + (lambda/2)||w||^2\n"
        "onde p_i = sigma(w^T*xi + b)"
    )
    pdf.P(
        "O problema de otimização não tem solução analítica fechada, mas é convexo "
        "(a Hessiana é semidefinida positiva para qualquer lambda>0), garantindo "
        "solução global única. Algoritmos de otimização de segunda ordem como "
        "L-BFGS (Limited-memory Broyden-Fletcher-Goldfarb-Shanno) convergem "
        "eficientemente (tipicamente em dezenas de iterações). No scikit-learn, "
        "max_iter=1000 garante convergência para datasets clínicos de tamanho "
        "moderado com normalização prévia."
    )
    pdf.SSUB("1.7.3  Extensão para Multiclasse: Softmax")
    pdf.P(
        "Para classificação com K > 2 classes, a Regressão Logística utiliza "
        "a função softmax (multinomial logistic regression):"
    )
    pdf.QUO(
        "P(y=k|x) = exp(wk^T*x + bk) / sum_{j=1}^{K} exp(wj^T*x + bj)"
    )
    pdf.P(
        "Cada classe k possui seu próprio vetor de parâmetros (wk, bk). A decisão "
        "é a classe com maior probabilidade: y_hat = argmax_k P(y=k|x)."
    )

    pdf.np()
    pdf.SUB("1.8  Naive Bayes Gaussiano")
    pdf.P(
        "O classificador Naive Bayes baseia-se no Teorema de Bayes combinado com "
        "a suposição de independência condicional entre atributos dada a classe. "
        "Apesar da suposição (frequentemente violada em dados reais, daí o 'naive'), "
        "o classificador apresenta desempenho surpreendentemente competitivo em "
        "muitos problemas práticos — especialmente quando as features são pouco "
        "correlacionadas dentro de cada classe."
    )
    pdf.SSUB("1.8.1  Fundamentação Bayesiana")
    pdf.P(
        "O classificador Bayes ótimo (Bayes optimal classifier) atribui a x a "
        "classe que maximiza a probabilidade posterior:"
    )
    pdf.QUO(
        "y_hat = argmax_k P(y=k|x) = argmax_k P(x|y=k) * P(y=k) / P(x)\n"
        "                           = argmax_k P(x|y=k) * P(y=k)   [P(x) e constante]"
    )
    pdf.P(
        "Onde P(y=k) é a probabilidade a priori da classe k (estimada pelas "
        "frequências relativas no treinamento) e P(x|y=k) é a verossimilhança — "
        "quão provável é observar x dado que a classe é k. O problema é que "
        "P(x|y=k) é uma distribuição sobre R^d, e estimá-la diretamente "
        "requer exponencialmente mais dados conforme d cresce (maldição da "
        "dimensionalidade)."
    )
    pdf.SSUB("1.8.2  A Suposição Naive e o Modelo Gaussiano")
    pdf.P(
        "A suposição de independência condicional simplifica radicalmente o modelo:"
    )
    pdf.QUO(
        "P(x|y=k) = product_{j=1}^{d} P(xj|y=k)   [independencia condicional]"
    )
    pdf.P(
        "Na versão gaussiana (GaussianNB), cada atributo xj segue distribuição "
        "normal condicionada à classe: P(xj|y=k) = N(mu_{jk}, sigma_{jk}^2), "
        "com parâmetros estimados por máxima verossimilhança:"
    )
    pdf.QUO(
        "mu_{jk}     = media de xj nos exemplos de classe k\n"
        "sigma_{jk}^2 = variancia de xj nos exemplos de classe k"
    )
    pdf.P(
        "O log da probabilidade posterior (para estabilidade numérica) torna-se:"
    )
    pdf.QUO(
        "log P(y=k|x) proporcional a log P(y=k) + sum_{j=1}^{d} log N(xj; mu_{jk}, sigma_{jk}^2)\n"
        "= log P(y=k) - (1/2)*sum_j [ log(2*pi*sigma_{jk}^2) + (xj-mu_{jk})^2/sigma_{jk}^2 ]"
    )
    pdf.P(
        "Vantagens do Naive Bayes: (1) extremamente rápido para treinar "
        "(O(n*d) para estimar parâmetros); (2) funciona bem com poucos dados; "
        "(3) naturalmente probabilístico; (4) robusto a features irrelevantes "
        "(um atributo com mu_{j0}=mu_{j1} e sigma_{j0}=sigma_{j1} tem contribuição "
        "constante e não afeta a decisão). Desvantagem principal: a suposição de "
        "independência entre features raramente é exata em dados clínicos, onde "
        "correlações (ex.: pressão arterial e colesterol) são biologicamente "
        "esperadas. Apesar disso, o modelo serve como baseline útil e é sempre "
        "incluído no sistema para comparação."
    )

def cap1_ensemble(pdf):
    """1.9 Ensemble"""
    pdf.np()
    pdf.SUB("1.9  Ensemble Learning")
    pdf.P(
        "Ensemble Learning é a estratégia de combinar múltiplos modelos de "
        "aprendizado de máquina para obter melhor desempenho preditivo, maior "
        "robustez e menor variância que qualquer modelo individual. O princípio "
        "é análogo ao senso coletivo humano: assim como a média das estimativas "
        "de uma grande crowd tende a ser mais precisa que a de qualquer indivíduo "
        "isolado (sabedoria das multidões), a combinação de classificadores com "
        "perspectivas distintas tende a superar qualquer classificador individual "
        "(KUNCHEVA, 2014)."
    )
    pdf.SSUB("1.9.1  Teoria da Diversidade de Ensemble")
    pdf.P(
        "Kuncheva (2014) demonstra matematicamente que o sucesso de um ensemble "
        "depende de duas condições necessárias: (1) os classificadores base devem "
        "ter acurácia superior a 50% (melhor que aleatório); (2) os erros dos "
        "classificadores devem ser diversificados — errar em amostras diferentes. "
        "A decomposição de ambiguidade (Zhou, 2012) formaliza isso:"
    )
    pdf.QUO(
        "Erro_ensemble(x) = Media_i[Erro_i(x)] - Media_i[Ambiguidade_i(x)]\n\n"
        "onde Ambiguidade_i(x) = (hi(x) - Media_j[hj(x)])^2  mede a diversidade\n"
        "Erro_i(x) = (hi(x) - y)^2  mede o erro individual"
    )
    pdf.P(
        "Esse resultado crucial mostra que o erro do ensemble é SEMPRE menor ou "
        "igual à média dos erros individuais, sendo a diferença proporcional à "
        "diversidade dos classificadores. Ensemble com classificadores idênticos "
        "(zero diversidade) não traz ganho algum; ensemble com classificadores "
        "maximamente diversos (erros completamente decorrelacionados) traz ganho "
        "máximo. No sistema implementado, os 5 classificadores base (KNN, SVM, RF, "
        "LR, NB) têm fundamentos matemáticos e fronteiras de decisão radicalmente "
        "distintos, garantindo diversidade substancial."
    )
    pdf.SSUB("1.9.2  Hard Voting (Votação Majoritária)")
    pdf.P(
        "Cada classificador hi emite um voto discreto para cada amostra x. "
        "A predição do ensemble é a classe com o maior número de votos:"
    )
    pdf.QUO(
        "y_hat = argmax_{c in C}  sum_{i=1}^{M} 1[hi(x) = c]\n\n"
        "Para M classificadores e K classes, o Hard Voting reduz ao voto da\n"
        "maioria absoluta (M/2 + 1 votos para M impar)."
    )
    pdf.P(
        "O Hard Voting não requer que os classificadores produzam probabilidades — "
        "apenas rótulos de classe. É robusto a classificadores mal calibrados em "
        "termos de probabilidade, mas desperdiça informação de confiança. "
        "No sistema implementado, os 5 modelos base votam e a classe com maiores "
        "votos (mínimo 3/5 para decisão majoritária) é escolhida."
    )
    pdf.SSUB("1.9.3  Soft Voting (Votação por Probabilidades)")
    pdf.P(
        "Cada classificador hi fornece probabilidades P_i(y=c|x) para cada classe c. "
        "O ensemble calcula a média das probabilidades:"
    )
    pdf.QUO(
        "P_ens(y=c|x) = (1/M) * sum_{i=1}^{M} P_i(y=c|x)\n"
        "y_hat = argmax_c P_ens(y=c|x)"
    )
    pdf.P(
        "O Soft Voting é geralmente superior ao Hard Voting quando as probabilidades "
        "estão bem calibradas, pois incorpora a CONFIANÇA de cada classificador: "
        "uma predição feita com 95% de confiança tem mais peso que uma feita com "
        "52% de confiança. Para que o Soft Voting funcione corretamente, todos os "
        "classificadores devem produzir probabilidades calibradas — razão pela qual "
        "SVC(probability=True) é usado no sistema."
    )
    pdf.SSUB("1.9.4  Stacking com Meta-aprendizado")
    pdf.P(
        "O Stacking (Wolpert, 1992) é uma abordagem de dois níveis que aprende "
        "a combinação ótima dos classificadores base. O nível 0 consiste nos M "
        "classificadores base; o nível 1 consiste em um meta-learner g que aprende "
        "a combinar as saídas dos classificadores base:"
    )
    pdf.QUO(
        "Nivel 0 (base):  Z_i(x) = [P_{h1}(y|x),..., P_{hM}(y|x)]   (meta-features)\n"
        "Nivel 1 (meta):  y_hat = g(Z(x))"
    )
    pdf.P(
        "O risco de overfitting é mitigado usando validação cruzada para gerar as "
        "meta-features: para cada dobra de CV, os classificadores base são treinados "
        "sem aquela dobra e geram predições sobre ela. Assim, as meta-features "
        "nunca são geradas pelo mesmo modelo que as usa para treinamento. "
        "No sistema, o meta-learner é uma Regressão Logística treinada sobre as "
        "probabilidades de saída dos 5 modelos base em CV de 5 dobras."
    )
    pdf.P(
        "O Stacking pode aprender combinações NÃO-LINEARES e ASSÍTRICAS dos "
        "classificadores base — ao contrário do Soft Voting que usa a média simples. "
        "Por exemplo, o meta-learner pode aprender que para determinados padrões "
        "de input o KNN é mais confiável, e para outros o SVM deve ter mais peso. "
        "No experimento, o Stacking obteve o melhor AUC-ROC (0,9520), corroborando "
        "sua superioridade em capacidade discriminativa."
    )
    pdf.SSUB("1.9.5  Por que KNN + SVM são Complementares?")
    pdf.P(
        "A complementaridade entre KNN e SVM no ensemble é teoricamente justificada "
        "pela distinção entre modelos lazy e eager:"
    )
    pdf.P(
        "KNN (Lazy Learner): toma decisões baseadas em vizinhança local — os K "
        "exemplos mais similares no espaço de features. É sensível a padrões locais "
        "e fronteiras de decisão irregulares. Em regiões onde a distribuição das "
        "classes é complexa e não-linear localmente, o KNN tende a acertar onde "
        "o SVM erra."
    )
    pdf.P(
        "SVM (Eager Learner): constrói uma representação global da fronteira de "
        "decisão definida pelos vetores de suporte, maximizando a margem geométrica. "
        "É robusto a outliers (ignorados se não forem vetores de suporte) e "
        "eficiente em espaços de alta dimensão. Em regiões onde a fronteira de "
        "decisão global é mais informativa que a estrutura local, o SVM tende a "
        "acertar onde o KNN erra."
    )
    pdf.P(
        "A taxa de concordância de 96,67% entre KNN e SVM no conjunto de teste "
        "indica que 58 em 60 predições concordam. Os 2 casos de discordância são "
        "justamente os casos ambíguos próximos à fronteira de decisão, onde a "
        "perspectiva complementar do ensemble pode ser decisiva. Kuncheva (2014) "
        "demonstra que mesmo com alta concordância entre classificadores, o ensemble "
        "pode trazer ganhos significativos se os casos de discordância forem "
        "correlacionados com acertos de um e erros de outro."
    )

def cap1_cnn(pdf):
    """1.10 CNN e EfficientNet"""
    pdf.np()
    pdf.SUB("1.10  Redes Neurais Convolucionais e EfficientNet-B0")
    pdf.P(
        "As Redes Neurais Convolucionais (CNNs) representam o paradigma dominante "
        "em visão computacional desde a vitória do AlexNet no ImageNet Challenge de "
        "2012 (reduzindo o erro de 26% para 15,3%). Diferente dos algoritmos "
        "clássicos que exigem extração manual de features, as CNNs aprendem "
        "automaticamente representações hierárquicas dos dados visuais por meio "
        "de camadas de convolução treinadas por retropropagação do gradiente."
    )
    pdf.SSUB("1.10.1  Operação de Convolução")
    pdf.P(
        "A operação fundamental é a correlação cruzada (confusamente denominada "
        "convolução na literatura de deep learning) entre a entrada X e um filtro W:"
    )
    pdf.QUO(
        "(X * W)[i,j] = sum_{m=0}^{f-1} sum_{n=0}^{f-1} X[i+m, j+n] * W[m,n] + b\n\n"
        "onde f x f eh o tamanho do filtro (tipicamente 3x3 ou 5x5)\n"
        "e b eh o vies do filtro"
    )
    pdf.P(
        "Cada filtro aprende a detectar um tipo específico de padrão visual: filtros "
        "nas camadas iniciais detectam bordas horizontais, verticais e diagonais; "
        "camadas intermediárias detectam texturas e formas simples; camadas profundas "
        "detectam características semânticas complexas como olhos, rodas, tumor. "
        "A hierarquia de representações aprendidas automaticamente é o que torna "
        "as CNNs tão poderosas para visão computacional."
    )
    pdf.SSUB("1.10.2  Max Pooling e Invariância a Translação")
    pdf.P(
        "As camadas de pooling (tipicamente max pooling) subsamplem os mapas de "
        "ativação, reduzindo sua resolução espacial e induzindo invariância a "
        "pequenas translações. Max pooling de tamanho 2x2 com stride 2 reduz cada "
        "dimensão pela metade, selecionando a ativação máxima em cada janela:"
    )
    pdf.QUO(
        "MaxPool(X)[i,j] = max(X[2i:2i+2, 2j:2j+2])"
    )
    pdf.P(
        "Essa operação reduz a sensibilidade a deslocamentos sub-pixel da feature, "
        "contribuindo para a robustez da CNN a variações de posição."
    )
    pdf.SSUB("1.10.3  Transfer Learning e Fine-tuning")
    pdf.P(
        "Treinar uma CNN do zero requer milhões de imagens rotuladas e dias de "
        "processamento em GPUs de alta performance. Transfer learning reutiliza "
        "pesos aprendidos em um dataset massivo (ImageNet: 1,2M imagens, 1000 "
        "classes) como inicialização para um novo problema com dataset menor. "
        "A premissa é que as features aprendidas nas camadas iniciais (bordas, "
        "texturas) são genéricas e transferíveis entre domínios."
    )
    pdf.P(
        "No sistema desenvolvido, o EfficientNet-B0 pré-treinado no ImageNet é "
        "carregado com EfficientNet_B0_Weights.DEFAULT do torchvision. A camada "
        "classificadora final (model.classifier) é substituída por uma camada "
        "Linear com saída de dimensão n_classes — o número de classes do problema "
        "específico do usuário. As demais camadas são inicializadas com os pesos "
        "do ImageNet. Treinamento por 8 épocas com taxa de aprendizado 1e-3 e "
        "scheduler OneCycleLR permite adaptar o modelo ao novo domínio eficientemente."
    )
    pdf.SSUB("1.10.4  Arquitetura EfficientNet-B0")
    pdf.P(
        "O EfficientNet foi proposto por Tan e Le (2019) com base no conceito de "
        "escalonamento composto (compound scaling): em vez de escalar apenas a "
        "profundidade, largura ou resolução, o EfficientNet escala as três "
        "dimensões de forma balanceada por um fator phi:"
    )
    pdf.QUO(
        "Profundidade: d = alpha^phi\n"
        "Largura:      w = beta^phi\n"
        "Resolucao:    r = gamma^phi\n"
        "sujeito a:    alpha * beta^2 * gamma^2 = 2  (restricao computacional)\n"
        "onde alpha=1.2, beta=1.1, gamma=1.15 sao otimizados por NAS"
    )
    pdf.P(
        "O EfficientNet-B0 é o modelo base (phi=1), com entrada 224x224, "
        "~5,3M parâmetros e ~390M FLOPs. Utiliza inverted residual blocks (MBConv) "
        "com squeeze-and-excitation (SE) networks para modelar dependências de "
        "canal. O fluxo de processamento no sistema é:"
    )
    pdf.BULL([
        "Entrada: imagem RGB 224x224x3;",
        "Stem: convolução 3x3, stride=2, 32 filtros;",
        "7 blocos MBConv com diferentes expansoes e strides;",
        "Head: convolução 1x1, 1280 filtros;",
        "Global average pooling;",
        "Dropout (taxa 0.2);",
        "Camada Linear: 1280 -> n_classes (substituída no fine-tuning).",
    ])
    pdf.SSUB("1.10.5  Função de Perda e Otimizador")
    pdf.P(
        "O treinamento minimiza a Cross-Entropy Loss sobre o conjunto de treinamento:"
    )
    pdf.QUO(
        "L(y, y_hat) = -(1/n)*sum_{i=1}^{n} sum_{k=1}^{K} y_{ik} * log(softmax(z_{ik}))\n"
        "onde z_i = W*phi(xi) + b eh a saida da camada linear (logits)"
    )
    pdf.P(
        "O otimizador Adam (Kingma e Ba, 2015) combina estimação adaptativa do "
        "gradiente (RMSprop) com momento de primeira ordem:"
    )
    pdf.QUO(
        "m_t = beta1*m_{t-1} + (1-beta1)*g_t      (1o momento)\n"
        "v_t = beta2*v_{t-1} + (1-beta2)*g_t^2   (2o momento)\n"
        "m_hat = m_t/(1-beta1^t);  v_hat = v_t/(1-beta2^t)  (correcao de vies)\n"
        "w_t = w_{t-1} - lr * m_hat/(sqrt(v_hat) + epsilon)"
    )
    pdf.P(
        "O scheduler OneCycleLR varia ciclicamente a taxa de aprendizado: "
        "aumenta de lr/10 para lr nas primeiras 30% das iterações, depois "
        "decai para lr/1000, permitindo exploração ampla do espaço de parâmetros "
        "seguida de convergência refinada. Configuração: lr=1e-3, weight_decay=1e-4."
    )

def cap1_hog(pdf):
    """1.11 HOG"""
    pdf.np()
    pdf.SUB("1.11  Histograma de Gradientes Orientados (HOG)")
    pdf.P(
        "O descritor HOG (Histogram of Oriented Gradients) foi proposto por "
        "Dalal e Triggs (2005) para detecção de pedestres e tornou-se um dos "
        "descritores de features mais utilizados em visão computacional antes "
        "do domínio das CNNs. O HOG representa a estrutura local da imagem por "
        "meio da distribuição de orientações de gradientes de intensidade em regiões "
        "locais (células), sendo robusto a variações de iluminação e deformações "
        "geométricas locais."
    )
    pdf.SSUB("1.11.1  Pipeline Completo de Extração")
    pdf.P(
        "O pipeline de extração HOG implementado no sistema compreende 6 etapas "
        "sequenciais:"
    )
    pdf.P(
        "Etapa 1 — Pré-processamento de imagem: a imagem de entrada (qualquer "
        "tamanho) é convertida para escala de cinza (cv2.IMREAD_GRAYSCALE) e "
        "redimensionada para 128x128 pixels via cv2.resize(). A conversão para "
        "escala de cinza elimina a informação de cor (3 canais) e reduz a dimensão "
        "de entrada por fator de 3, concentrando a análise na estrutura de "
        "intensidade."
    )
    pdf.P(
        "Etapa 2 — Cálculo dos gradientes: para cada pixel (i,j), calcula-se "
        "o gradiente horizontal Gx e vertical Gy via filtros de diferença centrada:"
    )
    pdf.QUO(
        "Gx(i,j) = I(i,j+1) - I(i,j-1)\n"
        "Gy(i,j) = I(i+1,j) - I(i-1,j)"
    )
    pdf.P(
        "A magnitude e orientação do gradiente em cada pixel são:"
    )
    pdf.QUO(
        "M(i,j) = sqrt(Gx(i,j)^2 + Gy(i,j)^2)      (magnitude)\n"
        "theta(i,j) = arctan(Gy(i,j) / Gx(i,j))     (orientacao em [0,180) graus)"
    )
    pdf.P(
        "A magnitude indica a 'força' da borda no pixel; a orientação indica a "
        "direção perpendicular à borda. Gradientes fortes correspondem a bordas, "
        "contornos e texturas — estruturas visualmente discriminativas."
    )
    pdf.P(
        "Etapa 3 — Construção de histogramas por célula: a imagem 128x128 é "
        "dividida em células de 16x16 pixels (resultando em 8x8=64 células). "
        "Para cada célula, os gradientes de todos os 256 pixels são acumulados "
        "em um histograma de 9 bins de orientação (0°-180°, intervalos de 20°) "
        "com votação bilinear ponderada pela magnitude:"
    )
    pdf.QUO(
        "hist_c[b] += M(i,j) * w_b(theta(i,j))   para cada pixel (i,j) na celula c\n"
        "onde w_b eh o peso de interpolacao para o bin b mais proximo"
    )
    pdf.P(
        "Etapa 4 — Normalização por bloco: células são agrupadas em blocos de "
        "2x2 células sobrepostos (com stride de 1 célula). Cada bloco contém "
        "4 células x 9 bins = 36 valores, normalizados por L2-Hys (norma L2 "
        "seguida de clipping em 0.2 e renormalização) para invariância a "
        "variações de iluminação e contraste. O deslizamento com stride=1 célula "
        "produz (8-2+1)x(8-2+1) = 7x7 = 49 blocos."
    )
    pdf.P(
        "Etapa 5 — Concatenação: os histogramas normalizados de todos os blocos "
        "são concatenados em um único vetor de features:"
    )
    pdf.QUO(
        "dim(HOG) = n_blocos * n_celulas_por_bloco * n_orientacoes\n"
        "         = 49       *  4                   *  9\n"
        "         = 1764 features\n\n"
        "Nota: com pixels_per_cell=(16,16) e cells_per_block=(2,2):\n"
        "n_blocos_h = (128/16 - 2 + 1) = 6 (horizontal)\n"
        "n_blocos_v = (128/16 - 2 + 1) = 6 (vertical)\n"
        "dim(HOG) = 6 * 6 * 4 * 9 = 1296 / 4 = 324 features"
    )
    pdf.P(
        "O vetor HOG final possui 324 dimensões para imagens 128x128 com os "
        "parâmetros orientations=9, pixels_per_cell=(16,16), cells_per_block=(2,2)."
    )
    pdf.SSUB("1.11.2  Propriedades do HOG como Descritor")
    pdf.P(
        "O descritor HOG apresenta as seguintes propriedades relevantes para "
        "classificação de imagens:"
    )
    pdf.BULL([
        "Robustez à iluminação: a normalização por bloco torna o descritor "
        "invariante a variações de escala de intensidade;",
        "Invariância parcial a translação: a estrutura de células e blocos "
        "fornece alguma invariância a pequenas translações;",
        "Captura de forma e textura: gradientes fortes ocorrem nas bordas dos "
        "objetos e em regiões texturizadas, sendo features discriminativas;",
        "Compacidade: 324 dimensões representam adequadamente a estrutura "
        "de uma imagem 128x128 (16.384 pixels) com fator de compressão de ~50x;",
        "Compatibilidade com classificadores lineares: o espaço HOG é adequado "
        "para SVMs com kernel linear e RBF, Random Forest e KNN.",
    ])

def cap1_metricas(pdf):
    """1.12 Métricas completas"""
    pdf.np()
    pdf.SUB("1.12  Métricas de Avaliação e Validação Cruzada")
    pdf.P(
        "A avaliação rigorosa de classificadores requer um conjunto abrangente de "
        "métricas que capturem diferentes aspectos do desempenho. A métrica mais "
        "simples — acurácia — é insuficiente quando as classes são desbalanceadas "
        "ou quando os custos dos diferentes tipos de erro são assimétricos. "
        "Neste trabalho, são computadas seis métricas complementares para cada "
        "modelo, além da validação cruzada estratificada como estimador de "
        "generalização."
    )
    pdf.SSUB("1.12.1  Matriz de Confusão")
    pdf.P(
        "Para classificação binária (classes: Positivo=Doente, Negativo=Saudável), "
        "a matriz de confusão organiza os resultados em quatro categorias:"
    )
    pdf.TABLE(
        "Quadro 1.4 – Estrutura da Matriz de Confusão",
        ["","Predito: Negativo","Predito: Positivo"],
        [
            ["Real: Negativo", "VN (Verdadeiro Negativo)", "FP (Falso Positivo)"],
            ["Real: Positivo", "FN (Falso Negativo)",      "VP (Verdadeiro Positivo)"],
        ],
        cw=[35,62,63], fsz=10
    )
    pdf.SRC("Fonte: Elaborado pelo autor.")
    pdf.P(
        "O Falso Negativo (FN) representa o erro mais crítico em triagem clínica: "
        "um paciente doente classificado como saudável que, sem tratamento, "
        "pode sofrer consequências severas. O Falso Positivo (FP) leva a exames "
        "adicionais desnecessários — custo financeiro e psicológico mas sem risco "
        "direto à saúde."
    )
    pdf.SSUB("1.12.2  Métricas Derivadas da Matriz de Confusão")
    pdf.TABLE(
        "Tabela 1.1 – Definições formais das métricas de avaliação",
        ["Métrica","Fórmula","Gama","Interpretação clínica"],
        [
            ["Acurácia","(VP+VN)/(VP+VN+FP+FN)","[0,1]","Proporção global de acertos"],
            ["Precisão","VP/(VP+FP)","[0,1]","Fração de alertas corretos"],
            ["Revocação (Sensib.)","VP/(VP+FN)","[0,1]","Fração de doentes detectados"],
            ["Especificidade","VN/(VN+FP)","[0,1]","Fração de saudáveis identificados"],
            ["F1-Score","2*P*R/(P+R)","[0,1]","Média harmônica precisão-revocação"],
            ["AUC-ROC","Área sob ROC","[0.5,1]","Discriminação entre classes"],
        ],
        cw=[38,44,16,62], fsz=9
    )
    pdf.SRC("Fonte: Elaborado pelo autor.")
    pdf.P(
        "Em contextos de triagem diagnóstica, a Revocação (sensibilidade) é "
        "frequentemente a métrica primária: maximizar a detecção de doentes "
        "é prioritário mesmo ao custo de maior taxa de falsos positivos. "
        "A Especificidade (1-FPR) é igualmente importante para evitar sobrecarga "
        "do sistema de saúde com falsos alarmes."
    )
    pdf.SSUB("1.12.3  Curva ROC e AUC")
    pdf.P(
        "A curva ROC (Receiver Operating Characteristic) plota a Taxa de "
        "Verdadeiro Positivo (TVP = revocação = VP/P) contra a Taxa de Falso "
        "Positivo (TFP = FP/N) para todos os possíveis limiares de decisão "
        "theta in [0,1]:"
    )
    pdf.QUO(
        "TVP(theta) = P(h(x) >= theta | y = 1)   = VP(theta) / (VP(theta) + FN(theta))\n"
        "TFP(theta) = P(h(x) >= theta | y = 0)   = FP(theta) / (FP(theta) + VN(theta))"
    )
    pdf.P(
        "A AUC (Area Under the ROC Curve) é a integral da curva ROC, "
        "equivalente à probabilidade de que o modelo rankeie uma amostra "
        "positiva aleatória acima de uma negativa aleatória:"
    )
    pdf.QUO(
        "AUC = P(h(x_pos) > h(x_neg)) = integral_0^1 TVP(TFP^{-1}(t)) dt"
    )
    pdf.P(
        "AUC = 0,5 indica modelo aleatório (diagonal); AUC = 1,0 indica "
        "modelo perfeito. AUC acima de 0,90 é considerado excelente em "
        "diagnóstico clínico. Para classificação multiclasse, a abordagem "
        "One-vs-Rest calcula uma curva ROC por classe e a AUC macro-media "
        "sobre todas as classes, implementada no sistema via roc_curve e auc "
        "do scikit-learn."
    )
    pdf.SSUB("1.12.4  F1-Score para Datasets Desbalanceados")
    pdf.P(
        "O F1-Score é especialmente útil quando as classes estão desbalanceadas: "
        "um classificador que sempre prediz a classe majoritária terá alta acurácia "
        "mas F1-Score baixo para a classe minoritária. A fórmula da média harmônica "
        "penaliza fortemente valores extremos:"
    )
    pdf.QUO(
        "F1 = 2 * Precisao * Revocacao / (Precisao + Revocacao)\n"
        "   = 2*VP / (2*VP + FP + FN)\n\n"
        "Weighted F1 = sum_k (w_k * F1_k)  onde w_k = suporte da classe k / total"
    )
    pdf.P(
        "Para avaliação multiclasse, o sistema utiliza F1 ponderado pela frequência "
        "de cada classe (average='weighted' no scikit-learn), que atribui mais "
        "peso às classes mais frequentes e é apropriado para datasets com "
        "desbalanceamento moderado."
    )
