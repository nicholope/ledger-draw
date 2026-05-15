#!/bin/bash
# ============================================================
# GN-1 Draw Package — Ledger CLI Query Scripts
# Usage: bash query_draw_costs.sh
# ============================================================

JOURNAL="/Users/nick/.openclaw/workspace/skills/ledger-draw/references/tn1_journal.ledger"
DRAW_START="2026-04-01"
DRAW_END="2026-05-07"

echo "============================================================"
echo " GN-1 DRAW #3 — Period: $DRAW_START to $DRAW_END"
echo "============================================================"

echo ""
echo "--- DRAW PERIOD COSTS BY CATEGORY ---"
ledger -f "$JOURNAL" balance Expenses --begin "$DRAW_START" --end "$DRAW_END" --depth 3

echo ""
echo "--- DRAW PERIOD TRANSACTION DETAIL ---"
ledger -f "$JOURNAL" register Expenses --begin "$DRAW_START" --end "$DRAW_END"

echo ""
echo "--- PROJECT-TO-DATE TOTALS BY CATEGORY ---"
ledger -f "$JOURNAL" balance Expenses --depth 3

echo ""
echo "--- CURRENT CASH BALANCE ---"
ledger -f "$JOURNAL" balance Assets:TN1:ConstructionAccount

echo ""
echo "--- TOTAL LOAN DRAWN TO DATE ---"
ledger -f "$JOURNAL" balance Liabilities:TN1:ConstructionLoan
