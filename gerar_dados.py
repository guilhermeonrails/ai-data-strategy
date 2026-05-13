#!/usr/bin/env python3
"""
Gerador de dados fictícios — NexTech E-commerce
Eletrônicos e Games | Demonstração IA Analítica
"""

from dotenv import load_dotenv
load_dotenv()

import pandas as pd
import numpy as np
import json
import sqlite3
import os
import random
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

os.makedirs("data", exist_ok=True)

START_DATE = datetime(2025, 6, 1)
END_DATE   = datetime(2025, 11, 30)

STATES = ["SP", "RJ", "MG", "RS", "PR", "BA", "SC", "GO", "PE", "CE"]

PRODUCTS = [
    {"name": "Smartphone Samsung Galaxy A55",    "category": "Smartphones", "base_price": 1800,  "tier": "mid"},
    {"name": "iPhone 15 128GB",                  "category": "Smartphones", "base_price": 4500,  "tier": "premium"},
    {"name": "TV Samsung 55\" QLED 4K",          "category": "Televisores", "base_price": 4200,  "tier": "premium"},
    {"name": "Notebook Dell Inspiron 15",         "category": "Computadores","base_price": 3500,  "tier": "premium"},
    {"name": "Cadeira Gamer ThunderX3",           "category": "Games",       "base_price": 1200,  "tier": "mid"},
    {"name": "PlayStation 5",                     "category": "Consoles",    "base_price": 3800,  "tier": "premium"},
    {"name": "Xbox Series X",                     "category": "Consoles",    "base_price": 3500,  "tier": "premium"},
    {"name": "Headset JBL Quantum 800",           "category": "Audio",       "base_price": 350,   "tier": "low"},
    {"name": "Smart Watch Samsung Galaxy Watch 6","category": "Wearables",   "base_price": 800,   "tier": "mid"},
    {"name": "Tablet Samsung Galaxy Tab A9",      "category": "Tablets",     "base_price": 1500,  "tier": "mid"},
    {"name": "Caixa de Som JBL Charge 5",         "category": "Audio",       "base_price": 280,   "tier": "low"},
    {"name": "Monitor LG UltraWide 29\"",         "category": "Monitores",   "base_price": 1800,  "tier": "mid"},
    {"name": "Teclado Mecânico Redragon K552",    "category": "Periféricos", "base_price": 450,   "tier": "low"},
    {"name": "Mouse Gamer Logitech G502",         "category": "Periféricos", "base_price": 350,   "tier": "low"},
    {"name": "Fone AirPods Pro 2",               "category": "Audio",       "base_price": 1900,  "tier": "premium"},
]


def rand_date(start=START_DATE, end=END_DATE):
    return start + timedelta(days=random.randint(0, (end - start).days))


def messy_date(d, fmt="%Y-%m-%d"):
    """Occasionally returns date in an inconsistent format (problema intencional)."""
    r = random.random()
    if r < 0.04:
        return d.strftime("%d/%m/%Y")
    if r < 0.06:
        return d.strftime("%Y/%m/%d")
    return d.strftime(fmt)


# ─────────────────────────────────────────────────────────────
# BASE 1 — marketing.csv
# ─────────────────────────────────────────────────────────────

