# Alia Alami — Data Analytics Portfolio

Hi, I'm Alia 👋 This repo is a collection of end-to-end data analysis projects I built using public Kaggle datasets — from raw data to cleaned data, exploratory analysis, and business recommendations.

📫 **Connect with me:** [LinkedIn](https://www.linkedin.com/in/alia-alami)

---

## 📊 Projects

| # | Project | Dataset | Skills Demonstrated | Key Question |
|---|---------|---------|----------------------|---------------|
| 1 | [HR Employee Attrition Analysis](./01-hr-employee-attrition) | [IBM HR Analytics (Kaggle)](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset) | Data cleaning, segmentation, hypothesis-driven EDA, visualization | Who is leaving the company, and why? |
| 2 | [Netflix Content Trends](./02-netflix-content-trends) | [Netflix Movies and TV Shows (Kaggle)](https://www.kaggle.com/datasets/shivamb/netflix-shows) | Text/categorical data wrangling, trend analysis, storytelling with charts | How has Netflix's content strategy shifted over time? |
| 3 | [California Home Price Prediction](./03-california-home-price-prediction) | [California Housing Prices (1990 Census)](https://www.kaggle.com/datasets/camnugent/california-housing-prices) | Regression modeling (OLS + neural network), VIF/multicollinearity, statistical diagnostics, model comparison | Can neighborhood demographics and geography predict home value, and what drives price? |
| 4 | [E-Commerce Customer Segmentation, Churn & CLV Prediction](./04-ecommerce-customer-segmentation) | [E-Commerce Customer Segmentation 2026 (Kaggle)](https://www.kaggle.com/datasets/datascikhan/e-commerce-customer-segmentation-2026) | K-Means clustering, classification & regression (scikit-learn), feature-leakage-aware model design, marketing targeting frameworks | Which customers are most valuable, which are at risk of churning, and how should marketing prioritize retention spend? |
| 5 | [Online Food Delivery — Customer Ordering Behavior](./05-online-food-delivery-analysis) | [Online Food Ordering Dataset (Kaggle)](https://www.kaggle.com/datasets/srisyra02/online-food-ordering-dataset) | Data cleaning (duplicate columns/rows), segmentation, crosstab analysis, visualization | Which demographic, income, and household factors are associated with placing an online food order? |

Each project folder contains:
- `README.md` — business question, approach, and key findings (written for a recruiter skimming in 60 seconds)
- `analysis.ipynb` — the full, executed notebook (data cleaning → EDA → insights, with charts and outputs saved)
- `images/` — exported charts referenced in the README
- `data/README.md` — dataset source link (the raw CSV is included directly in `data/` for projects 1, 2, 4, and 5 so the notebook runs out of the box; project 3 fetches its data at runtime — see its `data/README.md`)

Project 3 also includes `657_Final_Presentation.pptx`, the slide deck summarizing that project's methodology and results.

## 🛠 Tools

Python (pandas, numpy, matplotlib, seaborn, scikit-learn, statsmodels, TensorFlow/Keras), Jupyter, and standard data-analyst workflow: define question → clean data → explore → visualize → (model) → recommend.

## 🚀 Getting a project running locally

```bash
git clone https://github.com/aliaalami1213/data-analyst-portfolio.git
cd data-analyst-portfolio
pip install -r requirements.txt
```

Projects 1, 2, and 4's data is already included in `data/`, so you can open `analysis.ipynb` and run it directly — no download needed. Project 3 pulls its data from a hosted link at runtime; see its `data/README.md` for a fallback source. Each project's `data/README.md` links back to the original dataset.

## 📌 About me

I'm finishing my M.S. in Business Analytics at UMass Amherst (Aug 2026), on top of a B.S. in Mathematics with a concentration in Statistics and Data Science. I've worked as a data/analytics intern across nonprofit consulting, education-finance policy, legal research, and banking — turning large transactional and program datasets into dashboards, models, and recommendations that stakeholders acted on (including a $285M+ capital-formation impact dashboard and a $5.38M funding-disparity finding that shaped district budget decisions). I'm targeting Data Analyst / Business Analyst roles where I can pair Python/R/SQL analysis with clear storytelling in Tableau and Power BI.
