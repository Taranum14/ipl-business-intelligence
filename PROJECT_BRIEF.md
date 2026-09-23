# Project brief

## 1. Main question
Was this IPL player worth the auction price paid by the franchise?

## 2. Sub-questions and where they are answered
| Question | Status | Where |
|---|---|---|
| Which players gave the best value for money? | Answered | insights 4, 5, 12, 13 |
| Which teams spend their money most efficiently? | Answered, with caveats | insights 8, 15, 16 |
| Do overseas players give better or worse value than Indian players? | Answered | insight 7 |
| Does a higher price mean better performance? | Answered | insights 1, 2, 3 |

## 3. Deliverables
| Deliverable | Status |
|---|---|
| Cleaned dataset (`data/processed/player_season_master.csv`) | Done |
| Player Business ROI formula (`docs/roi_formula.md`, `notebooks/04_roi_formula.ipynb`) | Done |
| Franchise Efficiency Score | Done |
| Assumptions log and data dictionary | Done |
| Streamlit app: ROI calculator, animated value tracker, franchise dashboard | Next (Phase 5B) |
| README with screenshots, Medium article, deployment | Later (Phase 7) |

## 4. Out of scope (for now)
Sentiment analysis, partnership network graph, win-probability model and the auction strategy simulator.
They are added only after the core app is finished.

## 5. Success criteria
- App is live online.
- README explains the formula and its assumptions.
- I can explain the project in 2 minutes, including what the ROI is and is not.

## 6. The two-minute explanation
"IPL teams pay up to 25 crore for a player, but revenue per player is not public. So I modelled business value:
I measured each player's impact as runs above an average player, converted it into estimated on-field and
off-field value, and compared it with the price paid. ROI 1.0 means the market average. The main results:
a few purchases carry most of the value, cheap discoveries beat big signings, and team rankings are fragile.
I tested the assumptions and stated every limit."