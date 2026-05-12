# Installation

## Requirements

- Python 3.11 or 3.12
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Install from PyPI

```bash
pip install skatteprogressivitet
```

## Install from source (development)

```bash
git clone https://github.com/olaflaitinen/skatteprogressivitet.git
cd skatteprogressivitet
uv sync --extra dev --extra docs
```

## Verify the installation

```bash
skatteprogressivitet validate-legislation --all
# Expected: "7 legislation files valid."
```

## Optional dependencies

| Extra | Purpose |
|-------|---------|
| `dev` | linting, type-checking, testing |
| `docs` | MkDocs documentation build |
| `bench` | benchmarking with pytest-benchmark |

## Platform notes

The package is tested on Linux (Ubuntu 22.04 LTS) and macOS 14 under
Python 3.11 and 3.12. Windows is supported but not part of the CI matrix.

## Generating the synthetic data fixture

After installation, generate the synthetic LISA panel once:

```bash
uv run python scripts/generate_synthetic_data.py
```

This writes `data/synthetic/lisa_like.parquet` (~50 000 rows per year).
