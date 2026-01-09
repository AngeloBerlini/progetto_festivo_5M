import sqlite3
import os

PERCORSO_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PERCORSO_DATABASE = os.path.join(PERCORSO_SCRIPT, 'instance')
PERCORSO_DATABASE_FILE = os.path.join(PERCORSO_DATABASE, 'tuttocampo.sqlite')
PERCORSO_SCHEMA = os.path.join(PERCORSO_SCRIPT, 'app', 'schema.sql')


def configura():
    """Inizializza il database e le tabelle"""
    if not os.path.exists(PERCORSO_DATABASE):
        os.makedirs(PERCORSO_DATABASE)
        print(f"Cartella '{PERCORSO_DATABASE}' creata.")

    # Connettiti al database
    connessione = sqlite3.connect(PERCORSO_DATABASE_FILE)
    
    try:
        # Esegui lo script SQL per creare le tabelle
        with open(PERCORSO_SCHEMA, 'r') as f:
            connessione.executescript(f.read())
        connessione.commit()
        print("Ottimo! Tabelle create con successo nel database.")
    except Exception as e:
        print(f"Errore durante la creazione delle tabelle: {e}")
        connessione.close()
        return
    
    # Inserisci i campionati iniziali
    try:
        cursore = connessione.cursor()
        campionati = [
            ('Serie A', 'Campionato di calcio Serie A'),
            ('Serie B', 'Campionato di calcio Serie B'),
        ]
        for nome, descrizione in campionati:
            cursore.execute('INSERT INTO campionato (nome, descrizione) VALUES (?, ?)', (nome, descrizione))
        connessione.commit()
        print("Campionati aggiunti con successo!")
    except Exception as e:
        print(f"Errore durante l'inserimento dei campionati: {e}")
    finally:
        connessione.close()

if __name__ == '__main__':
    print("Inizializzazione del database Tuttocampo...")
    configura()
    print("Fatto. Ora puoi avviare l'app con 'python tuttocampo/run.py'.")