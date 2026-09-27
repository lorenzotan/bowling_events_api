# Bowling Events API — Coding Standards

FastAPI backend for tracking bowling locations and events. Python 3.13+, SQLModel, Alembic, PostgreSQL, managed with `uv`.

## Tooling

- **Lint/format:** [ruff](https://docs.astral.sh/ruff/) — `uv run ruff check .` and `uv run ruff format .`
- **Pre-commit:** `.pre-commit-config.yaml` runs `ruff --fix` and `ruff format` on every commit. Install once per clone with `uvx pre-commit install`. Run manually with `uvx pre-commit run --all-files`.
- **Tests:** `pytest`, run with `uv run pytest`.
- **Dependencies:** managed with `uv` (`uv add`, `uv add --dev`), locked in `uv.lock`. Don't hand-edit `pyproject.toml` dependency lists without re-locking.

## Style — PEP 8

This project follows [PEP 8](https://peps.python.org/pep-0008/). Most of it is enforced automatically by ruff — see `[tool.ruff]` in `pyproject.toml` (line length capped at 79, per PEP 8):

- Formatting (indentation, whitespace, blank lines, line length) — `ruff format`.
- Naming conventions (`snake_case` functions/variables/modules, `PascalCase` classes, `UPPER_CASE` constants) — rule set `N`.
- Import grouping/ordering (stdlib → third-party → local, one per line, blank line between groups) — rule set `I`.
- General correctness/style (`F`, `E`, `W`) — pyflakes + pycodestyle.

Run `uv run ruff check .` and `uv run ruff format .`; both also run automatically via pre-commit (see below). Don't hand-format against what ruff decides.

A few PEP 8 conventions ruff doesn't check mechanically — apply these by hand:

- Write a docstring for public modules, functions, classes, and methods (triple double quotes).
- Compare to `None` with `is` / `is not`, never `==`.
- Catch specific exceptions; never a bare `except:`.
- Prefer `def` over assigning a `lambda`.
- Use built-in generic types for hints (`list[X]`, `X | None`), not `typing.List` / `typing.Optional` — matches the existing SQLModel definitions in `app/db/models.py`.

Config/secrets come from environment variables via `python-decouple` (`config("DATABASE_URL")`), loaded from `.env`. Never commit real secrets in `.env`.

## Code Smells

Use [refactoring.guru's code smell catalog](https://refactoring.guru/refactoring/smells) as a review checklist when writing or refactoring code. ruff's `C90`, `PLR`, `SIM`, and `B` rule sets catch the mechanically-detectable smells automatically:

- **Bloaters** — long method / large class (`C90`, max complexity 10), long parameter list (`PLR0913`), magic values (`PLR2004`, ignored in `tests/` where literal assertions are idiomatic).
- **Needless complexity** — redundant conditionals, needlessly nested code (`SIM`).
- **Bug-prone patterns** — mutable default arguments, broad excepts, etc. (`B`).

The rest need human judgment during review — no linter catches them:

- **Object-Orientation Abusers** (switch-statement-as-polymorphism, refused bequest) — watch for this if router logic grows past simple CRUD.
- **Change Preventers** (shotgun surgery, divergent change) — if adding one field to `Event`/`Location` requires touching more than model + migration + router, the layers aren't separated cleanly.
- **Dispensables** (dead code, duplicate code) — delete rather than comment out; extract rather than copy-paste. Note: SQLModel table classes *should* look like plain data classes — that's normal for an ORM model, not a smell here.
- **Couplers** (feature envy, message chains, middle man) — keep routers talking to `Session`/SQLModel directly; don't add indirection layers speculatively.

## Project structure

- `app/api/v1/` — one router module per resource (`events.py`, `locations.py`). Routers stay thin: parse/validate input, open a `Session`, delegate to SQLModel queries, return. No business logic embedded in route handlers beyond simple CRUD.
- `app/db/models.py` — SQLModel table models. Relationships declared both sides with `Relationship(back_populates=...)`.
- `app/db/database.py` — the single shared `engine`. Import `engine` from here rather than constructing a new `create_engine(...)` per module (this used to be duplicated per-router; don't reintroduce that).
- `app/db/migrations/` — Alembic. Generate migrations for every schema change (`alembic revision --autogenerate -m "..."`); don't hand-edit the live DB schema or existing migration files after they've been applied.

## Tests

- Live under `tests/`, using `fastapi.testclient.TestClient` against the real `app` instance (see `tests/test_main.py`).
- Name test files `test_*.py`, test functions `test_*`.
