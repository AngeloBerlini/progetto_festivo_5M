from app.db import ottieni_db

def ottieni_tutte_partite():
    """Recupera tutte le partite con i nomi delle squadre"""
    return ottieni_db().execute(
        'SELECT m.*, t1.name as home_name, t2.name as away_name '
        'FROM match m '
        'JOIN team t1 ON m.home_team_id = t1.id '
        'JOIN team t2 ON m.away_team_id = t2.id '
        'ORDER BY m.match_date DESC'
    ).fetchall()

def ottieni_partite_per_campionato(id_campionato):
    """Recupera tutte le partite di un campionato specifico"""
    return ottieni_db().execute(
        'SELECT m.*, t1.name as home_name, t2.name as away_name '
        'FROM match m '
        'JOIN team t1 ON m.home_team_id = t1.id '
        'JOIN team t2 ON m.away_team_id = t2.id '
        'WHERE m.campionato_id = ? '
        'ORDER BY m.match_date DESC',
        (id_campionato,)
    ).fetchall()

def ottieni_classifica(id_campionato):#uso COALESCE per evitare valori nulli
    """
    Calcola e ritorna la classifica completa per un campionato.
    
    La classifica considera:
    - Punti: 3 per vittoria, 1 per pareggio, 0 per sconfitta
    - Differenza reti: gol segnati - gol subiti
    - Gol segnati (come criterio di spareggio)
    
    Il calcolo dei punti si fa dalle partite, non dalle statistiche, per maggior accuratezza.
    """
    db = ottieni_db()
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
    return db.execute(query, (id_campionato, id_campionato)).fetchall()

def crea_partita(id_squadra_casa, id_squadra_ospiti, gol_casa, gol_ospiti, data_partita, id_utente, id_campionato):
    """
    Crea una nuova partita e aggiorna le statistiche di entrambe le squadre.
    
    Incrementa:
    - Partite giocate per entrambe le squadre
    - Gol segnati e subiti secondo il risultato
    """
    db = ottieni_db()
    
    # Inserisci la partita
    db.execute(
        'INSERT INTO match (home_team_id, away_team_id, home_score, away_score, match_date, created_by, campionato_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (id_squadra_casa, id_squadra_ospiti, gol_casa, gol_ospiti, data_partita, id_utente, id_campionato)
    )
    
    # Aggiorna statistiche della squadra di casa
    db.execute(
        'UPDATE team_stats SET matches_played = matches_played + 1, goals_for = goals_for + ?, goals_against = goals_against + ? WHERE team_id = ?',
        (gol_casa, gol_ospiti, id_squadra_casa)
    )
    
    # Aggiorna statistiche della squadra ospite
    db.execute(
        'UPDATE team_stats SET matches_played = matches_played + 1, goals_for = goals_for + ?, goals_against = goals_against + ? WHERE team_id = ?',
        (gol_ospiti, gol_casa, id_squadra_ospiti)
    )
    
    db.commit()

def ottieni_statistiche_squadre(id_campionato=None):
    """
    Ritorna le statistiche di tutte le squadre (gol segnati, subiti, partite giocate).
    Se id_campionato è specificato, filtra per quel campionato e ordina per gol segnati.
    """
    if id_campionato:
        return ottieni_db().execute(
            'SELECT t.id, t.name, t.city, t.created_by, '
            'COALESCE(s.matches_played, 0) as matches_played, '
            'COALESCE(s.goals_for, 0) as goals_for, '
            'COALESCE(s.goals_against, 0) as goals_against '
            'FROM team t LEFT JOIN team_stats s ON t.id = s.team_id '
            'WHERE t.campionato_id = ? '
            'ORDER BY goals_for DESC',
            (id_campionato,)
        ).fetchall()
    else:
        return ottieni_db().execute(
            'SELECT t.id, t.name, t.city, t.created_by, '
            'COALESCE(s.matches_played, 0) as matches_played, '
            'COALESCE(s.goals_for, 0) as goals_for, '
            'COALESCE(s.goals_against, 0) as goals_against '
            'FROM team t LEFT JOIN team_stats s ON t.id = s.team_id '
            'ORDER BY goals_for DESC'
        ).fetchall()

def ottieni_partita_per_id(id_partita):
    """Recupera una partita specifica con i nomi delle squadre"""
    return ottieni_db().execute(
        'SELECT m.*, t1.name as home_name, t2.name as away_name '
        'FROM match m '
        'JOIN team t1 ON m.home_team_id = t1.id '
        'JOIN team t2 ON m.away_team_id = t2.id '
        'WHERE m.id = ?', 
        (id_partita,)
    ).fetchone()

def aggiorna_partita(id_partita, gol_casa, gol_ospiti, data_partita):
    """
    Aggiorna una partita e corregge le statistiche delle squadre.
    
    Sottrae i vecchi gol dalle statistiche e aggiunge i nuovi per mantenere l'accuratezza.
    """
    db = ottieni_db()
    
    # Recupera la partita originale per conoscere i vecchi valori
    partita = ottieni_partita_per_id(id_partita)
    vecchi_gol_casa = partita['home_score']
    vecchi_gol_ospiti = partita['away_score']
    id_squadra_casa = partita['home_team_id']
    id_squadra_ospiti = partita['away_team_id']
    
    # Aggiorna la partita
    db.execute(
        'UPDATE match SET home_score = ?, away_score = ?, match_date = ? WHERE id = ?',
        (gol_casa, gol_ospiti, data_partita, id_partita)
    )
    
    # Aggiorna le statistiche della squadra di casa (sottrae i vecchi valori e aggiunge i nuovi)
    db.execute(
        'UPDATE team_stats SET goals_for = goals_for - ? + ?, goals_against = goals_against - ? + ? WHERE team_id = ?',
        (vecchi_gol_casa, gol_casa, vecchi_gol_ospiti, gol_ospiti, id_squadra_casa)
    )
    
    # Aggiorna le statistiche della squadra ospite
    db.execute(
        'UPDATE team_stats SET goals_for = goals_for - ? + ?, goals_against = goals_against - ? + ? WHERE team_id = ?',
        (vecchi_gol_ospiti, gol_ospiti, vecchi_gol_casa, gol_casa, id_squadra_ospiti)
    )
    
    db.commit()

def elimina_partita(id_partita):
    """
    Elimina una partita e sottrae i gol dalle statistiche delle squadre.
    """
    db = ottieni_db()
    cursore = db.cursor()
    
    # Recupera i dati della partita
    partita = ottieni_partita_per_id(id_partita)
    id_squadra_casa = partita['home_team_id']
    id_squadra_ospiti = partita['away_team_id']
    gol_casa = partita['home_score']
    gol_ospiti = partita['away_score']
    
    # Sottrai i gol dalle statistiche della squadra di casa
    cursore.execute(
        'UPDATE team_stats SET matches_played = matches_played - 1, goals_for = goals_for - ?, goals_against = goals_against - ? WHERE team_id = ?',
        (gol_casa, gol_ospiti, id_squadra_casa)
    )
    
    # Sottrai i gol dalle statistiche della squadra ospite
    cursore.execute(
        'UPDATE team_stats SET matches_played = matches_played - 1, goals_for = goals_for - ?, goals_against = goals_against - ? WHERE team_id = ?',
        (gol_ospiti, gol_casa, id_squadra_ospiti)
    )
    
    # Elimina la partita
    cursore.execute('DELETE FROM match WHERE id = ?', (id_partita,))
    
    db.commit()