# Claude Prompt Templates — GN-1 Draw Package

## Main Draw Package Prompt

```
You are an expert real estate construction accountant preparing a lender draw request package for a multifamily development project.

Below is the financial data extracted from the project's Ledger CLI accounting journal for GN-1 (Glendale Neighborhood Phase 2).

PROJECT DETAILS:
- Property: GN-1 (Glendale Neighborhood Phase 2)
- Developer: Bien Arizonense
- Lender: Western Alliance Bank
- Total Loan Facility: $4,200,000
- Draw Number: 3
- Draw Period: April 1, 2026 – May 7, 2026

DRAW PERIOD COSTS (what we are requesting):
{draw_period_balance}

DRAW PERIOD TRANSACTION DETAIL:
{draw_period_register}

PROJECT-TO-DATE TOTALS:
{project_to_date_balance}

CURRENT CASH POSITION:
{cash_balance}

TOTAL LOAN DRAWN TO DATE:
{loan_balance}

CONTINGENCY USED TO DATE:
{contingency_balance}

---

## CRITICAL MATHEMATICAL REQUIREMENTS

ALL financial tables in the output MUST have exact arithmetic integrity. This is non-negotiable for lender acceptance.

### FOOTING VALIDATION (Before Output)

1. **Row Totals:** Every row must sum correctly
   - All line-item amounts in a row must equal the row subtotal
   - Example: $100 + $200 + $150 = $450 (TOTAL row)

2. **Column Totals:** Every column must sum correctly
   - All rows in a column must equal the column subtotal
   - Example: Budget column: $1,000 + $2,000 + $3,000 = $6,000 (TOTAL row)

3. **Remaining Calculation Accuracy:** Budget - Spent = Remaining (exactly)
   - Do NOT round or estimate
   - If Budget: $120,000 and Spent: $12,500, then Remaining MUST be $107,500
   - Any rounding discrepancies must be corrected

4. **Cross-Check All Totals:**
   - HARD COSTS total row must equal sum of all hard cost line items
   - SOFT COSTS total row must equal sum of all soft cost line items
   - CONTINGENCY total row must equal sum of all contingency line items
   - PROJECT TOTAL must equal: Hard Costs + Soft Costs + Contingency totals

### TABLE VALIDATION CHECKLIST

For each "Budget vs. Actual Schedule" table, verify BEFORE including in output:

✓ **Spent To Date column:** Sum of all category line items = Subtotal
✓ **This Draw column:** Sum of all category line items = Subtotal  
✓ **Remaining column:** Each row calculates as (Budget - Spent To Date)
✓ **Column cross-totals:** Budget column total + Spent total + This Draw total + Remaining total all reconcile
✓ **Grand total:** Sum of category totals = PROJECT SUMMARY total

### IF ANY TABLE DOES NOT FOOT:

**STOP. DO NOT OUTPUT THE DOCUMENT.**

1. Identify the failing table
2. Recalculate every cell independently
3. Verify sums by adding manually (not relying on prior calculations)
4. Only include the table in final output when 100% arithmetically correct
5. If you cannot reconcile, explain the discrepancy before output

### EXAMPLES

**CORRECT TABLE (all arithmetic exact):**
```
| Category | Budget Allocated | Spent to Date | This Draw | Remaining |
|----------|------------------|----------------|-----------|----------|
| MEP      | $350,000.00      | $112,500.00    | $112,500   | $237,500 |
| Drywall  | $200,000.00      | $44,300.00     | $44,300    | $155,700 |
| TOTAL    | $550,000.00      | $156,800.00    | $156,800   | $393,200 |
```
Verification: $112,500 + $44,300 = $156,800 ✓ | $237,500 + $155,700 = $393,200 ✓

**INCORRECT TABLE (rejected, do not output):**
```
| Category | Budget Allocated | Spent to Date | This Draw | Remaining |
|----------|------------------|----------------|-----------|----------|
| MEP      | $350,000.00      | $112,500.00    | $112,500   | $237,500 |
| Drywall  | $200,000.00      | $44,300.00     | $44,300    | $155,700 |
| TOTAL    | $550,000.00      | $156,800.00    | $156,800   | $392,100 | ← WRONG ($237,500 + $155,700 = $393,200, not $392,100)
```

**NO EXCEPTIONS.** Lender draw requests with mathematical errors will be rejected outright and damage borrower credibility.

---

Please generate a complete, professional draw request package in markdown format with the following sections:

1. DRAW REQUEST COVER SUMMARY
   - Draw number, period, property, lender
   - Total amount requested this draw
   - Total loan drawn to date
   - Remaining loan availability

2. BUDGET VS. ACTUAL SCHEDULE
   - Show each cost category (Hard Costs, Soft Costs, Contingency)
   - Include: Budget Allocated | Spent To Date | This Draw | Remaining
   - Use realistic budget allocations based on the data provided

3. TRANSACTION DETAIL — THIS DRAW PERIOD
   - List every invoice/transaction in the draw period
   - Include: Date | Vendor | Description | Amount
   - Subtotal by category

4. VARIANCE ANALYSIS
   - Identify any notable items (large invoices, change orders, unusual spend)
   - Write 2-3 sentences of plain English explanation for each
   - Flag any items that may require additional lender documentation

5. LENDER CHECKLIST
   - List documentation required for this draw (invoices, lien waivers, inspection cert, etc.)
   - Mark each as [REQUIRED] or [IF APPLICABLE]
   - Add a note for the change orders explaining they need signed CO documentation

6. CERTIFICATION STATEMENT
   - Standard draw certification language stating costs are accurate and draw-eligible

Keep the tone professional and concise. Format all dollar amounts with commas and 2 decimal places.
```
