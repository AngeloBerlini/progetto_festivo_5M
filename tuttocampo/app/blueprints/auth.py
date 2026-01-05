from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from app.repositories import user_repository

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = user_repository.get_user_by_id(user_id) if user_id else None

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']
        if user_repository.create_user(username, generate_password_hash(password)):
            return redirect(url_for('auth.login'))
        flash(f"Utente {username} già esistente.")
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        user = user_repository.get_user_by_username(request.form['username'])
        if user and check_password_hash(user['password'], request.form['password']):
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('main.index'))
        flash("Credenziali errate.")
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))