# GN-1 Ledger CLI — Demo Command Cheat Sheet

## Setup (run once)
```bash
export J="/Users/nick/.openclaw/workspace/skills/ledger-draw/references/tn1_journal.ledger"
```

---

## 1. FULL PROJECT BALANCE SUMMARY
```bash
ledger -f $J balance Expenses --depth 3
```
**What it shows:** All costs grouped by Hard Costs, Soft Costs, Contingency
**Say:** "This is the 30,000-foot view — total spend by major category since day one."

---

## 2. DRILL DOWN INTO HARD COSTS
```bash
ledger -f $J balance Expenses:TN1:HardCosts --depth 4
```
**What it shows:** Site work, concrete, framing, MEP, finishes, landscaping broken out
**Say:** "Framing is our biggest hard cost so far at $331K — typical for this phase of construction."

---

## 3. DRAW PERIOD COSTS (Current Draw Window)
```bash
ledger -f $J balance Expenses --begin 2026-04-01 --end 2026-05-07 --depth 3
```
**What it shows:** Only costs incurred in the current draw period
**Say:** "This is what we're submitting for Draw #3 — $348,400 in costs incurred since April 1st."

---

## 4. DRAW PERIOD TRANSACTION DETAIL
```bash
ledger -f $J register Expenses --begin 2026-04-01 --end 2026-05-07
```
**What it shows:** Every invoice in the draw period with running total
**Say:** "This is the supporting schedule — each line is a vendor invoice we need to attach to the draw package."

---

## 5. VENDOR SPEND HISTORY (Pick Any Vendor)
```bash
ledger -f $J register payee Mesa
```
**What it shows:** Every payment to Mesa Concrete across the whole project
**Say:** "Lenders want to see vendor history to spot overbilling. One command surfaces everything."

---

## 6. CASH POSITION
```bash
ledger -f $J balance Assets:TN1:ConstructionAccount
```
**What it shows:** Current bank balance in the construction account
**Say:** "We have $938K in the construction account. The draw request will tell us when we need to pull the next advance."

---

## 7. LOAN BALANCE
```bash
ledger -f $J balance Liabilities:TN1:ConstructionLoan
```
**What it shows:** Total loan drawn to date ($1.4M)
**Say:** "We've drawn $1.4M of the $4.2M loan facility. Equity went in first, then loan dollars followed."

---

## 8. CONTINGENCY CONSUMPTION
```bash
ledger -f $J balance Expenses:TN1:Contingency
```
**What it shows:** Total change orders / contingency used ($37,000)
**Say:** "This tracks how much of our contingency budget is consumed. $37K out of a typical 5-10% contingency reserve. Important to watch closely — once it's gone, you're in trouble."

---

## 9. MONTHLY BURN RATE
```bash
ledger -f $J register Expenses --monthly --collapse
```
**What it shows:** Total spend per month across the project
**Say:** "This gives us the burn rate by month — essential for cash flow forecasting and knowing when to pull the next draw."

---

## 10. SOFT COSTS BREAKDOWN
```bash
ledger -f $J balance Expenses:TN1:SoftCosts --depth 4
```
**What it shows:** Architecture, engineering, permits, PM fees, insurance
**Say:** "Soft costs are often overlooked but they're draw-eligible. Insurance and PM fees hit every month."

---

## 11. FULL REGISTER (Every Transaction)
```bash
ledger -f $J register
```
**What it shows:** Complete transaction history — every debit and credit
**Say:** "Plain text, fully auditable. Every transaction is here, timestamped, with a vendor name and invoice number."

---

## 12. RUN THE FULL DRAW QUERY SCRIPT
```bash
bash /Users/nick/.openclaw/workspace/skills/ledger-draw/scripts/query_draw_costs.sh
```
**What it shows:** Full draw package data output in one command
**Say:** "This single script generates everything I need to start building the draw package. Claude takes it from here."

---

## KEY NUMBERS TO MEMORIZE FOR DEMO
| Metric | Value |
|---|---|
| Total budget | $4,200,000 |
| Costs to date | $1,661,950 (40% of budget) |
| Draw #3 request | $348,400 |
| Cash on hand | $938,050 |
| Loan drawn to date | $1,400,000 |
| Contingency used | $37,000 |
| Lender | Western Alliance Bank |
| Property | GN-1 (Glendale Neighborhood Phase 2) |
