from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from app.repositories import user_repository

bp = Blueprint('auth', __name__, url_prefix='/auth')# Blueprint per le rotte di autenticazione

@bp.before_app_request
def carica_utente_loggato():
    """Carica l'utente dalla sessione a ogni richiesta"""
    id_utente = session.get('id_utente')
    g.utente = user_repository.ottieni_utente_per_id(id_utente) if id_utente else None

@bp.route('/registrazione', methods=('GET', 'POST'))
def registrazione():
    """Gestisce la registrazione di un nuovo utente"""
    if request.method == 'POST':
        nome_utente, password = request.form['nome_utente'], request.form['password']
        # Crea l'utente con la password hashata
        if user_repository.crea_utente(nome_utente, generate_password_hash(password)):
            return redirect(url_for('auth.accedi'))
        flash(f"Utente {nome_utente} già esistente.")
    return render_template('auth/registrazione.html')

@bp.route('/accedi', methods=('GET', 'POST'))
def accedi():
    """Gestisce l'accesso dell'utente"""
    if request.method == 'POST':
        # Recupera l'utente dal database
        utente = user_repository.ottieni_utente_per_nome(request.form['nome_utente'])
        # Verifica le credenziali
        if utente and check_password_hash(utente['password'], request.form['password']):
            session.clear()
            session['id_utente'] = utente['id']
            return redirect(url_for('main.indice'))
        flash("Credenziali errate.")
    return render_template('auth/accedi.html')

@bp.route('/esci')
def esci():
    """Effettua il logout dell'utente"""
    session.clear()
    return redirect(url_for('main.indice'))