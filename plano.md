# plan.md

# DEMONSTRAÇÃO — IA GENÉRICA VS AGENTE ANALÍTICO COM CONTEXTO

---

# Objetivo da Demonstração

Construir uma demonstração prática e visualmente impactante para mostrar:

* como empresas possuem dados espalhados
* como IA sem contexto falha
* como engenharia de prompt muda completamente os resultados
* como agentes de IA transformam análise em operação
* como um pipeline reutilizável elimina retrabalho

A apresentação deve causar o seguinte efeito:

> “Não é a IA que muda.
> O que muda é o contexto, a estrutura e o comportamento.”

---

# Narrativa Principal

A demonstração será construída em 4 níveis:

| Etapa                | Resultado             |
| -------------------- | --------------------- |
| IA Genérica          | Insights superficiais |
| Engenharia de Prompt | Insights melhores     |
| Agente Analítico     | Insights estratégicos |
| Pipeline de Dados    | Operação escalável    |

---

# Cenário do E-commerce

## Empresa fictícia

Criar um E-commerce fictício de médio/grande porte.

Segmento sugerido:

* eletrônicos
* moda
* casa e decoração
* vídeo games

---

# Problemas reais do negócio

O E-commerce deve apresentar:

* alto abandono de carrinho
* campanhas com ROAS ruim
* baixa conversão mobile
* canais com tráfego ruim
* gargalos no checkout
* clientes recorrentes com alto volume de tickets
* CAC elevado em alguns canais

---

# Objetivo da IA

Responder:

* onde a empresa perde dinheiro
* quais canais performam melhor
* quais campanhas devem ser pausadas
* onde existe fricção operacional
* quais oportunidades têm maior impacto

---

# Estrutura das Bases de Dados

A demonstração utilizará múltiplas fontes.

Todas devem ser criadas artificialmente.

Os dados devem parecer reais.

---

# BASE 1 — marketing.csv

## Objetivo

Aquisição de tráfego.

## Volume

3000 a 10000 linhas.

## Colunas

```csv
campaign_id
platform
campaign_name
impressions
clicks
ctr
cpc
spend
sessions
date
```

---

# Padrões obrigatórios (fictícios)

## Google Ads

* menor volume
* maior conversão
* ticket médio alto

---

## Instagram

* muito clique
* baixa retenção
* abandono alto

---

## TikTok

* tráfego enorme
* baixa compra
* sessões curtas

---

# BASE 2 — vendas.xlsx

## Objetivo

Pedidos realizados.

## Volume

2000 a 5000 linhas.

## Colunas

```csv id="jsv8bz"
order_id
customer_id
product
category
price
discount
payment_type
state
device
traffic_source
created_at
```

---

# Padrões obrigatórios

## Mobile

* conversão menor
* ticket menor

---

## Desktop

* ticket maior
* checkout mais eficiente

---

## Produtos premium

* vindos principalmente do Google Ads

---

# BASE 3 — navegacao.json

## Objetivo

Eventos de navegação.

## Volume

10.000 eventos.

## Estrutura

```json id="h61qpc"
{
  "session_id": "abc123",
  "clicked_home": 1,
  "product_view": 1,
  "added_to_cart": 0,
  "checkout_started": 0,
  "purchase": 0,
  "device": "mobile",
  "traffic_source": "instagram",
  "session_duration": 42
}
```

---

# Regras obrigatórias

## Eventos

Usar:

* 0 = não aconteceu
* 1 = aconteceu

---

# Padrões comportamentais

## Instagram

* alto clique
* baixa compra
* muito abandono

---

## Google Ads

* menos tráfego
* maior conversão

---

## Mobile

* abandono alto no checkout

---

# BASE 4 — crm.sqlite

## Objetivo

Relacionamento e retenção.

---

# Tabela customers

```sql id="gh4n3y"
customer_id
state
lifetime_value
created_at
```

---

# Tabela tickets

```sql id="72l9wt"
ticket_id
customer_id
category
sentiment
created_at
```

---

# Tabela nps

```sql id="2e8mk7"
customer_id
score
feedback
```

---

# Problemas intencionais nas bases

As bases NÃO devem ser perfeitas.

Adicionar:

* datas inconsistentes
* colunas faltantes
* categorias duplicadas
* nomes diferentes para a mesma origem
* valores nulos
* pequenas inconsistências

Objetivo:
mostrar o valor do agente.

---

# PARTE 1 — EXEMPLO RUIM

# Slide Conceitual

## Mensagem

> “A maioria usa IA assim.”

---

# Prompt utilizado

```text id="h2r7s9"
Explore os dados e traga insights relevantes.
```

---

# Objetivo do Exemplo Ruim

Demonstrar:

* ausência de contexto
* falta de direcionamento
* IA genérica
* análise superficial

---

# Comportamento esperado da IA

A IA deve:

* analisar superficialmente
* ignorar relações importantes
* produzir respostas vagas
* gerar insights óbvios
* não priorizar negócio
* não explicar impacto financeiro

---

# Resultado esperado

## Exemplos

