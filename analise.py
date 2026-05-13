#!/usr/bin/env python3
"""
Agente Analítico — NexTech E-commerce
Carrega os dados, monta o contexto e envia ao Groq usando o prompt_bom.txt.
"""

from dotenv import load_dotenv
load_dotenv()

import os
import json
import sqlite3
import numpy as np
import pandas as pd
from groq import Groq

client = Groq()
MODEL  = "llama-3.3-70b-versatile"

# ══════════════════════════════════════════════════════════════
# Normalização
# ══════════════════════════════════════════════════════════════

def _norm_platform(v):
    m = {
        "google": "Google Ads", "google ads": "Google Ads", "google adwords": "Google Ads",
        "instagram": "Instagram", "instagram ads": "Instagram", "ig": "Instagram", "INSTAGRAM": "Instagram",
        "tiktok": "TikTok", "Tiktok": "TikTok", "tiktok_ads": "TikTok", "TIKTOK": "TikTok",
    }
    s = str(v).strip()
    return m.get(s, m.get(s.lower(), s)) if pd.notna(v) else v

def _norm_source(v):
    m = {
        "google": "google_ads", "google ads": "google_ads",
        "instagram ads": "instagram", "ig": "instagram", "Instagram": "instagram",
        "TikTok": "tiktok", "Tiktok": "tiktok", "tiktok_ads": "tiktok",
    }
    s = str(v).strip()
    return m.get(s, s.lower()) if pd.notna(v) else v

def _clean_ctr(v):
    if pd.isna(v): return None
    s = str(v)
    return float(s.replace("%", "")) / 100 if "%" in s else float(s)

# ══════════════════════════════════════════════════════════════
# Leitura e processamento das bases
# ══════════════════════════════════════════════════════════════

def processar_marketing():
    df = pd.read_csv("data/marketing.csv")
    df["platform"]   = df["platform"].apply(_norm_platform)
    df["ctr"]        = df["ctr"].apply(_clean_ctr)
    df["spend"]      = pd.to_numeric(df["spend"],      errors="coerce")
    df["clicks"]     = pd.to_numeric(df["clicks"],     errors="coerce")
    df["impressions"]= pd.to_numeric(df["impressions"],errors="coerce")
    df["sessions"]   = pd.to_numeric(df["sessions"],   errors="coerce")

    agg = df.groupby("platform").agg(
        campanhas  =("campaign_id",  "count"),
        impressoes =("impressions",  "sum"),
        cliques    =("clicks",       "sum"),
        gasto_R$   =("spend",        "sum"),
        sessoes    =("sessions",     "sum"),
        cpc_medio  =("cpc",          "mean"),
    ).reset_index()

    agg["ctr_%"]     = (agg["cliques"]  / agg["impressoes"].replace(0, np.nan) * 100).round(2)
    agg["gasto_R$"]  = agg["gasto_R$"].round(2)
    agg["cpc_medio"] = agg["cpc_medio"].round(2)
    total            = agg["gasto_R$"].sum()
    agg["share_%"]   = (agg["gasto_R$"] / total * 100).round(1)

    return {
        "por_plataforma": agg.to_dict("records"),
        "total_campanhas": int(len(df)),
        "gasto_total_R$":  round(float(total), 2),
        "periodo":         f"{df['date'].min()} a {df['date'].max()}",
        "inconsistencias": {
            "plataformas_variantes": int(df["platform"].nunique()),
            "sessoes_nulas":         int(df["sessions"].isna().sum()),
            "impressoes_zero":       int((df["impressions"] == 0).sum()),
            "ctr_como_string":       int(df["ctr"].isna().sum()),
        },
    }


def processar_vendas():
    df = pd.read_excel("data/vendas.xlsx")
    df["price"]           = pd.to_numeric(df["price"],    errors="coerce")
    df["discount"]        = pd.to_numeric(df["discount"], errors="coerce")
    df["receita_liquida"] = df["price"] * (1 - df["discount"])
    df["source_ok"]       = df["traffic_source"].apply(_norm_source)

    by_dev = df.groupby("device").agg(
        pedidos        =("order_id",        "count"),
        ticket_medio   =("price",           "mean"),
        desconto_medio =("discount",        "mean"),
        receita        =("receita_liquida", "sum"),
    ).reset_index()
    by_dev["ticket_medio"]   = by_dev["ticket_medio"].round(2)
    by_dev["desconto_medio"] = (by_dev["desconto_medio"] * 100).round(1)
    by_dev["receita"]        = by_dev["receita"].round(2)

    by_src = df.groupby("source_ok").agg(
        pedidos      =("order_id",        "count"),
        ticket_medio =("price",           "mean"),
        receita      =("receita_liquida", "sum"),
        desc_medio   =("discount",        "mean"),
    ).reset_index()
    by_src["ticket_medio"] = by_src["ticket_medio"].round(2)
    by_src["receita"]      = by_src["receita"].round(2)
    by_src["desc_medio"]   = (by_src["desc_medio"] * 100).round(1)

    return {
        "por_dispositivo":  by_dev.to_dict("records"),
        "por_canal":        by_src.to_dict("records"),
        "total_pedidos":    int(len(df)),
        "receita_total_R$": round(float(df["receita_liquida"].sum()), 2),
        "ticket_medio_R$":  round(float(df["price"].mean()), 2),
    }


