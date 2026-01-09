from flask import Blueprint, render_template, request, redirect, url_for, g, flash, session
from app.repositories import match_repository, team_repository, campionato_repository

bp = Blueprint('main', __name__)

@bp.route('/')
def indice():
    """Pagina principale con classifica e partite del campionato selezionato"""
    # Recupera l'ID del campionato dalla sessione o dai parametri della richiesta
    id_campionato = request.args.get('id_campionato', session.get('id_campionato'))
    
    # Se non c'è un campionato selezionato, usa il primo disponibile
    if not id_campionato:
        campionati = campionato_repository.ottieni_tutti_campionati()
        if campionati:
            id_campionato = campionati[0]['id']
            session['id_campionato'] = id_campionato
    else:
        session['id_campionato'] = int(id_campionato)
        id_campionato = int(id_campionato)
    
    campionati = campionato_repository.ottieni_tutti_campionati()
    campionato_attuale = campionato_repository.ottieni_campionato_per_id(id_campionato) if id_campionato else None
    
    return render_template('index.html', 
                           classifica=match_repository.ottieni_classifica(id_campionato),
                           partite=match_repository.ottieni_partite_per_campionato(id_campionato),
                           campionati=campionati,
                           campionato_attuale=campionato_attuale)

@bp.route('/squadre')
def squadre():
    """Visualizza tutte le squadre del campionato selezionato con le loro statistiche"""
    id_campionato = session.get('id_campionato')
    if not id_campionato:
        campionati = campionato_repository.ottieni_tutti_campionati()
        if campionati:
            id_campionato = campionati[0]['id']
            session['id_campionato'] = id_campionato
    
    # Recupera le statistiche delle squadre
    statistiche = match_repository.ottieni_statistiche_squadre(id_campionato)
    
    return render_template('squadre.html', 
                           squadre=team_repository.ottieni_squadre_per_campionato(id_campionato), 
                           statistiche=statistiche,
                           id_campionato=id_campionato)

@bp.route('/squadre/nuova', methods=('GET', 'POST'))
def aggiungi_squadra():
    """Crea una nuova squadra (solo per utenti autenticati)"""
    if g.utente is None:
        return redirect(url_for('auth.accedi'))
    
    id_campionato = session.get('id_campionato')
    if not id_campionato:
        campionati = campionato_repository.ottieni_tutti_campionati()
        if campionati:
            id_campionato = campionati[0]['id']
    
    if request.method == 'POST':
        nome = request.form['nome']
        città = request.form['città']
        team_repository.crea_squadra(nome, città, g.utente['id'], id_campionato)
        flash("Squadra aggiunta con successo!")
        return redirect(url_for('main.squadre'))
        
    return render_template('aggiungi_squadra.html')

@bp.route('/squadre/<int:id_squadra>/modifica', methods=('GET', 'POST'))
def modifica_squadra(id_squadra):
    """Modifica una squadra (solo il creatore può modificarla)"""
    if g.utente is None:
        return redirect(url_for('auth.accedi'))
    
    squadra = team_repository.ottieni_squadra_per_id(id_squadra)
    
    if squadra is None:
        flash("Squadra non trovata!")
        return redirect(url_for('main.squadre'))
    
    if squadra['created_by'] != g.utente['id']:
        flash("Non puoi modificare una squadra creata da un altro utente!")
        return redirect(url_for('main.squadre'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        città = request.form['città']
        team_repository.aggiorna_squadra(id_squadra, nome, città)
        flash("Squadra modificata con successo!")
        return redirect(url_for('main.squadre'))
    
    return render_template('modifica_squadra.html', squadra=squadra)

@bp.route('/squadre/<int:id_squadra>/elimina', methods=('POST',))
def elimina_squadra(id_squadra):
    """Elimina una squadra (solo il creatore può eliminarla)"""
    if g.utente is None:
        return redirect(url_for('auth.accedi'))
    
    squadra = team_repository.ottieni_squadra_per_id(id_squadra)
    if squadra is None:
        flash("Squadra non trovata!")
        return redirect(url_for('main.squadre'))
    
    if squadra['created_by'] != g.utente['id']:
        flash("Non puoi eliminare una squadra creata da un altro utente!")
        return redirect(url_for('main.squadre'))
    
    team_repository.elimina_squadra(id_squadra)
    flash(f"Squadra '{squadra['name']}' eliminata con successo!")
    
    return redirect(url_for('main.squadre'))

@bp.route('/partite/nuova', methods=('GET', 'POST'))
def aggiungi_partita():
    """Crea una nuova partita (solo per utenti autenticati)"""
    if g.utente is None:
        return redirect(url_for('auth.accedi'))
    
    id_campionato = session.get('id_campionato')
    if not id_campionato:
        campionati = campionato_repository.ottieni_tutti_campionati()
        if campionati:
            id_campionato = campionati[0]['id']
        
    if request.method == 'POST':
        id_squadra_casa = request.form['id_squadra_casa']
        id_squadra_ospiti = request.form['id_squadra_ospiti']
        gol_casa = request.form['gol_casa']
        gol_ospiti = request.form['gol_ospiti']
        data_partita = request.form['data_partita']
        
        # Validazione: le due squadre non possono essere uguali
        if id_squadra_casa == id_squadra_ospiti:
            flash("Le due squadre non possono essere uguali!")
            return redirect(url_for('main.aggiungi_partita'))
        
        match_repository.crea_partita(id_squadra_casa, id_squadra_ospiti, gol_casa, gol_ospiti, data_partita, g.utente['id'], id_campionato)
        flash("Partita aggiunta con successo!")
        return redirect(url_for('main.indice'))
        
    return render_template('aggiungi_partita.html', squadre=team_repository.ottieni_squadre_per_campionato(id_campionato))

@bp.route('/partite/<int:id_partita>/modifica', methods=('GET', 'POST'))
def modifica_partita(id_partita):
    """Modifica una partita (solo il creatore può modificarla)"""
    if g.utente is None:
        return redirect(url_for('auth.accedi'))
    
    partita = match_repository.ottieni_partita_per_id(id_partita)
    
    if partita is None:
        flash("Partita non trovata!")
        return redirect(url_for('main.indice'))
    
    if partita['created_by'] != g.utente['id']:
        flash("Non puoi modificare una partita creata da un altro utente!")
        return redirect(url_for('main.indice'))
    
    if request.method == 'POST':
        gol_casa = request.form['gol_casa']
        gol_ospiti = request.form['gol_ospiti']
        data_partita = request.form['data_partita']
        
        match_repository.aggiorna_partita(id_partita, gol_casa, gol_ospiti, data_partita)
        flash("Partita modificata con successo!")
        return redirect(url_for('main.indice'))
    
    return render_template('modifica_partita.html', partita=partita, squadre=team_repository.ottieni_tutte_squadre())

@bp.route('/partite/<int:id_partita>/elimina', methods=('POST',))
def elimina_partita(id_partita):
    """Elimina una partita (solo il creatore può eliminarla)"""
    if g.utente is None:
        return redirect(url_for('auth.accedi'))
    
    partita = match_repository.ottieni_partita_per_id(id_partita)
    if partita is None:
        flash("Partita non trovata!")
        return redirect(url_for('main.indice'))
    
    if partita['created_by'] != g.utente['id']:
        flash("Non puoi eliminare una partita creata da un altro utente!")
        return redirect(url_for('main.indice'))
    
    match_repository.elimina_partita(id_partita)
    flash(f"Partita '{partita['home_name']} - {partita['away_name']}' eliminata con successo!")
    
    return redirect(url_for('main.indice'))