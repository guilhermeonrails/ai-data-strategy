# AI Data Strategy — NexTech E-commerce

Demonstração prática de como contexto, estrutura e engenharia de prompt transformam IA genérica em análise estratégica.

---

## Pré-requisitos

- [Docker](https://www.docker.com/products/docker-desktop) instalado e rodando
- Chave de API do [Groq](https://console.groq.com)

---

## Subindo o projeto

**1. Clone o repositório**

```bash
git clone https://github.com/guilhermeonrails/ai-data-strategy.git
cd ai-data-strategy
```

**2. Configure a chave da API**

```bash
export GROQ_API_KEY="sua_chave_aqui"
```

**3. Build e geração dos dados**

```bash
docker compose up --build
```

O container instala as dependências Python e gera automaticamente todas as bases de dados em um volume Docker:

| Arquivo | Descrição | Volume |
|---|---|---|
| `marketing.csv` | 4.300 campanhas — Google Ads, Instagram, TikTok | `dados` |
| `vendas.xlsx` | 3.000 pedidos com device, canal e receita | `dados` |
| `navegacao.json` | 10.000 eventos de sessão (funil completo) | `dados` |
| `crm.sqlite` | 2.000 clientes, tickets de suporte e NPS | `dados` |

---

## Rodando localmente (sem Docker)

**1. Crie o ambiente virtual**

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

**2. Instale as dependências**

```bash
pip install -r requirements.txt
```

**3. Gere as bases de dados**

```bash
python gerar_dados.py
```

---

## Estrutura do projeto

```
ai-data-strategy/
├── gerar_dados.py        # gerador de todas as bases fictícias
├── requirements.txt      # dependências Python
├── Dockerfile
├── docker-compose.yml
├── prompts/
│   ├── prompt_ruim.txt   # prompt genérico (sem contexto)
│   └── prompt_bom.txt    # prompt estruturado (agente analítico)
└── data/                 # gerado automaticamente — não versionado
    ├── marketing.csv
    ├── vendas.xlsx
    ├── navegacao.json
    ├── crm.sqlite
    └── marketing_dezembro.csv
```

---

## Sobre a demonstração

O projeto mostra 3 níveis de uso de IA sobre os mesmos dados:

| Nível | Abordagem | Resultado |
|---|---|---|
| IA Genérica | Prompt sem contexto | Insights superficiais |
| Engenharia de Prompt | Prompt estruturado | Insights melhores |
| Agente Analítico | Contexto + cruzamento de bases | Insights estratégicos e acionáveis |

Os dados possuem inconsistências intencionais (datas em formatos diferentes, categorias duplicadas, nomes de plataforma variados) para simular cenários reais de negócio.
