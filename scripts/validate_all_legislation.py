"""Validate all legislation YAML files.

Run:
    uv run python scripts/validate_all_legislation.py
"""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from skatteprogressivitet.legislation.loader import load_all


def main() -> None:
    print("Validating all legislation YAML files...")
    ledger = load_all()
    for year, leg in sorted(ledger.items()):
        print(f"  {year}: OK  (kommunal_rate={leg.kommunal_skatt.rate:.4f},"
              f"  IBB={leg.inkomstbasbelopp:,.0f})")
    print(f"\n{len(ledger)} file(s) valid.")


if __name__ == "__main__":
    main()
