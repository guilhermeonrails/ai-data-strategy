# Documentação — Pasta `data/`

Bases de dados fictícias geradas pelo script `gerar_dados.py`.  
Representam o e-commerce **NexTech** (Eletrônicos e Games) no período de **junho a novembro de 2025**.

Os dados foram construídos com padrões realistas de negócio e **inconsistências intencionais** (formatos de data variados, nomes de plataforma duplicados, valores nulos) para simular o ambiente real de dados de uma empresa.

---

## marketing.csv

Campanhas pagas veiculadas no período.

| Campo | Tipo | Descrição |
|---|---|---|
| `campaign_id` | string | Identificador único da campanha |
| `platform` | string | Plataforma de veiculação |
| `campaign_name` | string | Nome da campanha |
| `impressions` | integer | Total de impressões |
| `clicks` | integer | Total de cliques |
| `ctr` | float / string | Taxa de cliques (às vezes em formato `"2.5%"`) |
| `cpc` | float | Custo por clique em R$ |
| `spend` | float | Gasto total em R$ |
| `sessions` | integer | Sessões geradas |
| `date` | string | Data da campanha (formatos inconsistentes) |

**Volume:** 4.300 linhas  
**Gasto total:** R$ 5.153.025,94  
**Período:** junho a novembro de 2025

**Padrões por plataforma:**

| Plataforma | Comportamento |
|---|---|
| Google Ads | Menor volume, maior conversão, ticket alto |
| Instagram | Muitos cliques, baixa retenção, alto abandono |
| TikTok | Tráfego massivo, sessões curtas, baixíssima compra |

**Inconsistências intencionais:**
- 12 variações de nome de plataforma (`Google`, `google ads`, `Google AdWords`, `INSTAGRAM`, etc.)
- Datas em formatos `YYYY-MM-DD`, `DD/MM/YYYY` e `YYYY/MM/DD`
- ~340 linhas com CTR como string percentual (`"2.50%"`)
- ~114 linhas com `sessions` nulo
- ~87 linhas com `clicks` e `ctr` nulos
- ~15 linhas com `impressions = 0`

---

## vendas.xlsx

Pedidos realizados no período.

| Campo | Tipo | Descrição |
|---|---|---|
| `order_id` | string | Identificador único do pedido |
| `customer_id` | string | Identificador do cliente |
| `product` | string | Nome do produto |
| `category` | string | Categoria do produto |
| `price` | float | Preço em R$ |
| `discount` | float | Desconto aplicado (0 a 1) |
| `payment_type` | string | Forma de pagamento |
| `state` | string | Estado do cliente (UF) |
| `device` | string | Dispositivo usado na compra |
| `traffic_source` | string | Canal de origem |
| `created_at` | string | Data e hora do pedido |

**Volume:** 3.000 linhas  
**Receita líquida total:** R$ 5.010.619,10  
**Ticket médio bruto:** R$ 1.918,21

**Padrões por dispositivo:**

| Device | Pedidos | Ticket médio |
|---|---|---|
| Mobile | 1.441 (48%) | R$ 1.671 |
| Desktop | 1.264 (42%) | R$ 2.175 |
| Tablet | 295 (10%) | — |

**Inconsistências intencionais:**
- Categorias duplicadas (`Smartphones`, `Celulares`, `smartphone`, `Celular`)
- Nomes de canal inconsistentes (`instagram`, `Instagram Ads`, `ig`)
- ~53 linhas com `payment_type` nulo
- ~46 linhas com `state` nulo
- Timestamps em dois formatos (`YYYY-MM-DD HH:MM:SS` e `YYYY-MM-DD`)

---

## navegacao.json

Eventos de sessão — funil comportamental completo.

```json
{
  "session_id": "SES0000001",
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

Todos os campos de evento usam `0` (não ocorreu) ou `1` (ocorreu).

**Volume:** 10.000 eventos  
**Total de compras:** 27  
**Taxa de conversão geral:** 0,27%

**Padrões de conversão (checkout → compra):**

| Device | Taxa |
|---|---|
| Desktop | 18,5% |
| Mobile | 7,9% |

**Padrões por canal:**

| Canal | Comportamento |
|---|---|
| Google Ads | Menos sessões, maior conversão, duração longa |
| Instagram | Alto volume, baixíssima compra, sessões curtas |
| TikTok | Maior volume, quase zero compras |
| Orgânico / Direto | Melhor qualidade de tráfego |

---

## crm.sqlite

Banco relacional com três tabelas de relacionamento e retenção.

### `customers`

| Campo | Tipo | Descrição |
|---|---|---|
| `customer_id` | TEXT PK | Identificador único |
| `name` | TEXT | Nome completo |
| `email` | TEXT | E-mail |
| `state` | TEXT | Estado (UF) |
| `lifetime_value` | REAL | Receita total histórica em R$ |
| `created_at` | TEXT | Data de cadastro |

2.000 registros | LTV médio: R$ 6.826,62 | LTV máx: R$ 79.346,08

### `tickets`

| Campo | Tipo | Descrição |
|---|---|---|
| `ticket_id` | TEXT PK | Identificador único |
| `customer_id` | TEXT FK | Referência ao cliente |
| `category` | TEXT | Tipo do problema |
| `status` | TEXT | Estado do ticket |
| `sentiment` | TEXT | Sentimento (`positivo`, `neutro`, `negativo`) |
| `created_at` | TEXT | Data de abertura |

3.582 registros — clientes com alto LTV tendem a ter mais tickets (indicador de risco).

### `nps`

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | INTEGER PK | Auto-incremento |
| `customer_id` | TEXT FK | Referência ao cliente |
| `score` | INTEGER | Nota de 0 a 10 |
| `feedback` | TEXT | Comentário livre |
| `collected_at` | TEXT | Data da coleta |

1.118 registros (~55% de taxa de resposta).

---

## marketing_dezembro.csv

Arquivo adicional utilizado na **demonstração do pipeline**.  
Simula a chegada de dados novos (dezembro de 2025) para mostrar que o sistema detecta, padroniza e integra automaticamente sem retrabalho.

**Volume:** 500 linhas  
**Período:** 01/12/2025 a 31/12/2025  
**Schema:** idêntico ao `marketing.csv`
