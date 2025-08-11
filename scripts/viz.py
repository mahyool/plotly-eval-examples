#!/usr/bin/env python3
"""
CRM-style dashboard matching the reference:
- KPI cards
- Line: Tickets Created vs Tickets Solved
- Donut: Tickets by Type
- Donut: New vs Returned
- Bar: Tickets per Weekday
Outputs a single self-contained HTML.
"""
import pandas as pd
import plotly.graph_objects as go

DARK_BG = "#0f1221"
CARD_BG = "#14172a"
INK = "#e8ecff"

def load():
    kpis   = pd.read_csv("../data/metrics.csv")
    ts     = pd.read_csv("../data/tickets_timeseries.csv", parse_dates=["date"])
    bytype = pd.read_csv("../data/tickets_by_type.csv")
    newret = pd.read_csv("../data/new_vs_returned.csv")
    wk     = pd.read_csv("../data/tickets_by_weekday.csv")
    return kpis, ts, bytype, newret, wk

def fig_kpi(title, value, suffix="", delta=None):
    return go.Figure(go.Indicator(
        mode="number+delta" if delta is not None else "number",
        value=float(value),
        delta=dict(reference=float(value)-float(delta), increasing=dict(color="#25d28a"),
                   decreasing=dict(color="#ff6b9a")) if delta is not None else None,
        number=dict(suffix=suffix, font=dict(size=40, color=INK)),
        title={"text": f"<b>{title}</b>", "font":{"size":14, "color":INK}},
        domain={"x":[0,1], "y":[0,1]}
    )).update_layout(template="plotly_dark", paper_bgcolor=CARD_BG, margin=dict(t=10,l=10,r=10,b=0),
                     height=100)

def fig_line(ts):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ts["date"], y=ts["tickets_created"], name="Tickets Created",
                             mode="lines", line=dict(width=3, color="#a66bff")))
    fig.add_trace(go.Scatter(x=ts["date"], y=ts["tickets_solved"], name="Tickets Solved",
                             mode="lines", line=dict(width=3, color="#5cc8ff")))
    fig.update_layout(template="plotly_dark", paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
                      height=330, margin=dict(t=60,l=16,r=16,b=10),
                      title=dict(text="<b>Tickets Created vs Tickets Solved</b>", x=0.01, xanchor="left"),
                      legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center", bgcolor="rgba(0,0,0,0)"))
    fig.update_yaxes(gridcolor="rgba(255,255,255,.08)")
    fig.update_xaxes(gridcolor="rgba(255,255,255,.08)")
    return fig

def fig_donut(labels, values, title):
    fig = go.Figure(go.Pie(labels=labels, values=values, hole=0.55,
                           textinfo="percent+label", insidetextorientation="radial"))
    fig.update_traces(marker=dict(colors=["#2dd4ff","#7c3aed","#22c55e","#f59e0b","#ef4444","#a78bfa"][:len(labels)],
                                  line=dict(color=DARK_BG, width=2)))
    fig.update_layout(template="plotly_dark", paper_bgcolor=CARD_BG, height=300,
                      margin=dict(t=60,l=16,r=16,b=10),
                      title=dict(text=f"<b>{title}</b>", x=0.01, xanchor="left"))
    return fig

def fig_bar_weekday(df):
    fig = go.Figure(go.Bar(x=df["weekday"], y=df["count"], marker=dict(
        color=["#2dd4ff","#60a5fa","#a78bfa","#7c3aed","#22c55e","#f59e0b"])))
    fig.update_layout(template="plotly_dark", paper_bgcolor=CARD_BG, height=300,
                      margin=dict(t=60,l=16,r=16,b=10),
                      title=dict(text="<b>Number of Tickets / Week Day</b>", x=0.01, xanchor="left"))
    fig.update_yaxes(gridcolor="rgba(255,255,255,.08)")
    return fig

def build(kpis, ts, bytype, newret, wk, output="../outputs/dashboard.html"):
    cards = []
    for _, r in kpis.iterrows():
        delta = r["delta"] if pd.notna(r["delta"]) else None
        suffix = r["suffix"] if pd.notna(r["suffix"]) else ""
        cards.append(fig_kpi(r["metric"], r["value"], suffix=suffix, delta=delta))

    line = fig_line(ts)
    donut_type = fig_donut(bytype["type"], bytype["count"], "Tickets By Type")
    donut_ret  = fig_donut(newret["label"], newret["count"], "New Tickets vs Returned Tickets")
    bar_wk = fig_bar_weekday(wk)

    html = f"""
<style>
body {{ background:{DARK_BG}; color:{INK}; font-family: Inter, -apple-system, Segoe UI, Roboto, Arial; }}
.grid {{ display:grid; grid-template-columns: repeat(12, 1fr); gap:14px; max-width:1400px; margin:24px auto; }}
.card {{ border-radius:16px; overflow:hidden; }}
.kpi {{ grid-column: span 4; }}
.line {{ grid-column: span 12; }}
.half {{ grid-column: span 6; }}
</style>
<div class="grid">
  <div class="card kpi">{cards[0].to_html(full_html=False, include_plotlyjs=True)}</div>
  <div class="card kpi">{cards[1].to_html(full_html=False, include_plotlyjs=False)}</div>
  <div class="card kpi">{cards[2].to_html(full_html=False, include_plotlyjs=False)}</div>
  <div class="card kpi">{cards[3].to_html(full_html=False, include_plotlyjs=False)}</div>

  <div class="card line">{line.to_html(full_html=False, include_plotlyjs=False)}</div>
  <div class="card half">{donut_type.to_html(full_html=False, include_plotlyjs=False)}</div>
  <div class="card half">{donut_ret.to_html(full_html=False, include_plotlyjs=False)}</div>
  <div class="card half">{bar_wk.to_html(full_html=False, include_plotlyjs=False)}</div>
</div>
"""
    with open(output, "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    k, ts, bt, nr, wk = load()
    build(k, ts, bt, nr, wk)
    print("Dashboard created")
