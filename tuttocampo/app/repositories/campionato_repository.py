from app.db import ottieni_db

def ottieni_tutti_campionati():
    """Recupera tutti i campionati ordinati per nome"""
    return ottieni_db().execute('SELECT * FROM campionato ORDER BY nome').fetchall()

def ottieni_campionato_per_id(id_campionato):
    """Recupera un campionato specifico per ID"""
    return ottieni_db().execute('SELECT * FROM campionato WHERE id = ?', (id_campionato,)).fetchone()
