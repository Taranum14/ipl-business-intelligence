# Data sources

Raw files are not committed (see `.gitignore`). Download them into `data/raw/` with these names.

| File | Source | Link | Downloaded on |
|---|---|---|---|
| `matches.csv`, `deliveries.csv` | Kaggle: IPL Complete Dataset (2008-2024) by patrickb1912. Data from Cricsheet. | https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020 | [date] |
| `auction_2022.csv` | Kaggle: [dataset title and author] | [link] | [date] |
| `auction_2023.csv` | Kaggle: [dataset title and author] | [link] | [date] |
| `auction_2024.csv` | Kaggle: [dataset title and author] | [link] | [date] |

## Notes
- Auction data is one file per season and the three files use different formats (see `docs/data_dictionary.md`).
- Never edit the raw files. All cleaning is done in `notebooks/02_data_cleaning.ipynb`.
- Check each dataset's licence before redistributing any raw file.