# Generative AI - RAG

## Trabalho de Conclusão de Curso de Yago Ribeiro Bruno

#### Tema abordado: IA Generativa com Suporte de RAG (Geração Aumentada por Recuperação): Uma Abordagem para Otimização de Respostas em Ambientes Complexos



# Arquitetura

![imagem da arquitetura do projeto](/documentation/img/image.png)


# Documentos Utilizados para teste

## Relatório BTLG11

Relatório Gerencial de Fundo Imobiliário: Utilizou-se um documento gerencial autêntico do fundo BTG PACTUAL LOGÍSTICA FUNDO DE INVESTIMENTO IMOBILIÁRIO (BTLG11) para referência. Este documento simboliza o setor financeiro, destacando-se pela abundância de dados numéricos, tabelas, gráficos e expressões do mercado de capitais, como "vacância", "cap rate" e "rendimento por cota". O documento apresenta 23 páginas de conteúdo.

## Facebook AI Similarity Search (FAISS)

Documento Técnico sobre FAISS (Facebook AI Similarity Search): Escolhemos um documento que detalha a biblioteca FAISS, um instrumento para procurar similaridades em vetores de grande dimensão. Este texto apresenta conceitos intrincados de ciência da computação, matemática e algoritmos de busca. A decisão é justificada pela necessidade de verificar se o sistema é capaz de responder a questões precisas acerca das funcionalidades, parâmetros e arquitetura de uma tecnologia particular. O documento apresenta 10 páginas de conteúdo.

## Manual de Benefícios de Recursos Humanos (Simulado)

Para representar um cenário de uso comum no ambiente empresarial, elaborou-se um documento que detalha as políticas de benefícios de uma companhia imaginária. Inclui detalhes sobre assistência médica, vale-alimentação, políticas de férias e outros benefícios, incluindo critérios de elegibilidade e procedimentos. Este documento avalia a habilidade do sistema de percorrer informações organizadas em forma de políticas e responder a questões práticas dos colaboradores, que podem ser formuladas de formas ambíguas. O documento apresenta 3 páginas de conteúdo.


# Métricas de avaliação e metodologia de testes

## Metodologia

1. **Acurácia Factual:**
    Esta métrica verifica a consistência e a precisão das informações fornecidas na resposta do modelo em comparação com o conteúdo contido nos documentos originais. A meta é mensurar a habilidade do sistema em prevenir "alucinações" (produção de informações errôneas) ou distorções.

    **Metodologia de Avaliação:** Foi elaborado um questionário com uma série de questões e respostas de referência, extraídas manualmente dos documentos. Um humano comparou cada resposta produzida com o gabarito e o documento original. Uma resposta foi considerada "acurada" se todas as suas declarações pudessem ser comprovadas na fonte; caso contrário, era categorizada como "inaccurata".

2. **Relevância da Resposta:**
    A relevância avalia o quanto a resposta produzida corresponde à intenção e ao âmbito da questão proposta pelo usuário. Uma resposta pode estar correta factualmente, porém ser inútil se não tratar diretamente do problema.

    **Método de Avaliação:** Utilizou-se uma escala Likert de 1 a 5 para a avaliação humana, onde cada resposta foi classificada de acordo com os seguintes critérios:
    a. **Irrelevante:** A resposta não tem relação com a pergunta.
    b. **Pouco Relevante:** A resposta aborda o tópico de forma marginal, mas não responde à pergunta principal.
    c. **Relevante:** A resposta aborda a pergunta principal, mas de forma incompleta ou indireta.
    d. **Muito Relevante:** A resposta é direta e aborda todos os aspectos centrais da pergunta.
    e. **Perfeitamente Relevante:** A resposta é direta, completa e concisa, atendendo perfeitamente à necessidade do usuário.

3. **Completude da Resposta:**
    Esta métrica, adicional à relevância, verifica se a resposta do sistema abrange todas as informações cruciais e relevantes presentes nos documentos de origem, a fim de responder de maneira completa à questão do usuário.

    **Método de Avaliação:** Com base no gabarito, verificou-se se a resposta produzida omitiu detalhes cruciais que seriam indispensáveis para um entendimento integral do tema. A resposta foi categorizada como "completa" ou "incompleta".

4. **Acurácia da Citação de Fontes:**
    Um dos maiores benefícios do RAG é a sua habilidade de identificar as origens da informação, assegurando rastreabilidade e confiabilidade. Esta métrica avalia a exatidão com que o sistema correlaciona a informação produzida aos trechos (chunks) adequados dos documentos originais.

    **Método de Avaliação:** Para cada resposta, foram examinados os chunks de texto mencionados como fonte. A citação foi considerada correta se o chunk recuperado pelo banco de dados vetorial realmente continha a informação fundamental usada para resumir a resposta. A taxa percentual de respostas que contêm citações corretas e relevantes em relação ao total de respostas produzidas foi calculada.

# Sumário dos Resultados

| Documento | Acurácia Factual (%) | Relevância Média (1-5) | Completude (%) | Acurácia da Citação (%) |
|---|---|---|---|---|
| relatorio_BTLG11.pdf | 100% | 100% | 100% | 100% |
| Faiss_Engineering_at_Meta.pdf | 60% | 60% | 100% | 100% |
| Manual_de_Beneficios_ao_Colaborador-ConectaTech.pdf | 100% | 60% | 80% | 100% |

- [Resultado detalhado](https://docs.google.com/spreadsheets/d/1xJd3jqFTIRM3ZVT5kOtpBRhPYpK2NE6daSvKRz4vz9Y/edit?usp=sharing) 