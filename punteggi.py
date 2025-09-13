def calcola_punteggio(dati):
    punti = 0

    def is_checked(val):
        return val is not None

    # Bonus
    if is_checked(dati.get("pole")): punti += 2
    if is_checked(dati.get("fastest_lap")): punti += 1
    if is_checked(dati.get("driver_day")): punti += 1
    if is_checked(dati.get("fastest_pit")): punti += 2
    if is_checked(dati.get("back_to_points")): punti += 2
    punti += 0.5 * int(dati.get("pos_gain", 0) or 0)
    if is_checked(dati.get("win")): punti += 3
    if is_checked(dati.get("podium")): punti += 2

    # Malus
    if is_checked(dati.get("dsq")): punti -= 5
    if is_checked(dati.get("dnf")): punti -= 3
    if is_checked(dati.get("pen_6")): punti -= 4
    if is_checked(dati.get("pen_5")): punti -= 3
    if is_checked(dati.get("last")): punti -= 2
    if is_checked(dati.get("q1")): punti -= 1
    punti -= 0.5 * int(dati.get("pos_lost", 0) or 0)

    return punti