def processar_navegacao():
    with open("data/navegacao.json") as f:
        events = json.load(f)

    df = pd.DataFrame(events)
    df["source_ok"] = df["traffic_source"].apply(_norm_source)

    funnel = df.groupby("source_ok").agg(
        sessoes   =("session_id",       "count"),
        views     =("product_view",     "sum"),
        carrinhos =("added_to_cart",    "sum"),
        checkouts =("checkout_started", "sum"),
        compras   =("purchase",         "sum"),
        duracao   =("session_duration", "mean"),
    ).reset_index()

    funnel["tx_view_%"]      = (funnel["views"]     / funnel["sessoes"].replace(0, np.nan)   * 100).round(1)
    funnel["tx_carrinho_%"]  = (funnel["carrinhos"] / funnel["views"].replace(0, np.nan)     * 100).round(1)
    funnel["tx_checkout_%"]  = (funnel["checkouts"] / funnel["carrinhos"].replace(0, np.nan) * 100).round(1)
    funnel["tx_conversao_%"] = (funnel["compras"]   / funnel["sessoes"].replace(0, np.nan)   * 100).round(2)
    funnel["duracao_media"]  = funnel["duracao"].round(0).astype(int)

    mob  = df[df["device"] == "mobile"]
    desk = df[df["device"] == "desktop"]

    return {
        "funil_por_canal":            funnel.drop(columns="duracao").to_dict("records"),
        "mobile_checkout2compra_%":   round(mob["purchase"].sum()  / max(mob["checkout_started"].sum(),  1) * 100, 1),
        "desktop_checkout2compra_%":  round(desk["purchase"].sum() / max(desk["checkout_started"].sum(), 1) * 100, 1),
        "total_sessoes":              int(len(df)),
    }


def processar_crm():
    conn = sqlite3.connect("data/crm.sqlite")

    ltv = pd.read_sql("""
        SELECT ROUND(AVG(lifetime_value),2) AS ltv_medio,
               COUNT(*) AS total_clientes,
               SUM(lifetime_value > 15000) AS clientes_premium,
               ROUND(SUM(lifetime_value),2) AS ltv_total
        FROM customers
    """, conn).to_dict("records")[0]

    tickets = pd.read_sql("""
        SELECT t.category,
               COUNT(*) AS total,
               ROUND(AVG(c.lifetime_value),2) AS ltv_medio_reclamante,
               SUM(t.sentiment = 'negativo') AS negativos
        FROM tickets t JOIN customers c ON t.customer_id = c.customer_id
        GROUP BY t.category ORDER BY total DESC LIMIT 6
    """, conn).to_dict("records")

    nps = pd.read_sql("""
        SELECT ROUND(AVG(score),2) AS score_medio,
               SUM(score >= 9) AS promotores,
               SUM(score <= 6) AS detratores,
               COUNT(*)        AS total
        FROM nps
    """, conn).to_dict("records")[0]
    nps["nps_score"] = round((nps["promotores"] - nps["detratores"]) / max(nps["total"], 1) * 100, 1)

    at_risk = pd.read_sql("""
        SELECT c.customer_id, ROUND(c.lifetime_value,2) AS ltv, COUNT(t.ticket_id) AS tickets
        FROM customers c JOIN tickets t ON c.customer_id = t.customer_id
        WHERE c.lifetime_value > 10000
        GROUP BY c.customer_id HAVING tickets >= 4
        ORDER BY c.lifetime_value DESC LIMIT 5
    """, conn).to_dict("records")

    conn.close()
    return {"ltv": ltv, "tickets_por_categoria": tickets, "nps": nps, "clientes_em_risco": at_risk}


# ══════════════════════════════════════════════════════════════
# Montar contexto e chamar o Groq
# ══════════════════════════════════════════════════════════════

def montar_dados(mkt, vendas, nav, crm):
    return f"""
## Marketing
{json.dumps(mkt, ensure_ascii=False, indent=2)}

## Vendas
{json.dumps(vendas, ensure_ascii=False, indent=2)}

## Navegação
{json.dumps(nav, ensure_ascii=False, indent=2)}

## CRM
{json.dumps(crm, ensure_ascii=False, indent=2)}
"""


def carregar_prompt(arquivo):
    with open(arquivo, encoding="utf-8") as f:
        return f.read()


def rodar_analise():
    mkt    = processar_marketing()
    vendas = processar_vendas()
    nav    = processar_navegacao()
    crm    = processar_crm()

    prompt_sistema = carregar_prompt("prompts/prompt_bom.txt")
    dados_ctx      = montar_dados(mkt, vendas, nav, crm)
    prompt_sistema = prompt_sistema.replace("[inserir dados aqui]", dados_ctx)

    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=4000,
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user",   "content": "Execute a análise estratégica completa dos dados fornecidos."},
        ],
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    rodar_analise()
