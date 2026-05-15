#!/usr/bin/env python3
"""
Draw Package Table Validation Script

Validates all financial tables in a draw request package for exact arithmetic integrity.
Ensures row totals, column totals, and remaining calculations are correct.

Usage:
  python3 validate_draw_package.py <markdown_file>
  python3 validate_draw_package.py ../references/sample_output.md

Exit code 0: All tables valid
Exit code 1: One or more tables have math errors
"""

import sys
import re
from typing import List, Dict, Tuple
from decimal import Decimal, InvalidOperation

def extract_currency(text: str) -> Decimal:
    """Extract decimal value from currency string."""
    # Remove currency symbols, commas, parentheses
    clean = text.replace('$', '').replace(',', '').strip()
    
    # Handle negative values in parentheses
    is_negative = clean.startswith('(') and clean.endswith(')')
    if is_negative:
        clean = clean[1:-1]
    
    try:
        value = Decimal(clean)
        return -value if is_negative else value
    except (InvalidOperation, ValueError):
        return None

def format_currency(value: Decimal) -> str:
    """Format decimal as currency string."""
    if value is None:
        return "N/A"
    
    is_negative = value < 0
    abs_value = abs(value)
    
    # Format with 2 decimal places and commas
    formatted = f"${abs_value:,.2f}"
    
    if is_negative:
        formatted = f"({formatted})"
    
    return formatted

def parse_markdown_table(table_text: str) -> Tuple[List[str], List[List[str]]]:
    """Parse markdown table into headers and rows."""
    lines = table_text.strip().split('\n')
    
    if len(lines) < 3:
        return None, None
    
    # Parse header
    headers = [h.strip() for h in lines[0].split('|')[1:-1]]
    
    # Skip separator line (line 1)
    
    # Parse data rows
    rows = []
    for line in lines[2:]:
        if not line.strip() or '|' not in line:
            continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        rows.append(cells)
    
    return headers, rows

def validate_table(table_text: str, table_name: str) -> Tuple[bool, List[str]]:
    """Validate a single financial table for arithmetic integrity."""
    headers, rows = parse_markdown_table(table_text)
    
    if not headers or not rows:
        return False, [f"{table_name}: Could not parse table"]
    
    errors = []
    
    # Find column indices for numeric fields
    header_lower = [h.lower() for h in headers]
    
    # Expected columns for budget vs actual tables
    budget_idx = next((i for i, h in enumerate(header_lower) if 'budget' in h), None)
    spent_idx = next((i for i, h in enumerate(header_lower) if 'spent' in h or 'date' in h.split()), None)
    draw_idx = next((i for i, h in enumerate(header_lower) if 'draw' in h), None)
    remaining_idx = next((i for i, h in enumerate(header_lower) if 'remaining' in h), None)
    
    # Skip validation if this doesn't look like a budget table
    if budget_idx is None and spent_idx is None:
        return True, []
    
    # Track column sums
    col_sums = {i: Decimal(0) for i in range(len(headers))}
    total_row_idx = None
    
    for row_idx, row in enumerate(rows):
        # Check if this is a TOTAL row
        is_total_row = any(keyword in row[0].upper() for keyword in ['TOTAL', 'SUBTOTAL'])
        
        if is_total_row:
            total_row_idx = row_idx
        
        # For non-total rows, validate Remaining = Budget - Spent
        if not is_total_row and budget_idx is not None and spent_idx is not None and remaining_idx is not None:
            budget_val = extract_currency(row[budget_idx])
            spent_val = extract_currency(row[spent_idx])
            remaining_val = extract_currency(row[remaining_idx])
            
            if budget_val is not None and spent_val is not None and remaining_val is not None:
                expected_remaining = budget_val - spent_val
                if abs(expected_remaining - remaining_val) > Decimal('0.01'):  # Allow 1 cent rounding
                    errors.append(
                        f"{table_name}, Row '{row[0]}': "
                        f"Remaining calculation error. "
                        f"Budget {format_currency(budget_val)} - Spent {format_currency(spent_val)} "
                        f"= {format_currency(expected_remaining)}, "
                        f"but shows {format_currency(remaining_val)}"
                    )
        
        # Add numeric values to column sums
        for col_idx in range(len(headers)):
            if col_idx < len(row):
                value = extract_currency(row[col_idx])
                if value is not None:
                    col_sums[col_idx] += value
    
    # Validate TOTAL row against column sums
    if total_row_idx is not None:
        total_row = rows[total_row_idx]
        
        for col_idx in range(len(headers)):
            if col_idx >= len(total_row):
                continue
            
            total_val = extract_currency(total_row[col_idx])
            expected_sum = col_sums[col_idx]
            
            # Recalculate: sum of line items (excluding total row itself)
            line_item_sum = Decimal(0)
            for i, row in enumerate(rows):
                if i != total_row_idx and col_idx < len(row):
                    val = extract_currency(row[col_idx])
                    if val is not None:
                        line_item_sum += val
            
            if total_val is not None and abs(line_item_sum - total_val) > Decimal('0.01'):
                errors.append(
                    f"{table_name}, Column '{headers[col_idx]}': "
                    f"Total row error. "
                    f"Line items sum to {format_currency(line_item_sum)}, "
                    f"but TOTAL row shows {format_currency(total_val)}"
                )
    
    return len(errors) == 0, errors

def validate_draw_package(markdown_file: str) -> Tuple[bool, List[str]]:
    """Validate all tables in a draw package markdown file."""
    try:
        with open(markdown_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        return False, [f"File not found: {markdown_file}"]
    
    errors = []
    
    # Find all markdown tables (between | markers)
    table_pattern = r'\|.+\n\|[\s\-|:]+\n(?:\|.+\n?)+'
    tables = re.finditer(table_pattern, content)
    
    table_count = 0
    for match in tables:
        table_text = match.group(0)
        
        # Try to identify table name from preceding text
        preceding_text = content[max(0, match.start() - 200):match.start()]
        table_name_match = re.search(r'###?\s+([^\n]+)$', preceding_text, re.MULTILINE)
        table_name = table_name_match.group(1) if table_name_match else f"Table {table_count + 1}"
        
        is_valid, table_errors = validate_table(table_text, table_name)
        
        if not is_valid:
            errors.extend(table_errors)
        
        table_count += 1
    
    return len(errors) == 0, errors

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_draw_package.py <markdown_file>")
        print("Example: python3 validate_draw_package.py ../references/sample_output.md")
        sys.exit(1)
    
    markdown_file = sys.argv[1]
    
    print(f"Validating: {markdown_file}")
    print("=" * 80)
    
    is_valid, errors = validate_draw_package(markdown_file)
    
    if is_valid:
        print("✅ ALL TABLES VALID")
        print("All financial tables have exact arithmetic integrity.")
        sys.exit(0)
    else:
        print("❌ VALIDATION FAILED")
        print(f"\nFound {len(errors)} error(s):\n")
        for error in errors:
            print(f"  • {error}")
        print("\n" + "=" * 80)
        print("Fix the errors above and re-run validation.")
        sys.exit(1)

if __name__ == "__main__":
    main()