def gerar_marketing(path="data/marketing.csv"):
    platform_cfg = {
        "Google Ads": {
            "n": 800,
            "variants": ["Google Ads", "Google Ads", "Google Ads", "Google", "google ads", "Google AdWords"],
            "impressions": (8_000, 65_000),
            "ctr": (0.030, 0.058),
            "cpc": (2.50, 5.80),
            "spend": (400, 3_500),
            "session_ratio": (0.88, 0.96),
        },
        "Instagram": {
            "n": 1_500,
            "variants": ["Instagram", "Instagram", "Instagram", "instagram", "Instagram Ads", "INSTAGRAM"],
            "impressions": (40_000, 280_000),
            "ctr": (0.009, 0.024),
            "cpc": (0.70, 2.20),
            "spend": (250, 2_200),
            "session_ratio": (0.65, 0.82),
        },
        "TikTok": {
            "n": 2_000,
            "variants": ["TikTok", "TikTok", "TikTok", "Tiktok", "tiktok", "TIKTOK"],
            "impressions": (150_000, 1_800_000),
            "ctr": (0.003, 0.009),
            "cpc": (0.18, 0.85),
            "spend": (180, 1_600),
            "session_ratio": (0.50, 0.72),
        },
    }

    campaign_types = [
        "Awareness", "Conversão", "Remarketing", "Black_Friday",
        "Natal", "Verão", "Branding", "Performance",
    ]

    rows = []
    cid = 1
    for plat, cfg in platform_cfg.items():
        for _ in range(cfg["n"]):
            impressions = random.randint(*cfg["impressions"])
            ctr        = round(random.uniform(*cfg["ctr"]), 4)
            clicks     = max(1, int(impressions * ctr))
            cpc        = round(random.uniform(*cfg["cpc"]), 2)
            spend      = round(random.uniform(*cfg["spend"]), 2)
            sessions   = int(clicks * random.uniform(*cfg["session_ratio"]))
            d          = rand_date()
            plat_name  = random.choice(cfg["variants"])
            ctype      = random.choice(campaign_types)
            suffix     = random.randint(100, 999)
            name       = f"{plat.replace(' ','_')}_{ctype}_{suffix}"

            # ── problemas intencionais ──
            if random.random() < 0.030:
                sessions = None
            if random.random() < 0.020:
                ctr = None
                clicks = None
            if random.random() < 0.015:
                impressions = 0          # anomalia: 0 impressões com cliques

            # CTR como string percentual em ~8% dos casos
            ctr_val = (
                f"{ctr * 100:.2f}%"
                if (ctr is not None and random.random() < 0.08)
                else ctr
            )

            rows.append({
                "campaign_id":   f"CMP{cid:05d}",
                "platform":      plat_name,
                "campaign_name": name,
                "impressions":   impressions,
                "clicks":        clicks,
                "ctr":           ctr_val,
                "cpc":           cpc,
                "spend":         spend,
                "sessions":      sessions,
                "date":          messy_date(d),
            })
            cid += 1

    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    print(f"  ✓  marketing.csv          — {len(df):,} linhas")
    return df


# ─────────────────────────────────────────────────────────────
# BASE 2 — vendas.xlsx
# ─────────────────────────────────────────────────────────────

def gerar_vendas(path="data/vendas.xlsx"):
    PAYMENT_TYPES = [
        "credit_card", "pix", "debit_card", "boleto",
        "cartão de crédito", "PIX",          # inconsistências intencionais
    ]
    TRAFFIC_SOURCES = {
        "google_ads": 0.22, "instagram": 0.28, "tiktok": 0.18,
        "organic":    0.15, "direct":    0.10, "email":   0.07,
    }
    DEVICE_CFG = {
        "desktop": {"prob": 0.42, "price_mult": (1.05, 1.20), "disc": (0.00, 0.18)},
        "mobile":  {"prob": 0.48, "price_mult": (0.82, 0.95), "disc": (0.05, 0.30)},
        "tablet":  {"prob": 0.10, "price_mult": (0.95, 1.05), "disc": (0.02, 0.20)},
    }
    TRAFFIC_TIER = {
        "google_ads": ["premium"],
        "instagram":  ["mid", "low"],
        "tiktok":     ["low", "low", "mid"],
        "organic":    ["mid", "premium"],
        "direct":     ["mid", "premium"],
        "email":      ["mid"],
    }
    CATEGORY_VARIANTS = {
        "Smartphones": ["Smartphones", "Celulares", "smartphone", "Celular"],
        "Televisores": ["Televisores", "TVs", "Televisão", "televisores"],
        "Computadores":["Computadores","Laptops","Notebook","computadores"],
        "Games":       ["Games", "Gamer", "games", "Gaming"],
        "Consoles":    ["Consoles", "Console", "Video Game", "consoles"],
        "Audio":       ["Áudio", "Audio", "áudio", "Som"],
        "Wearables":   ["Wearables", "Smartwatch", "wearables"],
        "Tablets":     ["Tablets", "Tablet", "tablets"],
        "Monitores":   ["Monitores", "Monitor", "monitores"],
        "Periféricos": ["Periféricos", "Perifericos", "Acessórios", "periferico"],
    }
    SRC_VARIANTS = {
        "google_ads": ["google", "Google Ads", "google_ads", "Google"],
        "instagram":  ["Instagram", "instagram_ads", "ig", "Instagram Ads"],
        "tiktok":     ["TikTok", "tiktok_ads", "Tiktok"],
    }

    sources = list(TRAFFIC_SOURCES.keys())
    s_probs = list(TRAFFIC_SOURCES.values())
    devices = list(DEVICE_CFG.keys())
    d_probs = [DEVICE_CFG[d]["prob"] for d in devices]

    rows = []
    for i in range(3_000):
        traffic = np.random.choice(sources, p=s_probs)
        tier    = random.choice(TRAFFIC_TIER.get(traffic, ["mid"]))
        cands   = [p for p in PRODUCTS if p["tier"] == tier] or PRODUCTS
        product = random.choice(cands)

        device  = np.random.choice(devices, p=d_probs)
        dcfg    = DEVICE_CFG[device]
        price   = round(product["base_price"] * random.uniform(*dcfg["price_mult"]), 2)
        discount= round(random.uniform(*dcfg["disc"]), 2)
        payment = random.choice(PAYMENT_TYPES)
        state   = random.choice(STATES)
        d       = rand_date()
        cat_var = CATEGORY_VARIANTS.get(product["category"], [product["category"]])
        category= random.choice(cat_var)
        cust_id = f"CUST{random.randint(1, 2000):05d}"

        # ── problemas intencionais ──
        if random.random() < 0.020:
            state = None
        if random.random() < 0.015:
            payment = None
        if random.random() < 0.060:
            traffic = random.choice(SRC_VARIANTS.get(traffic, [traffic]))

        ts_fmt = "%Y-%m-%d %H:%M:%S" if random.random() > 0.10 else "%Y-%m-%d"
        rows.append({
            "order_id":       f"ORD{i + 1:06d}",
            "customer_id":    cust_id,
            "product":        product["name"],
            "category":       category,
            "price":          price,
            "discount":       discount,
            "payment_type":   payment,
            "state":          state,
            "device":         device,
            "traffic_source": traffic,
            "created_at":     messy_date(d, ts_fmt),
        })

    df = pd.DataFrame(rows)
    df.to_excel(path, index=False)
    print(f"  ✓  vendas.xlsx            — {len(df):,} linhas")
    return df


