# Player Business ROI: formula and assumptions

## What it is (and is not)
Revenue per player is not public, so this project does **not measure** revenue. It **models** the business
value each auction purchase created, using only public performance data plus explicit assumptions.
The model shares out a pool of value equal to total auction spend, in proportion to what each player
produced. So an ROI of 1.0 means "returned the market average for the money paid"; 2.0 means twice
the average. ROI is a *value-for-money index relative to this market*. It becomes a rupee-revenue
estimate only if `VALUE_MULTIPLE` is set from an external revenue estimate.

## Step 1: Impact score (runs above an average player)
Compared with the league average of the same season, using the same number of balls:

    par_rpb = league runs per ball faced          par_dpb = league dismissals per ball faced
    par_cpb = league runs conceded per legal ball par_wpb = league bowler wickets per legal ball
    V       = runs one wicket is worth (default 20)

    Batting impact = runs - V x dismissals - balls_faced x (par_rpb - V x par_dpb)
    Bowling impact = balls_bowled x par_cpb - runs_conceded + V x (wickets - balls_bowled x par_wpb)
    Impact         = Batting impact + Bowling impact

Both parts sum to zero across the whole league, so 0 means exactly average.

Illustrative example (made-up league averages): par_rpb = 1.30, par_dpb = 0.05, V = 20. A batter with
450 runs off 300 balls, out 12 times: 450 - 20x12 - 300 x (1.30 - 20x0.05) = 450 - 240 - 90 = **+120 runs**
above an average batter who faced the same 300 balls.

## Step 2: Business value
    Pool          = sum of all prices x VALUE_MULTIPLE
    On-field pool = Pool x ON_SHARE            Off-field pool = Pool x (1 - ON_SHARE)

    On-field value  = max(Impact, 0) x  On-field pool / sum of max(Impact, 0)
    Visibility      = balls_faced + balls_bowled + STAR_W x (sixes + wickets)
    Off-field value = Visibility x team_brand x Off-field pool / sum of (Visibility x team_brand)

    Business value = On-field value + Off-field value

## Step 3: Outputs
    Player Business ROI = Business value / Price
    Surplus (crore)     = Business value - Price
    Franchise Efficiency Score = sum of Business value / sum of Price   (per team, optionally per season)

Salary paid to players who did not play stays in the price total, so unavailability lowers a
franchise's score. Availability (matches played / team matches) is reported but not multiplied in,
because value only accrues when a player plays.

## Parameters
| Parameter | Default | Meaning | Tested in sensitivity |
|---|---|---|---|
| V | 20 | runs one wicket is worth | 10 and 30 |
| ON_SHARE | 0.70 | share of value created on the field | 0.50 and 0.90 |
| STAR_W | 10 | extra balls of screen time per six or wicket | 0 |
| VALUE_MULTIPLE | 1.0 | business value per rupee of salary at the market average | none (scales all values equally) |
| TEAM_BRAND | none | optional fan-base weights per team | fill from public follower counts |

## Limitations
1. Fielding, wicketkeeping and captaincy are not measured, so keepers and leaders are under-valued.
2. The brand side uses screen time and star moments as proxies. Social-media following, ticket and
   merchandise data are not used because they are not available per player.
3. ON_SHARE and V are assumptions, not estimates. Cell 8 of the notebook tests how much the
   conclusions depend on them, and Cell 11 tests how much depends on a few players. Report only
   conclusions that survive both.
4. Only 2022-2024 auction purchases are covered. Retained and carried-over contracts are missing.
5. A player with impact of 0 or less gets no on-field value, which treats poor performance as
   wasted money but does not model damage to results.
6. Team scores are dominated by a few purchases. Removing a team's single most valuable purchase changes
   several ranks (for example GT falls from 2nd to 6th), so treat team rankings as method-dependent.