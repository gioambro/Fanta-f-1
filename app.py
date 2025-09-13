from flask import Flask, render_template, request
import json, os, logging, traceback

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

STORICO_FILE = "storico.json"

# --- Funzione che calcola il punteggio di un singolo pilota ---
def calcola_punteggio_pilota(d):
    """
    d è un dict con:
      - pos (int or None)
      - griglia (int or None)
      - sprint (bool)
      - pole, fastest_lap, driver_day, fastest_pit, last_rows_points (bool)
      - win, podium (bool)
      - dsq, dnf, pen_6, pen_5, last_place, no_q1 (bool)
      - pos_gain (int), pos_loss (int)
    """
    punti = 0.0

    # converti valori (se passati come stringhe)
    pos = d.get("pos")
    sprint = d.get("sprint", False)

    # punti base (gara normale top10)
    punti_classifica = [25,18,15,12,10,8,6,4,2,1]
    # punti sprint top8
    punti_sprint = [8,7,6,5,4,3,2,1]

    if pos and isinstance(pos, int):
        if sprint:
            if pos <= len(punti_sprint):
                punti += punti_sprint[pos-1]
        else:
            if pos <= len(punti_classifica):
                punti += punti_classifica[pos-1]

    # bonus fissi
    if d.get("pole"): punti += 2
    if d.get("fastest_lap"): punti += 1
    if d.get("driver_day"): punti += 1
    if d.get("fastest_pit"): punti += 2
    if d.get("last_rows_points"): punti += 2

    # posizioni guadagnate (0.5 per posizione guadagnata)
    pos_gain = int(d.get("pos_gain") or 0)
    punti += 0.5 * pos_gain

    # vittoria/podio non valgono nelle sprint
    if not sprint:
        if d.get("win"): punti += 3
        if d.get("podium"): punti += 2

    # malus
    if d.get("dsq"): punti -= 5
    if d.get("dnf"): punti -= 3
    if d.get("pen_6"): punti -= 4
    if d.get("pen_5"): punti -= 3
    if d.get("last_place"): punti -= 2
    if d.get("no_q1"): punti -= 1

    # posizioni perse (malus 0.5 per posizione persa)
    pos_loss = int(d.get("pos_loss") or 0)
    punti -= 0.5 * pos_loss

    # arrotonda a 1 cifra decimale
    return round(punti, 1)


# --- funzioni file storico ---
def carica_storico():
    if os.path.exists(STORICO_FILE):
        try:
            with open(STORICO_FILE, "r") as f:
                return json.load(f)
        except Exception:
            app.logger.exception("Errore caricamento storico.json, reimposto lista vuota")
            return []
    return []

def salva_storico(storico):
    try:
        with open(STORICO_FILE, "w") as f:
            json.dump(storico, f, indent=2)
    except Exception:
        app.logger.exception("Errore scrittura storico.json")


# --- home (col link per inserire risultati) ---
@app.route("/")
def home():
    return render_template("home.html")


