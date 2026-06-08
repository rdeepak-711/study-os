# Freeze-kill rep 01 — FastAPI + MySQL vertical slice (gate seed)

Frozen 2026-06-08. Scope is locked. Do not add to this tonight.

## The contract (this is ALL of it)

- `POST /entry` with body `{ "text": "..." }` inserts one row into MySQL, returns the new id.
- `GET /entries` returns all rows, newest first.
- Table `entries`: `id` (PK, auto increment), `text` (varchar), `created_at` (timestamp, default now).

## Rules

- No Claude. No AI autocomplete. FastAPI and MySQL docs are allowed.
- Write `main.py` from a blank file, by hand.
- About 40 to 60 lines. Throwaway grade. It does not need to be pretty.
- Timebox: one session, roughly 45 to 60 minutes.
- MySQL, not SQLite. If MySQL setup eats the session, fall back to SQLite and say so in the log.
- Done = both routes work when you run it. Then log it and push via /studylog.

## What this is NOT (the scope cage)

- No auth. No frontend. No comments. No styling. No extra routes.
- This is not the portfolio. The portfolio is Phase 4.
