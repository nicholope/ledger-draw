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
