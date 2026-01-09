import sqlite3
import click
from flask import current_app, g

def ottieni_db():
    """
    Ottiene una connessione al database e la salva nel contesto di richiesta (g).
    Abilita il ritorno delle righe come oggetti Row per un accesso più facile.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

def chiudi_db(e=None):
    """Chiude la connessione al database al termine della richiesta"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def inizializza_db():
    """Crea tutte le tabelle del database eseguendo lo script SQL"""
    db = ottieni_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def comando_inizializza_db():
    """Comando CLI per inizializzare il database"""
    inizializza_db()
    click.echo('Database inizializzato!')

def inizializza_app(app):
    """Registra le funzioni di cleanup del database con Flask"""
    app.teardown_appcontext(chiudi_db)
    app.cli.add_command(comando_inizializza_db)