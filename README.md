# Tuttocampo - Gestione Campionato Calcistico

Applicazione web per gestire un campionato calcistico con 20 squadre, risultati delle partite e classifica aggiornata in tempo reale.

##  Funzionalità

- Autenticazione (registrazione e login)
- Gestione squadre con statistiche (partite, gol fatti/subiti, differenza reti)
- Aggiunta risultati con aggiornamento automatico della classifica
- Classifica ordinata per punti, differenza reti e gol segnati
- Visualizzazione storico partite

##  Installazione

### 1. Installare dipendenze
```bash
pip install -r requirements.txt
```

### 2. Inizializzare il database
```bash
python tuttocampo/setup_db.py
```

### 3. Avviare l'applicazione
```bash
python tuttocampo/run.py
```

L'app sarà disponibile a: **http://127.0.0.1:5000**

## Come Usare

1. **Registrazione/Login**: Crea un account o accedi
2. **Aggiungere squadre**: Vai al menu "Squadre" e clicca " + Aggiungi Squadra" per creare le tue squadre
3. **Visualizzare statistiche**: Nella pagina "Squadre" vedi tutte le statistiche (partite, gol, differenza reti)
4. **Aggiungere risultati**: Dalla Home clicca " + Aggiungi Risultato" per inserire una partita
5. **Classifica**: Si aggiorna automaticamente in base ai risultati

##  Iniziare

Il database parte vuoto. Devi aggiungere le squadre tu stesso dal menu "Squadre". Le statistiche si creano automaticamente quando aggiungi una squadra e si aggiornano quando inserisci i risultati delle partite.

##  Struttura

```
tuttocampo/
├── app/
│   ├── blueprints/       # auth.py, main.py
│   ├── repositories/     # user, team, match
│   ├── templates/        # HTML files
│   ├── db.py
│   └── schema.sql
├── run.py
└── setup_db.py
```

## Stack

- Flask (Python backend)
- SQLite3 (database)
- Jinja2 (template)
- Werkzeug (password security)

---
**Buon campionato!**