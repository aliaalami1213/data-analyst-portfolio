# Luxury Fashion Market & Trend Analysis (Net-a-Porter / Mr Porter)

**Dataset:** [Net-a-Porter/Mr Porter Fashion Dataset (Kaggle)](https://www.kaggle.com/datasets/justinpakzad/net-a-portermr-porter-fashion-dataset) — 43,508 product listings scraped from two elite luxury retailers (Net-a-Porter, women's; Mr Porter, men's), 807 brands, with brand/description/price/category

## Business Question
How is the luxury fashion market structured by category, brand, and gender — and what does the language of product descriptions reveal about which items command a price premium? Framed as market-intelligence and pricing analysis for a fashion company's merchandising, buying, or trend-forecasting team.

## Approach
1. **Clean & combine** — merge the women's and men's listings with a `gender` tag, check for missing/duplicate data.
2. **Price architecture** — price distribution by category and gender.
3. **Brand positioning map** — plot assortment depth (listing count) vs. median price for the top 25 brands by volume, the classic buying-team chart for portfolio balance.
4. **Price tiering** — quartile-based price tiers and how category mix shifts across them.
5. **Trend mining** — keyword search over descriptions for materials, style signals, and sustainability language; test each against price to surface real trend patterns (e.g. "quiet luxury").
6. **Classification model** — a TF-IDF + Logistic Regression model predicting whether an item is priced in the **top quartile within its own category** (so a $2,000 coat and a $2,000 bag are both "premium," not just "it's an expensive category"), evaluated by ROC/AUC.
7. **Model interpretation** — extract the actual words that push predictions toward "premium" vs. "accessible."

## Key Findings
- **Category sets the price ceiling**: watches ($4,663 median) and bags ($1,850) anchor the top; clothing ($595), accessories ($450), and sport ($160) are volume/traffic categories.
- **Brand positioning spans a huge range even among the best-stocked labels** — median price runs from $36 (SKIMS) to $2,130 (Alaïa) among the top 25 brands by volume, confirming these platforms deliberately carry accessible-luxury and ultra-luxury side by side.
- **"Quiet luxury" shows up in the data, not just in press coverage**: logo/monogram-mentioning items are *cheaper* on average ($450 vs. $627), while cashmere-mentioning items are markedly *more expensive* ($1,050 vs. $590) — visible branding and fine materials pull price in opposite directions.
- **Sustainability language ("sustain," "recycled," "organic") is associated with lower, not higher, prices** ($425 vs. $625 median) — sustainable positioning hasn't translated into a price premium in this market snapshot.
- **Description language alone predicts premium-for-category pricing with AUC 0.861** (vs. a 74.8% no-signal baseline), and the words driving it match real merchandising intuition: structured outerwear/eveningwear and fine materials ("gown," "coat," "cashmere," "silk," "shearling") signal premium; basics, intimates, and activewear ("socks," "beanie," "swimsuit," "bra," "dri fit") signal accessible.

## Recommendations
1. Use the **category price architecture** to set assortment and margin targets — bags/watches as margin anchors, clothing/accessories as traffic drivers.
2. Don't assume **logomania or sustainability messaging are automatic premium-pricing levers** — neither commands a premium in this market snapshot; a brand wanting to charge more for either would be pricing against the current market pattern.
3. Lean into **cashmere and structured outerwear/eveningwear language** in premium product copy — the one material and category signal that reliably tracks with higher pricing here.
4. Treat the **premium-language classifier as a lightweight copy-audit tool** — any new product description can be scored against historically premium vs. accessible language, useful for a merchandising or copywriting team standardizing tone across price tiers.

Full code and outputs are in [`analysis.ipynb`](./analysis.ipynb).

## Files
- `analysis.ipynb` — full notebook: cleaning → price architecture → brand positioning map → price tiering → trend/keyword mining → TF-IDF classification (scikit-learn) → model interpretation → findings & recommendations
- `data/` — both dataset CSVs (included directly, no download needed) + `data/README.md` with the source link
- `images/` — exported charts referenced above and in the notebook
