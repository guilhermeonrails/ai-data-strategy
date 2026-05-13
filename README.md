# AI Data Strategy — AI Festival StartSe

Demonstração prática de como contexto, estrutura e engenharia de prompt transformam IA genérica em análise estratégica de e-commerce.

Apresentação: [slides.google.com](https://docs.google.com/presentation/d/1Kn0lFPRHYG4tOna-NnYgeGXeierAm51U/edit?usp=sharing&ouid=116484345118893479565&rtpof=true&sd=true)

---

## Pré-requisitos

- Python 3.13+
- Chave de API do [Groq](https://console.groq.com)

---

## Configuração

**1. Clone o repositório**

```bash
git clone https://github.com/guilhermeonrails/ai-data-strategy.git
cd ai-data-strategy
```

**2. Crie e ative o ambiente virtual**

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

**3. Instale as dependências**

```bash
pip install -r requirements.txt
```

**4. Configure a chave da API**

```bash
cp .env.example .env
```

Abra o `.env` e substitua pelo valor real da sua chave do [Groq](https://console.groq.com).

---

## Dados disponíveis

As bases já estão geradas na pasta `data/` e simulam um e-commerce real (NexTech — Eletrônicos e Games, junho–novembro 2025):

| Arquivo | Conteúdo |
|---|---|
| `marketing.csv` | 4.300 campanhas — Google Ads, Instagram, TikTok |
| `vendas.xlsx` | 3.000 pedidos com device, canal e receita |
| `navegacao.json` | 10.000 eventos de sessão (funil completo) |
| `crm.sqlite` | 2.000 clientes, tickets de suporte e NPS |
| `marketing_dezembro.csv` | Campanhas de dezembro para análise comparativa |

Os dados contêm inconsistências intencionais (formatos de data variados, categorias duplicadas, nomes de plataforma divergentes) para simular cenários reais.

---

## Estrutura do projeto

```
ai-data-strategy/
├── prompts/
│   ├── prompt_ruim.txt       # prompt genérico — sem contexto de negócio
│   └── prompt_bom.txt        # prompt estruturado — agente analítico com contrato JSON
├── data/
│   ├── marketing.csv
│   ├── marketing_dezembro.csv
│   ├── vendas.xlsx
│   ├── navegacao.json
│   └── crm.sqlite
├── requirements.txt
├── .env.example
└── slide.md                  # link para os slides da apresentação
```

---

## Sobre a demonstração

O projeto ilustra 3 níveis de uso de IA sobre os mesmos dados:

| Nível | Abordagem | Resultado |
|---|---|---|
| IA Genérica | `prompt_ruim.txt` — sem contexto | Insights superficiais e genéricos |
| Engenharia de Prompt | `prompt_bom.txt` — estruturado | Insights melhores, mais focados |
| Agente Analítico | Contexto completo + cruzamento de bases | Insights estratégicos e acionáveis em JSON |

O `prompt_bom.txt` define um agente com quatro papéis combinados (Cientista de Dados, Consultor Executivo, Analista de BI e Especialista em E-commerce) e retorna um JSON estruturado com: resumo executivo, gargalos, oportunidades, relações entre bases, recomendações priorizadas e alertas de risco.
