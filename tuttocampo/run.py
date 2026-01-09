from app import crea_app

app = crea_app()

if __name__ == '__main__':
    # Avvia l'applicazione Flask in modalità debug
    app.run(debug=True)