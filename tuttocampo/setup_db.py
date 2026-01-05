import sqlite3
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(SCRIPT_DIR, 'instance')
DATABASE_PATH = os.path.join(DATABASE_DIR, 'tuttocampo.sqlite')
SCHEMA_PATH = os.path.join(SCRIPT_DIR, 'app', 'schema.sql')


def setup():
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)
        print(f"Cartella '{DATABASE_DIR}' creata.")


    connection = sqlite3.connect(DATABASE_PATH)
    

    try:
        with open(SCHEMA_PATH, 'r') as f:
            connection.executescript(f.read())
        connection.commit()
        print("Ottimo! Tabelle create con successo nel database.")
    except Exception as e:
        print(f"Errore durante la creazione delle tabelle: {e}")
        connection.close()
        return
    
    # Aggiungi i campionati
    try:
        cursor = connection.cursor()
        campionati = [
            ('Serie A', 'Campionato di calcio Serie A'),
            ('Serie B', 'Campionato di calcio Serie B'),
        ]
        for nome, descrizione in campionati:
            cursor.execute('INSERT INTO campionato (nome, descrizione) VALUES (?, ?)', (nome, descrizione))
        connection.commit()
        print("✅ Campionati aggiunti con successo!")
    except Exception as e:
        print(f"Errore durante l'inserimento dei campionati: {e}")
    finally:
        connection.close()

if __name__ == '__main__':
    print("Inizializzazione del database Tuttocampo...")
    setup()
    print("Fatto. Ora puoi avviare l'app con 'python tuttocampo/run.py'.")