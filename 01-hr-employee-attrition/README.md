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
- **Overall attrition rate: 16.1%** (237 of 1,470 employees). No nulls or duplicate rows in the raw data.
- **Overtime is the single strongest driver**: employees who work overtime leave at **30.5%**, almost **3x** the rate of those who don't (**10.4%**) — the highest correlation with attrition of any feature in the dataset (r = 0.25, vs. ≤0.17 for every numeric column).
- **Highest-risk segment**: Sales Representatives working overtime — **66.7%** attrition (n=24). More broadly, overtime employees with < 2 years' tenure churn at **55.1%** (n=69).
- **By role**: Sales Reps (39.8%) and Lab Technicians (23.9%) have the highest attrition; Managers (4.9%) and Research Directors (2.5%) the lowest.
- **By marital status**: Single employees leave at **25.5%** vs. 12.5% (married) and 10.1% (divorced).
- Leavers skew less tenured and lower paid: median monthly income for leavers is **$3,202** vs. **$5,204** for stayers; median tenure is **3 years** vs. **6 years**. `TotalWorkingYears`, `JobLevel`, and `MonthlyIncome` are the next-strongest correlated factors after OverTime (all negative — more experience/seniority/pay = less likely to leave).
- Job satisfaction score alone doesn't separate leavers from stayers (median 3/4 for both) — it's overtime, tenure, and role, not self-reported satisfaction, that predict who leaves.

## Recommendations
1. **Cap or compensate overtime, starting in Sales.** Overtime employees leave at 3x the base rate, and Sales Reps working overtime hit 67% attrition — review workload distribution and on-call/overtime pay in that team first.
2. **Target retention efforts at the first two years.** Overtime + <2 years tenure is a 55% attrition combination — an early "at-risk" flag (new hire + overtime) would let HR intervene with workload adjustments or check-ins before employees hit their 1-year mark.
3. **Revisit entry-level compensation for high-churn roles** (Sales Rep, Lab Technician) — leavers earn ~$2,000/month less than stayers on median, suggesting pay is a live factor even though self-reported job satisfaction isn't.

## Files
- `analysis.ipynb` — full notebook
- `data/README.md` — dataset download instructions
- `images/` — exported chart PNGs referenced above
