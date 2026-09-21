# Key insights: IPL auction purchases 2022-2024

Data: 356 auction purchases (204 from the 2022 mega auction, 80 from 2023, 72 from 2024), matched to
ball-by-ball performance. Part A comes from `notebooks/03_analysis.ipynb`, Part B from
`notebooks/04_roi_formula.ipynb`. Re-check every number after re-running.

# Part A: Exploration (Phase 4)
Performance in Part A is a rough score: runs + 20 x wickets.

## 1. Price predicts performance only moderately
The rank correlation between price and points is 0.52 overall (0.63 in 2022, 0.43 in 2023, 0.30 in 2024).
The scatter is wide: some 10+ crore players scored under 50 points while some 2-crore players scored 400+.
*Caveat:* expensive players also play more games (94% of purchases over 10 crore played, against 55% of
those up to 1 crore), and 2023-24 samples are small (51 and 46 players who played).

## 2. Returns diminish sharply with price
| Price band | Avg price (cr) | Avg points per player | Points per crore |
|---|---|---|---|
| up to 1 cr | 0.39 | 58 | 149 |
| 1-3 cr | 1.92 | 116 | 60 |
| 3-6 cr | 4.61 | 175 | 38 |
| 6-10 cr | 7.87 | 279 | 36 |
| over 10 cr | 14.4 | 355 | 25 |

The over-10-crore band costs about 37x the up-to-1-crore band per player and produces about 6x the points.
*Caveat:* most of the cheapest purchases are bench players (median 1.5 points), so their high points per
crore comes from a few who played a lot.

## 3. A few stars absorb the budget
The median purchase is 0.85 crore, but the 22 purchases of 10 crore or more (6.2% of all) took 31.6% of
total spend. (The band table counts 18 players "over 10 cr" because prices of exactly 10.00 fall in the 6-10 band.)

## 4. Best-value buys cost 1-3 crore
Among players with 5+ matches bought for 1 crore or more, the best points per crore came from Devon Conway
(1.0 cr, 252 runs), Kuldeep Yadav (2.0 cr, 21 wickets), Tilak Varma (1.7 cr, 397 runs), Tim Southee,
Umesh Yadav, Wriddhiman Saha and David Miller (3.0 cr, 481 runs).
*Caveat:* 13 of the top 15 are from 2022, which is 57% of the data.

## 5. Suspected poor value
Sameer Rizvi (8.4 cr, 51 runs in 5 matches), Spencer Johnson (10 cr, 4 wickets in 5 matches),
Shahrukh Khan (2022, 9 cr) and Rovman Powell (7.4 cr) returned the least per crore among players bought for
5 crore or more.
*Caveat:* the score ignores strike rate, economy and captaincy, so it under-rates finishers such as
Rahul Tewatia and Pat Cummins. Treat these as suspects, not verdicts.

## 6. Availability is a hidden cost
114 of 356 purchases (32%) never played that season, but they took only 116.5 crore (12.3% of spend).
The unused share rose from 10.0% in 2022 to 14.1% in 2023 and 16.5% in 2024 (small samples).
The three biggest 2022 non-players, Deepak Chahar (14 cr), Jofra Archer (8 cr) and Mark Wood (7.5 cr),
account for 29.5 of that year's 55.1 unused crore. [Verify the injury reports before publishing.]

## 7. Indian purchases returned more per crore than overseas purchases in every price band
| Band | Indian points per crore | Overseas points per crore |
|---|---|---|
| up to 1 cr | 172.0 | 110.1 |
| 1-3 cr | 64.1 | 57.7 |
| over 3 cr | 36.1 | 29.0 |

Overall, overseas players cost about 4x more at the median (2.0 vs 0.5 cr), play more often (75% vs 65%)
and score more per player (median 118 vs 25), but return fewer points per crore (37.5 vs 53.5).
In the over-3-crore band overseas players produced about the same points per player (254 vs 252) but cost
about 25% more (8.7 vs 7.0 cr). Mid-priced overseas players (1-3 cr) played less often (69% vs 86%), which
is consistent with the four-overseas-player limit in the playing XI.
*Caveats:* only 28 Indian purchases in the 1-3 cr band; one player's nationality was still missing when
these numbers were taken; rough score.

## 8. Team differences are modest (Part A score)
Points per crore of auction spend: MI 57.9, DC 54.2, LSG 46.8, RR 44.9, PBKS 44.1, RCB 44.0, SRH 42.8,
KKR 40.6, CSK 40.4, GT 40.3. Only MI and DC stand out; ranks 3-10 are close.
*Caveat:* auction buys only. MI and DC kept their biggest names through retention, so this shows how they
spent on the rest of the squad, not their whole team.

## 9. Efficiency fell in 2024
Points per crore by season: 51.5 (2022), 44.2 (2023), 31.1 (2024). Two purchases, Mitchell Starc (24.75 cr)
and Pat Cummins (20.5 cr), took 19.6% of 2024 auction spend and produced about 11.8% of its points.
*Caveat:* 2023 and 2024 were mini-auctions with small samples, so the seasons are not directly comparable.

