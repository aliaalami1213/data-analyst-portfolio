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
- **Overall catalog split**: 69.6% movies vs. 30.4% TV shows (8,807 titles total).
- **TV shows are gaining share**: the TV-show share of titles *added* dipped to 25% in 2018, then climbed back to 33.7% by 2021 — while movies added per year fell from 1,237 (2018) to 993 (2021), a **20% decline**, TV shows added grew from 412 to 505, a **23% increase** over the same period.
- **Fastest-growing genres (2018→2021 additions)**: Anime Series (+82%) and TV Action & Adventure (+76%) grew fastest — both TV formats, reinforcing the shift toward TV-style content. Kids' TV (+51%) and Children & Family Movies (+44%) also grew strongly.
- **Most common genres overall**: International Movies (2,752 titles), Dramas (2,427), Comedies (1,674) — international and drama content dominate the catalog by volume.
- **Countries**: the US leads with 3,689 titles (36.8% of titles with a listed country), but **India is the clear #2** at 1,046, followed by the UK (804) and Canada (445) — a meaningfully international footprint beyond just the US.
- **Ratings skew mature**: TV-MA is the most common rating (36.4% of titles), followed by TV-14 (24.5%) — together, ~61% of the catalog is rated for teens/adults or above.

## Conclusion
Netflix's catalog is still majority movies, but the *growth* since 2018 has clearly shifted toward TV — TV show additions grew ~23% while movie additions fell ~20%, and the fastest-growing genres (anime, TV action/adventure, kids' TV) are all series formats. Combined with India's strong #2 position behind the US, this points to a strategy leaning into serialized content and international (particularly South Asian) markets rather than continuing to scale the movie catalog. The heavy TV-MA/TV-14 skew suggests the core audience remains teens/adults even as the format mix shifts.

## Files
- `analysis.ipynb` — full notebook
- `data/README.md` — dataset download instructions
- `images/` — exported chart PNGs referenced above
