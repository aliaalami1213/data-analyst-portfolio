# E-Commerce Sales & Delivery Analysis

**Dataset:** [Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle, ~100k real anonymized orders, 2016-2018)

## Business Question
Which product categories and states drive the most revenue, and does delivery speed affect customer review scores? Where should the business focus to grow revenue and improve satisfaction?

## Approach
1. **Load & join** — this dataset is split across multiple CSVs (`orders`, `order_items`, `products`, `customers`, `order_reviews`, `sellers`); join them into one analysis table.
2. **Clean** — parse timestamps, handle missing delivery dates, translate category names (a `product_category_name_translation.csv` is provided).
3. **Revenue analysis** — monthly revenue trend, top categories by revenue, top states by order volume.
4. **Delivery vs. satisfaction** — compute delivery time (purchase → delivered) and compare against review score.
5. **Recommend** — 2-3 concrete actions (e.g. "categories X/Y are top revenue but have the slowest delivery — prioritize logistics there").

## Key Findings
_Fill in after running `analysis.ipynb` — e.g._
- Top revenue category: _____
- Top state by order volume: _____
- Correlation between delivery time and review score: _____

## Recommendations
_2-3 sentences translating the findings into business action._

## Files
- `analysis.ipynb` — full notebook
- `data/README.md` — dataset download instructions
- `images/` — exported chart PNGs referenced above
