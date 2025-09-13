def calcola_punteggio(dati):
    punti = 0

    # Bonus
    if dati.get("pole"): punti += 2
    if dati.get("fastest_lap"): punti += 1
    if dati.get("driver_day"): punti += 1
    if dati.get("fastest_pit"): punti += 2
    if dati.get("back_to_points"): punti += 2
    punti += 0.5 * int(dati.get("pos_gain", 0))
    if dati.get("win"): punti += 3
    if dati.get("podium"): punti += 2

    # Malus
    if dati.get("dsq"): punti -= 5
    if dati.get("dnf"): punti -= 3
    if dati.get("pen_6"): punti -= 4
    if dati.get("pen_5"): punti -= 3
    if dati.get("last"): punti -= 2
    if dati.get("q1"): punti -= 1
    punti -= 0.5 * int(dati.get("pos_lost", 0))

    return punti
