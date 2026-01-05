from app.db import get_db

def get_all_campionati():
    return get_db().execute('SELECT * FROM campionato ORDER BY nome').fetchall()

def get_campionato_by_id(campionato_id):
    return get_db().execute('SELECT * FROM campionato WHERE id = ?', (campionato_id,)).fetchone()
