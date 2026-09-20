# Key insights: IPL auction purchases 2022-2024

Numbers come from `notebooks/03_analysis.ipynb` (auction purchases only, 356 rows: 204 from the
2022 mega auction, 80 from 2023 and 72 from 2024). Re-check them after your final run.
Performance is measured with a rough score, runs + 20 x wickets, which Phase 5 will replace.

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
*So what:* an availability adjustment belongs in the ROI formula.

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
*Caveats:* only 28 Indian purchases in the 1-3 cr band; nationality for one player was still missing when
these numbers were taken; rough score.

## 8. Team differences are modest
Points per crore of auction spend: MI 57.9, DC 54.2, LSG 46.8, RR 44.9, PBKS 44.1, RCB 44.0, SRH 42.8,
KKR 40.6, CSK 40.4, GT 40.3. Only MI and DC stand out; ranks 3-10 are close.
PBKS had the lowest share of purchases who played (59%). SRH spent the most (134 cr) and ranks in the lower half.
*Caveat:* auction buys only. MI and DC kept their biggest names through retention, so this shows how they
spent on the rest of the squad, not their whole team. Three seasons only.

## 9. Efficiency fell in 2024
Points per crore by season: 51.5 (2022), 44.2 (2023), 31.1 (2024). Two purchases, Mitchell Starc (24.75 cr)
and Pat Cummins (20.5 cr), took 19.6% of 2024 auction spend and produced about 11.8% of its points.
*Caveat:* 2023 and 2024 were mini-auctions with small samples, so the seasons are not directly comparable.

## What Phase 5 must handle
1. A fairer performance score (strike rate, economy, role-adjusted).
2. An availability adjustment for players who do not play.
3. Price per season, for multi-year mega-auction contracts.
4. The revenue side (ticket, jersey, sponsorship proxies) with every assumption written down.