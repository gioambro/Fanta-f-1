from flask import Flask, render_template, request

app = Flask(__name__)

# Giocatori e punteggi iniziali (dopo 16 gare)
giocatori = ["Alfarumeno", "Stalloni", "WC in Geriatria", "Strolling Around", "Spartaboyz", "Vodkaredbull"]
classifica_generale = {
    "Alfarumeno": 12,
    "Stalloni": 10,
    "WC in Geriatria": 10,
    "Strolling Around": 5,
    "Spartaboyz": 5,
    "Vodkaredbull": 2
}
giornata_n = 17  # si riparte dalla gara 17

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

                # --- Posizione in gara ---
                if pos and pos.isdigit():
                    pos = int(pos)

                    punti_pos = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}
                    punteggi_giornata[g] += punti_pos.get(pos, 0)

                    # Bonus vittoria/podio
                    if pos == 1 or request.form.get(f"{g}_p{p}_vittoria"):
                        punteggi_giornata[g] += 3
                    if pos in [2, 3] or request.form.get(f"{g}_p{p}_podio"):
                        punteggi_giornata[g] += 2

                    # Bonus aggiuntivi
                    if request.form.get(f"{g}_p{p}_pole"):
                        punteggi_giornata[g] += 2
                    if request.form.get(f"{g}_p{p}_fastlap"):
                        punteggi_giornata[g] += 1
                    if request.form.get(f"{g}_p{p}_dotd"):
                        punteggi_giornata[g] += 1
                    if request.form.get(f"{g}_p{p}_pitstop"):
                        punteggi_giornata[g] += 2

                    # Posizioni guadagnate/perse
                    if griglia and griglia.isdigit():
                        griglia = int(griglia)
                        diff = griglia - pos
                        punteggi_giornata[g] += diff * 0.5

                # --- Sprint ---
                if sprint_pos and sprint_pos.isdigit():
                    sprint_pos = int(sprint_pos)
                    sprint_points = {1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1}
                    punteggi_giornata[g] += sprint_points.get(sprint_pos, 0)

                # --- Malus ---
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

        # aggiorna la classifica generale
        for g in giocatori:
            classifica_generale[g] += punteggi_giornata[g]

        giornata_n += 1
        return render_template(
            "risultato.html",
            classifica_giornata=punteggi_giornata,
            classifica_generale=classifica_generale,
            giornata=giornata_n - 1
        )

    return render_template("inserisci.html", giocatori=giocatori)

if __name__ == "__main__":
    app.run(debug=True)
