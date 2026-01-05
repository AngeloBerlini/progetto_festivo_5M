from flask import Blueprint, render_template,request,redirect,url_for,g,flash
from app.repositories import match_repository, team_repository

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html', 
                           classifica=match_repository.get_standings(),
                           partite=match_repository.get_all_matches())

@bp.route('/squadre')
def teams():
    return render_template('teams.html', squadre=team_repository.get_all_teams(), stats=match_repository.get_team_stats())

@bp.route('/squadre/nuova', methods=('GET', 'POST'))
def add_team():
    if g.user is None:
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        team_repository.create_team(name, city)
        return redirect(url_for('main.teams'))
        
    return render_template('add_team.html')

@bp.route('/partite/nuova', methods=('GET', 'POST'))
def add_match():
    if g.user is None:
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        home_team_id = request.form['home_team_id']
        away_team_id = request.form['away_team_id']
        home_score = request.form['home_score']
        away_score = request.form['away_score']
        match_date = request.form['match_date']
        
        if home_team_id == away_team_id:
            flash("Le due squadre non possono essere uguali!")
            return redirect(url_for('main.add_match'))
        
        match_repository.create_match(home_team_id, away_team_id, home_score, away_score, match_date)
        flash("Partita aggiunta con successo!")
        return redirect(url_for('main.index'))
        
    return render_template('add_match.html', squadre=team_repository.get_all_teams())