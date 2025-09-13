def calcola_punteggio(posizione, sprint, pole, dnf):
    # Base points (GP o Sprint)
    base_gp = [25,18,15,12,10,8,6,4,2,1]
    base_sprint = [8,7,6,5,4,3,2,1]

    punti = 0

    if dnf:
        return -3  # malus DNF

    if sprint:
        if posizione <= len(base_sprint):
            punti += base_sprint[posizione-1]
    else:
        if posizione <= len(base_gp):
            punti += base_gp[posizione-1]

    if pole:
        punti += 2  # bonus pole

    return punti
