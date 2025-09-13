from flask import Flask, render_template, request

app = Flask(__name__)

# Variabili globali
classifiche_giornate = []
classifica_generale = {f"Giocatore {i}": 0 for i in range(1, 7)}

# ----------------------------
# FUNZIONI DI CALCOLO
# ----------------------------
def calcola_sprint(posizione):
    """Restituisce i punti Sprint in base alla posizione"""
    punti_sprint = {1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1}
    return punti_sprint.get(posizione, 0)

def calcola_punteggio(dati):
    """Calcola i punti GP + Sprint"""
    punti = 0

    # --- Posizione finale GP ---
    pos = dati.get("posizione")
    if pos:
        pos = int(pos)
        if pos == 1:
            punti += 3   # Vittoria
        elif pos in [2, 3]:
            punti += 2   # Podio

    # --- Bonus vari ---
    if dati.get("pole"): punti += 2
    if dati.get("fastest_lap"): punti += 1
    if dati.get("driver_day"): punti += 1
    if dati.get("fastest_pit"): punti += 2

    # --- Malus ---
    if dati.get("dnf"): punti -= 3
    if dati.get("squalifica"): punti -= 5
    if dati.get("pen_6"): punti -= 4
    if dati.get("pen_5"): punti -= 3
    if dati.get("ultimo"): punti -= 2
    if dati.get("no_q1"): punti -= 1

    # --- Posizioni guadagnate/perse ---
    griglia = dati.get("griglia")
    if pos and griglia:
        griglia = int(griglia)
        delta = griglia - pos
        if delta > 0:   # guadagnate
            punti += 0.5 * delta
        elif delta < 0: # perse
            punti += 0.5 * abs(delta)

    # --- Sprint ---
    sprint_flag = dati.get("sprint_flag")
    sprint_pos = dati.get("sprint_pos")
    if sprint_flag == "si" and sprint_pos:
        punti += calcola_sprint(int(sprint_pos))

    return punti

# ----------------------------
# ROUTES
# ----------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/inserisci", methods=["GET", "POST"])
def inserisci():
    global classifiche_giornate, classifica_generale

    if request.method == "POST":
        classifica_giornata = {}

        for g in range(1, 7):
            dati = {
                "posizione": request.form.get(f"g{g}_pos"),
                "griglia": request.form.get(f"g{g}_griglia"),
                "pole": request.form.get(f"g{g}_pole"),
                "fastest_lap": request.form.get(f"g{g}_fastest_lap"),
                "driver_day": request.form.get(f"g{g}_driver_day"),
                "fastest_pit": request.form.get(f"g{g}_fastest_pit"),
                "dnf": request.form.get(f"g{g}_dnf"),
                "squalifica": request.form.get(f"g{g}_squalifica"),
                "pen_6": request.form.get(f"g{g}_pen_6"),
                "pen_5": request.form.get(f"g{g}_pen_5"),
                "ultimo": request.form.get(f"g{g}_ultimo"),
                "no_q1": request.form.get(f"g{g}_no_q1"),
                "sprint_flag": request.form.get(f"g{g}_sprint_flag"),
                "sprint_pos": request.form.get(f"g{g}_sprint_pos")
            }

            punti = calcola_punteggio(dati)
            giocatore = f"Giocatore {g}"
            classifica_giornata[giocatore] = punti
            classifica_generale[giocatore] += punti

        classifiche_giornate.append(classifica_giornata)

        return render_template(
            "risultato.html",
            giornata_n=len(classifiche_giornate),
            classifica_giornata=classifica_giornata,
            classifica_generale=classifica_generale
        )

    return render_template("inserisci.html")

@app.route("/classifica")
def classifica():
    return render_template("classifica.html", classifica_generale=classifica_generale)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
