# Bowling Events API — Coding Standards

FastAPI backend for tracking bowling locations and events. Python 3.13+, SQLModel, Alembic, PostgreSQL, managed with `uv`.

## Tooling

- **Lint/format:** [ruff](https://docs.astral.sh/ruff/) — `uv run ruff check .` and `uv run ruff format .`
- **Pre-commit:** `.pre-commit-config.yaml` runs `ruff --fix` and `ruff format` on every commit. Install once per clone with `uvx pre-commit install`. Run manually with `uvx pre-commit run --all-files`.
- **Tests:** `pytest`, run with `uv run pytest`.
- **Dependencies:** managed with `uv` (`uv add`, `uv add --dev`), locked in `uv.lock`. Don't hand-edit `pyproject.toml` dependency lists without re-locking.

## Style

- Use built-in generic types for hints (`list[X]`, `X | None`), not `typing.List` / `typing.Optional` — matches the existing SQLModel definitions in `app/db/models.py`.
- `snake_case` for functions, variables, and modules; `PascalCase` for SQLModel/Pydantic classes.
- Let ruff own formatting decisions (quote style, import layout, blank lines) — don't hand-format against it.
- Config/secrets come from environment variables via `python-decouple` (`config("DATABASE_URL")`), loaded from `.env`. Never commit real secrets in `.env`.

## Project structure

- `app/api/v1/` — one router module per resource (`events.py`, `locations.py`). Routers stay thin: parse/validate input, open a `Session`, delegate to SQLModel queries, return. No business logic embedded in route handlers beyond simple CRUD.
- `app/db/models.py` — SQLModel table models. Relationships declared both sides with `Relationship(back_populates=...)`.
- `app/db/database.py` — the single shared `engine`. Import `engine` from here rather than constructing a new `create_engine(...)` per module (this used to be duplicated per-router; don't reintroduce that).
- `app/db/migrations/` — Alembic. Generate migrations for every schema change (`alembic revision --autogenerate -m "..."`); don't hand-edit the live DB schema or existing migration files after they've been applied.

## Tests

- Live under `tests/`, using `fastapi.testclient.TestClient` against the real `app` instance (see `tests/test_main.py`).
- Name test files `test_*.py`, test functions `test_*`.
