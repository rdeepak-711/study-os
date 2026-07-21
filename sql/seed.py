#!/usr/bin/env python3
"""Generate soundwave.sql — schema + data for the study-os SQL track (MySQL 8).

Emits one plain .sql file. No database driver, no pip install: open the file in
MySQL Workbench and run it. Same file works for all three of us.

Deterministic — a fixed RNG seed means byte-identical data everywhere, so
"my query returns 7 rows" is a comparable claim on the nightly call.

    python3 seed.py                    # small: readable by eye, weeks 1-9
    python3 seed.py --plays 1000000    # week 10: big enough for indexes to matter

Deliberate teaching traps baked into the data (don't "fix" these):
  - one artist with no albums          → anti-join
  - one album with no tracks           → anti-join through two levels
  - one user who has never played      → LEFT JOIN + COALESCE to 0
  - one empty playlist                 → anti-join across a junction table
  - NULL genres and NULL devices       → COALESCE, and COUNT(col) vs COUNT(*)
  - referral chains among users        → self-join
  - plays where ms_played < duration   → conditional aggregation (skip rate)
"""

import argparse
import os
import random
from datetime import date, datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(HERE, "schema.sql")
OUT_PATH = os.path.join(HERE, "soundwave.sql")

SEED = 711
START = date(2026, 4, 1)   # 90-day activity window ending 2026-06-29
BATCH = 1000               # rows per multi-row INSERT

ARTISTS = [
    ("Neon Harbour",     "UK",        2011),
    ("Kavya Rao",        "India",     2018),
    ("The Slow Signal",  "USA",       2007),
    ("Marrow",           "Sweden",    2015),
    ("Anand Prakash",    "India",     2013),
    ("Glass Cathedral",  "Canada",    2019),
    ("Bitterroot",       "USA",       2009),
    ("Yuki Tanaka",      "Japan",     2020),
    ("Palmyra Drift",    "Australia", 2016),
    ("Sable Union",      "UK",        2021),   # trap: gets no albums
]

GENRES = ["indie", "electronic", "rock", "ambient", "hip-hop", None]
DEVICES = ["ios", "android", "web", None]
COUNTRIES = ["India", "USA", "UK", "Germany", "Japan", "Australia"]

ALBUM_WORDS_A = ["Slow", "Paper", "Northern", "Salt", "Amber", "Quiet", "Iron",
                 "Velvet", "Hollow", "Bright", "Winter", "Copper"]
ALBUM_WORDS_B = ["Rooms", "Machines", "Light", "Harbour", "Years", "Static",
                 "Gardens", "Signals", "Weather", "Cities", "Tide", "Hours"]
TRACK_WORDS = ["Undertow", "Ferry", "Blue Hour", "Cassette", "Meridian", "Dust",
               "Lantern", "Halfway", "Radio Silence", "Sundial", "Anchor",
               "Pilgrim", "Nightshift", "Marble", "Threshold", "Wilder",
               "Passenger", "Foxglove", "Overcast", "Kite String", "Lowlands",
               "Ash Wednesday", "Telegram", "Backroads"]
USER_NAMES = ["Deepak", "Aditi", "Rahul", "Meera", "Tom", "Sana", "Ishaan",
              "Nadia", "Kenji", "Priya", "Marcus", "Leila", "Arjun", "Freya",
              "Vikram"]
PLAYLIST_NAMES = ["Morning Run", "Deep Work", "Late Drive", "Rain", "Gym",
                  "Sunday Slow", "Discover", "Saved for Later"]


def lit(v):
    """Render a Python value as a MySQL literal."""
    if v is None:
        return "NULL"
    if isinstance(v, int):
        return str(v)
    return "'" + str(v).replace("\\", "\\\\").replace("'", "''") + "'"


def insert_stmts(table, rows):
    """Batched multi-row INSERTs — one statement per BATCH rows."""
    out = []
    for i in range(0, len(rows), BATCH):
        chunk = rows[i:i + BATCH]
        values = ",\n".join("  (" + ",".join(lit(c) for c in r) + ")"
                            for r in chunk)
        out.append(f"INSERT INTO {table} VALUES\n{values};\n")
    return "".join(out)


def play_dt(d, rng):
    """A random time-of-day on date d, weighted toward evenings."""
    hour = rng.choice([7, 8, 9, 12, 13, 18, 19, 20, 21, 21, 22, 22, 23])
    return datetime(d.year, d.month, d.day,
                    hour, rng.randrange(60), rng.randrange(60)
                    ).strftime("%Y-%m-%d %H:%M:%S")


