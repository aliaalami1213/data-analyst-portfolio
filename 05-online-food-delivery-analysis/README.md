# Online Food Delivery — Customer Ordering Behavior

**Dataset:** [Online Food Ordering Dataset (Kaggle)](https://www.kaggle.com/datasets/srisyra02/online-food-ordering-dataset) — 388 survey responses from customers of an online food delivery service in Bangalore, India

## Business Question
Which demographic, income, and household factors are associated with whether a customer places an online food order, and how satisfied are the customers who do?

## Approach
1. **Clean** — drop a duplicate "Output" column baked into the raw CSV, strip whitespace from `Feedback`, and check for missing/duplicate rows.
2. **Overview** — overall order rate and feedback sentiment.
3. **Segment by occupation & income** — order rate broken out by occupation and monthly income bracket.
4. **Segment by marital status & customer type** — order rate for single/married respondents and for New/Regular/Frequent customers.
5. **Segment by age & family size** — compare these between customers who did and didn't order.
6. **Classification model** — de-duplicate to unique respondents (285), then compare Logistic Regression and Random Forest against an "always predict Yes" baseline (5-fold CV) to see whether demographics can actually predict order likelihood, plus feature importances.
7. **Recommend** — translate the patterns into acquisition/retention priorities.

## Key Findings
- **77.6%** of respondents placed an order; **81.7%** gave positive feedback — the service converts and satisfies most people it reaches.
- **Students order at the highest rate (88.9%)**, ahead of house wives (77.8%), employees (64.4%), and the self-employed (63.0%) — despite students being the largest "No Income" group.
- Counterintuitively, the **"No Income" bracket has the highest order rate of any income group (87.7%)**, while "₹25,001–50,000" earners have the lowest (60.9%). This is really an occupation effect (No Income ≈ students) — income bracket alone is a weak, sometimes misleading, predictor of ordering without controlling for occupation and life stage.
- **Single respondents order at 85.4% vs. 61.1% for married respondents** — life stage looks like a stronger driver than raw income here.
- **Customer type tracks order rate as expected**: Frequent (76.7%) and Regular (78.9%) customers order at similar, higher rates than New customers (70.8%), consistent with New customers still being early in the relationship.
- Customers who did **not** order skew slightly older (mean age 26.0 vs. 24.2) and report a slightly larger family size (3.39 vs. 3.25) — real but modest gaps.
- **Data quality note:** 103 of 388 rows (26.5%) are exact duplicates. Plausible for a short categorical survey, but worth flagging before this data is used to train a predictive model, since duplicates can inflate confidence in patterns really driven by a handful of unique respondents.
- **Classification model:** on the 285 unique respondents, a Random Forest predicting `Output` from demographics ties the "always predict Yes" baseline on accuracy (77.2% vs. 76.1%) but reaches **ROC AUC 0.735** — it can rank customers by order likelihood better than chance, but demographics alone aren't a strong enough signal to reliably flip individual predictions at this sample size. **Age and family size are by far the top two predictors**, well ahead of any single occupation, income, or education category.

## Recommendations
1. Prioritize acquisition and retention on **students and single, no/low-income young adults** — the segment already converting and responding most positively — rather than assuming higher income brackets are the best-fit customer.
2. Investigate **why mid-income earners (₹25k–50k) convert least (60.9%)** — the one segment where price or product-market fit may need attention.
3. Treat **New customers (70.8% order rate)** as the group needing the most onboarding support to reach Regular/Frequent conversion levels.
4. Before modeling this data, **de-duplicate rows** and validate that the "No Income" → high-order-rate relationship isn't purely a proxy for the Student occupation group.

Full code and outputs are in [`analysis.ipynb`](./analysis.ipynb).

## Files
- `analysis.ipynb` — full notebook: cleaning → EDA → segment analysis → classification model (scikit-learn) → findings & recommendations
- `data/` — the dataset CSV (included directly, no download needed) + `data/README.md` with the source link
- `images/` — exported charts referenced above and in the notebook
