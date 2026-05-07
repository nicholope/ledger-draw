#!/usr/bin/env python3
"""
TN-1 Draw Package Generator
Pulls data from Ledger CLI and generates a draw request package via Claude.
"""

import subprocess
import anthropic
import datetime
import os

# ── Config ────────────────────────────────────────────────────────────────────
JOURNAL = "/Users/nick/.openclaw/workspace/skills/ledger-draw/references/tn1_journal.ledger"
DRAW_START = "2026-04-01"
DRAW_END = "2026-05-07"
DRAW_NUMBER = 3
OUTPUT_DIR = "/Users/nick/.openclaw/workspace/skills/ledger-draw"

# ── Ledger Query Helper ───────────────────────────────────────────────────────
def run_ledger(args):
    cmd = ["ledger", "-f", JOURNAL] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

# ── Pull All Data from Ledger ─────────────────────────────────────────────────
def gather_data():
    print("📊 Querying Ledger CLI...")

    data = {
        "draw_period_balance": run_ledger([
            "balance", "Expenses",
            "--begin", DRAW_START,
            "--end", DRAW_END,
            "--depth", "3"
        ]),
        "draw_period_register": run_ledger([
            "register", "Expenses",
            "--begin", DRAW_START,
            "--end", DRAW_END
        ]),
        "project_to_date_balance": run_ledger([
            "balance", "Expenses", "--depth", "3"
        ]),
        "cash_balance": run_ledger([
            "balance", "Assets:TN1:ConstructionAccount"
        ]),
        "loan_balance": run_ledger([
            "balance", "Liabilities:TN1:ConstructionLoan"
        ]),
        "contingency_balance": run_ledger([
            "balance", "Expenses:TN1:Contingency"
        ]),
    }

    print("✅ Ledger data gathered.\n")
    return data

# ── Build Claude Prompt ───────────────────────────────────────────────────────
def build_prompt(data):
    return f"""You are an expert real estate construction accountant preparing a lender draw request package for a multifamily development project.

Below is the financial data extracted from the project's Ledger CLI accounting journal for TN-1 (Culdesac Tempe Phase 2).

PROJECT DETAILS:
- Property: TN-1 (Culdesac Tempe Phase 2)
- Developer: Culdesac
- Lender: Western Alliance Bank
- Total Loan Facility: $4,200,000
- Draw Number: {DRAW_NUMBER}
- Draw Period: {DRAW_START} to {DRAW_END}

DRAW PERIOD COSTS (what we are requesting):
{data['draw_period_balance']}

DRAW PERIOD TRANSACTION DETAIL:
{data['draw_period_register']}

PROJECT-TO-DATE TOTALS:
{data['project_to_date_balance']}

CURRENT CASH POSITION:
{data['cash_balance']}

TOTAL LOAN DRAWN TO DATE:
{data['loan_balance']}

CONTINGENCY USED TO DATE:
{data['contingency_balance']}

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
"""

# ── Call Claude ───────────────────────────────────────────────────────────────
def call_claude(prompt):
    print("🤖 Sending to Claude...")
    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )

    print("✅ Claude response received.\n")
    return message.content[0].text

# ── Save Output ───────────────────────────────────────────────────────────────
def save_output(content):
    today = datetime.date.today().strftime("%Y-%m-%d")
    filename = f"draw_{DRAW_NUMBER}_{today}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w") as f:
        f.write(content)

    print(f"📄 Draw package saved: {filepath}")
    return filepath

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print(f"  TN-1 Draw #{DRAW_NUMBER} Package Generator")
    print(f"  Period: {DRAW_START} to {DRAW_END}")
    print("=" * 60 + "\n")

    data = gather_data()
    prompt = build_prompt(data)
    draw_package = call_claude(prompt)
    filepath = save_output(draw_package)

    print("\n" + "=" * 60)
    print("  DRAW PACKAGE PREVIEW")
    print("=" * 60)
    print(draw_package[:2000] + "\n...[truncated — see full file]" if len(draw_package) > 2000 else draw_package)
    print(f"\n✅ Full package: {filepath}")

if __name__ == "__main__":
    main()
