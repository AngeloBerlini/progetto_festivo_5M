from app.db import get_db

def get_user_by_id(user_id):
    return get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()

def get_user_by_username(username):
    return get_db().execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

def create_user(username, password):
    db = get_db()
    try:
        db.execute('INSERT INTO user (username, password) VALUES (?, ?)', (username, password))
        db.commit()
        return True
    except:
        return False