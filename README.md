# ledger-draw

**AI-powered construction draw package generator for real estate accounting.**

Uses [Ledger CLI](https://ledger-cli.org/) to extract project costs from a plain-text journal, then sends the data to [Claude](https://anthropic.com) to generate a complete, lender-ready draw request package in markdown — including cover summary, budget vs. actual schedule, transaction detail, variance analysis, and lender checklist.

Built for property developers and accountants managing construction loan draws.

---

## Demo Output

See [`references/sample_output.md`](references/sample_output.md) for a full example draw package generated from the included TN-1 sample journal.

---

## What It Does

1. Queries your Ledger CLI journal for costs in the draw period
2. Extracts project-to-date totals, cash position, and loan balance
3. Sends all data to Claude with a structured accounting prompt
4. Outputs a professional markdown draw package ready for lender submission

### Output Includes

- **Cover Summary** — draw number, period, amount requested, loan availability
- **Budget vs. Actual Schedule** — by cost category (hard costs, soft costs, contingency)
- **Transaction Detail** — every invoice in the draw period with vendor and amount
- **Variance Analysis** — Claude-written plain English explanation of notable items
- **Lender Checklist** — required documentation flagged per line item
- **Certification Statement** — standard draw certification language

---

## Requirements

- [Ledger CLI](https://ledger-cli.org/) — `brew install ledger`
- Python 3.8+
- Anthropic API key — [get one here](https://console.anthropic.com/)
- Anthropic Python SDK — `pip3 install anthropic`

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/nicholope/ledger-draw.git
cd ledger-draw
```

### 2. Install dependencies
```bash
brew install ledger
pip3 install anthropic
```

### 3. Set your Anthropic API key
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

Add to `~/.zshrc` for persistence:
```bash
echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.zshrc && source ~/.zshrc
```

> ⚠️ Never commit your API key. See `.env.example` for the expected variable name.

### 4. Configure your journal and draw period

Edit `scripts/prepare_draw.py` and update these variables:

```python
JOURNAL     = "/path/to/your/journal.ledger"
DRAW_START  = "2026-04-01"
DRAW_END    = "2026-05-07"
DRAW_NUMBER = 3
OUTPUT_DIR  = "/path/to/output/folder"
```

---

## Usage

### Run the draw package generator
```bash
python3 scripts/prepare_draw.py
```

Output is saved as `draw_{number}_{date}.md` in your configured `OUTPUT_DIR`.

### Try it with the sample journal
The repo includes a complete sample journal (`references/tn1_journal.ledger`) based on a fictional multifamily construction project. Run it out of the box to see the tool in action.

### Useful Ledger CLI queries

```bash
# Set journal path shortcut
export J="references/tn1_journal.ledger"

# Full project balance summary
ledger -f $J balance Expenses --depth 2

# Draw period costs only
ledger -f $J balance Expenses --begin 2026-04-01 --end 2026-05-07 --depth 3

# Draw period transaction detail
ledger -f $J register Expenses --begin 2026-04-01 --end 2026-05-07

# Monthly burn rate
ledger -f $J register Expenses --monthly --collapse

# Vendor spend history
ledger -f $J register payee "Vendor Name"

# Contingency consumed
ledger -f $J balance Expenses:TN1:Contingency

# Cash balance
ledger -f $J balance Assets
```

---

## Journal Structure

The skill expects a standard double-entry Ledger journal with accounts organized as:

```
Expenses:ProjectName:HardCosts:SiteWork
Expenses:ProjectName:HardCosts:Concrete
Expenses:ProjectName:HardCosts:Framing
Expenses:ProjectName:HardCosts:MEP:Plumbing
Expenses:ProjectName:HardCosts:MEP:Electrical
Expenses:ProjectName:HardCosts:MEP:HVAC
Expenses:ProjectName:HardCosts:Finishes:Drywall
Expenses:ProjectName:HardCosts:Landscaping
Expenses:ProjectName:SoftCosts:Architecture
Expenses:ProjectName:SoftCosts:Engineering
Expenses:ProjectName:SoftCosts:Permits
Expenses:ProjectName:SoftCosts:PMFee
Expenses:ProjectName:SoftCosts:Insurance
Expenses:ProjectName:Contingency:ChangeOrders
Assets:ProjectName:ConstructionAccount
Liabilities:ProjectName:ConstructionLoan
Equity:ProjectName:OwnerEquity
```

See [`references/tn1_journal.ledger`](references/tn1_journal.ledger) for a complete working example.

---

## File Structure

```
ledger-draw/
├── README.md                         # This file
├── SKILL.md                          # OpenClaw skill definition
├── .gitignore                        # Excludes .env files
├── .env.example                      # API key template (safe to commit)
├── scripts/
│   ├── prepare_draw.py               # Main draw package generator
│   └── query_draw_costs.sh           # Standalone Ledger query script
└── references/
    ├── tn1_journal.ledger            # Sample construction project journal
    ├── prompts.md                    # Claude prompt templates
    ├── demo_commands.md              # Ledger CLI cheat sheet
    └── sample_output.md             # Example draw package output
```

---

## Use Cases

- **Construction draw prep** — automate the most time-consuming part of a draw request
- **Variance reporting** — Claude narrates budget vs. actual in plain English
- **Lender reporting** — consistent, professional format every draw cycle
- **Audit trail** — plain-text journal is fully version-controllable in git

---

## Author

Built by [Nick Lopez](https://github.com/nicholope) as a real estate accounting automation skill.

Inspired by the AI tooling requirements at modern real estate operators — specifically the need to leverage Claude and MCP to accelerate finance workflows like reconciliation, draw prep, reporting, and variance analysis.

---

## License

MIT
