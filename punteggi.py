def calcola_punteggio(dati):
    """
    Calcola il punteggio di un pilota in base ai dati passati dal form.
    dati = dizionario con i valori del form (stringhe 'on' o numeri)
    """

    punteggio = 0.0

    # Posizione finale
    try:
        posizione = int(dati.get("posizione", 0))
    except ValueError:
        posizione = 0

    if posizione > 0:
        # esempio base (posizione = punti inversamente proporzionali)
        base_points = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8,
                       7: 6, 8: 4, 9: 2, 10: 1}
        punteggio += base_points.get(posizione, 0)

        # Bonus vittoria / podio
        if posizione == 1:
            punteggio += 3
        elif posizione in [2, 3]:
            punteggio += 2

    # BONUS
    if dati.get("pole") == "on":
        punteggio += 2
    if dati.get("fastest_lap") == "on":
        punteggio += 1
    if dati.get("driver_day") == "on":
        punteggio += 1
    if dati.get("fastest_pit") == "on":
        punteggio += 2
    if dati.get("last_rows_points") == "on":
        punteggio += 2

    # Posizioni guadagnate
    try:
        griglia = int(dati.get("griglia", posizione))
        if griglia > posizione:  # ha guadagnato posizioni
            punteggio += (griglia - posizione) * 0.5
        elif posizione > griglia:  # ha perso posizioni
            punteggio -= (posizione - griglia) * 0.5
    except ValueError:
        pass

    # MALUS
    if dati.get("squalifica") == "on":
        punteggio -= 5
    if dati.get("dnf") == "on":
        punteggio -= 3
    if dati.get("pen_6") == "on":
        punteggio -= 4
    if dati.get("pen_5") == "on":
        punteggio -= 3
    if dati.get("last_place") == "on":
        punteggio -= 2
    if dati.get("no_q1") == "on":
        punteggio -= 1

    return punteggio
