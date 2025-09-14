from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Giocatori con punteggi accumulati finora
giocatori = ["Alfarumeno", "Stalloni", "WC in Geriatria", "Strolling Around", "Spartaboyz", "Vodkaredbull"]
classifica_generale = {
    "Alfarumeno": 12,
    "Stalloni": 10,
    "WC in Geriatria": 10,
    "Strolling Around": 5,
    "Spartaboyz": 5,
    "Vodkaredbull": 2
}
giornata_n = 17  # ripartiamo dalla prossima gara

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inserisci", methods=["GET", "POST"])
def inserisci():
    global giornata_n
    if request.method == "POST":
        punteggi_giornata = {g: 0 for g in giocatori}

        for g in giocatori:
            for p in [1, 2]:
                pos = request.form.get(f"{g}_p{p}_pos")
                griglia = request.form.get(f"{g}_p{p}_griglia")
                sprint_pos = request.form.get(f"{g}_p{p}_sprint_pos")

                if pos:
                    pos = int(pos)
                    # Punti posizione (base F1)
                    if pos == 1:
                        punteggi_giornata[g] += 25
                    elif pos == 2:
                        punteggi_giornata[g] += 18
                    elif pos == 3:
                        punteggi_giornata[g] += 15
                    elif pos == 4:
                        punteggi_giornata[g] += 12
                    elif pos == 5:
                        punteggi_giornata[g] += 10
                    elif pos == 6:
                        punteggi_giornata[g] += 8
                    elif pos == 7:
                        punteggi_giornata[g] += 6
                    elif pos == 8:
                        punteggi_giornata[g] += 4
                    elif pos == 9:
                        punteggi_giornata[g] += 2
                    elif pos == 10:
                        punteggi_giornata[g] += 1

                    # Bonus vittoria/podio
                    if request.form.get(f"{g}_p{p}_vittoria"):
                        punteggi_giornata[g] += 3
                    if request.form.get(f"{g}_p{p}_podio"):
                        punteggi_giornata[g] += 2

                    # Bonus standard
                    if request.form.get(f"{g}_p{p}_pole"):
                        punteggi_giornata[g] += 2
                    if request.form.get(f"{g}_p{p}_fastlap"):
                        punteggi_giornata[g] += 1
                    if request.form.get(f"{g}_p{p}_dotd"):
                        punteggi_giornata[g] += 1
                    if request.form.get(f"{g}_p{p}_pitstop"):
                        punteggi_giornata[g] += 2

                    # Posizioni guadagnate/perse
                    if griglia:
                        griglia = int(griglia)
                        diff = griglia - pos
                        if diff > 0:
                            punteggi_giornata[g] += diff * 0.5
                        elif diff < 0:
                            punteggi_giornata[g] += diff * 0.5

                # Sprint
                if sprint_pos:
                    sprint_pos = int(sprint_pos)
                    sprint_points = {1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1}
                    punteggi_giornata[g] += sprint_points.get(sprint_pos, 0)

                # Malus
                if request.form.get(f"{g}_p{p}_squal"):
                    punteggi_giornata[g] -= 5
                if request.form.get(f"{g}_p{p}_dnf"):
                    punteggi_giornata[g] -= 3
                if request.form.get(f"{g}_p{p}_pen6"):
                    punteggi_giornata[g] -= 4
                if request.form.get(f"{g}_p{p}_pen5"):
                    punteggi_giornata[g] -= 3
                if request.form.get(f"{g}_p{p}_ultimo"):
                    punteggi_giornata[g] -= 2
                if request.form.get(f"{g}_p{p}_q1"):
                    punteggi_giornata[g] -= 1

        # aggiorna classifica generale
        for g in giocatori:
            classifica_generale[g] += punteggi_giornata[g]

        giornata_n += 1
        return render_template("risultato.html", classifica_giornata=punteggi_giornata, classifica_generale=classifica_generale, giornata=giornata_n-1)

    return render_template("inserisci.html", giocatori=giocatori)

if __name__ == "__main__":
    app.run(debug=True)
