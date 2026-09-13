# Data

This project uses the classic **California Housing Prices** dataset — 20,640 California district-level observations derived from the 1990 U.S. Census (the same dataset popularized by Aurélien Géron's *Hands-On Machine Learning*; also available on Kaggle as ["California Housing Prices"](https://www.kaggle.com/datasets/camnugent/california-housing-prices)).

`analysis.ipynb` fetches the CSV at runtime directly from a Google Drive link (see the second cell), rather than reading a local file in this folder. If that link ever stops working, download `housing.csv` from the Kaggle link above and point the notebook's `pd.read_csv(...)` call at it instead — the column names match exactly (`longitude`, `latitude`, `housing_median_age`, `total_rooms`, `total_bedrooms`, `population`, `households`, `median_income`, `median_house_value`, `ocean_proximity`).
