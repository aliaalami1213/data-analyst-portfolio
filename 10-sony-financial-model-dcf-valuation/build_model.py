"""Step 2 of the model: build sony_financial_model.xlsx.

Reads the reported statements in data/ and the segment growth rates produced by
forecast_revenue.py, then writes a linked Excel workbook in which every forecast
cell is a live formula:

    Assumptions -> revenue build -> income statement -> balance sheet -> cash flow -> DCF

The same model is written three times (Base, Upside, Downside sheets), each reading
its own column of the Assumptions sheet, so the scenarios are compared live.

Usage:  python build_model.py
"""
from pathlib import Path

import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

HERE = Path(__file__).parent
DATA = HERE / "data"
OUT = HERE / "sony_financial_model.xlsx"
FILING = "Sony Group Form 20-F FY2025 (SEC EDGAR, filed 2026-06-18)"
FILING_URL = "https://www.sec.gov/Archives/edgar/data/313838/000119312526274893/d28719d20f.htm"

# ---------------------------------------------------------------- styles
FONT = "Arial"
BLUE, BLACK, GREEN, WHITE, GREY = "0000FF", "000000", "008000", "FFFFFF", "595959"
F_INPUT = Font(name=FONT, size=10, color=BLUE)
F_CALC = Font(name=FONT, size=10, color=BLACK)
F_LINK = Font(name=FONT, size=10, color=GREEN)
F_BOLD = Font(name=FONT, size=10, bold=True)
F_NOTE = Font(name=FONT, size=9, italic=True, color=GREY)
F_TITLE = Font(name=FONT, size=14, bold=True)
F_HEAD = Font(name=FONT, size=10, bold=True, color=WHITE)
FILL_HEAD = PatternFill("solid", start_color="1F3864")
FILL_SECTION = PatternFill("solid", start_color="D9E1F2")
FILL_KEY = PatternFill("solid", start_color="FFFF00")
FILL_FCST = PatternFill("solid", start_color="F2F2F2")
TOP = Border(top=Side(style="thin"))
MONEY = "#,##0;(#,##0);-"
PCT = "0.0%;(0.0%);-"
DAYS = "0.0"
FACTOR = "0.000"
YEN = '"¥"#,##0'
USD = '"$"0.00'

HIST_YEARS = ["FY2023", "FY2024", "FY2025"]
FCST_YEARS = ["FY2026", "FY2027", "FY2028", "FY2029", "FY2030"]
HIST_COLS = dict(zip(HIST_YEARS, "CDE"))
FCST_COLS = list("FGHIJ")
SCENARIOS = {"Base": "C", "Upside": "D", "Downside": "E"}

SEGMENTS = [
    ("GNS", "Game & Network Services"),
    ("MUS", "Music"),
    ("PIC", "Pictures"),
    ("ETS", "Entertainment Technology & Services"),
    ("ISS", "Imaging & Sensing Solutions"),
    ("OTH", "All Other"),
]


def put(ws, ref, value, font=F_CALC, fmt=None, fill=None, bold=False, border=None, align=None):
    cell = ws[ref]
    cell.value = value
    cell.font = Font(name=font.name, size=font.size, color=font.color, italic=font.italic,
                     bold=bold or font.bold)
    if fmt:
        cell.number_format = fmt
    if fill:
        cell.fill = fill
    if border:
        cell.border = border
    if align:
        cell.alignment = align
    return cell


def header_row(ws, row, labels, first_col="A"):
    for i, label in enumerate(labels):
        col = chr(ord(first_col) + i)
        put(ws, f"{col}{row}", label, F_HEAD, fill=FILL_HEAD,
            align=Alignment(horizontal="left" if i == 0 else "center"))


def section(ws, row, label, last_col="J"):
    for col in range(1, ord(last_col) - 64 + 1):
        ws.cell(row=row, column=col).fill = FILL_SECTION
    put(ws, f"A{row}", label, F_BOLD, fill=FILL_SECTION)


def link_font(formula):
    """Green for a pure link to another sheet, black for a calculation."""
    body = str(formula)[1:]
    pure = "!" in body and not any(op in body for op in "+-*/(^,")
    return F_LINK if pure else F_CALC


# ---------------------------------------------------------------- load data
segments = pd.read_csv(DATA / "segment_sales.csv", index_col="segment")
income = pd.read_csv(DATA / "income_statement.csv", index_col="line_item")
balance = pd.read_csv(DATA / "balance_sheet.csv", index_col="line_item")
cash = pd.read_csv(DATA / "cash_flow.csv", index_col="line_item")
forecast = pd.read_csv(DATA / "revenue_forecast.csv", index_col="segment")
market = pd.read_csv(DATA / "market_inputs.csv", index_col="input")

wb = Workbook()

# ================================================================ Historical
hist = wb.active
hist.title = "Historical"
HIST_ALL = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025"]
HCOL = dict(zip(HIST_ALL, "BCDEF"))
HROW = {}  # (table, line item) -> row

put(hist, "A1", "Sony Group Corporation — reported financials", F_TITLE)
put(hist, "A2", "¥ millions. FY2025 = fiscal year ended March 31, 2026. Continuing operations "
                "(Financial Services, spun off in FY2025, is excluded from income and cash flow).", F_NOTE)
put(hist, "A3", f"Source: {FILING}, {FILING_URL}. Segment sales for FY2021–FY2022 from the FY2023 Form 20-F.", F_NOTE)

row = 5


def hist_table(title, frame, key):
    global row
    header_row(hist, row, [title] + HIST_ALL)
    row += 1
    for item, values in frame.iterrows():
        put(hist, f"A{row}", item)
        for year in HIST_ALL:
            if year in frame.columns:
                put(hist, f"{HCOL[year]}{row}", int(values[year]), F_INPUT, MONEY)
        is_total = item.startswith(("Total", "Operating income", "Income before", "Net income from"))
        if is_total:
            for col in "ABCDEF":
                hist[f"{col}{row}"].font = Font(name=FONT, size=10, bold=True,
                                                color=BLACK if col == "A" else BLUE)
        HROW[(key, item)] = row
        row += 1
    row += 1


