from flask import Blueprint, render_template,request,redirect,url_for,g,flash,session
from app.repositories import match_repository, team_repository, campionato_repository

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # Get campionato from session or request, default to first
    campionato_id = request.args.get('campionato_id', session.get('campionato_id'))
    
    if not campionato_id:
        campionati = campionato_repository.get_all_campionati()
        if campionati:
            campionato_id = campionati[0]['id']
            session['campionato_id'] = campionato_id
    else:
        session['campionato_id'] = int(campionato_id)
        campionato_id = int(campionato_id)
    
    campionati = campionato_repository.get_all_campionati()
    current_campionato = campionato_repository.get_campionato_by_id(campionato_id) if campionato_id else None
    
    return render_template('index.html', 
                           classifica=match_repository.get_standings(campionato_id),
                           partite=match_repository.get_matches_by_campionato(campionato_id),
                           campionati=campionati,
                           current_campionato=current_campionato)

@bp.route('/squadre')
def teams():
    campionato_id = session.get('campionato_id')
    if not campionato_id:
        campionati = campionato_repository.get_all_campionati()
        if campionati:
            campionato_id = campionati[0]['id']
            session['campionato_id'] = campionato_id
    
    # Get team stats for current campionato
    stats = match_repository.get_team_stats(campionato_id)
    
    return render_template('teams.html', 
                           squadre=team_repository.get_teams_by_campionato(campionato_id), 
                           stats=stats,
                           campionato_id=campionato_id)

@bp.route('/squadre/nuova', methods=('GET', 'POST'))
def add_team():
    if g.user is None:
        return redirect(url_for('auth.login'))
    
    campionato_id = session.get('campionato_id')
    if not campionato_id:
        campionati = campionato_repository.get_all_campionati()
        if campionati:
            campionato_id = campionati[0]['id']
    
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        team_repository.create_team(name, city, g.user['id'], campionato_id)
        flash("Squadra aggiunta con successo!")
        return redirect(url_for('main.teams'))
        
    return render_template('add_team.html')

@bp.route('/squadre/<int:team_id>/modifica', methods=('GET', 'POST'))
def edit_team(team_id):
    if g.user is None:
        return redirect(url_for('auth.login'))
    
    team = team_repository.get_team_by_id(team_id)
    
    if team is None:
        flash("Squadra non trovata!")
        return redirect(url_for('main.teams'))
    
    if team['created_by'] != g.user['id']:
        flash("Non puoi modificare una squadra creata da un altro utente!")
        return redirect(url_for('main.teams'))
    
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        team_repository.update_team(team_id, name, city)
        flash("Squadra modificata con successo!")
        return redirect(url_for('main.teams'))
    
    return render_template('edit_team.html', team=team)

@bp.route('/squadre/<int:team_id>/elimina', methods=('POST',))
def delete_team(team_id):
    if g.user is None:
        return redirect(url_for('auth.login'))
    
    team = team_repository.get_team_by_id(team_id)
    if team is None:
        flash("Squadra non trovata!")
        return redirect(url_for('main.teams'))
    
    if team['created_by'] != g.user['id']:
        flash("Non puoi eliminare una squadra creata da un altro utente!")
        return redirect(url_for('main.teams'))
    
    team_repository.delete_team(team_id)
    flash(f"Squadra '{team['name']}' eliminata con successo!")
    
    return redirect(url_for('main.teams'))

@bp.route('/partite/nuova', methods=('GET', 'POST'))
def add_match():
    if g.user is None:
        return redirect(url_for('auth.login'))
    
    campionato_id = session.get('campionato_id')
    if not campionato_id:
        campionati = campionato_repository.get_all_campionati()
        if campionati:
            campionato_id = campionati[0]['id']
        
    if request.method == 'POST':
        home_team_id = request.form['home_team_id']
        away_team_id = request.form['away_team_id']
        home_score = request.form['home_score']
        away_score = request.form['away_score']
        match_date = request.form['match_date']
        
        if home_team_id == away_team_id:
            flash("Le due squadre non possono essere uguali!")
            return redirect(url_for('main.add_match'))
        
        match_repository.create_match(home_team_id, away_team_id, home_score, away_score, match_date, g.user['id'], campionato_id)
        flash("Partita aggiunta con successo!")
        return redirect(url_for('main.index'))
        
    return render_template('add_match.html', squadre=team_repository.get_teams_by_campionato(campionato_id))

@bp.route('/partite/<int:match_id>/modifica', methods=('GET', 'POST'))
def edit_match(match_id):
    if g.user is None:
        return redirect(url_for('auth.login'))
    
    match = match_repository.get_match_by_id(match_id)
    
    if match is None:
        flash("Partita non trovata!")
        return redirect(url_for('main.index'))
    
    if match['created_by'] != g.user['id']:
        flash("Non puoi modificare una partita creata da un altro utente!")
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        home_score = request.form['home_score']
        away_score = request.form['away_score']
        match_date = request.form['match_date']
        
        match_repository.update_match(match_id, home_score, away_score, match_date)
        flash("Partita modificata con successo!")
        return redirect(url_for('main.index'))
    
    return render_template('edit_match.html', match=match, squadre=team_repository.get_all_teams())

@bp.route('/partite/<int:match_id>/elimina', methods=('POST',))
def delete_match(match_id):
    if g.user is None:
        return redirect(url_for('auth.login'))
    
    match = match_repository.get_match_by_id(match_id)
    if match is None:
        flash("Partita non trovata!")
        return redirect(url_for('main.index'))
    
    if match['created_by'] != g.user['id']:
        flash("Non puoi eliminare una partita creata da un altro utente!")
        return redirect(url_for('main.index'))
    
    match_repository.delete_match(match_id)
    flash(f"Partita '{match['home_name']} - {match['away_name']}' eliminata con successo!")
    
    return redirect(url_for('main.index'))