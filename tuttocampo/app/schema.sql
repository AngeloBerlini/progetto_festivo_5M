DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS campionato;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS match;
DROP TABLE IF EXISTS team_stats;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE campionato (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT UNIQUE NOT NULL,
  descrizione TEXT
);

CREATE TABLE team (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  city TEXT NOT NULL,
  created_by INTEGER NOT NULL,
  campionato_id INTEGER NOT NULL,
  FOREIGN KEY (created_by) REFERENCES user (id),
  FOREIGN KEY (campionato_id) REFERENCES campionato (id),
  UNIQUE(name, campionato_id)
);

CREATE TABLE match (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  home_team_id INTEGER NOT NULL,
  away_team_id INTEGER NOT NULL,
  home_score INTEGER DEFAULT 0,
  away_score INTEGER DEFAULT 0,
  match_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  created_by INTEGER NOT NULL,
  campionato_id INTEGER NOT NULL,
  FOREIGN KEY (home_team_id) REFERENCES team (id),
  FOREIGN KEY (away_team_id) REFERENCES team (id),
  FOREIGN KEY (created_by) REFERENCES user (id),
  FOREIGN KEY (campionato_id) REFERENCES campionato (id)
);

CREATE TABLE team_stats (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  team_id INTEGER NOT NULL UNIQUE,
  matches_played INTEGER DEFAULT 0,
  goals_for INTEGER DEFAULT 0,
  goals_against INTEGER DEFAULT 0,
  FOREIGN KEY (team_id) REFERENCES team (id)
);