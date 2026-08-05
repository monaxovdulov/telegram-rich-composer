# Contributing

Use Python 3.11 or newer. Keep `CompositionSpec` harness-independent and never add recipient or token fields.

```bash
uv venv .venv
uv pip install --python .venv/bin/python -e '.[dev]'
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/pytest --cov=telegram_rich_composer --cov-fail-under=85
.venv/bin/python scripts/check_docs.py
.venv/bin/python scripts/check_links.py
```

Add a golden spec for a new composition pattern. Add both English and Russian documentation files. A fallback change must include permanent-rejection and unknown-delivery tests. Do not add generated media, credentials, database files, request logs, or source copied from an unlicensed project.
