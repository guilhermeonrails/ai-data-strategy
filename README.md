# AI Data Strategy — Ai FESTIVAL STARTSE

Demonstração prática de como contexto, estrutura e engenharia de prompt transformam IA genérica em análise estratégica.

---

## Pré-requisitos

- Python 3.13+
- Chave de API do [Groq](https://console.groq.com)

---

## Subindo o projeto

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

Abra o `.env` e substitua `sua_chave_aqui` pela sua chave do [Groq](https://console.groq.com).

**5. Gere as bases de dados**

```bash
python gerar_dados.py
```

**6. Rode a análise estratégica**

```bash
python analise.py
```

As bases serão criadas na pasta `data/`:

| Arquivo | Descrição |
|---|---|
| `marketing.csv` | 4.300 campanhas — Google Ads, Instagram, TikTok |
| `vendas.xlsx` | 3.000 pedidos com device, canal e receita |
| `navegacao.json` | 10.000 eventos de sessão (funil completo) |
| `crm.sqlite` | 2.000 clientes, tickets de suporte e NPS |

---

## Estrutura do projeto

```
ai-data-strategy/
├── gerar_dados.py        # gerador de todas as bases fictícias
├── analise.py            # agente analítico — lê dados e envia ao Groq
├── requirements.txt      # dependências Python
├── .env                  # chave da API (não versionado)
├── .env.example          # modelo do .env
├── prompts/
│   ├── prompt_ruim.txt   # prompt genérico (sem contexto)
│   └── prompt_bom.txt    # prompt estruturado (agente analítico)
└── data/
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
