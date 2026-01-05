from app.db import get_db

def get_all_teams():
    return get_db().execute('SELECT * FROM team ORDER BY name').fetchall()

def create_team(name, city):
    db = get_db()
    db.execute('INSERT INTO team (name, city) VALUES (?, ?)', (name, city))
    db.commit()