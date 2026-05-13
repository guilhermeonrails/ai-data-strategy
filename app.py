from dotenv import load_dotenv
load_dotenv()

import json
import sqlite3
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from groq import Groq

st.set_page_config(page_title="NexTech — Análise Estratégica", layout="wide")

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
# Processamento das bases
# ══════════════════════════════════════════════════════════════

@st.cache_data(show_spinner=False)
def processar_dados():
    # ── Marketing ────────────────────────────────────────────
    mkt = pd.read_csv("data/marketing.csv")
    mkt["platform"]    = mkt["platform"].apply(_norm_platform)
    mkt["ctr"]         = mkt["ctr"].apply(_clean_ctr)
    mkt["spend"]       = pd.to_numeric(mkt["spend"],       errors="coerce")
    mkt["clicks"]      = pd.to_numeric(mkt["clicks"],      errors="coerce")
    mkt["impressions"] = pd.to_numeric(mkt["impressions"], errors="coerce")
    mkt["sessions"]    = pd.to_numeric(mkt["sessions"],    errors="coerce")

    mkt_agg = mkt.groupby("platform").agg(
        campanhas  =("campaign_id",  "count"),
        impressoes =("impressions",  "sum"),
        cliques    =("clicks",       "sum"),
        gasto      =("spend",        "sum"),
        sessoes    =("sessions",     "sum"),
        cpc_medio  =("cpc",          "mean"),
    ).reset_index()
    mkt_agg["ctr_%"]    = (mkt_agg["cliques"] / mkt_agg["impressoes"].replace(0, np.nan) * 100).round(2)
    mkt_agg["gasto"]    = mkt_agg["gasto"].round(2)
    mkt_agg["cpc_medio"]= mkt_agg["cpc_medio"].round(2)
    total_gasto         = mkt_agg["gasto"].sum()
    mkt_agg["share_%"]  = (mkt_agg["gasto"] / total_gasto * 100).round(1)

    # ── Vendas ───────────────────────────────────────────────
    v = pd.read_excel("data/vendas.xlsx")
    v["price"]    = pd.to_numeric(v["price"],    errors="coerce")
    v["discount"] = pd.to_numeric(v["discount"], errors="coerce")
    v["receita"]  = v["price"] * (1 - v["discount"])
    v["source"]   = v["traffic_source"].apply(_norm_source)

    v_dev = v.groupby("device").agg(
        pedidos      =("order_id", "count"),
        ticket_medio =("price",    "mean"),
        desc_medio   =("discount", "mean"),
        receita      =("receita",  "sum"),
    ).reset_index()
    v_dev["ticket_medio"] = v_dev["ticket_medio"].round(2)
    v_dev["desc_medio"]   = (v_dev["desc_medio"] * 100).round(1)
    v_dev["receita"]      = v_dev["receita"].round(2)

    v_src = v.groupby("source").agg(
        pedidos      =("order_id", "count"),
        ticket_medio =("price",    "mean"),
        receita      =("receita",  "sum"),
    ).reset_index()
    v_src["ticket_medio"] = v_src["ticket_medio"].round(2)
    v_src["receita"]      = v_src["receita"].round(2)

    # ── Navegação ────────────────────────────────────────────
    with open("data/navegacao.json") as f:
        nav_raw = json.load(f)
    nav = pd.DataFrame(nav_raw)
    nav["source"] = nav["traffic_source"].apply(_norm_source)

    funil = nav.groupby("source").agg(
        sessoes   =("session_id",       "count"),
        views     =("product_view",     "sum"),
        carrinhos =("added_to_cart",    "sum"),
        checkouts =("checkout_started", "sum"),
        compras   =("purchase",         "sum"),
        duracao   =("session_duration", "mean"),
    ).reset_index()
    funil["tx_conversao_%"] = (funil["compras"] / funil["sessoes"].replace(0, np.nan) * 100).round(2)

    mob  = nav[nav["device"] == "mobile"]
    desk = nav[nav["device"] == "desktop"]
    mob_chk2buy  = mob["purchase"].sum()  / max(mob["checkout_started"].sum(),  1) * 100
    desk_chk2buy = desk["purchase"].sum() / max(desk["checkout_started"].sum(), 1) * 100

    # ── CRM ──────────────────────────────────────────────────
    conn = sqlite3.connect("data/crm.sqlite")
    ltv  = pd.read_sql("SELECT ROUND(AVG(lifetime_value),2) AS media, COUNT(*) AS total FROM customers", conn).iloc[0]
    tkt  = pd.read_sql("""
        SELECT category, COUNT(*) AS total,
               SUM(sentiment='negativo') AS negativos
        FROM tickets GROUP BY category ORDER BY total DESC LIMIT 7
    """, conn)
    nps_df = pd.read_sql("""
        SELECT SUM(score>=9) AS promotores,
               SUM(score BETWEEN 7 AND 8) AS neutros,
               SUM(score<=6) AS detratores,
               ROUND(AVG(score),1) AS score_medio
        FROM nps
    """, conn).iloc[0]
    conn.close()

    nps_score = round((nps_df["promotores"] - nps_df["detratores"]) / max(nps_df["promotores"] + nps_df["neutros"] + nps_df["detratores"], 1) * 100, 1)

    return {
        "mkt_agg": mkt_agg, "total_gasto": total_gasto,
        "v_dev": v_dev, "v_src": v_src,
        "receita_total": v["receita"].sum(), "ticket_medio": v["price"].mean(),
        "funil": funil,
        "mob_chk2buy": round(mob_chk2buy, 1), "desk_chk2buy": round(desk_chk2buy, 1),
        "total_sessoes": len(nav),
        "ltv": ltv, "tkt": tkt,
        "nps_df": nps_df, "nps_score": nps_score,
    }

