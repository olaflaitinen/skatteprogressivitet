"""REUSE compliance and formatting guard tests."""

from __future__ import annotations

import pathlib
import re

import pytest

REPO_ROOT = pathlib.Path(__file__).parent.parent

EM_DASH = "\u2014"
EN_DASH = "\u2013"

EMOJI_PATTERN = re.compile(
    "[\U0001f300-\U0001f9ff"
    "\U00002600-\U000027bf"
    "\U0001fa00-\U0001fa9f"
    "\U00002702-\U000027b0]+",
    re.UNICODE,
)

SOURCE_EXTENSIONS = {".py", ".md", ".yaml", ".yml", ".toml", ".json", ".txt", ".cff", ".do", ".R"}

EXCLUDED_DIRS = {".git", ".venv", "venv", "__pycache__", ".mypy_cache", ".ruff_cache", "site"}


def _iter_source_files():
    for path in REPO_ROOT.rglob("*"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if path.suffix in SOURCE_EXTENSIONS and path.is_file():
            yield path


def test_no_em_dash_in_source_files() -> None:
    violations = []
    for path in _iter_source_files():
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if EM_DASH in content:
            lines = [
                i + 1
                for i, line in enumerate(content.splitlines())
                if EM_DASH in line
            ]
            violations.append(f"{path.relative_to(REPO_ROOT)}: lines {lines}")
    assert not violations, "Em-dash (U+2014) found:\n" + "\n".join(violations)


def test_no_en_dash_in_source_files() -> None:
    violations = []
    for path in _iter_source_files():
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if EN_DASH in content:
            lines = [
                i + 1
                for i, line in enumerate(content.splitlines())
                if EN_DASH in line
            ]
            violations.append(f"{path.relative_to(REPO_ROOT)}: lines {lines}")
    assert not violations, "En-dash (U+2013) found:\n" + "\n".join(violations)


def test_no_emoji_in_source_files() -> None:
    violations = []
    for path in _iter_source_files():
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if EMOJI_PATTERN.search(content):
            violations.append(str(path.relative_to(REPO_ROOT)))
    assert not violations, "Emoji found in:\n" + "\n".join(violations)


def test_no_spdx_headers_in_python_files() -> None:
    violations = []
    for path in REPO_ROOT.rglob("*.py"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if "SPDX-License-Identifier" in content:
            violations.append(str(path.relative_to(REPO_ROOT)))
    assert not violations, "SPDX headers found in:\n" + "\n".join(violations)


def test_license_file_exists() -> None:
    assert (REPO_ROOT / "LICENSE").exists()


def test_reuse_dep5_exists() -> None:
    assert (REPO_ROOT / ".reuse" / "dep5").exists()


def test_eupl_license_file_exists() -> None:
    assert (REPO_ROOT / "LICENSES" / "EUPL-1.2.txt").exists()


def test_cc0_license_file_exists() -> None:
    assert (REPO_ROOT / "LICENSES" / "CC0-1.0.txt").exists()


def test_cc_by_license_file_exists() -> None:
    assert (REPO_ROOT / "LICENSES" / "CC-BY-4.0.txt").exists()
