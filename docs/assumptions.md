# Assumptions and limitations

## A. Business metrics
1. Ticket, jersey and sponsorship revenue per player is not public. Business value is therefore modelled
   from performance data plus explicit assumptions (see section G and `docs/roi_formula.md`).
2. Auction prices are nominal (not adjusted for inflation) and are stored in crores.
3. A player who changed teams is counted separately for each team and season.
4. A player's price is linked to his performance in the same IPL season as the auction row.
   Fielding contributions (catches, run-outs) are not included in performance.
5. A player bought at a mega auction may keep the same salary across several seasons. Those later
   seasons are missing from the auction files, and the current model does not add them.

## B. Data coverage
6. Ball-by-ball data comes from Cricsheet via Kaggle (IPL Complete Dataset, patrickb1912) and covers 2008-2024 only.
7. Auction data covers 2022, 2023 and 2024 only, because no single all-season sold-price file was available.
   Each season comes from a separate Kaggle file.
8. Only players who received a price are analysed. Unsold players (status UNSOLD in 2023, team "Unsold" in 2024)
   are excluded.
9. The 2022 file lists auction purchases only. Retained players' salaries are missing (the highest price in
   the file is 15.25 crore).
10. The 2023 file includes retained players (158 rows) with their retention salary.
11. The 2024 file has no nationality column. The overseas flag was filled from the 2022 and 2023 files where
    the same player appears, then by hand from public knowledge for the remaining players.

## C. Cleaning decisions
12. Prices were converted to crores: 2022 text values such as "₹ 4,40,00,000" were divided by 10,000,000;
    2023 values in lakhs were divided by 100; 2024 values were already in crores. The 2024 base price
    (in rupees) was divided by 10,000,000.
13. Source spelling errors were mapped to team codes: "Gujrat Titans" (GT), "Royal Challengers Banglore" (RCB)
    and "Kolkata Night Riders" (KKR).
14. Renamed franchises are merged under one code: Delhi Daredevils = DC, Kings XI Punjab = PBKS,
    Royal Challengers Bangalore and Bengaluru = RCB. Defunct teams keep their own codes (DCH, GL, KTK, PWI, RPS).
15. The season year is taken from the match date, because the `season` text has mixed formats such as
    "2007/08" and "2020/21".
16. Player roles were standardised to Batter, Bowler, All-Rounder and Wicketkeeper.

## D. Player name matching
17. Auction names (for example "Ajinkya Rahane") were matched to Cricsheet names ("AM Rahane") using, in order:
    exact match, surname plus first initial, unique last name, and fuzzy spelling. Names with more than one
    possible match were left unmatched or fixed by hand.
18. Matches were validated by checking that each matched player appeared for the auction team in that season.
    Wrong matches found this way (for example "Shahrukh Khan" matched to "SN Khan") were replaced by manual
    overrides or set to "no match".
19. About [X]% of auction rows could not be matched to a ball-by-ball name (see the "Share of auction rows
    with no name match" line in cleaning Cell 10). These are mostly low-priced players or players who never
    played an IPL match. They are kept with zero performance and `played = False`.
20. Some manual overrides came from domain knowledge (for example "Wanindu Hasaranga" = "PWH de Silva") and
    were checked with the team-and-season validation. A wrong match can still go undetected if the wrong
    player played for the same team that season.

## E. Performance statistics
21. Matches played = matches where the player appears in the ball-by-ball data as batter, non-striker or bowler.
22. Balls faced exclude wides. Runs conceded exclude byes and leg-byes. Economy uses legal balls only.
23. Bowler wickets exclude run-outs and other non-bowler dismissals.
24. Player-season statistics were checked against known results: the top run-scorers (Buttler 863 in 2022,
    Gill 890 in 2023, Kohli 741 in 2024) and the 2024 leading wicket-takers (Harshal Patel 24,
    Varun Chakaravarthy 21, Bumrah 20) match.

## F. Analysis (Phase 4)
25. The exploratory performance score is runs + 20 x wickets. It ignores strike rate, economy, fielding and
    captaincy, and it favours all-rounders and wicketkeepers. The Phase 5 impact score replaces it.
26. The analysis uses auction purchases only (acquisition = "sold"), so 2022, 2023 and 2024 are comparable.
    The 158 retained players in the 2023 file are excluded. Set `AUCTION_ONLY = False` to include them.
27. A "regular" is a player with 5 or more matches; value rankings use regulars only. Best-value lists also
    require a price of 1 crore or more, because 20-lakh players always look cheap.
28. Points per crore is total points divided by total spend for a group, not an average of ratios.
29. Price bands include their upper value, for example (6, 10] and (10, 100]. "Over 10 cr" (18 purchases)
    therefore differs from "10 crore or more" (22 purchases) by the players priced at exactly 10.00.
30. `played = False` means no appearance was found in the ball-by-ball data. It covers injuries, bench players
    and players whose names could not be matched (for example Dilshan Madushanka and Robin Minz).
31. Team totals cover auction purchases only, not whole squads. Retained and traded players are missing.
32. Correlations are Spearman rank correlations on players who played, so purchases who never played are excluded.

## G. ROI model (Phase 5)
33. Business value is modelled, not measured. The model shares out a pool equal to total auction spend
    x VALUE_MULTIPLE (default 1.0) in proportion to each purchase's estimated contribution, so an ROI
    of 1.0 means "the market average for the money paid". It is a value-for-money index, not rupee revenue.
    The implied crore per run above average is a scale, not a price.
34. One wicket is worth V = 20 runs (a bowler gains it, a batter loses it when dismissed). Tested at 10 and 30.
35. 70% of business value is treated as on-field and 30% as off-field brand value. Tested at 50% and 90%.
36. Off-field value is proportional to screen time (balls faced + balls bowled) plus a bonus of 10 balls for
    each six or wicket. Team brand weights default to 1.0 for every team (no data). Social-media following,
    ticket sales and merchandise are not used.
37. A player with impact of 0 or less has zero on-field value (never negative). Salary paid to players who did
    not play counts in spend, so unavailability lowers efficiency.
38. Impact excludes fielding, wicketkeeping and captaincy, so wicketkeepers and captains are under-valued.
39. League averages are computed from all players of each season, so batting and bowling impact each sum
    to zero across the league.
40. Availability = matches played / the team's matches that season. It is reported, not multiplied in,
    because value only accrues in matches played.
41. ROI compares purchases with each other within the 2022-2024 auction set. It is not comparable with
    ROI from other datasets or seasons.
42. Team efficiency scores cover auction purchases only. Retained players (for example KKR's Narine and
    Russell) are excluded, and each score depends heavily on a few players. Rankings also change with
    the definition of the performance score (Phase 4 and Phase 5 rank teams differently).
43. `avg_availability` is averaged over all purchases, including players who never played (availability 0).