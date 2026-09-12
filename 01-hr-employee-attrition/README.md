# HR Employee Attrition Analysis

**Dataset:** [IBM HR Analytics Employee Attrition & Performance](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset) (Kaggle, ~1,470 rows, fictional but realistic IBM HR dataset)

## Business Question
Which employees are most likely to leave, and what factors (overtime, income, commute distance, job satisfaction, tenure) drive attrition? What would you recommend HR prioritize to reduce turnover?

## Approach
1. **Clean & prepare** — check for nulls/duplicates, fix data types, drop constant columns (e.g. `EmployeeCount`, `Over18`).
2. **Segment** — compare attrition rate across department, job role, overtime status, income bracket, and tenure.
3. **Explore relationships** — correlation between attrition and job satisfaction, work-life balance, distance from home, years since last promotion.
4. **Visualize** — bar charts of attrition rate by segment, distribution plots for income/tenure of leavers vs. stayers.
5. **Recommend** — translate findings into 2-3 concrete HR actions (e.g. "overtime employees leave at 3x the rate — review workload in X department").

## Key Findings
_Fill in after running `analysis.ipynb` — e.g._
- Attrition rate overall: **XX%**
- Highest-risk segment: _(e.g. Sales reps working overtime with < 2 years tenure)_
- Strongest correlated factor: _(e.g. OverTime, MonthlyIncome, JobSatisfaction)_

## Recommendations
_2-3 sentences of business advice based on the findings above — this is what separates a "data analyst" project from a plain EDA notebook._

## Files
- `analysis.ipynb` — full notebook
- `data/README.md` — dataset download instructions
- `images/` — exported chart PNGs referenced above