hist_table("Segment sales", segments, "seg")
hist_table("Income statement", income, "is")
hist_table("Balance sheet (March 31 following the fiscal year)", balance, "bs")
hist_table("Cash flow (selected lines)", cash, "cf")
put(hist, f"A{row}", "The March 31, 2025 balance sheet (FY2024) still includes Financial Services assets and "
                     "liabilities, so it is not comparable with March 31, 2026.", F_NOTE)
hist.column_dimensions["A"].width = 68
for col in "BCDEF":
    hist.column_dimensions[col].width = 14
hist.freeze_panes = "B6"


def H(key, item, year):
    return f"Historical!${HCOL[year]}${HROW[(key, item)]}"


# ================================================================ Assumptions
asm = wb.create_sheet("Assumptions")
AROW = {}
put(asm, "A1", "Assumptions", F_TITLE)
put(asm, "A2", "Blue = input you can change. Black = calculated. Yellow = key assumption that drives the "
               "scenarios. Each scenario sheet reads its own column.", F_NOTE)
header_row(asm, 4, ["Driver", "Unit", "Base", "Upside", "Downside", "Source / rationale"])
arow = 5


def asm_section(label):
    global arow
    section(asm, arow, label, "F")
    arow += 1


def assume(key, label, unit, base, up=None, down=None, fmt=PCT, note="", key_input=False, calc=False):
    """One assumption row. If up/down are omitted the scenarios share the Base value."""
    global arow
    put(asm, f"A{arow}", label)
    put(asm, f"B{arow}", unit, F_NOTE)
    font = F_CALC if calc else F_INPUT
    fill = FILL_KEY if key_input else None
    put(asm, f"C{arow}", base, link_font(base) if calc else font, fmt, fill)
    for col, value in (("D", up), ("E", down)):
        if value is None:
            put(asm, f"{col}{arow}", f"=$C{arow}", F_CALC, fmt)
        else:
            put(asm, f"{col}{arow}", value, font, fmt, fill)
    put(asm, f"F{arow}", note, F_NOTE)
    AROW[key] = arow
    arow += 1


def last(item, key="is"):
    return H(key, item, "FY2025")


asm_section("Revenue")
for code, name in SEGMENTS:
    assume(f"g_{code}", f"{name}: starting growth (FY2026)", "% yoy",
           float(forecast.loc[name, "start_growth"]),
           note=f"forecast_revenue.py: {forecast.loc[name, 'method']} "
                f"(raw {forecast.loc[name, 'raw_growth']:.1%}, capped to -5%..+12%)")
assume("g_adj", "Scenario adjustment to every segment's growth", "pp", 0.0, 0.02, -0.02, key_input=True,
       note="Analyst assumption: +/-2 points of growth a year in the upside/downside case")
assume("g_lr", "Long-run growth each segment fades to by FY2030", "% yoy", 0.02,
       note="Analyst assumption; matches LONG_RUN_GROWTH in forecast_revenue.py")
seg_sum = "+".join(H("seg", name, "FY2025") for _, name in SEGMENTS)
assume("elim", "Corporate and intersegment elimination", "% of segment sales",
       f"=1-{last('Sales')}/({seg_sum})", calc=True,
       note="FY2025 actual: segment sales less consolidated sales")

asm_section("Margins and reinvestment")
assume("cogs", "Cost of sales", "% of sales", 0.692, 0.682, 0.707, key_input=True,
       note="FY2023-25 actual: 71.8%, 70.7%, 69.2%. Base holds FY2025; downside is about the 3-yr average (70.6%)")
assume("sga", "Selling, general and administrative", "% of sales", 0.184,
       note="FY2025 actual 18.4% (FY2023-24: 19.1%, 18.8%)")
assume("da", "Depreciation and amortization", "% of sales", 0.095,
       note="FY2025 actual 9.5%; includes amortization of film and other content assets")
assume("capex", "Capital expenditure (PP&E and intangibles)", "% of sales", 0.047,
       note="FY2023-25 average (5.4%, 5.2%, 3.7%)")
assume("content", "Investment in content assets", "% of sales", 0.051,
       note="FY2023-25 average (4.3%, 5.7%, 5.3%); Sony reports this within operating cash flow")
assume("tax", "Tax rate", "% of pre-tax income", 0.26,
       note="FY2025 effective rate 25.8%; Japanese statutory rate 31.5% (Form 20-F income taxes note)")

asm_section("Working capital (held at FY2025 levels)")
assume("rec_days", "Receivable days", "days of sales",
       f"={last('Trade and other receivables, and contract assets', 'bs')}/{last('Sales')}*365",
       fmt=DAYS, calc=True, note="FY2025 actual")
assume("inv_days", "Inventory days", "days of cost of sales",
       f"={last('Inventories', 'bs')}/{last('Cost of sales')}*365", fmt=DAYS, calc=True, note="FY2025 actual")
assume("pay_days", "Payable days", "days of cost of sales",
       f"={last('Trade and other payables', 'bs')}/{last('Cost of sales')}*365", fmt=DAYS, calc=True,
       note="FY2025 actual")
oca = "+".join(last(i, "bs") for i in ("Other financial assets (current)", "Other current assets"))
ocl_items = ("Income taxes payable", "Participation and residual liabilities in the Pictures segment (current)",
             "Contract liabilities", "Other financial liabilities (current)", "Other current liabilities")
ocl = "+".join(last(i, "bs") for i in ocl_items)
assume("oca", "Other current assets", "% of sales", f"=({oca})/{last('Sales')}", calc=True, note="FY2025 actual")
assume("ocl", "Other current liabilities", "% of sales", f"=({ocl})/{last('Sales')}", calc=True,
       note="FY2025 actual; taxes payable, contract liabilities, participations, other")

asm_section("Financing")
assume("int_inc", "Interest earned on opening cash", "%", 0.015, note="Analyst assumption")
assume("int_exp", "Interest paid on opening debt and leases", "%", 0.035,
       note="Analyst assumption, in line with the pre-tax cost of debt below")
assume("payout", "Dividend payout", "% of net income", 0.13, note="FY2025 actual 12.8% of continuing net income")
assume("buyback", "Share repurchases per year", "¥ millions", 300000, fmt=MONEY,
       note="Analyst assumption; FY2023-25 actual: 203bn, 286bn, 522bn")
assume("debt_chg", "Net new borrowing per year", "¥ millions", 0, fmt=MONEY,
       note="Analyst assumption: maturing debt is refinanced")

