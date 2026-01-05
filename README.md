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

## 📖 Come Usare

1. **Registrazione/Login**: Crea un account o accedi
2. **Visualizzare squadre**: Vai al menu "Squadre" per vedere tutte le statistiche
3. **Aggiungere una squadra**: Clicca "➕ Aggiungi Squadra" (solo se loggato)
4. **Aggiungere un risultato**: Clicca "➕ Aggiungi Risultato" dalla Home
5. **Classifica**: La classifica si aggiorna automaticamente

## 📊 Squadre Preimpostate (20)

AC Milan, Inter, Juventus, Torino, Roma, Lazio, Napoli, Fiorentina, Atalanta, Sampdoria, Genoa, Venezia, Verona, Monza, Como, Lecce, Sassuolo, Empoli, Frosinone, Salernitana

Puoi aggiungerne altre dal menu!

## 📁 Struttura

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
**Buon campionato! ⚽🏆**