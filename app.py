<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>Inserisci risultati della giornata</title>
</head>
<body>
    <h1>Inserisci risultati della giornata</h1>

    <form method="POST">
        <label for="squadra">Seleziona squadra:</label>
        <select name="squadra" id="squadra" required>
            <option value="Alfarumeno">Alfarumeno</option>
            <option value="Stalloni">Stalloni</option>
            <option value="WC in Geriatria">WC in Geriatria</option>
            <option value="Strolling Around">Strolling Around</option>
            <option value="Spartaboyz">Spartaboyz</option>
            <option value="Vodkaredbull">Vodkaredbull</option>
        </select>

        <h2>Pilota 1</h2>
        <label>Posizione partenza: <input type="number" name="partenza1" min="1" max="20"></label><br>
        <label>Posizione arrivo: <input type="number" name="arrivo1" min="0" max="20"></label><br>
        <label><input type="checkbox" name="giro_veloce1"> Giro veloce</label><br>
        <label><input type="checkbox" name="ritiro1"> Ritiro</label><br>
        <label><input type="checkbox" name="sprint1"> Sprint</label><br>

        <h2>Pilota 2</h2>
        <label>Posizione partenza: <input type="number" name="partenza2" min="1" max="20"></label><br>
        <label>Posizione arrivo: <input type="number" name="arrivo2" min="0" max="20"></label><br>
        <label><input type="checkbox" name="giro_veloce2"> Giro veloce</label><br>
        <label><input type="checkbox" name="ritiro2"> Ritiro</label><br>
        <label><input type="checkbox" name="sprint2"> Sprint</label><br>

        <br>
        <button type="submit">Salva risultati</button>
    </form>

    <br>
    <a href="{{ url_for('index') }}">Torna alla home</a>
</body>
</html>
