-- study-os SQL practice schema — "Soundwave", a music streaming service.
-- Dialect: MySQL 8 (InnoDB). Matches TiDB / Outbuiltit / GlowZone.
--
-- Shapes this schema exercises:
--   1-to-many        artists → albums → tracks
--   many-to-many     playlists ↔ tracks (via playlist_tracks)
--   self-reference   users.referred_by_user_id → users.id
--   nullable columns albums.genre, users.referred_by_user_id, plays.device
--   a fact table     plays (real DATETIME, durations, high row count)
--   orphan rows      seeded on purpose so anti-joins have something to find

DROP DATABASE IF EXISTS soundwave;
CREATE DATABASE soundwave CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE soundwave;

CREATE TABLE artists (
  id          INT PRIMARY KEY,
  name        VARCHAR(100) NOT NULL,
  country     VARCHAR(50),
  formed_year SMALLINT
) ENGINE=InnoDB;

CREATE TABLE albums (
  id          INT PRIMARY KEY,
  artist_id   INT NOT NULL,
  title       VARCHAR(150) NOT NULL,
  genre       VARCHAR(30),                 -- nullable on purpose
  released_on DATE,
  FOREIGN KEY (artist_id) REFERENCES artists(id)
) ENGINE=InnoDB;

CREATE TABLE tracks (
  id           INT PRIMARY KEY,
  album_id     INT NOT NULL,
  title        VARCHAR(150) NOT NULL,
  duration_sec INT NOT NULL,
  FOREIGN KEY (album_id) REFERENCES albums(id)
) ENGINE=InnoDB;

CREATE TABLE users (
  id                  INT PRIMARY KEY,
  name                VARCHAR(100) NOT NULL,
  country             VARCHAR(50),
  plan                VARCHAR(10) NOT NULL,   -- 'free' | 'premium'
  signed_up_on        DATE NOT NULL,
  referred_by_user_id INT,                    -- NULL = organic; self-reference
  FOREIGN KEY (referred_by_user_id) REFERENCES users(id)
) ENGINE=InnoDB;

CREATE TABLE plays (
  id        INT PRIMARY KEY,
  user_id   INT NOT NULL,
  track_id  INT NOT NULL,
  played_at DATETIME NOT NULL,
  ms_played INT NOT NULL,                  -- may be < track length (a skip)
  device    VARCHAR(10),                   -- 'ios' | 'android' | 'web' | NULL
  FOREIGN KEY (user_id)  REFERENCES users(id),
  FOREIGN KEY (track_id) REFERENCES tracks(id)
) ENGINE=InnoDB;

CREATE TABLE playlists (
  id         INT PRIMARY KEY,
  user_id    INT NOT NULL,
  name       VARCHAR(100) NOT NULL,
  created_on DATE NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB;

CREATE TABLE playlist_tracks (
  playlist_id INT NOT NULL,
  track_id    INT NOT NULL,
  position    INT NOT NULL,
  PRIMARY KEY (playlist_id, track_id),
  FOREIGN KEY (playlist_id) REFERENCES playlists(id),
  FOREIGN KEY (track_id)    REFERENCES tracks(id)
) ENGINE=InnoDB;

-- NOTE: no secondary indexes, deliberately. InnoDB gives you the PK (clustered)
-- and the FK indexes it needs; nothing else. Week 10 is where you add indexes
-- and measure the difference with EXPLAIN. Adding them now hides the lesson.
