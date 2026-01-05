from app.db import get_db

def get_all_matches():
    return get_db().execute(
        'SELECT m.*, t1.name as home_name, t2.name as away_name '
        'FROM match m '
        'JOIN team t1 ON m.home_team_id = t1.id '
        'JOIN team t2 ON m.away_team_id = t2.id '
        'ORDER BY m.match_date DESC'
    ).fetchall()

def get_matches_by_campionato(campionato_id):
    return get_db().execute(
        'SELECT m.*, t1.name as home_name, t2.name as away_name '
        'FROM match m '
        'JOIN team t1 ON m.home_team_id = t1.id '
        'JOIN team t2 ON m.away_team_id = t2.id '
        'WHERE m.campionato_id = ? '
        'ORDER BY m.match_date DESC',
        (campionato_id,)
    ).fetchall()

def get_standings(campionato_id):
    """Ritorna la classifica completa per un campionato specifico"""
    db = get_db()
    query = """
    SELECT 
        t.id,
        t.name as team_name,
        COALESCE(s.matches_played, 0) as matches_played,
        COALESCE(s.goals_for, 0) as goals_for,
        COALESCE(s.goals_against, 0) as goals_against,
        COALESCE(s.goals_for, 0) - COALESCE(s.goals_against, 0) as goal_difference,
        COALESCE(SUM(CASE 
            WHEN m.home_team_id = t.id AND m.home_score > m.away_score THEN 3
            WHEN m.away_team_id = t.id AND m.away_score > m.home_score THEN 3
            WHEN m.home_team_id = t.id AND m.home_score = m.away_score THEN 1
            WHEN m.away_team_id = t.id AND m.away_score = m.home_score THEN 1
            ELSE 0
        END), 0) as points
    FROM team t
    LEFT JOIN team_stats s ON t.id = s.team_id
    LEFT JOIN match m ON (m.home_team_id = t.id OR m.away_team_id = t.id) AND m.campionato_id = ?
    WHERE t.campionato_id = ?
    GROUP BY t.id, t.name
    ORDER BY points DESC, goal_difference DESC, goals_for DESC
    """
    return db.execute(query, (campionato_id, campionato_id)).fetchall()

def create_match(home_team_id, away_team_id, home_score, away_score, match_date, user_id, campionato_id):
    db = get_db()
    
    db.execute(
        'INSERT INTO match (home_team_id, away_team_id, home_score, away_score, match_date, created_by, campionato_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (home_team_id, away_team_id, home_score, away_score, match_date, user_id, campionato_id)
    )
    
    db.execute(
        'UPDATE team_stats SET matches_played = matches_played + 1, goals_for = goals_for + ?, goals_against = goals_against + ? WHERE team_id = ?',
        (home_score, away_score, home_team_id)
    )
    
    db.execute(
        'UPDATE team_stats SET matches_played = matches_played + 1, goals_for = goals_for + ?, goals_against = goals_against + ? WHERE team_id = ?',
        (away_score, home_score, away_team_id)
    )
    
    db.commit()

def get_team_stats(campionato_id=None):
    """Ritorna le statistiche di tutte le squadre (filtrate per campionato se specificato) con i gol segnati e subiti"""
    if campionato_id:
        return get_db().execute(
            'SELECT t.id, t.name, t.city, t.created_by, '
            'COALESCE(s.matches_played, 0) as matches_played, '
            'COALESCE(s.goals_for, 0) as goals_for, '
            'COALESCE(s.goals_against, 0) as goals_against '
            'FROM team t LEFT JOIN team_stats s ON t.id = s.team_id '
            'WHERE t.campionato_id = ? '
            'ORDER BY goals_for DESC',
            (campionato_id,)
        ).fetchall()
    else:
        return get_db().execute(
            'SELECT t.id, t.name, t.city, t.created_by, '
            'COALESCE(s.matches_played, 0) as matches_played, '
            'COALESCE(s.goals_for, 0) as goals_for, '
            'COALESCE(s.goals_against, 0) as goals_against '
            'FROM team t LEFT JOIN team_stats s ON t.id = s.team_id '
            'ORDER BY goals_for DESC'
        ).fetchall()

def get_match_by_id(match_id):
    return get_db().execute(
        'SELECT m.*, t1.name as home_name, t2.name as away_name '
        'FROM match m '
        'JOIN team t1 ON m.home_team_id = t1.id '
        'JOIN team t2 ON m.away_team_id = t2.id '
        'WHERE m.id = ?', 
        (match_id,)
    ).fetchone()

def update_match(match_id, home_score, away_score, match_date):
    db = get_db()
    
    # Recupera la partita originale per aggiornare le statistiche correttamente
    match = get_match_by_id(match_id)
    old_home_score = match['home_score']
    old_away_score = match['away_score']
    home_team_id = match['home_team_id']
    away_team_id = match['away_team_id']
    
    # Aggiorna la partita
    db.execute(
        'UPDATE match SET home_score = ?, away_score = ?, match_date = ? WHERE id = ?',
        (home_score, away_score, match_date, match_id)
    )
    
    # Aggiorna le statistiche (sottrae i vecchi valori e aggiunge i nuovi)
    db.execute(
        'UPDATE team_stats SET goals_for = goals_for - ? + ?, goals_against = goals_against - ? + ? WHERE team_id = ?',
        (old_home_score, home_score, old_away_score, away_score, home_team_id)
    )
    
    db.execute(
        'UPDATE team_stats SET goals_for = goals_for - ? + ?, goals_against = goals_against - ? + ? WHERE team_id = ?',
        (old_away_score, away_score, old_home_score, home_score, away_team_id)
    )
    
    db.commit()

def delete_match(match_id):
    db = get_db()
    cursor = db.cursor()
    
    # Recupera i dati della partita
    match = get_match_by_id(match_id)
    home_team_id = match['home_team_id']
    away_team_id = match['away_team_id']
    home_score = match['home_score']
    away_score = match['away_score']
    
    # Sottrai i gol dalle statistiche
    cursor.execute(
        'UPDATE team_stats SET matches_played = matches_played - 1, goals_for = goals_for - ?, goals_against = goals_against - ? WHERE team_id = ?',
        (home_score, away_score, home_team_id)
    )
    
    cursor.execute(
        'UPDATE team_stats SET matches_played = matches_played - 1, goals_for = goals_for - ?, goals_against = goals_against - ? WHERE team_id = ?',
        (away_score, home_score, away_team_id)
    )
    
    # Elimina la partita
    cursor.execute('DELETE FROM match WHERE id = ?', (match_id,))
    
    db.commit()