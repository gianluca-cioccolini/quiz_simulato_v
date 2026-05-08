import pandas as pd

data = {
    "Numero": list(range(1, 11)),
    "Domanda": [
        "Un collaboratore ti chiede di rivedere un suo report urgente, ma hai già molti impegni. Cosa fai?",
        "Durante una riunione il tuo capo ti critica duramente davanti a tutti. Come reagisci?",
        "Un cliente importante si lamenta di un ritardo nella consegna di cui non sei responsabile. Cosa fai?",
        "Il tuo team non rispetta una scadenza importante. Come gestisci la situazione?",
        "Ti viene assegnato un progetto che ritieni al di sopra delle tue competenze attuali. Come agisci?",
        "Un collega prende il merito per un lavoro che hai fatto tu. Cosa fai?",
        "Devi comunicare una notizia negativa a un cliente. Come la gestisci?",
        "Hai ricevuto feedback contrastanti da due superiori su come gestire un problema. Cosa fai?",
        "Ti accorgi di aver commesso un errore che ha causato un problema lieve. Come ti comporti?",
        "Ti viene chiesto di svolgere un'attività fuori dal tuo ruolo senza compensazione aggiuntiva. Cosa fai?",
    ],
    "Risposta Efficace": [
        "Comunichi le tue priorità attuali, proponi una finestra temporale realistica e offri supporto parziale se possibile.",
        "Rimani calmo, ascolti il feedback senza difenderti eccessivamente e chiedi un colloquio privato per approfondire.",
        "Ti scusi per l'inconveniente, spieghi la situazione, e proponi soluzioni concrete per rimediare.",
        "Analizzi le cause del ritardo con il team, riorganizzate le priorità e comunicate tempestivamente lo stato ai stakeholder.",
        "Accetti il progetto esprimendo entusiasmo, identifichi le lacune e pianifichi come colmarle chiedendo supporto.",
        "Parli direttamente con il collega in privato, spieghi come ti senti e chiedete come gestire insieme il riconoscimento.",
        "Comunichi la notizia con empatia, senza minimizzare, spiegando le cause e presentando soluzioni immediate.",
        "Chiedi chiarezza ai due superiori insieme o separatamente, condividi i feedback ricevuti e cerca allineamento.",
        "Ammetti subito l'errore, ti scusi con chi è coinvolto e proponi un piano di correzione rapido.",
        "Esprimi disponibilità ma chiedi chiarezza sulle aspettative future, i tempi e l'impatto sulle tue responsabilità.",
    ],
    "Risposta Mediamente Efficace": [
        "Accetti di aiutarlo subito mettendo da parte il tuo lavoro, sperando di recuperare in seguito.",
        "Rispondi in modo difensivo durante la riunione cercando di spiegare il tuo punto di vista.",
        "Trasferisci il cliente al responsabile della logistica senza ulteriori spiegazioni.",
        "Aumenti il controllo con check giornalieri e reportistica più frequente per recuperare i tempi.",
        "Accetti silenziosamente senza dire nulla, cercando di arrangiarti con le risorse che hai.",
        "Ne parli ad altri colleghi per trovare solidarietà senza affrontare direttamente la situazione.",
        "Invii una mail formale con i dettagli del problema lasciando al cliente il compito di interpretare.",
        "Segui il consiglio del superiore più anziano senza confrontarti ulteriormente.",
        "Aspetti che qualcuno se ne accorga e poi ti scusi quando te lo fanno notare.",
        "Fai il lavoro senza commentare per non creare tensioni, valutando se lamentarti dopo.",
    ],
    "Risposta Non Efficace": [
        "Rifiuti seccamente senza spiegazioni perché hai il tuo da fare.",
        "Ti arrabbi visibilmente e rispondi in modo aggressivo difendendo il tuo operato.",
        "Dai la colpa apertamente al team di logistica davanti al cliente.",
        "Ignori il problema sperando che il team recuperi autonomamente senza intervenire.",
        "Declines il progetto dicendo che non sei qualificato e suggerisci qualcun altro.",
        "Non dici nulla e accumuli risentimento verso il collega senza prendere alcuna iniziativa.",
        "Minimizzi il problema e dici al cliente che non è poi così grave.",
        "Ignori entrambi i feedback e agisci come ritieni più opportuno senza comunicarlo.",
        "Nascondi l'errore sperando che non venga scoperto.",
        "Rifiuti l'incarico in modo brusco dicendo che non è compito tuo.",
    ],
}

df = pd.DataFrame(data)
df.to_excel("domande_esempio.xlsx", index=False)
print("✅ File 'domande_esempio.xlsx' creato con 10 domande di esempio.")