```text id="ew5n1v"
As campanhas possuem CTRs diferentes.
```

```text id="5dyf4m"
Existem usuários que abandonam o carrinho.
```

```text id="9p4qlx"
Alguns produtos vendem mais que outros.
```

```text id="3f0ghw"
Usuários mobile representam boa parte do tráfego.
```

---

# Sensação desejada

O público deve pensar:

> “Isso não ajuda a tomar decisão.”

---

# Problemas do exemplo ruim

## 1. Dados isolados

CSV separado do JSON.

---

## 2. Sem contexto de negócio

A IA não entende:

* CAC
* ROAS
* retenção
* funil
* impacto financeiro

---

## 3. Sem priorização

Tudo parece igualmente importante.

---

## 4. Visual ruim

* texto gigante
* pouca estrutura
* sem storytelling

---

# PARTE 2 — EXEMPLO BOM

# Slide Conceitual

## Mensagem

> “Agora vamos transformar IA em operação.”

---

# Objetivo do Exemplo Bom

Demonstrar:

* engenharia de prompt
* comportamento de agente
* inteligência contextual
* cruzamento de dados
* raciocínio estratégico

---

# Comportamento esperado do agente

O agente deve agir como:

* cientista de dados
* consultor executivo
* analista de BI
* especialista em E-commerce

---

# Prompt Estruturado

## Objetivo

O prompt deve instruir o agente a:

* entender múltiplas bases
* mapear schemas
* resolver inconsistências
* cruzar informações
* criar métricas automaticamente
* inferir padrões
* priorizar impacto financeiro

---

# Pipeline conceitual

```text id="ik1h4d"
CSV + XLSX + JSON + SQLite
                ↓
      Padronização
                ↓
      Contextualização
                ↓
        Agente IA
                ↓
Insights Estratégicos
                ↓
      Próximas Ações
```

---

# Etapa 1 — Entendimento estrutural

O agente deve identificar:

* quais arquivos existem
* papel de cada base
* relacionamentos
* qualidade dos dados
* inconsistências

---

# Etapa 2 — Padronização

Resolver automaticamente:

* formatos de data
* categorias
* ids
* nomenclaturas
* dados faltantes

---

# Etapa 3 — Criação automática de métricas

## Marketing

* CTR
* CPC
* CAC
* ROAS

---

## Conversão

* abandono
* taxa de checkout
* conversão por canal

---

## Receita

* ticket médio
* receita por origem
* margem estimada

---

## CRM

* retenção
* churn implícito
* satisfação

---

# Etapa 4 — Cruzamento inteligente

O diferencial deve estar nas RELAÇÕES.

---

# Exemplos esperados

```text id="b74zvu"
Instagram gera muito tráfego,
mas possui baixa retenção e alto abandono mobile.
```

---

```text id="m6q4sh"
Google Ads converte menos usuários,
mas possui ticket médio 31% maior.
```

---

```text id="1w9eaz"
Usuários mobile abandonam 43% mais durante checkout.
```

---

```text id="x0frs8"
Campanhas com desconto acima de 25%
aumentam conversão,
mas reduzem margem drasticamente.
```

---

# Etapa 5 — Impacto financeiro

Os insights devem quantificar impacto.

---

# Exemplo esperado

```text id="h0uq6k"
O checkout mobile pode estar causando
perda estimada de R$ 180 mil/mês.
```

---

# Etapa 6 — Recomendações acionáveis

A IA deve recomendar:

* otimizações
* cortes de campanha
* ajustes de UX
* melhorias operacionais

---

# Estrutura da resposta boa

# Resumo Executivo

---

# Principais Insights

---

# Gargalos Críticos

---

# Oportunidades

---

# Relações Entre Bases

---

# Hipóteses Estratégicas

---

# Próximas Ações

---

# Métricas-Chave

---

# Alertas e Riscos

---

# PARTE 3 — EVOLUÇÃO PARA PIPELINE

# Objetivo

Mostrar que:

* IA boa não depende de retrabalho
* o sistema vira reutilizável

---

# Slide Conceitual

## Antes

```text id="vy0qpn"
Toda análise precisava ser refeita.
```

---

## Depois

```text id="k6m9wt"
Novos dados entram.
O pipeline continua funcionando.
```

---

# Demonstração do Pipeline

## Novo arquivo

```text id="sz7o1u"
marketing_novembro.csv
```

---

# O agente deve:

* detectar automaticamente
* entender schema
* padronizar colunas
* integrar os dados
* recalcular métricas
* atualizar tendências

---

# Mensagem principal

> “O contexto vira infraestrutura.”

---

# COMPARAÇÃO FINAL

| IA Genérica          | Agente com Contexto   |
| -------------------- | --------------------- |
| análise superficial  | análise estratégica   |
| dados isolados       | dados conectados      |
| insight genérico     | insight acionável     |
| sem contexto         | contexto estruturado  |
| texto simples        | visão executiva       |
| resposta descartável | pipeline reutilizável |

---

# Frase Final

```text"
IA sem contexto responde.

Agentes com contexto geram resultados.
```
