#  Tuttocampo - Gestione Campionato Calcistico

Applicazione web moderna per creare e gestire campionati calcistici. Scegli tra più campionati (Serie A, Serie B), aggiungi squadre, inserisci risultati e visualizza una classifica aggiornata in tempo reale con statistiche complete.

## Caratteristiche

-  **Multi-Campionato**: Scegli tra Serie A e Serie B dalla home page
-  **Autenticazione**: Sistema di registrazione e login sicuro
-  **Classifica Dinamica**: Ordinamento automatico per punti, differenza reti e gol segnati
-  **Gestione Risultati**: Inserimento partite con aggiornamento istantaneo delle statistiche
-  **Statistiche Dettagliate**: Partite giocate, gol fatti/subiti, differenza reti
-  **Squadre Custom**: Crea le tue squadre e gestisci i campionati come vuoi
-  **Controllo Proprietà**: Solo chi crea una squadra/partita può modificarla o eliminarla

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

###  Scegli il Campionato
- Dalla Home vedrai il dropdown con Serie A e Serie B
- Seleziona il campionato - la scelta viene salvata

###  Aggiungi Squadre
- Vai al menu "Squadre"
- Clicca " + Aggiungi Squadra"
- Inserisci nome e città (per il campionato selezionato)

###  Aggiungi Risultati
- Dalla Home clicca " Aggiungi Risultato"
- Seleziona squadra casa/trasferta (del campionato attivo)
- Inserisci gol e data
- Salva - la classifica si aggiorna!

###  Modifica e Elimina
- Accanto a ogni squadra/risultato vedi i pulsanti Modifica ed Elimina
- Puoi modificare/eliminare solo ciò che hai creato

###  Visualizza Statistiche
- **Home**: Classifica con Pos | Squadra | Partite | Punti | GF | GS | DR
- **Squadre**: Tabella dettagliata di tutte le squadre (per campionato)
- **Risultati**: Storico di tutte le partite giocate (per campionato)

##  Struttura Progetto

```
tuttocampo/
├── app/
│   ├── blueprints/
│   │   ├── auth.py              (login, registrazione)
│   │   └── main.py              (rotte principali)
│   ├── repositories/
│   │   ├── user_repository.py
│   │   ├── team_repository.py
│   │   ├── match_repository.py
│   │   └── campionato_repository.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html           (con selector campionato)
│   │   ├── teams.html
│   │   ├── add_team.html
│   │   ├── edit_team.html
│   │   ├── add_match.html
│   │   ├── edit_match.html
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
- `campionato` - Campionati (Serie A, Serie B)
- `team` - Squadre (collegate a campionati)
- `match` - Risultati partite (collegate a campionati)
- `team_stats` - Statistiche squadre (aggiornate automaticamente)

Le statistiche si aggiornano automaticamente quando:
-  Aggiungi una squadra → creiamo il record stats
-  Inserisci una partita → aggiorniamo gol fatti/subiti di entrambe
-  Modifichi una partita → ricalcoliamo le differenze
-  Elimini una partita → ripristiniamo i valori originali

**Campionati Pre-caricati:**
Al primo avvio il database contiene:
- Serie A
- Serie B

Ogni squadra è unica per campionato (puoi avere due squadre con lo stesso nome se in campionati diversi).

**Porta 5000 occupata:**
Modifica `tuttocampo/run.py`:
```python
app.run(debug=True, port=5001)
```

##  Note

- Database parte con Serie A e Serie B vuoti - aggiungi squadre manualmente
- Password hashate con Werkzeug
- Session-based authentication con salvataggio campionato selezionato
- Controllo accesso: ogni utente può modificare solo le proprie squadre/partite
- Debug mode attivo (disabilitare in produzione)

---

**Crea il tuo campionato!**