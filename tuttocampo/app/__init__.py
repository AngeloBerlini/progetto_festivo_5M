import os
from flask import Flask

def crea_app():
    """
    Crea e configura l'applicazione Flask.
    Inizializza il database e registra i blueprint per l'autenticazione e le pagine principali.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'tuttocampo.sqlite'),
        SESSION_PERMANENT=False,
        SESSION_TYPE='filesystem',
    )

    # Inizializzazione del database
    from . import db
    db.inizializza_app(app)

    # Registrazione dei blueprints dalla cartella blueprints
    from .blueprints import main, auth
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)

    return app

    