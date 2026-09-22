"""IPL Franchise Business Intelligence: Streamlit app.

Run from the project root:   streamlit run app/app.py
Reads data/processed/player_roi.csv and roi_params.json (created by notebooks/04_roi_formula.ipynb).
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))
from roi_model import business_roi, value_players  # noqa: E402

st.set_page_config(page_title="IPL Franchise Business Intelligence", page_icon="🏏", layout="wide")

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"
DOCS = ROOT / "docs"
DEFAULTS = {"V": 20, "on_share": 70, "star_w": 10, "multiple": 1.0}
CAVEAT = ("Business value is **modelled, not measured**: revenue per player is not public. "
          "ROI 1.0 means the market average for the money paid, not rupees earned.")
DETAIL_COLS = ["season", "player_name", "team", "role", "price_cr", "matches_played",
               "impact", "value_cr", "roi", "surplus_cr"]


# ------------------------------------------------------------------ data
@st.cache_data
def load_data():
    players = pd.read_csv(PROCESSED / "player_roi.csv")
    with open(PROCESSED / "roi_params.json", encoding="utf-8") as f:
        params = json.load(f)
    par = pd.DataFrame(params["par"]).set_index("season_year")
    players["season"] = players["season"].astype(int)
    players["origin"] = players["is_overseas"].map({True: "Overseas", False: "Indian"}).fillna("Unknown")
    return players, params, par


try:
    players, params, par = load_data()
except FileNotFoundError:
    st.error("Data files not found. Run notebooks/02_data_cleaning.ipynb and notebooks/04_roi_formula.ipynb "
             "first: they create data/processed/player_roi.csv and roi_params.json.")
    st.stop()


@st.cache_data
def run_model(wicket_value, on_share_pct, star_w, multiple):
    return value_players(players, par, wicket_value, on_share_pct / 100, star_w, multiple,
                         params.get("team_brand") or {})


# ------------------------------------------------------------------ sidebar
for key, value in DEFAULTS.items():
    st.session_state.setdefault(key, value)


def reset_assumptions():
    for k, v in DEFAULTS.items():
        st.session_state[k] = v


st.sidebar.title("🏏 IPL Business Intelligence")
PAGES = ["Overview", "Player ROI calculator", "Auction value tracker",
         "Franchise dashboard", "Player explorer", "Method and limits"]
page = st.sidebar.radio("Page", PAGES)

st.sidebar.header("Model assumptions")
st.sidebar.slider("Runs one wicket is worth", 5, 40, key="V",
                  help="A bowler gains this many runs of impact per wicket; a batter loses it when dismissed.")
st.sidebar.slider("On-field share of business value (%)", 30, 95, step=5, key="on_share",
                  help="The rest is off-field brand value, shared by screen time and star moments.")
st.sidebar.slider("Star bonus (balls of screen time per six or wicket)", 0, 30, key="star_w")
st.sidebar.slider("Business value per rupee of salary at the market average", 1.0, 5.0, step=0.5, key="multiple",
                  help="1.0 means the value shared out equals total salaries. Higher values scale value and ROI equally.")
st.sidebar.button("Reset to defaults", on_click=reset_assumptions)

V = st.session_state["V"]
ON_SHARE = st.session_state["on_share"]
STAR_W = st.session_state["star_w"]
MULTIPLE = st.session_state["multiple"]

model, rates = run_model(V, ON_SHARE, STAR_W, MULTIPLE)
TEAM_BRAND = params.get("team_brand") or {}


# ------------------------------------------------------------------ pages
def page_overview():
    st.title("IPL Franchise Business Intelligence")
    st.subheader("Was this player worth the auction price?")
    st.info(CAVEAT)

    spend = model["price_cr"].sum()
    value_sorted = model["value_cr"].sort_values(ascending=False).reset_index(drop=True)
    top10 = value_sorted.head(int(len(value_sorted) * 0.10)).sum() / value_sorted.sum()
    unused = model.loc[~model["played"], "price_cr"].sum() / spend

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Auction purchases", f"{len(model):,}")
    c2.metric("Total spend", f"{spend:,.0f} cr")
    c3.metric("Returned more than cost", f"{(model['roi'] > 1).mean():.0%}")
    c4.metric("Value from top 10%", f"{top10:.0%}")
    c5.metric("Spend on players who never played", f"{unused:.1%}")

    curve = pd.DataFrame({
        "Share of purchases (%)": np.arange(1, len(value_sorted) + 1) / len(value_sorted) * 100,
        "Share of business value (%)": value_sorted.cumsum() / value_sorted.sum() * 100,
    })
    fig = px.line(curve, x="Share of purchases (%)", y="Share of business value (%)",
                  title="A few purchases create most of the value (purchases ranked best first)")
    fig.add_shape(type="line", x0=0, y0=0, x1=100, y1=100, line=dict(dash="dash"))
    st.plotly_chart(fig)

    st.markdown(
        "**Headline findings at the default assumptions** (2022-2024 auction purchases)\n"
        "- Price only moderately predicts performance, and returns per crore fall sharply as price rises.\n"
        "- A few purchases carry the returns: the top 10% create about 63% of business value.\n"
        "- The best surpluses came from cheap discoveries, not the biggest signings.\n"
        "- About 32% of purchases never played, taking 12.3% of spend, and injuries explain the largest 2022 losses.\n"
        "- Team rankings are fragile: only the best (DC) and worst (KKR) hold up when one player is removed."
    )
    st.caption("Use the sidebar to change the model assumptions; every page recalculates.")


def page_calculator():
    st.title("Player ROI calculator")
    st.info(CAVEAT)
    st.write("Enter a price and a season's stats to estimate the business value and ROI, "
             "or start from a real purchase.")

    ranked = model.sort_values("price_cr", ascending=False)
    labels = {f"{r.player_name} ({r.season}, {r.team}, {r.price_cr:g} cr)": i for i, r in ranked.iterrows()}
    none_label = "Enter my own numbers"
    choice = st.selectbox("Start from a real purchase (optional)", [none_label] + list(labels))
    row = None if choice == none_label else model.loc[labels[choice]]
    tag = "own" if row is None else str(labels[choice])

    def default(col, fallback=0):
        return fallback if row is None else float(row[col])

    seasons = sorted(par.index.astype(int).tolist(), reverse=True)
    teams = ["Not specified"] + sorted(players["team"].dropna().unique().tolist())
    left, mid, right = st.columns(3)
    with left:
        st.markdown("**Purchase**")
        price = st.number_input("Price paid (crore)", 0.1, 50.0, value=float(max(default("price_cr", 5.0), 0.1)),
                                step=0.25, key=f"price_{tag}")
        season_default = seasons.index(int(row["season"])) if row is not None else 0
        season = st.selectbox("Season (sets the league averages)", seasons, index=season_default, key=f"season_{tag}")
        team_default = teams.index(row["team"]) if row is not None and row["team"] in teams else 0
        team = st.selectbox("Team", teams, index=team_default, key=f"team_{tag}")
    with mid:
        st.markdown("**Batting**")
        runs = st.number_input("Runs", 0, 1200, value=int(default("runs")), step=10, key=f"runs_{tag}")
        balls_faced = st.number_input("Balls faced", 0, 900, value=int(default("balls_faced")), step=10, key=f"bf_{tag}")
        dismissals = st.number_input("Times dismissed", 0, 30, value=int(default("dismissals")), key=f"dis_{tag}")
        sixes = st.number_input("Sixes", 0, 80, value=int(default("sixes")), key=f"six_{tag}")
    with right:
        st.markdown("**Bowling**")
        wickets = st.number_input("Wickets", 0, 40, value=int(default("wickets")), key=f"wk_{tag}")
        balls_bowled = st.number_input("Balls bowled (6 = 1 over)", 0, 500, value=int(default("balls_bowled")),
                                       step=6, key=f"bb_{tag}")
        conceded = st.number_input("Runs conceded", 0, 800, value=int(default("runs_conceded")), step=10,
                                   key=f"rc_{tag}")

    result = business_roi(price, season, par, rates, V, STAR_W,
                          team=None if team == "Not specified" else team, team_brand=TEAM_BRAND,
                          runs=runs, balls_faced=balls_faced, dismissals=dismissals, sixes=sixes,
                          wickets=wickets, balls_bowled=balls_bowled, runs_conceded=conceded)

    st.divider()
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Impact (runs above average)", f"{result['impact_runs']:+.0f}")
    m2.metric("On-field value", f"{result['on_field_value_cr']:.2f} cr")
    m3.metric("Off-field value", f"{result['off_field_value_cr']:.2f} cr")
    m4.metric("Total business value", f"{result['total_value_cr']:.2f} cr")
    m5.metric("ROI", f"{result['roi']:.2f}")
    m6.metric("Surplus", f"{result['surplus_cr']:+.2f} cr")

    better_than = (model["roi"] < result["roi"]).mean()
    if result["roi"] >= 1:
        st.success(f"Above the market average for the money paid. Better ROI than {better_than:.0%} of the "
                   f"{len(model)} auction purchases.")
    else:
        st.warning(f"Below the market average for the money paid. Better ROI than {better_than:.0%} of the "
                   f"{len(model)} auction purchases.")
    if price < 1:
        st.caption("For very cheap players ROI is dominated by the small price. Look at the surplus instead.")
    if row is not None:
        st.caption(f"Value stored for this purchase at the current assumptions: {row['value_cr']:.2f} cr "
                   f"(ROI {row['roi']:.2f}).")


def page_tracker():
    st.title("Auction value tracker")
    st.info(CAVEAT)
    played = model[model["played"]].sort_values("season")
    limit = float(max(model["price_cr"].max(), played["value_cr"].max()) * 1.05)

    st.subheader("Price paid vs business value created, season by season")
    st.caption("Press play. Dots above the dashed line created more value than they cost. Bubble size = matches played.")
    fig = px.scatter(played, x="price_cr", y="value_cr", animation_frame="season", animation_group="player_name",
                     color="role", size="matches_played", size_max=24, hover_name="player_name",
                     hover_data=["team", "impact", "roi"], range_x=[0, limit], range_y=[0, limit],
                     labels={"price_cr": "Price (crore)", "value_cr": "Business value (crore)"})
    fig.add_shape(type="line", x0=0, y0=0, x1=limit, y1=limit, line=dict(dash="dash"))
    st.plotly_chart(fig)

    st.subheader("Franchise efficiency race (cumulative)")
    rows = []
    for s in sorted(model["season"].unique()):
        g = model[model["season"] <= s].groupby("team")[["value_cr", "price_cr"]].sum()
        for team, r in g.iterrows():
            rows.append({"Through season": f"through {s}", "team": team, "Efficiency": r["value_cr"] / r["price_cr"]})
    race = pd.DataFrame(rows)
    frames = sorted(race["Through season"].unique())
    final_order = race[race["Through season"] == frames[-1]].sort_values("Efficiency")["team"].tolist()
    fig2 = px.bar(race, x="Efficiency", y="team", orientation="h", animation_frame="Through season",
                  category_orders={"team": final_order, "Through season": frames},
                  range_x=[0, float(race["Efficiency"].max()) * 1.1])
    fig2.add_vline(x=1.0, line_dash="dash")
    st.plotly_chart(fig2)

    st.subheader("Biggest surpluses each season")
    top = (model.sort_values("surplus_cr", ascending=False).groupby("season").head(5)
                .sort_values(["season", "surplus_cr"], ascending=[True, False]))
    st.dataframe(top[DETAIL_COLS].round(2), hide_index=True)


def page_franchise():
    st.title("Franchise dashboard")
    st.info(CAVEAT + " Scores cover auction purchases only; retained stars are excluded.")

    team_tbl = model.groupby("team").agg(
        purchases=("player_name", "count"), spend_cr=("price_cr", "sum"), value_cr=("value_cr", "sum"),
        played_pct=("played", lambda s: round(s.mean() * 100)))
    unused = model[~model["played"]].groupby("team")["price_cr"].sum().rename("unused_cr")
    team_tbl = team_tbl.join(unused).fillna({"unused_cr": 0})
    team_tbl["unused_pct"] = (team_tbl["unused_cr"] / team_tbl["spend_cr"] * 100).round(1)
    team_tbl["efficiency"] = (team_tbl["value_cr"] / team_tbl["spend_cr"]).round(2)
    team_tbl = team_tbl.sort_values("efficiency", ascending=False)

    fig = px.bar(team_tbl.reset_index(), x="team", y="efficiency", color="unused_pct",
                 title="Franchise Efficiency Score (business value / auction spend)",
                 labels={"efficiency": "Efficiency (1.0 = market average)", "unused_pct": "Unused spend %"})
    fig.add_hline(y=1.0, line_dash="dash")
    st.plotly_chart(fig)
    st.dataframe(team_tbl.round(2))

    st.subheader("Efficiency by team and season")
    ts = model.groupby(["team", "season"])[["value_cr", "price_cr"]].sum()
    ts["efficiency"] = ts["value_cr"] / ts["price_cr"]
    heat = ts["efficiency"].unstack()
    heat = heat.loc[team_tbl.index]
    fig2 = px.imshow(heat, text_auto=".2f", aspect="auto", color_continuous_scale="RdYlGn",
                     color_continuous_midpoint=1.0, labels={"x": "Season", "y": "Team", "color": "Efficiency"})
    st.plotly_chart(fig2)

    st.subheader("How much does each team depend on one purchase?")
    rows = []
    for team, g in model.groupby("team"):
        best = g.loc[g["value_cr"].idxmax()]
        rest = g.drop(g["value_cr"].idxmax())
        rows.append({"team": team, "efficiency": round(g["value_cr"].sum() / g["price_cr"].sum(), 2),
                     "top purchase": f"{best['player_name']} ({int(best['season'])})",
                     "share of team value (%)": round(best["value_cr"] / g["value_cr"].sum() * 100),
                     "efficiency without it": round(rest["value_cr"].sum() / rest["price_cr"].sum(), 2)})
    conc = pd.DataFrame(rows).set_index("team").sort_values("efficiency", ascending=False)
    conc["rank"] = conc["efficiency"].rank(ascending=False, method="min").astype(int)
    conc["rank without it"] = conc["efficiency without it"].rank(ascending=False, method="min").astype(int)
    st.dataframe(conc)
    st.caption("If the rank changes a lot without one player, the team's score rests on that one purchase.")

    st.subheader("Team drill-down")
    team = st.selectbox("Team", team_tbl.index.tolist())
    detail = model[model["team"] == team].sort_values("surplus_cr", ascending=False)
    st.dataframe(detail[DETAIL_COLS].round(2), hide_index=True)


def page_explorer():
    st.title("Player explorer")
    st.info(CAVEAT)
    c1, c2, c3, c4 = st.columns(4)
    seasons = c1.multiselect("Season", sorted(model["season"].unique()), default=sorted(model["season"].unique()))
    teams = c2.multiselect("Team", sorted(model["team"].dropna().unique()))
    roles = c3.multiselect("Role", sorted(model["role"].dropna().unique()))
    origins = c4.multiselect("Nationality", sorted(model["origin"].unique()))
    d1, d2, d3 = st.columns(3)
    max_price = float(model["price_cr"].max())
    price_range = d1.slider("Price range (crore)", 0.0, max_price, (0.0, max_price))
    min_matches = d2.slider("Minimum matches played", 0, 17, 0)
    sort_by = d3.selectbox("Sort by", ["surplus_cr", "roi", "value_cr", "impact", "price_cr", "matches_played"])
    e1, e2 = st.columns(2)
    ascending = e1.checkbox("Ascending order", value=False)
    top_n = e2.slider("Rows to show", 10, 200, 50, step=10)

    df = model[model["season"].isin(seasons)]
    if teams:
        df = df[df["team"].isin(teams)]
    if roles:
        df = df[df["role"].isin(roles)]
    if origins:
        df = df[df["origin"].isin(origins)]
    df = df[df["price_cr"].between(*price_range) & (df["matches_played"] >= min_matches)]
    df = df.sort_values(sort_by, ascending=ascending)

    st.write(f"{len(df)} purchases match. Showing the top {min(top_n, len(df))}.")
    st.dataframe(df[DETAIL_COLS + ["origin"]].head(top_n).round(2), hide_index=True)
    st.download_button("Download the filtered table (CSV)", df[DETAIL_COLS + ["origin"]].to_csv(index=False),
                       file_name="ipl_players_filtered.csv", mime="text/csv")
    st.caption("ROI is unreliable for players priced under 1 crore (tiny divisor). Sort by surplus for those.")


def page_method():
    st.title("Method and limits")
    st.info(CAVEAT)
    st.markdown(
        "**Current settings:** wicket = {v} runs, on-field share = {s}%, star bonus = {w} balls, multiple = {m}.  \n"
        "**Market-implied scale:** one run above average is worth {r:.1f} lakh at these settings "
        "(a scale, not a price).".format(v=V, s=ON_SHARE, w=STAR_W, m=MULTIPLE, r=rates["cr_per_run"] * 100))
    for title, name, expanded in [("ROI formula", "roi_formula.md", True),
                                  ("Assumptions and limitations", "assumptions.md", False),
                                  ("Insights", "insights.md", False)]:
        path = DOCS / name
        with st.expander(title, expanded=expanded):
            if path.exists():
                st.markdown(path.read_text(encoding="utf-8"))
            else:
                st.write(f"{name} not found in the docs folder.")


{"Overview": page_overview, "Player ROI calculator": page_calculator,
 "Auction value tracker": page_tracker, "Franchise dashboard": page_franchise,
 "Player explorer": page_explorer, "Method and limits": page_method}[page]()