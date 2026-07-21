-- Look at everything. Not a drill — just orientation before you write queries.
-- Workbench: Execute All (⚡). Each SELECT opens its own result tab.

USE soundwave;

SELECT * FROM artists         ORDER BY id;   -- 10 rows
SELECT * FROM albums          ORDER BY id;   -- 15 rows
SELECT * FROM tracks          ORDER BY id;   -- 63 rows
SELECT * FROM users           ORDER BY id;   -- 15 rows
SELECT * FROM playlists       ORDER BY id;   --  8 rows
SELECT * FROM playlist_tracks ORDER BY playlist_id, position;  -- 47 rows

-- 500 rows: look at a slice, not the whole thing
SELECT * FROM plays ORDER BY id LIMIT 50;

-- Row counts, all in one line
SELECT
  (SELECT COUNT(*) FROM artists)         AS artists,
  (SELECT COUNT(*) FROM albums)          AS albums,
  (SELECT COUNT(*) FROM tracks)          AS tracks,
  (SELECT COUNT(*) FROM users)           AS users,
  (SELECT COUNT(*) FROM plays)           AS plays,
  (SELECT COUNT(*) FROM playlists)       AS playlists,
  (SELECT COUNT(*) FROM playlist_tracks) AS playlist_tracks;
