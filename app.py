from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dizionario per memorizzare i punteggi
punteggi = {}

# Squadre e piloti (modifica i nomi se vuoi)
squadre = {
    "Alfarumeno": ["Pilota 1", "Pilota 2"],
    "WC in Geriatria": ["Pilota 1", "Pilota 2"],
    "Strolling Around": ["Pilota 1", "Pilota 2"],
    "Spartaboyz": ["Pilota 1", "Pilota 2"],
    "Vodkaredbull": ["Pilota 1", "Pilota 2"]
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inserisci", methods=["GET", "POST"])
def inserisci():
    global punteggi
    if request.method == "POST":
        punteggi = {}

        for team, piloti in squadre.items():
            team_score = 0
            for i, pilota in enumerate(piloti, start=1):
                griglia = int(request.form.get(f"{team}_p{i}_griglia", 0))
                arrivo = int(request.form.get(f"{team}_p{i}_arrivo", 0))
                sprint = request.form.get(f"{team}_p{i}_sprint", "No")
                bonus = int(request.form.get(f"{team}_p{i}_bonus", 0))
                malus = int(request.form.get(f"{team}_p{i}_malus", 0))

                # Calcolo punteggio
                punti = 0
                # Punti per posizione finale
                if arrivo == 1:
                    punti += 25
                elif arrivo == 2:
                    punti += 18
                elif arrivo == 3:
                    punti += 15
                elif arrivo == 4:
                    punti += 12
                elif arrivo == 5:
                    punti += 10
                elif arrivo == 6:
                    punti += 8
                elif arrivo == 7:
                    punti += 6
                elif arrivo == 8:
                    punti += 4
                elif arrivo == 9:
                    punti += 2
                elif arrivo == 10:
                    punti += 1

                # Bonus/malus posizioni
                if griglia > 0 and arrivo > 0:
                    posizioni_guadagnate = griglia - arrivo
                    if posizioni_guadagnate > 0:
                        punti += posizioni_guadagnate * 0.5
                    elif posizioni_guadagnate < 0:
                        punti += posizioni_guadagnate * 0.5  # penalità (-0.5 per posizione persa)

                # Sprint race
                if sprint == "Si":
                    punti += 3

                # Bonus e malus manuali
                punti += bonus
                punti -= malus

                team_score += punti

            punteggi[team] = team_score

        return redirect(url_for("risultati"))

    return render_template("inserisci.html", squadre=squadre.keys())

@app.route("/risultati")
def risultati():
    # Ordina i team in base ai punteggi
    classifica = sorted(punteggi.items(), key=lambda x: x[1], reverse=True)
    return render_template("risultati.html", classifica=classifica)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
