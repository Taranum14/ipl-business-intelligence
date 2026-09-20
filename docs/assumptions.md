# Assumptions and limitations

## A. Business metrics
1. Ticket, jersey and sponsorship revenue per player is not public.
   Revenue is estimated using proxies (team performance, popularity, social
   following). The proxies and formula are defined in Phase 5.
2. Auction prices are nominal (not adjusted for inflation) and are stored in crores.
3. A player who changed teams is counted separately for each team and season.
4. A player's price is linked to his performance in the same IPL season
   as the auction row. Fielding contributions (catches, run-outs) are not
   included in performance.
5. A player bought at a mega auction may keep the same salary across several
   seasons. How to split that price per season will be decided in Phase 5.

## B. Data coverage
6. Ball-by-ball data comes from Cricsheet via Kaggle (IPL Complete Dataset,
   patrickb1912) and covers 2008-2024 only.
7. Auction data covers 2022, 2023 and 2024 only, because no single all-season
   sold-price file was available. Each season comes from a separate Kaggle file.
8. Only players who received a price are analysed. Unsold players
   (status UNSOLD in 2023, team "Unsold" in 2024) are excluded.
9. The 2022 file appears to list auction purchases only. Retained players'
   salaries are missing (the highest price in the file is 15.25 crore).
10. The 2023 file includes retained players; their price is their retention salary.
11. The 2024 file has no nationality column. The overseas flag is filled from
    the 2022 and 2023 files where the same player appears, and is missing
    for the rest.

## C. Cleaning decisions
12. Prices were converted to crores: 2022 text values such as "₹ 4,40,00,000"
    were divided by 10,000,000; 2023 values in lakhs were divided by 100;
    2024 values were already in crores. The 2024 base price (in rupees) was
    divided by 10,000,000.
13. Source spelling errors were corrected by mapping to team codes:
    "Gujrat Titans" (GT), "Royal Challengers Banglore" (RCB) and
    "Kolkata Night Riders" (KKR).
14. Renamed franchises are merged under one code: Delhi Daredevils = DC,
    Kings XI Punjab = PBKS, Royal Challengers Bangalore and Bengaluru = RCB.
    Defunct teams keep their own codes (DCH, GL, KTK, PWI, RPS).
15. The season year is taken from the match date, because the `season` text
    has mixed formats such as "2007/08" and "2020/21".
16. Player roles were standardised to Batter, Bowler, All-Rounder and Wicketkeeper.

## D. Player name matching
17. Auction names (for example "Ajinkya Rahane") were matched to Cricsheet names
    ("AM Rahane") using, in order: exact match, surname plus first initial,
    unique last name, and fuzzy spelling. Names with more than one possible
    match were left unmatched or fixed by hand.
18. Matches were validated by checking that each matched player appeared for the
    auction team in that season. Wrong matches found this way (for example
    "Shahrukh Khan" matched to "SN Khan") were replaced by manual overrides or
    set to "no match".
19. About [X]% of auction rows could not be matched to a ball-by-ball name.
    These are mostly low-priced players or players who never played an IPL match.
    They are kept in the table with zero performance and `played = False`.
20. Some manual overrides were made from domain knowledge (for example
    "Wanindu Hasaranga" = "PWH de Silva") and were checked against the team-and-season
    validation. A small number of wrong matches may remain undetected,
    for example when the wrong player played for the same team that season.

## E. Performance statistics
21. Matches played = matches where the player appears in the ball-by-ball data
    as batter, non-striker or bowler.
22. Balls faced exclude wides. Runs conceded exclude byes and leg-byes.
    Economy uses legal balls only (no wides or no-balls).
23. Bowler wickets exclude run-outs and other non-bowler dismissals.
24. Player-season statistics were checked against known results
    (top run-scorers and wicket-takers for 2022-2024) [add what you found].