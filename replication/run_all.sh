#!/usr/bin/env bash
# Replication script for Skatteprogressivitet
# Reproduces all tables and figures from the main paper.
# Run from the repository root: bash replication/run_all.sh

set -euo pipefail

echo "=== Skatteprogressivitet replication ==="
echo "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Python: $(python --version)"

echo ""
echo "Step 1: Validate legislation ledger"
uv run python scripts/validate_all_legislation.py

echo ""
echo "Step 2: Generate synthetic data fixtures"
uv run python scripts/generate_synthetic_data.py

echo ""
echo "Step 3: Run static simulation (2025 baseline)"
uv run skatteprogressivitet simulate --year 2025 --behavioural none \
  --output reports/sim_2025_static.parquet

echo ""
echo "Step 4: Run behavioural simulation (2025 baseline)"
uv run skatteprogressivitet simulate --year 2025 --behavioural full \
  --output reports/sim_2025_behavioural.parquet

echo ""
echo "Step 5: Compute progressivity indices"
uv run skatteprogressivitet progressivity --year 2025

echo ""
echo "Step 6: Run all scenarios"
for scenario_file in data/scenarios/*.yaml; do
  echo "  Running scenario: $scenario_file"
  uv run skatteprogressivitet scenario "$scenario_file"
done

echo ""
echo "Step 7: Generate report figures"
uv run skatteprogressivitet report --year 2025 --output-dir reports/

echo ""
echo "=== Replication complete ==="
echo "Outputs written to reports/"