def build(n_plays):
    rng = random.Random(SEED)

    artists = [(i + 1, *a) for i, a in enumerate(ARTISTS)]

    # albums — last artist deliberately gets none
    albums, album_id = [], 0
    for aid, _name, _country, formed in artists[:-1]:
        for _ in range(rng.randint(1, 3)):
            album_id += 1
            title = f"{rng.choice(ALBUM_WORDS_A)} {rng.choice(ALBUM_WORDS_B)}"
            released = date(rng.randint(max(formed, 2010), 2025),
                            rng.randint(1, 12), rng.randint(1, 28))
            albums.append((album_id, aid, title, rng.choice(GENRES),
                           released.isoformat()))

    # tracks — last album deliberately gets none
    tracks, track_id = [], 0
    for alb in albums[:-1]:
        for _ in range(rng.randint(3, 6)):
            track_id += 1
            tracks.append((track_id, alb[0], rng.choice(TRACK_WORDS),
                           rng.randint(105, 380)))

    # users — referral chain, user 1 is organic
    users = []
    for i, name in enumerate(USER_NAMES, start=1):
        signed = START - timedelta(days=rng.randint(0, 400))
        referrer = None if (i == 1 or rng.random() < 0.4) else rng.randint(1, i - 1)
        users.append((i, name, rng.choice(COUNTRIES),
                      "premium" if rng.random() < 0.45 else "free",
                      signed.isoformat(), referrer))

    # plays — last user deliberately gets none
    playable = [(t[0], t[3]) for t in tracks]
    active_users = [u[0] for u in users[:-1]]
    weights = [rng.choice([1, 1, 2, 3, 6]) for _ in active_users]

    plays = []
    for pid in range(1, n_plays + 1):
        uid = rng.choices(active_users, weights=weights, k=1)[0]
        tid, dur = rng.choice(playable)
        day = START + timedelta(days=rng.randrange(90))
        ms = (rng.randint(5, max(6, dur // 2)) if rng.random() < 0.25
              else rng.randint(dur - 3, dur)) * 1000
        plays.append((pid, uid, tid, play_dt(day, rng), ms, rng.choice(DEVICES)))

    # playlists — last one deliberately left empty
    playlists, pl_tracks = [], []
    for i, pname in enumerate(PLAYLIST_NAMES, start=1):
        owner = rng.choice(active_users)
        created = START + timedelta(days=rng.randrange(60))
        playlists.append((i, owner, pname, created.isoformat()))
        if i == len(PLAYLIST_NAMES):
            continue
        chosen = rng.sample(playable, rng.randint(4, 9))
        for pos, (tid, _d) in enumerate(chosen, start=1):
            pl_tracks.append((i, tid, pos))

    with open(SCHEMA_PATH) as f:
        schema = f.read()

    parts = [
        "-- Generated by seed.py — do not hand-edit. Regenerate instead.\n",
        f"-- plays rows: {n_plays:,}\n\n",
        schema,
        "\nSET FOREIGN_KEY_CHECKS = 0;\n\n",
        insert_stmts("artists", artists),
        insert_stmts("albums", albums),
        insert_stmts("tracks", tracks),
        insert_stmts("users", users),
        insert_stmts("plays", plays),
        insert_stmts("playlists", playlists),
        insert_stmts("playlist_tracks", pl_tracks),
        "\nSET FOREIGN_KEY_CHECKS = 1;\n",
    ]
    with open(OUT_PATH, "w") as f:
        f.write("".join(parts))

    return {"artists": len(artists), "albums": len(albums),
            "tracks": len(tracks), "users": len(users), "plays": len(plays),
            "playlists": len(playlists), "playlist_tracks": len(pl_tracks)}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--plays", type=int, default=500,
                    help="rows in plays (default 500; use 1000000 in week 10)")
    args = ap.parse_args()

    counts = build(args.plays)
    size_mb = os.path.getsize(OUT_PATH) / 1024 / 1024
    print(f"wrote {OUT_PATH}  ({size_mb:.1f} MB)")
    for table, n in counts.items():
        print(f"  {table:16} {n:>9,}")
    print("\ntraps seeded: 1 artist w/o albums · 1 album w/o tracks · "
          "1 user w/o plays · 1 empty playlist · NULL genres/devices/referrers")
    print("\nMySQL Workbench:  File → Open SQL Script → soundwave.sql → ⚡ Execute")
