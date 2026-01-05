from app.db import get_db

def get_all_matches():
    return get_db().execute(
        'SELECT m.*, t1.name as home_name, t2.name as away_name '
        'FROM match m '
        'JOIN team t1 ON m.home_team_id = t1.id '
        'JOIN team t2 ON m.away_team_id = t2.id '
        'ORDER BY m.match_date DESC'
    ).fetchall()

def get_standings():
    """Ritorna la classifica completa con punti, partite, gol fatti/subiti e differenza reti"""
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
    LEFT JOIN match m ON (m.home_team_id = t.id OR m.away_team_id = t.id)
    GROUP BY t.id, t.name
    ORDER BY points DESC, goal_difference DESC, goals_for DESC
    """
    return db.execute(query).fetchall()

def create_match(home_team_id, away_team_id, home_score, away_score, match_date):
    db = get_db()
    
    # Inserisci la partita
    db.execute(
        'INSERT INTO match (home_team_id, away_team_id, home_score, away_score, match_date) VALUES (?, ?, ?, ?, ?)',
        (home_team_id, away_team_id, home_score, away_score, match_date)
    )
    
    # Aggiorna le statistiche della squadra di casa
    db.execute(
        'UPDATE team_stats SET matches_played = matches_played + 1, goals_for = goals_for + ?, goals_against = goals_against + ? WHERE team_id = ?',
        (home_score, away_score, home_team_id)
    )
    
    # Aggiorna le statistiche della squadra in trasferta
    db.execute(
        'UPDATE team_stats SET matches_played = matches_played + 1, goals_for = goals_for + ?, goals_against = goals_against + ? WHERE team_id = ?',
        (away_score, home_score, away_team_id)
    )
    
    db.commit()

def get_team_stats():
    """Ritorna le statistiche di tutte le squadre con i gol segnati e subiti"""
    return get_db().execute(
        'SELECT t.id, t.name, t.city, '
        'COALESCE(s.matches_played, 0) as matches_played, '
        'COALESCE(s.goals_for, 0) as goals_for, '
        'COALESCE(s.goals_against, 0) as goals_against '
        'FROM team t LEFT JOIN team_stats s ON t.id = s.team_id '
        'ORDER BY goals_for DESC'
    ).fetchall()