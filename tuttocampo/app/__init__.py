import os
from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'tuttocampo.sqlite'),
        SESSION_PERMANENT=False,
        SESSION_TYPE='filesystem',
    )

    # Inizializzazione DB
    from . import db
    db.init_app(app)

    # Registrazione Blueprints
    from .blueprints import main, auth
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)

    return app