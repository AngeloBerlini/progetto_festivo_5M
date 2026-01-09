from app.db import ottieni_db

def ottieni_tutte_squadre():
    """Recupera tutte le squadre ordinate per nome"""
    return ottieni_db().execute('SELECT * FROM team ORDER BY name').fetchall()

def ottieni_squadre_per_campionato(id_campionato):
    """Recupera tutte le squadre di un campionato specifico"""
    return ottieni_db().execute('SELECT * FROM team WHERE campionato_id = ? ORDER BY name', (id_campionato,)).fetchall()

def ottieni_squadra_per_id(id_squadra):
    """Recupera una squadra specifica per ID"""
    return ottieni_db().execute('SELECT * FROM team WHERE id = ?', (id_squadra,)).fetchone()

def crea_squadra(nome, città, id_utente, id_campionato):
    """
    Crea una nuova squadra e inizializza le sue statistiche.
    Crea anche un record in team_stats per tracciare partite, gol segnati e subiti.
    """
    db = ottieni_db()
    cursore = db.cursor()
    
    # Inserisci la squadra
    cursore.execute('INSERT INTO team (name, city, created_by, campionato_id) VALUES (?, ?, ?, ?)', (nome, città, id_utente, id_campionato))
    id_squadra = cursore.lastrowid
    
    # Crea il record di statistiche per la squadra
    cursore.execute('INSERT INTO team_stats (team_id, matches_played, goals_for, goals_against) VALUES (?, 0, 0, 0)', (id_squadra,))
    
    db.commit()

def aggiorna_squadra(id_squadra, nome, città):
    """Aggiorna il nome e la città di una squadra"""
    db = ottieni_db()
    db.execute('UPDATE team SET name = ?, city = ? WHERE id = ?', (nome, città, id_squadra))
    db.commit()

def elimina_squadra(id_squadra):
    """
    Elimina una squadra e tutti i dati associati:
    - Statistiche della squadra
    - Partite in cui ha giocato
    - La squadra stessa
    """
    db = ottieni_db()
    cursore = db.cursor()
    
    # Elimina le statistiche
    cursore.execute('DELETE FROM team_stats WHERE team_id = ?', (id_squadra,))
    
    # Elimina le partite associate (sia come squadra di casa che ospite)
    cursore.execute('DELETE FROM match WHERE home_team_id = ? OR away_team_id = ?', (id_squadra, id_squadra))
    
    # Elimina la squadra
    cursore.execute('DELETE FROM team WHERE id = ?', (id_squadra,))
    
    db.commit()