# --- inserimento risultati (form) ---
@app.route("/inserisci", methods=["GET", "POST"])
def inserisci():
    try:
        if request.method == "POST":
            # carica storico esistente
            storico = carica_storico()
            giornata_n = len(storico) + 1

            # calcola punteggi per ogni giocatore
            punteggi_giornata = {}
            for g in range(1, 7):  # giocatori 1..6
                totale_giocatore = 0.0
                # due piloti per giocatore
                for p in range(1, 3):
                    prefix = f"g{g}_p{p}_"
                    # leggi valori dal form in modo sicuro
                    try:
                        pos_raw = request.form.get(prefix + "pos")
                        pos = int(pos_raw) if pos_raw and pos_raw.strip() != "" else None
                    except:
                        pos = None

                    try:
                        griglia_raw = request.form.get(prefix + "griglia")
                        griglia = int(griglia_raw) if griglia_raw and griglia_raw.strip() != "" else None
                    except:
                        griglia = None

                    sprint = request.form.get(prefix + "sprint") == "on"
                    # booleani per checkbox
                    def chk(name): return request.form.get(prefix + name) == "on"

                    # lettura pos_gain/pos_loss se il JS li ha riempiti come hidden; altrimenti li calcolo qui
                    try:
                        pos_gain = int(request.form.get(prefix + "pos_gain") or 0)
                    except:
                        pos_gain = 0
                    try:
                        pos_loss = int(request.form.get(prefix + "pos_loss") or 0)
                    except:
                        pos_loss = 0

                    # se pos e griglia presenti -> ricalcolo server-side per sicurezza
                    if pos and griglia:
                        if pos < griglia:
                            pos_gain = griglia - pos
                            pos_loss = 0
                        elif pos > griglia:
                            pos_gain = 0
                            pos_loss = pos - griglia
                        else:
                            pos_gain = 0
                            pos_loss = 0
                    else:
                        # se non ci sono dati -> lascia 0
                        pos_gain = pos_gain or 0
                        pos_loss = pos_loss or 0

                    dati_pilota = {
                        "pos": pos,
                        "griglia": griglia,
                        "sprint": sprint,
                        "pole": chk("pole"),
                        "fastest_lap": chk("fastest_lap"),
                        "driver_day": chk("driver_day"),
                        "fastest_pit": chk("fastest_pit"),
                        "last_rows_points": chk("last_rows_points"),
                        "win": chk("win"),
                        "podium": chk("podium"),
                        "dsq": chk("dsq"),
                        "dnf": chk("dnf"),
                        "pen_6": chk("pen_6"),
                        "pen_5": chk("pen_5"),
                        "last_place": chk("last_place"),
                        "no_q1": chk("no_q1"),
                        "pos_gain": pos_gain,
                        "pos_loss": pos_loss
                    }

                    # Se non ci sono informazioni per questo pilota -> punteggio 0 (non si somma)
                    has_data = any([
                        dati_pilota["pos"] is not None,
                        dati_pilota["pole"],
                        dati_pilota["fastest_lap"],
                        dati_pilota["driver_day"],
                        dati_pilota["fastest_pit"],
                        dati_pilota["last_rows_points"],
                        dati_pilota["dsq"],
                        dati_pilota["dnf"]
                    ])

                    if has_data:
                        punti_p = calcola_punteggio_pilota(dati_pilota)
                        totale_giocatore += punti_p
                    else:
                        # pilota non inserito -> 0 punti (non si tocca totale)
                        pass

                # salva punteggio totale del giocatore
                punteggi_giornata[f"Giocatore {g}"] = round(totale_giocatore, 1)

            # aggiungi allo storico in formato dict semplice
            record_giornata = {"giornata": giornata_n}
            record_giornata.update(punteggi_giornata)
            storico.append(record_giornata)
            salva_storico(storico)

            # calcola classifica generale
            totali = {f"Giocatore {i}": 0.0 for i in range(1,7)}
            for rec in storico:
                for i in range(1,7):
                    totali[f"Giocatore {i}"] += float(rec.get(f"Giocatore {i}", 0) or 0)

            # ordina classifica generale (discendente)
            classifica_generale = sorted(totali.items(), key=lambda x: x[1], reverse=True)

            # ordina classifica giornata (lista di tuple per visualizzare in ordine giocatore 1..6)
            classifica_giornata = [(g, punteggi_giornata[g]) for g in sorted(punteggi_giornata.keys())]

            return render_template("risultato.html",
                                   giornata_n=giornata_n,
                                   classifica_giornata=classifica_giornata,
                                   classifica_generale=classifica_generale)
        else:
            # GET -> mostra form
            return render_template("inserisci.html")
    except Exception as e:
        app.logger.exception("Errore durante POST /inserisci")
        # mostra pagina di errore minimale così non ricadi in altro errore di template
        tb = traceback.format_exc()
        return f"<h1>Errore interno</h1><pre>{tb}</pre>", 500


# --- pagina classifica (opzionale) ---
@app.route("/classifica")
def classifica():
    storico = carica_storico()
    totali = {f"Giocatore {i}": 0.0 for i in range(1,7)}
    for rec in storico:
        for i in range(1,7):
            totali[f"Giocatore {i}"] += float(rec.get(f"Giocatore {i}", 0) or 0)
    classifica_generale = sorted(totali.items(), key=lambda x: x[1], reverse=True)
    return render_template("classifica.html", classifica_generale=classifica_generale)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
