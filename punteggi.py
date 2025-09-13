def calcola_punteggio(risultato):
    """
    risultato = dizionario con info sul pilota
    esempio:
    {
        "posizione": 1, "sprint": False,
        "pole": False, "fastest_lap": False,
        "driver_of_the_day": False, "fastest_pitstop": False,
        "posizioni_guadagnate": 0, "posizioni_perse": 0,
        "dnf": False, "squalifica": False,
        "penalita_grave": False, "penalita_leggera": False,
        "ultimo": False, "podio": False, "vittoria": False
    }
    """

    punti = 0

    # Punti base GP
    base_points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
    if not risultato.get("sprint", False) and risultato["posizione"] <= 10:
        punti += base_points[risultato["posizione"] - 1]

    # Punti base Sprint
    sprint_points = [8, 7, 6, 5, 4, 3, 2, 1]
    if risultato.get("sprint", False) and risultato["posizione"] <= 8:
        punti += sprint_points[risultato["posizione"] - 1]

    # --- BONUS ---
    if risultato.get("pole", False):
        punti += 2
    if risultato.get("fastest_lap", False):
        punti += 1
    if risultato.get("driver_of_the_day", False):
        punti += 1
    if risultato.get("fastest_pitstop", False):
        punti += 2
    if risultato.get("posizioni_guadagnate", 0) > 0:
        punti += 0.5 * risultato["posizioni_guadagnate"]
    if risultato.get("vittoria", False) and not risultato.get("sprint", False):
        punti += 3
    if risultato.get("podio", False) and not risultato.get("sprint", False):
        punti += 2

    # --- MALUS ---
    if risultato.get("squalifica", False):
        punti -= 5
    if risultato.get("dnf", False):
        punti -= 3
    if risultato.get("penalita_grave", False):
        punti -= 4
    if risultato.get("penalita_leggera", False):
        punti -= 3
    if risultato.get("ultimo", False):
        punti -= 2
    if risultato.get("posizioni_perse", 0) > 0 and not risultato.get("dnf", False):
        punti -= 0.5 * risultato["posizioni_perse"]

    return punti
