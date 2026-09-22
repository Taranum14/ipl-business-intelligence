"""Player Business ROI model.

Same formulas as notebooks/04_roi_formula.ipynb, packaged so the Streamlit app can recompute the
model live when the assumptions change.
"""
import pandas as pd

RESULT_COLS = ["bat_impact", "bowl_impact", "impact", "visibility",
               "value_on_cr", "value_off_cr", "value_cr", "roi", "surplus_cr"]


def add_impact(df, par, wicket_value, season_col="season"):
    """Batting and bowling impact in runs above an average player who used the same balls."""
    out = df.copy()
    season = out[season_col]
    rpb = season.map(par["rpb"])
    dpb = season.map(par["dpb"])
    cpb = season.map(par["cpb"])
    wpb = season.map(par["wpb"])
    out["bat_impact"] = (out["runs"] - wicket_value * out["dismissals"]
                         - out["balls_faced"] * (rpb - wicket_value * dpb))
    out["bowl_impact"] = (out["balls_bowled"] * cpb - out["runs_conceded"]
                          + wicket_value * (out["wickets"] - out["balls_bowled"] * wpb))
    out["impact"] = out["bat_impact"] + out["bowl_impact"]
    return out


def value_players(df, par, wicket_value, on_share, star_w, multiple=1.0, team_brand=None):
    """Share a pool (total price x multiple) out in proportion to impact (on-field) and screen time (off-field)."""
    base = df.drop(columns=[c for c in RESULT_COLS if c in df.columns])
    out = add_impact(base, par, wicket_value)
    out["visibility"] = out["balls_faced"] + out["balls_bowled"] + star_w * (out["sixes"] + out["wickets"])
    brand = out["team"].map(team_brand or {}).fillna(1.0)

    pool = out["price_cr"].sum() * multiple
    pool_on, pool_off = pool * on_share, pool * (1 - on_share)

    positive = out["impact"].clip(lower=0)              # below-average players create no on-field value
    cr_per_run = pool_on / positive.sum()
    weighted_vis = out["visibility"] * brand
    cr_per_vis = pool_off / weighted_vis.sum()

    out["value_on_cr"] = positive * cr_per_run
    out["value_off_cr"] = weighted_vis * cr_per_vis
    out["value_cr"] = out["value_on_cr"] + out["value_off_cr"]
    out["roi"] = out["value_cr"] / out["price_cr"]
    out["surplus_cr"] = out["value_cr"] - out["price_cr"]
    return out, {"cr_per_run": cr_per_run, "cr_per_vis_unit": cr_per_vis, "pool_cr": pool}


def business_roi(price_cr, season, par, rates, wicket_value, star_w, team=None, team_brand=None,
                 runs=0, balls_faced=0, dismissals=0, sixes=0, wickets=0, balls_bowled=0, runs_conceded=0):
    """Estimated value and ROI for one (possibly hypothetical) player-season."""
    p = par.loc[season]
    bat = runs - wicket_value * dismissals - balls_faced * (p["rpb"] - wicket_value * p["dpb"])
    bowl = balls_bowled * p["cpb"] - runs_conceded + wicket_value * (wickets - balls_bowled * p["wpb"])
    impact = bat + bowl
    visibility = balls_faced + balls_bowled + star_w * (wickets + sixes)
    on_value = max(impact, 0) * rates["cr_per_run"]
    off_value = visibility * (team_brand or {}).get(team, 1.0) * rates["cr_per_vis_unit"]
    total = on_value + off_value
    return {"impact_runs": float(impact), "on_field_value_cr": float(on_value),
            "off_field_value_cr": float(off_value), "total_value_cr": float(total),
            "roi": float(total / price_cr), "surplus_cr": float(total - price_cr)}