# ─────────────────────────────────────────────────────────────
# BASE 3 — navegacao.json
# ─────────────────────────────────────────────────────────────

def gerar_navegacao(path="data/navegacao.json"):
    TRAFFIC_CFG = {
        "instagram": {
            "n": 3_500,
            "home_p":     0.90, "view_p":     0.60,
            "cart_p":     0.12, "checkout_p": 0.07,
            "purchase_p": 0.03,
            "duration":   (15, 90),
            "device_bias":{"mobile": 0.78, "desktop": 0.15, "tablet": 0.07},
        },
        "google_ads": {
            "n": 2_000,
            "home_p":     0.70, "view_p":     0.80,
            "cart_p":     0.35, "checkout_p": 0.28,
            "purchase_p": 0.20,
            "duration":   (90, 480),
            "device_bias":{"mobile": 0.40, "desktop": 0.52, "tablet": 0.08},
        },
        "tiktok": {
            "n": 2_800,
            "home_p":     0.92, "view_p":     0.50,
            "cart_p":     0.08, "checkout_p": 0.04,
            "purchase_p": 0.015,
            "duration":   (8, 45),
            "device_bias":{"mobile": 0.91, "desktop": 0.06, "tablet": 0.03},
        },
        "organic": {
            "n": 1_000,
            "home_p":     0.80, "view_p":     0.72,
            "cart_p":     0.30, "checkout_p": 0.22,
            "purchase_p": 0.16,
            "duration":   (120, 600),
            "device_bias":{"mobile": 0.45, "desktop": 0.48, "tablet": 0.07},
        },
        "direct": {
            "n": 700,
            "home_p":     0.75, "view_p":     0.78,
            "cart_p":     0.38, "checkout_p": 0.30,
            "purchase_p": 0.22,
            "duration":   (150, 700),
            "device_bias":{"mobile": 0.38, "desktop": 0.55, "tablet": 0.07},
        },
    }

    SRC_VARIANTS = {
        "google_ads": ["google", "Google Ads", "google_ads"],
        "instagram":  ["Instagram", "ig", "instagram"],
        "tiktok":     ["TikTok", "tiktok"],
    }
    MOBILE_CHECKOUT_PENALTY = 0.45

    events = []
    sess_n = 1

    for source, cfg in TRAFFIC_CFG.items():
        devs   = list(cfg["device_bias"].keys())
        d_prob = list(cfg["device_bias"].values())

        for _ in range(cfg["n"]):
            device = np.random.choice(devs, p=d_prob)

            home     = 1 if random.random() < cfg["home_p"] else 0
            view     = 1 if home     and random.random() < cfg["view_p"] else 0
            cart     = 1 if view     and random.random() < cfg["cart_p"] else 0

            chk_p    = cfg["checkout_p"] * (0.75 if device == "mobile" else 1.0)
            checkout = 1 if cart     and random.random() < chk_p else 0

            pur_p    = cfg["purchase_p"]
            if device == "mobile" and checkout:
                pur_p *= MOBILE_CHECKOUT_PENALTY
            purchase = 1 if checkout and random.random() < pur_p else 0

            duration = random.randint(*cfg["duration"])
            if not view:
                duration = min(duration, 30)

            src_display = (
                random.choice(SRC_VARIANTS.get(source, [source]))
                if random.random() < 0.05
                else source
            )

            events.append({
                "session_id":       f"SES{sess_n:07d}",
                "clicked_home":     home,
                "product_view":     view,
                "added_to_cart":    cart,
                "checkout_started": checkout,
                "purchase":         purchase,
                "device":           device,
                "traffic_source":   src_display,
                "session_duration": duration,
            })
            sess_n += 1

    random.shuffle(events)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)

    print(f"  ✓  navegacao.json         — {len(events):,} eventos")
    return events


