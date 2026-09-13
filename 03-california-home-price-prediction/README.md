# California Home Price Prediction

**Dataset:** California Housing Prices — 20,640 California districts (block groups) from the 1990 U.S. Census, 10 features ([data/README.md](./data)).

## Business Question
Can neighborhood-level demographics and geography accurately forecast California home values? California housing prices vary by up to ~30x depending on location, income, and density — a reliable price model helps home buyers avoid overpaying, sellers/agents price competitively, and investors spot undervalued areas.

## Approach
1. **Clean & prepare** — impute 207 missing `total_bedrooms` values with the median, log-transform right-skewed features (`total_rooms`, `total_bedrooms`, `population`, `households`), one-hot encode `ocean_proximity`.
2. **Explore** — correlation heatmap, distribution plots, and multicollinearity checks (VIF) across all numeric features.
3. **Feature engineer** — derive `bedrooms_per_household`, `rooms_per_household`, `population_per_household`; drop redundant/collinear columns (`longitude`, `latitude`, `total_rooms`) identified via VIF.
4. **Model** — fit two models on a log-transformed target (`median_house_value_log`): a baseline OLS regression (with full statistical diagnostics) and a neural network (TensorFlow/Keras), and compare them on R², MAE, and RMSE.
5. **Diagnose** — validate OLS assumptions (linearity, multicollinearity, homoscedasticity via Breusch-Pagan, normality of residuals via Q-Q plot) and interpret coefficients as business drivers.

## Key Findings
- **Neural network outperforms OLS**: R² = 0.68 (NN) vs. 0.617 (OLS) — the NN explains ~70% of the variance in California home prices.
- **Typical prediction error**: MAE = **$43,452**; RMSE = **$63,016** (higher than MAE, confirming a subset of large-error/outlier predictions — mostly expensive homes).
- **Income is the strongest driver**: every 1-unit increase in median neighborhood income is associated with a **~17% jump** in home value (r = 0.69 with price, the strongest single correlation in the dataset).
- **Location matters a lot**: being on an **island** carries a **70%+ price premium** over standard coastal properties, while moving **inland** cuts expected value by roughly **50%** compared to near-ocean properties.
- **Multicollinearity was a real issue**: `total_rooms`, `total_bedrooms`, `population`, and `households` were all highly correlated (|r| > 0.85) — engineered into ratio features (e.g. bedrooms per household) and/or dropped based on VIF rather than fed in raw.
- **Model diagnostics flagged heteroscedasticity** (Breusch-Pagan test): prediction errors are not evenly spread across price ranges — the model is less reliable at the high and low ends, partly because the target is capped at $500,001 in the source data, which suppresses signal for luxury homes.

## Limitations
1990 Census data with no temporal component (can't capture market cycles), a $500K price cap that hurts luxury-home accuracy, and ~30% of price variance still unexplained by the current feature set. See the [presentation](./657_Final_Presentation.pptx) for the full discussion of next steps (gradient boosting, segmented models by region/price tier, cross-validation, SHAP explainability).

## Files
- `analysis.ipynb` — full notebook: cleaning → EDA → feature engineering → OLS + neural network models → diagnostics
- `657_Final_Presentation.pptx` — final presentation summarizing the business framing, methodology, and results
- `images/` — key charts (correlation heatmap, ocean-proximity price differences, training curves, residual diagnostics)
- `data/README.md` — dataset source and how the notebook loads it
