import requests
import os
import json
from dotenv import load_dotenv

# import auth_ss, index_ss

load_dotenv("config.env")


def get_embeddings(input_list):

    formatted_data = [{"text": item} for item in input_list]

    # Convert to JSON string
    json_string = json.dumps(formatted_data)
    print(json_string)

    url = "https://api.jina.ai/v1/embeddings"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + str(os.getenv("JINA_TOKEN")),
    }

    data = {
        "model": "jina-embeddings-v3",
        "task": "text-matching",
        "late_chunking": False,
        "dimensions": 1024,
        "embedding_type": "float",
        "input": json_string,
        # expected format: {"text": "A blue cat"}
    }

    response = requests.post(url, headers=headers, json=data)
    # print(response.text)

    response_data = response.json()

    # Acessando o valor de embedding do índice 0
    embedding_index_0 = response_data["data"][0]["embedding"]
    print(embedding_index_0)

    return embedding_index_0


# conn = auth_ss.singlestore_auth()

json_string = [
    """O ano começa diferente – seus investimentos também?
 O Brasil de 2024 tem um pouco menos de incertezas do que o de 2023 – quando ainda não se sabia qual seria a política econômica do recém- -eleito governo Lula. Passados doze meses, um novo arcabouço fiscal está em vigência, a reforma tributária sobre o consumo foi aprovada e a inflação retrocedeu. Os juros já começaram a cair e a expectativa é de mais cortes até o fim do ano.
No exterior, alguns pontos de atenção também se dissiparam. Embora haja dúvidas sobre a intensidade e o ritmo dos cortes dos juros nos Esta- dos Unidos, parece ponto pacífico que as taxas chegaram ao teto – o que já é uma grande coisa aos olhos dos agentes financeiros.
Os ânimos estão melhores, é fato – mas até onde vai esse otimismo? Será suficiente para sustentar uma migração para ativos de risco, como as ações? Ou o melhor é continuar colhendo os ganhos dos juros ainda elevados? Quais são os melhores investimentos para 2024?
Questões como estas guiam o e-book Onde Investir 2024, uma realiza- ção do InfoMoney para auxiliar os investidores na tomada de decisões neste início de ano. Nele, você encontrará desde as perspectivas para o Ibovespa até as ações mais recomendadas – seja para ganhar com a valorização dos papéis, seja para montar uma carteira de renda passiva com dividendos.
Você também terá acesso a informações sobre fundos imobiliários, ETFs, dólar, investimentos no exterior e criptomoedas – além de recomenda- ções de investimentos de renda fixa, uma “estrela” do mercado em 2023.
O InfoMoney ouviu dezenas dos melhores especialistas do Brasil sobre onde investir em 2024. Na visão deles, há espaço para novas altas nas ações bra- sileiras e americanas, mesmo que em menor intensidade do que no ano pas- sado. O mesmo se vê na renda fixa: ainda há ganhos represados com juros de dois dígitos, tanto nos títulos públicos quanto no crédito privado.
Aproveite as reflexões e análises dos especialistas para fazer as melho- res escolhas neste ano. Boa leitura e bons investimentos!
 3
  A carteira ideal para ganhar e se proteger
 Uma das primeiras decisões dos investidores, quando estão montando uma carteira, é sobre a alocação: quanto deve ser direcionado para renda fixa, ações, ativos alternativos (como criptomoedas), mercado local ou global? Essa “divisão do bolo” precisa estar relacionada com os objetivos de cada um – mas também alinhada com o cenário para a economia.
O rumo dos juros americanos deu a tônica dos mercados em 2023 – as taxas nos EUA ainda em alta no primeiro trimestre afetaram os ativos de risco de países emergentes, como o Brasil. Mas, da metade do ano em diante, a percepção de que o pico já havia sido atingido lá fora, aliada ao início do ciclo de queda da Selic (taxa básica de juros brasileira) por aqui, impulsionou um rali de respeito.
O Ibovespa terminou 2023 com alta de 22%, enquanto o CDI (taxa de re- ferência para a renda fixa) acumulou 13%.
Para 2024, a trajetória dos juros americanos vai continuar fazendo preço. O Brasil tende a se beneficiar em caso de redução, o que atrairia recursos de investidores globais. Já no lado interno, a Selic – hoje em 11,75% – pode chegar aos 9%. Esse movimento tende a valorizar as ações e também os títulos de renda fixa prefixados, se a queda for além do esperado – já que quando a taxa cai, o preço do título sobe.
Clique e assista ao painel
   4

 A inflação brasileira promete seguir na meta – embora para Caio Mega- le, economista-chefe da XP, ainda não se pode afirmar que ela esteja completamente dominada. “O BC vai continuar cortando os juros, mas vai manter a cautela”, diz. Uma Selic abaixo de 9% só virá se houver confian- ça de que a inflação voltou para níveis normais.
Renda fixa, ações ou multimercados?
Como a Selic chegando aos níveis previstos, Catherine Cruz, CIO da Integrity Wealth Management, considera que a renda fixa segue sendo um bom in- vestimento. “Os títulos indexados à inflação são os nossos preferidos, espe- cialmente os isentos”, explica. “Observamos empresas sólidas pagando até IPCA mais 6,5%, uma das maiores taxas dos últimos cinco anos.”
E, nesse cenário, como ficam as ações? Investidores questionam se a alta de 22% do ano passado significa que há pouco espaço para novas valorizações em 2024. Ronaldo Patah, estrategista de investimentos para Brasil do UBS Wealth Management, considera que os ganhos devem per- sistir, já que o fluxo estrangeiro que impulsionou o Ibovespa nos últimos dois meses deve se manter ao longo do ano.
Os multimercados são sempre recomendados por conta da flexibilidade – e assim continuam para 2024, mesmo considerando que no ano passado o rendimento da categoria (de 9,3%) perdeu para o CDI. Para Patah, ainda é importante manter parte do patrimônio (20% do portfólio) nesse tipo de ativo para proteger a carteira.
Diversificação geográfica
A diversificação geográfica também é uma prioridade para os especialistas – afinal, pode ajudar a reduzir riscos. Com a tendência de queda dos juros em 2024, a renda variável nos Estados Unidos volta a merecer espaço na carteira, considera Patah - especialmente as empresas de tecnologia en- volvidas em projetos de inteligência artificial.
O mesmo vale para os bonds, títulos de renda fixa emitidos no exterior. Mesmo que o mercado espere o início de uma queda dos juros nos EUA, as taxas alcançaram o patamar mais alto das últimas duas décadas no ano passado – o que significa que ainda serão atrativos.
6,5% ao ano mais IPCA é o que pagam títulos de renda fixa de empresas sólidas
    5

  Ibovespa: novos recordes ou correção?
 O ano de 2024 tem potencial para ser positivo para a Bolsa brasileira, ainda que de forma menos intensa do que o ano passado, quando o Ibo- vespa fechou em alta de 22,28%, em sua maior pontuação nominal da história (134.185 pontos).
O principal motivo para o otimismo é a esperada continuidade do ciclo de quedas de juros no Brasil e Estados Unidos, possível graças ao recuo da inflação.
O Fed (banco central americano) começou a elevar os juros básicos em 2022 e só no fim de 2023 o mercado entendeu que não haveria mais no- vas altas - a expectativa é que as taxas comecem a ser reduzidas após março de 2024. Com esse cenário, os ativos de renda variável, como as ações, são beneficiados.
  As projeções dos analistas para o Ibovespa em 2024
O otimismo também é impulsio- nado pelas baixas cotações das ações brasileiras, quando compa- radas aos papéis de fora e mesmo aos próprios patamares históricos. Quando se leva em conta não a pontuação nominal do Ibovespa,
  Casa de análise
Santander Bradesco BBI Guide Genial Bank of America Itaú BBA
XP Investimentos Inter Research BB Investimentos Ativa Média
Projeção (em pontos)
160.000
 157.000 mas sim o indicador preço/lucro
(P/L) das ações que compõem o índice, isso fica evidente.
Aos 130 mil pontos, o P/L do Ibo- 145.000 vespa é de 8,5 vezes - sendo que
  155.000 151.200 145.000
   142.000 142.000 141.000 138.000 147.620
a média histórica é de 11 vezes, calcula a Santander Corretora.
Clique e veja as projeções completas para o Ibovespa
     Fonte: Instituições financeiras
6

  As ações “queridinhas” para 2024
 As perspectivas para a bolsa brasileira em 2024 são positivas – mas in- vestidor que se preza sabe que o desempenho dos ativos não é unifor- me. As ações escolhidas com mais frequência pelas casas de análise nas carteiras recomendadas podem dar uma indicação das candidatas a se sair melhor ao longo do ano.
Nessa lista estão duas empresas que podem valorizar por processos de privatização (Sabesp e Copel), uma companhia beneficiada pela redução dos juros (Localiza) e uma produtora de commodity (Vale).
A expectativa com a Sabesp (SBSP3) é positiva pelo avanço do processo de privatização. A Ativa Investimentos, por exemplo, espera que a venda da companhia para o setor privado destrave valor e aumente a eficiência.
“Uma vez privatizada, espera-se que a cultura da Sabesp mude, com melhora na eficiência, na geração de caixa e na margem de lucro”, afir- ma Pedro Serra, chefe de pesquisas da Ativa. A estabilidade do setor de saneamento, pouco dependente de ciclos econômicos, também favore- ce a empresa.
Com a Copel (CPLE6) – empresa de energia do Paraná, privatizada em 2023 – o pano de fundo é semelhante: agora nas mãos do setor privado, a eficiência da empresa deve aumentar, seja pelo corte de despesas operacionais ou pela concentração nos seus ativos-chave. Espera-se, por exemplo, que a companhia venda a Compagas.
  As ações mais indicadas para 2024
   Empresa
Sabesp Copel Localiza Vale
Ticker
SBSP3 CPLE6 RENT3 VALE3
Retorno em 2023
35,61% 36,05% 23,00% -5,73%
                Fonte: Santander, Ativa Investimentos, BTG Pactual, XP Investimentos, Ágora Investimentos, Guide e Economática
Clique e veja as recomendações completas para 2024
 7

 147.620é a média das projeções de pontos nove casas de análise para
o Ibovespa em 2024
A continuidade do corte dos juros aqui no Brasil é o que embasa a recomendação de compra de ações como as da Localiza (RENT3), que tem 85% da sua dívida atrelada ao CDI (taxa pós-fixada que acompanha a Selic).
Outros pontos que fundamentam a preferência pela locadora é a melhora do horizonte para o segmento de veículos seminovos e o fato de as ações estarem descontadas em relação ao valuation histórico, diz Ricardo Pe- retti, estrategista da Santander Corretora.
Já as ações da Vale (VALE3) são indicadas por conta da revisão para cima dos preços do minério de ferro. O BTG Pactual, por exemplo, es- pera um aumento da produção e das vendas da mineradora, assim como uma queda de custos.
Outras ações – como Itaú Unibanco (ITUB4), Equatorial (EQTL3), Mer- cado Livre (MELI34) e Prio (PRIO3) – também foram citadas com frequ- ência pelas casas de análise consultadas pelo InfoMoney.
     Clique e assista ao painel
  8

  Dividendos de ações ou FIIs: que tal ambos?
 A estratégia de investir buscando o retorno com dividendos – sejam eles pagos por ações ou por fundos imobiliários (FIIs) – é uma das preferidas pelos investidores que desejam receber uma renda recorrente e contar com carteiras mais estáveis. Afinal, embora os dividendos e juros sobre o capital próprio (JCP) variem de acordo com o desempenho das empresas e dos FIIs, essas oscilações geralmente são menores que as do mercado em geral.
Em 2024, tanto os FIIs quanto as ações devem se beneficiar da queda dos juros, que tende a valorizar as cotações e elevar os lucros. Vicente Guimarães, CEO da VG Research, ressalta que há mais de 100 empresas na Bolsa com dividend yield (taxa de retorno com dividendos) acima de 6% ao ano. Isso mostra que, apesar do rali das últimas semanas de 2023, ainda há muitas ações descontadas.
Em 2023, os retornos das ações que pagam bons dividendos foram maiores que dos FIIs. O Índice de Dividendos (IDIV) da B3 subiu 27%, enquanto o Ifix (índice que acompanha os FIIs mais negociados na Bol- sa) avançou 15%.
Para 2024, as ações mais citadas por cinco casas de análise consulta- das pelo InfoMoney como potenciais boas pagadoras de dividendos são Petrobras, BB Seguridade, Engie e Telefônica Brasil.
No caso da Petrobras (PETR4), embora a companhia tenha perdido o posto de melhor pagadora de dividendos em 2023 por conta da queda do faturamento, suas ações
continuam recomendadas.
      “A empresa está mudando, com foco muito mais em in- vestimentos e menos em di- videndos. Mas mesmo pa- gando o mínimo previsto em sua política, é um valor ele- vado, pois se trata de uma forte geradora de caixa”, afirma Pedro Serra, da Ativa.
Tem muitas ações baratas ainda, apesar de a bolsa ter dado o rali no final de ano, passando de 138 mil pontos.”
Vicente Guimarães, CEO da VG Research
9

  Mais de 100
Já a BB Seguridade (BBSE3)
foi uma das campeãs de di-
vidend yield de 2023 (a em-
presa deu retorno com di-
videndos com 10,34%) e a
expectativa dos analistas é
que repita o bom desempenho neste ano. “Os resultados recentes da companhia demonstram solidez, com um desempenho altamente positi- vo em todos os segmentos operacionais”, avalia Luis Novaes, analista da Terra Investimentos. A seguradora vem se expandindo a partir do aumen- to das parcerias e da penetração nos canais digitais.
A geradora de energia Engie (EGIE3) – historicamente uma boa pagadora de dividendos – também foi citada pelas casas de análise. Outra ação re- comendada com frequência é a Telefônica Brasil (VIVT3). A expectativa é que a distribuição de proventos aumente porque as demandas de in- vestimentos no setor de telecomunicações está reduzindo em relação ao passado – com isso, o lucro gerado poderia ser distribuído em maior pro- porção, em vez de ser reinvestido para o capex.
E quais serão os melhores FIIs para 2024? A queda da Selic deve benefi- ciar os fundos de shoppings, que podem tanto ter valorização das cotas quanto aumento dos dividendos, já que as vendas das lojas tendem a au- mentar. O mesmo se espera dos FIIs de lajes corporativas, um mercado que pode aquecer, gerando mais dividendos, especialmente nos imóveis das regiões mais nobres, diz Eduardo Mira, sócio do Clube FII.
Independentemente do momento, o ideal é ter uma carteira equilibrada (50% e 50%) entre fundos de “tijolo”, que investem diretamente em imó- veis, e de “papel”, que compram ativos de renda fixa.
Ações de dividendos mais recomendadas para 2024
ações na bolsa negociam com dividend yield superior a 6% ao ano
       Empresa
Petrobras BB Seguridade Engie Telefônica Brasil
Ticker
PETR4 BBSE3 EGIE3 VIVT3
Dividend yield em 2023 (%)
29,22 10,34 7,67 8,16
                Fonte: Ágora, Ativa, Guide, Terra Investimentos, XP Investimentos e Economática.
 Clique e veja as melhores ações de dividendos para 2024
10

  Clique e assista ao painel
 A gente ainda tem boas oportunidades nos fundos imobiliários porque eles não cresceram tanto quanto as ações”
Eduardo Mira, sócio do clube FII
Em 2023, os fundos de “papel” deram retornos superiores, se compara- dos aos de “tijolo”. “O motivo para o alto retorno dos FIIs de “papel” se deve ainda a um período de alta taxa de juros, referência para a rentabilidade desses fundos”, diz Fernanda Rosalem, head de investimentos da Paladin. Segundo ela, os fundos de “papel” geralmente são menos voláteis que os de “tijolo”. Mas, nos fundos de “tijolo”, geralmente o potencial de valoriza- ção da cota é superior.
Marcos Baroni, head de fundos imobiliários e analista da Suno Research, espera que os FIIs de “tijolo” sejam os mais beneficiados no ano. Para os investidores que desejam mais previsibilidade nos retornos, ele recomenda os fundos com galpões logísticos e shoppings: “Em geral, eles possuem contratos mais longos e maior estabilidade de fluxo”. Já os fundos de lajes corporativas podem ser uma alternativa interessante, mas ele diz que o ní- vel de alavancagem de alguns ainda é elevado, e que eles precisam vender os imóveis para destravar o valor para os cotistas.
      FIIs mais recomendados para 2024
   Ticker
BTLG11 HGBS11 PVBI11 HGLG11 KNIP11
Fundo
BTG Pactual Logística Hedge Brasil Shopping VBI Prime Properties CHSG Logística Kinea Índices de Preços
Dividend Yield – 12 meses (%)
8,96 10,33 8,29 9,06 10,68
                    Fonte: Economática
11

  XP, há mais de 20 anos transformando o mercado financeiro para melhorar
a vida das pessoas.
Na hora de planejar o futuro e decidir onde investir, é melhor contar com a ajuda de um profissional especializado.
O assessor de investimentos vai te ajudar a montar uma carteira de investimentos ideal para o seu perfil e momento de vida, sempre de forma imparcial e de olho exclusivamente nos seus interesses. E o melhor é que aqui na XP você não paga nada para abrir e manter sua conta, nem mesmo para fazer TED para retiradas.
  Vantagens de investir com a XP:
   Carteiras recomendadas
Deixe que nossaáreade Análises selecione os ativos para você investir. Escolha uma carteira para buscar maximizarseusresultados,em diferentes estratégias.
Produtos disponíveis:
Fundos de
I nvestimentos
COE
Relatório de oportunidades Assessoria exclusiva
Recomendaçõesdonossotimede Aqualificaçãotécnicadaequipeé analistasqueindicamparavocêas selecionadadeformarigorosa,com opçõesdeativoscombasenas certificaçõestécnicasparaconstruir
pri ncipais estratégias e escolas de o portfólio mais adequeado para o análisedomercado. seuperfil.
 .
Renda Fixa
Fundos Imobiliários
Ações
Previdência Privada"""
]


print(get_embeddings(json_string))
