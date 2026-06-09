# Freeze-kill rep 02 — full CRUD on the entries app (extends rep 01)

Frozen 2026-06-09. This **extends the gate-slice**. Do NOT start a new project or add a frontend tonight.

## Where you start (rep 01 already gives you C + R-all)

- `POST /entries` `{text}` → inserts, returns the new id
- `GET /entries` → all rows, newest first

## Tonight's contract (add these three)

- `GET /entries/{id}` → return that one row. If it doesn't exist, **404**.
- `PUT /entries/{id}` `{text}` → update that row's text. Return the updated row (or its id). **404** if missing.
- `DELETE /entries/{id}` → delete that row. Return a small confirmation. **404** if missing.

That's the full CRUD: Create, Read (one + all), Update, Delete.

## The new muscle (what you'll actually freeze on)

- **Path parameters:** how FastAPI binds `{id}` from the URL into the function.
- **HTTPException:** raising a `404` instead of returning `null`/`None` when the row isn't there.
- **UPDATE / DELETE SQL** with `WHERE id = %s`, and reading `cursor.rowcount` to know whether anything actually matched (that's how you decide 404 vs success).

## Rules (same as rep 01)

- No Claude, no AI autocomplete. FastAPI + MySQL docs allowed.
- Extend `main.py` by hand. Still throwaway grade. ~60–90 lines total now.
- Password stays in `os.environ`. No new secrets in the file.
- Timebox: 2 sessions (~3 hrs).

## Done =

All five routes work when you run it: create one, list, fetch it by id, update it, delete it, confirm the list shrank. A fetch / update / delete on a **missing** id returns **404**, not a crash and not `null`. Then grade each line against this SPEC before you log it.

## NOT tonight (the scope cage)

No frontend. No auth. No pagination. No new entity, no `users` table. The gate (`g0`) adds the frontend later, not now.
