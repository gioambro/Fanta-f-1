def calcola_punteggio(risultato):
    """
    risultato = dizionario con info sul pilota
    esempio:
    {"posizione": 1, "sprint": False, "pole": True, "dnf": False}
    """

    punti = 0

    # punti base GP (no sprint)
    base_points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
    if not risultato.get("sprint", False) and risultato["posizione"] <= 10:
        punti += base_points[risultato["posizione"] - 1]

    # punti base Sprint
    sprint_points = [8, 7, 6, 5, 4, 3, 2, 1]
    if risultato.get("sprint", False) and risultato["posizione"] <= 8:
        punti += sprint_points[risultato["posizione"] - 1]

    # bonus pole
    if risultato.get("pole", False):
        punti += 2

    # malus DNF
    if risultato.get("dnf", False):
        punti -= 3

    return punti
