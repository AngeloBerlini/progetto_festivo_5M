from app.db import get_db

def get_all_teams():
    return get_db().execute('SELECT * FROM team ORDER BY name').fetchall()

def create_team(name, city):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('INSERT INTO team (name, city) VALUES (?, ?)', (name, city))
    team_id = cursor.lastrowid
    
    cursor.execute('INSERT INTO team_stats (team_id, matches_played, goals_for, goals_against) VALUES (?, 0, 0, 0)', (team_id,))
    
    db.commit()