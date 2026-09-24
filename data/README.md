# IPL Franchise Business Intelligence Platform

Connecting on-field performance to off-field business value: **was this IPL player worth the auction price?**

## Status
Phases 1-5A complete: data collection and cleaning, player-name matching, exploratory analysis and the
Player Business ROI model. Next: a Streamlit app with an ROI calculator, an animated value tracker and a
franchise dashboard.

## Headline findings (IPL auctions 2022-2024, 356 auction purchases)
- Price only moderately predicts performance (rank correlation 0.52), and returns per crore fall sharply:
  over-10-crore players cost about 37x the cheapest band per player for about 6x the points.
- A few purchases carry the returns: the top 10% create 63% of business value; the typical purchase who played
  returned about two thirds of its price.
- The best surpluses came from cheap discoveries (Mohit Sharma, Mohsin Khan, Tristan Stubbs, Shashank Singh).
- 32% of purchases never played, taking 12.3% of spend.
- Indian purchases returned more points per crore than overseas purchases in every price band.
- Team rankings are fragile: DC (best) and KKR (worst) hold up, the middle of the table does not.

Full list with numbers and caveats: [`docs/insights.md`](docs/insights.md).

## Method in brief
1. **Data:** ball-by-ball data (Cricsheet via Kaggle, 2008-2024) and auction prices for 2022, 2023 and 2024.
2. **Cleaning:** unified three differently formatted auction files, fixed team-name typos, converted prices to
   crores, and matched auction names to ball-by-ball names (validated by checking each matched player played
   for the auction team that season).
3. **Impact score:** runs above an average player who used the same balls, with a value for each wicket.
   Batting and bowling impact each sum to zero across the league (checked every season).
4. **Business value and ROI:** a pool equal to total auction spend is shared out in proportion to impact
   (on-field) and screen time (off-field). ROI 1.0 means the market average for the money paid.
5. **Validation:** sanity checks against known top performers, a sensitivity analysis of the assumptions and a
   "without the top player" check on team scores.

Revenue per player is not public, so business value is **modelled, not measured**. Formula and parameters:
[`docs/roi_formula.md`](docs/roi_formula.md). Every assumption: [`docs/assumptions.md`](docs/assumptions.md).

## Repository structure
```
data/raw/          original downloads (not committed)
data/interim/      partly cleaned files (not committed)
data/processed/    final tables used by the analysis and the app
notebooks/         01 exploration, 02 cleaning, 03 analysis, 04 ROI formula
docs/              assumptions, data dictionary, ROI formula, insights
```

## How to reproduce
1. Download the data listed in [`data/README.md`](data/README.md) into `data/raw/`.
2. Create a virtual environment and install the requirements:
   ```
   pip install -r requirements.txt
   pip install nbformat
   ```
3. Run the notebooks in order: `02_data_cleaning.ipynb`, `03_analysis.ipynb`, `04_roi_formula.ipynb`.
   (`01_data_exploration.ipynb` is optional and shows the raw-data checks.)

## Limitations
- Only three auction seasons; 2022 is 57% of the data.
- Retained and carried-over contracts are missing, so team totals are not whole squads.
- Fielding, wicketkeeping and captaincy are not measured.
- Off-field value is a proxy (screen time and star moments), not social-media or ticket data.
- The 20-run wicket and the 70/30 on-field split are assumptions, tested but not estimated.

## Tech stack
Python, pandas, Plotly, Jupyter. Streamlit planned for the app.

## Data and licence note
Raw data comes from Kaggle datasets and Cricsheet. Check each dataset's licence before redistributing it.
Raw data is not included in this repository.