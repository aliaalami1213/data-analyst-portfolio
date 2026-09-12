# Netflix Content Trends

**Dataset:** [Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows) (Kaggle, ~8,800 titles as of 2021)

## Business Question
How has Netflix's content strategy shifted over time — movies vs. TV shows, genres, countries of origin, and content ratings? What does the trend suggest about where they're investing?

## Approach
1. **Clean** — parse `date_added`, split multi-value fields (`listed_in` genres, `country`, `cast`), handle missing `director`/`country`.
2. **Trend over time** — titles added per year, movie vs. TV show split over time.
3. **Genre & country analysis** — most common genres, top content-producing countries, how the mix has changed.
4. **Ratings** — distribution of content ratings (TV-MA, PG-13, etc.) and how it's shifted.
5. **Recommend / conclude** — 2-3 sentences on what the strategic shift appears to be (e.g. "TV shows have grown faster than movies since 2018, and international content now makes up X% vs Y% in 2015").

## Key Findings
_Fill in after running `analysis.ipynb` — e.g._
- Movies vs. TV shows split: _____
- Fastest-growing genre: _____
- Top country besides the US: _____

## Conclusion
_2-3 sentences interpreting what the trends suggest about Netflix's content strategy._

## Files
- `analysis.ipynb` — full notebook
- `data/README.md` — dataset download instructions
- `images/` — exported chart PNGs referenced above
