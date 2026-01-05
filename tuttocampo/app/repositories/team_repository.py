from app.db import get_db

def get_all_teams():
    return get_db().execute('SELECT * FROM team ORDER BY name').fetchall()

def get_teams_by_campionato(campionato_id):
    return get_db().execute('SELECT * FROM team WHERE campionato_id = ? ORDER BY name', (campionato_id,)).fetchall()

def get_team_by_id(team_id):
    return get_db().execute('SELECT * FROM team WHERE id = ?', (team_id,)).fetchone()

def create_team(name, city, user_id, campionato_id):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('INSERT INTO team (name, city, created_by, campionato_id) VALUES (?, ?, ?, ?)', (name, city, user_id, campionato_id))
    team_id = cursor.lastrowid
    
    cursor.execute('INSERT INTO team_stats (team_id, matches_played, goals_for, goals_against) VALUES (?, 0, 0, 0)', (team_id,))
    
    db.commit()

def update_team(team_id, name, city):
    db = get_db()
    db.execute('UPDATE team SET name = ?, city = ? WHERE id = ?', (name, city, team_id))
    db.commit()

def delete_team(team_id):
    db = get_db()
    cursor = db.cursor()
    
    # Elimina le statistiche
    cursor.execute('DELETE FROM team_stats WHERE team_id = ?', (team_id,))
    
    # Elimina le partite associate
    cursor.execute('DELETE FROM match WHERE home_team_id = ? OR away_team_id = ?', (team_id, team_id))
    
    # Elimina la squadra
    cursor.execute('DELETE FROM team WHERE id = ?', (team_id,))
    
    db.commit()