asm_section("Valuation")
assume("tg", "Terminal growth rate", "%", 0.02, 0.025, 0.015, key_input=True,
       note="Analyst assumption; below the 10-yr JGB yield so cash flows do not outgrow the risk-free rate")
m = market["value"]
assume("rf", "Risk-free rate (10-yr Japanese government bond)", "%", float(m["jgb_10y_yield_pct"]) / 100,
       fmt="0.00%", note=f"Japan Ministry of Finance, {market.loc['jgb_10y_yield_pct', 'as_of']}")
assume("erp", "Equity risk premium", "%", 0.055, key_input=True,
       note="Analyst assumption, not sourced. Replace with your own estimate")
assume("beta", "Equity beta", "x", 1.0, fmt="0.00", key_input=True,
       note="Analyst assumption, not estimated from data. Replace with your own estimate")
assume("kd", "Pre-tax cost of debt", "%", 0.035, note="Analyst assumption: risk-free rate plus about 0.5 points")
assume("price", "Share price (ADR, 1 ADR = 1 share)", "US$", float(m["share_price_usd"]), fmt=USD,
       note=f"Close on {market.loc['share_price_usd', 'as_of']} from project 6's price file")
assume("fx", "Exchange rate", "¥ per US$", float(m["usd_jpy"]), fmt="0.00",
       note=f"ECB reference rate, {market.loc['usd_jpy', 'as_of']}")
assume("shares", "Shares outstanding", "shares", int(m["shares_outstanding"]), fmt="#,##0",
       note="Form 20-F FY2025 cover page, as of March 31, 2026")
A = lambda key, col="C": f"Assumptions!${col}${AROW[key]}"  # noqa: E731
L = lambda key: f"$C${AROW[key]}"  # noqa: E731  (same-sheet reference)
assume("price_jpy", "Share price in yen", "¥", f"={L('price')}*{L('fx')}", fmt=YEN, calc=True)
assume("mcap", "Market capitalisation", "¥ millions", f"={L('price_jpy')}*{L('shares')}/1000000",
       fmt=MONEY, calc=True)
debt_items = ("Short-term borrowings", "Current portion of long-term debt", "Long-term debt")
lease_items = ("Lease liabilities (current)", "Lease liabilities (non-current)")
debt_sum = "+".join(last(i, "bs") for i in debt_items + lease_items)
assume("debt_mv", "Debt including lease liabilities", "¥ millions", f"={debt_sum}", fmt=MONEY, calc=True,
       note="Book value at March 31, 2026, used as a proxy for market value")
assume("w_e", "Weight of equity", "%", f"={L('mcap')}/({L('mcap')}+{L('debt_mv')})", calc=True)
assume("w_d", "Weight of debt", "%", f"=1-{L('w_e')}", calc=True)
assume("ke", "Cost of equity (CAPM)", "%", f"={L('rf')}+{L('beta')}*{L('erp')}", fmt="0.00%", calc=True,
       note="Risk-free rate + beta x equity risk premium")
assume("kd_at", "After-tax cost of debt", "%", f"={L('kd')}*(1-{L('tax')})", fmt="0.00%", calc=True)
assume("wacc", "WACC", "%", f"={L('w_e')}*{L('ke')}+{L('w_d')}*{L('kd_at')}", fmt="0.00%", calc=True,
       note="Discount rate applied to free cash flow in every scenario")
asm[f"A{AROW['wacc']}"].font = F_BOLD
asm.column_dimensions["A"].width = 50
asm.column_dimensions["B"].width = 20
for col in "CDE":
    asm.column_dimensions[col].width = 14
asm.column_dimensions["F"].width = 95
asm.freeze_panes = "C5"


