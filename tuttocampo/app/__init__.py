import os
from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # MODIFICA QUI:
    # os.environ.get('NOME_VAR', 'valore_default')
    # Se trova SECRET_KEY nel sistema/file .env la usa.
    # Altrimenti usa 'dev' (utile per non bloccarci se manca il file).
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE=os.path.join(app.instance_path, 'tuttocampo.sqlite'),
    )
    
    # ... resto del codice ...
    # Inizializzazione del database
    from . import db
    db.inizializza_app(app)

    # Registrazione dei blueprints dalla cartella blueprints
    from .blueprints import main, auth
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)

    return app

    