# Part B: Business ROI model (Phase 5)
Performance in Part B is *impact*: runs above an average player who used the same balls (formula in
`docs/roi_formula.md`). ROI 1.0 means "returned the market average for the money paid". It is a
value-for-money index relative to this auction data, not rupee revenue.

## 10. The model passes its sanity checks
Batting and bowling impact each sum to zero across the league in every season. The top five by impact are
familiar names: 2022 Buttler (863 runs), KL Rahul, David Miller, Andre Russell and Hardik Pandya; 2023 Shubman
Gill (890), Mohit Sharma (27 wickets), du Plessis, Conway and Kohli; 2024 Kohli (741), Narine, Bumrah, Pooran
and Russell.

## 11. Value is concentrated in a few purchases
Only 28% of purchases returned more than they cost. 269 of 356 created no on-field value: 114 never played and
roughly 155 played below average. In the value-versus-price chart most purchases sit below the value = price line
and a few sit far above it. [Add the concentration result: top 10% of purchases create X% of all value.]

## 12. The biggest surpluses were cheap discoveries
By surplus (value minus price): Mohit Sharma (GT 2023, 0.5 cr), David Miller (GT 2022, 3.0 cr), Tristan Stubbs
(DC 2024, 0.5 cr), Mohsin Khan (LSG 2022, 0.2 cr), Heinrich Klaasen (SRH 2023, 5.25 cr), Kuldeep Yadav
(DC 2022, 2.0 cr), David Warner (DC 2022, 6.25 cr) and Shashank Singh (PBKS 2024, 0.2 cr).
Among players bought for 1 crore or more with 5+ matches, the highest ROI came from Devon Conway (11.5),
David Miller (10.9), Kuldeep Yadav (9.7), Tilak Varma (7.4) and Aiden Markram (6.3).
*Caveat:* ROI for 20-lakh players is arithmetic (for example 107 for Mohsin Khan), so rank cheap players by
surplus, not ROI.

## 13. Suspected shortfalls
Spencer Johnson (GT 2024, 10 cr, ROI 0.07), Sameer Rizvi (CSK 2024, 8.4 cr, ROI 0.04), Daryl Mitchell
(CSK 2024, 14 cr, ROI 0.13), Cameron Green (MI 2023, 17.5 cr, ROI 0.49) and Nicholas Pooran (LSG 2023, 16 cr,
ROI 0.48).
*Caveats:* fielding, wicketkeeping and captaincy are not measured; a player who missed games through injury
looks like a shortfall; the loss for any purchase is capped at its price.

## 14. Player-level conclusions survive different assumptions
Across five alternative settings (wicket worth 10 or 30 runs, on-field share 50% or 90%, no star bonus) the ROI
rank correlation with the baseline stayed at 0.98-0.99, and 12-15 of the top 15 surplus purchases stayed the same.

## 15. Franchise efficiency (auction purchases only)
Franchise Efficiency Score (business value / auction spend): DC 1.43, GT 1.18, MI 1.16, LSG 1.16, RCB 1.12,
SRH 0.98, PBKS 0.89, RR 0.84, CSK 0.76, KKR 0.56. DC was best and KKR worst in all six scenarios (team rank
correlation 0.91-1.00).
*Caveats:* retained stars are excluded (KKR's Narine and Russell were retained, and KKR won the 2024 title);
one purchase can drive a team's score (Mohit Sharma alone created about 35% of GT's value).
[Add the result of the "with and without top player" check.]

## 16. Team rankings depend on the scoring method
GT was last in Part A (40.3 points per crore) and second in Part B (1.18); MI fell from first to third and KKR
from eighth to last. The same purchases give different team rankings under different scores, so present team
results as "auction efficiency under this model", not as a verdict.

## 17. Unused spend differs a lot between teams
Share of auction spend that went to players who never played: GT 22%, LSG 21%, CSK 20%, MI 18%, KKR 14%,
RCB 11%, DC 8%, PBKS 7%, SRH 4%, RR 3%.

# Limitations (all parts)
- Only 3 auction seasons; 2022 is 57% of the data and 2023-24 are small mini-auctions.
- Retained and carried-over contracts are missing, so team totals are not whole squads.
- Fielding, wicketkeeping and captaincy are not measured.
- Off-field value is a proxy (screen time and star moments), not social-media or ticket data.
- The 20-run wicket and the 70/30 split are assumptions, tested but not estimated.
- One player's nationality was still missing when the nationality numbers were taken; re-check after the fix.

# To fill in before publishing
1. Insight 11: top-10% concentration result.
2. Insight 15: the "with and without top player" team check.
3. Insight 6: verify the 2022 injury reports (Chahar, Archer, Wood).
4. Re-check Part A nationality numbers after the last nationality fix.