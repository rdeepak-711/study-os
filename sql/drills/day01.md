# SQL Day 1 — Basics · Mon Jul 20

`SELECT` · `WHERE` · `ORDER BY` · `LIMIT` · `DISTINCT` · NULL semantics

**Single table only. No joins tonight** — joins are next Wednesday. If you find yourself reaching for a join, re-read the question.

Write all 12 blank-file into `sql/day01-answers.sql` **before running anything**. Then run them, and mark which ones were wrong on first execution. That number is the score you bring to the call, not the number you eventually got green.

Start the file with `-- time: XXm`.

```bash
cd study-os/sql && python3 seed.py
```

Then in MySQL Workbench: **File → Open SQL Script → `soundwave.sql` → ⚡ Execute**, then `USE soundwave;`

---

### Warmup

1. Every artist's name and country, alphabetical by name.

2. All tracks longer than 5 minutes. Show the title and the duration **in minutes**, longest first.

3. The 5 most recently released albums — title and release date.

### Filtering

4. All users on the `premium` plan who signed up in 2026.

5. Every album released in 2015 **or later** whose genre is `indie` or `electronic`.

6. All plays from a mobile device (`ios` or `android`) that lasted **under 30 seconds**. Show the play id, device, and seconds played.

### DISTINCT

7. The distinct list of countries users come from.

8. How many **distinct** tracks have ever been played? (One number.)

### NULLs — the part that catches people

9. All albums with **no genre recorded**.

10. Every user who signed up organically (nobody referred them).

11. `SELECT COUNT(*) FROM plays;` and `SELECT COUNT(device) FROM plays;` return different numbers. Run both. **Write down in a comment why**, in one sentence — before you look it up.

12. Try `SELECT * FROM albums WHERE genre = NULL;`. It returns nothing, and it is not a bug. Explain in a comment what SQL actually evaluated, and what the correct query is.

---

### Stretch, only if the 12 land in under 40 minutes

13. Every play where the user listened for **less than half** the track's length. (Yes, this needs a join — take it as a preview of next week, not a requirement.)

---

## Bring to the call

- Your time
- How many were wrong on first execution
- Your answers to **11 and 12 in your own words** — those two are the whole point of the night. Everything else is finger exercises; NULL three-valued logic is the thing that shows up in production bugs and interview screens both.