# ================================================================ scenario sheets
def build_scenario(name):
    ws = wb.create_sheet(name)
    acol = SCENARIOS[name]
    a = lambda key: A(key, acol)  # noqa: E731
    R = {}

    put(ws, "A1", f"Sony Group — {name} case: three statements and DCF", F_TITLE)
    put(ws, "A2", "¥ millions unless stated. A = reported, E = forecast. Every forecast cell is a formula "
                  f"driven by the {name} column of the Assumptions sheet.", F_NOTE)
    header_row(ws, 4, ["", "Driver"] + [y + "A" for y in HIST_YEARS] + [y + "E" for y in FCST_YEARS])
    put(ws, "A5", "Forecast year", F_NOTE)
    for i, col in enumerate(FCST_COLS, start=1):
        put(ws, f"{col}5", i, F_NOTE, "0", align=Alignment(horizontal="center"))

    state = {"row": 6}

    def sec(label):
        state["row"] += 1
        section(ws, state["row"], label)
        state["row"] += 1

    def line(key, label, hist=None, fcst=None, fmt=MONEY, driver="", bold=False, top=False):
        """hist: {year: formula}; fcst: function(col, prev_col) -> formula."""
        r = state["row"]
        R[key] = r
        put(ws, f"A{r}", label, F_BOLD if bold else F_CALC)
        put(ws, f"B{r}", driver, F_NOTE)
        for year, formula in (hist or {}).items():
            put(ws, f"{HIST_COLS[year]}{r}", formula, link_font(formula), fmt, bold=bold,
                border=TOP if top else None)
        if fcst:
            for i, col in enumerate(FCST_COLS):
                prev = "E" if i == 0 else FCST_COLS[i - 1]
                formula = fcst(col, prev)
                put(ws, f"{col}{r}", formula, link_font(formula), fmt, FILL_FCST, bold=bold,
                    border=TOP if top else None)
        state["row"] += 1
        return r

    def hist_link(key, item, years=HIST_YEARS, sign=1):
        prefix = "=" if sign == 1 else "=-"
        return {y: f"{prefix}{H(key, item, y)}" for y in years}

    def hist_sum(items, years):
        return {y: "=" + "+".join(H("bs", i, y) for i in items) for y in years}

    def c(key, col):
        return f"{col}{R[key]}"

    # ---------------- revenue build
    sec("REVENUE BUILD")
    for code, seg_name in SEGMENTS:
        line(f"s_{code}", seg_name, hist_link("seg", seg_name),
             lambda col, prev, code=code: f"={prev}{R[f's_{code}']}*(1+{col}{R[f's_{code}'] + 1})")
        line(f"sg_{code}", "   growth", {y: f"={H('seg', seg_name, y)}/{H('seg', seg_name, HIST_ALL[HIST_ALL.index(y) - 1])}-1"
                                         for y in HIST_YEARS},
             lambda col, prev, code=code: f"={a(f'g_{code}')}+({a('g_lr')}-{a(f'g_{code}')})*({col}$5-1)/4+{a('g_adj')}",
             fmt=PCT, driver="start, fading to long-run")
    seg_keys = [f"s_{code}" for code, _ in SEGMENTS]
    total = lambda col: "+".join(c(k, col) for k in seg_keys)  # noqa: E731
    line("s_seg", "Segment sales", {y: f"={total(HIST_COLS[y])}" for y in HIST_YEARS},
         lambda col, prev: f"={total(col)}", top=True)
    line("s_elim", "Corporate and elimination",
         {y: f"={H('is', 'Sales', y)}-{c('s_seg', HIST_COLS[y])}" for y in HIST_YEARS},
         lambda col, prev: f"=-{a('elim')}*{c('s_seg', col)}", driver="% of segment sales")

    # ---------------- income statement
    sec("INCOME STATEMENT")
    line("sales", "Sales", hist_link("is", "Sales"),
         lambda col, prev: f"={c('s_seg', col)}+{c('s_elim', col)}", bold=True)
    line("sales_g", "   growth", {y: f"={c('sales', HIST_COLS[y])}/{c('sales', HIST_COLS[HIST_YEARS[i - 1]])}-1"
                                  for i, y in enumerate(HIST_YEARS) if i},
         lambda col, prev: f"={c('sales', col)}/{c('sales', prev)}-1", fmt=PCT)
    line("cogs", "Cost of sales", hist_link("is", "Cost of sales"),
         lambda col, prev: f"={a('cogs')}*{c('sales', col)}", driver="% of sales")
    line("gp", "Gross profit", {y: f"={c('sales', HIST_COLS[y])}-{c('cogs', HIST_COLS[y])}" for y in HIST_YEARS},
         lambda col, prev: f"={c('sales', col)}-{c('cogs', col)}", top=True)
    line("sga", "Selling, general and administrative", hist_link("is", "Selling, general and administrative"),
         lambda col, prev: f"={a('sga')}*{c('sales', col)}", driver="% of sales")
    line("oth", "Other operating (income) expense, net", hist_link("is", "Other operating (income) expense, net"),
         lambda col, prev: "=0", driver="assumed nil")
    line("eqm", "Share of profit (loss) of equity-method investments",
         hist_link("is", "Share of profit (loss) of equity-method investments"),
         lambda col, prev: "=0", driver="assumed nil")
    op = lambda col: f"={c('gp', col)}-{c('sga', col)}-{c('oth', col)}+{c('eqm', col)}"  # noqa: E731
    line("ebit", "Operating income", {y: op(HIST_COLS[y]) for y in HIST_YEARS},
         lambda col, prev: op(col), bold=True, top=True)
    line("ebit_m", "   operating margin", {y: f"={c('ebit', HIST_COLS[y])}/{c('sales', HIST_COLS[y])}" for y in HIST_YEARS},
         lambda col, prev: f"={c('ebit', col)}/{c('sales', col)}", fmt=PCT)
    state["row"] += 6  # reserve rows; balance-sheet keys are needed for interest
    interest_rows = state["row"] - 6
    state["row"] = interest_rows
    R["fin_inc"], R["fin_exp"], R["pbt"], R["taxes"], R["ni"], R["da"] = range(interest_rows, interest_rows + 6)
    state["row"] = interest_rows + 6
    line("ebitda", "EBITDA", {y: f"={c('ebit', HIST_COLS[y])}+{c('da', HIST_COLS[y])}" for y in HIST_YEARS},
         lambda col, prev: f"={c('ebit', col)}+{c('da', col)}")

    # ---------------- balance sheet
    bs_years = ["FY2024", "FY2025"]
    sec("BALANCE SHEET (March 31 following the fiscal year)")
    line("cash", "Cash and cash equivalents", hist_link("bs", "Cash and cash equivalents", bs_years))
    line("rec", "Trade and other receivables", hist_link("bs", "Trade and other receivables, and contract assets", bs_years),
         lambda col, prev: f"={a('rec_days')}/365*{c('sales', col)}", driver="days of sales")
    line("inv", "Inventories", hist_link("bs", "Inventories", bs_years),
         lambda col, prev: f"={a('inv_days')}/365*{c('cogs', col)}", driver="days of cost of sales")
    line("oca", "Other current assets",
         hist_sum(("Other financial assets (current)", "Other current assets"), bs_years),
         lambda col, prev: f"={a('oca')}*{c('sales', col)}", driver="% of sales")
    line("fs_a", "Financial Services assets (discontinued)",
         hist_sum(("Investments and advances in the Financial Services segment (current)",
                   "Investments and advances in the Financial Services segment (non-current)"), bs_years),
         lambda col, prev: "=0", driver="spun off")
    line("lta", "Operating long-term assets (PP&E, right-of-use, content, intangibles)",
         hist_sum(("Property, plant and equipment", "Right-of-use assets", "Content assets",
                   "Other intangible assets"), bs_years))
    line("gw", "Goodwill", hist_link("bs", "Goodwill", bs_years),
         lambda col, prev: f"={prev}{state['row']}", driver="held flat")
    line("onca", "Other non-current assets (investments, deferred tax, other)",
         hist_sum(("Investments accounted for using the equity method", "Deferred tax assets",
                   "Other financial assets (non-current)", "Other non-current assets"), bs_years),
         lambda col, prev: f"={prev}{state['row']}", driver="held flat")
    asset_keys = ["cash", "rec", "inv", "oca", "fs_a", "lta", "gw", "onca"]
    tot_a = lambda col: "=" + "+".join(c(k, col) for k in asset_keys)  # noqa: E731
    line("ta", "Total assets", {y: tot_a(HIST_COLS[y]) for y in bs_years}, lambda col, prev: tot_a(col),
         bold=True, top=True)
    line("pay", "Trade and other payables", hist_link("bs", "Trade and other payables", bs_years),
         lambda col, prev: f"={a('pay_days')}/365*{c('cogs', col)}", driver="days of cost of sales")
    line("ocl", "Other current liabilities", hist_sum(ocl_items, bs_years),
         lambda col, prev: f"={a('ocl')}*{c('sales', col)}", driver="% of sales")
    line("debt", "Borrowings", hist_sum(debt_items, bs_years),
         lambda col, prev: f"={prev}{state['row']}+{a('debt_chg')}", driver="prior + net new borrowing")
    line("lease", "Lease liabilities", hist_sum(lease_items, bs_years),
         lambda col, prev: f"={prev}{state['row']}", driver="held flat")
    line("fs_l", "Financial Services liabilities (discontinued)",
         hist_sum(("Deposits from customers in the banking business", "Insurance contract liabilities"), bs_years),
         lambda col, prev: "=0", driver="spun off")
    line("oncl", "Other non-current liabilities",
         hist_sum(("Defined benefit liabilities", "Deferred tax liabilities",
                   "Participation and residual liabilities in the Pictures segment (non-current)",
                   "Other financial liabilities (non-current)", "Other non-current liabilities"), bs_years),
         lambda col, prev: f"={prev}{state['row']}", driver="held flat")
    liab_keys = ["pay", "ocl", "debt", "lease", "fs_l", "oncl"]
    tot_l = lambda col: "=" + "+".join(c(k, col) for k in liab_keys)  # noqa: E731
    line("tl", "Total liabilities", {y: tot_l(HIST_COLS[y]) for y in bs_years}, lambda col, prev: tot_l(col),
         top=True)
    R["eq"] = state["row"]
    state["row"] += 1
    line("tle", "Total liabilities and equity", {y: f"={c('tl', HIST_COLS[y])}+{c('eq', HIST_COLS[y])}" for y in bs_years},
         lambda col, prev: f"={c('tl', col)}+{c('eq', col)}", bold=True, top=True)
    line("check", "Balance check (assets less liabilities and equity; must be zero)",
         {y: f"={c('ta', HIST_COLS[y])}-{c('tle', HIST_COLS[y])}" for y in bs_years},
         lambda col, prev: f"=ROUND({c('ta', col)}-{c('tle', col)},0)")

    # ---------------- cash flow
    sec("CASH FLOW")
    cf_start = state["row"]
    R.update({k: cf_start + i for i, k in enumerate(
        ["cf_ni", "cf_da", "cf_content", "cf_rec", "cf_inv", "cf_oca", "cf_pay", "cf_ocl", "cfo",
         "cf_capex", "cf_debt", "cf_div", "cf_buy", "cf_net", "cf_open", "cf_close"])})

    # ---------------- now that every row is known, fill the deferred lines
    def at(key):
        state["row"] = R[key]

    at("fin_inc")
    line("fin_inc", "Financial income", hist_link("is", "Financial income"),
         lambda col, prev: f"={a('int_inc')}*{c('cash', prev)}", driver="% of opening cash")
    line("fin_exp", "Financial expenses", hist_link("is", "Financial expenses"),
         lambda col, prev: f"={a('int_exp')}*({c('debt', prev)}+{c('lease', prev)})", driver="% of opening debt")
    pbt = lambda col: f"={c('ebit', col)}+{c('fin_inc', col)}-{c('fin_exp', col)}"  # noqa: E731
    line("pbt", "Income before income taxes", {y: pbt(HIST_COLS[y]) for y in HIST_YEARS},
         lambda col, prev: pbt(col), top=True)
    line("taxes", "Income taxes", hist_link("is", "Income taxes"),
         lambda col, prev: f"={a('tax')}*{c('pbt', col)}", driver="% of pre-tax income")
    line("ni", "Net income from continuing operations",
         {y: f"={c('pbt', HIST_COLS[y])}-{c('taxes', HIST_COLS[y])}" for y in HIST_YEARS},
         lambda col, prev: f"={c('pbt', col)}-{c('taxes', col)}", bold=True, top=True)
    line("da", "Depreciation and amortization (memo)", hist_link("is", "Depreciation and amortization"),
         lambda col, prev: f"={a('da')}*{c('sales', col)}", driver="% of sales")

    at("cash")
    line("cash", "Cash and cash equivalents", hist_link("bs", "Cash and cash equivalents", bs_years),
         lambda col, prev: f"={c('cf_close', col)}", driver="from cash flow")
    at("lta")
    line("lta", "Operating long-term assets (PP&E, right-of-use, content, intangibles)",
         hist_sum(("Property, plant and equipment", "Right-of-use assets", "Content assets",
                   "Other intangible assets"), bs_years),
         lambda col, prev: f"={c('lta', prev)}-{c('cf_capex', col)}-{c('cf_content', col)}-{c('da', col)}",
         driver="prior + investment - D&A")
    at("eq")
    line("eq", "Total equity", hist_link("bs", "Total equity", bs_years),
         lambda col, prev: f"={c('eq', prev)}+{c('ni', col)}+{c('cf_div', col)}+{c('cf_buy', col)}",
         driver="prior + income - payouts")

    at("cf_ni")
    line("cf_ni", "Net income from continuing operations", None, lambda col, prev: f"={c('ni', col)}")
    line("cf_da", "Depreciation and amortization", None, lambda col, prev: f"={c('da', col)}")
    line("cf_content", "Investment in content assets", hist_link("cf", "Increase in content assets"),
         lambda col, prev: f"=-{a('content')}*{c('sales', col)}", driver="% of sales")
    for key, bs_key, label, sign in (("cf_rec", "rec", "(Increase) decrease in receivables", "asset"),
                                     ("cf_inv", "inv", "(Increase) decrease in inventories", "asset"),
                                     ("cf_oca", "oca", "(Increase) decrease in other current assets", "asset"),
                                     ("cf_pay", "pay", "Increase (decrease) in payables", "liab"),
                                     ("cf_ocl", "ocl", "Increase (decrease) in other current liabilities", "liab")):
        if sign == "asset":
            line(key, label, None, lambda col, prev, k=bs_key: f"={c(k, prev)}-{c(k, col)}")
        else:
            line(key, label, None, lambda col, prev, k=bs_key: f"={c(k, col)}-{c(k, prev)}")
    cfo_keys = ["cf_ni", "cf_da", "cf_content", "cf_rec", "cf_inv", "cf_oca", "cf_pay", "cf_ocl"]
    line("cfo", "Cash from operating activities",
         hist_link("cf", "Net cash from operating activities (continuing)"),
         lambda col, prev: "=" + "+".join(c(k, col) for k in cfo_keys), bold=True, top=True)
    line("cf_capex", "Capital expenditure",
         hist_link("cf", "Payments for property, plant and equipment and other intangible assets"),
         lambda col, prev: f"=-{a('capex')}*{c('sales', col)}", driver="% of sales")
    line("cf_debt", "Net new borrowing", None, lambda col, prev: f"={a('debt_chg')}")
    line("cf_div", "Dividends paid", hist_link("cf", "Dividends paid"),
         lambda col, prev: f"=-{a('payout')}*{c('ni', col)}", driver="% of net income")
    line("cf_buy", "Share repurchases", hist_link("cf", "Payments for purchases of treasury stock"),
         lambda col, prev: f"=-{a('buyback')}")
    line("cf_net", "Net change in cash", None,
         lambda col, prev: "=" + "+".join(c(k, col) for k in ("cfo", "cf_capex", "cf_debt", "cf_div", "cf_buy")),
         top=True)
    line("cf_open", "Cash at beginning of year", None, lambda col, prev: f"={c('cash', prev)}")
    line("cf_close", "Cash at end of year", hist_link("cf", "Cash and cash equivalents at end of year"),
         lambda col, prev: f"={c('cf_open', col)}+{c('cf_net', col)}", bold=True)

    # ---------------- DCF
    sec("FREE CASH FLOW AND DCF")
    line("d_ebit", "Operating income", None, lambda col, prev: f"={c('ebit', col)}")
    line("d_tax", "Less: tax on operating income", None, lambda col, prev: f"=-{a('tax')}*{c('ebit', col)}")
    line("nopat", "Net operating profit after tax", None,
         lambda col, prev: f"={c('d_ebit', col)}+{c('d_tax', col)}", top=True)
    line("d_da", "Plus: depreciation and amortization", None, lambda col, prev: f"={c('da', col)}")
    line("d_capex", "Less: capital expenditure", None, lambda col, prev: f"={c('cf_capex', col)}")
    line("d_content", "Less: investment in content assets", None, lambda col, prev: f"={c('cf_content', col)}")
    line("d_nwc", "Less: increase in working capital", None,
         lambda col, prev: "=" + "+".join(c(k, col) for k in ("cf_rec", "cf_inv", "cf_oca", "cf_pay", "cf_ocl")))
    line("fcf", "Free cash flow to the firm", None,
         lambda col, prev: "=" + "+".join(c(k, col) for k in ("nopat", "d_da", "d_capex", "d_content", "d_nwc")),
         bold=True, top=True)
    line("df", "Discount factor", None, lambda col, prev: f"=1/(1+{a('wacc')})^{col}$5", fmt=FACTOR,
         driver="1 / (1 + WACC)^year")
    line("pv", "Present value of free cash flow", None, lambda col, prev: f"={c('fcf', col)}*{c('df', col)}")

    state["row"] += 1
    section(ws, state["row"], "VALUATION (as of March 31, 2026)")
    state["row"] += 1

    def value(key, label, formula, fmt=MONEY, bold=False, note=""):
        r = state["row"]
        R[key] = r
        put(ws, f"A{r}", label, F_BOLD if bold else F_CALC)
        put(ws, f"C{r}", formula, link_font(formula), fmt, bold=bold)
        put(ws, f"D{r}", note, F_NOTE)
        state["row"] += 1

    v = lambda key: f"$C${R[key]}"  # noqa: E731
    value("v_wacc", "WACC", f"={a('wacc')}", "0.00%")
    value("v_tg", "Terminal growth rate", f"={a('tg')}", "0.00%")
    value("v_pv", "Present value of FY2026–FY2030 free cash flow", f"=SUM(F{R['pv']}:J{R['pv']})")
    value("v_tv", "Terminal value at FY2030", f"=J{R['fcf']}*(1+{v('v_tg')})/({v('v_wacc')}-{v('v_tg')})",
          note="Gordon growth: FCF x (1 + g) / (WACC - g)")
    value("v_pvtv", "Present value of terminal value", f"={v('v_tv')}*J{R['df']}")
    value("v_ev", "Enterprise value", f"={v('v_pv')}+{v('v_pvtv')}", bold=True)
    value("v_cash", "Plus: cash and cash equivalents", f"=E{R['cash']}")
    eq_inv = "+".join(last(i, "bs") for i in ("Investments accounted for using the equity method",
                                             "Other financial assets (current)",
                                             "Other financial assets (non-current)"))
    value("v_inv", "Plus: equity-method investments and other financial assets", f"={eq_inv}",
          note="Book value; their income is excluded from operating income")
    value("v_debt", "Less: borrowings", f"=-E{R['debt']}")
    value("v_lease", "Less: lease liabilities", f"=-E{R['lease']}")
    value("v_pension", "Less: defined benefit liabilities", f"=-{last('Defined benefit liabilities', 'bs')}")
    value("v_nci", "Less: noncontrolling interests", f"=-{last('Noncontrolling interests', 'bs')}",
          note="Book value")
    value("v_bridge", "Net non-operating items",
          "=" + "+".join(v(k) for k in ("v_cash", "v_inv", "v_debt", "v_lease", "v_pension", "v_nci")))
    value("v_eq", "Equity value", f"={v('v_ev')}+{v('v_bridge')}", bold=True)
    value("v_ps", "Value per share (¥)", f"={v('v_eq')}*1000000/{a('shares')}", YEN, bold=True)
    value("v_adr", "Value per ADR (US$)", f"={v('v_ps')}/{a('fx')}", USD, bold=True)
    value("v_mkt", "Market price per share (¥)", f"={a('price_jpy')}", YEN)
    value("v_up", "Value versus market price", f"={v('v_ps')}/{v('v_mkt')}-1", "0.0%;-0.0%", bold=True)
    value("v_tvshare", "Terminal value as share of enterprise value", f"={v('v_pvtv')}/{v('v_ev')}", "0.0%")
    value("v_evebitda", "Implied EV / FY2025 EBITDA", f"={v('v_ev')}/E{R['ebitda']}", "0.0x")

    ws.column_dimensions["A"].width = 62
    ws.column_dimensions["B"].width = 26
    for col in "CDEFGHIJ":
        ws.column_dimensions[col].width = 13.5
    ws.freeze_panes = "C6"
    return R