# ══════════════════════════════════════════════════════════════
# Chamada ao Groq
# ══════════════════════════════════════════════════════════════

@st.cache_data(show_spinner=False)
def chamar_groq(dados_json: str) -> dict:
    with open("prompts/prompt_bom.txt", encoding="utf-8") as f:
        prompt = f.read()

    prompt = prompt.replace("[inserir dados aqui]", dados_json)

    resp = client.chat.completions.create(
        model=MODEL,
        max_tokens=4000,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user",   "content": "Execute a análise estratégica completa."},
        ],
    )
    return json.loads(resp.choices[0].message.content)

# ══════════════════════════════════════════════════════════════
# Helpers de formatação
# ══════════════════════════════════════════════════════════════

COR = {"vermelho": "#EF4444", "amarelo": "#F59E0B", "verde": "#10B981"}
ESFORCO_COR = {"Baixo": "🟢", "Médio": "🟡", "Alto": "🔴"}
URGENCIA_COR = {"Alta": "🔴", "Média": "🟡"}

def fmt_brl(v): return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ══════════════════════════════════════════════════════════════
# Render
# ══════════════════════════════════════════════════════════════

def main():
    st.title("📊 Análise Estratégica — NexTech E-commerce")
    st.caption("Período: Jun–Nov 2025 · Fontes: 4 bases integradas · Agente Analítico")

    with st.spinner("Carregando e processando dados..."):
        d = processar_dados()

    # serializa para enviar ao Groq
    dados_json = json.dumps({
        "marketing_por_plataforma": d["mkt_agg"].to_dict("records"),
        "gasto_total_R$": round(d["total_gasto"], 2),
        "vendas_por_dispositivo": d["v_dev"].to_dict("records"),
        "vendas_por_canal": d["v_src"].to_dict("records"),
        "receita_total_R$": round(d["receita_total"], 2),
        "ticket_medio_R$": round(d["ticket_medio"], 2),
        "funil_por_canal": d["funil"].to_dict("records"),
        "mobile_checkout_conversao_%": d["mob_chk2buy"],
        "desktop_checkout_conversao_%": d["desk_chk2buy"],
        "total_sessoes": d["total_sessoes"],
        "ltv_medio_R$": float(d["ltv"]["media"]),
        "total_clientes": int(d["ltv"]["total"]),
        "tickets_por_categoria": d["tkt"].to_dict("records"),
        "nps_score": d["nps_score"],
        "nps_promotores": int(d["nps_df"]["promotores"]),
        "nps_neutros": int(d["nps_df"]["neutros"]),
        "nps_detratores": int(d["nps_df"]["detratores"]),
    }, ensure_ascii=False)

    with st.spinner("Agente analisando dados..."):
        analise = chamar_groq(dados_json)

    # ── Resumo Executivo ──────────────────────────────────────
    st.header("🧭 Resumo Executivo")
    st.info(analise.get("resumo_executivo", ""))

    # ── Métricas-chave ────────────────────────────────────────
    st.header("📈 Métricas-Chave")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Receita Total",        fmt_brl(d["receita_total"]))
    c2.metric("Ticket Médio",         fmt_brl(d["ticket_medio"]))
    c3.metric("Gasto em Marketing",   fmt_brl(d["total_gasto"]))
    c4.metric("NPS Score",            f"{d['nps_score']}")
    c5.metric("Conversão Mobile Chk", f"{d['mob_chk2buy']}%",
              delta=f"{round(d['mob_chk2buy'] - d['desk_chk2buy'], 1)}% vs desktop",
              delta_color="inverse")

    # ── Gráficos ─────────────────────────────────────────────
    st.header("📊 Visão dos Dados")
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Gasto por Plataforma")
        fig = px.bar(d["mkt_agg"], x="platform", y="gasto", text="share_%",
                     color="platform",
                     color_discrete_sequence=[COR["vermelho"], COR["amarelo"], COR["verde"]],
                     labels={"platform": "", "gasto": "Gasto (R$)"})
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        fig.update_layout(showlegend=False, margin=dict(t=20))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader("Ticket Médio por Dispositivo")
        fig = px.bar(d["v_dev"], x="device", y="ticket_medio", text="ticket_medio",
                     color="device",
                     color_discrete_sequence=[COR["verde"], COR["amarelo"], COR["vermelho"]],
                     labels={"device": "", "ticket_medio": "Ticket Médio (R$)"})
        fig.update_traces(texttemplate="R$ %{text:,.0f}", textposition="outside")
        fig.update_layout(showlegend=False, margin=dict(t=20))
        st.plotly_chart(fig, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        st.subheader("Funil de Conversão por Canal")
        funil_top = d["funil"].sort_values("sessoes", ascending=False).head(5)
        fig = px.bar(funil_top, x="source", y=["sessoes", "carrinhos", "compras"],
                     barmode="group",
                     color_discrete_sequence=[COR["verde"], COR["amarelo"], COR["vermelho"]],
                     labels={"source": "", "value": "Qtd", "variable": "Etapa"})
        fig.update_layout(margin=dict(t=20))
        st.plotly_chart(fig, use_container_width=True)

    with col_d:
        st.subheader("NPS — Promotores vs Detratores")
        fig = go.Figure(go.Pie(
            labels=["Promotores", "Neutros", "Detratores"],
            values=[d["nps_df"]["promotores"], d["nps_df"]["neutros"], d["nps_df"]["detratores"]],
            hole=0.55,
            marker_colors=[COR["verde"], COR["amarelo"], COR["vermelho"]],
        ))
        fig.update_layout(margin=dict(t=20),
                          annotations=[dict(text=f"NPS<br>{d['nps_score']}", x=0.5, y=0.5,
                                           font_size=18, showarrow=False)])
        st.plotly_chart(fig, use_container_width=True)

    col_e, col_f = st.columns(2)

    with col_e:
        st.subheader("Tickets de Suporte por Categoria")
        fig = px.bar(d["tkt"].sort_values("total"), x="total", y="category",
                     orientation="h", text="total",
                     color_discrete_sequence=[COR["vermelho"]],
                     labels={"category": "", "total": "Tickets"})
        fig.update_layout(showlegend=False, margin=dict(t=20))
        st.plotly_chart(fig, use_container_width=True)

    with col_f:
        st.subheader("Checkout → Compra: Mobile vs Desktop")
        fig = go.Figure()
        for device, valor, cor in [
            ("Desktop", d["desk_chk2buy"], COR["verde"]),
            ("Mobile",  d["mob_chk2buy"],  COR["vermelho"]),
        ]:
            fig.add_trace(go.Bar(name=device, x=[device], y=[valor],
                                 marker_color=cor, text=[f"{valor}%"],
                                 textposition="outside"))
        fig.update_layout(showlegend=False, yaxis_title="Taxa (%)",
                          margin=dict(t=20), yaxis_range=[0, 30])
        st.plotly_chart(fig, use_container_width=True)

    # ── Gargalos Críticos ─────────────────────────────────────
    st.header("🚨 Gargalos Críticos")
    for g in analise.get("gargalos", []):
        st.error(
            f"**{g['nome']}**  \n"
            f"📌 {g['descricao']}  \n"
            f"📊 Evidência: {g['evidencia']}  \n"
            f"💸 Impacto estimado: **{g['impacto_rs']}**"
        )

    # ── Oportunidades ─────────────────────────────────────────
    st.header("💡 Oportunidades Imediatas")
    rows = []
    for o in analise.get("oportunidades", []):
        rows.append({
            "Oportunidade": o["descricao"],
            "Canal / Área": o["canal"],
            "Impacto Estimado": o["impacto_rs"],
            "Esforço": f"{ESFORCO_COR.get(o['esforco'], '')} {o['esforco']}",
        })
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ── Relações entre bases ──────────────────────────────────
    st.header("🔗 Relações Entre Bases")
    rows = []
    for r in analise.get("relacoes", []):
        rows.append({
            "Cruzamento":  r["cruzamento"],
            "Descoberta":  r["descoberta"],
            "Impacto":     r["impacto"],
        })
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ── Recomendações ─────────────────────────────────────────
    st.header("✅ Recomendações Acionáveis")
    for i, rec in enumerate(analise.get("recomendacoes", []), 1):
        with st.expander(f"{i}. {rec['titulo']} — {rec['impacto_rs']} / mês"):
            c1, c2 = st.columns(2)
            c1.markdown(f"**O quê:** {rec['o_que']}")
            c1.markdown(f"**Por quê:** {rec['por_que']}")
            c2.markdown(f"**Impacto:** `{rec['impacto_rs']} / mês`")
            c2.markdown(f"**Prazo sugerido:** {rec.get('prazo_dias', '—')} dias")

    # ── Alertas e Riscos ──────────────────────────────────────
    st.header("⚠️ Alertas e Riscos")
    for a in analise.get("alertas", []):
        urgencia = URGENCIA_COR.get(a["urgencia"], "🟡")
        st.warning(
            f"{urgencia} **{a['risco']}**  \n"
            f"📊 Sinal: {a['sinal']}  \n"
            f"⚡ Consequência: {a['consequencia']}"
        )

    st.divider()
    st.caption("Análise gerada por Agente Analítico com contexto estruturado · NexTech 2025")


if __name__ == "__main__":
    main()
