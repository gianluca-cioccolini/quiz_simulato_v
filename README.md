# Quiz Simulator 🎓

Applicazione desktop per simulare quiz da file Excel, con modalità Quiz e Modalità Studio.

---

## Struttura del file Excel

| Colonna 1  | Colonna 2 | Colonna 3         | Colonna 4                  | Colonna 5            |
|------------|-----------|-------------------|----------------------------|----------------------|
| Numero     | Domanda   | Risposta Efficace | Risposta Mediamente Efficace | Risposta Non Efficace |

- **Riga 1**: intestazione (ignorata automaticamente)
- Il numero di colonne deve essere esattamente 5
- Le risposte vengono mescolate in ordine casuale ad ogni domanda

---

## Punteggio

| Risposta             | Punti |
|----------------------|-------|
| Efficace             | 1.0   |
| Mediamente efficace  | 0.5   |
| Non efficace         | 0.0   |

---

## Modalità

### 🏆 Quiz
- Scegli una risposta tra le tre (in ordine casuale)
- Dopo ogni risposta vedi subito il feedback con la classificazione delle 3 risposte

### 📖 Modalità Studio
- Vedi subito le 3 risposte classificate senza dover scegliere
- Ideale per memorizzare le risposte corrette

---

## Come usare

### Eseguire da sorgente

```bash
# 1. Installa dipendenze
pip install pandas openpyxl

# 2. (Opzionale) Crea file Excel di esempio
python crea_esempio.py

# 3. Avvia l'applicazione
python quiz_app.py
```

### Creare l'eseguibile standalone

```bash
# Installa PyInstaller
pip install pyinstaller

# Genera l'eseguibile
python build.py
```

L'eseguibile verrà creato nella cartella `dist/`:
- **Linux**: `dist/QuizSimulator`
- **Windows**: `dist/QuizSimulator.exe`

> **Nota**: per creare l'eseguibile Windows devi eseguire il build su una macchina Windows.
> Per Linux, esegui su Linux. PyInstaller crea eseguibili nativi per la piattaforma corrente.

---

## Requisiti

- Python 3.9+
- `pandas`
- `openpyxl`
- `tkinter` (incluso in Python standard su Windows e Linux)
- `` (solo per creare l'eseguibile)

---

## Funzionalità

- ✅ Caricamento file `.xlsx` con file picker
- ✅ Scelta del numero di domande
- ✅ Ordine delle risposte casuale ad ogni domanda
- ✅ Feedback immediato dopo ogni risposta
- ✅ Punteggio in tempo reale
- ✅ Barra di progresso
- ✅ Schermata risultati con statistiche
- ✅ Revisione di tutte le risposte date
- ✅ Modalità Studio (risposta mostrata subito)
- ✅ Tema scuro moderno
- ✅ Eseguibile standalone (nessun Python richiesto)