ROWS = {name: build_scenario(name) for name in SCENARIOS}

# ================================================================ Scenarios
sc = wb.create_sheet("Scenarios")
put(sc, "A1", "Scenario comparison and sensitivity", F_TITLE)
put(sc, "A2", "Every figure links to the Base, Upside and Downside sheets; change an assumption and this page updates.",
    F_NOTE)
header_row(sc, 4, ["¥ millions unless stated", "Base", "Upside", "Downside"])
compare = [
    ("Growth adjustment (points per year)", lambda n: f"={A('g_adj', SCENARIOS[n])}", "0.0%;-0.0%;-"),
    ("Cost of sales (% of sales)", lambda n: f"={A('cogs', SCENARIOS[n])}", PCT),
    ("Terminal growth rate", lambda n: f"={A('tg', SCENARIOS[n])}", PCT),
    ("FY2030 sales", lambda n: f"={n}!J{ROWS[n]['sales']}", MONEY),
    ("Sales CAGR, FY2025–FY2030", lambda n: f"=({n}!J{ROWS[n]['sales']}/{n}!E{ROWS[n]['sales']})^(1/5)-1", PCT),
    ("FY2030 operating income", lambda n: f"={n}!J{ROWS[n]['ebit']}", MONEY),
    ("FY2030 operating margin", lambda n: f"={n}!J{ROWS[n]['ebit_m']}", PCT),
    ("Free cash flow, FY2026–FY2030 total", lambda n: f"=SUM({n}!F{ROWS[n]['fcf']}:J{ROWS[n]['fcf']})", MONEY),
    ("Enterprise value", lambda n: f"={n}!C{ROWS[n]['v_ev']}", MONEY),
    ("Equity value", lambda n: f"={n}!C{ROWS[n]['v_eq']}", MONEY),
    ("Value per share (¥)", lambda n: f"={n}!C{ROWS[n]['v_ps']}", YEN),
    ("Value per ADR (US$)", lambda n: f"={n}!C{ROWS[n]['v_adr']}", USD),
    ("Market price per share (¥)", lambda n: f"={n}!C{ROWS[n]['v_mkt']}", YEN),
    ("Value versus market price", lambda n: f"={n}!C{ROWS[n]['v_up']}", "0.0%;-0.0%"),
    ("Terminal value as share of enterprise value", lambda n: f"={n}!C{ROWS[n]['v_tvshare']}", "0.0%"),
    ("Balance check, all forecast years (must be zero)",
     lambda n: f"=SUM({n}!F{ROWS[n]['check']}:J{ROWS[n]['check']})", MONEY),
]
SC_ROW = {}
for i, (label, fn, fmt) in enumerate(compare, start=5):
    put(sc, f"A{i}", label, F_BOLD if "per share" in label or "versus" in label else F_CALC)
    for name, col in zip(SCENARIOS, "BCD"):
        formula = fn(name)
        put(sc, f"{col}{i}", formula, link_font(formula), fmt)
    SC_ROW[label] = i

