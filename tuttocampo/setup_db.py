import sqlite3
import os

# Definiamo i percorsi
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(SCRIPT_DIR, 'instance')
DATABASE_PATH = os.path.join(DATABASE_DIR, 'tuttocampo.sqlite')
SCHEMA_PATH = os.path.join(SCRIPT_DIR, 'app', 'schema.sql')

# Squadre preimpostate (20 squadre per un campionato completo)
DEFAULT_TEAMS = [
    ('AC Milan', 'Milano'),
    ('Inter', 'Milano'),
    ('Juventus', 'Torino'),
    ('Torino', 'Torino'),
    ('Roma', 'Roma'),
    ('Lazio', 'Roma'),
    ('Napoli', 'Napoli'),
    ('Fiorentina', 'Firenze'),
    ('Atalanta', 'Bergamo'),
    ('Sampdoria', 'Genova'),
    ('Genoa', 'Genova'),
    ('Venezia', 'Venezia'),
    ('Verona', 'Verona'),
    ('Monza', 'Monza'),
    ('Como', 'Como'),
    ('Lecce', 'Lecce'),
    ('Sassuolo', 'Reggio Emilia'),
    ('Empoli', 'Empoli'),
    ('Frosinone', 'Frosinone'),
    ('Salernitana', 'Salerno'),
]

def setup():
    # 1. Crea la cartella 'instance' se non esiste
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)
        print(f"Cartella '{DATABASE_DIR}' creata.")

    # 2. Connessione al database
    connection = sqlite3.connect(DATABASE_PATH)
    
    # 3. Lettura ed esecuzione dello schema SQL
    try:
        with open(SCHEMA_PATH, 'r') as f:
            connection.executescript(f.read())
        connection.commit()
        print("Ottimo! Tabelle create con successo nel database.")
    except Exception as e:
        print(f"Errore durante la creazione delle tabelle: {e}")
        connection.close()
        return
    
    # 4. Aggiunta squadre preimpostate
    try:
        cursor = connection.cursor()
        for name, city in DEFAULT_TEAMS:
            cursor.execute('INSERT INTO team (name, city) VALUES (?, ?)', (name, city))
            team_id = cursor.lastrowid
            cursor.execute('INSERT INTO team_stats (team_id, matches_played, goals_for, goals_against) VALUES (?, 0, 0, 0)', (team_id,))
        connection.commit()
        print(f"✅ {len(DEFAULT_TEAMS)} squadre preimpostate aggiunte con successo!")
    except Exception as e:
        print(f"Errore durante l'inserimento delle squadre: {e}")
    finally:
        connection.close()

if __name__ == '__main__':
    print("Inizializzazione del database Tuttocampo...")
    setup()
    print("Fatto. Ora puoi avviare l'app con 'python tuttocampo/run.py'.")