# ─────────────────────────────────────────────────────────────
# BASE 4 — crm.sqlite
# ─────────────────────────────────────────────────────────────

def gerar_crm(path="data/crm.sqlite"):
    conn = sqlite3.connect(path)
    cur  = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS nps;
        DROP TABLE IF EXISTS tickets;
        DROP TABLE IF EXISTS customers;

        CREATE TABLE customers (
            customer_id    TEXT PRIMARY KEY,
            name           TEXT,
            email          TEXT,
            state          TEXT,
            lifetime_value REAL,
            created_at     TEXT
        );
        CREATE TABLE tickets (
            ticket_id   TEXT PRIMARY KEY,
            customer_id TEXT,
            category    TEXT,
            status      TEXT,
            sentiment   TEXT,
            created_at  TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );
        CREATE TABLE nps (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT,
            score       INTEGER,
            feedback    TEXT,
            collected_at TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );
    """)

    TICKET_CATS   = [
        "Entrega atrasada", "Produto com defeito", "Devolução",
        "Problema no pagamento", "Dúvida técnica", "Troca", "Cancelamento",
    ]
    TICKET_STATUS = ["aberto", "resolvido", "em_andamento", "fechado"]
    SENTIMENTS    = ["positivo", "negativo", "neutro", "negativo", "negativo"]

    FEEDBACK_BAD  = [
        "Produto chegou com defeito.",
        "Atendimento péssimo, demorou muito.",
        "Tive problemas com o pagamento.",
        "Produto diferente da descrição.",
        "Não vou comprar novamente.",
        "Frete demorou 3 semanas.",
        "Suporte não resolve nada.",
        "Produto parou de funcionar em 2 dias.",
    ]
    FEEDBACK_GOOD = [
        "Ótimo produto, entrega rápida!",
        "Produto incrível, muito satisfeito.",
        "Atendimento excelente.",
        "Chegou antes do prazo.",
        "Recomendo muito!",
        "Qualidade superior ao esperado.",
        "Melhor compra que já fiz.",
    ]

    FIRST = ["Ana","João","Maria","Pedro","Lucas","Carla","Rafael","Fernanda",
             "Bruno","Juliana","Carlos","Patrícia","Marcos","Aline","Roberto",
             "Camila","André","Larissa","Felipe","Beatriz","Diego","Isabela"]
    LAST  = ["Silva","Santos","Oliveira","Souza","Lima","Costa","Ferreira",
             "Alves","Pereira","Gomes","Rodrigues","Martins","Rocha","Nascimento"]

    customers = []
    ids = [f"CUST{i:05d}" for i in range(1, 2001)]

    for cid in ids:
        name  = f"{random.choice(FIRST)} {random.choice(LAST)}"
        email = (
            f"{name.lower().replace(' ', '.')}{random.randint(1, 99)}"
            f"@{'gmail.com' if random.random() > 0.3 else 'hotmail.com'}"
        )
        state = random.choice(STATES)
        # distribuição de LTV com cauda longa
        r = random.random()
        if r < 0.08:
            ltv = round(random.uniform(15_000, 80_000), 2)
        elif r < 0.30:
            ltv = round(random.uniform(3_000, 15_000), 2)
        else:
            ltv = round(random.uniform(200, 3_000), 2)

        d = rand_date(datetime(2023, 1, 1), END_DATE)
        customers.append((cid, name, email, state, ltv, d.strftime("%Y-%m-%d")))

    cur.executemany("INSERT INTO customers VALUES (?,?,?,?,?,?)", customers)

    tickets = []
    tid = 1
    for cid, _, _, _, ltv, _ in customers:
        if ltv > 15_000:
            n = random.choices(range(1, 9), weights=[10,15,20,20,15,10,7,3])[0]
        else:
            n = random.choices(range(0, 7),  weights=[30,25,20,12,7,4,2])[0]

        for _ in range(n):
            cat       = random.choice(TICKET_CATS)
            status    = random.choice(TICKET_STATUS)
            sentiment = random.choice(SENTIMENTS)
            d         = rand_date()
            tickets.append((
                f"TKT{tid:06d}", cid, cat, status, sentiment,
                d.strftime("%Y-%m-%d %H:%M:%S"),
            ))
            tid += 1

    cur.executemany("INSERT INTO tickets VALUES (?,?,?,?,?,?)", tickets)

    # NPS — taxa de resposta ~55%
    ticket_counts = {}
    for t in tickets:
        ticket_counts[t[1]] = ticket_counts.get(t[1], 0) + 1

    nps_rows = []
    for cid, *_ in customers:
        if random.random() > 0.55:
            continue
        tc = ticket_counts.get(cid, 0)
        if tc >= 3:
            score    = random.choices(range(11), weights=[5,5,5,8,7,5,5,8,10,12,10])[0]
            feedback = random.choice(FEEDBACK_BAD)
        elif tc >= 1:
            score    = random.choices(range(11), weights=[2,2,3,4,5,6,8,12,15,18,15])[0]
            feedback = random.choice(FEEDBACK_BAD if score < 6 else FEEDBACK_GOOD)
        else:
            score    = random.choices(range(11), weights=[1,1,1,2,3,5,8,12,18,22,22])[0]
            feedback = random.choice(FEEDBACK_GOOD if score >= 7 else FEEDBACK_BAD)

        d = rand_date()
        nps_rows.append((cid, score, feedback, d.strftime("%Y-%m-%d")))

    cur.executemany(
        "INSERT INTO nps (customer_id, score, feedback, collected_at) VALUES (?,?,?,?)",
        nps_rows,
    )
    conn.commit()
    conn.close()

    print(
        f"  ✓  crm.sqlite              — "
        f"{len(customers):,} clientes | {len(tickets):,} tickets | {len(nps_rows):,} NPS"
    )


# ─────────────────────────────────────────────────────────────
# BÔNUS — marketing_dezembro.csv (demo do pipeline)
# ─────────────────────────────────────────────────────────────

def gerar_marketing_dezembro(path="data/marketing_dezembro.csv"):
    DEC_START = datetime(2025, 12, 1)
    DEC_END   = datetime(2025, 12, 31)

    platforms = ["Google Ads", "Instagram", "TikTok"]
    ctypes    = ["Black_Friday", "Natal", "Fim_de_Ano", "Liquidação"]
    rows = []

    for i in range(500):
        plat      = random.choice(platforms)
        ctype     = random.choice(ctypes)
        impressions = random.randint(50_000, 2_000_000)
        ctr       = round(random.uniform(0.003, 0.055), 4)
        clicks    = max(1, int(impressions * ctr))
        spend     = round(random.uniform(300, 5_000), 2)
        sessions  = int(clicks * random.uniform(0.65, 0.93))
        d         = rand_date(DEC_START, DEC_END)

        rows.append({
            "campaign_id":   f"CMP_DEC_{i + 1:04d}",
            "platform":      plat,
            "campaign_name": f"{plat.replace(' ','_')}_{ctype}_{i + 1}",
            "impressions":   impressions,
            "clicks":        clicks,
            "ctr":           ctr,
            "cpc":           round(spend / max(clicks, 1), 2),
            "spend":         spend,
            "sessions":      sessions,
            "date":          d.strftime("%Y-%m-%d"),
        })

    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    print(f"  ✓  marketing_dezembro.csv — {len(df):,} linhas  (demo pipeline)")


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("  NexTech E-commerce — Geração de Bases Fictícias")
    print("=" * 55 + "\n")

    gerar_marketing()
    gerar_vendas()
    gerar_navegacao()
    gerar_crm()
    gerar_marketing_dezembro()

    print("\n" + "=" * 55)
    print("  Todas as bases geradas em ./data/")
    print("=" * 55 + "\n")