sens = 5 + len(compare) + 2
put(sc, f"A{sens}", "Sensitivity: Base-case value per share (¥) to WACC and terminal growth", F_BOLD)
put(sc, f"A{sens + 1}", "Rows: WACC. Columns: terminal growth. The centre cell equals the Base-case value per share.",
    F_NOTE)
head = sens + 2
base = ROWS["Base"]
put(sc, f"A{head}", "WACC  \\  terminal growth", F_HEAD, fill=FILL_HEAD)
g_steps = [-0.01, -0.005, 0, 0.005, 0.01]
w_steps = [-0.02, -0.01, 0, 0.01, 0.02]
for j, step in enumerate(g_steps):
    col = "BCDEF"[j]
    put(sc, f"{col}{head}", f"={A('tg')}{step:+}", F_HEAD, "0.0%", FILL_HEAD, align=Alignment(horizontal="center"))
fcf_rng = f"Base!$F${base['fcf']}:$J${base['fcf']}"
yr_rng = "Base!$F$5:$J$5"
for i, step in enumerate(w_steps):
    r = head + 1 + i
    put(sc, f"A{r}", f"={A('wacc')}{step:+}", F_BOLD, "0.0%", align=Alignment(horizontal="left"))
    for j in range(len(g_steps)):
        col = "BCDEF"[j]
        w, g = f"$A{r}", f"{col}${head}"
        formula = (f"=(SUMPRODUCT({fcf_rng}/(1+{w})^{yr_rng})"
                   f"+Base!$J${base['fcf']}*(1+{g})/({w}-{g})/(1+{w})^5"
                   f"+Base!$C${base['v_bridge']})*1000000/{A('shares')}")
        put(sc, f"{col}{r}", formula, F_CALC, YEN, FILL_KEY if (i, j) == (2, 2) else None)

