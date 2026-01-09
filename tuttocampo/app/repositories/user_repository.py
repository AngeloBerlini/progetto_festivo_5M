from app.db import ottieni_db

def ottieni_utente_per_id(id_utente):
    """Recupera un utente dal database per ID"""
    return ottieni_db().execute('SELECT * FROM user WHERE id = ?', (id_utente,)).fetchone()

def ottieni_utente_per_nome(nome_utente):
    """Recupera un utente dal database per nome utente"""
    return ottieni_db().execute('SELECT * FROM user WHERE username = ?', (nome_utente,)).fetchone()

def crea_utente(nome_utente, password):
    """
    Crea un nuovo utente nel database.
    Ritorna True se la creazione è riuscita, False altrimenti (es. nome utente duplicato).
    """
    db = ottieni_db()
    try:
        db.execute('INSERT INTO user (username, password) VALUES (?, ?)', (nome_utente, password))
        db.commit()
        return True
    except:
        # L'eccezione viene generata se il nome utente è già presente (UNIQUE constraint)
        return False