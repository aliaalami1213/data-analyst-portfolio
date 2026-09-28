# Red Wine Quality — What Makes a Wine "Good"?

**Dataset:** [Red Wine Quality (Cortez et al., 2009) — Kaggle/UCI](https://www.kaggle.com/datasets/uciml/red-wine-quality-cortez-et-al-2009) — 1,599 Portuguese "Vinho Verde" red wines, 11 physicochemical inputs, 0–10 expert quality score

## Business Question
Which physicochemical properties distinguish a high-quality ("good") red wine from the rest, and how accurately can we predict it — practically enough to be useful for a winery's quality control?

## Approach
1. **Clean & explore** — check for missing/duplicate data, and look at the quality score distribution and its imbalance.
2. **Correlation analysis** — which of the 11 chemical features actually relate to quality.
3. **Segment by outcome** — compare good vs. other wines on the top correlated features.
4. **Classification framing** — per the dataset's own suggested approach: binarize quality at ≥7 = "good," drop the raw score to prevent leakage, de-duplicate before splitting.
5. **Model comparison** — Logistic Regression vs. a hyperparameter-tuned Decision Tree (via `GridSearchCV`, as the dataset tips suggest) vs. Random Forest, evaluated by ROC/AUC given the class imbalance.
6. **Feature importance & error analysis** — what drives the prediction, and where the best model gets it wrong.

## Key Findings
- Only **13.6%** of wines are rated "good" (quality ≥ 7) — a genuinely imbalanced target, so AUC and recall matter more than raw accuracy here.
- **Alcohol content (+0.48 correlation) and volatile acidity (-0.39) are the strongest chemical predictors of quality**, followed by sulphates (+0.25) and citric acid (+0.23) — consistent with basic wine chemistry (volatile acidity is an acetic-acid/vinegar off-flavor).
- A properly scaled **Logistic Regression reaches AUC 0.876**, matching the dataset's own published benchmark (~0.88), and **beats both a hyperparameter-tuned Decision Tree (AUC 0.829) and an untuned Random Forest (AUC 0.868)** — a clean reminder that a simple linear model can outperform tree ensembles on well-behaved, modestly-sized tabular data.
- **240 of 1,599 rows (15%) are exact duplicates.** De-duplicated before modeling so the same wine can't leak across the train/test split — skipping this step would silently overstate model performance.
- Random Forest feature importances confirm the EDA: **alcohol, sulphates, volatile acidity, and citric acid** together account for over half of predictive signal.

## Recommendations
1. Deploy the **Logistic Regression model** for a QC screening tool — it's both the top performer by AUC and fully interpretable (coefficients show each feature's direction and relative effect size), unlike the black-box Random Forest.
2. Prioritize **alcohol content and volatile acidity control** in production — the two chemical levers most associated with the "good" tier.
3. Treat the classification **threshold as a tunable business decision** — a QC team that wants to catch nearly every good batch should lower it; one optimizing inspector time should raise it.
4. **Always de-duplicate before splitting** this dataset (or similar lab-measurement data) — identical rows silently inflate reported model performance otherwise.

Full code and outputs are in [`analysis.ipynb`](./analysis.ipynb).

## Files
- `analysis.ipynb` — full notebook: cleaning → EDA → correlation → classification (Logistic Regression, tuned Decision Tree, Random Forest) → ROC/AUC comparison → feature importance → findings & recommendations
- `data/` — the dataset CSV (included directly, no download needed) + `data/README.md` with the source link
- `images/` — exported charts referenced above and in the notebook