chart = head + len(w_steps) + 3
put(sc, f"A{chart}", "Chart data (feeds the Dashboard)", F_BOLD)
years = [y + "A" for y in HIST_YEARS] + [y + "E" for y in FCST_YEARS]
header_row(sc, chart + 1, ["¥ trillions"] + years)
series = [("Sales — Base", "Base", "sales"), ("Sales — Upside", "Upside", "sales"),
          ("Sales — Downside", "Downside", "sales"), ("Operating income — Base", "Base", "ebit"),
          ("Free cash flow — Base", "Base", "fcf")]
CH = {}
for i, (label, name, key) in enumerate(series, start=chart + 2):
    put(sc, f"A{i}", label)
    for j, col in enumerate("CDEFGHIJ"):
        if key == "fcf" and j < 3:
            continue
        put(sc, f"{chr(66 + j)}{i}", f"={name}!{col}{ROWS[name][key]}/1000000", F_CALC, "0.00")
    CH[label] = i
vrow = chart + 2 + len(series) + 1
header_row(sc, vrow, ["Value per share (¥)", "Base", "Upside", "Downside", "Market price"])
put(sc, f"A{vrow + 1}", "Value per share (¥)")
for name, col in zip(SCENARIOS, "BCD"):
    put(sc, f"{col}{vrow + 1}", f"={name}!C{ROWS[name]['v_ps']}", F_LINK, YEN)
put(sc, f"E{vrow + 1}", f"={A('price_jpy')}", F_LINK, YEN)
sc.column_dimensions["A"].width = 52
for col in "BCDEFGHI":
    sc.column_dimensions[col].width = 14

