#  Tuttocampo - Gestione Campionato Calcistico

Applicazione web moderna per creare e gestire un campionato calcistico. Aggiungi squadre, inserisci risultati e visualizza una classifica aggiornata in tempo reale con statistiche complete.

## Caratteristiche

-  **Autenticazione**: Sistema di registrazione e login sicuro
-  **Classifica Dinamica**: Ordinamento automatico per punti, differenza reti e gol segnati
-  **Gestione Risultati**: Inserimento partite con aggiornamento istantaneo delle statistiche
-  **Statistiche Dettagliate**: Partite giocate, gol fatti/subiti, differenza reti
-  **Squadre Custom**: Crea le tue squadre e gestisci il campionato come vuoi

##  Quick Start

### Prerequisiti
- Python 3.8+
- pip

### Setup (3 step)

1. **Installa dipendenze**
```bash
pip install -r requirements.txt
```

2. **Crea il database**
```bash
python tuttocampo/setup_db.py
```

3. **Avvia l'app**
```bash
python tuttocampo/run.py
```

Visita: **http://127.0.0.1:5000**

## Guida Rapida

###  Registrati
- Clicca "Registrati" nel menu
- Crea username e password

###  Aggiungi Squadre
- Vai al menu "Squadre"
- Clicca " + Aggiungi Squadra"
- Inserisci nome e città

###  Aggiungi Risultati
- Dalla Home clicca " Aggiungi Risultato"
- Seleziona squadra casa/trasferta
- Inserisci gol e data
- Salva - la classifica si aggiorna!

###  Visualizza Statistiche
- **Home**: Classifica con Pos | Squadra | Partite | Punti | GF | GS | DR
- **Squadre**: Tabella dettagliata di tutte le squadre
- **Risultati**: Storico di tutte le partite giocate

##  Struttura Progetto

```
tuttocampo/
├── app/
│   ├── blueprints/
│   │   ├── auth.py          (login, registrazione)
│   │   └── main.py          (rotte principali)
│   ├── repositories/
│   │   ├── user_repository.py
│   │   ├── team_repository.py
│   │   └── match_repository.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── teams.html
│   │   ├── add_team.html
│   │   ├── add_match.html
│   │   └── auth/
│   ├── db.py
│   └── schema.sql
├── run.py
└── setup_db.py
```

##  Stack

| Componente | Tecnologia |
|-----------|-----------|
| Backend | Flask |
| Database | SQLite3 |
| Template | Jinja2 |
| Security | Werkzeug |

##  Database

**Tabelle:**
- `user` - Utenti registrati
- `team` - Squadre
- `match` - Risultati partite
- `team_stats` - Statistiche squadre (aggiornate automaticamente)

Le statistiche si aggiornano automaticamente quando:
-  Aggiungi una squadra → creiamo il record stats
-  Inserisci una partita → aggiorniamo gol fatti/subiti di entrambe

**Porta 5000 occupata:**
Modifica `tuttocampo/run.py`:
```python
app.run(debug=True, port=5001)
```

##  Note

- Database parte vuoto - aggiungi squadre manualmente
- Password hashate con Werkzeug
- Session-based authentication
- Debug mode attivo (disabilitare in produzione)

---

**Crea il tuo campionato!**