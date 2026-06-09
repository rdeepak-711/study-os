# gate-slice

Freeze-kill rep 01. FastAPI + MySQL vertical slice, built from a blank file, no AI. See `SPEC.md` for the locked contract.

## Run

The MySQL password is read from the environment, never hardcoded. Pass it inline:

```bash
MYSQL_PASSWORD=<your-mysql-password> uvicorn main:app --reload
```

Or export it once for the shell session:

```bash
export MYSQL_PASSWORD=<your-mysql-password>
uvicorn main:app --reload
```

## Endpoints

- `POST /entries` with body `{"text": "..."}` inserts one row, returns the new id.
- `GET /entries` returns all rows, newest first.
