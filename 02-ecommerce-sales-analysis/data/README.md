# Data

This project uses the **Olist Brazilian E-Commerce Public Dataset**.

1. Download it from Kaggle: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
   (free Kaggle account required — click "Download")
2. Unzip all CSVs directly into this `data/` folder. You should end up with files like:
   - `olist_orders_dataset.csv`
   - `olist_order_items_dataset.csv`
   - `olist_products_dataset.csv`
   - `olist_customers_dataset.csv`
   - `olist_order_reviews_dataset.csv`
   - `olist_sellers_dataset.csv`
   - `product_category_name_translation.csv`
3. The notebook reads all of these from `data/`.

Raw data isn't committed to the repo (kept out via `.gitignore`) — this keeps the repo small and respects Kaggle's dataset terms.