# ================================================================ Dashboard
dash = wb.create_sheet("Dashboard")
put(dash, "A1", "Sony Group — valuation dashboard", F_TITLE)
put(dash, "A2", "All figures are live links to the model. ¥ millions unless stated.", F_NOTE)
tiles = [
    ("Base value per share", f"=Base!C{base['v_ps']}", YEN),
    ("Market price per share", f"=Base!C{base['v_mkt']}", YEN),
    ("Base value vs. market", f"=Base!C{base['v_up']}", "0.0%;-0.0%"),
    ("Enterprise value (¥ tn)", f"=Base!C{base['v_ev']}/1000000", "0.0"),
    ("WACC", f"={A('wacc')}", "0.0%"),
    ("Terminal value share of EV", f"=Base!C{base['v_tvshare']}", "0.0%"),
]
for i, (label, formula, fmt) in enumerate(tiles):
    col = "ACEGIK"[i]
    nxt = chr(ord(col) + 1)
    dash.merge_cells(f"{col}4:{nxt}4")
    dash.merge_cells(f"{col}5:{nxt}5")
    put(dash, f"{col}4", label, F_HEAD, fill=FILL_HEAD, align=Alignment(horizontal="center"))
    dash[f"{nxt}4"].fill = FILL_HEAD
    put(dash, f"{col}5", formula, Font(name=FONT, size=16, bold=True), fmt, FILL_SECTION,
        align=Alignment(horizontal="center", vertical="center"))
    dash[f"{nxt}5"].fill = FILL_SECTION
dash.row_dimensions[5].height = 34
for col in "ABCDEFGHIJKL":
    dash.column_dimensions[col].width = 13

cats = Reference(sc, min_col=2, max_col=9, min_row=chart + 1)


def line_chart(title, labels, anchor, y_title="¥ trillions"):
    ch = LineChart()
    ch.title, ch.height, ch.width = title, 7.5, 15.5
    ch.y_axis.title = y_title
    for label in labels:
        ch.add_data(Reference(sc, min_col=1, max_col=9, min_row=CH[label]), from_rows=True, titles_from_data=True)
    ch.set_categories(cats)
    dash.add_chart(ch, anchor)


line_chart("Sales by scenario", ["Sales — Base", "Sales — Upside", "Sales — Downside"], "A7")
line_chart("Operating income — Base case", ["Operating income — Base"], "G7")
bar = BarChart()
bar.title, bar.height, bar.width = "Free cash flow — Base case", 7.5, 15.5
bar.y_axis.title = "¥ trillions"
bar.add_data(Reference(sc, min_col=1, max_col=9, min_row=CH["Free cash flow — Base"]), from_rows=True,
             titles_from_data=True)
bar.set_categories(cats)
dash.add_chart(bar, "A23")
val = BarChart()
val.title, val.height, val.width = "Value per share vs. market price (¥)", 7.5, 15.5
val.add_data(Reference(sc, min_col=1, max_col=5, min_row=vrow + 1), from_rows=True, titles_from_data=True)
val.set_categories(Reference(sc, min_col=2, max_col=5, min_row=vrow))
val.legend = None
dash.add_chart(val, "G23")

# ================================================================ Cover
cover = wb.create_sheet("Cover", 0)
put(cover, "A1", "Sony Group Corporation — three-statement model and DCF valuation", F_TITLE)
put(cover, "A2", "Built by Alia Alami from Sony's Form 20-F for FY2025 (year ended March 31, 2026). "
                 "Educational portfolio project, not investment advice.", F_NOTE)
guide = [
    ("How the model flows", None),
    ("1. Historical", "Reported segment sales, income statement, balance sheet and cash flow from the SEC filing."),
    ("2. Assumptions", "Every driver in one place, with a Base, Upside and Downside column and the source of each number."),
    ("3. Base / Upside / Downside", "Revenue build -> income statement -> balance sheet -> cash flow -> free cash flow -> DCF."),
    ("4. Scenarios", "Side-by-side scenario results and a WACC x terminal-growth sensitivity table."),
    ("5. Dashboard", "Headline valuation and charts."),
    ("", None),
    ("Colour code", None),
    ("Blue text", "Hard-coded input (reported figure or assumption)."),
    ("Black text", "Formula."),
    ("Green text", "Direct link to another sheet."),
    ("Yellow fill", "Key assumption: change these first to test the valuation."),
    ("Grey fill", "Forecast period."),
    ("", None),
    ("Integrity checks", None),
    ("Balance sheet", "Assets equal liabilities plus equity in every forecast year (Scenarios sheet, 'Balance check')."),
    ("Cash", "Balance-sheet cash is the closing cash from the cash-flow statement."),
    ("", None),
    ("Simplifications to know about", None),
    ("Financial Services", "Spun off in FY2025 and presented as a discontinued operation, so it is excluded from the forecast and the valuation."),
    ("Long-term assets", "PP&E, right-of-use, content and intangible assets are forecast as one line: prior + investment - D&A."),
    ("Leases and debt", "Held flat; lease liabilities are treated as debt in the equity bridge."),
    ("Other items", "Other operating items, equity-method income, goodwill changes and currency effects are assumed nil."),
]
for i, (left, right) in enumerate(guide, start=4):
    if right is None and left:
        section(cover, i, left, "B")
    else:
        put(cover, f"A{i}", left, F_BOLD)
        put(cover, f"B{i}", right)
for sample, font, fill in ((12, F_INPUT, None), (13, F_CALC, None), (14, F_LINK, None), (15, F_CALC, FILL_KEY),
                           (16, F_CALC, FILL_FCST)):
    cover[f"A{sample}"].font = Font(name=FONT, size=10, bold=True, color=font.color)
    if fill:
        cover[f"A{sample}"].fill = fill
cover.column_dimensions["A"].width = 30
cover.column_dimensions["B"].width = 110

asm["C5"].comment = Comment("Starting growth rates are written by forecast_revenue.py. "
                            "Re-run it, then build_model.py, to refresh them.", "Model")
wb.move_sheet("Dashboard", offset=-(len(wb.sheetnames) - 2))
for ws in wb.worksheets:
    ws.sheet_view.showGridLines = False
wb.save(OUT)
print(f"Wrote {OUT.name}: {', '.join(wb.sheetnames)}")
