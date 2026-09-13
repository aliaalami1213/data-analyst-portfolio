# E-Commerce Customer Segmentation, Churn & CLV Prediction

**Dataset:** [E-Commerce Customer Segmentation Dataset 2026 (Kaggle)](https://www.kaggle.com/datasets/datascikhan/e-commerce-customer-segmentation-2026) — 50,000 customers, 53 features (demographics, purchase behavior, engagement, RFM, CLV, churn risk)

## Business Question
Which customers are most valuable, which are at risk of churning, and how should marketing prioritize retention spend across them? This project builds an end-to-end pipeline — unsupervised segmentation, churn prediction, CLV prediction, and a marketing targeting model — to answer that.

## Approach
1. **Clean & explore** — check for missing/duplicate data, and correlate every raw behavioral feature against churn and CLV *before* modeling anything (this shapes every decision below).
2. **K-Means clustering** — segment customers from scratch on 11 raw behavioral/engagement features (elbow method + silhouette score to pick k, PCA to visualize), independent of the dataset's own pre-built segments.
3. **Churn prediction** — a Random Forest classifier, deliberately trained two ways: with recency features (production-realistic) and without them (an "early-warning" ablation, to test whether satisfaction/engagement/spend alone predict churn).
4. **CLV prediction** — a regression model, likewise trained with full purchase history and in a "cold-start" version (demographics only, simulating a brand-new customer).
5. **Marketing targeting model** — cross out-of-fold predicted churn risk × predicted CLV into a 2×2 targeting matrix with a distinct recommended action per quadrant.

## Key Findings
- **30.7%** of customers are churned (no purchase in 60+ days).
- Almost every "soft" signal — satisfaction, complaints, returns, email/click engagement, demographics — has **near-zero correlation** with churn or CLV. The two strong relationships in the data are structural: recency → churn label (r = 0.81) and total spend → CLV (r = 0.97).
- **K-Means (k=4)** finds four behavioral personas — *Dormant/Lapsed*, *Young & Email-Engaged*, *Young & Low-Engagement*, and *Senior & High-Converting* — that cut across the dataset's own value tiers rather than reproducing them (silhouette ≈ 0.07, i.e. modest separation, consistent with the weak correlations above).
- **Churn model:** AUC ≈ 1.00 with recency features, but only **AUC 0.489 (random)** once recency is removed — satisfaction, complaints, and engagement carry no independent early-warning signal in this data.
- **CLV model:** R² ≈ 0.93 using purchase history (dominated by total spend), but **R² ≈ 0** in a cold-start scenario using demographics alone — new-customer value can't be estimated from demographics here.
- **Targeting matrix:** splitting customers by predicted value × predicted risk isolates a **$98k-avg-CLV "VIP Win-Back" group** (12,352 customers, 62% already churned) from an **$18k-avg-CLV group** warranting only low-cost automated win-back — a ~5.5× value gap that should drive retention budget allocation.

## Recommendations
1. Monitor churn with simple **recency/RFM thresholds** (e.g. 30/60-day inactivity alerts) rather than a complex ML model — the added complexity buys nothing on this kind of data.
2. Route retention **spend** by predicted CLV: human-touch win-back for the high-value/high-risk quadrant, automated flows for the low-value/high-risk quadrant.
3. Don't score new-customer value from demographics alone; invest in capturing early behavioral signals (first-order size, first 30-day engagement) instead.
4. Use the four behavioral personas to tailor **channel and message** (e.g. email-first for the "Young & Email-Engaged" segment), not offer size.

Full methodology, code, and honest discussion of what each model does and doesn't show is in [`analysis.ipynb`](./analysis.ipynb).

## Files
- `analysis.ipynb` — full notebook: EDA → clustering → churn model → CLV model → targeting model → recommendations
- `data/` — the dataset CSV (included directly, no download needed) + `data/README.md` with the source link
- `images/` — exported charts referenced above and in the notebook
