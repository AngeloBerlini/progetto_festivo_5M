-- Elimina tutte le tabelle se esistono (per reset del database)
DROP TABLE IF EXISTS utente;
DROP TABLE IF EXISTS campionato;
DROP TABLE IF EXISTS squadra;
DROP TABLE IF EXISTS partita;
DROP TABLE IF EXISTS statistiche_squadra;

-- Tabella utenti
CREATE TABLE utente (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

-- Tabella campionati
CREATE TABLE campionato (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT UNIQUE NOT NULL,
  descrizione TEXT
);

-- Tabella squadre
CREATE TABLE squadra (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT NOT NULL,
  città TEXT NOT NULL,
  creato_da INTEGER NOT NULL,
  id_campionato INTEGER NOT NULL,
  FOREIGN KEY (creato_da) REFERENCES utente (id),
  FOREIGN KEY (id_campionato) REFERENCES campionato (id),
  UNIQUE(nome, id_campionato)
);

-- Tabella partite
CREATE TABLE partita (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_squadra_casa INTEGER NOT NULL,
  id_squadra_ospiti INTEGER NOT NULL,
  gol_casa INTEGER DEFAULT 0,
  gol_ospiti INTEGER DEFAULT 0,
  data_partita TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  creato_da INTEGER NOT NULL,
  id_campionato INTEGER NOT NULL,
  FOREIGN KEY (id_squadra_casa) REFERENCES squadra (id),
  FOREIGN KEY (id_squadra_ospiti) REFERENCES squadra (id),
  FOREIGN KEY (creato_da) REFERENCES utente (id),
  FOREIGN KEY (id_campionato) REFERENCES campionato (id)
);

-- Tabella statistiche squadre (aggiornate automaticamente)
CREATE TABLE statistiche_squadra (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_squadra INTEGER NOT NULL UNIQUE,
  partite_giocate INTEGER DEFAULT 0,
  gol_fatti INTEGER DEFAULT 0,
  gol_subiti INTEGER DEFAULT 0,
  FOREIGN KEY (id_squadra) REFERENCES squadra (id)
);