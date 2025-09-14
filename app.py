from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Punteggi base GP
punti_gp = {
    1: 25, 2: 18, 3: 15, 4: 12, 5: 10,
    6: 8, 7: 6, 8: 4, 9: 2, 10: 1
}

# Punteggi Sprint (se la sprint è attiva per quel pilota)
punti_sprint = {1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1}

# Classifica iniziale (nomi e punti che mi hai indicato)
classifica = {
    "Alfarumeno": 12,
    "Stalloni": 10,
    "WC in Geriatria": 10,
    "Strolling Around": 5,
    "Spartaboyz": 5,
    "Vodkaredbull": 2
}

# Archivio risultati (in memoria)
risultati = []

def to_int_safe(x):
    try:
        return int(x)
    except (TypeError, ValueError):
        return 0

@app.route("/")
def index():
    # ordiniamo i giocatori sempre nello stesso ordine
    players = list(classifica.keys())
    return render_template("index.html", classifica=classifica, players=players)

@app.route("/inserisci")
def inserisci():
    players = list(classifica.keys())
    return render_template("inserisci.html", players=players)

@app.route("/salva", methods=["POST"])
def salva():
    players = list(classifica.keys())
    giornata_record = []  # dettagli sulla giornata per mostrare in risultati

    # Per ogni giocatore prendo i 2 piloti
    for i, player in enumerate(players):
        total_player_points = 0.0
        pilots_info = []
        for p in (1, 2):
            prefix = f"p{i}_pilot{p}_"

            pilota_nome = request.form.get(prefix + "name", f"Pilota{p}")
            griglia = to_int_safe(request.form.get(prefix + "griglia"))
            posizione = to_int_safe(request.form.get(prefix + "posizione"))
            sprint = request.form.get(prefix + "sprint", "no")
            sprint_pos = to_int_safe(request.form.get(prefix + "sprint_pos")) if sprint == "si" else 0

            punti = 0.0

            # Punti GP (solo se posizione è tra 1-10)
            if posizione in punti_gp:
                punti += punti_gp[posizione]

            # Punti Sprint (se selezionato)
            if sprint == "si" and sprint_pos in punti_sprint:
                punti += punti_sprint[sprint_pos]

            # Bonus (tutti fields sono "si" o "no")
            if request.form.get(prefix + "pole") == "si":
                punti += 2
            if request.form.get(prefix + "fastest_lap") == "si":
                punti += 1
            if request.form.get(prefix + "driver_day") == "si":
                punti += 1
            if request.form.get(prefix + "fastest_pit") == "si":
                punti += 2
            if request.form.get(prefix + "rimonta") == "si":
                punti += 2

            # Posizioni guadagnate (automatico): se posizione < griglia
            if griglia and posizione and posizione < griglia:
                guadagnate = griglia - posizione
                punti += 0.5 * guadagnate

            # Vittoria/Podio: calcolati automaticamente sul risultato del GP (non su sprint)
            # Vittoria: +3, Podio (2°/3°): +2 ; non valgono per la sprint (sono inerenti al GP)
            if posizione == 1:
                punti += 3
            elif posizione in (2, 3):
                punti += 2

            # Malus
            dnf = request.form.get(prefix + "dnf") == "si"
            if request.form.get(prefix + "squalifica") == "si":
                punti -= 5
            if dnf:
                punti -= 3
            if request.form.get(prefix + "pen6") == "si":
                punti -= 4
            if request.form.get(prefix + "pen5") == "si":
                punti -= 3
            if request.form.get(prefix + "last_place") == "si":
                # se dnf è sì, per regola il malus "ultimo in gara" **non** si applica a chi non finisce
                if not dnf:
                    punti -= 2
            if request.form.get(prefix + "q1") == "si":
                punti -= 1

            # Posizioni perse: solo se non DNF
            if griglia and posizione and posizione > griglia and not dnf:
                perse = posizione - griglia
                punti -= 0.5 * perse

            # arrotonda a 2 decimali per sicurezza
            punti = round(punti, 2)
            total_player_points += punti

            pilots_info.append({
                "nome": pilota_nome,
                "griglia": griglia,
                "posizione": posizione,
                "sprint": sprint_pos if sprint == "si" else None,
                "punti": punti,
                "dnf": dnf
            })

        # aggiorna classifica (somma punti dei 2 piloti)
        classifica[player] = round(classifica.get(player, 0) + total_player_points, 2)

        # salva il record della giornata per questo giocatore
        giornata_record.append({
            "giocatore": player,
            "punti_totali": round(total_player_points, 2),
            "piloti": pilots_info
        })

    # memorizza la giornata (append completo)
    risultati.append({
        "giornata": len(risultati) + 1,
        "dettagli": giornata_record
    })

    return redirect(url_for("risultati_page"))

@app.route("/risultati")
def risultati_page():
    return render_template("risultati.html", risultati=risultati, classifica=classifica)

if __name__ == "__main__":
    app.run(debug=True)
