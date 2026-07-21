# SQL Day 2 — INNER JOIN · Tue Jul 21

The `ON` clause · table aliases · 3-table chains · many-to-many · **how joins multiply rows**

Day 1 was one table. Everything today crosses tables — which is where SQL actually earns its keep, and where yesterday's Q8 went wrong (you counted `tracks` when the question was about `plays`).

**No `GROUP BY` today.** If you find yourself reaching for it, the question doesn't need it — aggregation is day 4.

Write all 12 blank-file into `sql/day02-answers.sql` **before running anything**. Start the file with `-- time: XXm`.

Docs allowed: [MySQL JOIN syntax](https://dev.mysql.com/doc/refman/8.0/en/join.html).

---

### Warmup — two tables

1. Every album title with its artist's name. Order by artist name, then album title.

2. Every track title with the title of the album it appears on.

3. Every track title with its **artist's** name. (Three tables — `tracks` doesn't know about `artists` directly.)

### Filtering across tables

4. The titles of all albums by artists from India.

5. Titles of tracks longer than 4 minutes that appear on albums with genre `indie`.

6. The names of users who have ever played something on an `ios` device. No duplicate names.

### Many-to-many

7. Every track title in the playlist named `Deep Work`, **in playlist order**.

8. Every playlist's name alongside the name of the user who owns it.

9. Every playlist name with the titles of its tracks — ordered by playlist name, then position.

### Counting, and the trap

10. Run this:
    ```sql
    SELECT COUNT(*) FROM tracks JOIN plays ON plays.track_id = tracks.id;
    ```
    You know `tracks` has 63 rows and `plays` has 500. **Before running it, write down what number you expect and why.** Then run it. In a comment, say what that number actually counts — it is not the number of tracks, and it is not a coincidence.

11. Run both of these:
    ```sql
    SELECT COUNT(*) FROM artists;
    SELECT COUNT(DISTINCT ar.id) FROM artists ar JOIN albums al ON al.artist_id = ar.id;
    ```
    They differ by one. In a comment, explain **why an `INNER JOIN` lost a row.**

12. Find the **name** of the artist that disappeared in question 11 — using only what you know from day 1 and today. (You don't have `LEFT JOIN` yet. There is still a way. That's the point of the question.)

---

### Stretch, only if 1–12 land under 30 minutes

13. Track titles that appear in **more than one** playlist. You don't have `GROUP BY`/`HAVING` yet — see how far a self-join on `playlist_tracks` gets you, and note where it breaks down. Tomorrow and day 4 exist because of exactly this.

---

## Bring to the call

- Your time, and how many were wrong on first execution
- **Q10 in your own words** — what a join actually produces before you count it
- **Q11 in your own words** — which row vanished and why `INNER` chose to drop it

Q10 and Q11 are the night. Everything above them is syntax practice.

Q10 is the single most common join misconception in production code: people join a parent to a child table, run `COUNT(*)`, and report the child count as if it were the parent count. Q11 is the setup for tomorrow — `LEFT JOIN` exists precisely because `INNER JOIN` silently discards the thing you were often looking for.

## Two things to get right in your syntax today

**Alias every table** (`FROM artists ar JOIN albums al ON …`) and **qualify every column** (`ar.name`, not `name`). `artists`, `albums`, `tracks` and `playlists` all have `id`, `name` or `title` columns — unqualified references are ambiguous, and MySQL will either error or silently pick one. Qualifying is a habit, not a formality.

**`JOIN` means `INNER JOIN`.** The word `INNER` is optional and most people omit it. Write it out today anyway — tomorrow you add `LEFT` and the contrast should be visible in your own files.
