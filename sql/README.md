# SQL track — from scratch

**Daily.** Blank file, AI off, docs allowed. Pass = explain the query aloud on the call and defend why it returns what it returns.

Daily cadence means one concept per day and ~25 minutes, not a full night — SQL runs as a warm-up ahead of the night's main track, so the one-track-per-night rule still holds for the deep work.

## Build the database

**MySQL 8, via MySQL Workbench.**

```bash
cd study-os/sql
python3 seed.py            # writes soundwave.sql
```

Then in Workbench: **File → Open SQL Script → `soundwave.sql` → ⚡ Execute**. It drops and recreates the `soundwave` schema, so re-running is always safe. Hit the refresh icon in the schema sidebar afterwards or the tree won't show the new tables.

`seed.py` needs no database driver and no `pip install` — it just writes a plain `.sql` file. The RNG seed is fixed, so **all three of us get byte-identical data**: "my query returns 7 rows" is a comparable claim on the call.

Week 10 rebuilds at scale: `python3 seed.py --plays 1000000` (~70 MB — import from the command line rather than Workbench, which chokes on files that size):

```bash
mysql -u root -p < soundwave.sql
```

Verify the import landed:

```sql
USE soundwave;
SELECT
  (SELECT COUNT(*) FROM artists) AS artists,   -- 10
  (SELECT COUNT(*) FROM albums)  AS albums,    -- 15
  (SELECT COUNT(*) FROM tracks)  AS tracks,    -- 63
  (SELECT COUNT(*) FROM users)   AS users,     -- 15
  (SELECT COUNT(*) FROM plays)   AS plays;     -- 500
```

**One MySQL 8 default worth knowing now:** `ONLY_FULL_GROUP_BY` is on. It will reject a `GROUP BY` that selects a column it can't prove is functionally dependent on the grouping. This is correct behaviour and good for you — it catches the sloppy `GROUP BY` that older MySQL and SQLite silently allow. Don't turn it off.

## The schema — "Soundwave", a music streaming service

```
artists ──< albums ──< tracks ──< plays >── users ──┐
                         │                   │      │ (referred_by_user_id
                         │                   │      └──  self-reference)
                         └──< playlist_tracks >── playlists
```

| Table | Rows | What it teaches |
|---|---|---|
| `artists` | 10 | the simple end — one artist has **no albums** |
| `albums` | 15 | 1-to-many; `genre` is **nullable** |
| `tracks` | 63 | two levels deep; one album has **no tracks** |
| `users` | 15 | **self-reference** via `referred_by_user_id` (NULL = organic) |
| `plays` | 500 | the fact table — dates, durations, **NULL** devices, 28% skips |
| `playlists` | 8 | one is **empty** |
| `playlist_tracks` | 47 | **many-to-many** junction |

**The orphan rows are deliberate.** One artist with no albums, one album with no tracks, one user who has never pressed play, one empty playlist. If your anti-join returns zero rows, your anti-join is wrong — not the data.

**There are no indexes beyond the primary keys, on purpose.** Adding them now would hide week 10's entire lesson.

## Dialect

**MySQL 8 throughout.** Same dialect as TiDB, so everything transfers directly to Outbuiltit, GlowZone and billing-site — and it's what SQL screens assume. No dialect switch anywhere in the curriculum; week 10 changes the *data volume*, not the engine.

## Curriculum

One concept per day. Dates hold to the day *after* Goa (Aug 3–7) shifts everything.

| Day | Date | Topic |
|---|---|---|
| 1 | Jul 20 ✅ | **Basics** — `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `DISTINCT`, NULL semantics (`IS NULL`, never `= NULL`) · *scored 8/12* |
| 2 | Jul 21 | **INNER JOIN** — the `ON` clause, table aliases, 3-table chains, many-to-many, and how joins multiply rows |
| 3 | Jul 22 | **LEFT JOIN & the anti-join** — `LEFT JOIN … IS NULL`, `COALESCE`, finding what *isn't* there |
| 4 | Jul 23 | **Aggregation** — `GROUP BY`, `COUNT(*)` vs `COUNT(col)`, `SUM`/`AVG` and NULLs |
| 5 | Jul 24 | **`WHERE` vs `HAVING`** — filtering before vs after grouping, and why the alias rule from day 1 explains it |
| 6 | Jul 25 | **Subqueries** — scalar, `IN`, `EXISTS`, and the `NOT IN` + NULL trap |
| 7 | Jul 26 | **CTEs** — `WITH`, chaining, readability over cleverness |
| 8 | Jul 27 | **`CASE`** — conditional aggregation, pivots |
| 9 | Jul 28 | **`COALESCE` & NULL handling in aggregates** |
| 10 | Jul 29 | **Dates & strings** — ranges, truncation, the `BETWEEN` off-by-one |
| 11 | Jul 30 | **Self-joins** — the referral chain in `users` |
| 12 | Jul 31 | **Set ops** — `UNION` vs `UNION ALL`, `INTERSECT` alternatives in MySQL |
| 13 | Aug 1 | **Windows I** — `ROW_NUMBER`/`RANK`/`DENSE_RANK`, `PARTITION BY`, top-N-per-group |
| 14 | Aug 2 | **Windows II** — `LAG`/`LEAD`, running totals, frame clauses |
| — | Aug 3–7 | Goa, paused |
| 15 | Aug 8 | **Review** — mixed set, no new concepts |
| 16 | Aug 9 | **Indexing** — rebuild at 1M rows, read `EXPLAIN`, watch an index change the plan |
| 17 | Aug 10 | **Optimization** — N+1, covering indexes, when the planner ignores your index |
| 18+ | Aug 11 → | **Real schemas** — queries against the live Outbuiltit / GlowZone TiDB schemas. Toy data stops teaching around here. |

Days 1–15 are SQL fluency. Day 16 is where SQL stops being syntax and becomes engineering — **do not skip the row seeding**, you cannot see an index matter on 500 rows.

## How a session runs

1. Read the day's drills (`drills/dayNN.md`)
2. Write every query **blank-file, before running anything**, into `dayNN-answers.sql`
3. *Then* run them. Note which ones you got wrong on the first execution — that number is the real score
4. Bring the wrong ones to the call

Each answer file starts with `-- time: XXm`.
