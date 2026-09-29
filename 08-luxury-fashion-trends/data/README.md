# Data

This project uses the **Net-a-Porter/Mr Porter Fashion Dataset**, from Kaggle: https://www.kaggle.com/datasets/justinpakzad/net-a-portermr-porter-fashion-dataset

Two files are included in this folder (so `analysis.ipynb` runs as-is — no download needed):
- `net-a-porter.csv` — 23,161 women's luxury listings
- `mr-porter.csv` — 20,347 men's luxury listings

Each row has `brand`, `description`, `price_usd`, and `type` (clothing/shoes/bags/accessories/sport/watches). The notebook combines both files and tags each row with a `gender` column.
